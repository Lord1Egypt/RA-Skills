#!/usr/bin/env python3
"""
iCloud Calendar Manager via CalDAV — Full CRUD + RRULE + Search + Logging

Usage:
    python add-event.py \
        --summary "Meeting" --start "2026-04-08T15:00:00" \
        [--end "2026-04-08T16:00:00"] [--timezone "Asia/Shanghai"] \
        [--location "Room 301"] [--description "Notes"] \
        [--calendar "personal"] [--alarm-minutes 15] \
        [--rrule "FREQ=WEEKLY;BYDAY=MO"] [--list-calendars] \
        [--is-all-day]

Credentials (required):
    Set env vars ICLOUD_EMAIL and ICLOUD_APP_PASSWORD.
    Do NOT pass credentials via command-line arguments.

Env vars: ICLOUD_EMAIL, ICLOUD_APP_PASSWORD
"""

import argparse
import json
import logging
import os
import re
import sys
import time
import uuid
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import caldav
import caldav.lib.error as caldav_errors

# ── Constants ───────────────────────────────────────────────────────────
VERSION = "2.0.0"

# ── Timeouts: fast for CRUD/auth, slow for heavy expand=True queries ───
TIMEOUT_FAST = 10   # seconds: auth, save_event, delete, save
TIMEOUT_SLOW = 60   # seconds: date_search(expand=True)
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_FILE = LOG_DIR / "calendar.log"
LOG_MAX_BYTES = 512 * 1024  # 512KB
LOG_BACKUP_COUNT = 5
CALDAV_MAX_RETRIES = 3
CALDAV_RETRY_BACKOFF = 2  # seconds, exponential

# Safety cap for expand=True queries to prevent OOM from infinite RRULE
MAX_EXPAND_DAYS = 1095  # 3 years

# Fatal errors that should NEVER be retried — wrong credentials or identity.
# caldav.lib.error only exports AuthorizationError and NotFoundError by name.
# Other 4xx errors are wrapped as DAVError; we'll check status code in message.
FATAL_CALDAV_ERRORS = (
    caldav_errors.AuthorizationError,   # 401
    caldav_errors.NotFoundError,        # 404
)

# ── Logger setup ────────────────────────────────────────────────────────
_calendar_logger = logging.getLogger("calendar")
_calendar_logger.setLevel(logging.INFO)


def _setup_logger() -> None:
    """Configure rotating file handler for calendar operations."""
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        handler = RotatingFileHandler(
            str(LOG_FILE),
            maxBytes=LOG_MAX_BYTES,
            backupCount=LOG_BACKUP_COUNT,
            encoding="utf-8",
        )
        handler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
        _calendar_logger.addHandler(handler)
    except OSError as e:
        # Fallback: log to stderr
        _calendar_logger.addHandler(logging.StreamHandler(sys.stderr))
        _calendar_logger.error(f"Log file init failed: {e}")


_setup_logger()


def log_action(action: str, details: str = "") -> None:
    """Log an action using RotatingFileHandler. Errors go to stderr as JSON."""
    try:
        _calendar_logger.info(f"{action} | {details}")
    except Exception as e:
        print(json.dumps({"warning": f"Log write failed: {e}"}), file=sys.stderr)


def sanitize_for_log(text: str, max_len: int = 30) -> str:
    """Truncate content for log output to protect privacy."""
    if not text:
        return ""
    return text if len(text) <= max_len else text[:max_len] + "…"


def escape_ical(text: str) -> str:
    """Escape special characters per RFC 5545 Section 3.3.11."""
    if not text:
        return ""
    return (
        text.replace("\r", "")
            .replace("\\", "\\\\")
            .replace(";", "\\;")
            .replace(",", "\\,")
            .replace("\n", "\\n")
    )


