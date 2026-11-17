#!/usr/bin/env python3
"""
trip_detector.py — Trip Prep Candidate Lister

Lists upcoming non-recurring calendar events as candidates. The OpenClaw
agent (per skill CLAUDE.md principle 2) decides which (if any) are real
trips needing prep, fetches destination weather/env tags via tools.py
get_trip_data, composes the prep note, and calls tools.py
mark_trip_prep_sent to dedup.

Usage (CLI / cron):
    python -m features.trips.trip_detector --check
        List candidate events as JSON for the agent to judge.
    python -m features.trips.trip_detector --trip "Big Bear" --location "Big Bear Lake, CA"
        Manual single-trip data fetch (used by tools.py get_trip_data).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple

from core.config_loader import SKILL_DIR
from utils import write_json_atomic

# ─── Constants ────────────────────────────────────────────────────────────────

TRIP_KEYWORDS = [
    "trip", "vacation", "staycation", "visit", "drive to",
    "weekend", "getaway", "road trip", "travel",
]

HOUSEHOLD_DIR   = os.path.join(SKILL_DIR, "household")
PROFILES_PATH   = os.path.join(HOUSEHOLD_DIR, "kid_profiles.json")
SENT_PATH       = os.path.join(HOUSEHOLD_DIR, "trip_prep_sent.json")

# Environment tag inference rules: (keyword_in_title_or_location → tags)
ENV_RULES: List[Tuple[List[str], List[str]]] = [
    (["big bear", "mammoth", "tahoe", "yosemite", "mountain", "alpine", "summit",
      "trail", "ski", "snow", "cabin", "julian", "idyllwild"],
     ["mountain", "high_altitude", "dry", "winding_roads", "long_drive", "cold"]),
    (["beach", "malibu", "laguna", "santa monica", "san clemente", "oceanside",
      "ventura", "huntington", "newport", "pacific coast", "ocean", "surf"],
     ["beach", "humid", "sunny", "uv_high"]),
    (["desert", "palm springs", "joshua tree", "scottsdale", "phoenix", "las vegas",
      "death valley", "sedona"],
     ["desert", "dry", "hot", "uv_high"]),
    (["las vegas", "new york", "chicago", "seattle", "san francisco", "denver",
      "portland", "boston", "washington"],
     ["urban", "flight"]),
    (["fly", "flight", "airport", "lax", "sfo", "jfk"],
     ["flight"]),
    (["drive", "road", "freeway", "highway"],
     ["long_drive"]),
]


# ─── Profile helpers ──────────────────────────────────────────────────────────

def load_kid_profiles() -> Dict:
    """Load kid_profiles.json. Returns empty dict if file missing."""
    if not os.path.exists(PROFILES_PATH):
        return {}
    with open(PROFILES_PATH, "r") as f:
        return json.load(f)


def save_kid_profiles(profiles: Dict) -> None:
    write_json_atomic(PROFILES_PATH, profiles)


def load_sent_log() -> Dict:
    if not os.path.exists(SENT_PATH):
        return {}
    with open(SENT_PATH, "r") as f:
        return json.load(f)


def save_sent_log(log: Dict) -> None:
    write_json_atomic(SENT_PATH, log)


def log_kid_observation(
    child: str,
    text: str,
    category: str = "general",
    tags: Optional[List[str]] = None,
    trip_context: Optional[str] = None,
) -> str:
    """
    Append a new observation to a child's profile.
    Returns a short confirmation string.
    """
    import uuid

    profiles = load_kid_profiles()
    child_key = child.strip().title()
    if child_key not in profiles:
        profiles[child_key] = {"observations": []}

    entry = {
        "id":           str(uuid.uuid4()),
        "text":         text.strip(),
        "category":     category,
        "tags":         tags or [],
        "source":       "passive",
        "logged_at":    datetime.now().isoformat(),
        "trip_context": trip_context,
    }
    profiles[child_key]["observations"].append(entry)
    save_kid_profiles(profiles)
    return f"Got it — noted for {child_key} 👍"


def get_kid_profile(child: str) -> str:
    """Return a readable summary of a child's full profile."""
    profiles = load_kid_profiles()
    child_key = child.strip().title()
    data = profiles.get(child_key, {})
    obs  = data.get("observations", [])
    if not obs:
        return f"No profile observations logged yet for {child_key}."
    lines = [f"👤 *{child_key}'s Profile* ({len(obs)} observations)\n"]
    for o in obs:
        tags_str = ", ".join(o.get("tags", [])) or "—"
        ctx      = f"  _(trip: {o['trip_context']})_" if o.get("trip_context") else ""
        lines.append(f"• [{o['category']}] {o['text']}  tags: {tags_str}{ctx}")
    return "\n".join(lines)


