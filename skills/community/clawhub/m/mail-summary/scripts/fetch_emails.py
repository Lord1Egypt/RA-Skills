import re
import html
import unicodedata
import base64
import sys
import os
import logging
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from auth import auth_google, get_config

MAX_EMAILS = 50
MAX_BODY_LENGTH = 500

config = get_config()
LOG_LEVEL = getattr(logging, config.get('log_level', 'INFO').upper(), logging.INFO)
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler()]
)

def clean_text(text):
    text = html.unescape(text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Cf')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_body(payload):
    if payload.get('mimeType') == 'text/plain':
        data = payload.get('body', {}).get('data', '')
        if data:
            return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    for part in payload.get('parts', []):
        result = extract_body(part)
        if result:
            return result
    return ''

def _parse_date(date_str):
    """Parse RFC 2822 date string; return epoch-aware datetime or datetime.min on failure."""
    if not date_str:
        return datetime.min.replace(tzinfo=timezone.utc)
    try:
        return parsedate_to_datetime(date_str)
    except Exception:
        return datetime.min.replace(tzinfo=timezone.utc)

def fetch_emails(service, max_results=MAX_EMAILS):
    try:
        emails = []
        next_page_token = None
        logging.info("Fetching emails from Gmail API...")

        lookback_hours = int(config.get('lookback_hours', 24))
        lookback_str = f"newer_than:{lookback_hours}h"
        while len(emails) < max_results:
            batch_size = min(max_results - len(emails), 100)
            results = service.users().messages().list(
                userId='me',
                q=lookback_str,
                maxResults=batch_size,
                pageToken=next_page_token
            ).execute()

            messages = results.get('messages', [])
            logging.info(f"Fetched {len(messages)} message headers.")
            for msg in messages:
                msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
                headers = msg_data['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "")
                sender = next((h['value'] for h in headers if h['name'] == 'From'), "")
                date = next((h['value'] for h in headers if h['name'] == 'Date'), "")
                body = clean_text(extract_body(msg_data['payload']))
                if not body:
                    body = clean_text(msg_data.get('snippet', ''))
                if len(body) > MAX_BODY_LENGTH:
                    body = body[:MAX_BODY_LENGTH] + '...'
                emails.append({'subject': subject, 'from': sender, 'date': date, 'body': body})
                logging.info(f"Email: from={sender}, subject={subject}, date={date}")

            next_page_token = results.get('nextPageToken')
            if not next_page_token:
                break

        logging.info(f"Total emails fetched: {len(emails)}")
        return emails

    except HttpError as error:
        logging.error(f'An error occurred: {error}')
        return []

if __name__ == '__main__':
    creds = auth_google()
    service = build('gmail', 'v1', credentials=creds)
    emails = fetch_emails(service)
    emails.sort(key=lambda e: _parse_date(e['date']), reverse=True)
    print(f"Total emails: {len(emails)}")
    print("=" * 60)
    for email in emails:
        print(f"From: {email['from']}")
        print(f"Date: {email['date']}")
        print(f"Subject: {email['subject']}")
        print(f"Body:\n{email['body']}")
        print("=" * 60)
