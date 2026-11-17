#!/usr/bin/env python3
"""
Morning Briefing Orchestrator
Runs at 7:00 AM daily via the OpenClaw scheduler. Returns structured briefing
data as JSON to stdout — Python does NOT send WhatsApp messages. The OpenClaw
agent reads the JSON, composes the warm summary, and delivers it to the family
group itself.
"""

import json
import os
import sys

from core.config_loader import SKILL_DIR

from datetime import datetime
from features.calendar.calendar_aggregator import FamilyCalendarAggregator
from features.meals.meal_tracker import MealTracker
from features.school.snack_manager import SnackManager
from features.briefing.weather import get_weather_briefing
from features.briefing.daily_thought import get_daily_thought
from utils import write_json_atomic, locked_file


# ─── Config ──────────────────────────────────────────────────────────────────

# ─── Helpers ─────────────────────────────────────────────────────────────────

_DROPOFF_NEEDLES = ("drop off", "drop-off", "dropoff")


def has_dropoff_today(events):
    """Return events whose title or description names a drop-off.

    Matches the three common spellings: ``drop off`` (two words),
    ``drop-off`` (hyphen), and ``dropoff`` (one word). Case-insensitive.
    """
    out = []
    for e in events:
        title = (e.get("title") or "").lower()
        desc  = (e.get("description") or "").lower()
        if any(n in title or n in desc for n in _DROPOFF_NEEDLES):
            out.append(e)
    return out


# ─── Main ─────────────────────────────────────────────────────────────────────


def _load_primary_email_id() -> str:
    try:
        config_path = os.path.join(SKILL_DIR, "config.json")
        with open(config_path) as f:
            return json.load(f).get("calendar", {}).get("primary_email_id", "")
    except Exception:
        return ""


def validate_briefing_data(data: dict) -> list:
    warnings = []

    if not isinstance(data.get("events"), list):
        warnings.append("events is not a list")

    if data.get("weather") is None:
        warnings.append("weather data unavailable (API may be down)")
    elif isinstance(data["weather"], str) and "°F" not in data["weather"] and "°" not in data["weather"]:
        warnings.append("weather data missing temperature")

    meals = data.get("meal_suggestions", {})
    try:
        from core.config_loader import config as _cfg
        expected_kids = [k.name.lower() for k in _cfg.kids]
    except Exception:
        expected_kids = []
    for kid in expected_kids:
        if kid not in meals:
            warnings.append(f"meal suggestions missing for {kid}")

    today_str = datetime.now().strftime("%A, %B %d")
    if data.get("date") != today_str:
        warnings.append(f"date mismatch: expected '{today_str}', got '{data.get('date')}'")

    primary_email = _load_primary_email_id()
    if primary_email:
        for event in data.get("events", []):
            source = event.get("calendar_source", "")
            if primary_email.lower() in source.lower():
                warnings.append(f"personal calendar event detected: {event.get('title', '?')}")

    return warnings


def _record_reliability(data: dict, warnings: list):
    tracker_path = os.path.join(SKILL_DIR, "household", "briefing_reliability.json")
    os.makedirs(os.path.dirname(tracker_path), exist_ok=True)
    try:
        with locked_file(tracker_path):
            _record_reliability_locked(tracker_path, data, warnings)
    except TimeoutError as e:
        # locked_file's acquire is bounded, and this is the 6:05 AM path.
        # Reliability bookkeeping losing one sample is a non-event; the
        # briefing failing to send because a stale lock was held is not.
        print(f"[morning_briefing] reliability tracker skipped: {e}",
              file=sys.stderr)


def _record_reliability_locked(tracker_path: str, data: dict, warnings: list):
    try:
        if os.path.exists(tracker_path):
            with open(tracker_path) as f:
                tracker = json.load(f)
        else:
            tracker = {"tracking_start": datetime.now().strftime("%Y-%m-%d"), "days": []}
    except (json.JSONDecodeError, KeyError):
        tracker = {"tracking_start": datetime.now().strftime("%Y-%m-%d"), "days": []}

    try:
        from core.config_loader import config as _cfg
        _expected_kids = [k.name.lower() for k in _cfg.kids]
    except Exception:
        _expected_kids = []
    _meal_data = data.get("meal_suggestions", {}) or {}
    components = {
        "weather": data.get("weather") is not None,
        "calendar": isinstance(data.get("events"), list),
        "meals": bool(_expected_kids) and all(k in _meal_data for k in _expected_kids),
        "clothing": data.get("weather") is not None and isinstance(data.get("weather"), str) and "°" in data.get("weather", ""),
    }

    all_ok = all(components.values()) and not warnings
    status = "ok" if all_ok else "degraded"

    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": status,
        "delivered": True,
        "components": components,
    }
    if warnings:
        entry["notes"] = "; ".join(warnings)

    # Avoid duplicate entries for the same date
    tracker["days"] = [d for d in tracker["days"] if d.get("date") != entry["date"]]
    tracker["days"].append(entry)

    # Keep last 60 days
    tracker["days"] = tracker["days"][-60:]

    try:
        write_json_atomic(tracker_path, tracker)
    except Exception as e:
        print(f"Warning: could not write reliability tracker: {e}", file=sys.stderr)


