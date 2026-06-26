#!/usr/bin/env python3
import argparse
import json
import os
import sys
from datetime import timedelta

from _common import acquire_token, parse_time_with_tz, graph_headers

import requests

GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def create_event(access_token, subject, attendees_emails, start_dt, duration_min, timezone_name):
    end_dt = start_dt + timedelta(minutes=duration_min)

    attendees = [
        {
            "emailAddress": {"address": e.strip(), "name": e.strip()},
            "type": "required"
        } for e in attendees_emails if e.strip()
    ]

    payload = {
        "subject": subject,
        "body": {
            "contentType": "HTML",
            "content": "This event was created by your AI assistant."
        },
        "start": {
            "dateTime": start_dt.strftime('%Y-%m-%dT%H:%M:%S'),
            "timeZone": timezone_name
        },
        "end": {
            "dateTime": end_dt.strftime('%Y-%m-%dT%H:%M:%S'),
            "timeZone": timezone_name
        },
        "location": {
            "displayName": "Microsoft Teams Meeting"
        },
        "attendees": attendees,
        "allowNewTimeProposals": True,
        "isOnlineMeeting": True,
        "onlineMeetingProvider": "teamsForBusiness"
    }

    url = f"{GRAPH_BASE}/me/events"
    resp = requests.post(url, headers=graph_headers(access_token), data=json.dumps(payload))
    if resp.status_code >= 300:
        print(f"Error creating event: {resp.status_code} {resp.text}")
        sys.exit(1)
    event = resp.json()
    join_link = (event.get('onlineMeeting') or {}).get('joinUrl') or event.get('onlineMeetingUrl')
    return event, join_link


def main():
    parser = argparse.ArgumentParser(description="Create a Microsoft Teams meeting via Graph API")
    parser.add_argument('--title', required=True)
    parser.add_argument('--attendees', default='', help='Comma-separated email list')
    parser.add_argument('--start-time', required=True, help='"YYYY-MM-DD HH:MM" or ISO8601')
    parser.add_argument('--duration-minutes', type=int, default=30)
    parser.add_argument('--timezone', default=None, help='IANA timezone, e.g., Asia/Singapore')
    args = parser.parse_args()

    access_token, cfg = acquire_token()

    tzname = args.timezone or os.environ.get('TZ') or 'UTC'
    start_dt = parse_time_with_tz(args.start_time, tzname)

    attendees_emails = [e.strip() for e in args.attendees.split(',') if e.strip()]

    event, join_link = create_event(access_token, args.title, attendees_emails, start_dt, args.duration_minutes, tzname)

    print(json.dumps({
        "event_id": event.get('id'),
        "subject": event.get('subject'),
        "start": event.get('start'),
        "end": event.get('end'),
        "join_url": join_link,
        "web_link": event.get('webLink'),
        "attendees": event.get('attendees', []),
    }, indent=2))


if __name__ == '__main__':
    main()
