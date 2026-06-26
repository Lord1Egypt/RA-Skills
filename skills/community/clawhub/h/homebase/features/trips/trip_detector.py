#!/usr/bin/env python3
"""
trip_detector.py — Proactive Trip Prep System

Detects upcoming family trips from the Google Calendar, builds a destination
intelligence object (environment type + live weather forecast), runs the kids'
profiles through the LLM to find relevant observations, and composes a
WhatsApp-ready prep message.

Usage (CLI / cron):
    python -m features.trips.trip_detector --check     # check, surface if not yet sent
    python -m features.trips.trip_detector --dry-run   # same but print instead of sending
    python -m features.trips.trip_detector --trip "Big Bear" --location "Big Bear Lake, CA"
                                                       # manually trigger for a named trip
"""

from __future__ import annotations

import argparse
import json
import os
import re
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

def find_upcoming_trips(calendar_service, days_ahead: int = 4) -> List[Dict]:
    """
    Fetch calendar events in the next `days_ahead` days and flag 'trip' events.

    An event is considered a trip if ANY of:
    - Title contains a trip keyword
    - Event has a non-empty location field
    - Event spans multiple days (all-day multi-day)

    Returns list of dicts: {event_id, title, start_date, end_date, location}
    """
    now     = datetime.now(timezone.utc)
    horizon = now + timedelta(days=days_ahead)

    results = calendar_service.events().list(
        calendarId=_get_calendar_id(),
        timeMin=now.isoformat(),
        timeMax=horizon.isoformat(),
        maxResults=50,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    trips: List[Dict] = []
    for event in results.get("items", []):
        title    = event.get("summary", "")
        location = (event.get("location") or "").strip()
        start    = event.get("start", {})
        end      = event.get("end", {})

        start_date = start.get("date") or (start.get("dateTime") or "")[:10]
        end_date   = end.get("date")   or (end.get("dateTime")   or "")[:10]

        # Determine if trip
        title_lower = title.lower()
        is_trip = False

        # 1. keyword in title
        if any(kw in title_lower for kw in TRIP_KEYWORDS):
            is_trip = True

        # 2. has a location
        if location:
            is_trip = True

        # 3. multi-day all-day event WITH a location or trip keyword
        #    (without this guard, "Pay HOA Fees" spanning 2 days triggers a false trip)
        if start.get("date") and end.get("date") and start_date != end_date:
            if location or any(kw in title_lower for kw in TRIP_KEYWORDS):
                is_trip = True

        if is_trip:
            trips.append({
                "event_id":   event.get("id", ""),
                "title":      title,
                "start_date": start_date,
                "end_date":   end_date,
                "location":   location,
            })

    return trips


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
    """
    Geocode a location string to (lat, lon) using the free Open-Meteo geocoding API.
    Returns None on failure.
    """
    if not location:
        return None
    try:
        import urllib.parse, urllib.request  # noqa: PLC0415 (local import fine)
        encoded = urllib.parse.quote(location)
        url = (
            f"https://geocoding-api.open-meteo.com/v1/search"
            f"?name={encoded}&count=1&language=en&format=json"
        )
        with urllib.request.urlopen(url, timeout=8) as resp:
            data = json.loads(resp.read().decode())
        results = data.get("results", [])
        if results:
            return results[0]["latitude"], results[0]["longitude"]
    except Exception as e:
        print(f"[trip_detector] geocode failed for '{location}': {e}", file=sys.stderr)
    return None


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
            d0 = datetime.strptime(start_date, "%Y-%m-%d")
            d1 = datetime.strptime(end_date,   "%Y-%m-%d")
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
            f"&timezone=America%2FLos_Angeles"
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


def _fallback_trip_prep(trip: Dict, weather: Optional[Dict],
                        env_tags: List[str], profiles: Dict) -> str:
    """Simple non-LLM fallback message."""
    title = trip.get("title", "Upcoming Trip")
    start = trip.get("start_date", "")
    try:
        dt     = datetime.strptime(start, "%Y-%m-%d")
        days   = (dt.date() - datetime.now().date()).days
        label  = f"{dt.strftime('%a, %b %-d')} · {days} days away"
    except ValueError:
        label = start

    lines = [f"🏔️ *Trip Prep — {title} ({label})*\n"]
    if weather:
        lines.append(
            f"🌤️ *Weather there:* {weather['temp_low']}–{weather['temp_high']}°F, "
            f"{weather['condition']} · Humidity {weather['humidity']}%\n"
        )
    # Look up kid emoji from config, fall back to generic child emoji
    kid_emojis = {}
    try:
        from core.config_loader import config
        for kid in config.kids:
            kid_emojis[kid.name] = kid.emoji_char
    except Exception:
        pass
    for child, data in profiles.items():
        obs = data.get("observations", [])
        emoji = kid_emojis.get(child, "\U0001F9D2")
        if obs:
            lines.append(f"{emoji} *{child}*")
            for o in obs:
                lines.append(f"• {o['text']}")
            lines.append("")
    return "\n".join(lines)


# ─── Cron / CLI entrypoint ────────────────────────────────────────────────────

def run_check(dry_run: bool = False) -> None:
    """
    Cron logic — native mode:
    Outputs structured JSON for the agent to compose and send the prep message.
    The agent then calls tools.py mark_trip_prep_sent to record the send.
    """
    from core.keychain_secrets import load_google_secrets
    load_google_secrets()
    from features.calendar.calendar_manager import get_calendar_service

    service  = get_calendar_service()
    trips    = find_upcoming_trips(service, days_ahead=4)
    sent     = load_sent_log()
    profiles = load_kid_profiles()

    if not trips:
        print(json.dumps({"status": "no_trip"}))
        return

    for trip in trips:
        sent_key = f"{trip['event_id']}:{trip['start_date']}"
        if sent_key in sent:
            continue

        env_tags = infer_environment_tags(trip["title"], trip["location"])
        weather  = fetch_trip_weather(
            trip["location"] or trip["title"],
            trip["start_date"],
            trip["end_date"],
        )

        # Output structured data — the agent composes the message and sends it
        print(json.dumps({
            "status":   "trip_found",
            "sent_key": sent_key,
            "trip":     trip,
            "env_tags": env_tags,
            "weather":  weather,
            "profiles": {k: v.get("observations", []) for k, v in profiles.items()},
        }, default=str))
        return   # one trip at a time

    print(json.dumps({"status": "no_trip"}))


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
    parser = argparse.ArgumentParser(description="Trip prep detector")
    parser.add_argument("--check",    action="store_true",
                        help="Check for upcoming trips and send prep (idempotent)")
    parser.add_argument("--dry-run",  action="store_true",
                        help="Like --check but prints instead of sending")
    parser.add_argument("--trip",     type=str, default="",
                        help="Manually named trip title")
    parser.add_argument("--location", type=str, default="",
                        help="Destination location string")
    args = parser.parse_args()

    # Top-level guard so cron always exits cleanly with a parseable status.
    import traceback as _tb
    try:
        if args.check or args.dry_run:
            run_check(dry_run=args.dry_run)
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