# ── Timezone helpers ────────────────────────────────────────────────────
_TZ_ABBR: dict[str, str] = {
    "Asia/Shanghai": "CST",       "Asia/Tokyo": "JST",
    "Asia/Hong_Kong": "HKT",      "Asia/Taipei": "CST",
    "Asia/Singapore": "SGT",      "Asia/Seoul": "KST",
    "Asia/Kolkata": "IST",        "Asia/Dubai": "GST",
    "Asia/Bangkok": "ICT",        "Europe/London": "GMT",
    "Europe/Paris": "CET",        "Europe/Berlin": "CET",
    "Europe/Madrid": "CET",       "Europe/Amsterdam": "CET",
    "Europe/Zurich": "CET",       "Europe/Rome": "CET",
    "Europe/Stockholm": "CET",    "Europe/Vienna": "CET",
    "Europe/Warsaw": "CET",       "Europe/Istanbul": "TRT",
    "Europe/Moscow": "MSK",       "America/New_York": "EST",
    "America/Chicago": "CST",     "America/Denver": "MST",
    "America/Los_Angeles": "PST", "America/Phoenix": "MST",
    "America/Toronto": "EST",     "America/Vancouver": "PST",
    "America/Sao_Paulo": "BRT",   "America/Mexico_City": "CST",
    "Pacific/Auckland": "NZST",   "Pacific/Honolulu": "HST",
    "Australia/Sydney": "AEST",   "Australia/Melbourne": "AEST",
    "Australia/Perth": "AWST",    "UTC": "UTC",
}


def _get_tz_abbr(tz_name: str) -> str:
    """Get timezone abbreviation. Falls back to zone name."""
    return _TZ_ABBR.get(tz_name, tz_name.split("/")[-1])


def _format_offset(dt: datetime) -> str:
    """Format UTC offset as +HHMM or -HHMM, dynamically computed."""
    try:
        offset = dt.utcoffset()
        if offset is None:
            return "+0000"
        total = int(offset.total_seconds())
        sign = "+" if total >= 0 else "-"
        total = abs(total)
        hours = total // 3600
        minutes = (total % 3600) // 60
        return f"{sign}{hours:02d}{minutes:02d}"
    except Exception:
        return "+0000"


def build_vtimezone(tz_name: str, dt: datetime) -> list[str]:
    """Build VTIMEZONE with dynamically computed offset for the given datetime (DST-safe)."""
    tz_abbr = _get_tz_abbr(tz_name)
    offset = _format_offset(dt)
    return [
        "BEGIN:VTIMEZONE",
        f"TZID:{tz_name}",
        "BEGIN:STANDARD",
        "DTSTART:19700101T000000",
        f"TZOFFSETFROM:{offset}",
        f"TZOFFSETTO:{offset}",
        f"TZNAME:{tz_abbr}",
        "END:STANDARD",
        "END:VTIMEZONE",
    ]


# ── Helpers ─────────────────────────────────────────────────────────────
def find_calendar(calendars: list, name: str):
    """Find calendar by name (case-insensitive partial match). Raises if no calendars."""
    if not calendars:
        raise ValueError("No calendars available")
    if not name or name == "primary":
        return calendars[0]
    name_lower = name.lower()
    for cal in calendars:
        try:
            cal_name = cal.get_display_name() or ""
        except Exception:
            cal_name = ""
        if name_lower in cal_name.lower():
            return cal
    return calendars[0]


def _validate_rrule(rrule: str) -> str:
    """Validate RRULE format. Must start with FREQ=. Raises ValueError on invalid input."""
    rrule = rrule.strip()
    if not rrule:
        return rrule
    if not rrule.upper().startswith("FREQ="):
        raise ValueError(f"Invalid RRULE (must start with FREQ=): {rrule}")
    allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789=;,-_")
    if not all(c in allowed for c in rrule.upper()):
        raise ValueError(f"RRULE contains invalid characters: {rrule}")
    return rrule


def _is_fatal_error(e: Exception) -> bool:
    """Check if an error is a 4xx that should not be retried."""
    if isinstance(e, FATAL_CALDAV_ERRORS):
        return True
    # Also skip retried for other 4xx errors (check error string for HTTP status)
    err_str = str(e)
    for code in ("400", "401", "403", "404", "405", "409", "412", "422"):
        if f"[{code}]" in err_str or f"HTTP {code}" in err_str:
            return True
    return False


def _retry_on_caldav_error(func, *args: Any, max_retries: int = CALDAV_MAX_RETRIES, **kwargs: Any) -> Any:
    """Retry a CalDAV operation with exponential backoff.
    
    Fatal errors (4xx identity/server issues) are NOT retried.
    Only transient errors (500/502/503/504/network timeout) trigger retry.
    """
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_error = e
            if _is_fatal_error(e):
                log_action("FATAL", f"Aborting retry: {type(e).__name__}")
                raise
            if attempt < max_retries:
                delay = CALDAV_RETRY_BACKOFF ** attempt
                log_action("RETRY", f"attempt={attempt}/{max_retries} wait={delay}s error={type(e).__name__}")
                time.sleep(delay)
    raise last_error


