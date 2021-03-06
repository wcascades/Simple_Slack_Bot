import mysecrets
import logging
import csv
import my_parser

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

TOKEN = mysecrets.slack_token
DEFAULT_CHANNEL = mysecrets.default_slack_channel


def _get_from_address(str):
    return str[str.find("<") + 1:str.find(">")]


def notifyP1(mail, channel=DEFAULT_CHANNEL):
    if _get_from_address(mail["From"]) == mysecrets.ticket_system_email_address:
        message_for_slack = (my_parser.parse_subject_for_slack(mail["Subject"]) +
                             "\n" +
                             "Center ID: " +
                             my_parser.get_cid(mail) +
                             "\n"
                             "Summary: " +
                             my_parser.get_summary(mail))
    else:
        # todo: for testing purposes
        message_for_slack = (my_parser.parse_subject_for_slack(mail["Subject"]) +
                             "\n" +
                             "Center ID: " +
                             my_parser.get_cid(mail) +
                             "\n"
                             "Summary: " +
                             my_parser.get_summary(mail))
    send_slack_message(message_for_slack)


def notifyP2(mail, channel=DEFAULT_CHANNEL):
    notifyP1(mail)


def notifyOnCallUpdate(on_call_phone_num):
    send_slack_message("On call number has been updated! New on call number is " + on_call_phone_num)


def send_slack_message(message, channel=DEFAULT_CHANNEL):
    try:
        client = WebClient(token=TOKEN)
        response = client.chat_postMessage(channel=channel, text=message)
        # assertion errors are being raised when there isn't an issue. Looks like response has an extra
        # return carriage when it gets to a certain length.
        # response["message"]["text"] == message_for_slack
    except SlackApiError as e:
        logging.debug("slackhandler.py:: " + f"Response 'ok' : {e.response['ok']}")
        logging.debug("slackhandler.py:: " + "ERROR: " + e.response["error"])
    except AssertionError as e:
        logging.debug("slackhandler.py:: ASSERTION ERROR")

    logging.debug("slackhandler.py:: " + "message supplied is " + message)


def notify_inform_who_is_on_call(phone_num):
    send_slack_message("The current on call number is " + phone_num)
