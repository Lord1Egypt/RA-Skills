
import argparse
import sys
import os
import logging
import yaml
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

sys.path.insert(0, os.path.dirname(__file__))
from auth import auth_google

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler()]
)

def get_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config or {}
    except Exception as e:
        logging.warning(f"Could not read config.yaml: {e}. Using defaults.")
        return {}

config = get_config()
TIMEZONE = config.get('timezone', 'Asia/Bangkok')
LOG_LEVEL = getattr(logging, config.get('log_level', 'INFO').upper(), logging.INFO)
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler()]
)

def create_event(service, title, date, time, duration=60):
    if duration <= 0:
        logging.error(f"duration must be a positive number of minutes, got {duration}")
        raise ValueError(f"duration must be a positive number of minutes, got {duration}")
    start_dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    end_dt = start_dt + timedelta(minutes=duration)
    event = {
        'summary': title,
        'start': {'dateTime': start_dt.isoformat(), 'timeZone': TIMEZONE},
        'end': {'dateTime': end_dt.isoformat(), 'timeZone': TIMEZONE},
    }

    try:
        result = service.events().insert(calendarId='primary', body=event).execute()
        logging.info(f"Event created: {result.get('htmlLink')}")
        print(f"Event created: {result.get('htmlLink')}")
    except HttpError as error:
        logging.error(f'An error occurred: {error}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a Google Calendar event')
    parser.add_argument('--title', required=True, help='Event title')
    parser.add_argument('--date', required=True, help='Date in YYYY-MM-DD format')
    parser.add_argument('--time', required=True, help='Time in HH:MM format')
    parser.add_argument('--duration', type=int, default=60, help='Duration in minutes (default: 60)')
    args = parser.parse_args()

    creds = auth_google()
    service = build('calendar', 'v3', credentials=creds)
    create_event(service, args.title, args.date, args.time, args.duration)
