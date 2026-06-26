#!/usr/bin/env python3
"""Fetch both teams' roster snapshots for a game."""

from __future__ import annotations

import argparse
import json

from nba_pulse_core import build_scene_report, fetch_game_rosters


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch both rosters for a single game.")
    parser.add_argument("--tz")
    parser.add_argument("--date")
    parser.add_argument("--team", required=True)
    parser.add_argument("--lang", default="zh", choices=("zh", "en"))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_scene_report(tz=args.tz, date_text=args.date, team=args.team, lang=args.lang)
    print(json.dumps(fetch_game_rosters(report["games"][0]), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
