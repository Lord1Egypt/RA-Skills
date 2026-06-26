#!/usr/bin/env python3
"""diary_logger.log — entrypoint for "log diary" skill invocations.

Reads structured args, resolves time range, writes a Calendar event.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow running as a script: `./scripts/log.py ...`
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

import _calendar
import _time_parser


def _load_component_config() -> dict:
    cfg_path = Path(__file__).resolve().parents[1] / "component.toml"
    with cfg_path.open("rb") as fh:
        return tomllib.load(fh)


def main(argv: list[str] | None = None) -> int:
    cfg = _load_component_config()
    diary_cfg = cfg.get("diary_logger", {})
    default_tz = diary_cfg.get("default_timezone", _time_parser.DEFAULT_TIMEZONE)
    default_cat = diary_cfg.get("default_category", "prod")
    calendar_name = diary_cfg.get("calendar_name", "Glance Diary")

    parser = argparse.ArgumentParser(description="Log a diary entry to Google Calendar.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--category", default=default_cat, choices=["prod", "admin", "nonprod"])
    parser.add_argument("--start", help="Time token like '2:30pm'")
    parser.add_argument("--end", help="Time token like '4:00pm' or 'now'")
    parser.add_argument("--timezone", default=default_tz)
    parser.add_argument("--description")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    last_end = None
    if not (args.start and args.end):
        last_end = _calendar.last_event_end(
            calendar_name=calendar_name,
            timezone=args.timezone,
        )

    resolved = _time_parser.resolve_range(
        raw_title=args.title,
        timezone=args.timezone,
        explicit_start=args.start,
        explicit_end=args.end,
        last_event_end=last_end,
    )

    payload = {
        "title": resolved.cleaned_title,
        "category": args.category,
        "start": resolved.start.isoformat(),
        "end": resolved.end.isoformat(),
        "timezone": args.timezone,
        "mode": resolved.mode,
    }

    if args.dry_run:
        print(json.dumps({"dry_run": True, "plan": payload}, indent=2, ensure_ascii=False))
        return 0

    event = _calendar.write_event(
        calendar_name=calendar_name,
        title=resolved.cleaned_title,
        start=resolved.start,
        end=resolved.end,
        timezone=args.timezone,
        category=args.category,
        description=args.description,
    )
    print(json.dumps({"plan": payload, "calendar_event_id": event.get("id"),
                      "html_link": event.get("htmlLink")}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
