#!/usr/bin/env python3
"""Scene-specific day snapshot entrypoint."""

from __future__ import annotations

import argparse
import json

from nba_pulse_core import render_day_scene


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render day-level NBA snapshot.")
    parser.add_argument("--tz")
    parser.add_argument("--date")
    parser.add_argument("--lang", default="zh", choices=("zh", "en"))
    parser.add_argument("--format", default="markdown", choices=("markdown", "json"))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.format == "json":
        print(json.dumps({"markdown": render_day_scene(tz=args.tz, date_text=args.date, lang=args.lang)}, ensure_ascii=False, indent=2))
    else:
        print(render_day_scene(tz=args.tz, date_text=args.date, lang=args.lang))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
