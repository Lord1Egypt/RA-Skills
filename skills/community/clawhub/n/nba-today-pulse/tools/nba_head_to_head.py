#!/usr/bin/env python3
"""Build season-series and recent-meeting context for NBA_TR scenes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from nba_common import NBAReportError  # noqa: E402
from nba_teams import canonicalize_team_abbr  # noqa: E402
from nba_today_report import build_report_payload, event_matchup, format_matchup_line, normalize_competitors, validate_args  # noqa: E402
from provider_espn import fetch_team_schedule  # noqa: E402

SERIES_PATTERN = re.compile(r"\b([A-Z]{2,3})\s+leads\s+series\s+(\d+)-(\d+)\b", re.IGNORECASE)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Return season-series and head-to-head context.")
    parser.add_argument("--tz")
    parser.add_argument("--date")
    parser.add_argument("--team")
    parser.add_argument("--event-id")
    parser.add_argument("--lang", default="zh", choices=("zh", "en"))
    parser.add_argument("--format", default="json", choices=("json", "markdown"))
    parser.add_argument("--base-url")
    return parser.parse_args(argv)


def _event_mentions_matchup(event: dict[str, Any], away_abbr: str, home_abbr: str) -> bool:
    short_name = str(event.get("shortName") or "").upper()
    if away_abbr in short_name and home_abbr in short_name:
        return True
    competition = (event.get("competitions") or [{}])[0]
    competitors = competition.get("competitors") or []
    abbrs = {
        canonicalize_team_abbr(((competitor.get("team") or {}).get("abbreviation")))
        for competitor in competitors
        if competitor
    }
    return {away_abbr, home_abbr}.issubset({abbr for abbr in abbrs if abbr})


def _meeting_from_event(event: dict[str, Any]) -> dict[str, Any]:
    competition = (event.get("competitions") or [{}])[0]
    status = ((competition.get("status") or {}).get("type")) or {}
    competitors = competition.get("competitors") or []
    away_competitor, home_competitor = normalize_competitors(competitors)
    teams: list[dict[str, Any]] = []
    for competitor in (away_competitor, home_competitor):
        if not competitor:
            continue
        team = competitor.get("team") or {}
        teams.append(
            {
                "abbr": canonicalize_team_abbr(team.get("abbreviation")),
                "displayName": team.get("displayName") or "",
                "score": competitor.get("score"),
                "homeAway": competitor.get("homeAway"),
            }
        )
    away_team = next((team for team in teams if team.get("homeAway") == "away"), teams[0] if teams else {})
    home_team = next((team for team in teams if team.get("homeAway") == "home"), teams[1] if len(teams) > 1 else {})
    away_score = int(away_team["score"]) if str(away_team.get("score") or "").isdigit() else None
    home_score = int(home_team["score"]) if str(home_team.get("score") or "").isdigit() else None
    winner = None
    if away_score is not None and home_score is not None:
        winner = away_team["abbr"] if away_score > home_score else home_team["abbr"]
    matchup = event_matchup(event)
    return {
        "eventId": str(event.get("id") or ""),
        "date": str(event.get("date") or ""),
        "shortName": format_matchup_line(
            matchup.get("away") or away_team.get("abbr"),
            matchup.get("home") or home_team.get("abbr"),
            away_score=away_score,
            home_score=home_score,
        ),
        "status": str(status.get("state") or ""),
        "detail": str(status.get("detail") or status.get("description") or ""),
        "teams": teams,
        "winner": winner,
        "awayAbbr": matchup.get("away") or away_team.get("abbr"),
        "homeAbbr": matchup.get("home") or home_team.get("abbr"),
        "awayScore": away_score,
        "homeScore": home_score,
    }


def _wins_from_series(summary: str, away_abbr: str, home_abbr: str) -> dict[str, int]:
    match = SERIES_PATTERN.search(summary.upper())
    if not match:
        return {}
    leader, first, second = match.groups()
    first_count = int(first)
    second_count = int(second)
    if leader == away_abbr:
        return {away_abbr: first_count, home_abbr: second_count}
    if leader == home_abbr:
        return {home_abbr: first_count, away_abbr: second_count}
    return {}


def build_head_to_head_context(
    game: dict[str, Any],
    *,
    away_schedule: dict[str, Any] | None = None,
    home_schedule: dict[str, Any] | None = None,
) -> dict[str, Any]:
    away_abbr = game["away"]["abbr"]
    home_abbr = game["home"]["abbr"]
    season_series = game.get("seasonSeries") or []
    summary = str((season_series[0] or {}).get("summary") or "") if season_series else ""
    meetings: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for payload in (away_schedule or {}, home_schedule or {}):
        for event in payload.get("events") or []:
            event_id = str(event.get("id") or "")
            if not event_id or event_id == game["eventId"] or event_id in seen_ids:
                continue
            if not _event_mentions_matchup(event, away_abbr, home_abbr):
                continue
            seen_ids.add(event_id)
            meetings.append(_meeting_from_event(event))
    meetings.sort(key=lambda item: item.get("date") or "", reverse=True)
    wins_by_team = _wins_from_series(summary, away_abbr, home_abbr)
    if not wins_by_team:
        wins_by_team = {away_abbr: 0, home_abbr: 0}
        for meeting in meetings:
            winner = meeting.get("winner")
            if winner in wins_by_team:
                wins_by_team[winner] += 1
        if wins_by_team[away_abbr] == 0 and wins_by_team[home_abbr] == 0:
            wins_by_team = {}
    source = "unavailable"
    if summary:
        source = "espn_summary"
    elif meetings:
        source = "espn_team_schedule"
    return {
        "available": bool(summary or meetings),
        "source": source,
        "seasonSeriesSummary": summary,
        "winsByTeam": wins_by_team,
        "meetings": meetings[:5],
        "latestMeeting": meetings[0] if meetings else None,
    }


def _resolve_game(args: argparse.Namespace) -> dict[str, Any]:
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
                return game
        raise NBAReportError("当前条件下未找到对应比赛。", kind="not_found")
    return report["games"][0]


def render_markdown(context: dict[str, Any], lang: str) -> str:
    title = "历史交锋" if lang == "zh" else "Head-to-Head"
    lines = [f"# {title}", f"- Available: {context['available']}"]
    if context.get("seasonSeriesSummary"):
        lines.append(f"- Season Series: {context['seasonSeriesSummary']}")
    if context.get("winsByTeam"):
        wins = ", ".join(f"{abbr}={wins}" for abbr, wins in sorted(context["winsByTeam"].items()))
        lines.append(f"- Wins By Team: {wins}")
    for meeting in context.get("meetings") or []:
        lines.append(f"- {meeting['date']}: {meeting['shortName']} ({meeting['detail']})")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        game = _resolve_game(args)
        away_schedule = {}
        home_schedule = {}
        if game["away"].get("id"):
            try:
                away_schedule = fetch_team_schedule(game["away"]["id"], base_url=args.base_url)["data"]
            except NBAReportError:
                away_schedule = {}
        if game["home"].get("id"):
            try:
                home_schedule = fetch_team_schedule(game["home"]["id"], base_url=args.base_url)["data"]
            except NBAReportError:
                home_schedule = {}
        context = build_head_to_head_context(game, away_schedule=away_schedule, home_schedule=home_schedule)
        if args.format == "markdown":
            print(render_markdown(context, args.lang))
        else:
            print(json.dumps(context, ensure_ascii=False, indent=2))
        return 0
    except NBAReportError as exc:
        print(f"[{exc.kind}] {exc}", file=sys.stderr)
        return 2 if exc.kind == "invalid_arguments" else 1


if __name__ == "__main__":
    raise SystemExit(main())