# ─── Calendar helpers ─────────────────────────────────────────────────────────

def list_candidate_events(events: List[Dict]) -> List[Dict]:
    """
    List upcoming non-recurring calendar events for the agent to judge.

    Python no longer pre-filters by keyword or location — the trip-vs-not
    decision belongs to the agent (see skill CLAUDE.md principle 2).

    Recurring events are skipped UNLESS their title contains a trip keyword
    (covers cases like "Annual cabin trip" recurring yearly).

    Each candidate ships with a sent_key and already_sent flag so the agent
    can dedup against trip_prep_sent.json without a second tool call.

    Takes already-fetched events rather than a calendar service (2026-09-07).
    Fetching moved to the caller so this is a pure function over data: the
    tests hand it dicts and mock nothing, and it cannot reach the network by
    accident.

    Returns list of dicts: {event_id, title, start_date, end_date, all_day,
    multiday, location, sent_key, already_sent}.
    """
    sent = load_sent_log()
    candidates: List[Dict] = []

    for event in events:
        title = event.get("summary", "").strip()
        if not title:
            continue

        is_recurring = bool(event.get("recurringEventId"))
        title_lower  = title.lower()
        if is_recurring and not any(kw in title_lower for kw in TRIP_KEYWORDS):
            continue

        location = (event.get("location") or "").strip()
        start    = event.get("start", {})
        end      = event.get("end", {})
        start_date = start.get("date") or (start.get("dateTime") or "")[:10]
        end_date   = end.get("date")   or (end.get("dateTime")   or "")[:10]
        all_day    = bool(start.get("date"))

        sent_key = f"{event.get('id', '')}:{start_date}"
        candidates.append({
            "event_id":     event.get("id", ""),
            "title":        title,
            "start_date":   start_date,
            "end_date":     end_date,
            "all_day":      all_day,
            "multiday":     all_day and start_date != end_date,
            "location":     location,
            "sent_key":     sent_key,
            "already_sent": sent_key in sent,
        })

    return candidates


def _get_calendar_id() -> str:
    try:
        from core.config_loader import config
        return config.calendar_id
    except Exception:
        return ""


# ─── Destination intelligence ─────────────────────────────────────────────────

def infer_environment_tags(title: str, location: str) -> List[str]:
    """
    Infer environment tags from event title + location string.
    Combines matching across all ENV_RULES — no single-match short-circuit.
    """
    combined = (title + " " + location).lower()
    tags: List[str] = []
    for keywords, env_tags in ENV_RULES:
        if any(kw in combined for kw in keywords):
            for t in env_tags:
                if t not in tags:
                    tags.append(t)
    return tags


def geocode_location(location: str) -> Optional[Tuple[float, float]]:
    """Geocode a location string to (lat, lon).

    Thin re-export of features.briefing.weather.geocode_location — this module
    used to carry a byte-for-byte-equivalent second copy, neither of them
    cached. One implementation, one cache.
    """
    from features.briefing.weather import geocode_location as _geocode
    return _geocode(location)


