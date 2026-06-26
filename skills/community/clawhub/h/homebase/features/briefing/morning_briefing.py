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
from core.keychain_secrets import load_google_secrets
load_google_secrets()

from datetime import datetime
from features.calendar.calendar_aggregator import FamilyCalendarAggregator
from features.meals.meal_tracker import MealTracker
from features.school.snack_manager import SnackManager
from features.briefing.weather import get_weather_briefing
from utils import write_json_atomic


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


def is_school_day(snacks: SnackManager) -> bool:
    return not snacks.is_school_closed_today()


def format_briefing_message(events, meal_suggestions, dropoffs, snacks,
                             positive_message="Make today count.",
                             weather_text=None) -> str:
    today = datetime.now().strftime("%A, %B %d")
    lines = [f"🌅 *Morning Briefing — {today}*\n"]

    # ── Weather ───────────────────────────────────────────────────────────
    if weather_text:
        lines.append(weather_text)
        lines.append("")

    # ── Drop-off reminders (always at top) ───────────────────────────────
    if dropoffs:
        lines.append("🚗 *DROP-OFF TODAY*")
        for d in dropoffs:
            lines.append(f"  ⚠️ *{d['title']}* at {d.get('time', 'TBD')}")
        lines.append("")

    # ── Today's calendar events ───────────────────────────────────────────
    lines.append("📅 *Today's Events*")
    if events:
        for event in events:
            time_str = event.get('time', 'All day')
            if time_str in ("00:00", "All day"):
                display_time = "All day"
            else:
                h, m = map(int, time_str.split(':'))
                ampm = "AM" if h < 12 else "PM"
                h = h % 12 or 12
                display_time = f"{h}:{m:02d} {ampm}"
            lines.append(f"  • {event['title']} at {display_time}")
    else:
        lines.append("  No events today — enjoy the free day! 🎉")
    lines.append("")

    # ── School snacks (only on school days) ──────────────────────────────
    if is_school_day(snacks):
        snack_text = snacks.format_for_briefing()
        if snack_text:
            lines.append(snack_text)
            lines.append("")
        warning = snacks.should_warn_about_missing_schedule()
        if warning and not snack_text:
            lines.append(warning)
            lines.append("")

    # ── Meal plan ─────────────────────────────────────────────────────────
    lines.append("🍽️ *Kids Meal Plan*")
    for child_key, meals in meal_suggestions.items():
        name = meals.get("name", child_key.capitalize())
        lines.append(f"\n*{name}*")
        lines.append(f"  Breakfast: {meals['breakfast']}")
        lines.append(f"  Lunch: {meals['lunch']}")
        lines.append(f"  Side: {meals['side']}")
        if meals.get("note"):
            lines.append(f"  _{meals['note']}_")

    # ── Positive message ────────
    if positive_message:
        lines.append(f"\n_{positive_message}_")

    return "\n".join(lines)


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

    assistant.sync_with_google_calendar()
    today_events = assistant.get_events_for_today()
    dropoffs     = has_dropoff_today(today_events)

    try:
        from features.meals.weekly_meal_planner import get_todays_meals_from_locked_plan
        _locked = get_todays_meals_from_locked_plan()
        meal_suggestions = _locked if _locked else meals.get_meal_suggestions()
    except Exception:
        meal_suggestions = meals.get_meal_suggestions()

    weather_raw = get_weather_briefing()

    snack_text    = snacks.format_for_briefing() if not snacks.is_school_closed_today() else None
    snack_warning = snacks.should_warn_about_missing_schedule() if not snack_text else None

    data = {
        "date":             datetime.now().strftime("%A, %B %d"),
        "weather":          weather_raw,
        "events":           today_events,
        "dropoffs":         dropoffs,
        "meal_suggestions": meal_suggestions,
        "snack":            snack_text,
        "snack_warning":    snack_warning,
        "school_day":       not snacks.is_school_closed_today(),
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