def get_briefing_data() -> dict:
    """
    Collect all briefing data and return as a structured dict — no LLM, no WA send.
    The OpenClaw agent calls this via --data-only and composes the briefing message itself.
    """
    assistant = FamilyCalendarAggregator(SKILL_DIR)
    meals     = MealTracker(SKILL_DIR)
    snacks    = SnackManager(SKILL_DIR)

    assistant.sync_with_google_calendar(detect_restaurants=True, force=True)
    today_events = assistant.get_events_for_today()
    dropoffs     = has_dropoff_today(today_events)

    # Events with no title (e.g. work calendar busy blocks stripped by org
    # policy) carry no information worth showing in the family briefing.
    # The untitled event itself stays in the calendar cache — other readers
    # like the Club Studio recommender still need its time slot for
    # conflict checks — it's just excluded from what gets displayed here.
    visible_events = [e for e in today_events if e.get("title") != "Untitled"]

    # Where is the household today? A trip event on the calendar redirects the
    # forecast; without this the family reads Irvine's weather in another city
    # and dresses for it. Computed off the already-synced cache, no round-trip.
    from features.trips.travel_window import get_travel_window
    travel = get_travel_window(
        datetime.now().strftime("%Y-%m-%d"), list(assistant.calendar.values())
    )

    # The trip event itself is not a thing to do today. It only ever reaches
    # this list on departure day (get_events_by_date matches start dates), and
    # on that one day it would sit beside the flight under a header already
    # naming the destination — three statements of one fact.
    if travel.get("event_id"):
        visible_events = [e for e in visible_events
                          if e.get("id") != travel["event_id"]]

    try:
        from features.meals.weekly_meal_planner import get_todays_meals_from_locked_plan
        _locked = get_todays_meals_from_locked_plan()
        meal_suggestions = _locked if _locked else meals.get_meal_suggestions()
    except Exception:
        meal_suggestions = meals.get_meal_suggestions()

    # `weather_location` is empty on departure day — they wake up at home that
    # morning and this briefing is read in their own kitchen.
    weather_raw = get_weather_briefing(travel.get("weather_location") or None)

    # Away means the kids are not at their school, whatever the school calendar
    # says, so the daily snack menu is noise. This is a data question — there is
    # no snack — not a presentation one, so it is answered here rather than left
    # to the composer with a "skip this when travelling" instruction.
    #
    # Departure day is included: a midday flight means no school that morning
    # either, and a snack menu for a day the kids are on a plane is noise
    # whichever end of the trip it lands on.
    #
    # `snack_warning` deliberately still flows: it says next month's schedule is
    # due, which stays true and actionable-on-return, and suppressing it across
    # a trip that straddles a month boundary could swallow the only reminder.
    at_school     = not snacks.is_school_closed_today() and not travel["away"]
    snack_text    = snacks.format_for_briefing() if at_school else None
    # Ungated on purpose. `if not snack_text` looks like "don't nag when we
    # clearly have a schedule", but it never suppressed the missing-current-
    # month warning (that one cannot fire when a snack exists) and always
    # suppressed the end-of-month "send next month's photo" reminder, whose
    # whole window is normal school days with snacks. September 2026's
    # reminder was generated and discarded on every run of its window.
    snack_warning = snacks.should_warn_about_missing_schedule()

    data = {
        "date":             datetime.now().strftime("%A, %B %d"),
        "weather":          weather_raw,
        "events":           visible_events,
        "dropoffs":         dropoffs,
        "meal_suggestions": meal_suggestions,
        "snack":            snack_text,
        "snack_warning":    snack_warning,
        "school_day":       at_school,
        "travel":           travel,
        "daily_thought":    get_daily_thought(),
    }

    # ── Output validation ─────────────────────────────────────────────────
    warnings = validate_briefing_data(data)
    if warnings:
        data["warnings"] = warnings

    # ── Reliability tracking ──────────────────────────────────────────────
    _record_reliability(data, warnings)

    return data


if __name__ == "__main__":
    # Output structured JSON for the agent to compose and deliver the briefing.
    # Top-level guard: a crash here is the difference between "agent gets a
    # degraded payload it can still summarize" and "cron silently swallows
    # the morning briefing". Always emit valid JSON to stdout.
    try:
        _payload = get_briefing_data()
    except Exception as _e:
        import traceback
        _payload = {
            "status": "crashed",
            "error": str(_e),
            "traceback": traceback.format_exc(),
            "date": datetime.now().strftime("%A, %B %d"),
        }
        print(json.dumps(_payload, indent=2, default=str))
        sys.exit(1)
    print(json.dumps(_payload, indent=2, default=str))
