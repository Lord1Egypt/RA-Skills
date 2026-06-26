#!/usr/bin/env python3
"""Build richer game full-stats payloads for NBA_TR scenes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from entity_guard import normalize_player_identity  # noqa: E402
from nba_common import NBAReportError  # noqa: E402
from nba_teams import canonicalize_team_abbr  # noqa: E402
from nba_today_report import build_report_payload, safe_int, validate_args  # noqa: E402
from provider_nba import fetch_live_boxscore, find_game_id_by_matchup  # noqa: E402

PLAYER_KEY_ALIASES = {
    "minutes": "MIN",
    "min": "MIN",
    "points": "PTS",
    "rebounds": "REB",
    "reboundstotal": "REB",
    "assists": "AST",
    "steals": "STL",
    "blocks": "BLK",
    "turnovers": "TOV",
    "offensiverebounds": "OREB",
    "defensiverebounds": "DREB",
    "personalfouls": "PF",
}
TEAM_LABEL_ALIASES = {
    "PTS": "PTS",
    "REB": "REB",
    "REBOUNDS": "REB",
    "AST": "AST",
    "ASSISTS": "AST",
    "STL": "STL",
    "STEALS": "STL",
    "BLK": "BLK",
    "BLOCKS": "BLK",
    "TOV": "TOV",
    "TO": "TOV",
    "TURNOVERS": "TOV",
    "OREB": "OREB",
    "OR": "OREB",
    "OFFENSIVE REBOUNDS": "OREB",
    "DREB": "DREB",
    "DR": "DREB",
    "DEFENSIVE REBOUNDS": "DREB",
    "PF": "PF",
    "FOULS": "PF",
    "FG": "FG",
    "3PT": "3PT",
    "FT": "FT",
}
EMPTY_STATS = {
    "MIN": None,
    "PTS": None,
    "REB": None,
    "AST": None,
    "STL": None,
    "BLK": None,
    "TOV": None,
    "FG": None,
    "3PT": None,
    "FT": None,
    "OREB": None,
    "DREB": None,
    "PF": None,
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Return richer team/player full stats for a game.")
    parser.add_argument("--tz")
    parser.add_argument("--date")
    parser.add_argument("--team")
    parser.add_argument("--event-id")
    parser.add_argument("--lang", default="zh", choices=("zh", "en"))
    parser.add_argument("--format", default="json", choices=("json", "markdown"))
    parser.add_argument("--base-url")
    return parser.parse_args(argv)


def _stat_line(made: Any, attempted: Any) -> str | None:
    made_text = str(made).strip() if made not in (None, "") else ""
    if made_text and attempted in (None, "") and re.fullmatch(r"\d+\s*-\s*\d+", made_text):
        return made_text.replace(" ", "")
    made_int = safe_int(made)
    attempted_int = safe_int(attempted)
    if made_int is None and attempted_int is None:
        return None
    return f"{made_int or 0}-{attempted_int or 0}"


def _canonical_player_stats(stat_map: dict[str, Any]) -> dict[str, Any]:
    result = dict(EMPTY_STATS)
    lowered_map = {str(key).lower(): value for key, value in stat_map.items()}
    for key, target in PLAYER_KEY_ALIASES.items():
        if key in lowered_map:
            if target == "MIN":
                result[target] = str(lowered_map[key])
            else:
                result[target] = safe_int(lowered_map[key])
    result["FG"] = _stat_line(
        lowered_map.get("fieldgoalsmade-fieldgoalsattempted") or lowered_map.get("fieldgoalsmade"),
        lowered_map.get("fieldgoalsattempted"),
    )
    result["3PT"] = _stat_line(
        lowered_map.get("threepointfieldgoalsmade-threepointfieldgoalsattempted") or lowered_map.get("threepointfieldgoalsmade"),
        lowered_map.get("threepointfieldgoalsattempted"),
    )
    result["FT"] = _stat_line(
        lowered_map.get("freethrowsmade-freethrowsattempted") or lowered_map.get("freethrowsmade"),
        lowered_map.get("freethrowsattempted"),
    )
    return result


def _player_allowed(name: str, allowed_names: set[str] | None) -> bool:
    if not allowed_names:
        return True
    return normalize_player_identity(name) in allowed_names


def _players_from_summary(boxscore: dict[str, Any], allowed_names: set[str] | None) -> dict[str, list[dict[str, Any]]]:
    players_by_team: dict[str, list[dict[str, Any]]] = {}
    for group in boxscore.get("players") or []:
        team = group.get("team") or {}
        abbr = canonicalize_team_abbr(team.get("abbreviation"))
        if not abbr:
            continue
        team_players: list[dict[str, Any]] = []
        for stat_group in group.get("statistics") or []:
            keys = stat_group.get("keys") or []
            for athlete_entry in stat_group.get("athletes") or []:
                athlete = athlete_entry.get("athlete") or {}
                name = athlete.get("displayName") or athlete.get("shortName") or ""
                if not name or not _player_allowed(str(name), allowed_names):
                    continue
                stats = athlete_entry.get("stats") or []
                stat_map = {str(keys[index]): stats[index] for index in range(min(len(keys), len(stats)))}
                team_players.append(
                    {
                        "playerName": str(name),
                        "starter": bool(athlete_entry.get("starter")),
                        "stats": _canonical_player_stats(stat_map),
                    }
                )
        if team_players:
            players_by_team[abbr] = team_players
    return players_by_team


def _teams_from_summary(boxscore: dict[str, Any]) -> dict[str, dict[str, Any]]:
    teams: dict[str, dict[str, Any]] = {}
    for entry in boxscore.get("teams") or []:
        team = entry.get("team") or {}
        abbr = canonicalize_team_abbr(team.get("abbreviation"))
        if not abbr:
            continue
        stats = dict(EMPTY_STATS)
        for stat in entry.get("statistics") or []:
            target = None
            for identifier in (
                stat.get("abbreviation"),
                stat.get("label"),
                stat.get("name"),
            ):
                normalized = str(identifier or "").strip().upper()
                if not normalized:
                    continue
                target = TEAM_LABEL_ALIASES.get(normalized)
                if target:
                    break
            if not target:
                continue
            value = stat.get("displayValue")
            stats[target] = value
        teams[abbr] = stats
    return teams


def _players_from_nba_live(payload: dict[str, Any], allowed_names: set[str] | None) -> tuple[dict[str, list[dict[str, Any]]], dict[str, dict[str, Any]]]:
    game = payload.get("game") or {}
    players_by_team: dict[str, list[dict[str, Any]]] = {}
    teams: dict[str, dict[str, Any]] = {}
    for side_key in ("awayTeam", "homeTeam"):
        team = game.get(side_key) or {}
        abbr = canonicalize_team_abbr(team.get("teamTricode") or team.get("teamCode"))
        if not abbr:
            continue
        team_players: list[dict[str, Any]] = []
        aggregate = dict(EMPTY_STATS)
        aggregate.update({"PTS": 0, "REB": 0, "AST": 0, "STL": 0, "BLK": 0, "TOV": 0, "OREB": 0, "DREB": 0, "PF": 0})
        for player in team.get("players") or []:
            name = player.get("name") or player.get("familyName") or ""
            raw_stats = player.get("statistics") or {}
            stat_map = {
                "minutes": raw_stats.get("minutes"),
                "points": raw_stats.get("points"),
                "reboundsTotal": raw_stats.get("reboundsTotal"),
                "assists": raw_stats.get("assists"),
                "steals": raw_stats.get("steals"),
                "blocks": raw_stats.get("blocks"),
                "turnovers": raw_stats.get("turnovers"),
                "offensiveRebounds": raw_stats.get("reboundsOffensive"),
                "defensiveRebounds": raw_stats.get("reboundsDefensive"),
                "personalFouls": raw_stats.get("foulsPersonal"),
                "fieldGoalsMade": raw_stats.get("fieldGoalsMade"),
                "fieldGoalsAttempted": raw_stats.get("fieldGoalsAttempted"),
                "threePointFieldGoalsMade": raw_stats.get("threePointersMade"),
                "threePointFieldGoalsAttempted": raw_stats.get("threePointersAttempted"),
                "freeThrowsMade": raw_stats.get("freeThrowsMade"),
                "freeThrowsAttempted": raw_stats.get("freeThrowsAttempted"),
            }
            canonical = _canonical_player_stats(stat_map)
            for key in ("PTS", "REB", "AST", "STL", "BLK", "TOV", "OREB", "DREB", "PF"):
                aggregate[key] += canonical.get(key) or 0
            if not name or not _player_allowed(str(name), allowed_names):
                continue
            team_players.append(
                {
                    "playerName": str(name),
                    "starter": bool(player.get("starter")),
                    "stats": canonical,
                }
            )
        players_by_team[abbr] = team_players
        aggregate["FG"] = None
        aggregate["3PT"] = None
        aggregate["FT"] = None
        aggregate["MIN"] = None
        teams[abbr] = aggregate
    return players_by_team, teams


def _has_enough_stats(teams: dict[str, dict[str, Any]], players: dict[str, list[dict[str, Any]]]) -> bool:
    if not players:
        return False
    for team_players in players.values():
        for player in team_players:
            stats = player.get("stats") or {}
            if any(stats.get(key) is not None for key in ("PTS", "REB", "AST", "3PT")):
                return True
    for stats in teams.values():
        if any(stats.get(key) is not None for key in ("PTS", "REB", "AST", "FG", "3PT", "FT")):
            return True
    return False


def build_full_stats(
    game: dict[str, Any],
    *,
    allowed_names: set[str] | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    if game.get("statusState") not in {"in", "post"}:
        return {"available": False, "source": "unavailable", "teams": {}, "players": {}}
    normalized_allowed = {normalize_player_identity(name) for name in allowed_names or set() if name}
    summary_boxscore = game.get("summaryBoxscore") or {}
    teams = _teams_from_summary(summary_boxscore)
    players = _players_from_summary(summary_boxscore, normalized_allowed or None)
    if _has_enough_stats(teams, players):
        return {"available": True, "source": "espn", "teams": teams, "players": players}
    live_boxscore = game.get("nbaLiveBoxscore") or {}
    if not live_boxscore and game.get("eventId"):
        game_id = game.get("nbaGameId")
        if not game_id and game.get("requestedDate"):
            try:
                game_id = find_game_id_by_matchup(
                    game["requestedDate"],
                    game["away"]["abbr"],
                    game["home"]["abbr"],
                    base_url=base_url,
                )
            except NBAReportError:
                game_id = None
        try:
            if game_id:
                live_boxscore = fetch_live_boxscore(str(game_id), base_url=base_url)["data"]
        except NBAReportError:
            live_boxscore = {}
    players, teams = _players_from_nba_live(live_boxscore, normalized_allowed or None)
    if _has_enough_stats(teams, players):
        return {"available": True, "source": "nba_live", "teams": teams, "players": players}
    return {"available": False, "source": "unavailable", "teams": {}, "players": {}}


def render_markdown(payload: dict[str, Any], lang: str) -> str:
    title = "比赛全统计" if lang == "zh" else "Full Game Stats"
    lines = [f"# {title}", f"- Available: {payload['available']}", f"- Source: {payload['source']}"]
    for abbr, stats in sorted((payload.get("teams") or {}).items()):
        compact = ", ".join(f"{key}={value}" for key, value in stats.items() if value is not None)
        lines.append(f"- {abbr}: {compact or 'N/A'}")
    for abbr, players in sorted((payload.get("players") or {}).items()):
        if not players:
            continue
        lines.append(f"## {abbr}")
        for player in players[:8]:
            stats = ", ".join(f"{key}={value}" for key, value in player["stats"].items() if value is not None)
            lines.append(f"- {player['playerName']}: {stats or 'N/A'}")
    return "\n".join(lines)


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
                game["requestedDate"] = report["requestedDate"]
                return game
        raise NBAReportError("当前条件下未找到对应比赛。", kind="not_found")
    game = report["games"][0]
    game["requestedDate"] = report["requestedDate"]
    return game


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        game = _resolve_game(args)
        payload = build_full_stats(game, base_url=args.base_url)
        if args.format == "markdown":
            print(render_markdown(payload, args.lang))
        else:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    except NBAReportError as exc:
        print(f"[{exc.kind}] {exc}", file=sys.stderr)
        return 2 if exc.kind == "invalid_arguments" else 1


if __name__ == "__main__":
    raise SystemExit(main())
