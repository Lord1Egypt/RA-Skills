#!/usr/bin/env python3
"""Fetch a single team's current roster snapshot."""

from __future__ import annotations

import argparse
import json

from nba_pulse_core import fetch_team_roster_snapshot
from nba_teams import normalize_team_input


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch verified team roster.")
    parser.add_argument("--team", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    team = normalize_team_input(args.team)
    print(json.dumps(fetch_team_roster_snapshot(team or args.team), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
