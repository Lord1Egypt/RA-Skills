#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timedelta

from _common import acquire_token, graph_headers
import requests

GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def list_events(access_token, start_dt, end_dt, top):
    params = {
        'startDateTime': start_dt.isoformat(),
        'endDateTime': end_dt.isoformat(),
        '$top': str(top),
        '$orderby': 'start/dateTime',
    }
    url = f"{GRAPH_BASE}/me/calendar/calendarView"
    resp = requests.get(url, headers=graph_headers(access_token), params=params)
    if resp.status_code >= 300:
        raise SystemExit(f"Error listing meetings: {resp.status_code} {resp.text}")
    items = resp.json().get('value', [])
    meetings = []
    for e in items:
        is_online = e.get('isOnlineMeeting') or (e.get('onlineMeeting') is not None) or (e.get('onlineMeetingProvider') == 'teamsForBusiness')
        if is_online:
            join_link = (e.get('onlineMeeting') or {}).get('joinUrl') or e.get('onlineMeetingUrl')
            meetings.append({
                'id': e.get('id'),
                'subject': e.get('subject'),
                'start': e.get('start'),
                'end': e.get('end'),
                'join_url': join_link,
                'web_link': e.get('webLink'),
            })
    return meetings


def main():
    parser = argparse.ArgumentParser(description="List upcoming Microsoft Teams meetings")
    parser.add_argument('--days', type=int, default=7)
    parser.add_argument('--limit', type=int, default=20)
    args = parser.parse_args()

    access_token, _ = acquire_token()

    now = datetime.utcnow()
    end = now + timedelta(days=args.days)

    meetings = list_events(access_token, now, end, args.limit)
    print(json.dumps(meetings, indent=2))


if __name__ == '__main__':
    main()