def fetch_trip_weather(location: str, start_date: str, end_date: str) -> Optional[Dict]:
    """
    Fetch weather forecast for a destination during the trip dates.
    Uses weather.py's fetch_weather() with location overrides.
    Falls back to inline Open-Meteo call if geocoding succeeds.
    """
    from features.briefing.weather import fetch_weather as _fetch_local, weather_code_to_description

    coords = geocode_location(location)
    if coords:
        lat, lon = coords
        # Determine forecast_days needed (at least 1, at most 7)
        try:
            d1 = datetime.strptime(end_date, "%Y-%m-%d")
            days_needed = max(1, (d1 - datetime.now()).days + 2)
            days_needed = min(days_needed, 7)
        except ValueError:
            days_needed = 3

        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,apparent_temperature,weather_code,"
            f"wind_speed_10m,relative_humidity_2m"
            f"&daily=temperature_2m_max,temperature_2m_min,"
            f"precipitation_probability_max,relative_humidity_2m_max"
            f"&temperature_unit=fahrenheit"
            f"&wind_speed_unit=mph"
            f"&timezone=auto"     # the destination's own local time
            f"&forecast_days={days_needed}"
        )
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                data = json.loads(resp.read().decode())

            current = data.get("current", {})
            daily   = data.get("daily", {})
            code    = current.get("weather_code", 0)

            # Pick the day index corresponding to trip start
            try:
                today = datetime.now().date()
                trip_day = (datetime.strptime(start_date, "%Y-%m-%d").date() - today).days
                trip_day = max(0, min(trip_day, days_needed - 1))
            except ValueError:
                trip_day = 0

            highs = daily.get("temperature_2m_max") or []
            lows  = daily.get("temperature_2m_min")  or []
            rain  = daily.get("precipitation_probability_max") or []
            humid = daily.get("relative_humidity_2m_max") or []

            # Average humidity across trip dates
            end_day = trip_day + max(1, (datetime.strptime(end_date, "%Y-%m-%d").date()
                                        - datetime.strptime(start_date, "%Y-%m-%d").date()).days + 1)
            end_day = min(end_day, len(humid))
            avg_humidity = (
                round(sum(humid[trip_day:end_day]) / max(1, end_day - trip_day))
                if humid else round(current.get("relative_humidity_2m", 0))
            )

            return {
                "temp_current":    round(current.get("temperature_2m", 0)),
                "temp_feels_like": round(current.get("apparent_temperature", 0)),
                "temp_high":       round(highs[trip_day]) if highs else 0,
                "temp_low":        round(lows[trip_day])  if lows  else 0,
                "condition":       weather_code_to_description(code),
                "wind_speed":      round(current.get("wind_speed_10m", 0)),
                "humidity":        avg_humidity,
                "rain_chance":     rain[trip_day] if rain else 0,
                "location":        location,
            }
        except Exception as e:
            print(f"[trip_detector] weather fetch failed: {e}", file=sys.stderr)

    # Fallback — home weather (better than nothing)
    return _fetch_local()


# ─── Cron / CLI entrypoint ────────────────────────────────────────────────────

def run_check() -> None:
    """
    List upcoming non-recurring events for the agent to judge.

    The agent decides which (if any) qualify as real trips needing prep,
    fetches weather/env tags via tools.py get_trip_data for the chosen one,
    composes a prep note, and calls tools.py mark_trip_prep_sent to dedup.
    """
    from core import gcal

    # The fetch lives here now; list_candidate_events is pure.
    now     = datetime.now(timezone.utc)
    horizon = now + timedelta(days=4)
    events  = gcal.list_events(
        _get_calendar_id(), now.isoformat(), horizon.isoformat()
    )
    candidates = list_candidate_events(events)
    profiles   = load_kid_profiles()

    print(json.dumps({
        "status":     "candidates",
        "candidates": candidates,
        "profiles":   {k: v.get("observations", []) for k, v in profiles.items()},
    }, default=str))


def mark_sent(sent_key: str, trip_title: str, start_date: str) -> None:
    """Record that trip prep was sent (called by tools.py after the agent sends the message)."""
    sent = load_sent_log()
    sent[sent_key] = {
        "title":      trip_title,
        "sent_at":    datetime.now().isoformat(),
        "start_date": start_date,
    }
    save_sent_log(sent)


def run_manual(event_title: str, location: str) -> str:
    """Return structured trip data JSON without calendar lookup (used by tools.py get_trip_data)."""
    profiles = load_kid_profiles()
    trip = {
        "event_id":   "manual",
        "title":      event_title,
        "start_date": datetime.now().strftime("%Y-%m-%d"),
        "end_date":   datetime.now().strftime("%Y-%m-%d"),
        "location":   location,
    }
    env_tags = infer_environment_tags(event_title, location)
    weather  = fetch_trip_weather(location or event_title, trip["start_date"], trip["end_date"])
    return json.dumps({
        "trip":     trip,
        "env_tags": env_tags,
        "weather":  weather,
        "profiles": {k: v.get("observations", []) for k, v in profiles.items()},
    }, default=str)



# ─── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trip prep candidate lister")
    parser.add_argument("--check",    action="store_true",
                        help="List upcoming non-recurring events for the agent to judge")
    parser.add_argument("--trip",     type=str, default="",
                        help="Manual trip title (for tools.py get_trip_data)")
    parser.add_argument("--location", type=str, default="",
                        help="Destination location string")
    args = parser.parse_args()

    # Top-level guard so cron always exits cleanly with a parseable status.
    import traceback as _tb
    try:
        if args.check:
            run_check()
        elif args.trip:
            msg = run_manual(args.trip, args.location)
            print(msg)
        else:
            parser.print_help()
    except Exception as _e:
        print(json.dumps({
            "status": "crashed",
            "error": str(_e),
            "traceback": _tb.format_exc(),
        }, indent=2))
        sys.exit(1)
