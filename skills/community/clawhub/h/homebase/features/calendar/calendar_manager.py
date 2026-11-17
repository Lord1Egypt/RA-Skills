#!/usr/bin/env python3
"""
Calendar Manager
Create, edit and delete events in the family Google Calendar.
Callers pass explicit dates and times; the agent does the language part.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Tuple

def _get_calendar_id():
    try:
        from core.config_loader import config
        return config.calendar_id
    except Exception:
        return ""
CALENDAR_ID = _get_calendar_id()

def _get_timezone():
    try:
        from core.config_loader import config
        return config.timezone
    except Exception:
        return "America/Los_Angeles"
TIMEZONE = _get_timezone()

# ─── Auth ────────────────────────────────────────────────────────────────────
#
# There is none here any more (2026-09-07). `get_calendar_service` and its
# memoized `_SERVICE`, plus `reset_calendar_service`, are gone: core/gcal.py
# shells out to the `gog` CLI, which resolves its own refresh token from the
# Keychain per invocation.
#
# The memoization those functions existed for is gone with them, and so is
# what it was worth: building a service once per process saved a token refresh
# round trip on each of create/delete/update, which mattered most to
# confirm_pending_school_events calling create_event in a loop. gog pays its
# own auth cost per subprocess, so a five-event confirmation is five
# invocations again. Measure before optimizing that — a batch create in gog,
# not a service cache here, is the fix if it ever shows up.

# ─── Calendar Operations ─────────────────────────────────────────────────────

def create_event(title: str, date_str: str, time_str: str = None,
                 duration_minutes: int = 60, is_all_day: bool = False,
                 description: str = "", end_date: str = None,
                 location: str = "") -> Dict:
    """Create an event in the family calendar.

    `end_date` is the INCLUSIVE last day of a multi-day all-day event — pass
    the day the trip actually ends and the exclusive form Google wants is
    derived here. Ignored for timed events, whose length comes from
    `duration_minutes`.
    """
    from core import gcal

    if is_all_day or not time_str:
        # Google's all-day `end.date` is exclusive, so a one-day event ends the
        # day AFTER it starts. This used to send end == start, i.e. a
        # zero-length span, which Google silently normalizes for a single day
        # but which cannot express a multi-day event at all.
        #
        # The conversion stays HERE rather than in core.gcal: homebase speaks
        # inclusive end dates everywhere (a trip ends the day it ends), and
        # exactly one place should know that Google disagrees.
        last_day = end_date or date_str
        exclusive_end = (
            datetime.strptime(last_day, "%Y-%m-%d") + timedelta(days=1)
        ).strftime("%Y-%m-%d")
        return gcal.create_event(
            CALENDAR_ID, title, date_str, exclusive_end,
            all_day=True, description=description, location=location,
        )

    start_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    end_dt   = start_dt + timedelta(minutes=duration_minutes)
    return gcal.create_event(
        CALENDAR_ID, title, start_dt.isoformat(), end_dt.isoformat(),
        description=description, location=location, timezone=TIMEZONE,
    )


def delete_event(search_term: str, date_str: str = None) -> Tuple[bool, str]:
    """
    Find and delete an event by title (and optionally date).
    Returns (success, message). If more than one upcoming event matched,
    the earliest one is still deleted (existing behavior — callers like the
    club_studio watcher rely on loose matching plus a silent "not found"),
    but the message flags how many other events also matched so an ambiguous
    delete is never silent.
    """
    from core import gcal
    now = datetime.now(timezone.utc).isoformat()
    horizon = (datetime.now(timezone.utc) + timedelta(days=400)).isoformat()

    events = gcal.list_events(CALENDAR_ID, now, horizon, query=search_term)
    if not events:
        return False, f"No upcoming event found matching '{search_term}'"

    # If date specified, filter by date
    if date_str:
        events = [e for e in events
                  if e['start'].get('date', e['start'].get('dateTime', ''))[:10] == date_str]

    if not events:
        return False, f"No event matching '{search_term}' on {date_str}"

    # Delete first (earliest) match
    event = events[0]
    gcal.delete_event(CALENDAR_ID, event['id'])
    deleted_summary = event.get('summary', 'Event')

    if len(events) > 1:
        others = ", ".join(e.get('summary', 'Event') for e in events[1:4])
        return True, f"{deleted_summary} (⚠️ {len(events) - 1} other event(s) also matched '{search_term}': {others} — verify this was the right one)"

    return True, deleted_summary


def update_event(search_term: str, new_title: str = None,
                 new_date: str = None, new_time: str = None) -> Tuple[bool, str]:
    """Find and update an event. Returns (success, message). If more than
    one upcoming event matched, the earliest one is still updated (existing
    behavior), but the message flags how many others also matched so an
    ambiguous update is never silent."""
    from core import gcal
    now = datetime.now(timezone.utc).isoformat()
    horizon = (datetime.now(timezone.utc) + timedelta(days=400)).isoformat()

    events = gcal.list_events(CALENDAR_ID, now, horizon, query=search_term)
    if not events:
        return False, f"No upcoming event found matching '{search_term}'"

    event = events[0]

    # Accumulated into a PATCH rather than mutated onto the event and PUT back.
    patch: Dict = {}
    if new_title:
        patch["summary"] = new_title

    if new_date or new_time:
        # What kind of event is this *now*? A timed event moved to a new date
        # must stay timed — the previous code rewrote start/end as bare
        # {"date": ...} whenever new_time was absent, silently converting a
        # 4pm appointment into an all-day block. For a trip event that also
        # flips travel_window's most load-bearing input.
        was_timed = "dateTime" in event.get("start", {})
        old_start = event.get("start", {}).get("dateTime", "")
        old_date  = (event.get("start", {}).get("date")
                     or old_start[:10])
        old_time  = old_start[11:16] if old_start else None

        target_date = new_date or old_date
        target_time = new_time or (old_time if was_timed else None)

        if target_time:
            # Preserve the original duration rather than forcing an hour.
            duration = timedelta(hours=1)
            old_end = event.get("end", {}).get("dateTime", "")
            if old_start and old_end:
                try:
                    duration = (datetime.fromisoformat(old_end)
                                - datetime.fromisoformat(old_start))
                except ValueError:
                    pass
            start_dt = datetime.strptime(f"{target_date} {target_time}", "%Y-%m-%d %H:%M")
            end_dt   = start_dt + duration
            patch["start"]    = start_dt.isoformat()
            patch["end"]      = end_dt.isoformat()
            patch["timezone"] = TIMEZONE
        else:
            # All-day. Google's end.date is EXCLUSIVE, so a one-day event ends
            # the day AFTER it starts. Preserve the event's ORIGINAL span
            # rather than forcing one day: re-dating a 9-day `Trip to Seattle`
            # collapsed it to a single day, and travel_window gates on exactly
            # that span, so the remaining 8 days silently reverted to home
            # weather. create_event derives its span from `end_date`; this
            # branch has no equivalent argument, so it reads the span off the
            # event it is editing.
            span_days = 1
            old_exclusive = event.get("end", {}).get("date")
            if old_exclusive and old_date:
                try:
                    span_days = max(
                        (datetime.strptime(old_exclusive, "%Y-%m-%d")
                         - datetime.strptime(old_date, "%Y-%m-%d")).days,
                        1,
                    )
                except ValueError:
                    span_days = 1
            exclusive_end = (
                datetime.strptime(target_date, "%Y-%m-%d")
                + timedelta(days=span_days)
            ).strftime("%Y-%m-%d")
            patch["start"]   = target_date
            patch["end"]     = exclusive_end
            patch["all_day"] = True

    updated = gcal.update_event(CALENDAR_ID, event['id'], **patch)

    updated_summary = updated.get('summary') or new_title or event.get('summary', 'Event')
    if len(events) > 1:
        others = ", ".join(e.get('summary', 'Event') for e in events[1:4])
        return True, f"{updated_summary} (⚠️ {len(events) - 1} other event(s) also matched '{search_term}': {others} — verify this was the right one)"

    return True, updated_summary


# ─── CLI ─────────────────────────────────────────────────────────────────────
#
# Production reaches this module through tools.py (add_calendar_event and
# friends), which passes explicit date/time arguments. There is no natural
# language left to parse here — the agent does that — so there is no CLI.