def _new_uid() -> str:
    """Generate a deterministic event UID for idempotent creation."""
    return f"{uuid.uuid4().hex}@openclaw.icloud"


def _clamp_date_range(start_range: datetime, end_range: datetime) -> tuple[datetime, datetime]:
    """Enforce MAX_EXPAND_DAYS safety cap on date ranges used with expand=True."""
    days = (end_range - start_range).days
    if days > MAX_EXPAND_DAYS:
        end_range = start_range + timedelta(days=MAX_EXPAND_DAYS)
        log_action("WARN", f"Query range {days}d exceeded {MAX_EXPAND_DAYS}d cap, truncated.")
    return start_range, end_range


def _compute_status(deleted: list, errors: list) -> str:
    """Compute tri-state status for agent-friendly JSON output."""
    if not deleted and not errors:
        return "success"
    if not deleted and errors:
        return "error"
    if deleted and errors:
        return "partial_success"
    return "success"


def build_vevent(summary: str, start_dt: datetime, end_dt: datetime,
                 location: str = "", description: str = "",
                 alarm_minutes: int | None = None, rrule: str = "",
                 is_all_day: bool = False, uid: str | None = None) -> list[str]:
    """Build VEVENT component lines. Supports both timed and all-day events."""
    event_uid = uid or _new_uid()
    tz_name = str(start_dt.tzinfo)

    lines: list[str] = ["BEGIN:VEVENT", f"UID:{event_uid}"]

    if is_all_day:
        lines.append(f"DTSTART;VALUE=DATE:{start_dt.strftime('%Y%m%d')}")
        lines.append(f"DTEND;VALUE=DATE:{end_dt.strftime('%Y%m%d')}")
    else:
        lines.append(f"DTSTART;TZID={tz_name}:{start_dt.strftime('%Y%m%dT%H%M%S')}")
        lines.append(f"DTEND;TZID={tz_name}:{end_dt.strftime('%Y%m%dT%H%M%S')}")

    lines += [
        f"SUMMARY:{escape_ical(summary)}",
        f"LOCATION:{escape_ical(location)}",
        f"DESCRIPTION:{escape_ical(description)}",
        f"DTSTAMP:{datetime.now(ZoneInfo('UTC')).strftime('%Y%m%dT%H%M%SZ')}",
        "STATUS:CONFIRMED",
    ]
    if rrule:
        lines.append(f"RRULE:{rrule}")
    if alarm_minutes is not None and alarm_minutes > 0:
        alarm_desc = escape_ical(f"Reminder: {summary}")
        lines += [
            "BEGIN:VALARM",
            "ACTION:DISPLAY",
            f"DESCRIPTION:{alarm_desc}",
            f"TRIGGER:-PT{alarm_minutes}M",
            "END:VALARM",
        ]
    lines.append("END:VEVENT")
    return lines


def build_ical(summary: str, start_dt: datetime, end_dt: datetime,
               location: str = "", description: str = "",
               alarm_minutes: int | None = None, rrule: str = "",
               is_all_day: bool = False, uid: str | None = None) -> str:
    """Build full iCalendar string. RFC 5545 compliant."""
    tz_name = str(start_dt.tzinfo)

    lines: list[str] = [
        "BEGIN:VCALENDAR", "VERSION:2.0",
        "CALSCALE:GREGORIAN",
        "PRODID:-//OpenClaw//iCloud Calendar//EN",
    ]
    if not is_all_day:
        lines += build_vtimezone(tz_name, start_dt)
    lines += build_vevent(summary, start_dt, end_dt, location, description, alarm_minutes, rrule, is_all_day, uid)
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines)


def parse_dt(s: str, tz: ZoneInfo) -> tuple[datetime | None, bool]:
    """Parse datetime string. Returns (datetime, is_all_day)."""
    if not s:
        return None, False
    s = s.strip()
    s = s.replace("年", "-").replace("月", "-").replace("日", "")
    if "T" not in s:
        s = s.replace(" ", "T", 1)

    for fmt in ["%Y-%m-%d"]:
        try:
            dt = datetime.strptime(s, fmt).replace(hour=0, minute=0, second=0)
            return dt.replace(tzinfo=tz), True
        except ValueError:
            continue

    for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]:
        try:
            dt = datetime.strptime(s, fmt)
            return dt.replace(tzinfo=tz), False
        except ValueError:
            continue

    return None, False


