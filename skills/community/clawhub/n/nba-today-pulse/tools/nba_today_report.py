#!/usr/bin/env python3
"""Render NBA today's games using requestor timezone-aware filtering."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from nba_common import NBAReportError  # noqa: E402
from nba_player_names import display_player_name, localize_player_line, localize_player_list  # noqa: E402
from nba_teams import TEAM_DISPLAY, canonicalize_team_abbr, extract_teams_from_text, format_matchup_display, infer_zh_locale, normalize_team_input, team_display_name  # noqa: E402
from provider_espn import fetch_scoreboard, fetch_summary, fetch_team_schedule, fetch_team_statistics  # noqa: E402
from timezone_resolver import ResolvedTimezone, resolve_timezone  # noqa: E402

DEFAULT_SCOREBOARD_WORKERS = 3
DEFAULT_SUMMARY_WORKERS = 6

I18N = {
    "zh": {
        "title_day": "NBA 今日赛况",
        "title_game": "NBA 单场赛况",
        "timezone": "请求方时区",
        "requested_date": "请求日期",
        "view": "视图",
        "status_final": "已结束",
        "status_live": "进行中",
        "status_pre": "未开赛",
        "no_games": "该时区当天没有 NBA 比赛。",
        "final_section": "已结束比赛",
        "live_section": "进行中比赛",
        "pre_section": "未开赛比赛",
        "overview": "总览",
        "local_tip": "以下时间均为请求方本地时间。",
        "start_time": "开赛时间",
        "venue": "场馆",
        "broadcasts": "转播",
        "records": "战绩",
        "score_by_period": "各节比分",
        "leaders": "球队领袖",
        "starters": "首发名单",
        "lineup_unconfirmed": "首发尚未公布或当前免费数据源不可确认。",
        "injuries": "伤病",
        "recent_plays": "近期关键回合",
        "hotspots": "热点",
        "key_players": "关键球员",
        "status": "状态",
        "latest": "今日",
        "none": "无",
        "filter_team": "目标球队",
        "clock": "比赛时间",
        "team_stats": "球队数据",
        "data_note": "热点仅基于结构化赛况事实，不额外编造。",
        "counts_summary": "总场次",
        "advanced_section": "高阶分析",
        "analysis_summary": "分析摘要",
        "analysis_reasons": "核心依据",
        "analysis_trend": "走势判断",
        "analysis_turning_point": "转折点",
        "analysis_key_matchup": "关键对位",
        "analysis_deep_note": "高阶分析仅基于结构化比赛与球队数据，不提供投注建议。",
        "team_form": "球队近况",
        "head_to_head": "历史交锋",
        "season_series": "赛季交锋",
        "full_stats": "比赛全统计",
        "team_totals_compare": "球队整体数据对比",
        "key_player_lines": "关键球员数据",
        "season_average": "赛季场均",
        "pending": "待确认",
    },
    "en": {
        "title_day": "NBA Daily Report",
        "title_game": "NBA Game Report",
        "timezone": "Requestor Timezone",
        "requested_date": "Requested Date",
        "view": "View",
        "status_final": "Final",
        "status_live": "Live",
        "status_pre": "Scheduled",
        "no_games": "No NBA games fall on the requestor's local date.",
        "final_section": "Final Games",
        "live_section": "Live Games",
        "pre_section": "Scheduled Games",
        "overview": "Overview",
        "local_tip": "All times below are in the requestor's local timezone.",
        "start_time": "Start Time",
        "venue": "Venue",
        "broadcasts": "Broadcasts",
        "records": "Records",
        "score_by_period": "Score by Period",
        "leaders": "Team Leaders",
        "starters": "Starting Lineups",
        "lineup_unconfirmed": "Starting lineups are not yet confirmed or cannot be confirmed from the free data source.",
        "injuries": "Injuries",
        "recent_plays": "Recent Key Plays",
        "hotspots": "Hotspots",
        "key_players": "Key Players",
        "status": "Status",
        "latest": "today",
        "none": "None",
        "filter_team": "Target Team",
        "clock": "Game Clock",
        "team_stats": "Team Stats",
        "data_note": "Hotspots are derived only from structured game facts.",
        "counts_summary": "Game Counts",
        "advanced_section": "Advanced Analysis",
        "analysis_summary": "Analysis Summary",
        "analysis_reasons": "Key Reasons",
        "analysis_trend": "Direction",
        "analysis_turning_point": "Turning Point",
        "analysis_key_matchup": "Key Matchup",
        "analysis_deep_note": "Advanced analysis is derived from structured game and team data, not betting advice.",
        "team_form": "Team Form",
        "head_to_head": "Head-to-Head",
        "season_series": "Season Series",
        "full_stats": "Full Game Stats",
        "team_totals_compare": "Team Totals Comparison",
        "key_player_lines": "Key Player Lines",
        "season_average": "Season Avg",
        "pending": "Pending",
    },
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Return NBA daily status for the requestor's local date.")
    parser.add_argument("--tz", help="IANA timezone, UTC offset, or city hint")
    parser.add_argument("--date", help="Requested local date in YYYY-MM-DD; defaults to today in requestor timezone")
    parser.add_argument("--team", help="Optional team abbreviation or alias")
    parser.add_argument("--view", default="day", choices=("day", "game"), help="Render daily overview or a single game")
    parser.add_argument("--lang", default="zh", choices=("zh", "en"), help="Response language")
    parser.add_argument("--zh-locale", choices=("cn", "hk", "tw"), help="Chinese locale variant for team names")
    parser.add_argument("--format", default="markdown", choices=("markdown", "json"), help="Output format")
    parser.add_argument("--base-url", help="Override ESPN base URL for testing")
    return parser.parse_args(argv)


def validate_args(args: argparse.Namespace) -> None:
    if args.date:
        try:
            datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError as exc:
            raise NBAReportError("date 参数格式不合法，必须为 YYYY-MM-DD", kind="invalid_arguments") from exc


def parse_iso_datetime(value: str) -> datetime:
    normalized = (value or "").strip().replace("Z", "+00:00")
    if not normalized:
        raise NBAReportError("比赛时间字段缺失。", kind="invalid_data")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def format_local_datetime(value: datetime, tz: ResolvedTimezone) -> str:
    return value.astimezone(tz.tzinfo).strftime("%Y-%m-%d %H:%M %Z")


def localize_status_detail(status_state: str, status_detail: str, labels: dict[str, str]) -> str:
    if status_state == "pre":
        return labels["status_pre"]
    if status_state == "in":
        return status_detail or labels["status_live"]
    if status_state == "post":
        return status_detail or labels["status_final"]
    return status_detail or labels["status_pre"]


def build_game_counts(games: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"total": len(games), "pre": 0, "in": 0, "post": 0}
    for game in games:
        state = game.get("statusState")
        if state in counts:
            counts[state] += 1
    return counts


def format_counts_summary(counts: dict[str, int], labels: dict[str, str]) -> str:
    if labels["timezone"] == "请求方时区":
        return (
            f"{labels['counts_summary']}: 共 {counts['total']} 场 / "
            f"{labels['status_pre']} {counts['pre']} / "
            f"{labels['status_live']} {counts['in']} / "
            f"{labels['status_final']} {counts['post']}"
        )
    return (
        f"{labels['counts_summary']}: {counts['total']} total / "
        f"{labels['status_pre']} {counts['pre']} / "
        f"{labels['status_live']} {counts['in']} / "
        f"{labels['status_final']} {counts['post']}"
    )


def record_summary(competitor: dict[str, Any]) -> str | None:
    records = competitor.get("records") or []
    if records:
        summary = records[0].get("summary")
        if summary:
            return str(summary)
    return None


def parse_linescores(competitor: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for item in competitor.get("linescores") or []:
        value = item.get("displayValue") or item.get("value")
        if value is not None:
            values.append(str(value))
    return values


def normalize_competitors(competitors: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    home = next((item for item in competitors if item.get("homeAway") == "home"), {})
    away = next((item for item in competitors if item.get("homeAway") == "away"), {})
    if away or home:
        return away, home
    if len(competitors) >= 2:
        return competitors[0], competitors[1]
    return {}, {}


def parse_short_name_matchup(short_name: str) -> tuple[str | None, str | None]:
    teams = extract_teams_from_text(short_name)
    if len(teams) < 2:
        return None, None
    return teams[0], teams[1]


def event_matchup(event: dict[str, Any]) -> dict[str, str]:
    competition = (event.get("competitions") or [{}])[0]
    competitors = competition.get("competitors") or []
    away_competitor, home_competitor = normalize_competitors(competitors)
    away_abbr = canonicalize_team_abbr(((away_competitor.get("team") or {}).get("abbreviation")))
    home_abbr = canonicalize_team_abbr(((home_competitor.get("team") or {}).get("abbreviation")))
    if away_abbr and home_abbr:
        return {"away": away_abbr, "home": home_abbr}
    short_name = str(event.get("shortName") or "")
    away_text, home_text = parse_short_name_matchup(short_name)
    return {"away": away_text or "", "home": home_text or ""}


def format_matchup_line(
    away_abbr: str | None,
    home_abbr: str | None,
    *,
    away_score: Any = None,
    home_score: Any = None,
) -> str:
    away = away_abbr or "AWAY"
    home = home_abbr or "HOME"
    if away_score is not None or home_score is not None:
        return f"{away} {away_score or ''} @ {home} {home_score or ''}".replace("  ", " ").strip()
    return f"{away} @ {home}"


def _labels_lang(labels: dict[str, str]) -> str:
    return "zh" if labels.get("timezone") == "请求方时区" else "en"


def extract_summary_leaders(summary: dict[str, Any]) -> dict[str, list[str]]:
    by_team: dict[str, list[str]] = {}
    for entry in summary.get("leaders") or []:
        team = entry.get("team") or {}
        abbr = canonicalize_team_abbr(team.get("abbreviation"))
        if not abbr:
            continue
        lines: list[str] = []
        for leader in entry.get("leaders") or []:
            athlete = leader.get("leaders", [{}])[0].get("athlete", {})
            athlete_name = athlete.get("displayName") or athlete.get("shortName")
            display_value = leader.get("leaders", [{}])[0].get("displayValue")
            if athlete_name and display_value:
                lines.append(f"{athlete_name} ({display_value})")
        if lines:
            by_team[str(abbr)] = lines[:3]
    return by_team


def extract_injuries(summary: dict[str, Any]) -> dict[str, list[str]]:
    by_team: dict[str, list[str]] = defaultdict(list)
    for entry in summary.get("injuries") or []:
        team = entry.get("team") or {}
        abbr = canonicalize_team_abbr(team.get("abbreviation"))
        if not abbr:
            continue
        for injury in entry.get("injuries") or []:
            athlete = injury.get("athlete") or {}
            name = athlete.get("displayName") or athlete.get("shortName")
            status = injury.get("status") or injury.get("type") or {}
            status_text = status.get("description") if isinstance(status, dict) else status
            detail = injury.get("detail") or injury.get("description")
            parts = [part for part in (name, status_text, detail) if part]
            if parts:
                by_team[str(abbr)].append(" - ".join(str(part) for part in parts))
    return dict(by_team)


def extract_starters_and_players(summary: dict[str, Any]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    starters: dict[str, list[str]] = {}
    key_players: dict[str, list[str]] = {}
    boxscore = summary.get("boxscore") or {}
    for team_group in boxscore.get("players") or []:
        team = team_group.get("team") or {}
        abbr = canonicalize_team_abbr(team.get("abbreviation"))
        if not abbr:
            continue
        team_starters: list[str] = []
        spotlights: list[str] = []
        for stat_group in team_group.get("statistics") or []:
            keys = stat_group.get("keys") or []
            for athlete_entry in stat_group.get("athletes") or []:
                athlete = athlete_entry.get("athlete") or {}
                name = athlete.get("displayName") or athlete.get("shortName")
                if not name:
                    continue
                if athlete_entry.get("starter"):
                    team_starters.append(str(name))
                stats = athlete_entry.get("stats") or []
                if not stats or not keys:
                    continue
                stat_map = {key: stats[index] for index, key in enumerate(keys) if index < len(stats)}
                points = stat_map.get("points")
                rebounds = stat_map.get("rebounds")
                assists = stat_map.get("assists")
                summary_parts = [name]
                if points is not None:
                    summary_parts.append(f"{points} PTS")
                if rebounds is not None:
                    summary_parts.append(f"{rebounds} REB")
                if assists is not None:
                    summary_parts.append(f"{assists} AST")
                if len(summary_parts) > 1:
                    spotlights.append(" | ".join(summary_parts))
            if team_starters or spotlights:
                break
        starters[str(abbr)] = team_starters[:5]
        key_players[str(abbr)] = spotlights[:5]
    return starters, key_players


def extract_recent_plays(summary: dict[str, Any], limit: int = 4) -> list[str]:
    recent: list[str] = []
    for play in (summary.get("plays") or [])[-limit:]:
        text = play.get("text")
        period = play.get("period", {}).get("displayValue") or play.get("period", {}).get("number")
        clock = play.get("clock", {}).get("displayValue")
        if text:
            prefix = " ".join(part for part in (f"P{period}" if period else "", clock or "") if part).strip()
            recent.append(f"{prefix} {text}".strip())
    return recent


def extract_headlines(event: dict[str, Any], summary: dict[str, Any]) -> list[str]:
    headlines: list[str] = []
    competition = (event.get("competitions") or [{}])[0]
    for item in competition.get("headlines") or []:
        headline = item.get("shortLinkText") or item.get("description") or item.get("text")
        if headline:
            headlines.append(str(headline))
    news = summary.get("news") or []
    if isinstance(news, dict):
        for item in news.get("articles") or []:
            if isinstance(item, dict) and item.get("headline"):
                headlines.append(str(item["headline"]))
    elif isinstance(news, list):
        for item in news:
            if isinstance(item, dict) and item.get("headline"):
                headlines.append(str(item["headline"]))
            elif isinstance(item, str) and item.strip():
                headlines.append(item.strip())
    deduped: list[str] = []
    seen: set[str] = set()
    for headline in headlines:
        key = headline.casefold()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(headline)
    return deduped[:3]


def extract_team_stats(summary: dict[str, Any]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    boxscore = summary.get("boxscore") or {}
    for entry in boxscore.get("teams") or []:
        team = entry.get("team") or {}
        abbr = canonicalize_team_abbr(team.get("abbreviation"))
        if not abbr:
            continue
        stats: list[str] = []
        for stat in entry.get("statistics") or []:
            label = stat.get("label") or stat.get("abbreviation")
            value = stat.get("displayValue")
            if label and value:
                stats.append(f"{label}: {value}")
        result[str(abbr)] = stats[:6]
    return result


def safe_float(value: Any) -> float | None:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def safe_int(value: Any) -> int | None:
    parsed = safe_float(value)
    if parsed is None:
        return None
    return int(parsed)


def extract_predictor(summary: dict[str, Any]) -> dict[str, Any] | None:
    predictor = summary.get("predictor")
    if not isinstance(predictor, dict):
        return None
    home_team = predictor.get("homeTeam") or {}
    away_team = predictor.get("awayTeam") or {}
    home_projection = safe_float(home_team.get("gameProjection"))
    away_projection = safe_float(away_team.get("gameProjection"))
    if home_projection is None and away_projection is None:
        return None
    return {
        "header": predictor.get("header") or "",
        "homeTeamId": str(home_team.get("id") or ""),
        "awayTeamId": str(away_team.get("id") or ""),
        "homeProjection": home_projection,
        "awayProjection": away_projection,
    }


def extract_pickcenter(summary: dict[str, Any]) -> dict[str, Any] | None:
    pickcenter_entries = summary.get("pickcenter") or []
    if not pickcenter_entries:
        return None
    entry = pickcenter_entries[0]
    if not isinstance(entry, dict):
        return None
    return {
        "provider": ((entry.get("provider") or {}).get("name")) or "",
        "details": entry.get("details") or "",
        "spread": safe_float(entry.get("spread")),
        "overUnder": safe_float(entry.get("overUnder")),
        "homeMoneyLine": safe_int((((entry.get("homeTeamOdds") or {}).get("moneyLine")))),
        "awayMoneyLine": safe_int((((entry.get("awayTeamOdds") or {}).get("moneyLine")))),
    }


def extract_article(summary: dict[str, Any]) -> dict[str, str] | None:
    article = summary.get("article")
    if not isinstance(article, dict):
        return None
    headline = article.get("headline") or article.get("title")
    if not headline:
        return None
    return {
        "type": str(article.get("type") or ""),
        "headline": str(headline),
        "description": str(article.get("description") or ""),
        "source": str(article.get("source") or ""),
    }


def extract_standings_snapshot(summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    snapshots: dict[str, dict[str, Any]] = {}
    standings = summary.get("standings") or {}
    groups = standings.get("groups") or []
    for group in groups:
        entries = ((group.get("standings") or {}).get("entries")) or []
        for index, entry in enumerate(entries, start=1):
            team_id = str(entry.get("id") or "")
            if not team_id:
                continue
            stats = {stat.get("name"): stat.get("displayValue") for stat in entry.get("stats") or [] if stat.get("name")}
            snapshots[team_id] = {
                "rank": index,
                "team": entry.get("team") or "",
                "wins": stats.get("wins"),
                "losses": stats.get("losses"),
                "winPercent": stats.get("winPercent"),
                "gamesBehind": stats.get("gamesBehind"),
                "streak": stats.get("streak"),
            }
    return snapshots


def extract_last_five_snapshot(summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for entry in summary.get("lastFiveGames") or []:
        team = entry.get("team") or {}
        team_id = str(team.get("id") or "")
        abbr = canonicalize_team_abbr(team.get("abbreviation"))
        events = entry.get("events") or []
        wins = 0
        losses = 0
        games_counted = 0
        recent_scores: list[str] = []
        for event in events[:5]:
            game_result = str(event.get("gameResult") or "").strip().upper()
            outcome: str | None = None
            if game_result in {"W", "L"}:
                outcome = game_result
            else:
                winner_raw = event.get("winner")
                if isinstance(winner_raw, bool):
                    outcome = "W" if winner_raw else "L"
                else:
                    winner_text = str(winner_raw or "").strip().lower()
                    if winner_text == "true":
                        outcome = "W"
                    elif winner_text == "false":
                        outcome = "L"
            if outcome == "W":
                wins += 1
                games_counted += 1
            elif outcome == "L":
                losses += 1
                games_counted += 1
            if event.get("score"):
                recent_scores.append(str(event["score"]))
        if team_id:
            record = f"{wins}-{losses}" if games_counted else ""
            result[team_id] = {
                "abbr": abbr,
                "record": record,
                "wins": wins,
                "losses": losses,
                "gamesCounted": games_counted,
                "scores": recent_scores[:5],
            }
    return result


def flatten_team_statistics_payload(payload: dict[str, Any]) -> dict[str, str]:
    results = ((payload.get("results") or {}).get("stats") or {}).get("categories") or []
    flattened: dict[str, str] = {}
    for category in results:
        for stat in category.get("stats") or []:
            name = stat.get("name")
            display_value = stat.get("displayValue")
            if name and display_value is not None:
                flattened[str(name)] = str(display_value)
    return flattened


def extract_schedule_context(schedule_payload: dict[str, Any], event_id: str, start_time_utc: datetime) -> dict[str, Any]:
    events = schedule_payload.get("events") or []
    parsed_events: list[tuple[datetime, dict[str, Any]]] = []
    for event in events:
        try:
            parsed_events.append((parse_iso_datetime(event.get("date")), event))
        except NBAReportError:
            continue
    parsed_events.sort(key=lambda item: item[0])

    previous_event: dict[str, Any] | None = None
    next_event: dict[str, Any] | None = None
    for event_time, event in parsed_events:
        if str(event.get("id")) == event_id:
            continue
        if event_time < start_time_utc:
            previous_event = event
        elif event_time > start_time_utc and next_event is None:
            next_event = event

    def summarize_event(event: dict[str, Any] | None) -> dict[str, Any] | None:
        if not event:
            return None
        competition = (event.get("competitions") or [{}])[0]
        status = (competition.get("status") or {}).get("type") or {}
        return {
            "eventId": str(event.get("id") or ""),
            "shortName": str(event.get("shortName") or ""),
            "date": str(event.get("date") or ""),
            "status": str(status.get("state") or ""),
            "detail": str(status.get("detail") or status.get("description") or ""),
        }

    context: dict[str, Any] = {
        "previousGame": summarize_event(previous_event),
        "nextGame": summarize_event(next_event),
        "restDays": None,
        "isBackToBack": False,
    }
    if previous_event and previous_event.get("date"):
        previous_date = parse_iso_datetime(previous_event.get("date")).date()
        current_date = start_time_utc.date()
        rest_days = max((current_date - previous_date).days - 1, 0)
        context["restDays"] = rest_days
        context["isBackToBack"] = rest_days == 0
    return context


def extract_play_timeline(summary: dict[str, Any], limit: int = 600) -> list[dict[str, Any]]:
    timeline: list[dict[str, Any]] = []
    plays = summary.get("plays") or []
    for play in plays[-limit:]:
        timeline.append(
            {
                "id": str(play.get("id") or ""),
                "text": str(play.get("text") or ""),
                "shortDescription": str(play.get("shortDescription") or ""),
                "period": safe_int(((play.get("period") or {}).get("number"))),
                "clock": str(((play.get("clock") or {}).get("displayValue")) or ""),
                "homeScore": safe_int(play.get("homeScore")),
                "awayScore": safe_int(play.get("awayScore")),
                "scoreValue": safe_int(play.get("scoreValue")),
                "scoringPlay": bool(play.get("scoringPlay")),
                "teamId": str(((play.get("team") or {}).get("id")) or ""),
            }
        )
    return timeline


def extract_win_probability(summary: dict[str, Any], limit: int = 600) -> list[dict[str, Any]]:
    timeline: list[dict[str, Any]] = []
    entries = summary.get("winprobability") or []
    for entry in entries[-limit:]:
        timeline.append(
            {
                "playId": str(entry.get("playId") or ""),
                "homeWinPercentage": safe_float(entry.get("homeWinPercentage")),
                "tiePercentage": safe_float(entry.get("tiePercentage")),
            }
        )
    return timeline


def build_hotspots(game: dict[str, Any], labels: dict[str, str]) -> list[str]:
    hotspots: list[str] = []
    if game["statusState"] == "post":
        leaders = game["leaders"]
        for team_abbr in (game["away"]["abbr"], game["home"]["abbr"]):
            if leaders.get(team_abbr):
                hotspots.append(f"{team_abbr}: {leaders[team_abbr][0]}")
        if game["headlines"]:
            hotspots.append(game["headlines"][0])
    elif game["statusState"] == "in":
        if game["recentPlays"]:
            hotspots.append(game["recentPlays"][-1])
        leaders = game["leaders"]
        home_abbr = game["home"]["abbr"]
        away_abbr = game["away"]["abbr"]
        if leaders.get(home_abbr):
            hotspots.append(f"{home_abbr}: {leaders[home_abbr][0]}")
        if leaders.get(away_abbr):
            hotspots.append(f"{away_abbr}: {leaders[away_abbr][0]}")
    else:
        if game["startersConfirmed"]:
            hotspots.append(
                f"{labels['starters']}: "
                f"{game['away']['abbr']} {', '.join(game['starters'].get(game['away']['abbr']) or [])} / "
                f"{game['home']['abbr']} {', '.join(game['starters'].get(game['home']['abbr']) or [])}"
            )
        elif game["injuries"].get(game["away"]["abbr"]) or game["injuries"].get(game["home"]["abbr"]):
            away_injuries = game["injuries"].get(game["away"]["abbr"]) or []
            home_injuries = game["injuries"].get(game["home"]["abbr"]) or []
            first_injury = (away_injuries + home_injuries)[0] if (away_injuries or home_injuries) else None
            if first_injury:
                hotspots.append(first_injury)
    return hotspots[:3]


def enrich_game(
    event: dict[str, Any],
    summary: dict[str, Any],
    resolved_tz: ResolvedTimezone,
    labels: dict[str, str],
    team_statistics: dict[str, dict[str, str]],
    team_schedule_context: dict[str, dict[str, Any]],
    team_schedule_payloads: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    competition = (event.get("competitions") or [{}])[0]
    competitors = competition.get("competitors") or []
    away, home = normalize_competitors(competitors)
    status = competition.get("status") or event.get("status") or {}
    status_type = status.get("type") or {}
    start_time_utc = parse_iso_datetime(competition.get("date") or event.get("date"))
    leaders = extract_summary_leaders(summary)
    injuries = extract_injuries(summary)
    starters, key_players = extract_starters_and_players(summary)
    team_stats = extract_team_stats(summary)
    standings = extract_standings_snapshot(summary)
    last_five_games = extract_last_five_snapshot(summary)
    home_team_id = str((home.get("team") or {}).get("id") or "")
    away_team_id = str((away.get("team") or {}).get("id") or "")
    raw_status_detail = status_type.get("detail") or status_type.get("description") or ""
    status_state = status_type.get("state") or "pre"
    game = {
        "eventId": str(event.get("id")),
        "shortName": event.get("shortName") or "",
        "statusState": status_state,
        "statusDetail": localize_status_detail(status_state, raw_status_detail, labels),
        "displayStatusLocal": localize_status_detail(status_state, raw_status_detail, labels),
        "rawStatusDetail": raw_status_detail,
        "displayClock": status.get("displayClock") or "",
        "period": status.get("period"),
        "startTimeUtc": start_time_utc.isoformat(),
        "startTimeLocal": format_local_datetime(start_time_utc, resolved_tz),
        "startLocalDate": start_time_utc.astimezone(resolved_tz.tzinfo).date().isoformat(),
        "venue": (((summary.get("gameInfo") or {}).get("venue") or {}).get("fullName")) or (((competition.get("venue") or {}).get("fullName"))),
        "broadcasts": [item.get("names", [None])[0] or item.get("market") for item in competition.get("broadcasts") or [] if item],
        "away": {
            "id": away_team_id,
            "abbr": canonicalize_team_abbr((away.get("team") or {}).get("abbreviation")),
            "displayName": ((away.get("team") or {}).get("displayName")) or "",
            "score": away.get("score"),
            "record": record_summary(away),
            "linescores": parse_linescores(away),
        },
        "home": {
            "id": home_team_id,
            "abbr": canonicalize_team_abbr((home.get("team") or {}).get("abbreviation")),
            "displayName": ((home.get("team") or {}).get("displayName")) or "",
            "score": home.get("score"),
            "record": record_summary(home),
            "linescores": parse_linescores(home),
        },
        "leaders": leaders,
        "injuries": injuries,
        "starters": starters,
        "keyPlayers": key_players,
        "recentPlays": extract_recent_plays(summary),
        "headlines": extract_headlines(event, summary),
        "teamStats": team_stats,
        "predictor": extract_predictor(summary),
        "pickcenter": extract_pickcenter(summary),
        "standings": standings,
        "lastFiveGames": last_five_games,
        "seasonSeries": summary.get("seasonseries") or [],
        "article": extract_article(summary),
        "summaryBoxscore": summary.get("boxscore") or {},
        "teamSeasonStats": {
            canonicalize_team_abbr((away.get("team") or {}).get("abbreviation")): team_statistics.get(away_team_id) or {},
            canonicalize_team_abbr((home.get("team") or {}).get("abbreviation")): team_statistics.get(home_team_id) or {},
        },
        "teamScheduleContext": {
            canonicalize_team_abbr((away.get("team") or {}).get("abbreviation")): team_schedule_context.get(away_team_id) or {},
            canonicalize_team_abbr((home.get("team") or {}).get("abbreviation")): team_schedule_context.get(home_team_id) or {},
        },
        "teamSchedulePayloads": {
            canonicalize_team_abbr((away.get("team") or {}).get("abbreviation")): (team_schedule_payloads or {}).get(away_team_id) or {},
            canonicalize_team_abbr((home.get("team") or {}).get("abbreviation")): (team_schedule_payloads or {}).get(home_team_id) or {},
        },
        "playTimeline": extract_play_timeline(summary),
        "winProbabilityTimeline": extract_win_probability(summary),
        "analysisSignals": {},
        "analysisSummary": {},
        "context": {
            "teamForm": {},
            "headToHead": {},
        },
        "fullStats": {
            "available": False,
            "source": "unavailable",
            "teams": {},
            "players": {},
        },
        "meta": {
            "sections": {},
        },
    }
    game["startersConfirmed"] = bool(game["starters"].get(game["away"]["abbr"])) and bool(game["starters"].get(game["home"]["abbr"]))
    game["hotspots"] = build_hotspots(game, labels)
    return game


def _scoreboard_workers() -> int:
    raw_value = os.environ.get("NBA_TR_SCOREBOARD_WORKERS", "").strip()
    try:
        return max(1, min(int(raw_value), DEFAULT_SCOREBOARD_WORKERS))
    except ValueError:
        return DEFAULT_SCOREBOARD_WORKERS


def _summary_workers() -> int:
    raw_value = os.environ.get("NBA_TR_SUMMARY_WORKERS", "").strip()
    try:
        return max(1, min(int(raw_value), 12))
    except ValueError:
        return DEFAULT_SUMMARY_WORKERS


def load_candidate_events(
    target_date: date,
    resolved_tz: ResolvedTimezone,
    base_url: str | None,
    *,
    persistent_cache: bool = False,
) -> list[dict[str, Any]]:
    candidates: dict[str, dict[str, Any]] = {}
    provider_dates = [(target_date + timedelta(days=offset)).strftime("%Y%m%d") for offset in (-1, 0, 1)]
    payloads: list[dict[str, Any]] = []
    max_workers = min(len(provider_dates), _scoreboard_workers())
    if max_workers <= 1:
        for provider_date in provider_dates:
            payloads.append(fetch_scoreboard(provider_date, base_url=base_url, persistent_cache=persistent_cache)["data"])
    else:
        ordered_payloads: dict[str, dict[str, Any]] = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {
                executor.submit(
                    fetch_scoreboard,
                    provider_date,
                    base_url=base_url,
                    persistent_cache=persistent_cache,
                ): provider_date
                for provider_date in provider_dates
            }
            for future in as_completed(future_map):
                ordered_payloads[future_map[future]] = future.result()["data"]
        payloads = [ordered_payloads[provider_date] for provider_date in provider_dates]
    for payload in payloads:
        for event in payload.get("events") or []:
            event_id = str(event.get("id"))
            if not event_id:
                continue
            competition = (event.get("competitions") or [{}])[0]
            start_time_utc = parse_iso_datetime(competition.get("date") or event.get("date"))
            local_date = start_time_utc.astimezone(resolved_tz.tzinfo).date()
            if local_date == target_date:
                candidates[event_id] = event
    return list(candidates.values())


def fetch_event_summaries(
    events: list[dict[str, Any]],
    *,
    base_url: str | None,
    persistent_cache: bool = False,
) -> dict[str, dict[str, Any]]:
    event_ids = [str(event.get("id") or "") for event in events if str(event.get("id") or "")]
    if not event_ids:
        return {}
    max_workers = min(len(event_ids), _summary_workers())
    if max_workers <= 1:
        return {
            event_id: fetch_summary(event_id, base_url=base_url, persistent_cache=persistent_cache)["data"]
            for event_id in event_ids
        }
    results: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(
                fetch_summary,
                event_id,
                base_url=base_url,
                persistent_cache=persistent_cache,
            ): event_id
            for event_id in event_ids
        }
        for future in as_completed(future_map):
            results[future_map[future]] = future.result()["data"]
    return results


def _fetch_game_team_details(
    team_id: str,
    *,
    event_id: str,
    start_time_utc: datetime,
    base_url: str | None,
) -> tuple[str, dict[str, str], dict[str, Any], dict[str, Any]]:
    team_statistics: dict[str, str] = {}
    team_schedule_context: dict[str, Any] = {}
    team_schedule_payload: dict[str, Any] = {}
    if not team_id:
        return team_id, team_statistics, team_schedule_context, team_schedule_payload
    try:
        team_statistics = flatten_team_statistics_payload(fetch_team_statistics(team_id, base_url=base_url)["data"])
    except NBAReportError:
        team_statistics = {}
    try:
        team_schedule_payload = fetch_team_schedule(team_id, base_url=base_url)["data"]
        team_schedule_context = extract_schedule_context(team_schedule_payload, event_id, start_time_utc)
    except NBAReportError:
        team_schedule_payload = {}
        team_schedule_context = {}
    return team_id, team_statistics, team_schedule_context, team_schedule_payload


def build_report_payload(args: argparse.Namespace) -> dict[str, Any]:
    labels = I18N[args.lang]
    resolved_tz = resolve_timezone(args.tz)
    zh_locale = infer_zh_locale(
        lang=args.lang,
        tz_name=resolved_tz.name,
        explicit_zh_locale=getattr(args, "zh_locale", None),
    )
    target_date = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else datetime.now(resolved_tz.tzinfo).date()
    team_filter = normalize_team_input(args.team)
    target_view = "game" if team_filter else args.view
    detail_level = str(getattr(args, "detail_level", "full") or "full")
    persistent_cache = target_view == "day"
    events = load_candidate_events(target_date, resolved_tz, args.base_url, persistent_cache=persistent_cache)
    summaries_by_event = fetch_event_summaries(events, base_url=args.base_url, persistent_cache=persistent_cache)
    games: list[dict[str, Any]] = []
    selected_events: dict[str, dict[str, Any]] = {}
    for event in events:
        event_id = str(event.get("id"))
        summary_payload = summaries_by_event.get(event_id) or {}
        game = enrich_game(event, summary_payload, resolved_tz, labels, {}, {}, {})
        game.setdefault("meta", {})["zhLocale"] = zh_locale
        games.append(game)
        selected_events[event_id] = event

    games.sort(key=lambda item: item["startTimeUtc"])
    if team_filter:
        games = [game for game in games if team_filter in {game["home"]["abbr"], game["away"]["abbr"]}]

    view = target_view
    if view == "game":
        if not games:
            raise NBAReportError("当前条件下未找到对应比赛。", kind="not_found")
        if len(games) > 1 and not team_filter:
            raise NBAReportError("单场视图需要指定球队，否则当天存在多场比赛。", kind="invalid_arguments")
        if detail_level == "full":
            selected_game = games[0]
            selected_event = selected_events.get(selected_game["eventId"])
            if selected_event:
                competition = (selected_event.get("competitions") or [{}])[0]
                start_time_utc = parse_iso_datetime(competition.get("date") or selected_event.get("date"))
                team_ids = [
                    str((competitor.get("team") or {}).get("id") or "")
                    for competitor in competition.get("competitors") or []
                    if str((competitor.get("team") or {}).get("id") or "")
                ]
                unique_team_ids = list(dict.fromkeys(team_ids))
                team_statistics_cache: dict[str, dict[str, str]] = {}
                team_schedule_cache: dict[str, dict[str, Any]] = {}
                team_schedule_payload_cache: dict[str, dict[str, Any]] = {}
                if unique_team_ids:
                    max_workers = min(len(unique_team_ids), 2)
                    if max_workers <= 1:
                        for team_id in unique_team_ids:
                            fetched_team_id, team_stats, team_schedule_context, team_schedule_payload = _fetch_game_team_details(
                                team_id,
                                event_id=selected_game["eventId"],
                                start_time_utc=start_time_utc,
                                base_url=args.base_url,
                            )
                            team_statistics_cache[fetched_team_id] = team_stats
                            team_schedule_cache[fetched_team_id] = team_schedule_context
                            team_schedule_payload_cache[fetched_team_id] = team_schedule_payload
                    else:
                        with ThreadPoolExecutor(max_workers=max_workers) as executor:
                            future_map = {
                                executor.submit(
                                    _fetch_game_team_details,
                                    team_id,
                                    event_id=selected_game["eventId"],
                                    start_time_utc=start_time_utc,
                                    base_url=args.base_url,
                                ): team_id
                                for team_id in unique_team_ids
                            }
                            for future in as_completed(future_map):
                                fetched_team_id, team_stats, team_schedule_context, team_schedule_payload = future.result()
                                team_statistics_cache[fetched_team_id] = team_stats
                                team_schedule_cache[fetched_team_id] = team_schedule_context
                                team_schedule_payload_cache[fetched_team_id] = team_schedule_payload
                selected_game = enrich_game(
                    selected_event,
                    summaries_by_event.get(selected_game["eventId"]) or {},
                    resolved_tz,
                    labels,
                    team_statistics_cache,
                    team_schedule_cache,
                    team_schedule_payload_cache,
                )
                selected_game.setdefault("meta", {})["zhLocale"] = zh_locale
                games = [selected_game]
        games = [games[0]]

    game_counts = build_game_counts(games)

    return {
        "timezone": resolved_tz.name,
        "timezoneSource": resolved_tz.source,
        "requestedDate": target_date.isoformat(),
        "view": view,
        "lang": args.lang,
        "zhLocale": zh_locale,
        "teamFilter": team_filter,
        "games": games,
        "gameCounts": game_counts,
        "labels": labels,
    }


def render_team_lines(game: dict[str, Any], labels: dict[str, str]) -> list[str]:
    lang = _labels_lang(labels)
    zh_locale = (game.get("meta") or {}).get("zhLocale")
    away = game["away"]
    home = game["home"]
    away_name = team_display_name(away["abbr"], lang, zh_locale=zh_locale)
    home_name = team_display_name(home["abbr"], lang, zh_locale=zh_locale)
    lines = [
        f"### {format_matchup_display(away['abbr'], home['abbr'], lang=lang, zh_locale=zh_locale, away_score=away['score'], home_score=home['score'])}",
        f"- {labels['status']}: {game.get('displayStatusLocal') or game['statusDetail']}",
        f"- {labels['start_time']}: {game['startTimeLocal']}",
    ]
    if game["statusState"] == "in" and game.get("displayClock"):
        lines.append(f"- {labels['clock']}: Q{game.get('period') or '?'} {game['displayClock']}")
    if game.get("venue"):
        lines.append(f"- {labels['venue']}: {game['venue']}")
    if game.get("broadcasts"):
        lines.append(f"- {labels['broadcasts']}: {', '.join([item for item in game['broadcasts'] if item])}")
    lines.append(
        f"- {labels['records']}: {away_name} {away.get('record') or labels['none']} / "
        f"{home_name} {home.get('record') or labels['none']}"
    )
    if away.get("linescores") or home.get("linescores"):
        lines.append(
            f"- {labels['score_by_period']}: "
            f"{away_name} {'-'.join(away.get('linescores') or []) or labels['none']} / "
            f"{home_name} {'-'.join(home.get('linescores') or []) or labels['none']}"
        )
    if game["startersConfirmed"]:
        lines.append(
            f"- {labels['starters']}: "
            f"{away_name} {', '.join(localize_player_list(game['starters'].get(away['abbr']) or [], lang))} / "
            f"{home_name} {', '.join(localize_player_list(game['starters'].get(home['abbr']) or [], lang))}"
        )
    elif game["statusState"] == "pre":
        lines.append(f"- {labels['starters']}: {labels['lineup_unconfirmed']}")
    return lines


FULL_STATS_TEAM_ORDER = ("PTS", "REB", "OREB", "DREB", "AST", "STL", "BLK", "TOV", "PF", "FG", "3PT", "FT")
FULL_STATS_PLAYER_ORDER = ("MIN", "PTS", "REB", "AST", "STL", "BLK", "TOV", "FG", "3PT", "FT")
COMPACT_TEAM_TOTAL_KEYS = ("REB", "AST", "TOV", "FG", "3PT", "FT")

STAT_LABELS = {
    "zh": {
        "PTS": "得分",
        "REB": "篮板",
        "AST": "助攻",
        "STL": "抢断",
        "BLK": "盖帽",
        "TOV": "失误",
        "FG": "投篮",
        "3PT": "三分",
        "FT": "罚球",
        "MIN": "时间",
    },
    "en": {
        "PTS": "PTS",
        "REB": "REB",
        "AST": "AST",
        "STL": "STL",
        "BLK": "BLK",
        "TOV": "TOV",
        "FG": "FG",
        "3PT": "3PT",
        "FT": "FT",
        "MIN": "MIN",
    },
}

STAT_SUFFIXES_ZH = {
    "PTS": "分",
    "REB": "板",
    "AST": "助",
    "STL": "断",
    "BLK": "帽",
    "TOV": "失误",
}


def render_full_stats_team_line(stats: dict[str, Any]) -> str:
    parts = [f"{key} {stats[key]}" for key in FULL_STATS_TEAM_ORDER if stats.get(key) not in (None, "")]
    return ", ".join(parts)


def render_compact_team_totals_line(
    stats: dict[str, Any],
    *,
    lang: str,
    keys: tuple[str, ...] = COMPACT_TEAM_TOTAL_KEYS,
) -> str:
    parts: list[str] = []
    labels = STAT_LABELS.get(lang, STAT_LABELS["en"])
    separator = "，" if lang == "zh" else ", "
    for key in keys:
        value = stats.get(key)
        if value in (None, ""):
            continue
        label = labels.get(key, key)
        if lang == "zh":
            parts.append(f"{label} {value}")
        else:
            parts.append(f"{label} {value}")
    return separator.join(parts)


def _render_average_value(value: Any, *, percent: bool = False) -> str | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if percent:
        return f"{number * 100:.1f}%"
    if number.is_integer():
        return f"{int(number)}"
    return f"{number:.1f}"


def render_season_average_line(averages: dict[str, Any] | None, labels: dict[str, str]) -> str | None:
    if not averages:
        return None
    parts: list[str] = []
    for key in ("PTS", "REB", "AST", "STL", "BLK"):
        rendered = _render_average_value(averages.get(key))
        if rendered is not None:
            parts.append(f"{key} {rendered}")
    fg = _render_average_value(averages.get("FG_PCT"), percent=True)
    fg3 = _render_average_value(averages.get("FG3_PCT"), percent=True)
    if fg is not None:
        parts.append(f"FG% {fg}")
    if fg3 is not None:
        parts.append(f"3PT% {fg3}")
    if not parts:
        return None
    return f"{labels['season_average']}: {', '.join(parts)}"


def render_full_stats_player_line(player: dict[str, Any], labels: dict[str, str]) -> str:
    lang = _labels_lang(labels)
    stats = player.get("stats") or {}
    parts = [f"{key} {stats[key]}" for key in FULL_STATS_PLAYER_ORDER if stats.get(key) not in (None, "")]
    display_name = display_player_name(str(player.get("playerName") or ""), lang)
    text = f"{display_name}: {', '.join(parts)}" if parts else display_name
    averages = render_season_average_line(player.get("seasonAverages"), labels)
    if averages:
        return f"{text} ({averages})"
    return text


def render_compact_player_stat_line(
    player: dict[str, Any],
    *,
    lang: str,
    include_shooting: bool = True,
    include_minutes: bool = False,
    include_secondary: bool = True,
) -> str:
    stats = player.get("stats") or {}
    display_name = display_player_name(str(player.get("playerName") or ""), lang)
    if not display_name:
        return ""

    core_parts: list[str] = []
    for key in ("PTS", "REB", "AST"):
        value = stats.get(key)
        if value in (None, ""):
            continue
        if lang == "zh":
            core_parts.append(f"{value}{STAT_SUFFIXES_ZH[key]}")
        else:
            core_parts.append(f"{value} {STAT_LABELS['en'][key].lower()}")

    secondary_parts: list[str] = []
    if include_secondary:
        for key in ("STL", "BLK", "TOV"):
            value = stats.get(key)
            if value in (None, "", 0, "0"):
                continue
            if lang == "zh":
                secondary_parts.append(f"{value}{STAT_SUFFIXES_ZH[key]}")
            else:
                secondary_parts.append(f"{value} {STAT_LABELS['en'][key].lower()}")

    shooting_parts: list[str] = []
    if include_shooting:
        for key in ("FG", "3PT", "FT"):
            value = stats.get(key)
            if value in (None, ""):
                continue
            label = STAT_LABELS.get(lang, STAT_LABELS["en"]).get(key, key)
            shooting_parts.append(f"{label} {value}")

    if include_minutes and stats.get("MIN") not in (None, ""):
        minutes = stats["MIN"]
        if lang == "zh":
            secondary_parts.insert(0, f"{minutes}分钟")
        else:
            secondary_parts.insert(0, f"MIN {minutes}")

    if lang == "zh":
        body_parts = [" ".join(part for part in core_parts if part)]
        if secondary_parts:
            body_parts.append(" ".join(secondary_parts))
        if shooting_parts:
            body_parts.append("，".join(shooting_parts))
        body = "，".join(part for part in body_parts if part)
        return f"{display_name}：{body}" if body else display_name

    body = ", ".join(part for part in [", ".join(core_parts), ", ".join(secondary_parts), ", ".join(shooting_parts)] if part)
    return f"{display_name}: {body}" if body else display_name


def render_detail_blocks(game: dict[str, Any], labels: dict[str, str]) -> list[str]:
    lang = _labels_lang(labels)
    zh_locale = (game.get("meta") or {}).get("zhLocale")
    lines: list[str] = []
    if game["leaders"]:
        lines.append(f"#### {labels['leaders']}")
        for abbr in (game["away"]["abbr"], game["home"]["abbr"]):
            items = [localize_player_line(item, lang) for item in (game["leaders"].get(abbr) or [labels["none"]])]
            lines.append(f"- {team_display_name(abbr, lang, zh_locale=zh_locale)}: {', '.join(items)}")
        lines.append("")
    if game["keyPlayers"]:
        lines.append(f"#### {labels['key_players']}")
        for abbr in (game["away"]["abbr"], game["home"]["abbr"]):
            if game["keyPlayers"].get(abbr):
                items = [localize_player_line(item, lang) for item in game["keyPlayers"][abbr][:3]]
                lines.append(f"- {team_display_name(abbr, lang, zh_locale=zh_locale)}: {', '.join(items)}")
        lines.append("")
    if game["teamStats"]:
        lines.append(f"#### {labels['team_stats']}")
        for abbr in (game["away"]["abbr"], game["home"]["abbr"]):
            if game["teamStats"].get(abbr):
                lines.append(f"- {team_display_name(abbr, lang, zh_locale=zh_locale)}: {', '.join(game['teamStats'][abbr][:4])}")
        lines.append("")
    if game["injuries"]:
        lines.append(f"#### {labels['injuries']}")
        for abbr in (game["away"]["abbr"], game["home"]["abbr"]):
            if game["injuries"].get(abbr):
                items = [localize_player_line(item, lang) for item in game["injuries"][abbr][:4]]
                lines.append(f"- {team_display_name(abbr, lang, zh_locale=zh_locale)}: {'; '.join(items)}")
        lines.append("")
    if game["recentPlays"] and game["statusState"] == "in":
        lines.append(f"#### {labels['recent_plays']}")
        for item in game["recentPlays"]:
            lines.append(f"- {item}")
        lines.append("")
    if game["hotspots"]:
        lines.append(f"#### {labels['hotspots']}")
        for item in game["hotspots"]:
            lines.append(f"- {item}")
        lines.append("")
    context = game.get("context") or {}
    team_form = context.get("teamForm") or {}
    if team_form:
        lines.append(f"#### {labels['team_form']}")
        for abbr in (game["away"]["abbr"], game["home"]["abbr"]):
            snapshot = team_form.get(abbr) or {}
            if not snapshot.get("available"):
                continue
            recent = (snapshot.get("recentForm") or {}).get("record") or "N/A"
            rest_days = (snapshot.get("schedule") or {}).get("restDays")
            injuries = (snapshot.get("injuries") or {}).get("count")
            rest_text = labels["pending"] if rest_days is None else str(rest_days)
            lines.append(
                f"- {team_display_name(abbr, lang, zh_locale=zh_locale)}: recent {recent}, rest {rest_text}, "
                f"injuries {injuries if injuries is not None else labels['none']}"
            )
        lines.append("")
    head_to_head = context.get("headToHead") or {}
    if head_to_head.get("available"):
        lines.append(f"#### {labels['head_to_head']}")
        if head_to_head.get("seasonSeriesSummary"):
            lines.append(f"- {labels['season_series']}: {head_to_head['seasonSeriesSummary']}")
        latest = head_to_head.get("latestMeeting")
        if latest:
            latest_text = format_matchup_display(
                latest.get("awayAbbr"),
                latest.get("homeAbbr"),
                lang=lang,
                zh_locale=zh_locale,
                away_score=latest.get("awayScore"),
                home_score=latest.get("homeScore"),
            )
            lines.append(f"- latest: {latest_text} ({latest.get('detail') or labels['none']})")
        lines.append("")
    full_stats = game.get("fullStats") or {}
    if full_stats.get("available"):
        lines.append(f"#### {labels['full_stats']}")
        lines.append(f"##### {labels['team_totals_compare']}")
        for abbr in (game["away"]["abbr"], game["home"]["abbr"]):
            stats = (full_stats.get("teams") or {}).get(abbr) or {}
            if stats:
                compact = render_full_stats_team_line(stats)
                if compact:
                    lines.append(f"- {team_display_name(abbr, lang, zh_locale=zh_locale)}: {compact}")
        lines.append("")
        lines.append(f"##### {labels['key_player_lines']}")
        for abbr in (game["away"]["abbr"], game["home"]["abbr"]):
            players = (full_stats.get("players") or {}).get(abbr) or []
            if players:
                top_lines = [render_full_stats_player_line(player, labels) for player in players[:3]]
                lines.append(f"- {team_display_name(abbr, lang, zh_locale=zh_locale)}: {'; '.join([line for line in top_lines if line])}")
        lines.append("")
    return lines


def render_markdown(report: dict[str, Any]) -> str:
    labels = report["labels"]
    games = report["games"]
    game_counts = report["gameCounts"]
    title = labels["title_game"] if report["view"] == "game" else labels["title_day"]
    lines = [
        f"# {title} ({report['requestedDate']})",
        f"> {labels['timezone']}: {report['timezone']}",
        f"> {labels['requested_date']}: {report['requestedDate']}",
        f"> {labels['view']}: {report['view']}",
    ]
    if report.get("teamFilter"):
        lines.append(f"> {labels['filter_team']}: {report['teamFilter']}")
    if report["view"] == "day":
        lines.append(f"> {format_counts_summary(game_counts, labels)}")
    lines.extend(["", labels["local_tip"], ""])

    if not games:
        lines.append(f"- {labels['no_games']}")
        return "\n".join(lines)

    if report["view"] == "game":
        game = games[0]
        lines.extend(render_team_lines(game, labels))
        lines.append("")
        lines.extend(render_detail_blocks(game, labels))
        lines.append(labels["data_note"])
        return "\n".join(lines)

    grouped: dict[str, list[dict[str, Any]]] = {"post": [], "in": [], "pre": []}
    for game in games:
        grouped[game["statusState"]].append(game)

    for state, heading in (("in", labels["live_section"]), ("post", labels["final_section"]), ("pre", labels["pre_section"])):
        section_games = grouped.get(state) or []
        if not section_games:
            continue
        lines.extend([f"## {heading}", ""])
        for game in section_games:
            lines.extend(render_team_lines(game, labels))
            if game["hotspots"]:
                hotspot = " / ".join(game["hotspots"])
                lines.append(f"- {labels['hotspots']}: {hotspot}")
            lines.append("")
    lines.append(labels["data_note"])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        validate_args(args)
        report = build_report_payload(args)
        payload = report if args.format == "json" else render_markdown(report)
        if args.format == "json":
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(payload)
        return 0
    except NBAReportError as exc:
        print(f"[{exc.kind}] {exc}", file=sys.stderr)
        return 2 if exc.kind == "invalid_arguments" else 1


if __name__ == "__main__":
    sys.exit(main())
