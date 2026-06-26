#!/usr/bin/env python3
"""Render NBA reports with advanced pregame, live, and postgame analysis."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Callable

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from nba_common import NBAReportError  # noqa: E402
from entity_guard import extract_primary_name, normalize_player_identity  # noqa: E402
from nba_today_report import (  # noqa: E402
    I18N,
    build_report_payload,
    format_counts_summary,
    render_detail_blocks,
    render_team_lines,
    safe_float,
    validate_args,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Return NBA report with advanced analysis.")
    parser.add_argument("--tz", help="IANA timezone, UTC offset, or city hint")
    parser.add_argument("--date", help="Requested local date in YYYY-MM-DD; defaults to today in requestor timezone")
    parser.add_argument("--team", help="Optional team abbreviation or alias")
    parser.add_argument("--view", default="day", choices=("day", "game"), help="Render daily overview or a single game")
    parser.add_argument("--lang", default="zh", choices=("zh", "en"), help="Response language")
    parser.add_argument("--format", default="markdown", choices=("markdown", "json"), help="Output format")
    parser.add_argument("--base-url", help="Override ESPN base URL for testing")
    parser.add_argument(
        "--analysis-mode",
        default="auto",
        choices=("auto", "pregame", "live", "post"),
        help="Choose analysis logic automatically or force a specific mode.",
    )
    return parser.parse_args(argv)


def parse_record_text(value: str | None) -> tuple[int, int] | None:
    text = (value or "").strip()
    if "-" not in text:
        return None
    wins_text, losses_text = text.split("-", 1)
    try:
        return int(wins_text), int(losses_text)
    except ValueError:
        return None


def parse_period_score(value: str | None) -> int:
    try:
        return int((value or "0").strip())
    except ValueError:
        return 0


def abbr_by_team_id(game: dict[str, Any], team_id: str | None) -> str | None:
    if not team_id:
        return None
    if game["home"].get("id") == team_id:
        return game["home"]["abbr"]
    if game["away"].get("id") == team_id:
        return game["away"]["abbr"]
    return None


def team_form_for_side(game: dict[str, Any], side: str) -> dict[str, Any]:
    abbr = game[side]["abbr"]
    return (game.get("context", {}).get("teamForm", {}) or {}).get(abbr) or {}


def standings_for_side(game: dict[str, Any], side: str) -> dict[str, Any]:
    snapshot = team_form_for_side(game, side)
    if snapshot.get("standings"):
        return snapshot["standings"]
    team_id = game[side].get("id") or ""
    return game.get("standings", {}).get(team_id) or {}


def last_five_for_side(game: dict[str, Any], side: str) -> dict[str, Any]:
    snapshot = team_form_for_side(game, side)
    if snapshot.get("recentForm"):
        return snapshot["recentForm"]
    team_id = game[side].get("id") or ""
    return game.get("lastFiveGames", {}).get(team_id) or {}


def season_stats_for_side(game: dict[str, Any], side: str) -> dict[str, str]:
    snapshot = team_form_for_side(game, side)
    if snapshot.get("seasonStats"):
        return snapshot["seasonStats"]
    return game.get("teamSeasonStats", {}).get(game[side]["abbr"]) or {}


def schedule_context_for_side(game: dict[str, Any], side: str) -> dict[str, Any]:
    snapshot = team_form_for_side(game, side)
    if snapshot.get("schedule"):
        return snapshot["schedule"]
    return game.get("teamScheduleContext", {}).get(game[side]["abbr"]) or {}


def head_to_head_context(game: dict[str, Any]) -> dict[str, Any]:
    return game.get("context", {}).get("headToHead") or {}


def full_stats_for_side(game: dict[str, Any], side: str) -> dict[str, Any]:
    return (game.get("fullStats", {}).get("teams") or {}).get(game[side]["abbr"]) or {}


def injury_burden(game: dict[str, Any], side: str) -> float:
    snapshot = team_form_for_side(game, side)
    injury_snapshot = snapshot.get("injuries") or {}
    if injury_snapshot.get("burden") is not None:
        return float(injury_snapshot["burden"])
    burden = 0.0
    for item in game.get("injuries", {}).get(game[side]["abbr"], []):
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


def compare_metric(game: dict[str, Any], metric: str, higher_is_better: bool = True) -> str | None:
    home_value = safe_float(season_stats_for_side(game, "home").get(metric))
    away_value = safe_float(season_stats_for_side(game, "away").get(metric))
    if home_value is None or away_value is None or home_value == away_value:
        return None
    better_side = "home" if home_value > away_value else "away"
    if not higher_is_better:
        better_side = "away" if better_side == "home" else "home"
    return better_side


def matchup_text(game: dict[str, Any], labels: dict[str, str]) -> str | None:
    away_matchup = matchup_candidate_text(game, "away")
    home_matchup = matchup_candidate_text(game, "home")
    if away_matchup and home_matchup:
        return f"{game['away']['abbr']} {away_matchup} vs {game['home']['abbr']} {home_matchup}"
    return None


INELIGIBLE_MATCHUP_STATUSES = {"out", "doubtful", "questionable"}


def _injury_status_by_team(game: dict[str, Any], side: str) -> dict[str, str]:
    abbr = game[side]["abbr"]
    statuses: dict[str, str] = {}
    for item in (game.get("injuryItems", {}) or {}).get(abbr) or []:
        name = normalize_player_identity(item.get("playerName"))
        status = str(item.get("status") or "").strip()
        if name and status:
            statuses[name] = status
    return statuses


def _matchup_candidate_lines(game: dict[str, Any], side: str) -> list[str]:
    abbr = game[side]["abbr"]
    candidates: list[str] = []
    for group_name in ("leaders", "keyPlayers", "starters"):
        for line in (game.get(group_name, {}).get(abbr) or []):
            if line not in candidates:
                candidates.append(line)
    return candidates


def _is_matchup_eligible(line: str, *, allowed_names: set[str], status_by_player: dict[str, str]) -> bool:
    primary_name = extract_primary_name(line)
    normalized_name = normalize_player_identity(primary_name)
    if not normalized_name:
        return False
    if allowed_names and normalized_name not in allowed_names:
        return False
    lowered_status = str(status_by_player.get(normalized_name) or "").strip().casefold()
    if lowered_status in INELIGIBLE_MATCHUP_STATUSES:
        return False
    return True


def matchup_candidate_text(game: dict[str, Any], side: str) -> str | None:
    allowed_names = {normalize_player_identity(name) for name in (game.get("verifiedPlayers") or []) if name}
    status_by_player = _injury_status_by_team(game, side)
    for line in _matchup_candidate_lines(game, side):
        if _is_matchup_eligible(line, allowed_names=allowed_names, status_by_player=status_by_player):
            return line
    return None


def top_full_stats_player(game: dict[str, Any], side: str) -> str | None:
    players = (game.get("fullStats", {}).get("players") or {}).get(game[side]["abbr"]) or []
    best: tuple[int, str] | None = None
    for player in players:
        stats = player.get("stats") or {}
        points = stats.get("PTS")
        if points is None:
            continue
        line_parts = [str(player.get("playerName") or "")]
        for key in ("PTS", "REB", "AST"):
            if stats.get(key) is not None:
                line_parts.append(f"{stats[key]} {key}")
        line = " | ".join(line_parts)
        if best is None or int(points) > best[0]:
            best = (int(points), line)
    return best[1] if best else None


def team_totals_edge_reason(game: dict[str, Any], favored_side: str, labels: dict[str, str]) -> str | None:
    own = full_stats_for_side(game, favored_side)
    other = full_stats_for_side(game, "away" if favored_side == "home" else "home")
    if not own or not other:
        return None
    favored_abbr = game[favored_side]["abbr"]
    for key, higher_better in (
        ("REB", True),
        ("AST", True),
        ("TOV", False),
    ):
        own_value = safe_float(own.get(key))
        other_value = safe_float(other.get(key))
        if own_value is None or other_value is None or own_value == other_value:
            continue
        better = own_value > other_value if higher_better else own_value < other_value
        if better:
            if labels["timezone"] == "请求方时区":
                if key == "REB":
                    return f"{favored_abbr} 在篮板上以 {own_value:.0f}-{other_value:.0f} 占优"
                if key == "AST":
                    return f"{favored_abbr} 在助攻上以 {own_value:.0f}-{other_value:.0f} 占优"
                return f"{favored_abbr} 把失误控制在 {own_value:.0f} 次，对手是 {other_value:.0f} 次"
            if key == "REB":
                return f"{favored_abbr} won the glass {own_value:.0f}-{other_value:.0f}"
            if key == "AST":
                return f"{favored_abbr} finished ahead in assists {own_value:.0f}-{other_value:.0f}"
            return f"{favored_abbr} was cleaner with the ball, committing {own_value:.0f} turnovers to {other_value:.0f}"
    return None


def resolve_mode(game: dict[str, Any], requested_mode: str) -> str:
    state_to_mode = {"pre": "pregame", "in": "live", "post": "post"}
    actual_mode = state_to_mode.get(game["statusState"], "pregame")
    if requested_mode == "auto":
        return actual_mode
    if requested_mode != actual_mode:
        return actual_mode
    return requested_mode


def make_summary_line(game: dict[str, Any], labels: dict[str, str], favored_side: str | None, strength: int) -> str:
    if favored_side is None:
        return "两队赛前信号接近，属于胶着对局。" if labels["timezone"] == "请求方时区" else "The pregame indicators are tightly split, so this profiles as a close matchup."
    favored_abbr = game[favored_side]["abbr"]
    if labels["timezone"] == "请求方时区":
        if strength >= 4:
            return f"倾向 {favored_abbr}，赛前信号优势较明确。"
        if strength >= 2:
            return f"倾向 {favored_abbr}，但比赛仍有波动空间。"
        return f"{favored_abbr} 略占上风，整体仍接近五五开。"
    if strength >= 4:
        return f"{favored_abbr} has the clearer pregame edge."
    if strength >= 2:
        return f"{favored_abbr} has the better pregame case, but the matchup still has swing potential."
    return f"{favored_abbr} holds a slight edge, but the game still profiles as close."


def _story_signals(game: dict[str, Any]) -> list[dict[str, str]]:
    story = game.get("officialStory") or {}
    if not story.get("available"):
        return []
    return [signal for signal in (story.get("summarySignals") or []) if isinstance(signal, dict)]


def _story_brief(game: dict[str, Any], *, mode: str) -> dict[str, Any]:
    story = game.get("officialStory") or {}
    if not story.get("available"):
        return {}
    brief = story.get("storyBrief") or {}
    if not isinstance(brief, dict):
        return {}
    if str(brief.get("phase") or "") not in ("", "unknown", mode):
        return {}
    return brief


def _story_reason_text(signal: dict[str, str], labels: dict[str, str], *, mode: str) -> str:
    kind = str(signal.get("kind") or "")
    subject = str(signal.get("subject") or "").strip()
    value = str(signal.get("value") or "").strip()
    zh = labels["timezone"] == "请求方时区"
    if zh:
        if kind == "standout_scorer" and subject and value:
            return f"报道主线: {subject} {value} 分表现被列为重点"
        if kind == "short_handed":
            return "报道背景: 阵容短缺影响了比赛配置"
        if kind == "availability":
            return "报道背景: 伤病或球员可用性是关键变量"
        if kind == "series_context":
            return "报道背景: 这场比赛处在系列赛开局语境中"
        if kind == "previous_matchups":
            return "报道背景: 常规赛交手和阵容变化会影响判断"
        if kind == "efficiency":
            return "报道主线: 投篮效率是解释比赛的关键线索"
        if kind == "matchup_watch":
            return "报道看点: 阵容变化会影响核心对位"
        return "报道背景: NBA.com 提供了额外比赛语境"
    if kind == "standout_scorer" and subject and value:
        return f"Storyline: {subject}'s {value}-point night was central"
    if kind == "short_handed":
        return "Storyline: short-handed roster context shaped the game"
    if kind == "availability":
        return "Storyline: availability and injury context mattered"
    if kind == "series_context":
        return "Storyline: the game carried series-opening context"
    if kind == "previous_matchups":
        return "Storyline: prior meetings and changed lineups shape the preview"
    if kind == "efficiency":
        return "Storyline: shooting efficiency was a key explanation"
    if kind == "matchup_watch":
        return "Storyline: lineup changes shape the key matchup"
    return "Storyline: NBA.com added game context"


def _localized_player_stat_fragment(line: str | None, labels: dict[str, str]) -> str:
    value = str(line or "").strip()
    if labels["timezone"] != "请求方时区" or not value:
        return value
    value = re.sub(r"\s+\|\s+", " / ", value)
    value = re.sub(r"(\d+(?:\.\d+)?)\s+PTS\b", r"\1分", value)
    value = re.sub(r"(\d+(?:\.\d+)?)\s+REB\b", r"\1板", value)
    value = re.sub(r"(\d+(?:\.\d+)?)\s+AST\b", r"\1助", value)
    return value


def build_pregame_analysis(game: dict[str, Any], labels: dict[str, str]) -> dict[str, Any]:
    scores = {"home": 0, "away": 0}
    reasons: list[tuple[int, str]] = []
    predictor = game.get("predictor") or {}
    pickcenter = game.get("pickcenter") or {}

    home_projection = predictor.get("homeProjection")
    away_projection = predictor.get("awayProjection")
    if home_projection is not None and away_projection is not None:
        diff = abs(home_projection - away_projection)
        favored_side = "home" if home_projection > away_projection else "away"
        scores[favored_side] += 2 if diff >= 10 else 1
        if labels["timezone"] == "请求方时区":
            reasons.append((3, f"ESPN predictor: {game[favored_side]['abbr']} {max(home_projection, away_projection):.1f}%"))
        else:
            reasons.append((3, f"ESPN predictor gives {game[favored_side]['abbr']} {max(home_projection, away_projection):.1f}%"))

    for side in ("home", "away"):
        last_five = last_five_for_side(game, side)
        if last_five:
            scores[side] += 0
    home_last_five = last_five_for_side(game, "home")
    away_last_five = last_five_for_side(game, "away")
    if home_last_five and away_last_five:
        home_wins = int(home_last_five.get("wins") or 0)
        away_wins = int(away_last_five.get("wins") or 0)
        if home_wins != away_wins:
            favored_side = "home" if home_wins > away_wins else "away"
            scores[favored_side] += 2 if abs(home_wins - away_wins) >= 2 else 1
            if labels["timezone"] == "请求方时区":
                reasons.append((2, f"近5场状态: {game[favored_side]['abbr']} {max(home_wins, away_wins)}-{min(home_wins, away_wins)}"))
            else:
                reasons.append((2, f"Recent form: {game[favored_side]['abbr']} is {max(home_wins, away_wins)}-{min(home_wins, away_wins)} over the last five"))

    home_standings = standings_for_side(game, "home")
    away_standings = standings_for_side(game, "away")
    home_pct = safe_float(home_standings.get("winPercent"))
    away_pct = safe_float(away_standings.get("winPercent"))
    if home_pct is not None and away_pct is not None and home_pct != away_pct:
        favored_side = "home" if home_pct > away_pct else "away"
        scores[favored_side] += 2 if abs(home_pct - away_pct) >= 0.08 else 1
        if labels["timezone"] == "请求方时区":
            reasons.append((2, f"赛季战绩边际更好: {game[favored_side]['abbr']}"))
        else:
            reasons.append((2, f"Season profile edge: {game[favored_side]['abbr']} has the stronger record"))

    home_rest = schedule_context_for_side(game, "home")
    away_rest = schedule_context_for_side(game, "away")
    home_rest_days = home_rest.get("restDays")
    away_rest_days = away_rest.get("restDays")
    if home_rest_days is not None and away_rest_days is not None and home_rest_days != away_rest_days:
        favored_side = "home" if home_rest_days > away_rest_days else "away"
        scores[favored_side] += 1
        if labels["timezone"] == "请求方时区":
            reasons.append((1, f"赛程边际: {game[favored_side]['abbr']} 休整更充分"))
        else:
            reasons.append((1, f"Scheduling edge: {game[favored_side]['abbr']} comes in with more rest"))

    home_injury = injury_burden(game, "home")
    away_injury = injury_burden(game, "away")
    if home_injury != away_injury:
        favored_side = "home" if home_injury < away_injury else "away"
        scores[favored_side] += 1
        if labels["timezone"] == "请求方时区":
            reasons.append((1, f"可用性边际: {game[favored_side]['abbr']} 伤病压力更小"))
        else:
            reasons.append((1, f"Availability edge: {game[favored_side]['abbr']} carries less injury risk"))

    profile_points = {"home": 0, "away": 0}
    for metric in ("avgPoints", "fieldGoalPct", "threePointPct", "assistTurnoverRatio"):
        winner = compare_metric(game, metric)
        if winner:
            profile_points[winner] += 1
    if profile_points["home"] != profile_points["away"]:
        favored_side = "home" if profile_points["home"] > profile_points["away"] else "away"
        scores[favored_side] += 1
        if labels["timezone"] == "请求方时区":
            reasons.append((1, f"进攻指标更优: {game[favored_side]['abbr']}"))
        else:
            reasons.append((1, f"Offensive profile edge: {game[favored_side]['abbr']}"))

    head_to_head = head_to_head_context(game)
    season_series_summary = str(head_to_head.get("seasonSeriesSummary") or "")
    wins_by_team = head_to_head.get("winsByTeam") or {}
    if wins_by_team:
        home_wins = int(wins_by_team.get(game["home"]["abbr"]) or 0)
        away_wins = int(wins_by_team.get(game["away"]["abbr"]) or 0)
        if home_wins != away_wins:
            favored_side = "home" if home_wins > away_wins else "away"
            scores[favored_side] += 1
            if labels["timezone"] == "请求方时区":
                reasons.append((1, f"交锋边际: {game[favored_side]['abbr']}"))
            else:
                reasons.append((1, f"Head-to-head edge: {game[favored_side]['abbr']}"))
    elif season_series_summary:
        if game["home"]["abbr"] in season_series_summary and "lead" in season_series_summary.lower():
            scores["home"] += 1
        elif game["away"]["abbr"] in season_series_summary and "lead" in season_series_summary.lower():
            scores["away"] += 1

    favored_side: str | None = None
    if scores["home"] != scores["away"]:
        favored_side = "home" if scores["home"] > scores["away"] else "away"
    strength = abs(scores["home"] - scores["away"])
    sorted_reasons = [text for _, text in sorted(reasons, key=lambda item: item[0], reverse=True)[:4]]
    for signal in _story_signals(game):
        story_reason = _story_reason_text(signal, labels, mode="pregame")
        if story_reason and story_reason not in sorted_reasons:
            sorted_reasons.append(story_reason)
        if len(sorted_reasons) >= 4:
            break
    analysis = {
        "mode": "pregame",
        "summary": make_summary_line(game, labels, favored_side, strength),
        "reasons": sorted_reasons,
        "trend": (
            f"{game[favored_side]['abbr']} 更像是赛前占优的一方。"
            if labels["timezone"] == "请求方时区" and favored_side
            else (
                f"{game[favored_side]['abbr']} has the stronger pregame lean."
                if favored_side
                else ("暂时没有明确赛前倾向。" if labels["timezone"] == "请求方时区" else "No clear pregame lean stands out.")
            )
        ),
        "turningPoint": "",
        "keyMatchup": matchup_text(game, labels) or "",
        "signals": {
            "homeScore": scores["home"],
            "awayScore": scores["away"],
            "pickcenter": pickcenter,
            "storySignals": _story_signals(game),
            "storyBrief": _story_brief(game, mode="pregame"),
        },
    }
    return analysis


def summarize_recent_run(game: dict[str, Any]) -> tuple[str | None, int]:
    scoring_plays = [play for play in game.get("playTimeline", [])[-8:] if play.get("scoringPlay")]
    if not scoring_plays:
        return None, 0
    points = {"home": 0, "away": 0}
    for play in scoring_plays:
        side = "home" if play.get("teamId") == game["home"].get("id") else "away"
        points[side] += int(play.get("scoreValue") or 0)
    if points["home"] == points["away"]:
        return None, 0
    side = "home" if points["home"] > points["away"] else "away"
    return side, abs(points["home"] - points["away"])


def win_probability_edge(game: dict[str, Any]) -> tuple[str | None, float | None]:
    timeline = game.get("winProbabilityTimeline") or []
    if not timeline:
        return None, None
    last_value = timeline[-1].get("homeWinPercentage")
    if last_value is None:
        return None, None
    if last_value > 0.5:
        return "home", float(last_value)
    if last_value < 0.5:
        return "away", float(1 - last_value)
    return None, float(last_value)


def biggest_swing_text(game: dict[str, Any], winner_side: str | None = None) -> str:
    timeline = game.get("winProbabilityTimeline") or []
    if len(timeline) < 2:
        return ""
    play_lookup = {play.get("id"): play for play in game.get("playTimeline", []) if play.get("id")}
    best_entry: tuple[float, dict[str, Any]] | None = None
    previous = timeline[0]
    for current in timeline[1:]:
        previous_value = previous.get("homeWinPercentage")
        current_value = current.get("homeWinPercentage")
        if previous_value is None or current_value is None:
            previous = current
            continue
        delta = current_value - previous_value
        if winner_side == "away":
            delta *= -1
        elif winner_side is None:
            delta = abs(delta)
        if best_entry is None or delta > best_entry[0]:
            best_entry = (delta, current)
        previous = current
    if not best_entry or best_entry[0] <= 0:
        return ""
    play = play_lookup.get(best_entry[1].get("playId") or "")
    if not play:
        return ""
    prefix = " ".join(part for part in (f"P{play.get('period')}" if play.get("period") else "", play.get("clock") or "") if part).strip()
    return f"{prefix} {play.get('text')}".strip()


def build_live_analysis(game: dict[str, Any], labels: dict[str, str]) -> dict[str, Any]:
    home_score = parse_period_score(game["home"].get("score"))
    away_score = parse_period_score(game["away"].get("score"))
    margin = abs(home_score - away_score)
    leading_side = "home" if home_score > away_score else "away" if away_score > home_score else None
    wp_side, wp_value = win_probability_edge(game)
    run_side, run_margin = summarize_recent_run(game)
    reasons: list[str] = []
    if leading_side:
        if labels["timezone"] == "请求方时区":
            reasons.append(f"当前比分: {game[leading_side]['abbr']} 领先 {margin} 分")
        else:
            reasons.append(f"Live score: {game[leading_side]['abbr']} leads by {margin}")
    if wp_side and wp_value is not None:
        percent = wp_value * 100
        if labels["timezone"] == "请求方时区":
            reasons.append(f"实时胜率倾向: {game[wp_side]['abbr']} 约 {percent:.1f}%")
        else:
            reasons.append(f"Win probability edge: {game[wp_side]['abbr']} around {percent:.1f}%")
    if run_side and run_margin:
        if labels["timezone"] == "请求方时区":
            reasons.append(f"近期攻势: {game[run_side]['abbr']} 近段净胜 {run_margin} 分")
        else:
            reasons.append(f"Recent run: {game[run_side]['abbr']} is +{run_margin} over the latest scoring stretch")
    if leading_side:
        full_stats_reason = team_totals_edge_reason(game, leading_side, labels)
        if full_stats_reason:
            reasons.append(full_stats_reason)

    if leading_side and ((margin >= 8 and (game.get("period") or 0) >= 4) or (wp_side == leading_side and (wp_value or 0) >= 0.75)):
        summary = (
            f"{game[leading_side]['abbr']} 当前更像是在掌控比赛走向。"
            if labels["timezone"] == "请求方时区"
            else f"{game[leading_side]['abbr']} currently looks in control of the game."
        )
    elif leading_side:
        summary = (
            f"{game[leading_side]['abbr']} 暂时占优，但比赛仍在可逆转区间。"
            if labels["timezone"] == "请求方时区"
            else f"{game[leading_side]['abbr']} holds the edge, but the game is still in swing range."
        )
    else:
        summary = "比赛仍然非常胶着。" if labels["timezone"] == "请求方时区" else "The game remains tightly contested."

    key_players: list[str] = []
    for side in ("away", "home"):
        entries = game.get("keyPlayers", {}).get(game[side]["abbr"]) or []
        if entries:
            key_players.append(f"{game[side]['abbr']} {entries[0]}")

    analysis = {
        "mode": "live",
        "summary": summary,
        "reasons": reasons[:4],
        "trend": (
            f"{game[leading_side]['abbr']} 目前更接近终盘优势方。"
            if labels["timezone"] == "请求方时区" and leading_side
            else (
                f"{game[leading_side]['abbr']} is better positioned right now."
                if leading_side
                else ("两队都还在争夺主动权。" if labels["timezone"] == "请求方时区" else "Both teams are still fighting for control.")
            )
        ),
        "turningPoint": biggest_swing_text(game),
        "keyMatchup": " / ".join(key_players[:2]),
        "signals": {
            "margin": margin,
            "leadingSide": leading_side,
            "winProbabilitySide": wp_side,
            "recentRunSide": run_side,
        },
    }
    return analysis


def decisive_period_text(game: dict[str, Any], winner_side: str, labels: dict[str, str]) -> str:
    info = decisive_period_info(game, winner_side, labels)
    return str(info.get("text") or "") if info else ""


def decisive_period_info(game: dict[str, Any], winner_side: str, labels: dict[str, str]) -> dict[str, Any] | None:
    away_scores = [parse_period_score(value) for value in game["away"].get("linescores") or []]
    home_scores = [parse_period_score(value) for value in game["home"].get("linescores") or []]
    if not away_scores or not home_scores:
        return None
    best_period = None
    best_margin = -1
    for index, (away_score, home_score) in enumerate(zip(away_scores, home_scores), start=1):
        diff = home_score - away_score
        winner_margin = diff if winner_side == "home" else -diff
        if winner_margin > best_margin:
            best_margin = winner_margin
            best_period = index
    if best_period is None or best_margin <= 0:
        return None
    if labels["timezone"] == "请求方时区":
        text = f"第 {best_period} 节净胜 {best_margin} 分"
    else:
        text = f"Quarter {best_period}: +{best_margin}"
    return {"period": best_period, "margin": best_margin, "text": text}


def _ordinal_period(period: int | None) -> str:
    if period is None:
        return "late game"
    mapping = {1: "first", 2: "second", 3: "third", 4: "fourth"}
    if period in mapping:
        return f"the {mapping[period]} quarter"
    return "overtime"


def _clock_text(play: dict[str, Any]) -> str:
    return str(play.get("clock") or "").strip()


def _period_value(play: dict[str, Any]) -> int | None:
    try:
        return int(play.get("period"))
    except (TypeError, ValueError):
        return None


def _period_time_label(play: dict[str, Any], labels: dict[str, str]) -> str:
    period = _period_value(play)
    clock = _clock_text(play)
    if labels["timezone"] == "请求方时区":
        if period and period > 4:
            return f"加时还剩 {clock}" if clock else "加时阶段"
        if period and clock:
            return f"第 {period} 节还剩 {clock}"
        if period:
            return f"第 {period} 节"
        return "关键阶段"
    if period and period > 4:
        return f"with {clock} left in overtime" if clock else "in overtime"
    if period and clock:
        return f"with {clock} left in {_ordinal_period(period)}"
    if period:
        return f"in {_ordinal_period(period)}"
    return "in the key stretch"


def _stage_label(play: dict[str, Any], labels: dict[str, str]) -> str:
    period = _period_value(play)
    clock = _clock_text(play)
    if not period:
        return "关键阶段" if labels["timezone"] == "请求方时区" else "the key stretch"
    if period > 4:
        return "加时阶段" if labels["timezone"] == "请求方时区" else "overtime"
    stage = ""
    if ":" in clock:
        minutes_text, _, _ = clock.partition(":")
        try:
            minutes = int(minutes_text)
        except ValueError:
            minutes = None
        if minutes is not None:
            if minutes >= 8:
                stage = "开局" if labels["timezone"] == "请求方时区" else "early"
            elif minutes >= 4:
                stage = "中段" if labels["timezone"] == "请求方时区" else "midway through"
            else:
                stage = "后段" if labels["timezone"] == "请求方时区" else "late in"
    if labels["timezone"] == "请求方时区":
        return f"第 {period} 节{stage}" if stage else f"第 {period} 节"
    if stage:
        return f"{stage} {_ordinal_period(period)}"
    return _ordinal_period(period)


def _play_side(game: dict[str, Any], play: dict[str, Any]) -> str | None:
    team_id = str(play.get("teamId") or "")
    if not team_id:
        return None
    if team_id == str(game["home"].get("id") or ""):
        return "home"
    if team_id == str(game["away"].get("id") or ""):
        return "away"
    return None


def _play_points(play: dict[str, Any], previous_play: dict[str, Any] | None, side: str) -> int:
    score_value = play.get("scoreValue")
    try:
        numeric = int(score_value)
    except (TypeError, ValueError):
        numeric = 0
    if numeric > 0:
        return numeric
    current_home = parse_period_score(str(play.get("homeScore") or "0"))
    current_away = parse_period_score(str(play.get("awayScore") or "0"))
    previous_home = parse_period_score(str((previous_play or {}).get("homeScore") or "0"))
    previous_away = parse_period_score(str((previous_play or {}).get("awayScore") or "0"))
    if side == "home":
        return max(0, current_home - previous_home)
    return max(0, current_away - previous_away)


def _scoring_plays(game: dict[str, Any]) -> list[dict[str, Any]]:
    plays = game.get("playTimeline") or []
    scoring: list[dict[str, Any]] = []
    previous_play: dict[str, Any] | None = None
    for play in plays:
        side = _play_side(game, play)
        if not side:
            previous_play = play
            continue
        points = _play_points(play, previous_play, side)
        if bool(play.get("scoringPlay")) or (play.get("scoreValue") in (None, "") and points > 0):
            if points > 0:
                scoring.append({"play": play, "side": side, "points": points})
        previous_play = play
    return scoring


def _best_scoring_streak(game: dict[str, Any], winner_side: str) -> dict[str, Any] | None:
    best: dict[str, Any] | None = None
    current: dict[str, Any] | None = None
    for item in _scoring_plays(game):
        if item["side"] != winner_side:
            current = None
            continue
        play = item["play"]
        points = int(item["points"])
        if current is None:
            current = {
                "side": winner_side,
                "points": points,
                "startPlay": play,
                "endPlay": play,
            }
        else:
            current_end = current.get("endPlay") or {}
            same_period = _period_value(current_end) == _period_value(play)
            previous_loser_score = current_end.get("awayScore") if winner_side == "home" else current_end.get("homeScore")
            current_loser_score = play.get("awayScore") if winner_side == "home" else play.get("homeScore")
            loser_score_held = (
                previous_loser_score not in (None, "")
                and current_loser_score not in (None, "")
                and parse_period_score(str(previous_loser_score)) == parse_period_score(str(current_loser_score))
            )
            if same_period and loser_score_held:
                current["points"] += points
                current["endPlay"] = play
            else:
                current = {
                    "side": winner_side,
                    "points": points,
                    "startPlay": play,
                    "endPlay": play,
                }
        if best is None or int(current["points"]) > int(best["points"]):
            best = dict(current)
    if best and int(best.get("points") or 0) >= 6:
        return best
    return None


def _scoring_sequences(game: dict[str, Any]) -> list[dict[str, Any]]:
    sequences: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for item in _scoring_plays(game):
        play = item["play"]
        side = item["side"]
        points = int(item["points"])
        if current is None:
            current = {
                "side": side,
                "points": points,
                "startPlay": play,
                "endPlay": play,
            }
            continue
        current_end = current.get("endPlay") or {}
        same_side = current.get("side") == side
        same_period = _period_value(current_end) == _period_value(play)
        previous_other_score = current_end.get("awayScore") if side == "home" else current_end.get("homeScore")
        current_other_score = play.get("awayScore") if side == "home" else play.get("homeScore")
        other_score_held = (
            previous_other_score not in (None, "")
            and current_other_score not in (None, "")
            and parse_period_score(str(previous_other_score)) == parse_period_score(str(current_other_score))
        )
        if same_side and same_period and other_score_held:
            current["points"] += points
            current["endPlay"] = play
        else:
            sequences.append(current)
            current = {
                "side": side,
                "points": points,
                "startPlay": play,
                "endPlay": play,
            }
    if current is not None:
        sequences.append(current)
    return sequences


def _margin_after_play(game: dict[str, Any], play: dict[str, Any], winner_side: str) -> int | None:
    home_score = play.get("homeScore")
    away_score = play.get("awayScore")
    if home_score in (None, "") or away_score in (None, ""):
        return None
    diff = parse_period_score(str(home_score)) - parse_period_score(str(away_score))
    winner_margin = diff if winner_side == "home" else -diff
    if winner_margin <= 0:
        return None
    return winner_margin


def _min_margin_after_play(game: dict[str, Any], play_id: str, winner_side: str) -> int | None:
    seen = False
    margins: list[int] = []
    for play in game.get("playTimeline") or []:
        if str(play.get("id") or "") == play_id:
            seen = True
        if not seen:
            continue
        margin = _margin_after_play(game, play, winner_side)
        if margin is not None:
            margins.append(margin)
    if not margins:
        return None
    return min(margins)


def _first_nonpositive_margin_after_play(game: dict[str, Any], play_id: str, winner_side: str) -> dict[str, Any] | None:
    seen = False
    for play in game.get("playTimeline") or []:
        if str(play.get("id") or "") == play_id:
            seen = True
            continue
        if not seen:
            continue
        home_score = play.get("homeScore")
        away_score = play.get("awayScore")
        if home_score in (None, "") or away_score in (None, ""):
            continue
        margin = _winner_margin_from_scores(home_score, away_score, winner_side)
        if margin <= 0:
            return play
    return None


def _play_sequence(game: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    plays = game.get("playTimeline") or []
    index_by_id = {
        str(play.get("id") or ""): index
        for index, play in enumerate(plays)
        if str(play.get("id") or "")
    }
    return plays, index_by_id


def _winner_margin_from_scores(home_score: Any, away_score: Any, winner_side: str) -> int:
    diff = parse_period_score(str(home_score or "0")) - parse_period_score(str(away_score or "0"))
    return diff if winner_side == "home" else -diff


def _margin_before_play(game: dict[str, Any], play: dict[str, Any], winner_side: str) -> int | None:
    plays, index_by_id = _play_sequence(game)
    play_id = str(play.get("id") or "")
    index = index_by_id.get(play_id)
    if index is None:
        return None
    if index > 0:
        previous = plays[index - 1]
        if previous.get("homeScore") in (None, "") or previous.get("awayScore") in (None, ""):
            return None
        return _winner_margin_from_scores(previous.get("homeScore"), previous.get("awayScore"), winner_side)
    side = _play_side(game, play)
    if not side or play.get("homeScore") in (None, "") or play.get("awayScore") in (None, ""):
        return None
    points = _play_points(play, None, side)
    home_before = parse_period_score(str(play.get("homeScore") or "0")) - (points if side == "home" else 0)
    away_before = parse_period_score(str(play.get("awayScore") or "0")) - (points if side == "away" else 0)
    return _winner_margin_from_scores(home_before, away_before, winner_side)


def _durable_margin_threshold(play: dict[str, Any]) -> int:
    period = _period_value(play) or 0
    return 2 if period >= 4 else 4


def _has_overtime(game: dict[str, Any]) -> bool:
    away_lines = game.get("away", {}).get("linescores") or []
    home_lines = game.get("home", {}).get("linescores") or []
    if len(away_lines) > 4 or len(home_lines) > 4:
        return True
    status_detail = str(game.get("statusDetail") or game.get("rawStatusDetail") or "")
    return "OT" in status_detail.upper()


def _clock_seconds(play: dict[str, Any]) -> float | None:
    clock = _clock_text(play)
    if not clock:
        return None
    if ":" in clock:
        minutes_text, _, seconds_text = clock.partition(":")
        try:
            return int(minutes_text) * 60 + float(seconds_text)
        except ValueError:
            return None
    try:
        return float(clock)
    except ValueError:
        return None


def _is_late_closeout_window(play: dict[str, Any]) -> bool:
    period = _period_value(play) or 0
    if period > 4:
        return True
    if period != 4:
        return False
    clock_seconds = _clock_seconds(play)
    return clock_seconds is not None and clock_seconds <= 180


def _play_index(game: dict[str, Any], play: dict[str, Any] | None) -> int | None:
    if not play:
        return None
    _, index_by_id = _play_sequence(game)
    return index_by_id.get(str(play.get("id") or ""))


def _play_within_range(game: dict[str, Any], play: dict[str, Any] | None, start_play: dict[str, Any], end_play: dict[str, Any]) -> bool:
    index = _play_index(game, play)
    start_index = _play_index(game, start_play)
    end_index = _play_index(game, end_play)
    if index is None or start_index is None or end_index is None:
        return False
    return start_index <= index <= end_index


def _sequence_start_margin(game: dict[str, Any], sequence: dict[str, Any], winner_side: str) -> int | None:
    return _margin_before_play(game, sequence.get("startPlay") or {}, winner_side)


def _sequence_end_margin(game: dict[str, Any], sequence: dict[str, Any], winner_side: str) -> int | None:
    return _margin_after_play(game, sequence.get("endPlay") or {}, winner_side)


def _sequence_margin_gain(game: dict[str, Any], sequence: dict[str, Any], winner_side: str) -> int | None:
    start_margin = _sequence_start_margin(game, sequence, winner_side)
    end_margin = _sequence_end_margin(game, sequence, winner_side)
    if start_margin is None or end_margin is None:
        return None
    return end_margin - start_margin


def _is_meaningful_separation_sequence(game: dict[str, Any], sequence: dict[str, Any], winner_side: str) -> bool:
    points = int(sequence.get("points") or 0)
    start_margin = _sequence_start_margin(game, sequence, winner_side)
    end_margin = _sequence_end_margin(game, sequence, winner_side)
    gain = _sequence_margin_gain(game, sequence, winner_side)
    if start_margin is None or end_margin is None:
        return False
    if points >= 6 and start_margin <= 0 and end_margin >= 4:
        return True
    if points >= 8 and end_margin >= 6:
        return True
    if gain is not None and gain >= 6 and end_margin >= 6:
        return True
    return False


def _sequence_break_play(game: dict[str, Any], sequence: dict[str, Any], winner_side: str) -> dict[str, Any] | None:
    return _first_nonpositive_margin_after_play(
        game,
        str((sequence.get("endPlay") or {}).get("id") or ""),
        winner_side,
    )


def _sequence_meta(game: dict[str, Any], sequence: dict[str, Any], winner_side: str) -> dict[str, Any]:
    start_play = sequence.get("startPlay") or {}
    end_play = sequence.get("endPlay") or {}
    break_play = _sequence_break_play(game, sequence, winner_side)
    return {
        "period": _period_value(start_play),
        "points": int(sequence.get("points") or 0),
        "startMargin": _sequence_start_margin(game, sequence, winner_side),
        "endMargin": _sequence_end_margin(game, sequence, winner_side),
        "marginGain": _sequence_margin_gain(game, sequence, winner_side),
        "leadBroken": break_play is not None,
        "breakPlayId": str((break_play or {}).get("id") or ""),
    }


def _best_sequence_for_side(
    game: dict[str, Any],
    side: str,
    *,
    predicate: Callable[[dict[str, Any]], bool] | None = None,
    winner_side: str | None = None,
    decisive_period_number: int | None = None,
    volatile_game: bool = False,
) -> dict[str, Any] | None:
    best: dict[str, Any] | None = None
    best_score: tuple[int, int, int, int, int] | None = None
    for sequence in _scoring_sequences(game):
        if sequence.get("side") != side:
            continue
        if predicate and not predicate(sequence):
            continue
        points = int(sequence.get("points") or 0)
        start_margin = _sequence_start_margin(game, sequence, winner_side or side)
        end_margin = _sequence_end_margin(game, sequence, winner_side or side) or 0
        gain = _sequence_margin_gain(game, sequence, winner_side or side) or 0
        period = _period_value(sequence.get("startPlay") or {}) or 99
        lead_broken = _sequence_break_play(game, sequence, winner_side or side) is not None
        if volatile_game:
            if points >= 8 and gain >= 8 and end_margin >= 8:
                category = 0
            elif start_margin is not None and start_margin <= 0 and points >= 6 and end_margin >= 6:
                category = 1
            elif decisive_period_number is not None and period == decisive_period_number and points >= 8:
                category = 2
            elif decisive_period_number is not None and period == decisive_period_number:
                category = 3
            else:
                category = 4
            if lead_broken and period == 1:
                if points <= 6 and end_margin <= 6:
                    category += 3
                else:
                    category += 1
            score = (-category, points, gain, end_margin, period)
        else:
            if start_margin is not None and start_margin <= 0 and end_margin >= 4:
                category = 0
            elif start_margin is not None and start_margin <= 3 and end_margin >= 6:
                category = 1
            elif decisive_period_number is not None and period == decisive_period_number:
                category = 2
            else:
                category = 3
            if lead_broken and period == 1 and points <= 6 and end_margin <= 6:
                category += 2
            score = (-category, points, gain, end_margin, -period)
        if best is None or score > best_score:
            best = sequence
            best_score = score
    return best


def _last_late_winner_play(game: dict[str, Any], winner_side: str) -> dict[str, Any] | None:
    fallback: dict[str, Any] | None = None
    for play in game.get("playTimeline") or []:
        if not _is_late_closeout_window(play):
            continue
        if _play_side(game, play) != winner_side:
            continue
        if _margin_after_play(game, play, winner_side) is None:
            continue
        fallback = play
    return fallback


def _play_descriptor(play: dict[str, Any], labels: dict[str, str]) -> str:
    play_text = str(play.get("text") or "").strip()
    if not play_text:
        return ""
    if labels["timezone"] == "请求方时区":
        return f"（{play_text}）"
    return f" ({play_text})"


def _sequence_or_play_time_label(sequence: dict[str, Any], labels: dict[str, str]) -> str:
    start_play = sequence.get("startPlay") or {}
    return _period_time_label(start_play, labels)


def _describe_margin_state(margin: int, *, lang: str) -> str:
    if lang == "zh":
        if margin < 0:
            return f"落后{abs(margin)}分"
        if margin == 0:
            return "平分"
        return f"领先{margin}分"
    if margin < 0:
        return f"a {abs(margin)}-point deficit"
    if margin == 0:
        return "a tie game"
    return f"a {margin}-point lead"


def _describe_break_context(
    game: dict[str, Any],
    break_play: dict[str, Any] | None,
    winner_side: str,
    loser_side: str,
    *,
    lang: str,
) -> str:
    if not break_play:
        return ""
    loser_abbr = game[loser_side]["abbr"]
    winner_margin = _winner_margin_from_scores(break_play.get("homeScore"), break_play.get("awayScore"), winner_side)
    period = _period_value(break_play)
    time_label = _period_time_label(break_play, {"timezone": "请求方时区" if lang == "zh" else "Requester Timezone"})
    if lang == "zh":
        if winner_margin < 0:
            return f"不过{loser_abbr} 在{time_label}一度完成反超"
        return f"不过{loser_abbr} 在{time_label}还是追平了比分"
    if winner_margin < 0:
        return f"But {loser_abbr} answered in {time_label} and briefly moved in front"
    return f"But {loser_abbr} answered in {time_label} and pulled level"


def _build_sequence_narrative(
    game: dict[str, Any],
    sequence: dict[str, Any],
    winner_side: str,
    loser_side: str,
    labels: dict[str, str],
    *,
    sequence_type: str,
    closeout_play: dict[str, Any] | None = None,
) -> str:
    lang = "zh" if labels["timezone"] == "请求方时区" else "en"
    winner_abbr = game[winner_side]["abbr"]
    loser_abbr = game[loser_side]["abbr"]
    time_label = _sequence_or_play_time_label(sequence, labels)
    start_margin = _sequence_start_margin(game, sequence, winner_side)
    end_margin = _sequence_end_margin(game, sequence, winner_side)
    points = int(sequence.get("points") or 0)
    end_play_id = str((sequence.get("endPlay") or {}).get("id") or "")
    lead_broken_play = _first_nonpositive_margin_after_play(game, end_play_id, winner_side)
    min_after = _min_margin_after_play(game, end_play_id, winner_side) if end_play_id else None
    threshold = _durable_margin_threshold(sequence.get("endPlay") or {})
    forced_overtime = _has_overtime(game)
    closeout_label = _period_time_label(closeout_play, labels) if closeout_play else ""
    closeout_descriptor = _play_descriptor(closeout_play or {}, labels)

    if lang == "zh":
        if start_margin is not None and end_margin is not None:
            sentence = (
                f"{time_label}，{winner_abbr} 借这波连得{points}分的攻势把比分从{_describe_margin_state(start_margin, lang='zh')}打到{_describe_margin_state(end_margin, lang='zh')}，"
                f"比赛从这里开始倾向{winner_abbr}。"
            )
        else:
            sentence = f"{time_label}，{winner_abbr} 借这波连得{points}分的攻势把比赛带向自己这一边。"
        if lead_broken_play and forced_overtime:
            if closeout_play:
                return (
                    f"{sentence} {_describe_break_context(game, lead_broken_play, winner_side, loser_side, lang='zh')}，"
                    f"最后还是{winner_abbr} 在{closeout_label}重新收住比赛{closeout_descriptor}。"
                )
            return f"{sentence} {_describe_break_context(game, lead_broken_play, winner_side, loser_side, lang='zh')}，最后还是{winner_abbr} 在加时重新收住比赛。"
        if lead_broken_play:
            if closeout_play:
                return (
                    f"{sentence} {_describe_break_context(game, lead_broken_play, winner_side, loser_side, lang='zh')}，"
                    f"最后还是{winner_abbr} 在{closeout_label}重新收住比赛{closeout_descriptor}。"
                )
            return f"{sentence} {_describe_break_context(game, lead_broken_play, winner_side, loser_side, lang='zh')}，最后还是{winner_abbr} 重新收住比赛。"
        if min_after is not None and min_after > threshold:
            return f"{sentence} {loser_abbr} 此后虽有追分，但没再把分差追到{threshold}分以内。"
        return f"{sentence} {loser_abbr} 此后虽有追分，但没再把比分带回平局或反超。"

    if start_margin is not None and end_margin is not None:
        sentence = (
            f"{time_label[0].upper() + time_label[1:]}, {winner_abbr} used a {points}-0 burst to turn "
            f"{_describe_margin_state(start_margin, lang='en')} into {_describe_margin_state(end_margin, lang='en')}, "
            f"which is where the game started to tilt."
        )
    else:
        sentence = f"{time_label[0].upper() + time_label[1:]}, {winner_abbr} used that stretch to tilt the game its way."
    if lead_broken_play and forced_overtime:
        if closeout_play:
            return (
                f"{sentence} {_describe_break_context(game, lead_broken_play, winner_side, loser_side, lang='en')}, "
                f"but {winner_abbr} regained control {closeout_label}{closeout_descriptor}."
            )
        return f"{sentence} {_describe_break_context(game, lead_broken_play, winner_side, loser_side, lang='en')}, but {winner_abbr} regained control in overtime."
    if lead_broken_play:
        if closeout_play:
            return (
                f"{sentence} {_describe_break_context(game, lead_broken_play, winner_side, loser_side, lang='en')}, "
                f"but {winner_abbr} regained control {closeout_label}{closeout_descriptor}."
            )
        return f"{sentence} {_describe_break_context(game, lead_broken_play, winner_side, loser_side, lang='en')}, but {winner_abbr} regained control late."
    if min_after is not None and min_after > threshold:
        return f"{sentence} {loser_abbr} threatened, but never got the margin back within {threshold} after that stretch."
    return f"{sentence} {loser_abbr} threatened, but never got back to level after that stretch."


def _build_closeout_narrative(
    game: dict[str, Any],
    play: dict[str, Any],
    winner_side: str,
    loser_side: str,
    decisive_period: dict[str, Any] | None,
    labels: dict[str, str],
) -> str:
    lang = "zh" if labels["timezone"] == "请求方时区" else "en"
    winner_abbr = game[winner_side]["abbr"]
    time_label = _period_time_label(play, labels)
    margin_after = _margin_after_play(game, play, winner_side)
    descriptor = _play_descriptor(play, labels)
    decisive_period_number = int(decisive_period["period"]) if decisive_period else None

    if lang == "zh":
        main = f"{time_label}，{winner_abbr} 用这次回合把比赛真正收住"
        if margin_after is not None:
            main += f"，场面也稳在{margin_after}分优势上"
        main += f"{descriptor}。"
        if decisive_period_number and _period_value(play) != decisive_period_number:
            return f"{main} 真正把分差拉开的是第 {decisive_period_number} 节，{winner_abbr} 单节净胜{decisive_period['margin']}分。"
        return main

    main = f"{time_label[0].upper() + time_label[1:]}, {winner_abbr} effectively shut the game down"
    if margin_after is not None:
        main += f" with the margin sitting at {margin_after}"
    main += f"{descriptor}."
    if decisive_period_number and _period_value(play) != decisive_period_number:
        return f"{main} The bigger separation had already come in {_ordinal_period(decisive_period_number)}, when {winner_abbr} won the quarter by {decisive_period['margin']}."
    return main


def _select_turning_point_narrative(
    game: dict[str, Any],
    winner_side: str,
    loser_side: str,
    labels: dict[str, str],
) -> dict[str, Any]:
    decisive_period = decisive_period_info(game, winner_side, labels)
    meaningful_sequences = [
        sequence
        for sequence in _scoring_sequences(game)
        if sequence.get("side") == winner_side and _is_meaningful_separation_sequence(game, sequence, winner_side)
    ]
    stable_meaningful_sequences = [
        sequence
        for sequence in meaningful_sequences
        if _sequence_break_play(game, sequence, winner_side) is None
    ]
    volatile_game = _has_overtime(game) or not stable_meaningful_sequences
    separation_sequence = _best_sequence_for_side(
        game,
        winner_side,
        predicate=lambda seq: _is_meaningful_separation_sequence(game, seq, winner_side),
        winner_side=winner_side,
        decisive_period_number=int(decisive_period["period"]) if decisive_period else None,
        volatile_game=volatile_game,
    )
    swing_sequence = _best_sequence_for_side(
        game,
        winner_side,
        predicate=lambda seq: (_sequence_start_margin(game, seq, winner_side) or 1) <= 0,
        winner_side=winner_side,
        decisive_period_number=int(decisive_period["period"]) if decisive_period else None,
        volatile_game=volatile_game,
    )
    closeout_play = _last_late_winner_play(game, winner_side)
    forced_overtime = _has_overtime(game)

    if separation_sequence:
        sequence_type = "swing_sequence" if (_sequence_start_margin(game, separation_sequence, winner_side) or 1) <= 0 else "separation_sequence"
        return {
            "text": _build_sequence_narrative(
                game,
                separation_sequence,
                winner_side,
                loser_side,
                labels,
                sequence_type=sequence_type,
                closeout_play=closeout_play,
            ),
            "type": sequence_type,
            "leadBroken": _sequence_break_play(game, separation_sequence, winner_side) is not None,
            "forcedOvertime": forced_overtime,
            "selectedSequenceWindow": {
                "startPlayId": str((separation_sequence.get("startPlay") or {}).get("id") or ""),
                "endPlayId": str((separation_sequence.get("endPlay") or {}).get("id") or ""),
            },
            "selectedSequenceMeta": _sequence_meta(game, separation_sequence, winner_side),
            "usedSequenceReason": True,
        }
    if swing_sequence:
        return {
            "text": _build_sequence_narrative(
                game,
                swing_sequence,
                winner_side,
                loser_side,
                labels,
                sequence_type="swing_sequence",
                closeout_play=closeout_play,
            ),
            "type": "swing_sequence",
            "leadBroken": _sequence_break_play(game, swing_sequence, winner_side) is not None,
            "forcedOvertime": forced_overtime,
            "selectedSequenceWindow": {
                "startPlayId": str((swing_sequence.get("startPlay") or {}).get("id") or ""),
                "endPlayId": str((swing_sequence.get("endPlay") or {}).get("id") or ""),
            },
            "selectedSequenceMeta": _sequence_meta(game, swing_sequence, winner_side),
            "usedSequenceReason": True,
        }
    if closeout_play:
        return {
            "text": _build_closeout_narrative(game, closeout_play, winner_side, loser_side, decisive_period, labels),
            "type": "closeout_sequence",
            "leadBroken": False,
            "forcedOvertime": forced_overtime,
            "selectedSequenceWindow": {
                "startPlayId": str(closeout_play.get("id") or ""),
                "endPlayId": str(closeout_play.get("id") or ""),
            },
            "selectedSequenceMeta": {},
            "usedSequenceReason": False,
        }
    return {
        "text": "",
        "type": "",
        "leadBroken": False,
        "forcedOvertime": forced_overtime,
        "selectedSequenceWindow": {},
        "selectedSequenceMeta": {},
        "usedSequenceReason": False,
    }


def _biggest_swing_play(game: dict[str, Any], winner_side: str | None = None) -> dict[str, Any] | None:
    timeline = game.get("winProbabilityTimeline") or []
    if len(timeline) < 2:
        return None
    play_lookup = {play.get("id"): play for play in game.get("playTimeline", []) if play.get("id")}
    best_entry: tuple[float, dict[str, Any]] | None = None
    previous = timeline[0]
    for current in timeline[1:]:
        previous_value = previous.get("homeWinPercentage")
        current_value = current.get("homeWinPercentage")
        if previous_value is None or current_value is None:
            previous = current
            continue
        delta = current_value - previous_value
        if winner_side == "away":
            delta *= -1
        elif winner_side is None:
            delta = abs(delta)
        if best_entry is None or delta > best_entry[0]:
            best_entry = (delta, current)
        previous = current
    if not best_entry or best_entry[0] <= 0:
        return None
    return play_lookup.get(best_entry[1].get("playId") or "")


def _describe_post_turning_point(game: dict[str, Any], winner_side: str, loser_side: str, labels: dict[str, str]) -> str:
    return (_select_turning_point_narrative(game, winner_side, loser_side, labels).get("text") or "").strip()


def _streak_reason_text(game: dict[str, Any], streak: dict[str, Any], winner_side: str, labels: dict[str, str]) -> str:
    points = int(streak.get("points") or 0)
    end_play = streak.get("endPlay") or {}
    stage = _stage_label(streak.get("startPlay") or {}, labels)
    margin_after = _margin_after_play(game, end_play, winner_side)
    winner_abbr = game[winner_side]["abbr"]
    if labels["timezone"] == "请求方时区":
        if margin_after is not None:
            return f"{stage}，{winner_abbr} 还打出一波连得{points}分的攻势，把领先抬到{margin_after}分。"
        return f"{stage}，{winner_abbr} 还打出一波连得{points}分的攻势。"
    if margin_after is not None:
        return f"{winner_abbr} also put together a {points}-0 burst {stage}, stretching the lead to {margin_after}."
    return f"{winner_abbr} also pieced together a {points}-0 burst {stage}."


def build_post_analysis(game: dict[str, Any], labels: dict[str, str]) -> dict[str, Any]:
    home_score = parse_period_score(game["home"].get("score"))
    away_score = parse_period_score(game["away"].get("score"))
    winner_side = "home" if home_score > away_score else "away"
    loser_side = "away" if winner_side == "home" else "home"
    margin = abs(home_score - away_score)
    decisive_period = decisive_period_text(game, winner_side, labels)
    turning_point = biggest_swing_text(game, winner_side=winner_side)
    reasons = [
        (
            f"最终比分差 {margin} 分，{game[winner_side]['abbr']} 收下比赛。"
            if labels["timezone"] == "请求方时区"
            else f"{game[winner_side]['abbr']} won by {margin} points."
        )
    ]
    if decisive_period:
        if labels["timezone"] == "请求方时区":
            reasons.append(f"决定性阶段: {decisive_period}")
        else:
            reasons.append(f"Decisive stretch: {decisive_period}")
    winner_key_player = top_full_stats_player(game, winner_side) or (game.get("keyPlayers", {}).get(game[winner_side]["abbr"]) or [None])[0]
    if winner_key_player:
        winner_key_player_display = _localized_player_stat_fragment(winner_key_player, labels)
        if labels["timezone"] == "请求方时区":
            reasons.append(f"关键球员: {game[winner_side]['abbr']} {winner_key_player_display}")
        else:
            reasons.append(f"Lead performer: {game[winner_side]['abbr']} {winner_key_player_display}")
    else:
        winner_key_player_display = ""
    full_stats_reason = team_totals_edge_reason(game, winner_side, labels)
    if full_stats_reason:
        reasons.append(full_stats_reason)
    for signal in _story_signals(game):
        story_reason = _story_reason_text(signal, labels, mode="post")
        if story_reason and story_reason not in reasons:
            reasons.append(story_reason)
        if len(reasons) >= 5:
            break
    article = game.get("article") or {}
    if article.get("headline"):
        reasons.append(str(article["headline"]))

    if labels["timezone"] == "请求方时区":
        if winner_key_player_display and full_stats_reason:
            summary = f"{game[winner_side]['abbr']} 赢下 {margin} 分，主线是 {winner_key_player_display} 的输出以及 {full_stats_reason}。"
        elif winner_key_player_display:
            summary = f"{game[winner_side]['abbr']} 赢下 {margin} 分，{winner_key_player_display} 是最直接的进攻支点。"
        elif full_stats_reason:
            summary = f"{game[winner_side]['abbr']} 赢下 {margin} 分，关键差异来自 {full_stats_reason}。"
        else:
            summary = f"{game[winner_side]['abbr']} 赢下 {margin} 分，决定性阶段来自 {decisive_period or '终场前的执行'}。"
    else:
        if winner_key_player_display and full_stats_reason:
            summary = f"{game[winner_side]['abbr']} won by {margin}, led by {winner_key_player_display} and {full_stats_reason}."
        elif winner_key_player_display:
            summary = f"{game[winner_side]['abbr']} won by {margin}, with {winner_key_player_display} as the clearest offensive hinge."
        elif full_stats_reason:
            summary = f"{game[winner_side]['abbr']} won by {margin}, with the key edge coming from {full_stats_reason}."
        else:
            summary = f"{game[winner_side]['abbr']} won by {margin}, with the decisive stretch coming from {decisive_period or 'late execution'}."
    trend = (
        f"{game[winner_side]['abbr']} 在关键时段压住了 {game[loser_side]['abbr']}。"
        if labels["timezone"] == "请求方时区"
        else f"{game[winner_side]['abbr']} separated during the decisive stretch against {game[loser_side]['abbr']}."
    )
    return {
        "mode": "post",
        "summary": summary,
        "reasons": reasons[:4],
        "trend": trend,
        "turningPoint": turning_point,
        "keyMatchup": matchup_text(game, labels) or "",
        "signals": {
            "winner": game[winner_side]["abbr"],
            "margin": margin,
            "decisivePeriod": decisive_period,
            "storySignals": _story_signals(game),
            "storyBrief": _story_brief(game, mode="post"),
        },
    }


def build_analysis(game: dict[str, Any], requested_mode: str, labels: dict[str, str]) -> dict[str, Any]:
    mode = resolve_mode(game, requested_mode)
    if mode == "pregame":
        analysis = build_pregame_analysis(game, labels)
    elif mode == "live":
        analysis = build_live_analysis(game, labels)
    else:
        analysis = build_post_analysis(game, labels)
    game["analysisSignals"] = analysis.get("signals") or {}
    game["analysisSummary"] = analysis
    return analysis


def render_analysis_block(analysis: dict[str, Any], labels: dict[str, str]) -> list[str]:
    lines = [f"## {labels['advanced_section']}", ""]
    lines.append(f"- {labels['analysis_summary']}: {analysis['summary']}")
    if analysis.get("trend"):
        lines.append(f"- {labels['analysis_trend']}: {analysis['trend']}")
    if analysis.get("keyMatchup"):
        lines.append(f"- {labels['analysis_key_matchup']}: {analysis['keyMatchup']}")
    if analysis.get("turningPoint"):
        lines.append(f"- {labels['analysis_turning_point']}: {analysis['turningPoint']}")
    if analysis.get("reasons"):
        lines.append(f"- {labels['analysis_reasons']}: {' / '.join(analysis['reasons'])}")
    lines.extend(["", labels["analysis_deep_note"]])
    return lines


def render_markdown(report: dict[str, Any], analysis_mode: str) -> str:
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
        analysis = build_analysis(game, analysis_mode, labels)
        lines.extend(render_team_lines(game, labels))
        lines.append("")
        lines.extend(render_detail_blocks(game, labels))
        lines.extend(render_analysis_block(analysis, labels))
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
            analysis = build_analysis(game, analysis_mode, labels)
            lines.extend(render_team_lines(game, labels))
            lines.append(f"- {labels['analysis_summary']}: {analysis['summary']}")
            if analysis.get("reasons"):
                lines.append(f"- {labels['analysis_reasons']}: {' / '.join(analysis['reasons'][:3])}")
            lines.append("")
    lines.append(labels["analysis_deep_note"])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        validate_args(args)
        report = build_report_payload(args)
        for game in report["games"]:
            build_analysis(game, args.analysis_mode, report["labels"])
        if args.format == "json":
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(render_markdown(report, args.analysis_mode))
        return 0
    except NBAReportError as exc:
        print(f"[{exc.kind}] {exc}", file=sys.stderr)
        return 2 if exc.kind == "invalid_arguments" else 1


if __name__ == "__main__":
    sys.exit(main())
