import argparse
import sys
import os
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

sys.path.insert(0, os.path.dirname(__file__))
from auth import auth_google

def create_event(service, title, date, time, duration=60):
    start_dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    end_dt = start_dt + timedelta(minutes=duration)

    event = {
        'summary': title,
        'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'Asia/Bangkok'},
        'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'Asia/Bangkok'},
    }

    try:
        result = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {result.get('htmlLink')}")
    except HttpError as error:
        print(f'An error occurred: {error}')

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
