#!/usr/bin/env python3
"""Compact play-by-play digest helpers for NBA_TR."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


def _format_score(play: dict[str, Any], game: dict[str, Any]) -> str:
    away_score = play.get("awayScore")
    home_score = play.get("homeScore")
    if away_score in (None, "") or home_score in (None, ""):
        return ""
    away_abbr = ((game.get("away") or {}).get("abbr")) or "AWAY"
    home_abbr = ((game.get("home") or {}).get("abbr")) or "HOME"
    return f" ({away_abbr} {away_score}-{home_score} {home_abbr})"


def _format_play(play: dict[str, Any], game: dict[str, Any]) -> str:
    period = play.get("period")
    clock = play.get("clock") or ""
    text = play.get("text") or play.get("description") or ""
    prefix = " ".join(part for part in (f"P{period}" if period else "", clock) if part).strip()
    score = _format_score(play, game)
    return f"{prefix} {text}{score}".strip()


def _clock_seconds_remaining(clock: Any) -> float | None:
    text = str(clock or "").strip()
    if not text:
        return None
    if ":" in text:
        minute_text, second_text = text.split(":", 1)
        try:
            return int(minute_text) * 60 + float(second_text)
        except ValueError:
            return None
    try:
        return float(text)
    except ValueError:
        return None


def _score_value(value: Any) -> int | None:
    try:
        if value in (None, ""):
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def _recent_run_summary(game: dict[str, Any], *, lang: str, window_seconds: int = 180) -> str:
    plays = game.get("playTimeline") or []
    if not plays:
        return ""
    current_period = next((play.get("period") for play in reversed(plays) if play.get("period") not in (None, "")), None)
    if current_period in (None, ""):
        return ""
    period_plays = [play for play in plays if play.get("period") == current_period]
    scoring = [
        play
        for play in period_plays
        if _score_value(play.get("awayScore")) is not None and _score_value(play.get("homeScore")) is not None
    ]
    if len(scoring) < 2:
        return ""
    latest = scoring[-1]
    latest_clock = _clock_seconds_remaining(latest.get("clock"))
    if latest_clock is None:
        return ""
    window_floor = latest_clock + window_seconds
    start = scoring[0]
    for play in reversed(scoring[:-1]):
        play_clock = _clock_seconds_remaining(play.get("clock"))
        if play_clock is None:
            continue
        if play_clock <= window_floor:
            start = play
        else:
            break
    start_away = _score_value(start.get("awayScore"))
    start_home = _score_value(start.get("homeScore"))
    end_away = _score_value(latest.get("awayScore"))
    end_home = _score_value(latest.get("homeScore"))
    if None in (start_away, start_home, end_away, end_home):
        return ""
    away_run = max(0, int(end_away) - int(start_away))
    home_run = max(0, int(end_home) - int(start_home))
    away_name = ((game.get("away") or {}).get("abbr")) or "AWAY"
    home_name = ((game.get("home") or {}).get("abbr")) or "HOME"
    label = "最近3分钟攻击波" if lang == "zh" else "Last 3-minute run"
    return f"{label}: {away_name} {away_run}-{home_run} {home_name}"


def build_play_digest(game: dict[str, Any], *, lang: str, limit: int = 8) -> dict[str, Any]:
    plays = game.get("playTimeline") or []
    scoring = [play for play in plays if play.get("scoringPlay") or play.get("scoreValue")]
    recent = [_format_play(play, game) for play in scoring[-limit:]]
    turning_point = ""
    if scoring:
        turning_point = _format_play(scoring[-1], game)
    recent_run = _recent_run_summary(game, lang=lang)
    summary = (
        "未从结构化源确认到足够的回合细节。"
        if lang == "zh" and not recent
        else (
            "Structured play detail is currently unavailable."
            if not recent
            else (
                f"压缩为 {len(recent)} 个关键回合。"
                if lang == "zh"
                else f"Compressed to {len(recent)} key plays."
            )
        )
    )
    return {
        "summary": summary,
        "turningPoint": turning_point,
        "recentRun": recent_run,
        "plays": recent,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Digest play timeline JSON into compact key plays.")
    parser.add_argument("--lang", default="zh", choices=("zh", "en"))
    parser.add_argument("--limit", type=int, default=5)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    payload = json.load(sys.stdin)
    print(json.dumps(build_play_digest(payload, lang=args.lang, limit=args.limit), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
