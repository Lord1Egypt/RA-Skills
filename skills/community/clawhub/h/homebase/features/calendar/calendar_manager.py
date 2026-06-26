#!/usr/bin/env python3
"""
Calendar Manager
Create, edit and delete events in the family Google Calendar.
Uses natural language parsing to extract event details.
"""

import os
import re
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

from core.keychain_secrets import load_google_secrets
load_google_secrets()

def _get_calendar_id():
    try:
        from core.config_loader import config
        return config.calendar_id
    except Exception:
        return ""
CALENDAR_ID = _get_calendar_id()

# ─── Auth ────────────────────────────────────────────────────────────────────

def get_calendar_service():
    """Build Google Calendar service with auto-refresh."""
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = Credentials(
        token="",
        refresh_token=os.environ.get("GOOGLE_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ.get("GOOGLE_CLIENT_ID"),
        client_secret=os.environ.get("GOOGLE_CLIENT_SECRET")
    )
    creds.refresh(Request())
    return build('calendar', 'v3', credentials=creds)


# ─── Date/Time Parsing ───────────────────────────────────────────────────────

MONTH_MAP = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    "january": 1, "february": 2, "march": 3, "april": 4, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10,
    "november": 11, "december": 12
}

DAY_MAP = {
    "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
    "friday": 4, "saturday": 5, "sunday": 6,
    "mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6
}


def parse_datetime(text: str) -> Tuple[Optional[str], Optional[str], bool]:
    """
    Parse date and time from natural language.
    Returns (date_str, time_str, is_all_day)
    date_str format: YYYY-MM-DD
    time_str format: HH:MM
    """
    text = text.lower().strip()
    now = datetime.now()
    date = None
    time_str = None
    is_all_day = True

    # Relative dates
    if "today" in text:
        date = now
    elif "tomorrow" in text:
        date = now + timedelta(days=1)
    elif "next week" in text:
        date = now + timedelta(weeks=1)
    elif "monday" in text or "tuesday" in text or "wednesday" in text or \
         "thursday" in text or "friday" in text or "saturday" in text or "sunday" in text:
        for day_name, day_num in DAY_MAP.items():
            if day_name in text:
                days_ahead = (day_num - now.weekday()) % 7
                if days_ahead == 0:
                    days_ahead = 7
                date = now + timedelta(days=days_ahead)
                break

    # Absolute dates — "March 20", "Mar 20", "3/20", "20th March"
    if not date:
        # "Month Day" or "Day Month"
        month_day = re.search(
            r'(?:(\d{1,2})(?:st|nd|rd|th)?\s+(' + '|'.join(MONTH_MAP.keys()) + r')|'
            r'(' + '|'.join(MONTH_MAP.keys()) + r')\s+(\d{1,2})(?:st|nd|rd|th)?)',
            text
        )
        if month_day:
            if month_day.group(1):
                day = int(month_day.group(1))
                month = MONTH_MAP[month_day.group(2)]
            else:
                month = MONTH_MAP[month_day.group(3)]
                day = int(month_day.group(4))
            year = now.year
            # If date has passed this year, assume next year
            try:
                candidate = datetime(year, month, day)
                if candidate.date() < (now - timedelta(days=7)).date():
                    year += 1
                date = datetime(year, month, day)
            except ValueError:
                pass

        # "MM/DD" or "MM/DD/YYYY"
        if not date:
            slash_date = re.search(r'(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?', text)
            if slash_date:
                month = int(slash_date.group(1))
                day   = int(slash_date.group(2))
                year  = int(slash_date.group(3)) if slash_date.group(3) else now.year
                if year < 100:
                    year += 2000
                try:
                    date = datetime(year, month, day)
                except ValueError:
                    pass

    # Time parsing
    # Time parsing — require "at" before time to avoid matching date numbers
    time_match = re.search(
        r'\bat\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)',
        text
    )
    # Fallback — time with am/pm but no "at"
    if not time_match:
        time_match = re.search(
            r'(?<!\d)(\d{1,2})(?::(\d{2}))?\s*(am|pm)',
            text
        )

    if time_match:
        # Adjust group indices based on which pattern matched
        if 'at' in time_match.group(0):
            hour   = int(time_match.group(1))
            minute = int(time_match.group(2)) if time_match.group(2) else 0
            ampm   = time_match.group(3)
        else:
            hour   = int(time_match.group(1))
            minute = int(time_match.group(2)) if time_match.group(2) else 0
            ampm   = time_match.group(3)

        if ampm == 'pm' and hour < 12:
            hour += 12
        elif ampm == 'am' and hour == 12:
            hour = 0

        time_str = f"{hour:02d}:{minute:02d}"
        is_all_day = False

    if not date:
        return None, None, True
    return date.strftime("%Y-%m-%d"), time_str, is_all_day


