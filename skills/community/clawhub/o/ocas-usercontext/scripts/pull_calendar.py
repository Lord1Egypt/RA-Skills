#!/usr/bin/env python3
"""
3-day calendar pull for ocas-usercontext cron job.
Uses google_auth_mcp with fallback from Jared's token to Indigo's token.
Outputs JSON with events for yesterday, today, tomorrow.
"""

import sys
import os
import json
from datetime import datetime, timezone, timedelta

# Add google_auth_mcp to path
sys.path.insert(0, '/root/.hermes/scripts')

from google_auth_mcp import get_service

# Timezone handling - host is America/Los_Angeles (PDT = -07:00 in August)
PDT = timezone(timedelta(hours=-7))

# Calendar IDs to query
CALENDARS = [
    'jared.zimmerman@gmail.com',  # Jared's primary
    'family08350553536598846140@group.calendar.google.com',  # Family calendar
]

# Accounts to try in order (fallback pattern) - use the email addresses that match credential files
ACCOUNTS = [
    'jared.zimmerman@gmail.com',
    'mx.indigo.karasu@gmail.com',
]

def get_calendar_service():
    """Try each account until one works."""
    for account in ACCOUNTS:
        try:
            cal = get_service('calendar', 'v3',
                ['https://www.googleapis.com/auth/calendar.readonly'],
                account=account)
            # Test the connection
            cal.calendarList().list(maxResults=1).execute()
            print(f"Using account: {account}", file=sys.stderr)
            return cal
        except Exception as e:
            print(f"Account {account} failed: {e}", file=sys.stderr)
            continue
    return None

def parse_event_time(ev):
    """Parse event start time to local timezone."""
    start = ev.get('start', {})
    if 'dateTime' in start:
        raw = start['dateTime']
        if raw.endswith('Z'):
            dt = datetime.fromisoformat(raw.replace('Z', '+00:00'))
        else:
            dt = datetime.fromisoformat(raw)
        local_dt = dt.astimezone(PDT)
        return local_dt.strftime('%H:%M'), local_dt.date()
    elif 'date' in start:
        # All-day event
        dt = datetime.fromisoformat(start['date']).date()
        return 'all day', dt
    return None, None

def format_event(ev):
    """Format event as bullet string."""
    time_str, event_date = parse_event_time(ev)
    if time_str is None:
        return None
    summary = ev.get('summary', '(no title)')
    location = ev.get('location', '')
    if location:
        return f"{summary}, {time_str}, {location}"
    return f"{summary}, {time_str}"

def pull_events_for_date(calendar, target_date):
    """Pull events for a specific date from all calendars."""
    # timeMin = start of target date in PDT
    # timeMax = start of next day in PDT
    time_min = datetime.combine(target_date, datetime.min.time(), tzinfo=PDT).isoformat()
    time_max = datetime.combine(target_date + timedelta(days=1), datetime.min.time(), tzinfo=PDT).isoformat()

    all_events = []
    seen = set()  # for dedup: (summary, start_time, location)

    for cal_id in CALENDARS:
        try:
            result = calendar.events().list(
                calendarId=cal_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime',
                showDeleted=False
            ).execute()
            events = result.get('items', [])
            for ev in events:
                time_str, ev_date = parse_event_time(ev)
                if ev_date != target_date:
                    continue
                summary = ev.get('summary', '(no title)')
                location = ev.get('location', '')
                start_dt = ev.get('start', {}).get('dateTime', ev.get('start', {}).get('date', ''))
                dedup_key = (summary, start_dt, location)
                if dedup_key not in seen:
                    seen.add(dedup_key)
                    formatted = format_event(ev)
                    if formatted:
                        all_events.append(formatted)
        except Exception as e:
            print(f"Error querying calendar {cal_id}: {e}", file=sys.stderr)

    return all_events

def main():
    # Current date in host timezone
    now = datetime.now(PDT)
    today = now.date()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    calendar = get_calendar_service()
    if calendar is None:
        print(json.dumps({
            "yesterday": ["No available calendar data"],
            "today": ["No available calendar data"],
            "tomorrow": ["No available calendar data"],
            "degraded": "oauth_stale"
        }))
        return

    result = {
        "yesterday": pull_events_for_date(calendar, yesterday),
        "today": pull_events_for_date(calendar, today),
        "tomorrow": pull_events_for_date(calendar, tomorrow),
    }

    # Replace empty lists with "No scheduled events"
    for day in result:
        if day != "degraded" and not result[day]:
            result[day] = ["No scheduled events"]

    print(json.dumps(result))

if __name__ == '__main__':
    main()