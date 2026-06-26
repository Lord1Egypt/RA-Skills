#!/usr/bin/env python3
"""Build compact live-game context for a single NBA game."""

from __future__ import annotations

import argparse
import json

from nba_pulse_core import build_game_scene, render_game_scene_markdown, scene_payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render compact live game context.")
    parser.add_argument("--tz")
    parser.add_argument("--date")
    parser.add_argument("--team", required=True)
    parser.add_argument("--lang", default="zh", choices=("zh", "en"))
    parser.add_argument("--format", default="json", choices=("json", "markdown"))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    scene = build_game_scene(tz=args.tz, date_text=args.date, team=args.team, lang=args.lang, analysis_mode="live")
    if args.format == "markdown":
        print(render_game_scene_markdown(scene))
    else:
        print(json.dumps(scene_payload(scene), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