def parse_event_details(message: str) -> Dict:
    """
    Extract event title, date, time, and duration from natural language.
    Examples:
      "add dentist appointment March 25 at 2pm"
      "create team meeting tomorrow at 3:30pm for 1 hour"
      "schedule gymnastics every Tuesday at 4pm"
    """
    msg = message.lower()

    # Remove action words
    title_msg = re.sub(
        r'^(?:add|create|schedule|set up|book|new event|new|put)\s+',
        '', message.strip(), flags=re.IGNORECASE
    )

    # Extract duration
    duration_minutes = 60  # default 1 hour
    duration_match = re.search(r'for\s+(\d+)\s*(hour|hr|minute|min)', msg)
    if duration_match:
        val  = int(duration_match.group(1))
        unit = duration_match.group(2)
        duration_minutes = val * 60 if 'hour' in unit or 'hr' in unit else val

    # Parse date/time
    date_str, time_str, is_all_day = parse_datetime(msg)

    # Extract title — remove date/time phrases from message
    title = title_msg
    # Remove date/time patterns
    title = re.sub(
        r'\b(?:today|tomorrow|next week|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
        '', title, flags=re.IGNORECASE
    )
    title = re.sub(
        r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|january|february|march|'
        r'april|june|july|august|september|october|november|december)\s+\d{1,2}\b',
        '', title, flags=re.IGNORECASE
    )
    title = re.sub(r'\d{1,2}/\d{1,2}(?:/\d{2,4})?', '', title)
    title = re.sub(r'\bat\s+\d{1,2}(?::\d{2})?\s*(?:am|pm)?\b', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\bfor\s+\d+\s*(?:hour|hr|minute|min)s?\b', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s+', ' ', title).strip().strip(',').strip()

    return {
        "title": title,
        "date": date_str,
        "time": time_str,
        "is_all_day": is_all_day,
        "duration_minutes": duration_minutes
    }


# ─── Calendar Operations ─────────────────────────────────────────────────────

def create_event(title: str, date_str: str, time_str: str = None,
                 duration_minutes: int = 60, is_all_day: bool = False) -> Dict:
    """Create an event in the family calendar."""
    service = get_calendar_service()

    if is_all_day or not time_str:
        event_body = {
            "summary": title,
            "start": {"date": date_str},
            "end":   {"date": date_str}
        }
    else:
        start_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        end_dt   = start_dt + timedelta(minutes=duration_minutes)
        tz       = "America/Los_Angeles"
        event_body = {
            "summary": title,
            "start": {"dateTime": start_dt.isoformat(), "timeZone": tz},
            "end":   {"dateTime": end_dt.isoformat(),   "timeZone": tz}
        }

    created = service.events().insert(
        calendarId=CALENDAR_ID,
        body=event_body
    ).execute()

    return created


def delete_event(search_term: str, date_str: str = None) -> Tuple[bool, str]:
    """
    Find and delete an event by title (and optionally date).
    Returns (success, message)
    """
    service = get_calendar_service()
    now = datetime.utcnow().isoformat() + 'Z'

    # Search upcoming events
    results = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=now,
        maxResults=50,
        singleEvents=True,
        orderBy='startTime',
        q=search_term
    ).execute()

    events = results.get('items', [])
    if not events:
        return False, f"No upcoming event found matching '{search_term}'"

    # If date specified, filter by date
    if date_str:
        events = [e for e in events
                  if e['start'].get('date', e['start'].get('dateTime', ''))[:10] == date_str]

    if not events:
        return False, f"No event matching '{search_term}' on {date_str}"

    # Delete first match
    event = events[0]
    service.events().delete(calendarId=CALENDAR_ID, eventId=event['id']).execute()
    return True, event.get('summary', 'Event')


def update_event(search_term: str, new_title: str = None,
                 new_date: str = None, new_time: str = None) -> Tuple[bool, str]:
    """Find and update an event."""
    service = get_calendar_service()
    now = datetime.utcnow().isoformat() + 'Z'

    results = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=now,
        maxResults=20,
        singleEvents=True,
        orderBy='startTime',
        q=search_term
    ).execute()

    events = results.get('items', [])
    if not events:
        return False, f"No upcoming event found matching '{search_term}'"

    event = events[0]

    if new_title:
        event['summary'] = new_title

    if new_date and new_time:
        start_dt = datetime.strptime(f"{new_date} {new_time}", "%Y-%m-%d %H:%M")
        end_dt   = start_dt + timedelta(hours=1)
        tz       = "America/Los_Angeles"
        event['start'] = {"dateTime": start_dt.isoformat(), "timeZone": tz}
        event['end']   = {"dateTime": end_dt.isoformat(),   "timeZone": tz}
    elif new_date:
        event['start'] = {"date": new_date}
        event['end']   = {"date": new_date}

    updated = service.events().update(
        calendarId=CALENDAR_ID,
        eventId=event['id'],
        body=event
    ).execute()

    return True, updated.get('summary', 'Event')


# ─── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: calendar_manager.py <natural language command>")
        print("Examples:")
        print("  calendar_manager.py 'add dentist March 25 at 2pm'")
        print("  calendar_manager.py 'delete dentist'")
        sys.exit(1)

    msg = " ".join(sys.argv[1:])
    details = parse_event_details(msg)
    print(f"Parsed: {details}")

    if details["date"] and details["title"]:
        result = create_event(
            title=details["title"],
            date_str=details["date"],
            time_str=details["time"],
            duration_minutes=details["duration_minutes"],
            is_all_day=details["is_all_day"]
        )
        print(f"Created: {result.get('summary')} on {result['start']}")
