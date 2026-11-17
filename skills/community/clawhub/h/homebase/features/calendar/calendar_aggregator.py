#!/usr/bin/env python3
"""
Family Calendar Aggregator & Household Assistant for OpenClaw
Focused on Google Calendar and WhatsApp integration
"""

import json
import os
import sys
from typing import Dict, List, Optional
from datetime import datetime, timedelta, timezone

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
        self.sync_marker_file = os.path.join(self.calendar_path, "last_sync.json")
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
                    # No credential fields: gcal.list_events uses only `id`,
                    # and gog resolves its own token. Carrying empty GOOGLE_*
                    # copies here made a calendar entry look configurable per
                    # calendar when it never was.
                    self.config["supported_calendars"] = [{
                        "name": "Family Calendar",
                        "type": "google",
                        "id": cfg.calendar_id,
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

    @staticmethod
    def _inclusive_end_date(start: str, end: str) -> str:
        """
        Last date an event actually covers, inclusive.

        Timed events carry a real end timestamp, so their date part is already
        inclusive. All-day events do not: Google reports `end.date` as the day
        AFTER the last one, so it gets rolled back a day. An event missing an
        end falls back to its own start rather than returning empty, so callers
        can always compare `date <= end_date` without a None check.
        """
        if not end:
            return start.split('T')[0] if start else ""
        if 'T' in end:
            return end.split('T')[0]
        try:
            return (datetime.strptime(end, "%Y-%m-%d").date() - timedelta(days=1)).isoformat()
        except ValueError:
            return start.split('T')[0] if start else ""

    def get_events_by_date(self, date: str) -> List[Dict]:
        """Events that START on `date`.

        Deliberately a start-date match, not a span match: the briefings build a
        day's timeline from this, and a 9-day trip should appear as one row on
        departure day rather than as a repeated line every morning.
        """
        return [e for e in self.calendar.values() if e.get("date") == date]

    def get_events_for_today(self) -> List[Dict]:
        today = datetime.now().strftime("%Y-%m-%d")
        return self.get_events_by_date(today)

    # ─── Google Calendar Sync ───────────────────────────────────────────────

    # `_build_credentials` lived here until 2026-09-07. Credentials are gog's
    # business now — see core/gcal.py — so there is nothing to build, refresh,
    # or fail at. The "missing credentials in env vars" skip it used to print
    # is gone with it: gog reports its own auth state via `gog auth status`,
    # which can tell a missing secret from an unreadable keyring, and this
    # never could.

    # Sync window: how many days back/forward we replace from Google's truth.
    # Yesterday → +30 days covers same-day manual reruns and ~1 month of
    # forward visibility for the briefing and weekly planner. Events outside
    # this window in the local cache are left alone (they're historical
    # records the briefing never reads anyway).
    SYNC_WINDOW_DAYS_BACK    = 1
    SYNC_WINDOW_DAYS_FORWARD = 30
    # SYNC_PAGE_SIZE / MAX_SYNC_PAGES retired 2026-09-07 with the hand-rolled
    # pagination loop; gog's --all-pages owns that now.

    # How long a sync stays fresh enough to reuse.
    #
    # Every calendar tool called sync unconditionally, so "what's on today"
    # cost an OAuth refresh, a paginated events.list and a 119 KB rewrite of
    # the cache — measured at 1.2-1.6s, ~85% of it network wait. An agent
    # answering one question often makes three such calls in a turn.
    #
    # Two minutes is chosen against the failure it has to avoid: someone adds
    # an event on their phone and immediately asks about it. Two minutes of
    # staleness is shorter than that round trip in practice, and it collapses
    # the repeated-calls-in-one-turn case completely. The briefings pass
    # force=True regardless — they must never read a cache.
    SYNC_TTL_SECONDS = 120

    def _seconds_since_sync(self) -> Optional[float]:
        """Age of the last successful sync, or None if there has never been one."""
        try:
            with open(self.sync_marker_file) as f:
                stamp = json.load(f).get("synced_at", "")
            return (datetime.now() - datetime.fromisoformat(stamp)).total_seconds()
        except Exception:
            # Deliberately broad. This is a disposable cache: any unreadable
            # shape at all — including a file that parses to something with no
            # .get, which raised AttributeError straight out of every calendar
            # tool — must mean "sync now", never "break the caller".
            return None

    def _record_sync(self) -> None:
        write_json_atomic(self.sync_marker_file, {"synced_at": datetime.now().isoformat()})

    def sync_with_google_calendar(self, detect_restaurants: bool = False,
                                  force: bool = False) -> bool:
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

        `detect_restaurants` opts into the calendar → restaurant auto-log.
        It is a write, so read-only callers leave it False.

        `force` skips the SYNC_TTL_SECONDS freshness check. The briefings pass
        it; ad-hoc reads reuse a sync younger than the TTL.
        """
        if not force:
            age = self._seconds_since_sync()
            if age is not None and 0 <= age < self.SYNC_TTL_SECONDS:
                print(f"Calendar cache is {age:.0f}s old — reusing.", file=sys.stderr)
                # `force` governs whether we re-FETCH, not whether the
                # caller's requested side effect runs. Returning straight out
                # of here silently dropped detect_restaurants, so a caller
                # asking for the auto-log got a cache hit and no auto-log.
                if detect_restaurants:
                    self._detect_restaurant_events()
                return True

        print("Syncing with Google Calendar...", file=sys.stderr)
        total_added   = 0
        total_dropped = 0
        enabled_count = 0
        succeeded_count = 0

        # Window in local time, then convert to UTC for the API call
        now_local      = datetime.now()
        window_start   = (now_local - timedelta(days=self.SYNC_WINDOW_DAYS_BACK)).replace(
            hour=0, minute=0, second=0, microsecond=0)
        window_end     = (now_local + timedelta(days=self.SYNC_WINDOW_DAYS_FORWARD)).replace(
            hour=23, minute=59, second=59, microsecond=0)
        window_start_s = window_start.strftime("%Y-%m-%d")
        window_end_s   = window_end.strftime("%Y-%m-%d")
        time_min       = (datetime.now(timezone.utc) - timedelta(days=self.SYNC_WINDOW_DAYS_BACK)).isoformat()
        time_max       = (datetime.now(timezone.utc) + timedelta(days=self.SYNC_WINDOW_DAYS_FORWARD)).isoformat()

        enabled = [c for c in self.config.get("supported_calendars", [])
                   if c.get("type") == "google" and c.get("enabled", True)]
        enabled_count = len(enabled)

        # No credential handling here any more (2026-09-07). `gog` resolves its
        # own token from the Keychain per invocation, so the eager
        # build-credentials-once dance this used to do — to avoid paying a
        # blocking token refresh per calendar — has nothing left to optimize.
        from core import gcal

        # Evict everything belonging to a calendar that is no longer enabled.
        #
        # The per-calendar invalidation below only drops events from calendars
        # it actually syncs, which is deliberate — a calendar that failed this
        # run keeps its cached events rather than vanishing from the briefing.
        # The side effect was that DISABLING a calendar left its events cached
        # forever: turning off the work calendar on 2026-09-07 stopped 225
        # events being refreshed without removing a single one of them.
        #
        # Keyed on the configured name, the same value stored as
        # `calendar_source`.
        enabled_names = {c.get('name', '<unknown>') for c in enabled}
        stale = [eid for eid, e in self.calendar.items()
                 if e.get("calendar_source") not in enabled_names]
        for eid in stale:
            del self.calendar[eid]
        if stale:
            print(f"  Dropped {len(stale)} event(s) from disabled calendars.",
                  file=sys.stderr)

        for cal in enabled:
            cal_name = cal.get('name', '<unknown>')
            try:

                # Pagination now belongs to gog's --all-pages (see core.gcal).
                # This used to hand-roll it with a MAX_SYNC_PAGES ceiling,
                # because `while True` on nextPageToken had no bound and each
                # page carried googleapiclient's 60s default — a slow or
                # looping response could stall the 6:05 send for pages x 60s.
                # gog bounds the whole call with its own timeout instead.
                #
                # A busy fortnight genuinely exceeds one page, and gog's
                # default is --max=10, so --all-pages inside gcal.list_events
                # is what keeps this from silently returning the first ten
                # events and reporting the rest as cancelled.
                fresh: Dict[str, Dict] = {}
                for event in gcal.list_events(cal["id"], time_min, time_max):
                    start = event['start'].get('dateTime', event['start'].get('date', ''))
                    end = event.get('end', {}).get('dateTime', event.get('end', {}).get('date', ''))
                    fresh[event['id']] = {
                        "id":              event['id'],
                        "title":           (event.get('summary') or '').strip() or 'Untitled',
                        "date":            start.split('T')[0] if 'T' in start else start,
                        "time":            start.split('T')[1][:5] if 'T' in start else "All day",
                        "end_time":        end.split('T')[1][:5] if 'T' in end else "All day",
                        # Inclusive last day the event covers. Until 2026-08-28 only
                        # `date` was kept, so a multi-day all-day event (a trip, a
                        # conference, "Sam out of town") existed in the cache on
                        # its first day and vanished on every day after — invisible to
                        # every briefing that asked about those days.
                        #
                        # Google's all-day `end.date` is EXCLUSIVE: Aug 29–Sep 6
                        # inclusive arrives as end.date == 2026-09-07. Normalize that
                        # here so no consumer has to remember the rule.
                        "end_date":        self._inclusive_end_date(start, end),
                        "location":        (event.get('location') or '').strip(),
                        "attendees":       self.config.get("family_members", []),
                        "description":     event.get('description', ''),
                        "calendar_source": cal_name,
                        "original_id":     event['id'],
                    }

            except Exception as e:
                print(f"  Error syncing '{cal_name}': {e} — leaving cache for this calendar untouched.", file=sys.stderr)
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
            succeeded_count += 1

        # Nothing was added to self.calendar when no calendar succeeded, so
        # the write is provably a no-op there — and it serializes 126 KB.
        if succeeded_count:
            self.save_calendar()
        # Freshness has to mean EVERY enabled calendar is fresh. A run where
        # any calendar errored must not stamp the marker: with two enabled
        # calendars and a per-calendar token refresh, one failing while the
        # other succeeds is the plausible case, and `any` would then serve a
        # cache holding stale data for that calendar to every non-forced
        # reader for the whole TTL. The school runner's dedup is the sharpest
        # consumer — its own guard only catches a lookup that FAILS, and a
        # TTL-cached lookup succeeds while returning stale data.
        if enabled_count and succeeded_count == enabled_count:
            self._record_sync()
        print(f"Synced: {total_added} kept/added, {total_dropped} dropped from window {window_start_s} → {window_end_s}.", file=sys.stderr)

        # Auto-detect restaurant visits from calendar events.
        #
        # Off by default. This is a WRITE, and it used to run on every sync —
        # which is every calendar tool call — so asking "what's on today"
        # appended to restaurants.json. Only the two briefings, which run once
        # each per day, opt in.
        if detect_restaurants:
            self._detect_restaurant_events()

        return True

    def _detect_restaurant_events(self):
        """Auto-log restaurant visits found in calendar events."""
        try:
            from features.dining.restaurant_tracker import (
                check_calendar_for_restaurants, log_visit
            )
            # Today and earlier only. The cache spans yesterday -> +30 days,
            # so scanning all of it logged future reservations as completed
            # visits — and get_pending_reminders gates on `logged_at`, not on
            # the visit date, so a reservation three weeks out produced a
            # "how was it?" prompt two hours later.
            today = datetime.now().strftime("%Y-%m-%d")
            events = [e for e in self.calendar.values()
                      if (e.get("date") or "") <= today]

            # Dedupe lives in log_visit(), which merges on (date, restaurant).
            # This loop used to keep its own copy of that rule; the receipt
            # path did not, so a receipt for a dinner the calendar had already
            # caught appended a second visit and a second rating prompt.
            for hit in check_calendar_for_restaurants(events):
                log_visit(
                    restaurant = hit["restaurant"],
                    date       = hit["date"],
                    meal_type  = hit["meal_type"],
                    source     = "calendar"
                )

        except Exception as e:
            print(f"Restaurant calendar detection error: {e}", file=sys.stderr)



# ─── Quick smoke test ────────────────────────────────────────────────────────
if __name__ == "__main__":
    # No .env: gog owns the Google credentials and resolves them per invocation.
    assistant = FamilyCalendarAggregator(".")
    assistant.sync_with_google_calendar()
    print(f"Synced {len(assistant.calendar)} events.")