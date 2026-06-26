#!/usr/bin/env python3
"""Locate a single game with provider fallback."""

from __future__ import annotations

import argparse
import json

from nba_pulse_core import locate_game


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Locate a single NBA game for a team/date/timezone.")
    parser.add_argument("--tz")
    parser.add_argument("--date")
    parser.add_argument("--team", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    print(json.dumps(locate_game(tz=args.tz, date_text=args.date, team=args.team), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
