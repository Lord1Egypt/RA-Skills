#!/usr/bin/env python3
"""Build stable team-form snapshots for NBA_TR scenes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from nba_common import NBAReportError  # noqa: E402
from nba_today_report import build_report_payload, validate_args  # noqa: E402
from nba_teams import normalize_team_input  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Return stable team-form data for the selected game/team.")
    parser.add_argument("--tz")
    parser.add_argument("--date")
    parser.add_argument("--team")
    parser.add_argument("--event-id")
    parser.add_argument("--lang", default="zh", choices=("zh", "en"))
    parser.add_argument("--format", default="json", choices=("json", "markdown"))
    parser.add_argument("--base-url")
    return parser.parse_args(argv)


def _injury_burden(items: list[str]) -> float:
    burden = 0.0
    for item in items:
        lowered = item.lower()
        if "out" in lowered or "缺阵" in lowered:
            burden += 1.5
        elif "doubt" in lowered:
            burden += 1.25
        elif "question" in lowered or "questionable" in lowered or "成疑" in lowered:
            burden += 1.0
        elif "day-to-day" in lowered or "每日观察" in lowered:
            burden += 0.5
    return burden


def build_team_form_snapshot(game: dict[str, Any], side: str) -> dict[str, Any]:
    team = game[side]
    abbr = team["abbr"]
    team_id = team.get("id") or ""
    standings = game.get("standings", {}).get(team_id) or {}
    season_stats = game.get("teamSeasonStats", {}).get(abbr) or {}
    recent_form = game.get("lastFiveGames", {}).get(team_id) or {}
    schedule = game.get("teamScheduleContext", {}).get(abbr) or {}
    injuries = game.get("injuries", {}).get(abbr) or []
    snapshot = {
        "available": bool(standings or season_stats or recent_form or schedule or injuries),
        "team": {
            "id": team_id,
            "abbr": abbr,
            "displayName": team.get("displayName") or "",
            "record": team.get("record") or "",
        },
        "standings": standings,
        "seasonStats": season_stats,
        "recentForm": {
            "record": recent_form.get("record") or "",
            "wins": recent_form.get("wins"),
            "losses": recent_form.get("losses"),
            "scores": recent_form.get("scores") or [],
        },
        "schedule": {
            "restDays": schedule.get("restDays"),
            "isBackToBack": bool(schedule.get("isBackToBack")),
            "previousGame": schedule.get("previousGame"),
            "nextGame": schedule.get("nextGame"),
        },
        "injuries": {
            "count": len(injuries),
            "burden": _injury_burden(injuries),
            "notable": injuries[:3],
        },
    }
    return snapshot


def build_team_form_context(game: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        game["away"]["abbr"]: build_team_form_snapshot(game, "away"),
        game["home"]["abbr"]: build_team_form_snapshot(game, "home"),
    }


def _resolve_game(args: argparse.Namespace) -> tuple[dict[str, Any], str]:
    if not args.team and not args.event_id:
        raise NBAReportError("team 或 event-id 必须至少提供一个。", kind="invalid_arguments")
    request = argparse.Namespace(
        tz=args.tz,
        date=args.date,
        team=args.team,
        view="game" if args.team else "day",
        lang=args.lang,
        format="json",
        base_url=args.base_url,
    )
    validate_args(request)
    report = build_report_payload(request)
    if args.event_id:
        for game in report["games"]:
            if game["eventId"] == args.event_id:
                target_abbr = normalize_team_input(args.team) if args.team else game["away"]["abbr"]
                return game, target_abbr
        raise NBAReportError("当前条件下未找到对应比赛。", kind="not_found")
    target_abbr = normalize_team_input(args.team)
    if not target_abbr:
        raise NBAReportError("未能识别球队缩写。", kind="invalid_arguments")
    return report["games"][0], target_abbr


def render_markdown(snapshot: dict[str, Any], lang: str) -> str:
    title = "球队近期状态" if lang == "zh" else "Team Form Snapshot"
    lines = [
        f"# {title}",
        f"- Team: {snapshot['team']['abbr']} ({snapshot['team']['displayName']})",
        f"- Record: {snapshot['team']['record'] or 'N/A'}",
        f"- Recent Form: {snapshot['recentForm']['record'] or 'N/A'}",
        f"- Rest Days: {snapshot['schedule']['restDays'] if snapshot['schedule']['restDays'] is not None else 'N/A'}",
        f"- Back-to-Back: {snapshot['schedule']['isBackToBack']}",
        f"- Injury Burden: {snapshot['injuries']['burden']:.2f}",
    ]
    if snapshot["recentForm"]["scores"]:
        lines.append(f"- Recent Scores: {', '.join(snapshot['recentForm']['scores'])}")
    if snapshot["injuries"]["notable"]:
        lines.append(f"- Injuries: {'; '.join(snapshot['injuries']['notable'])}")
    if snapshot["seasonStats"]:
        stats = ", ".join(f"{key}={value}" for key, value in sorted(snapshot["seasonStats"].items())[:6])
        lines.append(f"- Season Stats: {stats}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        game, target_abbr = _resolve_game(args)
        context = build_team_form_context(game)
        snapshot = context.get(target_abbr)
        if not snapshot:
            raise NBAReportError("当前条件下未找到对应球队快照。", kind="not_found")
        if args.format == "markdown":
            print(render_markdown(snapshot, args.lang))
        else:
            print(json.dumps(snapshot, ensure_ascii=False, indent=2))
        return 0
    except NBAReportError as exc:
        print(f"[{exc.kind}] {exc}", file=sys.stderr)
        return 2 if exc.kind == "invalid_arguments" else 1


if __name__ == "__main__":
    raise SystemExit(main())