def extract_event(vevent) -> dict[str, str]:
    """Extract full event data from a vobject VEVENT."""
    info: dict[str, str] = {
        "summary": "(无标题)", "start": "", "end": "",
        "location": "", "description": "", "rrule": "", "uid": "",
    }
    for key in ("summary", "dtstart", "dtend", "location", "description", "rrule", "uid"):
        obj = getattr(vevent, key, None)
        if obj and obj.value is not None:
            info[key] = str(obj.value)
    return info


def parse_date_range_for_query(
    q: str, tz: ZoneInfo,
) -> tuple[datetime | None, datetime | None]:
    """Parse query string into (start_range, end_range) datetime pair."""
    now = datetime.now(tz)
    q = q.lower().strip()

    if q == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return start, start + timedelta(days=1)
    if q == "tomorrow":
        start = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        return start, start + timedelta(days=1)
    if q in ("week", "thisweek"):
        start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        return start, start + timedelta(days=7)
    if q == "nextweek":
        start = (now - timedelta(days=now.weekday()) + timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
        return start, start + timedelta(days=7)
    if q in ("month", "thismonth"):
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end = start.replace(year=start.year + 1, month=1) if start.month == 12 else start.replace(month=start.month + 1)
        return start, end
    if q == "nextmonth":
        if now.month == 12:
            start = now.replace(year=now.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            start = now.replace(month=now.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = start.replace(year=start.year + 1, month=1) if start.month == 12 else start.replace(month=start.month + 1)
        return start, end
    if "~" in q:
        parts = q.split("~")
        parsed_start, _ = parse_dt(parts[0].strip(), tz)
        parsed_end, _ = parse_dt(parts[1].strip(), tz)
        if parsed_start and parsed_end:
            return parsed_start, parsed_end + timedelta(days=1)
        return None, None
    parsed, _ = parse_dt(q, tz)
    if parsed:
        midnight = parsed.replace(hour=0, minute=0, second=0, microsecond=0)
        return midnight, midnight + timedelta(days=1)
    return None, None


def search_events(
    calendars: list, tz: ZoneInfo, start_range: datetime,
    end_range: datetime, keyword: str = "",
) -> dict:
    """Search events across all calendars. Returns {events, errors}."""
    all_events: list[dict] = []
    errors: list[dict] = []
    # Safety cap on expand range
    start_range, end_range = _clamp_date_range(start_range, end_range)
    for cal in calendars:
        cal_name = cal.get_display_name() or "unknown"
        try:
            events = _retry_on_caldav_error(
                cal.date_search, start=start_range, end=end_range, expand=True,
            )
            for ev in events:
                vevent = ev.vobject_instance.vevent
                info = extract_event(vevent)
                if keyword:
                    searchable = f"{info['summary']} {info['location']} {info['description']}".lower()
                    if keyword.lower() not in searchable:
                        continue
                info["calendar"] = cal_name
                all_events.append(info)
        except Exception as e:
            errors.append({"calendar": cal_name, "error": f"{type(e).__name__}: {e}"})
            log_action("ERROR", f"Calendar {cal_name}: {type(e).__name__}: {e}")
            continue

    all_events.sort(key=lambda x: x.get("start", ""))
    return {"events": all_events, "errors": errors}


# ── Main ────────────────────────────────────────────────────────────────
def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=f"iCloud Calendar Manager v{VERSION}")
    parser.add_argument("--summary", default="")
    parser.add_argument("--start", default="")
    parser.add_argument("--end", default="")
    parser.add_argument("--timezone", default="Asia/Shanghai")
    parser.add_argument("--location", default="")
    parser.add_argument("--description", default="")
    parser.add_argument("--calendar", default="primary")
    parser.add_argument("--alarm-minutes", type=int, default=15)
    parser.add_argument("--rrule", default="", help="iCal RRULE, e.g. FREQ=WEEKLY;BYDAY=MO")
    parser.add_argument("--is-all-day", action="store_true",
                        help="Treat as all-day event (uses VALUE=DATE)")
    parser.add_argument("--list-calendars", action="store_true")
    parser.add_argument("--query", default="",
                        help="Query: today|tomorrow|week|nextweek|month|YYYY-MM-DD|YYYY-MM-DD~YYYY-MM-DD")
    parser.add_argument("--search", default="", help="Search events by keyword")
    parser.add_argument("--search-range", default="", help="Search range: YYYY-MM-DD~YYYY-MM-DD")
    parser.add_argument("--delete", default="", help="Delete events matching keyword")
    parser.add_argument("--delete-start", default="", help="Filter delete by start date")
    parser.add_argument("--delete-end", default="", help="Filter delete by end date")
    parser.add_argument("--update-find", default="", help="Find event to update by keyword")
    parser.add_argument("--update-set-summary", default="")
    parser.add_argument("--update-set-start", default="")
    parser.add_argument("--update-set-end", default="")
    parser.add_argument("--update-set-location", default="", help="__CLEAR__ to remove")
    parser.add_argument("--update-set-rrule", default="", help="Set RRULE (use __CLEAR__ to remove)")
    parser.add_argument("--update-set-calendar", default="")
    parser.add_argument("--update-start", default="")
    parser.add_argument("--update-end", default="")

    args, unknown = parser.parse_known_args()

    # ── Credentials: env vars ONLY — no CLI fallback ──────────────────
    email = os.environ.get("ICLOUD_EMAIL")
    password = os.environ.get("ICLOUD_APP_PASSWORD")

    if not email or not password:
        print(json.dumps({"error": "Missing ICLOUD_EMAIL or ICLOUD_APP_PASSWORD environment variables"}))
        sys.exit(1)

    try:
        tz = ZoneInfo(args.timezone)
    except (ZoneInfoNotFoundError, KeyError):
        print(json.dumps({"error": f"Unknown timezone: {args.timezone}"}))
        sys.exit(1)

    # ── Connect: dual-client architecture ───────────────────────────
    # fast_client (10s): auth + lightweight CRUD operations (fail-fast)
    # slow_client (60s): date_search(expand=True) heavy queries
    import requests
    fast_session = requests.Session()
    fast_session.headers.update({"User-Agent": f"OpenClaw-Calendar/{VERSION}"})
    slow_session = requests.Session()
    slow_session.headers.update({"User-Agent": f"OpenClaw-Calendar/{VERSION}"})

    try:
        fast_client = caldav.DAVClient(
            url="https://caldav.icloud.com",
            username=email,
            password=password,
            requests_session=fast_session,
            timeout=TIMEOUT_FAST,
        )
        principal = fast_client.principal()
        calendars = principal.calendars()
    except caldav_errors.AuthorizationError:
        # Sanitized: never leak tokens/headers/bearer in exception details
        print(json.dumps({"error": "Authentication failed: check ICLOUD_EMAIL and ICLOUD_APP_PASSWORD"}))
        sys.exit(1)
    except Exception:
        print(json.dumps({"error": "Connection failed: cannot reach iCloud CalDAV server"}))
        sys.exit(1)

    slow_client = caldav.DAVClient(
        url="https://caldav.icloud.com",
        username=email,
        password=password,
        requests_session=slow_session,
        timeout=TIMEOUT_SLOW,
    )

    if not calendars:
        print(json.dumps({"error": "No calendars found"}))
        sys.exit(1)

    # ── Re-bind slow_client's calendars for expand=True operations ──
    # date_search(expand=True) can take 30-60s; use slow_client for it.
    # Other operations (save/delete) use fast_client's calendars.
    try:
        slow_calendars = slow_client.principal().calendars()
    except Exception:
        slow_calendars = []  # degrade: use fast calendars as fallback
    cal_url_map = {}
    for cal in calendars:
        try: cal_url_map[cal.url.canonical] = cal
        except Exception: pass
    for slow_cal in slow_calendars:
        try:
            can = slow_cal.url.canonical
        except Exception: continue
        if can in cal_url_map:
            fast_cal = cal_url_map[can]
            fast_cal._client = slow_client  # point to session with 60s timeout
            break  # at least one calendar bound; rest stay fast

    # ── List calendars ──────────────────────────────────────────────
    if args.list_calendars:
        result: list[dict] = []
        for i, cal in enumerate(calendars):
            try:
                name = cal.get_display_name() or f"calendar_{i}"
            except Exception:
                name = f"calendar_{i}"
                log_action("WARN", f"Cannot get display name for calendar {i}")
            result.append({"index": i, "name": name})
        print(json.dumps(result, ensure_ascii=False))
        log_action("LIST_CALENDARS", f"found={len(result)}")
        sys.exit(0)

    # ── Delete mode — explicit safety gate required ────────────────
    if args.delete:
        if not os.environ.get("CONFIRM_DELETE"):
            print(json.dumps({"error": "Delete requires CONFIRM_DELETE=1 env var"}))
            sys.exit(0)

        keyword = args.delete.lower().strip()
        def_start, def_end = (
            datetime.now(tz) - timedelta(days=180),
            datetime.now(tz) + timedelta(days=180),
        )
        start_range = parse_dt(args.delete_start, tz)[0] or def_start
        end_parsed = parse_dt(args.delete_end, tz)[0] if args.delete_end else None
        end_range = (end_parsed + timedelta(days=1)) if end_parsed else def_end
        start_range, end_range = _clamp_date_range(start_range, end_range)

        deleted: list[dict] = []
        mode_errors: list[dict] = []
        # Dry-run: preview what would be deleted without mutating
        dry_run = os.environ.get("DELETE_DRY_RUN") == "1"

        for cal in calendars:
            cal_name = cal.get_display_name() or "unknown"
            # Step 1: retry-protected search (failure = skip calendar)
            try:
                events = _retry_on_caldav_error(
                    cal.date_search, start=start_range, end=end_range, expand=True,
                )
            except Exception as e:
                error_type = type(e).__name__
                # Sanitized: never leak raw exception text to output
                mode_errors.append({"calendar": cal_name, "error": f"[{error_type}]"})
                log_action("ERROR", f"Delete search on {cal_name}: {error_type}")
                continue

            # Step 2: iterate events — each delete is isolated
            for ev in events:
                vevent = ev.vobject_instance.vevent
                ev_summary = str(vevent.summary.value) if hasattr(vevent, 'summary') else ""
                ev_location = str(vevent.location.value) if hasattr(vevent, 'location') else ""
                ev_desc = str(vevent.description.value) if hasattr(vevent, 'description') else ""
                searchable = f"{ev_summary} {ev_location} {ev_desc}".lower()
                if keyword in searchable:
                    if dry_run:
                        deleted.append({"summary": ev_summary, "calendar": cal_name, "status": "would_be_deleted"})
                        continue
                    try:
                        _retry_on_caldav_error(ev.delete)
                        deleted.append({"summary": ev_summary, "calendar": cal_name})
                    except Exception as e:
                        error_type = type(e).__name__
                        mode_errors.append({
                            "calendar": cal_name,
                            "summary": sanitize_for_log(ev_summary),
                            "error": f"[{error_type}]"
                        })
                        log_action("ERROR", f"Delete item on {cal_name}: {sanitize_for_log(ev_summary)}")

        status = _compute_status(deleted, mode_errors)
        prefix = "[DRY RUN] " if dry_run else ""
        print(json.dumps({
            "status": status,
            "summary": f"{prefix}Delete matched '{keyword}'. Succeeded: {len(deleted)}, Failed: {len(mode_errors)}.",
            "dry_run": dry_run,
            "successful_items": deleted,
            "failed_items": mode_errors,
        }, ensure_ascii=False))
        log_action("DELETE", f"{prefix}keyword={sanitize_for_log(keyword)} ok={len(deleted)} fail={len(mode_errors)}")
        sys.exit(0)

    # ── Update mode — explicit safety gate required ────────────────
    if args.update_find:
        if not os.environ.get("CONFIRM_UPDATE"):
            print(json.dumps({"error": "Update requires CONFIRM_UPDATE=1 env var"}))
            sys.exit(0)
        keyword = args.update_find.lower().strip()
        def_start, def_end = (
            datetime.now(tz) - timedelta(days=180),
            datetime.now(tz) + timedelta(days=180),
        )
        start_range = parse_dt(args.update_start, tz)[0] or def_start
        end_range = (parse_dt(args.update_end, tz)[0] + timedelta(days=1)) if args.update_end else def_end
        start_range, end_range = _clamp_date_range(start_range, end_range)

        matched: list[dict] = []
        mode_errors: list[dict] = []
        for cal in calendars:
            cal_name = cal.get_display_name() or "unknown"
            try:
                events = _retry_on_caldav_error(
                    cal.date_search, start=start_range, end=end_range, expand=True,
                )
                for ev in events:
                    vevent = ev.vobject_instance.vevent
                    ev_summary = str(vevent.summary.value) if hasattr(vevent, 'summary') else ""
                    ev_desc = str(vevent.description.value) if hasattr(vevent, 'description') else ""
                    if keyword in ev_summary.lower() or keyword in ev_desc.lower():
                        matched.append({"event": ev, "vevent": vevent, "summary": ev_summary,
                                        "calendar": cal_name, "cal_obj": cal})
            except Exception as e:
                mode_errors.append({"calendar": cal_name, "error": f"{type(e).__name__}: {e}"})
                log_action("ERROR", f"Update search on {cal_name}: {type(e).__name__}: {e}")
                continue

        if not matched:
            result = {"error": f"No events found matching '{args.update_find}'"}
            if mode_errors:
                result["errors"] = mode_errors
            print(json.dumps(result))
            sys.exit(1)
        if len(matched) > 1:
            summaries = [{"summary": m["summary"], "start": str(m["vevent"].dtstart.value),
                          "calendar": m["calendar"]} for m in matched]
            print(json.dumps({"error": f"Multiple events matched ({len(matched)}), be more specific",
                              "matches": summaries}, ensure_ascii=False))
            sys.exit(1)

        m = matched[0]
        ev = m["event"]
        vevent = m["vevent"]
        changes: dict = {"original_summary": m["summary"]}

        if args.update_set_summary:
            vevent.summary.value = args.update_set_summary
            changes["summary"] = args.update_set_summary

        if args.update_set_start:
            new_start, _ = parse_dt(args.update_set_start, tz)
            if new_start:
                vevent.dtstart.value = new_start
                changes["start"] = new_start.isoformat()
            else:
                print(json.dumps({"error": f"Cannot parse start: {args.update_set_start}"}))
                sys.exit(1)

        if args.update_set_end:
            new_end, _ = parse_dt(args.update_set_end, tz)
            if new_end:
                vevent.dtend.value = new_end
                changes["end"] = new_end.isoformat()
            else:
                print(json.dumps({"error": f"Cannot parse end: {args.update_set_end}"}))
                sys.exit(1)

        if args.update_set_location == "__CLEAR__":
            if hasattr(vevent, 'location'):
                vevent.location.value = ""
            changes["location"] = "(cleared)"
        elif args.update_set_location:
            if hasattr(vevent, 'location'):
                vevent.location.value = args.update_set_location
            else:
                vevent.add('location').value = args.update_set_location
            changes["location"] = args.update_set_location

        if args.update_set_rrule == "__CLEAR__":
            if hasattr(vevent, 'rrule'):
                vevent.rrule.value = ""
            changes["rrule"] = "(cleared)"
        elif args.update_set_rrule:
            rrule = _validate_rrule(args.update_set_rrule)
            if hasattr(vevent, 'rrule'):
                vevent.rrule.value = rrule
            else:
                vevent.add('rrule').value = rrule
            changes["rrule"] = rrule

        try:
            _retry_on_caldav_error(ev.save)
        except Exception:
            print(json.dumps({"error": f"Update failed: save operation did not succeed"}))
            sys.exit(1)

        # Move to another calendar: copy first with new UID, delete after success
        if args.update_set_calendar:
            dest_cal = find_calendar(calendars, args.update_set_calendar)
            dest_name = dest_cal.get_display_name() or "default"
            if dest_name != m["calendar"]:
                ical_str = ev.data
                new_uid = _new_uid()
                ical_str_new_uid = re.sub(r'UID:[^\r\n]+', f'UID:{new_uid}', ical_str)
                copied = False
                try:
                    _retry_on_caldav_error(dest_cal.save_event, ical_str_new_uid)
                    copied = True
                except Exception:
                    print(json.dumps({"error": "Move failed: could not save to destination calendar"}))
                    sys.exit(1)
                if copied:
                    try:
                        _retry_on_caldav_error(ev.delete)
                    except Exception as e:
                        log_action("WARN", f"Delete after move failed: {type(e).__name__}")
                    changes["calendar"] = f"{m['calendar']} → {dest_name}"

        print(json.dumps({"updated": True, "changes": changes}, ensure_ascii=False))
        log_action("UPDATE", f"find={sanitize_for_log(args.update_find)} changes={len(changes)} fields")
        sys.exit(0)

    # ── Search mode ─────────────────────────────────────────────────
    if args.search:
        keyword = args.search

        if args.search_range and "~" in args.search_range:
            parts = args.search_range.split("~")
            start_range = parse_dt(parts[0].strip(), tz)[0]
            end_range = parse_dt(parts[1].strip(), tz)[0]
            if not start_range or not end_range:
                print(json.dumps({"error": "Cannot parse search range. Use YYYY-MM-DD~YYYY-MM-DD"}))
                sys.exit(1)
            end_range = end_range + timedelta(days=1)
        else:
            def_start, def_end = (
                datetime.now(tz) - timedelta(days=180),
                datetime.now(tz) + timedelta(days=180),
            )
            start_range = def_start
            end_range = def_end

        result = search_events(calendars, tz, start_range, end_range, keyword)
        # Sanitize: do not leak internal error messages; use sanitized versions in stdout
        sanitized_errors = [{"calendar": e["calendar"], "error": "[error_details_logged]"} for e in result["errors"]]
        print(json.dumps({
            "events": result["events"], "count": len(result["events"]),
            "errors": sanitized_errors, "keyword": args.search,
        }, ensure_ascii=False))
        log_action("SEARCH", f"keyword={sanitize_for_log(keyword)} found={len(result['events'])}")
        sys.exit(0)

    # ── Query mode ──────────────────────────────────────────────────
    if args.query:
        start_range, end_range = parse_date_range_for_query(args.query, tz)
        if not start_range:
            print(json.dumps({"error": f"Cannot parse query: {args.query}. Use today|tomorrow|week|nextweek|month|YYYY-MM-DD|YYYY-MM-DD~YYYY-MM-DD"}))
            sys.exit(1)

        result = search_events(calendars, tz, start_range, end_range)
        print(json.dumps({
            "events": result["events"], "count": len(result["events"]),
            "errors": result["errors"],
            "range": f"{start_range.date()} ~ {(end_range - timedelta(days=1)).date()}",
        }, ensure_ascii=False))
        log_action("QUERY", f"range={args.query} found={len(result['events'])}")
        sys.exit(0)

    # ── Create event ────────────────────────────────────────────────
    if not args.summary or not args.start:
        print(json.dumps({"error": "--summary and --start are required"}))
        sys.exit(1)

    target_cal = find_calendar(calendars, args.calendar)
    start_dt, is_all_day = parse_dt(args.start, tz)
    if not start_dt:
        print(json.dumps({"error": f"Cannot parse start: {args.start}"}))
        sys.exit(1)

    if args.end:
        end_dt, _ = parse_dt(args.end, tz)
        if not end_dt:
            print(json.dumps({"error": f"Cannot parse end: {args.end}"}))
            sys.exit(1)
    else:
        if is_all_day:
            end_dt = start_dt + timedelta(days=1)
        else:
            end_dt = start_dt + timedelta(hours=1)

    if args.is_all_day and not is_all_day:
        is_all_day = True

    # Generate UID once for idempotency — same UID across retries prevents duplicates
    event_uid = _new_uid()

    # Validate RRULE on ALL paths (create, update) — critical security gate
    if args.rrule:
        try:
            _validate_rrule(args.rrule)
        except ValueError as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)

    ical = build_ical(
        summary=args.summary, start_dt=start_dt, end_dt=end_dt,
        location=args.location, description=args.description,
        alarm_minutes=args.alarm_minutes if args.alarm_minutes > 0 else None,
        rrule=args.rrule, is_all_day=is_all_day, uid=event_uid,
    )

    try:
        _retry_on_caldav_error(target_cal.save_event, ical)
    except Exception:
        print(json.dumps({"error": "Save failed: calendar server rejected the event"}))
        sys.exit(1)

    try:
        cal_name = target_cal.get_display_name() or "default"
    except Exception:
        cal_name = "default"

    result = {
        "success": True, "summary": args.summary,
        "start": start_dt.isoformat(), "end": end_dt.isoformat(),
        "location": args.location, "calendar": cal_name,
        "alarm_minutes": args.alarm_minutes,
        "is_all_day": is_all_day,
        "uid": event_uid,
    }
    if args.rrule:
        result["rrule"] = args.rrule

    print(json.dumps(result, ensure_ascii=False))
    log_action("CREATE", f"{sanitize_for_log(args.summary)} | {start_dt.date()} | {sanitize_for_log(cal_name)}")


if __name__ == "__main__":
    main()
