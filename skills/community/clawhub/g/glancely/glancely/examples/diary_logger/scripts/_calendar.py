"""Google Calendar client for diary_logger.

Auth is delegated to `glancely.core.auth` (user brings own OAuth client).
This module just translates diary intent <-> Calendar API calls.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Optional

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore

# core.auth is implemented in the next pass; this import is the stable seam.
from glancely.core.auth import get_calendar_service  # type: ignore


CATEGORY_COLOR_IDS = {
    "prod": "9",      # blueberry
    "admin": "8",     # graphite
    "nonprod": "5",   # banana
}


def _resolve_calendar_id(service, calendar_name: str) -> str:
    env_id = os.environ.get("GLANCE_DIARY_CALENDAR_ID")
    if env_id:
        return env_id
    page_token = None
    while True:
        resp = service.calendarList().list(pageToken=page_token).execute()
        for entry in resp.get("items", []):
            if entry.get("summary") == calendar_name:
                return entry["id"]
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    raise RuntimeError(
        f"Calendar named {calendar_name!r} not found. Create it in Google Calendar "
        f"and re-run install.sh, or set GLANCE_DIARY_CALENDAR_ID."
    )


def _fmt(dt: datetime, tz: str) -> dict:
    if ZoneInfo is not None and dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo(tz))
    return {"dateTime": dt.isoformat(), "timeZone": tz}


def write_event(
    *,
    calendar_name: str,
    title: str,
    start: datetime,
    end: datetime,
    timezone: str,
    category: str = "prod",
    description: Optional[str] = None,
) -> dict:
    service = get_calendar_service()
    cal_id = _resolve_calendar_id(service, calendar_name)
    body = {
        "summary": f"[{category}] {title}",
        "start": _fmt(start, timezone),
        "end": _fmt(end, timezone),
        "extendedProperties": {"private": {"category": category}},
    }
    if description:
        body["description"] = description
    color = CATEGORY_COLOR_IDS.get(category)
    if color:
        body["colorId"] = color
    return service.events().insert(calendarId=cal_id, body=body).execute()


def list_events(
    *,
    calendar_name: str,
    timezone: str,
    time_min: datetime,
    time_max: datetime,
) -> list[dict]:
    service = get_calendar_service()
    cal_id = _resolve_calendar_id(service, calendar_name)
    if ZoneInfo is not None and time_min.tzinfo is None:
        time_min = time_min.replace(tzinfo=ZoneInfo(timezone))
    if ZoneInfo is not None and time_max.tzinfo is None:
        time_max = time_max.replace(tzinfo=ZoneInfo(timezone))
    events: list[dict] = []
    page_token = None
    while True:
        resp = service.events().list(
            calendarId=cal_id,
            timeMin=time_min.isoformat(),
            timeMax=time_max.isoformat(),
            singleEvents=True,
            orderBy="startTime",
            pageToken=page_token,
            timeZone=timezone,
        ).execute()
        events.extend(resp.get("items", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return events


def last_event_end(
    *,
    calendar_name: str,
    timezone: str,
    within_hours: int = 24,
) -> Optional[datetime]:
    tz = ZoneInfo(timezone) if ZoneInfo else None
    now = datetime.now(tz) if tz else datetime.now()
    window_start = now - timedelta(hours=within_hours)
    events = list_events(
        calendar_name=calendar_name,
        timezone=timezone,
        time_min=window_start,
        time_max=now,
    )
    candidates: list[datetime] = []
    for ev in events:
        end_raw = (ev.get("end") or {}).get("dateTime")
        if not end_raw:
            continue
        end_dt = datetime.fromisoformat(end_raw.replace("Z", "+00:00"))
        if tz is not None:
            end_dt = end_dt.astimezone(tz)
        if end_dt > now:
            continue
        candidates.append(end_dt)
    return max(candidates) if candidates else None


def parse_event_category(event: dict) -> str:
    cat = ((event.get("extendedProperties") or {}).get("private") or {}).get("category")
    if cat:
        return cat
    summary = event.get("summary") or ""
    if summary.startswith("[") and "]" in summary:
        return summary[1 : summary.index("]")]
    return "prod"


def event_duration_minutes(event: dict) -> float:
    start_raw = (event.get("start") or {}).get("dateTime")
    end_raw = (event.get("end") or {}).get("dateTime")
    if not (start_raw and end_raw):
        return 0.0
    s = datetime.fromisoformat(start_raw.replace("Z", "+00:00"))
    e = datetime.fromisoformat(end_raw.replace("Z", "+00:00"))
    return max(0.0, (e - s).total_seconds() / 60.0)
