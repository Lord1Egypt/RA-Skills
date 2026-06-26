#!/usr/bin/env python3
"""
Family Calendar Aggregator & Household Assistant for OpenClaw
Focused on Google Calendar and WhatsApp integration
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from utils import write_json_atomic


class FamilyCalendarAggregator:
    """Advanced calendar aggregator and household assistant focused on Google Calendar and WhatsApp."""

    def __init__(self, base_path: str = "."):
        self.base_path = base_path
        self.calendar_path = os.path.join(base_path, "calendar_data")
        self.inventory_path = os.path.join(base_path, "household")

        os.makedirs(self.calendar_path, exist_ok=True)
        os.makedirs(self.inventory_path, exist_ok=True)

        self.calendar_file = os.path.join(self.calendar_path, "family_calendar.json")
        self.config_file = os.path.join(base_path, "config.json")

        self.load_config()
        self.load_calendar()

    # ─── Config ────────────────────────────────────────────────────────────────

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "family_members": [],
                "default_reminder_minutes": 30,
                "driving_buffer_minutes": 30,
                "supported_calendars": [],
                "whatsapp_number": "",
                "google_calendar_enabled": True
            }
            self.save_config()

        # Use config_loader as source of truth for calendar settings
        # Falls back gracefully if config_loader not available
        if not self.config.get("supported_calendars"):
            try:
                from core.config_loader import config as cfg
                if cfg.calendar_id:
                    self.config["supported_calendars"] = [{
                        "name": "Family Calendar",
                        "type": "google",
                        "id": cfg.calendar_id,
                        "client_id": os.environ.get("GOOGLE_CLIENT_ID", ""),
                        "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET", ""),
                        "refresh_token": os.environ.get("GOOGLE_REFRESH_TOKEN", ""),
                        "access_token": "",
                        "enabled": True
                    }]
            except Exception:
                pass

    def save_config(self):
        write_json_atomic(self.config_file, self.config)

    # ─── Calendar (stored as dict keyed by event id) ────────────────────────

    def load_calendar(self):
        """Load calendar, auto-migrating list → dict if needed."""
        if os.path.exists(self.calendar_file):
            with open(self.calendar_file, 'r') as f:
                data = json.load(f)
            # FIX: Migrate old list format to dict
            if isinstance(data, list):
                self.calendar = {str(e["id"]): e for e in data}
                self.save_calendar()
            else:
                self.calendar = data
        else:
            self.calendar = {}
            self.save_calendar()

    def save_calendar(self):
        write_json_atomic(self.calendar_file, self.calendar)

    def add_event(self, title: str, date: str, time: str,
                  attendees: List[str] = None, description: str = "",
                  calendar_source: str = "manual",
                  add_driving_buffers: bool = True) -> Dict:
        """Add a new calendar event."""
        event_id = str(len(self.calendar) + 1)
        event = {
            "id": event_id,
            "title": title,
            "date": date,
            "time": time,
            "attendees": attendees or [],
            "description": description,
            "calendar_source": calendar_source,
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat()
        }
        if add_driving_buffers:
            buffer = self.config.get("driving_buffer_minutes", 30)
            event["driving_buffer_before"] = buffer
            event["driving_buffer_after"] = buffer

        self.calendar[event_id] = event
        self.save_calendar()
        return event

    def get_upcoming_events(self, days: int = 7) -> List[Dict]:
        """Get upcoming events for the next N days."""
        today = datetime.now()
        cutoff = today + timedelta(days=days)
        upcoming = []

        # FIX: Always iterate over dict values — no more isinstance branching
        for event in self.calendar.values():
            try:
                event_date = datetime.strptime(event["date"], "%Y-%m-%d")
                if today <= event_date <= cutoff:
                    upcoming.append(event)
            except (ValueError, KeyError):
                continue

        return sorted(upcoming, key=lambda x: x["date"] + " " + x.get("time", ""))

    def get_events_by_date(self, date: str) -> List[Dict]:
        return [e for e in self.calendar.values() if e.get("date") == date]

    def get_events_for_today(self) -> List[Dict]:
        today = datetime.now().strftime("%Y-%m-%d")
        return self.get_events_by_date(today)

    def get_conflicting_events(self) -> List[tuple]:
        """Find events on the same date and time."""
        conflicts = []
        # FIX: Always use dict values
        events_list = list(self.calendar.values())

        for i, e1 in enumerate(events_list):
            if not isinstance(e1, dict) or e1.get("time") == "00:00":
                continue
            for e2 in events_list[i + 1:]:
                if not isinstance(e2, dict) or e2.get("time") == "00:00":
                    continue
                if e1.get("date") == e2.get("date") and e1.get("time") == e2.get("time"):
                    if e1.get("title") != e2.get("title"):
                        conflicts.append((e1, e2))
        return conflicts

    def add_driving_buffer(self, event_id: str, minutes_before: int, minutes_after: int) -> bool:
        """Add driving buffers to an existing event."""
        # FIX: Renamed loop variable to avoid shadowing the parameter
        for eid, event in self.calendar.items():
            if eid == str(event_id):
                event["driving_buffer_before"] = minutes_before
                event["driving_buffer_after"] = minutes_after
                event["modified"] = datetime.now().isoformat()
                self.save_calendar()
                return True
        return False

    def create_morning_briefing(self, days_ahead: int = 3) -> Dict:
        today = datetime.now().strftime("%Y-%m-%d")
        upcoming_events = self.get_upcoming_events(days_ahead)

        events_by_date: Dict[str, List] = {}
        for event in upcoming_events:
            date = event["date"]
            events_by_date.setdefault(date, []).append(event)

        return {
            "date": today,
            "upcoming_events": events_by_date,
            "conflicts": self.get_conflicting_events(),
            "total_events": len(upcoming_events),
            "generated_at": datetime.now().isoformat()
        }

    # ─── Google Calendar Sync ───────────────────────────────────────────────

    def _build_credentials(self, cal: Dict):
    	"""Build and auto-refresh Google credentials from env vars directly."""
    	from google.oauth2.credentials import Credentials
    	from google.auth.transport.requests import Request
    	client_id     = os.environ.get("GOOGLE_CLIENT_ID", "")
    	client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "")
    	refresh_token = os.environ.get("GOOGLE_REFRESH_TOKEN", "")

    	if not all([client_id, client_secret, refresh_token]):
        	print(f"  Skipping '{cal.get('name')}' — missing credentials in env vars.")
        	return None

    	creds = Credentials(
        	token="",
        	refresh_token=refresh_token,
        	token_uri="https://oauth2.googleapis.com/token",
        	client_id=client_id,
        	client_secret=client_secret
    	)

    	try:
        	creds.refresh(Request())
    	except Exception as e:
        	print(f"  Token refresh failed for '{cal.get('name')}': {e}")
        	return None

    	return creds

    # Sync window: how many days back/forward we replace from Google's truth.
    # Yesterday → +30 days covers same-day manual reruns and ~1 month of
    # forward visibility for the briefing and weekly planner. Events outside
    # this window in the local cache are left alone (they're historical
    # records the briefing never reads anyway).
    SYNC_WINDOW_DAYS_BACK    = 1
    SYNC_WINDOW_DAYS_FORWARD = 30
    SYNC_PAGE_SIZE           = 250  # Google's max for events.list

    def sync_with_google_calendar(self) -> bool:
        """Sync events from all enabled Google Calendars.

        Replaces every cached event whose date falls within the sync window
        (yesterday → +30 days) with the authoritative list from Google.
        Events Google no longer returns are dropped from the cache, fixing
        the historical bug where deleted/cancelled events lived forever in
        the local cache and kept appearing in the morning briefing.

        Failure isolation: each calendar is sync'd inside its own try/except
        and the cache is only mutated for calendars whose API call returned
        cleanly. A network or auth failure on calendar A leaves cached
        events from a previous successful sync of A in place — we'd rather
        show stale data than show empty.
        """
        print("Syncing with Google Calendar...")
        total_added   = 0
        total_dropped = 0

        # Window in local time, then convert to UTC for the API call
        now_local      = datetime.now()
        window_start   = (now_local - timedelta(days=self.SYNC_WINDOW_DAYS_BACK)).replace(
            hour=0, minute=0, second=0, microsecond=0)
        window_end     = (now_local + timedelta(days=self.SYNC_WINDOW_DAYS_FORWARD)).replace(
            hour=23, minute=59, second=59, microsecond=0)
        window_start_s = window_start.strftime("%Y-%m-%d")
        window_end_s   = window_end.strftime("%Y-%m-%d")
        time_min       = (datetime.utcnow() - timedelta(days=self.SYNC_WINDOW_DAYS_BACK)).isoformat() + 'Z'
        time_max       = (datetime.utcnow() + timedelta(days=self.SYNC_WINDOW_DAYS_FORWARD)).isoformat() + 'Z'

        for cal in self.config.get("supported_calendars", []):
            if not (cal.get("type") == "google" and cal.get("enabled", True)):
                continue

            creds = self._build_credentials(cal)
            if not creds:
                continue

            cal_name = cal.get('name', '<unknown>')
            try:
                from googleapiclient.discovery import build
                service = build('calendar', 'v3', credentials=creds)

                # Paginate to handle busy weeks (>250 events in a month)
                fresh: Dict[str, Dict] = {}
                page_token = None
                while True:
                    events_result = service.events().list(
                        calendarId=cal["id"],
                        timeMin=time_min,
                        timeMax=time_max,
                        maxResults=self.SYNC_PAGE_SIZE,
                        singleEvents=True,
                        orderBy='startTime',
                        pageToken=page_token,
                    ).execute()
                    for event in events_result.get('items', []):
                        start = event['start'].get('dateTime', event['start'].get('date', ''))
                        fresh[event['id']] = {
                            "id":              event['id'],
                            "title":           event.get('summary', 'Untitled'),
                            "date":            start.split('T')[0] if 'T' in start else start,
                            "time":            start.split('T')[1][:5] if 'T' in start else "All day",
                            "attendees":       self.config.get("family_members", []),
                            "description":     event.get('description', ''),
                            "calendar_source": cal_name,
                            "original_id":     event['id'],
                        }
                    page_token = events_result.get('nextPageToken')
                    if not page_token:
                        break

            except Exception as e:
                print(f"  Error syncing '{cal_name}': {e} — leaving cache for this calendar untouched.")
                continue

            # Successful API call: drop every cached event from THIS calendar
            # whose date is in the sync window, then write the fresh set in.
            # Events from OTHER calendars and events outside the window are
            # left alone.
            dropped_ids = [
                eid for eid, e in self.calendar.items()
                if e.get("calendar_source") == cal_name
                and window_start_s <= (e.get("date") or "") <= window_end_s
            ]
            for eid in dropped_ids:
                del self.calendar[eid]
            self.calendar.update(fresh)
            total_added   += len(fresh)
            total_dropped += len(dropped_ids)

        self.save_calendar()
        print(f"Synced: {total_added} kept/added, {total_dropped} dropped from window {window_start_s} → {window_end_s}.")

        # Auto-detect restaurant visits from calendar events
        self._detect_restaurant_events()

        return True

    def _detect_restaurant_events(self):
        """Auto-log restaurant visits found in calendar events."""
        try:
            from features.dining.restaurant_tracker import (
                check_calendar_for_restaurants, log_visit,
                load_data, format_visit_confirmation
            )
            events = list(self.calendar.values())
            restaurant_hits = check_calendar_for_restaurants(events)

            if not restaurant_hits:
                return

            data = load_data()
            existing_dates_names = {
                (v["date"], v["restaurant"].lower())
                for v in data["visits"]
            }

            for hit in restaurant_hits:
                key = (hit["date"], hit["restaurant"].lower())
                if key in existing_dates_names:
                    continue  # Already logged

                log_visit(
                    restaurant = hit["restaurant"],
                    date       = hit["date"],
                    meal_type  = hit["meal_type"],
                    source     = "calendar"
                )
                print(f"Auto-logged restaurant from calendar: {hit['restaurant']}")

        except Exception as e:
            print(f"Restaurant calendar detection error: {e}")



# ─── Quick smoke test ────────────────────────────────────────────────────────
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))
    assistant = FamilyCalendarAggregator(".")
    assistant.sync_with_google_calendar()
    print(f"Synced {len(assistant.calendar)} events.")