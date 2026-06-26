#!/usr/bin/env python3
"""diary_logger.stats — dashboard payload for the diary panel."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore

import _calendar


def _load_cfg() -> dict:
    cfg_path = Path(__file__).resolve().parents[1] / "component.toml"
    with cfg_path.open("rb") as fh:
        return tomllib.load(fh)


def build_stats() -> dict:
    cfg = _load_cfg().get("diary_logger", {})
    tz_name = cfg.get("default_timezone", "America/Denver")
    calendar_name = cfg.get("calendar_name", "Glance Diary")
    tz = ZoneInfo(tz_name) if ZoneInfo else None
    now = datetime.now(tz) if tz else datetime.now()

    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = day_start - timedelta(days=6)

    try:
        events = _calendar.list_events(
            calendar_name=calendar_name,
            timezone=tz_name,
            time_min=week_start,
            time_max=now,
        )
    except Exception as exc:
        return {
            "freshness_hours": None,
            "status": "error",
            "summary": {"error": str(exc)},
            "rows": [],
        }

    if not events:
        return {
            "freshness_hours": None,
            "status": "empty",
            "summary": {"today_count": 0, "total_minutes_today": 0, "by_category_today": {}},
            "rows": [],
        }

    today_minutes_by_cat: dict[str, float] = {}
    today_count = 0
    week_minutes_by_cat: dict[str, float] = {}
    last_end_dt: datetime | None = None
    rows: list[dict] = []

    for ev in events:
        start_raw = (ev.get("start") or {}).get("dateTime")
        end_raw = (ev.get("end") or {}).get("dateTime")
        if not (start_raw and end_raw):
            continue
        start_dt = datetime.fromisoformat(start_raw.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end_raw.replace("Z", "+00:00"))
        if tz is not None:
            start_dt = start_dt.astimezone(tz)
            end_dt = end_dt.astimezone(tz)
        category = _calendar.parse_event_category(ev)
        minutes = max(0.0, (end_dt - start_dt).total_seconds() / 60.0)

        week_minutes_by_cat[category] = week_minutes_by_cat.get(category, 0) + minutes
        if start_dt >= day_start:
            today_minutes_by_cat[category] = today_minutes_by_cat.get(category, 0) + minutes
            today_count += 1

        if last_end_dt is None or end_dt > last_end_dt:
            last_end_dt = end_dt

        rows.append({
            "start": start_dt.strftime("%Y-%m-%d %H:%M"),
            "end": end_dt.strftime("%H:%M"),
            "title": (ev.get("summary") or "").split("] ", 1)[-1],
            "category": category,
            "duration_minutes": round(minutes, 1),
        })

    rows = rows[-10:][::-1]
    freshness_hours = None
    status = "ok"
    if last_end_dt is not None:
        freshness_hours = round((now - last_end_dt).total_seconds() / 3600.0, 2)
        if freshness_hours > 24:
            status = "stale"

    return {
        "freshness_hours": freshness_hours,
        "status": status,
        "summary": {
            "today_count": today_count,
            "total_minutes_today": round(sum(today_minutes_by_cat.values()), 1),
            "by_category_today": {k: round(v, 1) for k, v in today_minutes_by_cat.items()},
            "by_category_7d": {k: round(v, 1) for k, v in week_minutes_by_cat.items()},
        },
        "rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    print(json.dumps(build_stats(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
