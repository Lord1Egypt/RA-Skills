#!/usr/bin/env python3
"""Shared context builders for scene-specific NBA_TR scripts."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Any

from entity_guard import blocked_names, extract_primary_name, fallback_matchup_text, filter_headlines, filter_named_lines, normalize_player_identity, roster_names, verified_player_names, verified_player_names_by_team
from nba_game_full_stats import build_full_stats
from nba_head_to_head import build_head_to_head_context
from nba_advanced_report import build_analysis, render_analysis_block
from nba_common import NBAReportError
from nba_player_names import display_player_name, extract_player_mentions_from_text, localize_player_line, localize_player_list
from nba_play_digest import build_play_digest
from nba_team_form_snapshot import build_team_form_context
from nba_teams import canonicalize_team_abbr, extract_team_from_text, extract_teams_from_text, format_matchup_display, infer_zh_locale, normalize_team_input, provider_team_id, team_display_name
from nba_today_report import I18N, build_report_payload, format_counts_summary, load_candidate_events, render_compact_player_stat_line, render_compact_team_totals_line, render_detail_blocks, render_team_lines
from nba_today_report import render_full_stats_player_line, render_full_stats_team_line
from provider_nba_injuries import resolve_team_injury_sources
from provider_espn import extract_roster_players as extract_espn_roster_players
from provider_espn import fetch_scoreboard, fetch_team_roster, fetch_team_schedule
from provider_nba import (
    extract_boxscore_players,
    extract_live_boxscore_snapshot,
    extract_team_player_averages,
    extract_play_actions,
    extract_roster_players as extract_nba_roster_players,
    extract_scoreboard_games,
    fetch_team_player_averages,
    find_game_id_by_matchup,
    find_game_id_by_schedule,
    fetch_live_boxscore,
    fetch_play_by_play,
    fetch_nba_game_story,
    fetch_scoreboard as fetch_nba_scoreboard,
    fetch_team_roster as fetch_nba_team_roster,
    public_game_story_payload,
    unavailable_game_story,
)
from timezone_resolver import extract_timezone_hint, resolve_timezone

LANG_EN_PATTERNS = [r"\bin english\b", r"\benglish\b", r"\blang\s*=\s*en\b", r"\ben\b", r"\b英文\b"]
LANG_ZH_PATTERNS = [r"\bin chinese\b", r"\bchinese\b", r"\blang\s*=\s*zh\b", r"\bzh\b", r"\b中文\b"]
DATE_PATTERN = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")
_MULTI_PREGAME_BUDGET_LOCK = threading.Lock()
_MULTI_PREGAME_DEADLINE: float | None = None


def _pregame_multi_budget_seconds() -> int:
    raw = (os.environ.get("NBA_TR_PREGAME_MULTI_BUDGET_SECONDS") or "").strip()
    try:
        return max(int(raw), 0) if raw else 30
    except ValueError:
        return 30


@contextmanager
def _pregame_multi_budget_scope(enabled: bool):
    global _MULTI_PREGAME_DEADLINE
    with _MULTI_PREGAME_BUDGET_LOCK:
        previous_deadline = _MULTI_PREGAME_DEADLINE
        _MULTI_PREGAME_DEADLINE = time.monotonic() + _pregame_multi_budget_seconds() if enabled else None
    try:
        yield
    finally:
        with _MULTI_PREGAME_BUDGET_LOCK:
            _MULTI_PREGAME_DEADLINE = previous_deadline


def _remaining_pregame_multi_budget() -> float | None:
    with _MULTI_PREGAME_BUDGET_LOCK:
        deadline = _MULTI_PREGAME_DEADLINE
    if deadline is None:
        return None
    return deadline - time.monotonic()


def _bounded_multi_timeout(default_seconds: int, *, minimum_seconds: int = 1) -> int:
    remaining = _remaining_pregame_multi_budget()
    if remaining is None:
        return default_seconds
    if remaining <= 0:
        return 0
    return max(minimum_seconds, min(default_seconds, math.ceil(remaining)))
PREGAME_PATTERNS = [
    r"比赛前瞻",
    r"前瞻预测",
    r"比赛预测",
    r"对阵预测",
    r"对位分析",
    r"赛前情报",
    r"赛前信息",
    r"赛前预测",
    r"赛前分析",
    r"赛前展望",
    r"赛前看点",
    r"赛前解读",
    r"赛前",
    r"前瞻",
    r"预测",
    r"展望",
    r"对局分析",
    r"看好谁",
    r"谁更占优",
    r"谁会赢",
    r"谁能赢",
    r"\bpreview\b",
    r"\bpregame\b",
    r"\bpre[- ]?game\b",
    r"\bgame preview\b",
    r"\bmatch preview\b",
    r"\bpreview prediction\b",
    r"\bmatch prediction\b",
    r"\bpreview analysis\b",
    r"\bpredict(?:ion)?\b",
    r"\bmatchup analysis\b",
    r"\bwho has the edge\b",
    r"\bwho wins\b",
    r"\bwho will win\b",
    r"\bgame outlook\b",
    r"\bhow do they match up\b",
    r"\banaly[sz]e(?: the)? (?:game|matchup|preview|prediction)\b",
    r"\banaly[sz]e\b",
]
LIVE_PATTERNS = [
    r"赛中",
    r"正在进行",
    r"进行中",
    r"比赛进行中",
    r"走势",
    r"实时",
    r"实况",
    r"直播",
    r"实时比分",
    r"当前比分",
    r"比分更新",
    r"比赛走势",
    r"实时走势",
    r"比赛进程",
    r"比赛过程",
    r"\blive\b",
    r"\blive score\b",
    r"\bcurrent score\b",
    r"\bscore update\b",
    r"\bin[- ]?game\b",
    r"\bin progress\b",
    r"\bgame flow\b",
    r"\bplay[- ]?by[- ]?play\b",
    r"\bmomentum\b",
]
POST_PATTERNS = [
    r"复盘",
    r"复盘一下",
    r"回顾",
    r"赛后",
    r"赛后复盘",
    r"赛后回顾",
    r"赛后总结",
    r"赛后分析",
    r"赛后点评",
    r"赛后解析",
    r"赛后战报",
    r"比赛复盘",
    r"比赛回顾",
    r"比赛总结",
    r"总结比赛",
    r"\brecap\b",
    r"\bgame recap\b",
    r"\bpost\b",
    r"\bpost[- ]?game\b",
    r"\bpostgame\b",
    r"\bafter the game\b",
    r"\bafter[- ]?game\b",
    r"\bgame review\b",
    r"\bfinal recap\b",
    r"\bwhat happened in the game\b",
    r"\breview\b",
]
INJURY_PATTERNS = [
    r"伤病报告",
    r"伤病名单",
    r"伤病更新",
    r"伤病情况",
    r"伤病状态",
    r"伤病",
    r"伤情",
    r"伤情更新",
    r"伤停",
    r"伤停名单",
    r"可用性",
    r"出战情况",
    r"缺阵",
    r"缺席",
    r"\binjury report\b",
    r"\binjury updates?\b",
    r"\binjuries\b",
    r"\binjury\b",
    r"\bavailability\b",
    r"\bavailability report\b",
    r"\bstatus report\b",
    r"\binactive(?:s)?\b",
    r"\bwho(?:'s| is) out\b",
    r"\bwho(?:'s| is) in\b",
]
OFFICIAL_REPORT_PATTERNS = [
    r"https?://[^\s)>\]}]+/game/",
    r"官方报道",
    r"官网报道",
    r"官方报道总结",
    r"NBA\s*官网报道",
    r"赛前报道",
    r"赛后报道",
    r"官方文章",
    r"官方文章总结",
    r"报道总结",
    r"文章总结",
    r"官方复盘",
    r"官方赛报",
    r"官方故事",
    r"官网文章",
    r"官网赛报",
    r"报道摘要",
    r"故事摘要",
    r"\bpreview article\b",
    r"\bpreview articles\b",
    r"\brecap article\b",
    r"\brecap articles\b",
    r"\bofficial preview\b",
    r"\bofficial recap\b",
    r"\bofficial story\b",
    r"\bofficial stories\b",
    r"\bofficial article\b",
    r"\bofficial articles\b",
    r"\bofficial report\b",
    r"\bofficial reports\b",
    r"\bgame story\b",
    r"\bgame stories\b",
    r"\bgame article\b",
    r"\bgame articles\b",
    r"\bstory summary\b",
    r"\barticle summary\b",
    r"\breport summary\b",
    r"\bnba\.com story\b",
    r"\bnba\.com article\b",
]
STATS_DAY_PATTERNS = [
    r"今天比赛谁得分最高",
    r"比赛谁得分最高",
    r"今天谁得分最高",
    r"谁得分最高",
    r"今日得分王",
    r"得分王",
    r"最高得分",
    r"今天谁篮板最多",
    r"谁篮板最多",
    r"今日篮板王",
    r"今天谁助攻最多",
    r"谁助攻最多",
    r"今日助攻王",
    r"今天三分最多的是谁",
    r"三分最多的是谁",
    r"今日三分王",
    r"今天有谁拿到三双",
    r"有谁拿到三双",
    r"今天有谁拿到两双",
    r"有谁拿到两双",
    r"今日最佳表现",
    r"最佳表现",
    r"今天最大分差是哪场",
    r"最大分差是哪场",
    r"数据王",
    r"今日数据王",
    r"今日统计",
    r"今日数据统计",
    r"今天数据榜",
    r"数据榜",
    r"统计榜",
    r"今日排行榜",
    r"今日得分榜",
    r"今日篮板榜",
    r"今日助攻榜",
    r"今日三分榜",
    r"今天\s*NBA\s*统计",
    r"今日\s*NBA\s*统计",
    r"\bNBA\s*统计\b",
    r"今日统计",
    r"\b统计\b",
    r"\btoday'?s nba stats\b",
    r"\btoday stats\b",
    r"\btoday'?s stats\b",
    r"\bstat(?:s)? leaders\b",
    r"\btoday'?s leaders\b",
    r"\bleaders today\b",
    r"\btoday top scorer\b",
    r"\btop scorer\b",
    r"\bwho scored the most today\b",
    r"\bwho scored the most\b",
    r"\bwho had the most rebounds today\b",
    r"\bwho had the most rebounds\b",
    r"\bwho had the most assists today\b",
    r"\bwho had the most assists\b",
    r"\bmost threes today\b",
    r"\bmost threes\b",
    r"\bbest performance today\b",
    r"\bbest performance\b",
    r"\blargest margin today\b",
    r"\blargest margin\b",
    r"\bbiggest win\b",
    r"\bbest stat line\b",
]
ALL_GAMES_PATTERNS = [
    r"所有比赛",
    r"全部比赛",
    r"全部对局",
    r"今日赛程",
    r"今天赛程",
    r"今日比赛",
    r"今天比赛",
    r"今日赛况",
    r"今天赛况",
    r"\ball games\b",
    r"\bevery game\b",
    r"\ball matchups\b",
    r"\btoday'?s games\b",
    r"\ball games today\b",
    r"\bevery game today\b",
    r"\btoday'?s slate\b",
    r"\bdaily slate\b",
    r"\bgame slate\b",
    r"\btoday schedule\b",
]
MULTI_MATCHUP_SPLIT_PATTERNS = [r"和", r"以及", r"、", r",", r"，", r"\+", r"\band\b"]
DAY_LIVE_ONLY_PATTERNS = [
    r"今天正在打的比赛",
    r"今天进行中的比赛",
    r"进行中比赛",
    r"今天只看进行中",
    r"只看进行中",
    r"今天只看直播",
    r"只看直播",
    r"live only",
    r"today live only",
    r"\blive games\b",
    r"\blive games only\b",
    r"\bgames in progress\b",
    r"\bgames in progress only\b",
    r"\bongoing games\b",
    r"\bongoing games only\b",
    r"\btoday'?s live games\b",
    r"\bcurrent games\b",
]
DAY_POST_ONLY_PATTERNS = [
    r"今天已结束比赛复盘",
    r"今日赛后重点",
    r"今天已结束的比赛",
    r"今天只看已结束",
    r"只看已结束",
    r"今天只看赛后",
    r"只看赛后",
    r"今天只看完场",
    r"只看完场",
    r"final recap",
    r"today final only",
    r"today finished games",
    r"today'?s finished games",
    r"\bfinished games\b",
    r"\bfinished games only\b",
    r"\bfinal games\b",
    r"\bfinal games only\b",
    r"\bcompleted games\b",
    r"\bcompleted games only\b",
    r"\bfinal scores only\b",
]
FOCUS_KEY_PLAYER_PATTERNS = [
    r"只看关键球员",
    r"只看球员",
    r"只看核心球员",
    r"只看主要球员",
    r"只看.*球员",
    r"关键球员",
    r"球员表现",
    r"球员数据",
    r"主力球员",
    r"\bkey players only\b",
    r"\bjust key players\b",
    r"\bkey players\b",
    r"\bplayer breakdown\b",
    r"\bplayer lines\b",
    r"\bplayers only\b",
]
FOCUS_PLAY_DIGEST_PATTERNS = [
    r"只看回合摘要",
    r"只看回合",
    r"回合摘要",
    r"回合明细",
    r"回合梳理",
    r"关键回合",
    r"\bplay digest\b",
    r"\bplay by play\b",
    r"\bplay-by-play\b",
    r"\bpbp\b",
    r"\bjust plays\b",
    r"\bplays only\b",
    r"\bgame flow\b",
]
FOCUS_FOURTH_QUARTER_PATTERNS = [
    r"只看第四节",
    r"第四节",
    r"第4节",
    r"第四节回合",
    r"第四节摘要",
    r"末节",
    r"决胜节",
    r"\b4th quarter\b",
    r"\bfourth quarter\b",
    r"\bfinal quarter\b",
    r"\blast quarter\b",
    r"\b4q\b",
]
FOCUS_INJURY_PATTERNS = [
    r"只看伤病",
    r"只看伤情",
    r"\binjuries only\b",
    r"\binjury only\b",
    r"\binjury focus\b",
    r"\binjury breakdown\b",
]
FOLLOW_UP_REFRESH_PATTERNS = [
    r"^\s*(更新|刷新|再看一下|再看下|重新看|重新查|再来一版|再来一次|再看一遍|update|refresh|again|show again)\s*[。.!?？]*\s*$",
    r"^\s*(比分不对|比分变了吗|现在呢|现在比分|最新比分|最新情况|current score|latest score|score update|what(?:'s| is) the latest)\s*[。.!?？]*\s*$",
]
RELATIVE_DATE_PATTERNS = [
    (r"后天", 2),
    (r"明天|明日|\btomorrow\b", 1),
    (r"今天|今日|\btoday\b", 0),
    (r"昨天|昨日|\byesterday\b", -1),
]


def contains_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def detect_lang(command: str) -> str:
    lowered = command.strip()
    if contains_any(lowered, LANG_EN_PATTERNS):
        return "en"
    if contains_any(lowered, LANG_ZH_PATTERNS):
        return "zh"
    zh_chars = len(re.findall(r"[\u4e00-\u9fff]", lowered))
    en_words = len(re.findall(r"\b[a-zA-Z][a-zA-Z'-]*\b", lowered))
    return "zh" if zh_chars > en_words else "en"


def detect_analysis_mode(command: str) -> str:
    lowered = command.strip()
    if contains_any(lowered, PREGAME_PATTERNS):
        return "pregame"
    if contains_any(lowered, LIVE_PATTERNS):
        return "live"
    if contains_any(lowered, POST_PATTERNS):
        return "post"
    return "auto"


def detect_intent(command: str) -> str:
    lowered = command.strip()
    if contains_any(lowered, OFFICIAL_REPORT_PATTERNS):
        return "official_report"
    if contains_any(lowered, DAY_LIVE_ONLY_PATTERNS) or contains_any(lowered, DAY_POST_ONLY_PATTERNS):
        return "day"
    if contains_any(lowered, INJURY_PATTERNS):
        return "injury"
    if contains_any(lowered, STATS_DAY_PATTERNS):
        return "stats_day"
    if contains_any(lowered, POST_PATTERNS):
        return "post"
    if contains_any(lowered, LIVE_PATTERNS):
        return "live"
    if contains_any(lowered, PREGAME_PATTERNS):
        return "pregame"
    return "day"


def _contains_multi_separator(text: str) -> bool:
    return contains_any(text, MULTI_MATCHUP_SPLIT_PATTERNS)


def _all_games_requested(text: str) -> bool:
    return contains_any(text, ALL_GAMES_PATTERNS)


def extract_matchups_from_text(text: str | None) -> list[dict[str, str]]:
    teams = extract_teams_from_text(text or "")
    if len(teams) < 2:
        return []
    if len(teams) == 2:
        return [{"team": teams[0], "opponent": teams[1]}]
    if len(teams) % 2 != 0 or not _contains_multi_separator(text or ""):
        return []
    return [{"team": teams[index], "opponent": teams[index + 1]} for index in range(0, len(teams), 2)]


def detect_scope(command: str, intent: str, matchups: list[dict[str, str]], teams: list[str]) -> str:
    if intent == "official_report":
        if _all_games_requested(command) or (not teams and not matchups and not re.search(r"https?://[^\s)>\]}]+/game/", command, flags=re.IGNORECASE)):
            return "multi_all"
        if len(matchups) > 1:
            return "multi_explicit"
        return "single"
    if intent == "stats_day":
        return "multi_all"
    if intent == "pregame":
        if _all_games_requested(command) or (not teams and not matchups):
            return "multi_all"
        if len(matchups) > 1:
            return "multi_explicit"
    return "single"


def detect_day_phase_filter(command: str, intent: str) -> str | None:
    if intent != "day":
        return None
    if contains_any(command, DAY_LIVE_ONLY_PATTERNS):
        return "live"
    if contains_any(command, DAY_POST_ONLY_PATTERNS):
        return "post"
    return None


def detect_focus_section(command: str) -> str | None:
    if contains_any(command, FOCUS_FOURTH_QUARTER_PATTERNS):
        return "fourth_quarter"
    if contains_any(command, FOCUS_KEY_PLAYER_PATTERNS):
        return "key_players"
    if contains_any(command, FOCUS_INJURY_PATTERNS):
        return "injuries"
    if contains_any(command, FOCUS_PLAY_DIGEST_PATTERNS):
        return "play_digest"
    return None


def detect_followup_action(command: str) -> str | None:
    if contains_any(command, FOLLOW_UP_REFRESH_PATTERNS):
        return "refresh"
    return None


def _reference_now(tz: str | None) -> datetime:
    resolved_tz = resolve_timezone(tz)
    env_override = (os.environ.get("NBA_TR_NOW_ISO") or "").strip()
    if env_override:
        parsed = datetime.fromisoformat(env_override.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=resolved_tz.tzinfo)
        return parsed.astimezone(resolved_tz.tzinfo)
    return datetime.now(resolved_tz.tzinfo)


def detect_requested_date(command: str, tz: str | None) -> str | None:
    date_match = DATE_PATTERN.search(command)
    if date_match:
        return date_match.group(1)
    for pattern, offset in RELATIVE_DATE_PATTERNS:
        if re.search(pattern, command, flags=re.IGNORECASE):
            now = _reference_now(tz)
            return (now.date() + timedelta(days=offset)).isoformat()
    return None


def command_has_explicit_date(command: str) -> bool:
    if DATE_PATTERN.search(command):
        return True
    return any(re.search(pattern, command, flags=re.IGNORECASE) for pattern, _ in RELATIVE_DATE_PATTERNS)


def command_options(command: str, tz_hint: str | None = None) -> dict[str, Any]:
    timezone_hint = extract_timezone_hint(tz_hint) if tz_hint else extract_timezone_hint(command)
    tz_name = timezone_hint.name if timezone_hint else None
    lang = detect_lang(command)
    teams = extract_teams_from_text(command)
    matchups = extract_matchups_from_text(command)
    intent = detect_intent(command)
    players = extract_player_mentions_from_text(command)
    return {
        "lang": lang,
        "analysis_mode": detect_analysis_mode(command),
        "intent": intent,
        "date": detect_requested_date(command, tz_name),
        "team": teams[0] if teams else extract_team_from_text(command),
        "opponent": teams[1] if len(teams) > 1 else None,
        "teams": teams,
        "player": players[0] if players else None,
        "players": players,
        "matchups": matchups,
        "scope": detect_scope(command, intent, matchups, teams),
        "day_phase_filter": detect_day_phase_filter(command, intent),
        "focus_section": detect_focus_section(command),
        "followup_action": detect_followup_action(command),
        "tz": tz_name,
        "zh_locale": infer_zh_locale(lang=lang, tz_name=tz_name, command_text=command),
    }


def _normalize_injury_status(value: str | None) -> str:
    return str(value or "").strip().casefold()


def _pregame_injury_priority(
    item: dict[str, Any],
    *,
    leader_names: set[str],
    key_player_names: set[str],
    season_average_names: set[str],
) -> tuple[int, int, int, str]:
    player_name = extract_primary_name(str(item.get("playerName") or ""))
    status = _normalize_injury_status(item.get("status"))
    status_rank = {
        "out": 0,
        "doubtful": 1,
        "questionable": 2,
        "day-to-day": 3,
        "probable": 4,
    }.get(status, 5)
    player_rank = 3
    if player_name in leader_names:
        player_rank = 0
    elif player_name in key_player_names:
        player_rank = 1
    elif player_name in season_average_names:
        player_rank = 2
    return (status_rank, player_rank, 0, player_name.casefold())


def _format_injury_item(item: dict[str, Any]) -> str:
    return " - ".join(
        part
        for part in (
            item.get("playerName"),
            item.get("status"),
            item.get("detail"),
        )
        if part
    )


def _select_pregame_injury_lines(game: dict[str, Any], team_abbr: str, *, limit: int | None = None) -> list[str]:
    items = ((game.get("injuryItems") or {}).get(team_abbr) or [])
    if not items:
        return []
    leader_names = {extract_primary_name(line) for line in (game.get("leaders", {}).get(team_abbr) or [])}
    key_player_names = {extract_primary_name(line) for line in (game.get("keyPlayers", {}).get(team_abbr) or [])}
    season_average_names = set(((game.get("gameContext") or {}).get("seasonAverages") or {}).get(team_abbr, {}).keys())
    ordered = sorted(
        items,
        key=lambda item: _pregame_injury_priority(
            item,
            leader_names=leader_names,
            key_player_names=key_player_names,
            season_average_names=season_average_names,
        ),
    )
    lines: list[str] = []
    seen: set[str] = set()
    for item in ordered:
        line = _format_injury_item(item)
        if not line or line in seen:
            continue
        seen.add(line)
        lines.append(line)
    return lines if limit is None else lines[:limit]


def _report_args(
    *,
    tz: str | None,
    date_text: str | None,
    team: str | None,
    lang: str,
    zh_locale: str | None = None,
    detail_level: str = "full",
) -> argparse.Namespace:
    return argparse.Namespace(
        tz=tz,
        date=date_text,
        team=team,
        view="game" if team else "day",
        lang=lang,
        zh_locale=zh_locale,
        detail_level=detail_level,
        format="json",
        base_url=None,
    )


def build_scene_report(
    *,
    tz: str | None,
    date_text: str | None,
    team: str | None,
    lang: str,
    zh_locale: str | None = None,
    detail_level: str = "full",
) -> dict[str, Any]:
    return build_report_payload(
        _report_args(
            tz=tz,
            date_text=date_text,
            team=team,
            lang=lang,
            zh_locale=zh_locale,
            detail_level=detail_level,
        )
    )


def _target_date(date_text: str | None, tz: str | None) -> datetime.date:
    if date_text:
        return datetime.strptime(date_text, "%Y-%m-%d").date()
    return _reference_now(tz).date()


def _event_local_date(event: dict[str, Any], tz: str | None) -> datetime.date | None:
    resolved_tz = resolve_timezone(tz)
    competition = (event.get("competitions") or [{}])[0]
    raw_date = competition.get("date") or event.get("date")
    if not raw_date:
        return None
    return datetime.fromisoformat(str(raw_date).replace("Z", "+00:00")).astimezone(resolved_tz.tzinfo).date()


def _event_abbrs(event: dict[str, Any]) -> set[str]:
    competition = (event.get("competitions") or [{}])[0]
    competitors = competition.get("competitors") or []
    abbrs = {
        canonicalize_team_abbr(str(((item.get("team") or {}).get("abbreviation")) or "").upper())
        for item in competitors
    }
    short_name = str(event.get("shortName") or "")
    for abbr in extract_teams_from_text(short_name):
        abbrs.add(abbr)
    return {abbr for abbr in abbrs if abbr}


def _event_matches(event: dict[str, Any], team_abbr: str, opponent_abbr: str | None = None) -> bool:
    abbrs = _event_abbrs(event)
    if team_abbr not in abbrs:
        return False
    if opponent_abbr and opponent_abbr not in abbrs:
        return False
    return True


def resolve_requested_game(
    *,
    tz: str | None,
    date_text: str | None,
    team: str,
    opponent: str | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    team_abbr = normalize_team_input(team)
    opponent_abbr = normalize_team_input(opponent) if opponent else None
    if not team_abbr:
        raise NBAReportError("未能识别球队缩写。", kind="invalid_arguments")
    if date_text:
        target_date = _target_date(date_text, tz)
        for event in load_candidate_events(target_date, resolve_timezone(tz), base_url):
            if _event_matches(event, team_abbr, opponent_abbr):
                return {
                    "eventId": str(event.get("id") or ""),
                    "source": "espn_scoreboard",
                    "event": event,
                    "requestedDate": target_date.isoformat(),
                }
        raise NBAReportError("当前条件下未找到对应比赛。", kind="not_found")

    if opponent_abbr:
        espn_team_id = provider_team_id(team_abbr, "espn")
        schedule_payload = {}
        if espn_team_id:
            try:
                schedule_payload = fetch_team_schedule(espn_team_id, base_url=base_url)["data"]
            except NBAReportError:
                schedule_payload = {}
        events = [event for event in (schedule_payload.get("events") or []) if _event_matches(event, team_abbr, opponent_abbr)]
        today = _target_date(None, tz)
        future_events = [
            event for event in events if (_event_local_date(event, tz) is not None and _event_local_date(event, tz) >= today)
        ]
        candidate_pool = sorted(future_events, key=lambda item: str(item.get("date") or ""))
        source = "espn_team_schedule"
        if not candidate_pool:
            candidate_pool = sorted(events, key=lambda item: str(item.get("date") or ""), reverse=True)
        if candidate_pool:
            event = candidate_pool[0]
            local_date = _event_local_date(event, tz)
            return {
                "eventId": str(event.get("id") or ""),
                "source": source,
                "event": event,
                "requestedDate": local_date.isoformat() if local_date else None,
            }
    located = locate_game(tz=tz, date_text=date_text, team=team_abbr, base_url=base_url)
    located["requestedDate"] = _target_date(date_text, tz).isoformat()
    return located


def locate_game(*, tz: str | None, date_text: str | None, team: str, base_url: str | None = None) -> dict[str, Any]:
    team_abbr = normalize_team_input(team)
    if not team_abbr:
        raise NBAReportError("未能识别球队缩写。", kind="invalid_arguments")

    target_date = _target_date(date_text, tz)
    resolved_tz = resolve_timezone(tz)
    for offset in (-1, 0, 1):
        provider_date = (target_date + timedelta(days=offset)).strftime("%Y%m%d")
        try:
            payload = fetch_scoreboard(provider_date, base_url=base_url)["data"]
        except NBAReportError:
            payload = {}
        for event in payload.get("events") or []:
            competition = (event.get("competitions") or [{}])[0]
            event_date = competition.get("date") or event.get("date")
            if not event_date:
                continue
            local_date = datetime.fromisoformat(event_date.replace("Z", "+00:00")).astimezone(resolved_tz.tzinfo).date()
            if local_date != target_date:
                continue
            competitors = competition.get("competitors") or []
            abbrs = {
                canonicalize_team_abbr(str(((item.get("team") or {}).get("abbreviation")) or "").upper())
                for item in competitors
            }
            if team_abbr in abbrs:
                return {
                    "eventId": str(event.get("id") or ""),
                    "source": "espn_scoreboard",
                    "event": event,
                }

    espn_team_id = provider_team_id(team_abbr, "espn")
    if espn_team_id:
        try:
            schedule_payload = fetch_team_schedule(espn_team_id, base_url=base_url)["data"]
            for event in schedule_payload.get("events") or []:
                raw_date = str(event.get("date") or "")
                if raw_date:
                    local_date = datetime.fromisoformat(raw_date.replace("Z", "+00:00")).astimezone(resolved_tz.tzinfo).date()
                    if local_date == target_date:
                        return {
                            "eventId": str(event.get("id") or ""),
                            "source": "espn_team_schedule",
                            "event": event,
                        }
        except NBAReportError:
            pass

    try:
        nba_payload = fetch_nba_scoreboard(target_date.isoformat())["data"]
        for game in extract_scoreboard_games(nba_payload):
            if team_abbr in {game.get("awayAbbr"), game.get("homeAbbr")}:
                return {
                    "eventId": str(game.get("gameId") or ""),
                    "source": "nba_scoreboard",
                    "event": game,
                }
    except NBAReportError:
        pass

    raise NBAReportError("当前条件下未找到对应比赛。", kind="not_found")


def infer_matchup_from_players(
    *,
    tz: str | None,
    date_text: str | None,
    player_names: list[str],
    base_url: str | None = None,
) -> dict[str, str | None]:
    if not player_names:
        return {"team": None, "opponent": None}
    target_date = _target_date(date_text, tz)
    resolved_tz = resolve_timezone(tz)
    events = load_candidate_events(target_date, resolved_tz, base_url)
    roster_cache: dict[str, set[str]] = {}
    primary_team: str | None = None
    player_teams: dict[str, str] = {}

    for event in events:
        if _event_local_date(event, tz) != target_date:
            continue
        competition = (event.get("competitions") or [{}])[0]
        competitors = competition.get("competitors") or []
        event_teams: list[str] = []
        for competitor in competitors:
            abbr = canonicalize_team_abbr(str(((competitor.get("team") or {}).get("abbreviation")) or "").upper())
            if not abbr:
                continue
            event_teams.append(abbr)
            if abbr not in roster_cache:
                snapshot = fetch_team_roster_snapshot(abbr)
                roster_cache[abbr] = roster_names(snapshot.get("players") or [])
        for player_name in player_names:
            identity = normalize_player_identity(player_name)
            if not identity or player_name in player_teams:
                continue
            for abbr in event_teams:
                if identity in roster_cache.get(abbr, set()):
                    player_teams[player_name] = abbr
                    if primary_team is None:
                        primary_team = abbr
                    break

    if not player_teams:
        return {"team": None, "opponent": None}

    ordered_teams = [player_teams[player_name] for player_name in player_names if player_name in player_teams]
    primary_team = ordered_teams[0] if ordered_teams else primary_team
    if not primary_team:
        return {"team": None, "opponent": None}

    for event in events:
        if _event_local_date(event, tz) != target_date:
            continue
        competition = (event.get("competitions") or [{}])[0]
        competitors = competition.get("competitors") or []
        abbrs = [
            canonicalize_team_abbr(str(((competitor.get("team") or {}).get("abbreviation")) or "").upper())
            for competitor in competitors
        ]
        abbrs = [abbr for abbr in abbrs if abbr]
        if primary_team not in abbrs:
            continue
        opponent_team = next((team for team in ordered_teams[1:] if team in abbrs and team != primary_team), None)
        if opponent_team is None and len(abbrs) == 2:
            opponent_team = abbrs[0] if abbrs[1] == primary_team else abbrs[1]
        return {"team": primary_team, "opponent": opponent_team}
    return {"team": primary_team, "opponent": None}


def fetch_team_roster_snapshot(team_abbr: str) -> dict[str, Any]:
    espn_team_id = provider_team_id(team_abbr, "espn")
    nba_team_id = provider_team_id(team_abbr, "nba")
    if espn_team_id:
        try:
            payload = fetch_team_roster(espn_team_id)
            players = extract_espn_roster_players(payload["data"])
            if players:
                return {
                    "team": team_abbr,
                    "players": players,
                    "source": "espn",
                    "dataFreshness": payload.get("dataFreshness", "fresh"),
                }
        except NBAReportError:
            pass
    if nba_team_id:
        try:
            payload = fetch_nba_team_roster(nba_team_id)
            players = extract_nba_roster_players(payload["data"])
            return {
                "team": team_abbr,
                "players": players,
                "source": "nba",
                "dataFreshness": payload.get("dataFreshness", "fresh"),
            }
        except NBAReportError:
            pass
    return {
        "team": team_abbr,
        "players": [],
        "source": "unavailable",
        "dataFreshness": "fresh",
    }


def fetch_game_rosters(game: dict[str, Any]) -> dict[str, dict[str, Any]]:
    roster_snapshots: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_map = {
            executor.submit(fetch_team_roster_snapshot, game["away"]["abbr"]): game["away"]["abbr"],
            executor.submit(fetch_team_roster_snapshot, game["home"]["abbr"]): game["home"]["abbr"],
        }
        for future in as_completed(future_map):
            roster_snapshots[future_map[future]] = future.result()
    return roster_snapshots


def apply_roster_guard(game: dict[str, Any], roster_snapshots: dict[str, dict[str, Any]], *, lang: str) -> dict[str, Any]:
    rosters_by_abbr = {abbr: snapshot.get("players") or [] for abbr, snapshot in roster_snapshots.items()}
    allowed_names_by_team = verified_player_names_by_team(game, rosters_by_abbr)
    allowed_names = verified_player_names(game, rosters_by_abbr)
    blocked: set[str] = set()
    original_candidate_lines_by_team: dict[str, list[str]] = {}
    for group in (game.get("leaders") or {}, game.get("starters") or {}, game.get("keyPlayers") or {}):
        for abbr, lines in group.items():
            original_candidate_lines_by_team.setdefault(str(abbr), []).extend(lines or [])
    for abbr, candidate_lines in original_candidate_lines_by_team.items():
        blocked.update(blocked_names(candidate_lines, allowed_names_by_team.get(str(abbr), set())))

    game["leaders"] = {
        abbr: filter_named_lines(lines or [], allowed_names_by_team.get(str(abbr), set()))
        for abbr, lines in (game.get("leaders") or {}).items()
    }
    game["starters"] = {
        abbr: filter_named_lines(lines or [], allowed_names_by_team.get(str(abbr), set()))
        for abbr, lines in (game.get("starters") or {}).items()
    }
    game["keyPlayers"] = {
        abbr: filter_named_lines(lines or [], allowed_names_by_team.get(str(abbr), set()))
        for abbr, lines in (game.get("keyPlayers") or {}).items()
    }
    game["headlines"] = filter_headlines(game.get("headlines") or [], blocked)
    if game.get("playTimeline"):
        team_id_to_abbr = {
            str((game.get(side) or {}).get("id") or ""): str((game.get(side) or {}).get("abbr") or "")
            for side in ("away", "home")
            if (game.get(side) or {}).get("id") and (game.get(side) or {}).get("abbr")
        }
        filtered_timeline: list[dict[str, Any]] = []
        for play in game.get("playTimeline") or []:
            player_name = play.get("playerName")
            if not player_name:
                filtered_timeline.append(play)
                continue
            team_abbr = team_id_to_abbr.get(str(play.get("teamId") or ""))
            team_allowed_names = allowed_names_by_team.get(team_abbr or "", set()) or allowed_names
            if team_allowed_names and normalize_player_identity(player_name) not in team_allowed_names:
                continue
            filtered_timeline.append(play)
        game["playTimeline"] = filtered_timeline
        game["recentPlays"] = [item.get("text") or "" for item in filtered_timeline[-4:] if item.get("text")]
    if allowed_names:
        filtered_injury_items: dict[str, list[dict[str, Any]]] = {}
        filtered_injuries: dict[str, list[str]] = {}
        for abbr, items in (game.get("injuryItems") or {}).items():
            kept_items: list[dict[str, Any]] = []
            team_allowed_names = allowed_names_by_team.get(str(abbr), set()) or allowed_names
            for item in items or []:
                player_name = extract_primary_name(str(item.get("playerName") or ""))
                if player_name and normalize_player_identity(player_name) in team_allowed_names:
                    kept_items.append(item)
            filtered_injury_items[abbr] = kept_items
            filtered_injuries[abbr] = [_format_injury_item(item) for item in kept_items if _format_injury_item(item)]
        game["injuryItems"] = filtered_injury_items
        game["injuries"] = filtered_injuries
    game["startersConfirmed"] = bool(game["starters"].get(game["away"]["abbr"])) and bool(game["starters"].get(game["home"]["abbr"]))
    game["verifiedPlayers"] = sorted(allowed_names)
    game["verifiedPlayersByTeam"] = {abbr: sorted(names) for abbr, names in allowed_names_by_team.items()}
    game["rosters"] = roster_snapshots
    if blocked:
        game["forceFallbackMatchup"] = True
    game["fallbackMatchup"] = fallback_matchup_text(game, lang=lang)
    return game


def _player_line_from_boxscore(player: dict[str, Any]) -> str:
    name = player.get("displayName") or ""
    stats = player.get("stats") or {}
    parts = [name]
    if stats.get("points") is not None:
        parts.append(f"{stats['points']} PTS")
    if stats.get("rebounds") is not None:
        parts.append(f"{stats['rebounds']} REB")
    if stats.get("assists") is not None:
        parts.append(f"{stats['assists']} AST")
    return " | ".join(str(part) for part in parts if part)


def _sync_live_scoreboard(
    game: dict[str, Any],
    *,
    away_score: Any = None,
    home_score: Any = None,
    period: Any = None,
    display_clock: Any = None,
) -> None:
    if away_score not in (None, ""):
        game["away"]["score"] = str(away_score)
    if home_score not in (None, ""):
        game["home"]["score"] = str(home_score)
    if period not in (None, ""):
        game["period"] = period
    if display_clock not in (None, ""):
        game["displayClock"] = str(display_clock)


def _sync_full_stats_scoreboard(game: dict[str, Any]) -> None:
    if game.get("statusState") not in {"in", "post"}:
        return
    full_stats = game.get("fullStats") or {}
    teams = full_stats.get("teams") or {}
    for side in ("away", "home"):
        team = game.get(side) or {}
        abbr = team.get("abbr")
        score = team.get("score")
        if not abbr or score in (None, ""):
            continue
        stats = teams.get(abbr)
        if isinstance(stats, dict) and stats.get("PTS") in (None, ""):
            stats["PTS"] = str(score)


def augment_game_with_nba_live(game: dict[str, Any], *, requested_date: str) -> dict[str, Any]:
    try:
        game_id = find_game_id_by_matchup(requested_date, game["away"]["abbr"], game["home"]["abbr"])
    except NBAReportError:
        return {"source": None, "dataFreshness": "fresh", "fallbackLevel": "none"}
    if not game_id:
        return {"source": None, "dataFreshness": "fresh", "fallbackLevel": "none"}
    game["nbaGameId"] = str(game_id)
    meta = {"source": None, "dataFreshness": "fresh", "fallbackLevel": "none"}
    should_refresh_live_timeline = game.get("statusState") == "in" or not game.get("playTimeline")
    if should_refresh_live_timeline:
        try:
            payload = fetch_play_by_play(game_id)
            actions = extract_play_actions(payload["data"])
            if actions:
                game["playTimeline"] = [
                    {
                        "id": str(item.get("actionNumber") or ""),
                        "text": item.get("description") or "",
                        "shortDescription": item.get("description") or "",
                        "period": item.get("period"),
                        "clock": item.get("clock"),
                        "homeScore": item.get("homeScore"),
                        "awayScore": item.get("awayScore"),
                        "scoreValue": None,
                        "scoringPlay": True if item.get("homeScore") or item.get("awayScore") else False,
                        "teamId": item.get("teamId") or "",
                        "playerName": item.get("playerName") or "",
                    }
                    for item in actions
                ]
                game["recentPlays"] = [item["text"] for item in game["playTimeline"][-4:] if item.get("text")]
                latest_with_score = next(
                    (
                        item
                        for item in reversed(actions)
                        if item.get("homeScore") not in (None, "") or item.get("awayScore") not in (None, "")
                    ),
                    actions[-1],
                )
                _sync_live_scoreboard(
                    game,
                    away_score=latest_with_score.get("awayScore"),
                    home_score=latest_with_score.get("homeScore"),
                    period=latest_with_score.get("period"),
                    display_clock=latest_with_score.get("clock"),
                )
                meta = {"source": "nba_live", "dataFreshness": payload.get("dataFreshness", "fresh"), "fallbackLevel": "nba_live"}
        except NBAReportError:
            pass
    should_refresh_live_boxscore = (
        game.get("statusState") == "in"
        or not any((game.get("keyPlayers") or {}).values())
        or not any((game.get("starters") or {}).values())
        or game["away"].get("score") in (None, "")
        or game["home"].get("score") in (None, "")
    )
    if should_refresh_live_boxscore:
        try:
            payload = fetch_live_boxscore(game_id)
            game["nbaLiveBoxscore"] = payload["data"]
            live_snapshot = extract_live_boxscore_snapshot(payload["data"])
            away_score = live_snapshot.get("awayScore")
            home_score = live_snapshot.get("homeScore")
            away_score_source = live_snapshot.get("awayScoreSource")
            home_score_source = live_snapshot.get("homeScoreSource")
            _sync_live_scoreboard(
                game,
                away_score=away_score if away_score_source == "explicit" or game["away"].get("score") in (None, "") else None,
                home_score=home_score if home_score_source == "explicit" or game["home"].get("score") in (None, "") else None,
                period=live_snapshot.get("period"),
                display_clock=live_snapshot.get("displayClock"),
            )
            players_by_team = extract_boxscore_players(payload["data"])
            game["boxscorePlayersByTeam"] = players_by_team
            active_participants: list[str] = []
            active_participants_by_team: dict[str, list[str]] = {}
            for abbr, players in players_by_team.items():
                starters = [player["displayName"] for player in players if player.get("starter")]
                if starters:
                    game["starters"][abbr] = starters[:5]
                ordered_players = sorted(
                    players,
                    key=lambda player: (
                        -(float((player.get("stats") or {}).get("points") or 0)),
                        -(float((player.get("stats") or {}).get("rebounds") or 0)),
                        -(float((player.get("stats") or {}).get("assists") or 0)),
                        0 if player.get("starter") else 1,
                    ),
                )
                lines = [_player_line_from_boxscore(player) for player in ordered_players]
                if lines:
                    game["keyPlayers"][abbr] = [line for line in lines if line][:5]
                # 收集实际上场球员（有 minutes 记录的）
                team_active: list[str] = []
                for player in players:
                    minutes_val = (player.get("stats") or {}).get("minutes")
                    has_minutes = False
                    if minutes_val:
                        # minutesCalculated 格式可能是 "PT12M34.00S" 或数字
                        if isinstance(minutes_val, str):
                            has_minutes = minutes_val not in ("", "PT00M00.00S", "PT0M0.00S")
                        else:
                            has_minutes = float(minutes_val) > 0
                    if has_minutes and player.get("displayName"):
                        active_participants.append(player["displayName"])
                        team_active.append(player["displayName"])
                active_participants_by_team[abbr] = team_active
            # live boxscore 补充后重新计算 startersConfirmed
            if bool(game["starters"].get(game["away"]["abbr"])) and bool(game["starters"].get(game["home"]["abbr"])):
                game["startersConfirmed"] = True
            game["activeParticipants"] = active_participants
            game["activeParticipantsByTeam"] = active_participants_by_team
            meta = {"source": "nba_live", "dataFreshness": payload.get("dataFreshness", "fresh"), "fallbackLevel": "nba_live"}
        except NBAReportError:
            pass
    return meta


def _team_player_averages(team_abbr: str) -> dict[str, dict[str, float | None]]:
    nba_team_id = provider_team_id(team_abbr, "nba")
    if not nba_team_id:
        return {}
    timeout_seconds = _bounded_multi_timeout(8)
    if timeout_seconds <= 0:
        return {}
    try:
        payload = fetch_team_player_averages(nba_team_id, timeout_seconds=timeout_seconds)["data"]
    except NBAReportError:
        return {}
    return extract_team_player_averages(payload)


def _team_player_averages_for_game(game: dict[str, Any]) -> dict[str, dict[str, dict[str, float | None]]]:
    averages_by_team: dict[str, dict[str, dict[str, float | None]]] = {}
    team_abbrs = [game["away"]["abbr"], game["home"]["abbr"]]
    max_workers = min(len(team_abbrs), 2)
    if max_workers <= 1:
        for abbr in team_abbrs:
            averages_by_team[abbr] = _team_player_averages(abbr)
        return averages_by_team
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {executor.submit(_team_player_averages, abbr): abbr for abbr in team_abbrs}
        for future in as_completed(future_map):
            averages_by_team[future_map[future]] = future.result()
    return averages_by_team


def attach_season_averages(
    game: dict[str, Any],
    *,
    team_averages: dict[str, dict[str, dict[str, float | None]]] | None = None,
) -> None:
    full_stats = game.get("fullStats") or {}
    if not full_stats.get("available"):
        return
    players_by_team = full_stats.get("players") or {}
    averages_by_team = team_averages if team_averages is not None else game.get("teamPlayerAverages")
    if averages_by_team is None:
        averages_by_team = _team_player_averages_for_game(game)
        game["teamPlayerAverages"] = averages_by_team
    for abbr in (game["away"]["abbr"], game["home"]["abbr"]):
        averages = averages_by_team.get(abbr) or {}
        if not averages:
            continue
        normalized_lookup = {name.casefold(): stats for name, stats in averages.items()}
        for player in players_by_team.get(abbr) or []:
            name = str(player.get("playerName") or "").strip()
            if not name:
                continue
            average_stats = normalized_lookup.get(name.casefold())
            if average_stats:
                player["seasonAverages"] = average_stats


def _collect_context_candidate_names(game: dict[str, Any], team_abbr: str) -> list[str]:
    candidates: list[str] = []
    for group_name in ("leaders", "keyPlayers", "starters"):
        for line in (game.get(group_name, {}).get(team_abbr) or []):
            name = extract_primary_name(line)
            if name and name not in candidates:
                candidates.append(name)
    return candidates[:6]


def build_season_averages_context(
    game: dict[str, Any],
    *,
    team_averages: dict[str, dict[str, dict[str, float | None]]] | None = None,
) -> dict[str, dict[str, Any]]:
    by_team: dict[str, dict[str, Any]] = {}
    averages_by_team = team_averages if team_averages is not None else game.get("teamPlayerAverages")
    if averages_by_team is None:
        averages_by_team = _team_player_averages_for_game(game)
        game["teamPlayerAverages"] = averages_by_team
    for abbr in (game["away"]["abbr"], game["home"]["abbr"]):
        averages = averages_by_team.get(abbr) or {}
        players: dict[str, Any] = {}
        for name in _collect_context_candidate_names(game, abbr):
            stats = averages.get(name)
            if stats:
                players[name] = stats
        by_team[abbr] = players
    return by_team


def build_game_context(game: dict[str, Any]) -> dict[str, Any]:
    info = {
        "eventId": game["eventId"],
        "matchup": {
            "text": f"{game['away']['abbr']} @ {game['home']['abbr']}",
            "away": game["away"],
            "home": game["home"],
        },
        "requestedDate": game.get("requestedDate"),
        "statusState": game.get("statusState"),
        "statusDetail": game.get("statusDetail"),
        "startTimeLocal": game.get("startTimeLocal"),
        "venue": game.get("venue"),
        "broadcasts": game.get("broadcasts") or [],
        "standings": {
            game["away"]["abbr"]: (game.get("context", {}).get("teamForm", {}).get(game["away"]["abbr"], {}).get("standings") or {}),
            game["home"]["abbr"]: (game.get("context", {}).get("teamForm", {}).get(game["home"]["abbr"], {}).get("standings") or {}),
        },
    }
    lineups = {
        "startersConfirmed": bool(game.get("startersConfirmed")),
        "starters": game.get("starters") or {},
        "keyPlayers": game.get("keyPlayers") or {},
        "leaders": game.get("leaders") or {},
        "verifiedPlayers": game.get("verifiedPlayers") or [],
        "activeParticipants": game.get("activeParticipants") or [],
    }
    injuries = {
        "items": game.get("injuryItems") or {},
        "byTeam": game.get("injuries") or {},
        "meta": game.get("injuryMeta") or {},
    }
    live_state = {
        "displayClock": game.get("displayClock"),
        "period": game.get("period"),
        "recentPlays": game.get("recentPlays") or [],
        "playTimeline": game.get("playTimeline") or [],
        "winProbabilityTimeline": game.get("winProbabilityTimeline") or [],
    }
    return {
        "info": info,
        "lineups": lineups,
        "injuries": injuries,
        "teamForm": (game.get("context") or {}).get("teamForm") or {},
        "headToHead": (game.get("context") or {}).get("headToHead") or {},
        "seasonAverages": build_season_averages_context(game),
        "liveState": live_state,
        "fullStats": game.get("fullStats") or {"available": False, "teams": {}, "players": {}},
        "officialStory": game.get("officialStory") or {},
    }


def attach_official_story(game: dict[str, Any], *, requested_date: str | None) -> None:
    if game.get("officialStory"):
        return
    remaining_budget = _remaining_pregame_multi_budget()
    if remaining_budget is not None and remaining_budget <= 0:
        game["officialStory"] = unavailable_game_story("budget_exhausted")
        return
    game_id = str(game.get("nbaGameId") or "").strip()
    if not game_id and requested_date:
        date_candidates = [requested_date]
        try:
            base_date = datetime.strptime(requested_date, "%Y-%m-%d").date()
            for offset in (-1, 1):
                candidate = (base_date + timedelta(days=offset)).isoformat()
                if candidate not in date_candidates:
                    date_candidates.append(candidate)
        except ValueError:
            pass
        for candidate_date in date_candidates:
            schedule_timeout = _bounded_multi_timeout(6)
            if schedule_timeout <= 0:
                break
            try:
                game_id = find_game_id_by_schedule(candidate_date, game["away"]["abbr"], game["home"]["abbr"], timeout_seconds=schedule_timeout) or ""
            except NBAReportError:
                game_id = ""
            if not game_id:
                scoreboard_timeout = _bounded_multi_timeout(4)
                if scoreboard_timeout <= 0:
                    break
                try:
                    game_id = find_game_id_by_matchup(candidate_date, game["away"]["abbr"], game["home"]["abbr"], timeout_seconds=scoreboard_timeout) or ""
                except NBAReportError:
                    game_id = ""
            if game_id:
                break
    if game_id:
        game["nbaGameId"] = game_id
        story_timeout = _bounded_multi_timeout(4)
        if story_timeout <= 0:
            game["officialStory"] = unavailable_game_story("budget_exhausted")
            game["storyAiContextRaw"] = _build_day_story_ai_context(game, game["officialStory"], phase="unknown")
            return
        story = fetch_nba_game_story(game_id, game["away"]["abbr"], game["home"]["abbr"], timeout_seconds=story_timeout)
        game["storyAiContextRaw"] = _build_day_story_ai_context(game, story, phase="unknown")
        game["officialStory"] = public_game_story_payload(story)
    else:
        game["officialStory"] = public_game_story_payload(None)
        game["storyAiContextRaw"] = _build_day_story_ai_context(game, game["officialStory"], phase="unknown")


def build_pregame_view(game: dict[str, Any], analysis: dict[str, Any]) -> dict[str, Any]:
    featured_injuries = {
        game["away"]["abbr"]: _select_pregame_injury_lines(game, game["away"]["abbr"]),
        game["home"]["abbr"]: _select_pregame_injury_lines(game, game["home"]["abbr"]),
    }
    compact_injuries = {
        game["away"]["abbr"]: _select_pregame_injury_lines(game, game["away"]["abbr"], limit=2),
        game["home"]["abbr"]: _select_pregame_injury_lines(game, game["home"]["abbr"], limit=2),
    }
    return {
        "info": game.get("gameContext", {}).get("info") or {},
        "lineups": game.get("gameContext", {}).get("lineups") or {},
        "injuries": {
            **(game.get("gameContext", {}).get("injuries") or {}),
            "featuredByTeam": featured_injuries,
            "compactByTeam": compact_injuries,
        },
        "teamForm": game.get("gameContext", {}).get("teamForm") or {},
        "prediction": {
            "summary": analysis.get("summary") or "",
            "reasons": analysis.get("reasons") or [],
            "trend": analysis.get("trend") or "",
            "keyMatchup": analysis.get("keyMatchup") or "",
        },
        "summary": analysis.get("summary") or "",
    }


def build_live_view(game: dict[str, Any], analysis: dict[str, Any]) -> dict[str, Any]:
    game_context = game.get("gameContext", {}) or {}
    lineups = game_context.get("lineups") or {}
    full_stats = game_context.get("fullStats") or {"available": False, "teams": {}, "players": {}}
    matchup = (game_context.get("info") or {}).get("matchup") or {}
    selected_players, coverage = _build_live_player_display(full_stats=full_stats, lineups=lineups, matchup=matchup, limit=5)
    return {
        "info": game_context.get("info") or {},
        "lineups": _lineups_with_live_player_display(lineups, selected_players),
        "injuries": game_context.get("injuries") or {},
        "liveState": game_context.get("liveState") or {},
        "momentum": {
            "trend": analysis.get("trend") or "",
            "reasons": analysis.get("reasons") or [],
        },
        "playerStatsCoverage": coverage,
        "summary": analysis.get("summary") or "",
    }


def build_postgame_view(game: dict[str, Any], analysis: dict[str, Any]) -> dict[str, Any]:
    return {
        "info": game.get("gameContext", {}).get("info") or {},
        "lineups": game.get("gameContext", {}).get("lineups") or {},
        "injuries": game.get("gameContext", {}).get("injuries") or {},
        "fullStats": game.get("gameContext", {}).get("fullStats") or {"available": False, "teams": {}, "players": {}},
        "turningPoint": analysis.get("turningPoint") or "",
        "summary": analysis.get("summary") or "",
    }


def _phase_labels(lang: str) -> dict[str, str]:
    if lang == "zh":
        return {
            "live_title": "NBA 单场实时走势",
            "post_title": "NBA 单场赛后复盘",
            "info": "比赛信息",
            "lineups": "阵容与关键球员",
            "starters_section": "首发名单",
            "injuries": "伤病情况",
            "live_flow": "实时走势",
            "post_flow": "比赛结果与走势总结",
            "team_totals": "球队整体数据对比",
            "post_team_totals": "球队整体对比",
            "key_player_lines": "关键球员数据",
            "post_key_players": "关键球员表现",
            "play_digest": "回合摘要",
            "turning_point": "转折点",
            "summary": "总结",
            "starters_pending": "首发尚未公布或当前免费数据源不可确认。",
            "none": "无",
        }
    return {
        "live_title": "NBA Live Game Report",
        "post_title": "NBA Postgame Recap",
        "info": "Game Info",
        "lineups": "Lineups and Key Players",
        "starters_section": "Starting Lineups",
        "injuries": "Injuries",
        "live_flow": "Live Momentum",
        "post_flow": "Game Result and Flow",
        "team_totals": "Team Totals Comparison",
        "post_team_totals": "Team Comparison",
        "key_player_lines": "Key Player Lines",
        "post_key_players": "Key Performances",
        "play_digest": "Play Digest",
        "turning_point": "Turning Point",
        "summary": "Summary",
        "starters_pending": "Starting lineups are not yet confirmed or cannot be confirmed from the free data source.",
        "none": "None",
    }


def _day_labels(lang: str) -> dict[str, str]:
    if lang == "zh":
        return {
            "title": "NBA 综合赛况",
            "view": "综合赛况视图",
            "live_title": "进行中比赛",
            "post_title": "已结束比赛",
            "pre_title": "未开赛比赛",
            "counts": "场次摘要",
            "phase_pregame": "赛前",
            "phase_live": "赛中",
            "phase_post": "赛后",
            "team_form": "球队状态",
            "prediction": "预测摘要",
            "latest_play": "最新回合",
            "turning_point": "转折点",
            "none": "无",
        }
    return {
        "title": "NBA Mixed Status Day View",
        "view": "mixed-status day view",
        "live_title": "Live Games",
        "post_title": "Final Games",
        "pre_title": "Scheduled Games",
        "counts": "Counts",
        "phase_pregame": "Pregame",
        "phase_live": "Live",
        "phase_post": "Postgame",
        "team_form": "Team Form",
        "prediction": "Prediction",
        "latest_play": "Latest Play",
        "turning_point": "Turning Point",
        "none": "None",
    }


def _stats_day_labels(lang: str) -> dict[str, str]:
    if lang == "zh":
        return {
            "title": "NBA 今日统计",
            "view": "当日统计视图",
            "completed_games": "已统计比赛",
            "best_performance": "今日最佳表现",
            "top_scorer": "最高得分",
            "top_rebounder": "最高篮板",
            "top_assists": "最高助攻",
            "top_three": "最高三分",
            "double_triple": "两双 / 三双",
            "largest_margin": "最大分差",
            "no_completed_games": "当前该日期还没有已结束比赛，暂时无法汇总当日统计。",
            "none": "无",
            "double_double": "两双",
            "triple_double": "三双",
            "summary_prefix": "统计摘要",
            "points": "分",
            "rebounds": "板",
            "assists": "助攻",
            "made_threes": "记三分",
            "won_by": "赢",
        }
    return {
        "title": "NBA Daily Stats",
        "view": "day stats view",
        "completed_games": "Completed Games Counted",
        "best_performance": "Best Performance",
        "top_scorer": "Top Scorer",
        "top_rebounder": "Top Rebounder",
        "top_assists": "Top Assists",
        "top_three": "Top Three-Point Shooter",
        "double_triple": "Double-Doubles / Triple-Doubles",
        "largest_margin": "Largest Margin",
        "no_completed_games": "No completed games are available for day-level stats on the requested date yet.",
        "none": "None",
        "double_double": "double-double",
        "triple_double": "triple-double",
        "summary_prefix": "Summary",
        "points": "PTS",
        "rebounds": "REB",
        "assists": "AST",
        "made_threes": "3PM",
        "won_by": "won by",
    }


def _display_team(abbr: str | None, lang: str, zh_locale: str | None = None) -> str:
    return team_display_name(abbr, lang, zh_locale=zh_locale) or (abbr or "")


def _matchup_team_abbrs(matchup: dict[str, Any] | None) -> list[str]:
    if not matchup:
        return []
    abbrs: list[str] = []
    for side in ("away", "home"):
        abbr = canonicalize_team_abbr((matchup.get(side) or {}).get("abbr"))
        if abbr and abbr not in abbrs:
            abbrs.append(abbr)
    return abbrs


def _localize_team_mentions(
    text: str | None,
    *,
    lang: str,
    zh_locale: str | None = None,
    team_abbrs: list[str] | None = None,
) -> str:
    rendered = str(text or "").strip()
    if not rendered:
        return ""
    for abbr in team_abbrs or []:
        canonical = canonicalize_team_abbr(abbr)
        display = _display_team(canonical, lang, zh_locale)
        if not display:
            continue
        rendered = re.sub(rf"(?<![A-Z]){re.escape(canonical)}(?![A-Z])", display, rendered)
        if canonical == "WAS":
            rendered = re.sub(r"(?<![A-Z])WSH(?![A-Z])", display, rendered)
    return rendered


def _ordinal_period(period: Any) -> str:
    try:
        number = int(period)
    except (TypeError, ValueError):
        return str(period or "?")
    if 10 <= number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
    return f"{number}{suffix}"


def _append_unique_line(lines: list[str], text: str | None) -> None:
    normalized = str(text or "").strip()
    if not normalized:
        return
    candidate = f"- {normalized}"
    if lines and lines[-1] == candidate:
        return
    lines.append(candidate)


def _normalize_comparable_text(text: str | None) -> str:
    value = str(text or "").strip().casefold()
    if not value:
        return ""
    value = re.sub(r"^[\-\s]+", "", value)
    value = re.sub(r"[。．.!！?？]+$", "", value)
    value = re.sub(r"\s+", " ", value)
    return value


def _append_team_player_block(lines: list[str], team_heading: str, player_lines: list[str]) -> bool:
    rendered = [line for line in player_lines if str(line or "").strip()]
    if not rendered:
        return False
    lines.append(f"- {team_heading}:")
    lines.extend([f"  - {line}" for line in rendered])
    return True


def _should_render_provenance(scene: dict[str, Any]) -> bool:
    sources = scene.get("sources") or []
    if sorted(sources) != ["espn"]:
        return True
    if scene.get("fallbackLevel") not in (None, "", "none"):
        return True
    if scene.get("dataFreshness") not in (None, "", "fresh"):
        return True
    return False


def _append_provenance_lines(lines: list[str], scene: dict[str, Any]) -> None:
    if not _should_render_provenance(scene):
        return
    lines.extend(
        [
            f"> sources: {', '.join(scene['sources'])}",
            f"> fallbackLevel: {scene['fallbackLevel']}",
            f"> dataFreshness: {scene['dataFreshness']}",
        ]
    )


def _official_story_available(official_story: dict[str, Any] | None) -> bool:
    story = official_story or {}
    return bool(story.get("available")) and bool(
        story.get("url")
        or story.get("headline")
        or story.get("storyBrief")
        or story.get("storySummary")
        or story.get("summarySignals")
    )


def _card_has_official_report(card: dict[str, Any] | None, game_context: dict[str, Any] | None = None) -> bool:
    card = card or {}
    game_context = game_context or {}
    story_context = card.get("storyAiContext") or {}
    if story_context.get("available"):
        return True
    if _official_story_available(game_context.get("officialStory")):
        return True
    return bool(
        _story_brief_is_substantive(card.get("storyBrief"))
        or card.get("storySummary")
        or card.get("storySignal")
    )


def _official_report_prompt_text(
    *,
    kind: str,
    lang: str,
    requested_date: str,
    timezone: str,
    away_abbr: str | None = None,
    home_abbr: str | None = None,
) -> str:
    date_part = str(requested_date or "").strip()
    tz_part = str(timezone or "").strip()
    matchup_part = " vs ".join(part for part in (away_abbr, home_abbr) if part)
    if lang == "zh":
        suffix = f"，按 {tz_part}" if tz_part else ""
        if kind == "day":
            query = f"{date_part} NBA 官方报道{suffix}" if date_part else f"今天 NBA 官方报道{suffix}"
            return f"官方报道提示：本日部分比赛有 NBA.com 官方报道；如需全文摘要，可问「{query}」。"
        if kind == "pregame_multi":
            query = f"{date_part} NBA 官方报道{suffix}" if date_part else f"明天 NBA 官方报道{suffix}"
            return f"官方报道提示：这些前瞻有 NBA.com 赛前稿；如需逐场文章摘要，可问「{query}」。"
        if kind == "pregame_single":
            query = f"{date_part} {matchup_part} 官方报道{suffix}".strip()
            return f"官方报道提示：这场比赛有 NBA.com 赛前稿；如需全文摘要，可问「{query}」。"
        query_team = home_abbr or away_abbr or matchup_part
        query = f"复盘 {date_part} {query_team} 的官方报道{suffix}".strip()
        return f"官方报道提示：这场比赛有 NBA.com 赛后报道；如需全文摘要，可问「{query}」。"

    suffix = f" in {tz_part}" if tz_part else ""
    if kind == "day":
        query = f"{date_part} NBA official reports{suffix}".strip()
        return f"Official report tip: NBA.com stories are available for part of this slate; ask \"{query}\" for full summaries."
    if kind == "pregame_multi":
        query = f"{date_part} NBA official reports{suffix}".strip()
        return f"Official report tip: NBA.com previews are available for these matchups; ask \"{query}\" for article summaries."
    if kind == "pregame_single":
        query = f"{date_part} {matchup_part} official report{suffix}".strip()
        return f"Official report tip: an NBA.com preview is available for this game; ask \"{query}\" for the full summary."
    query_team = home_abbr or away_abbr or matchup_part
    query = f"recap {date_part} {query_team} official report{suffix}".strip()
    return f"Official report tip: an NBA.com recap is available for this game; ask \"{query}\" for the full summary."


def _official_report_prompt_for_scene(scene: dict[str, Any], *, kind: str) -> str:
    game = scene.get("game") or {}
    story = (game.get("gameContext") or {}).get("officialStory") or game.get("officialStory") or {}
    if not _official_story_available(story):
        return ""
    report = scene.get("report") or {}
    return _official_report_prompt_text(
        kind=kind,
        lang=str(report.get("lang") or "zh"),
        requested_date=str(report.get("requestedDate") or game.get("requestedDate") or ""),
        timezone=str(report.get("timezone") or ""),
        away_abbr=(game.get("away") or {}).get("abbr"),
        home_abbr=(game.get("home") or {}).get("abbr"),
    )


def _append_summary_section_if_needed(
    lines: list[str],
    *,
    title: str,
    summary: str | None,
    none_label: str,
    already_shown: str | None = None,
) -> None:
    rendered = str(summary or none_label).strip()
    if not rendered:
        rendered = none_label
    if already_shown and _normalize_comparable_text(rendered) == _normalize_comparable_text(already_shown):
        return
    lines.extend([f"## {title}", "", f"- {rendered}", ""])


def _filter_player_stats(
    players: list[dict[str, Any]],
    *,
    player_focus: str | None,
) -> list[dict[str, Any]]:
    if not player_focus:
        return players
    focus_identity = normalize_player_identity(player_focus)
    return [
        player
        for player in players
        if normalize_player_identity(str(player.get("playerName") or "")) == focus_identity
    ]


def _narrative_team_form(team_name: str, recent: str, rest_text: str, lang: str) -> str:
    if lang == "zh":
        return f"{team_name}近况是最近 {recent}，休息天数 {rest_text}。"
    rest_phrase = "rest pending" if rest_text == "Pending" else f"{rest_text} day{'s' if str(rest_text) != '1' else ''} of rest"
    return f"{team_name} come in at {recent} over the last five with {rest_phrase}."


def _narrative_team_totals(team_name: str, compact: str, lang: str) -> str:
    if lang == "zh":
        return f"数据层面，{team_name}是 {compact}。"
    return f"On the numbers, {team_name} finished at {compact}."


def _narrative_latest_play(play_text: str, lang: str) -> str:
    if not str(play_text or "").strip():
        return ""
    if lang == "zh":
        return f"最新一次明显波动出现在 {play_text}。"
    return f"The latest swing came on {play_text}."


def _narrative_turning_point(turning_point: str, lang: str) -> str:
    value = str(turning_point or "").strip()
    if not value or value in {"无", "None"}:
        return value or ""
    if lang == "zh" and ("，" in value or "。" in value):
        return value if value.endswith("。") else f"{value}。"
    if lang == "en" and (value.startswith("With ") or value.startswith("In ") or value.startswith("The ") or value.endswith(".")):
        return value if value.endswith(".") else f"{value}."
    if lang == "zh":
        return f"比赛的关键片段出现在 {value}。"
    return f"The key stretch turned on {value}."


def _post_reasons_sentence(reasons: list[str], *, lang: str) -> str:
    cleaned = [str(reason or "").strip().rstrip(".。") for reason in reasons if str(reason or "").strip()]
    if not cleaned:
        return ""
    if lang == "zh":
        return f"支撑这场走势的依据包括：{'；'.join(cleaned)}。"
    return f"The supporting evidence included: {'; '.join(cleaned)}."


def _english_reason_fragment(reason: str) -> str:
    value = str(reason or "").strip().rstrip(".")
    if not value:
        return ""
    won_match = re.match(r"^(?P<team>.+?) won by (?P<margin>\d+)(?: points?)?$", value)
    if won_match:
        team = won_match.group("team").strip()
        margin = won_match.group("margin").strip()
        return f"a {margin}-point win for {team}"
    if value.startswith("Decisive stretch:"):
        detail = value.split(":", 1)[1].strip()
        return f"the decisive stretch in {detail}"
    if value.startswith("Lead performer:"):
        detail = value.split(":", 1)[1].strip().replace(" | ", ", ")
        return f"{detail} setting the tone"
    if value.startswith("Rebounding edge:"):
        detail = value.split(":", 1)[1].strip()
        return f"a rebounding edge of {detail}"
    return value[0].lower() + value[1:] if value[:1].isupper() else value


def _narrative_reasons(reasons: list[str], *, lang: str) -> str:
    if not reasons:
        return ""
    if lang == "zh":
        joined = " / ".join(reasons)
        return f"关键依据主要在于 {joined}。"
    english_reasons = [_english_reason_fragment(reason) for reason in reasons if str(reason or "").strip()]
    joined = "; ".join(fragment for fragment in english_reasons if fragment)
    return f"The edge was backed by {joined}."


def _render_story_signal_text(signal: dict[str, Any] | None, *, lang: str) -> str:
    if not signal:
        return ""
    source = str(signal.get("sourceLabel") or "NBA.com")
    kind = str(signal.get("kind") or "")
    subject = display_player_name(str(signal.get("subject") or ""), lang)
    value = str(signal.get("value") or "").strip()
    if lang == "zh":
        if kind == "standout_scorer" and subject and value:
            return f"报道看点：{source} 把 {subject} 的 {value} 分表现列为比赛主线。"
        if kind == "short_handed":
            return f"报道背景：{source} 提到阵容短缺是这场比赛的重要背景。"
        if kind == "availability":
            return f"报道背景：{source} 提到伤病或球员可用性是关键变量。"
        if kind == "series_context":
            return f"报道背景：{source} 将这场比赛放在系列赛走势里观察。"
        if kind == "previous_matchups":
            return f"报道背景：{source} 提到双方常规赛交手和阵容变化会影响赛前判断。"
        if kind == "efficiency":
            return f"报道看点：{source} 把投篮效率列为比赛的重要解释线索。"
        if kind == "matchup_watch":
            return f"报道看点：{source} 提醒这场对位会受阵容变化和核心轮换影响。"
        return f"报道看点：{source} 提供了这场比赛的背景线索。"
    if kind == "standout_scorer" and subject and value:
        return f"Story note: {source} framed {subject}'s {value}-point performance as a central theme."
    if kind == "short_handed":
        return f"Story note: {source} highlighted the short-handed roster context."
    if kind == "availability":
        return f"Story note: {source} highlighted availability and injury context."
    if kind == "series_context":
        return f"Story note: {source} framed this game through the series context."
    if kind == "previous_matchups":
        return f"Story note: {source} pointed to the regular-season meetings and changed lineups."
    if kind == "efficiency":
        return f"Story note: {source} pointed to shooting efficiency as a key explanation."
    if kind == "matchup_watch":
        return f"Story note: {source} flagged lineup and rotation context for the matchup."
    return f"Story note: {source} added matchup context."


def _append_story_signal_line(lines: list[str], signal: dict[str, Any] | None, *, lang: str) -> None:
    rendered = _render_story_signal_text(signal, lang=lang)
    if rendered:
        _append_unique_line(lines, rendered)


def _story_summary_text(official_story: dict[str, Any] | None, *, phase: str, lang: str) -> str:
    story = official_story or {}
    if not story.get("available"):
        return ""
    summary = (story.get("storySummary") or {}).get(phase) or {}
    if not isinstance(summary, dict):
        return ""
    return str(summary.get(lang) or summary.get("zh" if lang == "en" else "en") or "").strip()


def _story_brief(official_story: dict[str, Any] | None, *, phase: str) -> dict[str, Any]:
    story = official_story or {}
    if not story.get("available"):
        return {}
    brief = story.get("storyBrief") or {}
    if not isinstance(brief, dict):
        return {}
    brief_phase = str(brief.get("phase") or "")
    if brief_phase and brief_phase != "unknown" and brief_phase != phase:
        return {}
    return brief


def _clean_story_ai_paragraphs(story: dict[str, Any] | None, *, limit: int = 16) -> list[str]:
    paragraphs: list[str] = []
    for item in (story or {}).get("content") or []:
        text = re.sub(r"\s+", " ", str(item or "")).strip()
        if not text:
            continue
        paragraphs.append(text)
        if len(paragraphs) >= limit:
            break
    return paragraphs


def _build_day_story_ai_context(game: dict[str, Any], story: dict[str, Any] | None, *, phase: str) -> dict[str, Any]:
    story = story or {}
    paragraphs = _clean_story_ai_paragraphs(story)
    available = bool(story.get("available")) and bool(paragraphs)
    return {
        "available": available,
        "reason": "" if available else str(story.get("reason") or "missing_story_content"),
        "eventId": game.get("eventId") or "",
        "phase": phase,
        "matchup": {
            "away": game["away"]["abbr"],
            "home": game["home"]["abbr"],
            "text": f"{game['away']['abbr']} @ {game['home']['abbr']}",
        },
        "headline": story.get("headline") or "",
        "storyType": story.get("storyType") or "",
        "date": story.get("date") or "",
        "byline": story.get("byline") or story.get("bytitle") or "",
        "sourceLabel": story.get("sourceLabel") or "NBA.com",
        "sourceUrl": story.get("url") or "",
        "paragraphCount": len(paragraphs),
        "cleanedParagraphs": paragraphs,
    }


def _story_ai_context_for_card(game: dict[str, Any], *, phase: str) -> dict[str, Any]:
    context = dict(game.get("storyAiContextRaw") or {})
    if not context:
        context = _build_day_story_ai_context(game, game.get("officialStory"), phase=phase)
    context["phase"] = phase
    return context


def _story_brief_text(official_story: dict[str, Any] | None, *, phase: str, lang: str) -> str:
    brief = _story_brief(official_story, phase=phase)
    if not brief:
        return ""
    key = "compactZh" if lang == "zh" else "compactEn"
    fallback_key = "compactEn" if lang == "zh" else "compactZh"
    return str(brief.get(key) or brief.get(fallback_key) or "").strip()


def _naturalize_embedded_story_text(text: str, *, phase: str, lang: str) -> str:
    value = str(text or "").strip()
    if not value:
        return ""
    if lang == "zh":
        replacements = (
            ("NBA.com 的报道标题提供了这场比赛的基础背景：", ""),
            ("NBA.com 的标题只提供了基础报道背景：", ""),
            ("NBA.com 提到 ", ""),
            ("NBA.com 强调 ", ""),
            ("NBA.com 复盘认为 ", ""),
            ("NBA.com 复盘强调 ", ""),
            ("NBA.com 复盘把 ", ""),
            ("NBA.com 复盘里重点提到了", ""),
            ("NBA.com 把 ", ""),
            ("是官方复盘里的核心个人主线。", "是复盘主线。"),
            ("是官方复盘里的核心个人主线", "是复盘主线"),
            ("是官方报道里的核心个人主线。", "是报道主线。"),
            ("是官方报道里的核心个人主线", "是报道主线"),
            ("这场比赛被放在系列赛首战语境中解读，胜负会影响首轮开局叙事。", "这场比赛仍被放在系列赛首战语境下解读。"),
            ("这场比赛被放在系列赛首战语境中解读，胜负会影响首轮开局叙事", "这场比赛仍被放在系列赛首战语境下解读"),
            ("阵容可用性和轮换变化的影响。", "阵容可用性和轮换变化。"),
        )
        for source, target in replacements:
            value = value.replace(source, target)
        value = re.sub(r"^；+", "", value)
        value = re.sub(r"\s+", " ", value).strip()
        value = re.sub(r"^[，。；:：\s]+", "", value)
        value = re.sub(r"[；]+\s*；", "；", value)
        value = re.sub(r"([。！？])\1+", r"\1", value)
        return value
    replacements_en = (
        ("NBA.com's headline provides the basic story frame: ", ""),
        ("NBA.com's headline only provides a basic story frame: ", ""),
        ("NBA.com highlights that ", ""),
        ("NBA.com highlights ", ""),
        ("NBA.com notes that ", ""),
        ("NBA.com notes ", ""),
        ("NBA.com emphasizes that ", ""),
        ("NBA.com emphasizes ", ""),
        ("NBA.com frames the turning point around ", ""),
        ("NBA.com frames the recap around ", ""),
    )
    for source, target in replacements_en:
        value = value.replace(source, target)
    return re.sub(r"\s+", " ", value).strip()


def _story_brief_is_substantive(brief: dict[str, Any] | None) -> bool:
    if not isinstance(brief, dict) or not brief:
        return False
    themes = {str(theme) for theme in (brief.get("themes") or [])}
    if not themes:
        return False
    return themes != {"headline_fallback"}


def _render_pregame_story_background(official_story: dict[str, Any] | None, *, lang: str) -> str:
    story = official_story or {}
    if not story.get("available"):
        return ""
    brief_text = _story_brief_text(story, phase="pregame", lang=lang)
    if brief_text:
        brief_text = _naturalize_embedded_story_text(brief_text, phase="pregame", lang=lang)
        if lang == "zh":
            return f"官方报道背景：{brief_text}"
        return f"Official story background: {brief_text}"
    summary_text = _story_summary_text(story, phase="pregame", lang=lang)
    if summary_text:
        summary_text = _naturalize_embedded_story_text(summary_text, phase="pregame", lang=lang)
        if lang == "zh":
            return f"官方报道背景：{summary_text}"
        return f"Official story background: {summary_text}"
    signal = _pregame_story_signal(story)
    if signal:
        rendered = _render_story_signal_text(signal, lang=lang)
        if lang == "zh":
            if rendered.startswith("报道看点："):
                return rendered.replace("报道看点：", "官方报道背景：", 1)
            if rendered.startswith("报道背景："):
                return rendered.replace("报道背景：", "官方报道背景：", 1)
            return f"官方报道背景：{rendered}"
        return rendered.replace("Story note:", "Official story background:", 1)
    source = str(story.get("sourceLabel") or "NBA.com")
    if lang == "zh":
        return f"官方报道背景：{source} 赛前稿给这场对决补充了额外背景，但没有形成更明确的主线信号。"
    return f"Official story background: {source} added extra pregame context, even without a clearer lead signal."


def _append_pregame_story_background_line(lines: list[str], official_story: dict[str, Any] | None, *, lang: str) -> None:
    rendered = _render_pregame_story_background(official_story, lang=lang)
    if rendered:
        _append_unique_line(lines, rendered)


def _render_postgame_story_background(official_story: dict[str, Any] | None, *, lang: str) -> str:
    story = official_story or {}
    if not story.get("available"):
        return ""
    brief_text = _story_brief_text(story, phase="post", lang=lang)
    if brief_text:
        brief_text = _naturalize_embedded_story_text(brief_text, phase="post", lang=lang)
        if lang == "zh":
            return f"官方报道复盘：{brief_text}"
        return f"Official recap theme: {brief_text}"
    summary_text = _story_summary_text(story, phase="post", lang=lang)
    if summary_text:
        summary_text = _naturalize_embedded_story_text(summary_text, phase="post", lang=lang)
        if lang == "zh":
            return f"官方报道复盘：{summary_text}"
        return f"Official recap theme: {summary_text}"
    signal = _primary_story_signal(story)
    if signal:
        rendered = _render_story_signal_text(signal, lang=lang)
        if lang == "zh":
            if rendered.startswith("报道看点："):
                return rendered.replace("报道看点：", "官方报道复盘：", 1)
            if rendered.startswith("报道背景："):
                return rendered.replace("报道背景：", "官方报道复盘：", 1)
            return f"官方报道复盘：{rendered}"
        return rendered.replace("Story note:", "Official recap theme:", 1)
    source = str(story.get("sourceLabel") or "NBA.com")
    if lang == "zh":
        return f"官方报道复盘：{source} 对这场比赛补充了额外主线。"
    return f"Official recap theme: {source} adds extra recap context."


def _append_postgame_story_background_line(lines: list[str], official_story: dict[str, Any] | None, *, lang: str) -> None:
    rendered = _render_postgame_story_background(official_story, lang=lang)
    if rendered:
        _append_unique_line(lines, rendered)


LEADER_LINE_PATTERN = re.compile(r"^(?P<name>.+?)\s*\((?P<stats>.+)\)$")
LEADER_STAT_PATTERN = re.compile(r"(?P<value>\d+(?:\.\d+)?)\s*(?P<label>PTS|REB|AST)\b", re.IGNORECASE)


def _numeric_value(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return int(number)


def _three_pt_made(value: Any) -> int | None:
    if value is None or value == "":
        return None
    text = str(value).strip()
    if not text:
        return None
    if "-" in text:
        text = text.split("-", 1)[0]
    return _numeric_value(text)


def _leader_stats_from_line(line: str) -> tuple[str, dict[str, int]]:
    match = LEADER_LINE_PATTERN.match(str(line or "").strip())
    if not match:
        return "", {}
    stats_map: dict[str, int] = {}
    for stat_match in LEADER_STAT_PATTERN.finditer(match.group("stats")):
        key = str(stat_match.group("label") or "").upper()
        value = _numeric_value(stat_match.group("value"))
        if value is not None:
            stats_map[key] = value
    return str(match.group("name") or "").strip(), stats_map


def _format_stat_matchup(entry: dict[str, Any], lang: str, zh_locale: str | None = None) -> str:
    return format_matchup_display(
        str(entry.get("awayAbbr") or ""),
        str(entry.get("homeAbbr") or ""),
        lang=lang,
        zh_locale=zh_locale,
        away_score=entry.get("awayScore"),
        home_score=entry.get("homeScore"),
    )


def _build_stat_entry(
    *,
    player_name: str,
    team_abbr: str,
    away_abbr: str,
    home_abbr: str,
    away_score: Any,
    home_score: Any,
    value: int,
    stat_label: str,
    lang: str,
    zh_locale: str | None,
    source: str,
    extra_stats: dict[str, int] | None = None,
) -> dict[str, Any]:
    return {
        "playerName": player_name,
        "displayName": display_player_name(player_name, lang),
        "teamAbbr": team_abbr,
        "teamName": _display_team(team_abbr, lang, zh_locale),
        "awayAbbr": away_abbr,
        "homeAbbr": home_abbr,
        "awayScore": away_score,
        "homeScore": home_score,
        "matchup": _format_stat_matchup(
            {
                "awayAbbr": away_abbr,
                "homeAbbr": home_abbr,
                "awayScore": away_score,
                "homeScore": home_score,
            },
            lang,
            zh_locale,
        ),
        "value": value,
        "displayValue": f"{value} {stat_label}",
        "source": source,
        "stats": extra_stats or {},
    }


def _update_best_entries(current: list[dict[str, Any]], candidate: dict[str, Any], *, top_n: int = 2) -> list[dict[str, Any]]:
    if not current:
        return [candidate]
    current_value = int(current[0].get("value") or 0)
    candidate_value = int(candidate.get("value") or 0)
    if candidate_value > current_value:
        return [candidate]
    if candidate_value < current_value:
        return current
    merged = current + [candidate]
    return merged[:top_n]


def _double_double_tier(player_stats: dict[str, Any]) -> tuple[str, dict[str, int]] | None:
    categories = {
        "PTS": _numeric_value(player_stats.get("PTS")),
        "REB": _numeric_value(player_stats.get("REB")),
        "AST": _numeric_value(player_stats.get("AST")),
        "STL": _numeric_value(player_stats.get("STL")),
        "BLK": _numeric_value(player_stats.get("BLK")),
    }
    achieved = {key: value for key, value in categories.items() if value is not None and value >= 10}
    if len(achieved) >= 3:
        return "tripleDouble", achieved
    if len(achieved) >= 2:
        return "doubleDouble", achieved
    return None


def _performance_sort_key(entry: dict[str, Any]) -> tuple[int, int]:
    tier = str(entry.get("tier") or "")
    priority = 1 if tier == "tripleDouble" else 0
    return (priority, int(entry.get("value") or 0))


def _stats_block(
    leaders: list[dict[str, Any]],
    *,
    none_text: str,
) -> dict[str, Any]:
    if not leaders:
        return {"value": None, "leaders": [], "summary": none_text}
    top_value = leaders[0].get("value")
    return {
        "value": top_value,
        "leaders": leaders,
        "summary": ", ".join(str(item.get("displayValue") or "") for item in leaders if item.get("displayValue")) or none_text,
    }


def build_day_stats_view(*, tz: str | None, date_text: str | None, lang: str, zh_locale: str | None = None) -> dict[str, Any]:
    day_payload = build_day_view(tz=tz, date_text=date_text, lang=lang, zh_locale=zh_locale, detail_level="full")
    labels = _stats_day_labels(lang)
    completed_games = [game for game in (day_payload.get("games") or []) if game.get("phase") == "post"]
    top_scorer: list[dict[str, Any]] = []
    top_rebounder: list[dict[str, Any]] = []
    top_assists: list[dict[str, Any]] = []
    top_three: list[dict[str, Any]] = []
    double_doubles: list[dict[str, Any]] = []
    triple_doubles: list[dict[str, Any]] = []
    largest_margin_game: dict[str, Any] | None = None

    for entry in completed_games:
        teams = entry.get("teams") or {}
        away_abbr = str((teams.get("away") or {}).get("abbr") or "")
        home_abbr = str((teams.get("home") or {}).get("abbr") or "")
        away_score = (teams.get("away") or {}).get("score")
        home_score = (teams.get("home") or {}).get("score")
        game_context = entry.get("gameContext") or {}
        full_stats = game_context.get("fullStats") or {}
        players_by_team = full_stats.get("players") or {}
        lineups = game_context.get("lineups") or {}

        away_score_value = _numeric_value(away_score)
        home_score_value = _numeric_value(home_score)
        if away_score_value is not None and home_score_value is not None:
            margin = abs(home_score_value - away_score_value)
            if largest_margin_game is None or margin > int(largest_margin_game.get("margin") or 0):
                winner_abbr = home_abbr if home_score_value > away_score_value else away_abbr
                loser_abbr = away_abbr if winner_abbr == home_abbr else home_abbr
                largest_margin_game = {
                    "margin": margin,
                    "winnerAbbr": winner_abbr,
                    "winnerName": _display_team(winner_abbr, lang, zh_locale),
                    "loserAbbr": loser_abbr,
                    "loserName": _display_team(loser_abbr, lang, zh_locale),
                    "awayAbbr": away_abbr,
                    "homeAbbr": home_abbr,
                    "awayScore": away_score,
                    "homeScore": home_score,
                    "matchup": _format_stat_matchup(
                        {
                            "awayAbbr": away_abbr,
                            "homeAbbr": home_abbr,
                            "awayScore": away_score,
                            "homeScore": home_score,
                        },
                        lang,
                        zh_locale,
                    ),
                    "summary": f"{_display_team(winner_abbr, lang, zh_locale)} {labels['won_by']} {margin}",
                }

        for abbr in (away_abbr, home_abbr):
            team_players = list(players_by_team.get(abbr) or [])
            if team_players:
                for player in team_players:
                    name = str(player.get("playerName") or "")
                    if not name:
                        continue
                    player_stats = player.get("stats") or {}
                    points = _numeric_value(player_stats.get("PTS"))
                    rebounds = _numeric_value(player_stats.get("REB"))
                    assists = _numeric_value(player_stats.get("AST"))
                    made_threes = _three_pt_made(player_stats.get("3PT"))
                    extra_stats = {
                        key: value
                        for key, value in {
                            "PTS": points,
                            "REB": rebounds,
                            "AST": assists,
                            "STL": _numeric_value(player_stats.get("STL")),
                            "BLK": _numeric_value(player_stats.get("BLK")),
                        }.items()
                        if value is not None
                    }
                    if points is not None:
                        top_scorer = _update_best_entries(
                            top_scorer,
                            _build_stat_entry(
                                player_name=name,
                                team_abbr=abbr,
                                away_abbr=away_abbr,
                                home_abbr=home_abbr,
                                away_score=away_score,
                                home_score=home_score,
                                value=points,
                                stat_label="PTS",
                                lang=lang,
                                zh_locale=zh_locale,
                                source="fullStats",
                                extra_stats=extra_stats,
                            ),
                        )
                    if rebounds is not None:
                        top_rebounder = _update_best_entries(
                            top_rebounder,
                            _build_stat_entry(
                                player_name=name,
                                team_abbr=abbr,
                                away_abbr=away_abbr,
                                home_abbr=home_abbr,
                                away_score=away_score,
                                home_score=home_score,
                                value=rebounds,
                                stat_label="REB",
                                lang=lang,
                                zh_locale=zh_locale,
                                source="fullStats",
                                extra_stats=extra_stats,
                            ),
                        )
                    if assists is not None:
                        top_assists = _update_best_entries(
                            top_assists,
                            _build_stat_entry(
                                player_name=name,
                                team_abbr=abbr,
                                away_abbr=away_abbr,
                                home_abbr=home_abbr,
                                away_score=away_score,
                                home_score=home_score,
                                value=assists,
                                stat_label="AST",
                                lang=lang,
                                zh_locale=zh_locale,
                                source="fullStats",
                                extra_stats=extra_stats,
                            ),
                        )
                    if made_threes is not None:
                        top_three = _update_best_entries(
                            top_three,
                            _build_stat_entry(
                                player_name=name,
                                team_abbr=abbr,
                                away_abbr=away_abbr,
                                home_abbr=home_abbr,
                                away_score=away_score,
                                home_score=home_score,
                                value=made_threes,
                                stat_label="3PM",
                                lang=lang,
                                zh_locale=zh_locale,
                                source="fullStats",
                                extra_stats=extra_stats,
                            ),
                        )
                    tier = _double_double_tier(player_stats)
                    if tier:
                        tier_name, achieved = tier
                        achievement = _build_stat_entry(
                            player_name=name,
                            team_abbr=abbr,
                            away_abbr=away_abbr,
                            home_abbr=home_abbr,
                            away_score=away_score,
                            home_score=home_score,
                            value=points or 0,
                            stat_label="PTS",
                            lang=lang,
                            zh_locale=zh_locale,
                            source="fullStats",
                            extra_stats=achieved,
                        )
                        achievement["tier"] = tier_name
                        achievement["achievement"] = (
                            labels["triple_double"] if tier_name == "tripleDouble" else labels["double_double"]
                        )
                        if tier_name == "tripleDouble":
                            triple_doubles.append(achievement)
                        else:
                            double_doubles.append(achievement)
                continue

            for line in (lineups.get("leaders") or {}).get(abbr) or []:
                name, leader_stats = _leader_stats_from_line(line)
                if not name:
                    continue
                extra_stats = {key: leader_stats[key] for key in ("PTS", "REB", "AST") if key in leader_stats}
                if leader_stats.get("PTS") is not None:
                    top_scorer = _update_best_entries(
                        top_scorer,
                        _build_stat_entry(
                            player_name=name,
                            team_abbr=abbr,
                            away_abbr=away_abbr,
                            home_abbr=home_abbr,
                            away_score=away_score,
                            home_score=home_score,
                            value=int(leader_stats["PTS"]),
                            stat_label="PTS",
                            lang=lang,
                            zh_locale=zh_locale,
                            source="leaders",
                            extra_stats=extra_stats,
                        ),
                    )
                if leader_stats.get("REB") is not None:
                    top_rebounder = _update_best_entries(
                        top_rebounder,
                        _build_stat_entry(
                            player_name=name,
                            team_abbr=abbr,
                            away_abbr=away_abbr,
                            home_abbr=home_abbr,
                            away_score=away_score,
                            home_score=home_score,
                            value=int(leader_stats["REB"]),
                            stat_label="REB",
                            lang=lang,
                            zh_locale=zh_locale,
                            source="leaders",
                            extra_stats=extra_stats,
                        ),
                    )
                if leader_stats.get("AST") is not None:
                    top_assists = _update_best_entries(
                        top_assists,
                        _build_stat_entry(
                            player_name=name,
                            team_abbr=abbr,
                            away_abbr=away_abbr,
                            home_abbr=home_abbr,
                            away_score=away_score,
                            home_score=home_score,
                            value=int(leader_stats["AST"]),
                            stat_label="AST",
                            lang=lang,
                            zh_locale=zh_locale,
                            source="leaders",
                            extra_stats=extra_stats,
                        ),
                    )

    double_doubles = sorted(double_doubles, key=lambda item: (int(item.get("value") or 0)), reverse=True)[:2]
    triple_doubles = sorted(triple_doubles, key=lambda item: (int(item.get("value") or 0)), reverse=True)[:2]
    best_performance_candidates = sorted(triple_doubles + top_scorer, key=_performance_sort_key, reverse=True)
    best_performance = best_performance_candidates[:2]
    if completed_games:
        summary = (
            ", ".join(
                f"{entry.get('displayName')} {entry.get('displayValue')}"
                for entry in best_performance
                if entry.get("displayName") and entry.get("displayValue")
            )
            or labels["none"]
        )
    else:
        summary = labels["no_completed_games"]

    return {
        "intent": "stats_day",
        "scope": "multi_all",
        "requestedDate": day_payload["requestedDate"],
        "timezone": day_payload["timezone"],
        "lang": lang,
        "zhLocale": day_payload.get("zhLocale"),
        "leaders": {
            "topScorer": top_scorer,
            "topRebounder": top_rebounder,
            "topAssists": top_assists,
            "topThreePointMade": top_three,
        },
        "notableGames": [largest_margin_game] if largest_margin_game else [],
        "statsView": {
            "completedGamesCount": len(completed_games),
            "bestPerformance": best_performance,
            "topScorer": _stats_block(top_scorer, none_text=labels["none"]),
            "topRebounder": _stats_block(top_rebounder, none_text=labels["none"]),
            "topAssists": _stats_block(top_assists, none_text=labels["none"]),
            "topThreePointMade": _stats_block(top_three, none_text=labels["none"]),
            "doubleDoubles": double_doubles,
            "tripleDoubles": triple_doubles,
            "largestMarginGame": largest_margin_game,
            "summary": summary,
        },
    }


def _render_stat_leader_block(title: str, block: dict[str, Any], *, labels: dict[str, str]) -> list[str]:
    lines = [f"## {title}"]
    leaders = block.get("leaders") or []
    if not leaders:
        lines.extend(["", f"- {labels['none']}", ""])
        return lines
    lines.append("")
    for entry in leaders:
        context_parts: list[str] = []
        if entry.get("teamName"):
            context_parts.append(str(entry["teamName"]))
        if entry.get("matchup"):
            context_parts.append(str(entry["matchup"]))
        context_text = f" | {' | '.join(context_parts)}" if context_parts else ""
        lines.append(f"- {entry.get('displayName') or entry.get('playerName')} | {entry.get('displayValue')}{context_text}")
    lines.append("")
    return lines


def render_day_stats_markdown(payload: dict[str, Any]) -> str:
    lang = str(payload.get("lang") or "zh")
    base_labels = I18N.get(lang, I18N["en"])
    labels = _stats_day_labels(lang)
    stats_view = payload.get("statsView") or {}
    lines = [
        f"# {labels['title']} ({payload['requestedDate']})",
        f"> {base_labels['timezone']}: {payload['timezone']}",
        f"> {base_labels['requested_date']}: {payload['requestedDate']}",
        f"> {base_labels['view']}: {labels['view']}",
        f"> {labels['completed_games']}: {stats_view.get('completedGamesCount', 0)}",
        "",
    ]
    if not stats_view.get("completedGamesCount"):
        lines.append(f"- {labels['no_completed_games']}")
        return "\n".join(lines)
    best_performance = stats_view.get("bestPerformance") or []
    lines.extend([f"## {labels['best_performance']}", ""])
    if best_performance:
        for entry in best_performance:
            extras = entry.get("stats") or {}
            extras_text = ", ".join(f"{value} {key}" for key, value in extras.items())
            suffix = f" | {extras_text}" if extras_text else ""
            lines.append(
                f"- {entry.get('displayName') or entry.get('playerName')} | {entry.get('teamName') or ''} | {entry.get('matchup') or ''}{suffix}".replace(" |  | ", " | ")
            )
    else:
        lines.append(f"- {labels['none']}")
    lines.append("")
    lines.extend(_render_stat_leader_block(labels["top_scorer"], stats_view.get("topScorer") or {}, labels=labels))
    lines.extend(_render_stat_leader_block(labels["top_rebounder"], stats_view.get("topRebounder") or {}, labels=labels))
    lines.extend(_render_stat_leader_block(labels["top_assists"], stats_view.get("topAssists") or {}, labels=labels))
    lines.extend(_render_stat_leader_block(labels["top_three"], stats_view.get("topThreePointMade") or {}, labels=labels))
    lines.extend([f"## {labels['double_triple']}", ""])
    double_doubles = stats_view.get("doubleDoubles") or []
    triple_doubles = stats_view.get("tripleDoubles") or []
    if triple_doubles or double_doubles:
        for entry in triple_doubles + double_doubles:
            achievement = entry.get("achievement") or labels["none"]
            extras = ", ".join(f"{value} {key}" for key, value in (entry.get("stats") or {}).items())
            extras_text = f" | {extras}" if extras else ""
            lines.append(
                f"- {entry.get('displayName') or entry.get('playerName')} | {achievement} | {entry.get('teamName') or ''} | {entry.get('matchup') or ''}{extras_text}".replace(" |  | ", " | ")
            )
    else:
        lines.append(f"- {labels['none']}")
    lines.extend(["", f"## {labels['largest_margin']}", ""])
    largest_margin = stats_view.get("largestMarginGame") or {}
    if largest_margin:
        lines.append(
            f"- {largest_margin.get('matchup')} | {largest_margin.get('winnerName')} {labels['won_by']} {largest_margin.get('margin')}"
        )
    else:
        lines.append(f"- {labels['none']}")
    lines.extend(["", f"## {labels['summary_prefix']}", "", f"- {stats_view.get('summary') or labels['none']}"])
    return "\n".join(lines).rstrip()


def _render_info_section(
    info: dict[str, Any],
    labels: dict[str, str],
    phase_labels: dict[str, str],
    *,
    zh_locale: str | None = None,
) -> list[str]:
    lang = "zh" if labels.get("timezone") == "请求方时区" else "en"
    lines = [f"## {phase_labels['info']}"]
    matchup = info.get("matchup") or {}
    team_abbrs = _matchup_team_abbrs(matchup)
    away_abbr = ((matchup.get("away") or {}).get("abbr"))
    home_abbr = ((matchup.get("home") or {}).get("abbr"))
    away_score = (matchup.get("away") or {}).get("score")
    home_score = (matchup.get("home") or {}).get("score")
    if away_abbr and home_abbr:
        if info.get("statusState") in {"in", "post"} and (away_score not in (None, "") or home_score not in (None, "")):
            lines.append(f"- {format_matchup_display(away_abbr, home_abbr, lang=lang, zh_locale=zh_locale, away_score=away_score, home_score=home_score)}")
        else:
            lines.append(f"- {format_matchup_display(away_abbr, home_abbr, lang=lang, zh_locale=zh_locale)}")
    elif matchup.get("text"):
        lines.append(f"- {_localize_team_mentions(matchup['text'], lang=lang, zh_locale=zh_locale, team_abbrs=team_abbrs)}")
    if info.get("startTimeLocal"):
        lines.append(f"- {labels['start_time']}: {info['startTimeLocal']}")
    status_detail = info.get("statusDetail")
    if status_detail:
        lines.append(f"- {labels['status']}: {status_detail}")
    if info.get("venue"):
        lines.append(f"- {labels['venue']}: {info['venue']}")
    broadcasts = info.get("broadcasts") or []
    if broadcasts:
        lines.append(f"- {labels['broadcasts']}: {', '.join(broadcasts)}")
    standings = info.get("standings") or {}
    for side in ("away", "home"):
        team = matchup.get(side) or {}
        abbr = team.get("abbr")
        if not abbr:
            continue
        record = team.get("record") or labels["none"]
        standing = standings.get(abbr) or {}
        rank_bits: list[str] = []
        if standing.get("wins") is not None and standing.get("losses") is not None:
            rank_bits.append(f"{standing['wins']}-{standing['losses']}")
        if standing.get("streak"):
            rank_bits.append(str(standing["streak"]))
        suffix = f" ({', '.join(rank_bits)})" if rank_bits else ""
        if lang == "zh":
            lines.append(f"- {_display_team(abbr, lang, zh_locale)} {labels['records']}: {record}{suffix}")
        else:
            lines.append(f"- {_display_team(abbr, lang, zh_locale)} enter at {record}{suffix}.")
    lines.append("")
    return lines


def _render_lineups_section(
    lineups: dict[str, Any],
    season_averages: dict[str, Any],
    matchup: dict[str, Any],
    labels: dict[str, str],
    phase_labels: dict[str, str],
    *,
    zh_locale: str | None = None,
) -> list[str]:
    lang = "zh" if labels.get("timezone") == "请求方时区" else "en"
    lines = [f"## {phase_labels['lineups']}"]
    if lineups.get("startersConfirmed"):
        for side in ("away", "home"):
            team = matchup.get(side) or {}
            abbr = team.get("abbr")
            if not abbr:
                continue
            starters = (lineups.get("starters") or {}).get(abbr) or []
            rendered = ", ".join(localize_player_list(starters, lang)) if starters else phase_labels["none"]
            lines.append(f"- {_display_team(abbr, lang, zh_locale)} {labels['starters']}: {rendered}")
    else:
        lines.append(f"- {phase_labels['starters_pending']}")
    for side in ("away", "home"):
        team = matchup.get(side) or {}
        abbr = team.get("abbr")
        if not abbr:
            continue
        key_players = (lineups.get("keyPlayers") or {}).get(abbr) or (lineups.get("leaders") or {}).get(abbr) or []
        if not key_players:
            continue
        lines.append(f"- {_display_team(abbr, lang, zh_locale)}:")
        for line in key_players[:5]:
            lines.append(f"  - {localize_player_line(line, lang)}")
    lines.append("")
    return lines


def _render_injuries_section(
    injuries: dict[str, Any],
    matchup: dict[str, Any],
    labels: dict[str, str],
    phase_labels: dict[str, str],
    *,
    zh_locale: str | None = None,
    active_players: list[str] | None = None,
) -> list[str]:
    lang = "zh" if labels.get("timezone") == "请求方时区" else "en"
    lines = [f"## {phase_labels['injuries']}"]
    by_team = injuries.get("byTeam") or {}
    # 如果有已确认上场球员名单，则过滤掉其中的人（名字子字符串匹配）
    active_lower: set[str] = {n.lower() for n in (active_players or []) if n}
    for side in ("away", "home"):
        team = matchup.get(side) or {}
        abbr = team.get("abbr")
        if not abbr:
            continue
        items = by_team.get(abbr) or []
        filtered: list[str] = []
        for item in items[:6]:
            player_name = extract_primary_name(item).lower()
            if active_lower and any(
                player_name in active.lower() or active.lower() in player_name
                for active in active_lower
            ):
                continue
            filtered.append(item)
        localized = [localize_player_line(item, lang) for item in filtered]
        lines.append(f"- {_display_team(abbr, lang, zh_locale)}: {'; '.join(localized) if localized else phase_labels['none']}")
    lines.append("")
    return lines


def _render_team_totals_section(
    full_stats: dict[str, Any],
    matchup: dict[str, Any],
    labels: dict[str, str],
    phase_labels: dict[str, str],
    *,
    zh_locale: str | None = None,
) -> list[str]:
    lang = "zh" if labels.get("timezone") == "请求方时区" else "en"
    lines = [f"## {phase_labels['team_totals']}"]
    teams = full_stats.get("teams") or {}
    emitted = False
    for side in ("away", "home"):
        team = matchup.get(side) or {}
        abbr = team.get("abbr")
        if not abbr:
            continue
        stats = teams.get(abbr) or {}
        compact = render_full_stats_team_line(stats)
        if compact:
            lines.append(f"- {_display_team(abbr, lang, zh_locale)}: {compact}")
            emitted = True
    if not emitted:
        lines.append(f"- {phase_labels['none']}")
    lines.append("")
    return lines


def _render_key_player_lines_section(
    full_stats: dict[str, Any],
    matchup: dict[str, Any],
    labels: dict[str, str],
    phase_labels: dict[str, str],
    *,
    limit: int = 3,
    player_focus: str | None = None,
    zh_locale: str | None = None,
) -> list[str]:
    lang = "zh" if labels.get("timezone") == "请求方时区" else "en"
    lines = [f"## {phase_labels['key_player_lines']}"]
    players_by_team = full_stats.get("players") or {}
    emitted = False
    for side in ("away", "home"):
        team = matchup.get(side) or {}
        abbr = team.get("abbr")
        if not abbr:
            continue
        players = _filter_player_stats(players_by_team.get(abbr) or [], player_focus=player_focus)
        if not players:
            continue
        top_lines = [render_compact_player_stat_line(player, lang=lang, include_secondary=True, include_shooting=True) for player in players[:limit]]
        if _append_team_player_block(lines, _display_team(abbr, lang, zh_locale), top_lines):
            emitted = True
    if not emitted:
        lines.append(f"- {phase_labels['none']}")
    lines.append("")
    return lines


def _render_post_starters_section(
    lineups: dict[str, Any],
    matchup: dict[str, Any],
    phase_labels: dict[str, str],
    *,
    lang: str,
    zh_locale: str | None = None,
) -> list[str]:
    lines = [f"## {phase_labels['starters_section']}"]
    if lineups.get("startersConfirmed"):
        for side in ("away", "home"):
            team = matchup.get(side) or {}
            abbr = team.get("abbr")
            if not abbr:
                continue
            starters = (lineups.get("starters") or {}).get(abbr) or []
            rendered = ", ".join(localize_player_list(starters, lang)) if starters else phase_labels["none"]
            lines.append(f"- {_display_team(abbr, lang, zh_locale)}: {rendered}")
    else:
        lines.append(f"- {phase_labels['starters_pending']}")
    lines.append("")
    return lines


def _render_post_key_performances_section(
    full_stats: dict[str, Any],
    lineups: dict[str, Any],
    matchup: dict[str, Any],
    phase_labels: dict[str, str],
    *,
    lang: str,
    limit: int = 3,
    player_focus: str | None = None,
    zh_locale: str | None = None,
) -> list[str]:
    lines = [f"## {phase_labels['post_key_players']}"]
    players_by_team = full_stats.get("players") or {}
    emitted = False
    for side in ("away", "home"):
        team = matchup.get(side) or {}
        abbr = team.get("abbr")
        if not abbr:
            continue
        players = _filter_player_stats(players_by_team.get(abbr) or [], player_focus=player_focus)
        rendered_players = []
        for player in players[:limit]:
            line = render_compact_player_stat_line(
                player,
                lang=lang,
                include_secondary=False,
                include_shooting=False,
            )
            if line:
                rendered_players.append(line)
        if rendered_players:
            _append_team_player_block(lines, _display_team(abbr, lang, zh_locale), rendered_players)
            emitted = True
            continue
        fallback_players = (lineups.get("keyPlayers") or {}).get(abbr) or (lineups.get("leaders") or {}).get(abbr) or []
        if player_focus:
            focus_identity = normalize_player_identity(player_focus)
            fallback_players = [
                item for item in fallback_players if normalize_player_identity(extract_primary_name(item)) == focus_identity
            ]
        if fallback_players:
            localized_fallback = [localize_player_line(item, lang) for item in fallback_players[:limit]]
            if _append_team_player_block(lines, _display_team(abbr, lang, zh_locale), localized_fallback):
                emitted = True
    if not emitted:
        lines.append(f"- {phase_labels['none']}")
    lines.append("")
    return lines


def _render_post_team_totals_section(
    full_stats: dict[str, Any],
    matchup: dict[str, Any],
    phase_labels: dict[str, str],
    *,
    lang: str,
    zh_locale: str | None = None,
) -> list[str]:
    lines = [f"## {phase_labels['post_team_totals']}"]
    teams = full_stats.get("teams") or {}
    emitted = False
    for side in ("away", "home"):
        team = matchup.get(side) or {}
        abbr = team.get("abbr")
        if not abbr:
            continue
        compact = render_compact_team_totals_line(teams.get(abbr) or {}, lang=lang)
        if compact:
            lines.append(f"- {_display_team(abbr, lang, zh_locale)}: {compact}")
            emitted = True
    if not emitted:
        lines.append(f"- {phase_labels['none']}")
    lines.append("")
    return lines


def _player_impact_sort_key(player: dict[str, Any]) -> tuple[float, float, float, float, float, float]:
    stats = player.get("stats") or {}
    def num(key: str) -> float:
        value = stats.get(key)
        try:
            return float(value)
        except (TypeError, ValueError):
            return -1.0
    return (
        num("PTS"),
        num("REB"),
        num("AST"),
        num("STL"),
        num("BLK"),
        num("MIN"),
    )


def _select_live_players_for_display(
    *,
    abbr: str,
    players_by_team: dict[str, list[dict[str, Any]]],
    lineups: dict[str, Any],
    limit: int = 5,
    prioritize_starters: bool = False,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    players = list(players_by_team.get(abbr) or [])
    starters = (lineups.get("starters") or {}).get(abbr) or []
    leader_names = {
        normalize_player_identity(extract_primary_name(line))
        for line in (lineups.get("leaders") or {}).get(abbr) or []
        if extract_primary_name(line)
    }
    normalized_players = {
        normalize_player_identity(str(player.get("playerName") or "")): player
        for player in players
        if player.get("playerName")
    }
    matched_starters: list[str] = []
    unmatched_starters: list[str] = []
    for starter_name in starters:
        normalized = normalize_player_identity(starter_name)
        player = normalized_players.get(normalized)
        if player:
            matched_starters.append(starter_name)
        else:
            unmatched_starters.append(starter_name)
    ranked: list[tuple[int, dict[str, Any]]] = []
    for index, player in enumerate(players):
        normalized = normalize_player_identity(str(player.get("playerName") or ""))
        if not normalized:
            continue
        ranked.append((index, player))
    if prioritize_starters:
        selected: list[dict[str, Any]] = []
        seen: set[str] = set()
        for starter_name in starters:
            normalized = normalize_player_identity(starter_name)
            player = normalized_players.get(normalized)
            if not player or normalized in seen:
                continue
            selected.append(player)
            seen.add(normalized)
        remaining = [(index, player) for index, player in ranked if normalize_player_identity(str(player.get("playerName") or "")) not in seen]
        remaining.sort(
            key=lambda item: (
                0 if item[1].get("starter") else 1,
                -_player_impact_sort_key(item[1])[0],
                -_player_impact_sort_key(item[1])[1],
                -_player_impact_sort_key(item[1])[2],
                -_player_impact_sort_key(item[1])[3],
                -_player_impact_sort_key(item[1])[4],
                -_player_impact_sort_key(item[1])[5],
                item[0],
            )
        )
        selected.extend(player for _, player in remaining[: max(0, limit - len(selected))])
        return selected[:limit], {
            "availableCount": len(players),
            "renderedCount": len(selected[:limit]),
            "matchedStarters": matched_starters,
            "unmatchedStarters": unmatched_starters,
        }
    ranked.sort(
        key=lambda item: (
            0 if normalize_player_identity(str(item[1].get("playerName") or "")) in leader_names else 1,
            -_player_impact_sort_key(item[1])[0],
            -_player_impact_sort_key(item[1])[2],
            -_player_impact_sort_key(item[1])[1],
            -_player_impact_sort_key(item[1])[3],
            -_player_impact_sort_key(item[1])[4],
            -_player_impact_sort_key(item[1])[5],
            0 if item[1].get("starter") else 1,
            item[0],
        )
    )
    selected = [player for _, player in ranked[:limit]]
    return selected[:limit], {
        "availableCount": len(players),
        "renderedCount": len(selected[:limit]),
        "matchedStarters": matched_starters,
        "unmatchedStarters": unmatched_starters,
    }


def _build_live_player_display(
    *,
    full_stats: dict[str, Any],
    lineups: dict[str, Any],
    matchup: dict[str, Any],
    limit: int = 5,
    prioritize_starters: bool = False,
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, dict[str, Any]]]:
    players_by_team = full_stats.get("players") or {}
    selected_by_team: dict[str, list[dict[str, Any]]] = {}
    coverage_by_team: dict[str, dict[str, Any]] = {}
    for side in ("away", "home"):
        team = matchup.get(side) or {}
        abbr = team.get("abbr")
        if not abbr:
            continue
        selected, coverage = _select_live_players_for_display(
            abbr=abbr,
            players_by_team=players_by_team,
            lineups=lineups,
            limit=limit,
            prioritize_starters=prioritize_starters,
        )
        selected_by_team[abbr] = selected
        coverage_by_team[abbr] = coverage
    return selected_by_team, coverage_by_team


def _player_line_from_full_stats(player: dict[str, Any]) -> str:
    name = str(player.get("playerName") or "").strip()
    stats = player.get("stats") or {}
    parts = [name]
    for key in ("PTS", "REB", "AST"):
        value = stats.get(key)
        if value not in (None, ""):
            parts.append(f"{value} {key}")
    return " | ".join(part for part in parts if part)


def _lineups_with_live_player_display(
    lineups: dict[str, Any],
    selected_by_team: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    display_lineups = dict(lineups)
    key_players = dict(lineups.get("keyPlayers") or {})
    for abbr, players in selected_by_team.items():
        lines = [_player_line_from_full_stats(player) for player in players]
        if lines:
            key_players[abbr] = [line for line in lines if line]
    display_lineups["keyPlayers"] = key_players
    return display_lineups


def _status_to_phase(status_state: str) -> str:
    if status_state == "in":
        return "live"
    if status_state == "post":
        return "post"
    return "pregame"


def _day_card_status_title(phase: str, labels: dict[str, str]) -> str:
    if phase == "live":
        return labels["live_title"]
    if phase == "post":
        return labels["post_title"]
    return labels["pre_title"]


def _primary_story_signal(official_story: dict[str, Any] | None) -> dict[str, str]:
    story = official_story or {}
    if not story.get("available"):
        return {}
    signals = [signal for signal in (story.get("summarySignals") or []) if isinstance(signal, dict)]
    if not signals:
        return {}
    return {
        "sourceLabel": str(story.get("sourceLabel") or "NBA.com"),
        "headline": str(story.get("headline") or ""),
        "url": str(story.get("url") or ""),
        **{str(key): str(value or "") for key, value in signals[0].items()},
    }


def _story_signal_by_priority(
    official_story: dict[str, Any] | None,
    preferred_kinds: tuple[str, ...],
) -> dict[str, str]:
    story = official_story or {}
    if not story.get("available"):
        return {}
    signals = [signal for signal in (story.get("summarySignals") or []) if isinstance(signal, dict)]
    if not signals:
        return {}
    selected = None
    for kind in preferred_kinds:
        selected = next((signal for signal in signals if str(signal.get("kind") or "") == kind), None)
        if selected:
            break
    if not selected:
        selected = signals[0]
    return {
        "sourceLabel": str(story.get("sourceLabel") or "NBA.com"),
        "headline": str(story.get("headline") or ""),
        "url": str(story.get("url") or ""),
        **{str(key): str(value or "") for key, value in selected.items()},
    }


def _pregame_story_signal(official_story: dict[str, Any] | None) -> dict[str, str]:
    return _story_signal_by_priority(
        official_story,
        (
            "availability",
            "short_handed",
            "matchup_watch",
            "previous_matchups",
            "series_context",
            "efficiency",
            "standout_scorer",
        ),
    )


def _compact_lineups_for_day(scene: dict[str, Any]) -> dict[str, Any]:
    game = scene["game"]
    lineups = (game.get("gameContext") or {}).get("lineups") or {}
    season_averages = (game.get("gameContext") or {}).get("seasonAverages") or {}
    compact: dict[str, list[str]] = {}
    for abbr in (game["away"]["abbr"], game["home"]["abbr"]):
        candidates = (lineups.get("keyPlayers") or {}).get(abbr) or (lineups.get("leaders") or {}).get(abbr) or []
        lines: list[str] = []
        for line in candidates[:2]:
            primary = extract_primary_name(line)
            averages = _format_average_line((season_averages.get(abbr) or {}).get(primary) or {})
            suffix = f" ({averages})" if averages else ""
            lines.append(f"{line}{suffix}")
        compact[abbr] = lines
    return {
        "startersConfirmed": bool(lineups.get("startersConfirmed")),
        "starters": lineups.get("starters") or {},
        "keyPlayersByTeam": compact,
    }


def _build_pregame_card(scene: dict[str, Any]) -> dict[str, Any]:
    game = scene["game"]
    pregame = scene.get("pregame") or {}
    prediction = pregame.get("prediction") or {}
    story_signal = _primary_story_signal(game.get("officialStory"))
    return {
        "type": "pregameCard",
        "info": pregame.get("info") or {},
        "lineups": _compact_lineups_for_day(scene),
        "injuries": {
            "featuredByTeam": (pregame.get("injuries") or {}).get("compactByTeam") or (pregame.get("injuries") or {}).get("featuredByTeam") or {},
        },
        "teamForm": pregame.get("teamForm") or {},
        "prediction": {
            "summary": prediction.get("summary") or "",
            "trend": prediction.get("trend") or "",
            "keyMatchup": prediction.get("keyMatchup") or "",
        },
        "summary": pregame.get("summary") or "",
        "storySignal": story_signal,
        "storyBrief": _story_brief(game.get("officialStory"), phase="pregame"),
        "storySummary": _story_summary_text(game.get("officialStory"), phase="pregame", lang=scene["report"]["lang"]),
        "storyAiContext": _story_ai_context_for_card(game, phase="pregame"),
        "teams": {
            "away": game["away"],
            "home": game["home"],
        },
    }


def _build_live_card(scene: dict[str, Any]) -> dict[str, Any]:
    live = scene.get("live") or {}
    live_state = live.get("liveState") or {}
    full_stats = ((scene["game"].get("gameContext") or {}).get("fullStats") or {"available": False, "teams": {}, "players": {}})
    lineups = live.get("lineups") or {}
    matchup = ((live.get("info") or {}).get("matchup") or {})
    _, coverage = _build_live_player_display(full_stats=full_stats, lineups=lineups, matchup=matchup, limit=3, prioritize_starters=True)
    latest_play = ""
    if live_state.get("playTimeline"):
        item = (live_state.get("playTimeline") or [])[-1]
        latest_clock = " ".join(
            part
            for part in (
                f"P{item.get('period')}" if item.get("period") else "",
                item.get("clock") or "",
            )
            if part
        ).strip()
        latest_text = item.get("text") or item.get("shortDescription") or ""
        latest_play = f"{latest_clock} {latest_text}".strip()
    return {
        "type": "liveCard",
        "info": live.get("info") or {},
        "lineups": _compact_lineups_for_day(scene),
        "injuries": live.get("injuries") or {},
        "liveState": {
            "displayClock": live_state.get("displayClock"),
            "period": live_state.get("period"),
            "latestPlay": latest_play,
            "winProbabilityTimeline": live_state.get("winProbabilityTimeline") or [],
        },
        "momentum": live.get("momentum") or {},
        "fullStats": full_stats,
        "playerStatsCoverage": coverage,
        "digest": {
            "plays": (scene.get("digest") or {}).get("plays") or [],
        },
        "summary": live.get("summary") or "",
    }


def _build_postgame_card(scene: dict[str, Any]) -> dict[str, Any]:
    postgame = scene.get("postgame") or {}
    story_signal = _primary_story_signal((scene["game"] or {}).get("officialStory"))
    return {
        "type": "postgameCard",
        "info": postgame.get("info") or {},
        "lineups": _compact_lineups_for_day(scene),
        "injuries": postgame.get("injuries") or {},
        "fullStats": postgame.get("fullStats") or {"available": False, "teams": {}, "players": {}},
        "turningPoint": postgame.get("turningPoint") or "",
        "summary": postgame.get("summary") or "",
        "trend": scene.get("analysis", {}).get("trend") or "",
        "reasons": scene.get("analysis", {}).get("reasons") or [],
        "storySignal": story_signal,
        "storyBrief": _story_brief((scene["game"] or {}).get("officialStory"), phase="post"),
        "storySummary": _story_summary_text((scene["game"] or {}).get("officialStory"), phase="post", lang=scene["report"]["lang"]),
        "storyAiContext": _story_ai_context_for_card(scene["game"], phase="post"),
    }


def _build_day_card(scene: dict[str, Any], phase: str) -> dict[str, Any]:
    if phase == "live":
        return _build_live_card(scene)
    if phase == "post":
        return _build_postgame_card(scene)
    return _build_pregame_card(scene)


def _compact_lineups_from_game(game: dict[str, Any]) -> dict[str, Any]:
    compact: dict[str, list[str]] = {}
    for abbr in (game["away"]["abbr"], game["home"]["abbr"]):
        candidates = (game.get("keyPlayers") or {}).get(abbr) or (game.get("leaders") or {}).get(abbr) or []
        compact[abbr] = [str(line) for line in candidates[:2] if str(line).strip()]
    return {
        "startersConfirmed": bool(game.get("startersConfirmed")),
        "starters": game.get("starters") or {},
        "keyPlayersByTeam": compact,
    }


def _build_day_game_context_minimal(game: dict[str, Any]) -> dict[str, Any]:
    return {
        "info": {
            "eventId": game["eventId"],
            "matchup": {
                "text": f"{game['away']['abbr']} @ {game['home']['abbr']}",
                "away": game["away"],
                "home": game["home"],
            },
            "requestedDate": game.get("requestedDate"),
            "statusState": game.get("statusState"),
            "statusDetail": game.get("statusDetail"),
            "startTimeLocal": game.get("startTimeLocal"),
            "venue": game.get("venue"),
            "broadcasts": game.get("broadcasts") or [],
            "standings": {},
        },
        "lineups": {
            "startersConfirmed": bool(game.get("startersConfirmed")),
            "starters": game.get("starters") or {},
            "keyPlayers": game.get("keyPlayers") or {},
            "leaders": game.get("leaders") or {},
            "verifiedPlayers": game.get("verifiedPlayers") or [],
            "activeParticipants": game.get("activeParticipants") or [],
        },
        "injuries": {
            "items": game.get("injuryItems") or {},
            "byTeam": game.get("injuries") or {},
            "meta": game.get("injuryMeta") or {},
        },
        "teamForm": {},
        "headToHead": {},
        "seasonAverages": {},
        "liveState": {
            "displayClock": game.get("displayClock"),
            "period": game.get("period"),
            "recentPlays": game.get("recentPlays") or [],
            "playTimeline": game.get("playTimeline") or [],
            "winProbabilityTimeline": game.get("winProbabilityTimeline") or [],
        },
        "fullStats": game.get("fullStats") or {"available": False, "source": "unavailable", "teams": {}, "players": {}},
        "officialStory": game.get("officialStory") or {},
    }


def _build_day_fast_card(game: dict[str, Any], analysis: dict[str, Any], phase: str) -> dict[str, Any]:
    game_context = game.get("gameContext") or {}
    if phase == "live":
        live_state = game_context.get("liveState") or {}
        full_stats = game_context.get("fullStats") or {"available": False, "source": "unavailable", "teams": {}, "players": {}}
        lineups = game_context.get("lineups") or {}
        matchup = (game_context.get("info") or {}).get("matchup") or {}
        _, coverage = _build_live_player_display(full_stats=full_stats, lineups=lineups, matchup=matchup, limit=3, prioritize_starters=True)
        latest_play = ""
        if live_state.get("playTimeline"):
            item = (live_state.get("playTimeline") or [])[-1]
            latest_clock = " ".join(
                part
                for part in (
                    f"P{item.get('period')}" if item.get("period") else "",
                    item.get("clock") or "",
                )
                if part
            ).strip()
            latest_text = item.get("text") or item.get("shortDescription") or ""
            latest_play = f"{latest_clock} {latest_text}".strip()
        return {
            "type": "liveCard",
            "info": game_context.get("info") or {},
            "lineups": _compact_lineups_from_game(game),
            "injuries": game_context.get("injuries") or {},
            "liveState": {
                "displayClock": live_state.get("displayClock"),
                "period": live_state.get("period"),
                "latestPlay": latest_play,
                "winProbabilityTimeline": live_state.get("winProbabilityTimeline") or [],
            },
            "momentum": {
                "trend": analysis.get("trend") or "",
                "reasons": analysis.get("reasons") or [],
            },
            "fullStats": full_stats,
            "playerStatsCoverage": coverage,
            "digest": {
                "plays": [],
            },
            "summary": analysis.get("summary") or "",
        }
    if phase == "post":
        return {
            "type": "postgameCard",
            "info": game_context.get("info") or {},
            "lineups": _compact_lineups_from_game(game),
            "injuries": game_context.get("injuries") or {},
            "fullStats": game_context.get("fullStats") or {"available": False, "source": "unavailable", "teams": {}, "players": {}},
            "turningPoint": analysis.get("turningPoint") or "",
            "summary": analysis.get("summary") or "",
            "trend": analysis.get("trend") or "",
            "reasons": analysis.get("reasons") or [],
            "storySignal": _primary_story_signal(game.get("officialStory")),
            "storyBrief": _story_brief(game.get("officialStory"), phase="post"),
            "storySummary": _story_summary_text(game.get("officialStory"), phase="post", lang=game.get("lang") or "zh"),
            "storyAiContext": _story_ai_context_for_card(game, phase="post"),
        }
    return {
        "type": "pregameCard",
        "info": game_context.get("info") or {},
        "lineups": _compact_lineups_from_game(game),
        "injuries": {
            "featuredByTeam": {
                game["away"]["abbr"]: (game.get("injuries") or {}).get(game["away"]["abbr"], [])[:2],
                game["home"]["abbr"]: (game.get("injuries") or {}).get(game["home"]["abbr"], [])[:2],
            },
        },
        "teamForm": {},
        "prediction": {
            "summary": analysis.get("summary") or "",
            "trend": analysis.get("trend") or "",
            "keyMatchup": analysis.get("keyMatchup") or "",
        },
        "summary": analysis.get("summary") or "",
        "storySignal": _primary_story_signal(game.get("officialStory")),
        "storyBrief": _story_brief(game.get("officialStory"), phase="pregame"),
        "storySummary": _story_summary_text(game.get("officialStory"), phase="pregame", lang=game.get("lang") or "zh"),
        "storyAiContext": _story_ai_context_for_card(game, phase="pregame"),
        "teams": {
            "away": game["away"],
            "home": game["home"],
        },
    }


def _day_bucket_defs(lang: str) -> tuple[dict[str, Any], list[tuple[str, str, str]]]:
    day_labels = _day_labels(lang)
    bucket_defs = [
        ("live", "in", day_labels["live_title"]),
        ("post", "post", day_labels["post_title"]),
        ("pregame", "pre", day_labels["pre_title"]),
    ]
    return day_labels, bucket_defs


def _finalize_day_payload(
    *,
    report: dict[str, Any],
    games_payload: list[dict[str, Any]],
    phase_filter: str | None,
    bucket_defs: list[tuple[str, str, str]],
) -> dict[str, Any]:
    if phase_filter:
        games_payload = [game for game in games_payload if game.get("phase") == phase_filter]
    status_buckets: list[dict[str, Any]] = []
    for phase, state, title in bucket_defs:
        if phase_filter and phase != phase_filter:
            continue
        event_ids = [game["eventId"] for game in games_payload if game.get("phase") == phase]
        status_buckets.append(
            {
                "phase": phase,
                "statusState": state,
                "title": title,
                "count": len(event_ids),
                "eventIds": event_ids,
            }
        )
    filtered_counts = {
        "total": len(games_payload),
        "in": sum(1 for game in games_payload if game.get("phase") == "live"),
        "post": sum(1 for game in games_payload if game.get("phase") == "post"),
        "pre": sum(1 for game in games_payload if game.get("phase") == "pregame"),
    }
    summary = format_counts_summary(filtered_counts, report["labels"])
    payload = {
        "intent": "day",
        "scope": "multi_all",
        "requestedDate": report["requestedDate"],
        "timezone": report["timezone"],
        "lang": report["lang"],
        "zhLocale": report.get("zhLocale"),
        "dayView": {
            "counts": filtered_counts,
            "statusBuckets": status_buckets,
            "summary": summary,
            "phaseFilter": phase_filter,
        },
        "games": games_payload,
    }
    return payload


def _build_day_view_full(
    *,
    tz: str | None,
    date_text: str | None,
    lang: str,
    zh_locale: str | None,
    phase_filter: str | None,
) -> dict[str, Any]:
    report = build_scene_report(tz=tz, date_text=date_text, team=None, lang=lang, zh_locale=zh_locale, detail_level="full")
    _, bucket_defs = _day_bucket_defs(lang)
    raw_games = sorted(
        report["games"],
        key=lambda game: (
            {"in": 0, "post": 1, "pre": 2}.get(str(game.get("statusState") or "pre"), 3),
            str(game.get("startTimeLocal") or ""),
            str(game.get("eventId") or ""),
        ),
    )
    scenes: list[dict[str, Any]] = []
    for game in raw_games:
        phase = _status_to_phase(str(game.get("statusState") or "pre"))
        scenes.append(finalize_scene_game(report=report, game=game, lang=lang, analysis_mode=phase, intent="day", scope="multi_all"))
    games_payload = [
        {
            "eventId": scene["game"]["eventId"],
            "phase": _status_to_phase(str(scene["game"].get("statusState") or "pre")),
            "teams": {
                "away": scene["game"]["away"],
                "home": scene["game"]["home"],
            },
            "gameContext": scene["game"].get("gameContext") or {},
            "card": _build_day_card(scene, _status_to_phase(str(scene["game"].get("statusState") or "pre"))),
        }
        for scene in scenes
    ]
    return _finalize_day_payload(report=report, games_payload=games_payload, phase_filter=phase_filter, bucket_defs=bucket_defs)


def _build_day_view_fast(
    *,
    tz: str | None,
    date_text: str | None,
    lang: str,
    zh_locale: str | None,
    phase_filter: str | None,
) -> dict[str, Any]:
    report = build_scene_report(tz=tz, date_text=date_text, team=None, lang=lang, zh_locale=zh_locale, detail_level="day_fast")
    _, bucket_defs = _day_bucket_defs(lang)
    raw_games = sorted(
        report["games"],
        key=lambda game: (
            {"in": 0, "post": 1, "pre": 2}.get(str(game.get("statusState") or "pre"), 3),
            str(game.get("startTimeLocal") or ""),
            str(game.get("eventId") or ""),
        ),
    )
    games_payload: list[dict[str, Any]] = []
    for game in raw_games:
        phase = _status_to_phase(str(game.get("statusState") or "pre"))
        game["requestedDate"] = report["requestedDate"]
        game["lang"] = report["lang"]
        if phase == "live" and (not game.get("playTimeline") or not game.get("winProbabilityTimeline")):
            augment_game_with_nba_live(game, requested_date=report["requestedDate"])
        game["fullStats"] = build_full_stats(game)
        game["gameContext"] = _build_day_game_context_minimal(game)
        analysis = build_analysis(game, phase, report["labels"])
        games_payload.append(
            {
                "eventId": game["eventId"],
                "phase": phase,
                "teams": {
                    "away": game["away"],
                    "home": game["home"],
                },
                "gameContext": game.get("gameContext") or {},
                "card": _build_day_fast_card(game, analysis, phase),
            }
        )
    return _finalize_day_payload(report=report, games_payload=games_payload, phase_filter=phase_filter, bucket_defs=bucket_defs)


def build_day_view(
    *,
    tz: str | None,
    date_text: str | None,
    lang: str,
    zh_locale: str | None = None,
    phase_filter: str | None = None,
    detail_level: str = "fast",
) -> dict[str, Any]:
    if detail_level == "full":
        return _build_day_view_full(tz=tz, date_text=date_text, lang=lang, zh_locale=zh_locale, phase_filter=phase_filter)
    return _build_day_view_fast(tz=tz, date_text=date_text, lang=lang, zh_locale=zh_locale, phase_filter=phase_filter)


def _day_starters_line(
    *,
    lineups: dict[str, Any],
    matchup: dict[str, Any],
    lang: str,
    zh_locale: str | None,
) -> str:
    if not lineups.get("startersConfirmed"):
        return ""
    parts: list[str] = []
    for side in ("away", "home"):
        team = matchup.get(side) or {}
        abbr = team.get("abbr")
        if not abbr:
            continue
        starters = (lineups.get("starters") or {}).get(abbr) or []
        if not starters:
            continue
        rendered = ", ".join(localize_player_list(starters, lang))
        parts.append(f"{_display_team(abbr, lang, zh_locale)}: {rendered}")
    if not parts:
        return ""
    label = "首发" if lang == "zh" else "Starters"
    joiner = " / " if lang == "zh" else " | "
    return f"{label}: {joiner.join(parts)}"


def _day_key_player_lines(
    *,
    full_stats: dict[str, Any],
    lineups: dict[str, Any],
    matchup: dict[str, Any],
    lang: str,
    zh_locale: str | None,
    limit: int = 2,
) -> list[str]:
    players_by_team = full_stats.get("players") or {}
    lines: list[str] = []
    for side in ("away", "home"):
        team = matchup.get(side) or {}
        abbr = team.get("abbr")
        if not abbr:
            continue
        selected, _coverage = _select_live_players_for_display(
            abbr=abbr,
            players_by_team=players_by_team,
            lineups=lineups,
            limit=limit,
            prioritize_starters=False,
        )
        rendered = [
            render_compact_player_stat_line(player, lang=lang, include_secondary=False, include_shooting=False)
            for player in selected[:limit]
        ]
        rendered = [item for item in rendered if item]
        if not rendered:
            fallback = (lineups.get("keyPlayersByTeam") or {}).get(abbr) or (lineups.get("keyPlayers") or {}).get(abbr) or []
            rendered = [localize_player_line(item, lang) for item in fallback[:limit] if str(item or "").strip()]
        if rendered:
            team_name = _display_team(abbr, lang, zh_locale)
            label = "关键球员" if lang == "zh" else "Key players"
            lines.append(f"{team_name} {label}: {'; '.join(rendered)}")
    return lines


def _day_team_totals_lines(
    *,
    full_stats: dict[str, Any],
    matchup: dict[str, Any],
    lang: str,
    zh_locale: str | None,
) -> list[str]:
    teams = full_stats.get("teams") or {}
    lines: list[str] = []
    for side in ("away", "home"):
        team = matchup.get(side) or {}
        abbr = team.get("abbr")
        if not abbr:
            continue
        compact = render_compact_team_totals_line(teams.get(abbr) or {}, lang=lang)
        if compact:
            label = "球队统计" if lang == "zh" else "Team totals"
            lines.append(f"{_display_team(abbr, lang, zh_locale)} {label}: {compact}")
    return lines


def render_day_view_markdown(payload: dict[str, Any]) -> str:
    lang = str(payload.get("lang") or "zh")
    zh_locale = payload.get("zhLocale")
    labels = I18N.get(lang, I18N["en"])
    day_labels = _day_labels(lang)
    lines = [
        f"# {labels['title_day']} ({payload['requestedDate']})",
        f"> {labels['timezone']}: {payload['timezone']}",
        f"> {labels['requested_date']}: {payload['requestedDate']}",
        f"> {labels['view']}: {day_labels['view']}",
        f"> {payload['dayView']['summary']}",
        "",
        labels["local_tip"],
        "",
    ]
    games = payload.get("games") or []
    if not games:
        lines.append(f"- {labels['no_games']}")
        return "\n".join(lines)
    section_order = [
        ("live", day_labels["live_title"]),
        ("post", day_labels["post_title"]),
        ("pregame", day_labels["pre_title"]),
    ]
    for phase, title in section_order:
        section_games = [game for game in games if game.get("phase") == phase]
        if not section_games:
            continue
        lines.extend([f"## {title}", ""])
        for entry in section_games:
            info = (entry.get("gameContext") or {}).get("info") or {}
            matchup = info.get("matchup") or {}
            team_abbrs = _matchup_team_abbrs(matchup)
            away_abbr = entry["teams"]["away"]["abbr"]
            home_abbr = entry["teams"]["home"]["abbr"]
            away_score = (entry["teams"]["away"] or {}).get("score")
            home_score = (entry["teams"]["home"] or {}).get("score")
            text = format_matchup_display(away_abbr, home_abbr, lang=lang, zh_locale=zh_locale, away_score=away_score, home_score=home_score)
            lines.append(f"### {text}")
            info_parts: list[str] = []
            if info.get("startTimeLocal"):
                info_parts.append(f"{labels['start_time']}: {info['startTimeLocal']}")
            if info.get("venue"):
                info_parts.append(f"{labels['venue']}: {info['venue']}")
            if info_parts:
                lines.append(f"- {'，'.join(info_parts) if lang == 'zh' else ' | '.join(info_parts)}")
            card = entry.get("card") or {}
            if phase == "pregame":
                injuries = (card.get("injuries") or {}).get("featuredByTeam") or {}
                for abbr in (away_abbr, home_abbr):
                    items = injuries.get(abbr) or []
                    if items:
                        localized = [localize_player_line(item, lang) for item in items[:2]]
                        prefix = "伤病重点" if lang == "zh" else "Injury watch"
                        lines.append(f"- {_display_team(abbr, lang, zh_locale)} {prefix}: {'; '.join(localized)}")
                team_form = card.get("teamForm") or {}
                for abbr in (away_abbr, home_abbr):
                    snapshot = team_form.get(abbr) or {}
                    if not snapshot:
                        continue
                    recent = (snapshot.get("recentForm") or {}).get("record") or "N/A"
                    rest_days = (snapshot.get("schedule") or {}).get("restDays")
                    rest_text = labels["pending"] if rest_days is None else str(rest_days)
                    lines.append(f"- {_narrative_team_form(_display_team(abbr, lang, zh_locale), recent, rest_text, lang)}")
                prediction = card.get("prediction") or {}
                if prediction.get("summary"):
                    localized_prediction = _localize_team_mentions(prediction["summary"], lang=lang, zh_locale=zh_locale, team_abbrs=team_abbrs)
                    lines.append(f"- {day_labels['prediction']}: {localized_prediction}")
                if prediction.get("keyMatchup"):
                    key_matchup = _localize_team_mentions(prediction["keyMatchup"], lang=lang, zh_locale=zh_locale, team_abbrs=team_abbrs)
                    lines.append(f"- {'关键对位' if lang == 'zh' else 'Key matchup'}: {key_matchup}")
                if card.get("summary") and not prediction.get("summary"):
                    _append_unique_line(
                        lines,
                        _localize_team_mentions(card["summary"], lang=lang, zh_locale=zh_locale, team_abbrs=team_abbrs),
                    )
            elif phase == "live":
                live_state = card.get("liveState") or {}
                momentum = card.get("momentum") or {}
                lineups = card.get("lineups") or {}
                if live_state.get("displayClock") or live_state.get("period"):
                    if lang == "zh":
                        lines.append(f"- 比赛进程：第 {live_state.get('period') or '?'} 节，{labels['clock']} {live_state.get('displayClock') or labels['pending']}")
                    else:
                        lines.append(
                            f"- The game is in the {_ordinal_period(live_state.get('period'))} quarter with {live_state.get('displayClock') or labels['pending']} on the clock."
                        )
                if momentum.get("trend"):
                    _append_unique_line(
                        lines,
                        _localize_team_mentions(momentum["trend"], lang=lang, zh_locale=zh_locale, team_abbrs=team_abbrs),
                    )
                if live_state.get("latestPlay"):
                    latest_play = _narrative_latest_play(live_state["latestPlay"], lang)
                    lines.append(f"- {day_labels['latest_play']}: {latest_play}")
                full_stats = card.get("fullStats") or {}
                players, _ = _build_live_player_display(full_stats=full_stats, lineups=lineups, matchup=matchup, limit=3, prioritize_starters=True)
                for abbr in (away_abbr, home_abbr):
                    player_lines = [
                        render_compact_player_stat_line(player, lang=lang, include_secondary=False, include_shooting=False)
                        for player in (players.get(abbr) or [])
                    ]
                    player_lines = [line for line in player_lines if line]
                    if player_lines:
                        team_name = _display_team(abbr, lang, zh_locale)
                        heading = f"{team_name}主要输出" if lang == "zh" else f"{team_name} key contributions"
                        _append_team_player_block(lines, heading, player_lines)
                if card.get("summary"):
                    _append_unique_line(
                        lines,
                        _localize_team_mentions(card["summary"], lang=lang, zh_locale=zh_locale, team_abbrs=team_abbrs),
                    )
            else:
                if card.get("summary"):
                    _append_unique_line(
                        lines,
                        _localize_team_mentions(card["summary"], lang=lang, zh_locale=zh_locale, team_abbrs=team_abbrs),
                    )
                lineups = card.get("lineups") or {}
                full_stats = card.get("fullStats") or {}
                starters_line = _day_starters_line(lineups=lineups, matchup=matchup, lang=lang, zh_locale=zh_locale)
                if starters_line:
                    lines.append(f"- {starters_line}")
                for player_line in _day_key_player_lines(
                    full_stats=full_stats,
                    lineups=lineups,
                    matchup=matchup,
                    lang=lang,
                    zh_locale=zh_locale,
                    limit=2,
                ):
                    lines.append(f"- {player_line}")
                for totals_line in _day_team_totals_lines(full_stats=full_stats, matchup=matchup, lang=lang, zh_locale=zh_locale):
                    lines.append(f"- {totals_line}")
                if card.get("reasons"):
                    localized_reasons = [
                        _localize_team_mentions(_localize_analysis_reason(reason, lang), lang=lang, zh_locale=zh_locale, team_abbrs=team_abbrs)
                        for reason in (card.get("reasons") or [])[:2]
                    ]
                    if localized_reasons:
                        lines.append(f"- {'关键依据' if lang == 'zh' else 'Key reasons'}: {' / '.join(localized_reasons)}")
                if card.get("turningPoint"):
                    localized_turning_point = _localize_team_mentions(card["turningPoint"], lang=lang, zh_locale=zh_locale, team_abbrs=team_abbrs)
                    lines.append(f"- {day_labels['turning_point']}: {_narrative_turning_point(localized_turning_point, lang)}")
            lines.append("")
    return "\n".join(lines).rstrip()


def render_live_scene_markdown(scene: dict[str, Any]) -> str:
    report = scene["report"]
    labels = report["labels"]
    phase_labels = _phase_labels(report["lang"])
    zh_locale = report.get("zhLocale")
    live = scene.get("live") or {}
    info = live.get("info") or {}
    matchup = info.get("matchup") or {}
    team_abbrs = _matchup_team_abbrs(matchup)
    lineups = live.get("lineups") or {}
    injuries = live.get("injuries") or {}
    live_state = live.get("liveState") or {}
    momentum = live.get("momentum") or {}
    game_context = scene["game"].get("gameContext") or {}
    full_stats = game_context.get("fullStats") or {"available": False, "teams": {}, "players": {}}
    player_focus = scene.get("playerFocus")
    selected_players, _ = _build_live_player_display(full_stats=full_stats, lineups=lineups, matchup=matchup, limit=5)
    lines = [
        f"# {phase_labels['live_title']} ({report['requestedDate']})",
        f"> {labels['timezone']}: {report['timezone']}",
        f"> {labels['requested_date']}: {report['requestedDate']}",
        f"> {labels['view']}: game",
        f"> {labels['filter_team']}: {report['teamFilter']}",
        "",
        labels["local_tip"],
        "",
    ]
    lines.extend(_render_info_section(info, labels, phase_labels, zh_locale=zh_locale))
    lines.extend(_render_lineups_section(lineups, game_context.get("seasonAverages") or {}, matchup, labels, phase_labels, zh_locale=zh_locale))
    lines.extend(_render_injuries_section(injuries, matchup, labels, phase_labels, zh_locale=zh_locale, active_players=lineups.get("activeParticipants") or []))
    lines.append(f"## {phase_labels['live_flow']}")
    if live.get("summary"):
        localized_summary = _localize_team_mentions(live["summary"], lang=report["lang"], zh_locale=zh_locale, team_abbrs=team_abbrs)
        lines.append(f"- {labels['analysis_summary']}: {localized_summary}")
    if momentum.get("trend"):
        localized_trend = _localize_team_mentions(momentum["trend"], lang=report["lang"], zh_locale=zh_locale, team_abbrs=team_abbrs)
        lines.append(f"- {labels['analysis_trend']}: {localized_trend}")
    if live_state.get("displayClock"):
        lines.append(f"- {labels['clock']}: {live_state['displayClock']}")
    if live_state.get("period"):
        period_label = "当前节次" if report["lang"] == "zh" else "Current Period"
        lines.append(f"- {period_label}: {live_state['period']}")
    if live_state.get("playTimeline"):
        latest_play = (live_state.get("playTimeline") or [])[-1]
        latest_clock = " ".join(part for part in (f"P{latest_play.get('period')}" if latest_play.get("period") else "", latest_play.get("clock") or "") if part).strip()
        latest_text = latest_play.get("text") or latest_play.get("shortDescription") or ""
        if latest_text:
            prefix = f"{latest_clock} " if latest_clock else ""
            latest_play_label = "最新回合" if report["lang"] == "zh" else "Latest Play"
            lines.append(f"- {latest_play_label}: {prefix}{latest_text}".strip())
    if live_state.get("winProbabilityTimeline"):
        latest_win_probability = (live_state.get("winProbabilityTimeline") or [])[-1]
        home_probability = latest_win_probability.get("homeWinPercentage")
        if home_probability is not None:
            home_probability_label = "主队实时胜率" if report["lang"] == "zh" else "Home Win Probability"
            lines.append(f"- {home_probability_label}: {home_probability:.0%}")
    if scene.get("analysis", {}).get("turningPoint"):
        localized_turning_point = _localize_team_mentions(scene["analysis"]["turningPoint"], lang=report["lang"], zh_locale=zh_locale, team_abbrs=team_abbrs)
        lines.append(f"- {labels['analysis_turning_point']}: {localized_turning_point}")
    if momentum.get("reasons"):
        localized_reasons = [
            _localize_team_mentions(reason, lang=report["lang"], zh_locale=zh_locale, team_abbrs=team_abbrs)
            for reason in (momentum.get("reasons") or [])
        ]
        lines.append(f"- {labels['analysis_reasons']}: {' / '.join(localized_reasons[:2])}")
    lines.append("")
    lines.extend(_render_team_totals_section(full_stats, matchup, labels, phase_labels, zh_locale=zh_locale))
    lines.extend(_render_key_player_lines_section({"players": selected_players}, matchup, labels, phase_labels, limit=5, player_focus=player_focus, zh_locale=zh_locale))
    if scene["digest"]["plays"]:
        lines.extend([f"## {phase_labels['play_digest']}", ""])
        if scene["digest"].get("recentRun"):
            recent_run = _localize_team_mentions(scene["digest"]["recentRun"], lang=report["lang"], zh_locale=zh_locale, team_abbrs=team_abbrs)
            lines.append(f"- {recent_run}")
        for item in scene["digest"]["plays"][:8]:
            lines.append(f"- {item}")
        lines.append("")
    localized_summary = _localize_team_mentions(live.get("summary") or phase_labels["none"], lang=report["lang"], zh_locale=zh_locale, team_abbrs=team_abbrs)
    _append_summary_section_if_needed(
        lines,
        title=phase_labels["summary"],
        summary=localized_summary,
        none_label=phase_labels["none"],
        already_shown=_localize_team_mentions(live.get("summary"), lang=report["lang"], zh_locale=zh_locale, team_abbrs=team_abbrs),
    )
    _append_provenance_lines(lines, scene)
    return "\n".join(lines)


def render_postgame_scene_markdown(scene: dict[str, Any]) -> str:
    report = scene["report"]
    labels = report["labels"]
    phase_labels = _phase_labels(report["lang"])
    lang = report["lang"]
    zh_locale = report.get("zhLocale")
    postgame = scene.get("postgame") or {}
    info = postgame.get("info") or {}
    matchup = info.get("matchup") or {}
    team_abbrs = _matchup_team_abbrs(matchup)
    lineups = postgame.get("lineups") or {}
    injuries = postgame.get("injuries") or {}
    full_stats = postgame.get("fullStats") or {"available": False, "teams": {}, "players": {}}
    player_focus = scene.get("playerFocus")
    lines = [
        f"# {phase_labels['post_title']} ({report['requestedDate']})",
        f"> {labels['timezone']}: {report['timezone']}",
        f"> {labels['requested_date']}: {report['requestedDate']}",
        f"> {labels['view']}: game",
        f"> {labels['filter_team']}: {report['teamFilter']}",
        "",
        labels["local_tip"],
        "",
    ]
    lines.extend(_render_info_section(info, labels, phase_labels, zh_locale=zh_locale))
    lines.extend(_render_post_starters_section(lineups, matchup, phase_labels, lang=lang, zh_locale=zh_locale))
    lines.append(f"## {phase_labels['post_flow']}")
    if postgame.get("summary"):
        lines.append(f"- {labels['analysis_summary']}: {postgame['summary']}")
    if scene.get("analysis", {}).get("trend"):
        lines.append(f"- {labels['analysis_trend']}: {scene['analysis']['trend']}")
    if scene.get("analysis", {}).get("reasons"):
        localized_reasons = [_localize_analysis_reason(reason, lang) for reason in (scene.get("analysis", {}).get("reasons") or [])]
        lines.append(f"- {labels['analysis_reasons']}: {' / '.join(localized_reasons[:2])}")
    lines.append("")
    lines.extend(_render_post_key_performances_section(full_stats, lineups, matchup, phase_labels, lang=lang, player_focus=player_focus, zh_locale=zh_locale))
    lines.extend(_render_post_team_totals_section(full_stats, matchup, phase_labels, lang=lang, zh_locale=zh_locale))
    lines.extend(_render_injuries_section(injuries, matchup, labels, phase_labels, zh_locale=zh_locale))
    localized_turning_point = _localize_team_mentions(postgame.get("turningPoint") or phase_labels["none"], lang=lang, zh_locale=zh_locale, team_abbrs=team_abbrs)
    lines.extend([f"## {phase_labels['turning_point']}", "", f"- {localized_turning_point}", ""])
    localized_summary = _localize_team_mentions(postgame.get("summary") or phase_labels["none"], lang=lang, zh_locale=zh_locale, team_abbrs=team_abbrs)
    _append_summary_section_if_needed(
        lines,
        title=phase_labels["summary"],
        summary=localized_summary,
        none_label=phase_labels["none"],
        already_shown=_localize_team_mentions(postgame.get("summary"), lang=lang, zh_locale=zh_locale, team_abbrs=team_abbrs),
    )
    _append_provenance_lines(lines, scene)
    return "\n".join(lines)


def harden_game_injuries(game: dict[str, Any], *, tz: str | None) -> None:
    reference_time = _reference_now(tz)
    game.setdefault("injuryMeta", {})
    game.setdefault("injuryItems", {})
    merged_injuries: dict[str, list[str]] = {}
    resolved_injuries: list[tuple[str, str, dict[str, Any]]] = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_map = {
            executor.submit(
                resolve_team_injury_sources,
                team_abbr=game[side]["abbr"],
                team_id=game[side].get("id") or provider_team_id(game[side]["abbr"], "espn"),
                team_display_name=game[side].get("displayName") or "",
                summary_lines=(game.get("injuries") or {}).get(game[side]["abbr"], []),
                start_time_utc=game.get("startTimeUtc") or "",
                away_abbr=game["away"]["abbr"],
                home_abbr=game["home"]["abbr"],
                reference_time=reference_time,
            ): side
            for side in ("away", "home")
        }
        for future in as_completed(future_map):
            side = future_map[future]
            team = game[side]
            abbr = team["abbr"]
            resolved_injuries.append((side, abbr, future.result()))
    for side, abbr, resolution in resolved_injuries:
        game["injuryItems"][abbr] = [dict(item) for item in resolution["items"]]
        merged_injuries[abbr] = [
            " - ".join(
                part
                for part in (
                    item.get("playerName"),
                    item.get("status"),
                    item.get("detail"),
                )
                if part
            )
            for item in resolution["items"]
        ]
        game["injuryMeta"][abbr] = {
            "primarySource": resolution["primarySource"],
            "sources": resolution["sources"],
            "reportDateTime": resolution["reportDateTime"],
            "provisional": resolution["provisional"],
        }
    game["injuries"] = merged_injuries


def finalize_scene_game(
    *,
    report: dict[str, Any],
    game: dict[str, Any],
    lang: str,
    analysis_mode: str,
    intent: str,
    scope: str = "single",
    include_full_stats: bool = True,
    include_context_enrichment: bool = True,
) -> dict[str, Any]:
    game["requestedDate"] = report["requestedDate"]
    roster_snapshots: dict[str, Any] = {}
    if include_context_enrichment:
        harden_game_injuries(game, tz=report.get("timezone"))
        roster_snapshots = fetch_game_rosters(game)
        game = apply_roster_guard(game, roster_snapshots, lang=lang)
    sources = ["espn"]
    freshness = "fresh"
    fallback_level = "none"
    should_refresh_nba_live = (
        analysis_mode in {"live", "post", "auto"}
        and (
            game.get("statusState") == "in"
            or not game.get("playTimeline")
            or not any((game.get("keyPlayers") or {}).values())
        )
    )
    if should_refresh_nba_live:
        augment_meta = augment_game_with_nba_live(game, requested_date=report["requestedDate"])
        if augment_meta.get("source"):
            sources.append("nba_live")
            freshness = augment_meta.get("dataFreshness", freshness)
            fallback_level = augment_meta.get("fallbackLevel", fallback_level)
            if include_context_enrichment:
                game = apply_roster_guard(game, roster_snapshots, lang=lang)
    team_schedule_payloads = game.get("teamSchedulePayloads") or {}
    if include_full_stats:
        if include_context_enrichment:
            with ThreadPoolExecutor(max_workers=2) as executor:
                full_stats_future = executor.submit(build_full_stats, game, allowed_names=set(game.get("verifiedPlayers") or []))
                team_averages_future = executor.submit(_team_player_averages_for_game, game)
                game["fullStats"] = full_stats_future.result()
                team_player_averages = team_averages_future.result()
        else:
            game["fullStats"] = build_full_stats(game, allowed_names=set(game.get("verifiedPlayers") or []))
            team_player_averages = {}
        _sync_full_stats_scoreboard(game)
    else:
        team_player_averages = _team_player_averages_for_game(game)
        game["fullStats"] = {
            "available": False,
            "source": "unavailable",
            "teams": {},
            "players": {},
        }
    game["teamPlayerAverages"] = team_player_averages
    if include_context_enrichment:
        attach_season_averages(game, team_averages=team_player_averages)
        game["context"] = {
            "teamForm": build_team_form_context(game),
            "headToHead": build_head_to_head_context(
                game,
                away_schedule=(
                    team_schedule_payloads.get(game["away"]["abbr"])
                    if team_schedule_payloads.get(game["away"]["abbr"]) is not None
                    else _team_schedule_payload(game["away"].get("id"))
                ),
                home_schedule=(
                    team_schedule_payloads.get(game["home"]["abbr"])
                    if team_schedule_payloads.get(game["home"]["abbr"]) is not None
                    else _team_schedule_payload(game["home"].get("id"))
                ),
            ),
        }
    else:
        game["context"] = {
            "teamForm": {"available": False, "source": "deferred_live_fast_path"},
            "headToHead": {"available": False, "source": "deferred_live_fast_path"},
        }
    game["meta"] = {
        "sections": {
            "analysis": {
                "sources": sources[:],
                "fallbackLevel": fallback_level,
            },
            "context": {
                "teamForm": {
                    "source": (
                        "espn_summary+espn_team_statistics+espn_team_schedule"
                        if include_context_enrichment
                        else "deferred_live_fast_path"
                    )
                },
                "headToHead": {"source": (game["context"]["headToHead"].get("source") or "unavailable")},
            },
            "fullStats": {
                "source": game["fullStats"].get("source") or "unavailable",
            },
        }
    }
    game["gameContext"] = build_game_context(game)
    analysis = build_analysis(game, analysis_mode, report["labels"])
    if game.get("forceFallbackMatchup") and game.get("fallbackMatchup"):
        analysis["keyMatchup"] = game["fallbackMatchup"]
    elif not analysis.get("keyMatchup") and game.get("fallbackMatchup"):
        analysis["keyMatchup"] = game["fallbackMatchup"]
    digest = build_play_digest(game, lang=lang)
    scene = {
        "intent": intent,
        "scope": scope,
        "report": report,
        "game": game,
        "analysis": analysis,
        "digest": digest,
        "sources": sources,
        "fallbackLevel": fallback_level,
        "dataFreshness": freshness,
    }
    phase = analysis_mode if analysis_mode == "live" else (analysis.get("mode") or analysis_mode)
    if phase == "pregame":
        scene["pregame"] = build_pregame_view(game, analysis)
    elif phase == "live":
        scene["live"] = build_live_view(game, analysis)
    elif phase == "post":
        scene["postgame"] = build_postgame_view(game, analysis)
    return scene


def _team_schedule_payload(team_id: str | None) -> dict[str, Any]:
    if not team_id:
        return {}
    try:
        return fetch_team_schedule(team_id)["data"]
    except NBAReportError:
        return {}


def build_game_scene(
    *,
    tz: str | None,
    date_text: str | None,
    team: str,
    lang: str,
    analysis_mode: str,
    zh_locale: str | None = None,
) -> dict[str, Any]:
    requested_mode = analysis_mode
    report_detail_level = "live_fast" if requested_mode == "live" else "full"
    report = build_scene_report(
        tz=tz,
        date_text=date_text,
        team=team,
        lang=lang,
        zh_locale=zh_locale,
        detail_level=report_detail_level,
    )
    game = report["games"][0]
    effective_mode = analysis_mode
    if effective_mode == "auto":
        effective_mode = {"pre": "pregame", "in": "live", "post": "post"}.get(game.get("statusState"), "pregame")
    include_full_stats = effective_mode != "pregame"
    include_context_enrichment = analysis_mode != "live"
    intent = analysis_mode if analysis_mode in {"pregame", "live", "post"} else "scene"
    return finalize_scene_game(
        report=report,
        game=game,
        lang=lang,
        analysis_mode=analysis_mode,
        intent=intent,
        include_full_stats=include_full_stats,
        include_context_enrichment=include_context_enrichment,
    )


def _pregame_labels(lang: str) -> dict[str, str]:
    if lang == "zh":
        return {
            "title_single": "NBA 赛前前瞻",
            "title_multi": "NBA 多场赛前前瞻",
            "info": "比赛信息",
            "lineups": "阵容与关键球员",
            "injuries": "伤病情况",
            "team_form": "球队状态",
            "prediction": "预测分析",
            "summary": "总结",
            "starters_pending": "首发尚未公布或当前免费数据源不可确认。",
            "none": "无",
            "all_games_none": "该日期没有可用的赛前比赛。",
        }
    return {
        "title_single": "NBA Pregame Preview",
        "title_multi": "NBA Multi-Game Pregame Preview",
        "info": "Game Info",
        "lineups": "Lineups and Key Players",
        "injuries": "Injuries",
        "team_form": "Team Form",
        "prediction": "Prediction",
        "summary": "Summary",
        "starters_pending": "Starting lineups are not yet confirmed or cannot be confirmed from the free data source.",
        "none": "None",
        "all_games_none": "No scheduled pregame matchups were found for the requested date.",
    }


def _format_average_line(stats: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in ("PTS", "REB", "AST", "STL", "BLK"):
        value = stats.get(key)
        if value is None:
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            parts.append(f"{key} {value}")
            continue
        parts.append(f"{key} {int(number) if number.is_integer() else number:.1f}".replace(".0", ""))
    return ", ".join(parts)


def _localize_analysis_reason(reason: str, lang: str) -> str:
    text = str(reason or "")
    if lang != "zh" or not text:
        return text
    replacements = (
        (r"(\d+(?:\.\d+)?)\s+PTS\b", r"\1分"),
        (r"(\d+(?:\.\d+)?)\s+REB\b", r"\1板"),
        (r"(\d+(?:\.\d+)?)\s+AST\b", r"\1助"),
        (r"\s+\|\s+", " / "),
    )
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    return text


def render_pregame_scene_markdown(scene: dict[str, Any]) -> str:
    report = scene["report"]
    game = scene["game"]
    pregame = scene.get("pregame") or {}
    labels = _pregame_labels(report["lang"])
    lang = report["lang"]
    zh_locale = report.get("zhLocale")
    team_abbrs = [game["away"]["abbr"], game["home"]["abbr"]]
    lines = [
        f"# {labels['title_single']} ({report['requestedDate']})",
        f"> {report['labels']['timezone']}: {report['timezone']}",
        f"> {report['labels']['requested_date']}: {report['requestedDate']}",
        f"> {report['labels']['filter_team']}: {report['teamFilter']}",
        "",
        f"## {labels['info']}",
        "",
        *render_team_lines(game, report["labels"]),
        "",
        f"## {labels['lineups']}",
    ]
    lineups = pregame.get("lineups") or {}
    if lineups.get("startersConfirmed"):
        for abbr in (game["away"]["abbr"], game["home"]["abbr"]):
            starters = (lineups.get("starters") or {}).get(abbr) or []
            rendered = ", ".join(localize_player_list(starters, lang)) if starters else labels["none"]
            lines.append(f"- {_display_team(abbr, lang, zh_locale)} starters: {rendered}")
    else:
        lines.append(f"- {labels['starters_pending']}")
    season_averages = (game.get("gameContext") or {}).get("seasonAverages") or {}
    for abbr in (game["away"]["abbr"], game["home"]["abbr"]):
        key_players = (lineups.get("keyPlayers") or {}).get(abbr) or []
        if not key_players:
            continue
        lines.append(f"- {_display_team(abbr, lang, zh_locale)}:")
        for line in key_players[:3]:
            primary = extract_primary_name(line)
            averages = _format_average_line((season_averages.get(abbr) or {}).get(primary) or {})
            suffix = f" ({averages})" if averages else ""
            lines.append(f"  - {localize_player_line(line, lang)}{suffix}")
    lines.extend(["", f"## {labels['injuries']}"])
    injuries = pregame.get("injuries") or {}
    for abbr in (game["away"]["abbr"], game["home"]["abbr"]):
        items = (injuries.get("featuredByTeam") or {}).get(abbr) or (injuries.get("byTeam") or {}).get(abbr) or []
        localized = [localize_player_line(item, lang) for item in items]
        lines.append(f"- {_display_team(abbr, lang, zh_locale)}: {'; '.join(localized) if localized else labels['none']}")
    lines.extend(["", f"## {labels['team_form']}"])
    team_form = pregame.get("teamForm") or {}
    for abbr in (game["away"]["abbr"], game["home"]["abbr"]):
        snapshot = team_form.get(abbr) or {}
        if not snapshot:
            continue
        recent = (snapshot.get("recentForm") or {}).get("record") or "N/A"
        rest_days = (snapshot.get("schedule") or {}).get("restDays")
        rest_text = report["labels"]["pending"] if rest_days is None else str(rest_days)
        injury_count = (snapshot.get("injuries") or {}).get("count")
        base_sentence = _narrative_team_form(_display_team(abbr, lang, zh_locale), recent, rest_text, lang)
        if lang == "zh":
            suffix = f" 伤病人数 {injury_count if injury_count is not None else labels['none']}。"
        else:
            suffix = f" Injury count: {injury_count if injury_count is not None else labels['none']}."
        lines.append(f"- {base_sentence[:-1]}，{suffix.lstrip()}" if lang == "zh" else f"- {base_sentence[:-1]}. {suffix.strip()}")
    prediction = pregame.get("prediction") or {}
    lines.extend(["", f"## {labels['prediction']}"])
    if prediction.get("summary"):
        lines.append(f"- {report['labels']['analysis_summary']}: {prediction['summary']}")
    if prediction.get("trend"):
        lines.append(f"- {report['labels']['analysis_trend']}: {prediction['trend']}")
    if prediction.get("keyMatchup"):
        lines.append(f"- {report['labels']['analysis_key_matchup']}: {prediction['keyMatchup']}")
    if prediction.get("reasons"):
        lines.append(f"- {report['labels']['analysis_reasons']}: {' / '.join((prediction.get('reasons') or [])[:2])}")
    localized_summary = _localize_team_mentions(pregame.get("summary") or labels["none"], lang=lang, zh_locale=zh_locale, team_abbrs=team_abbrs)
    _append_summary_section_if_needed(
        lines,
        title=labels["summary"],
        summary=localized_summary,
        none_label=labels["none"],
        already_shown=_localize_team_mentions(prediction.get("summary"), lang=lang, zh_locale=zh_locale, team_abbrs=team_abbrs),
    )
    _append_provenance_lines(lines, scene)
    return "\n".join(lines)


def _story_key_for_game(game: dict[str, Any]) -> tuple[str, str]:
    return str((game.get("away") or {}).get("abbr") or ""), str((game.get("home") or {}).get("abbr") or "")


def _apply_prefetched_story(scene: dict[str, Any], official_story: dict[str, Any] | None) -> None:
    story = official_story or {}
    if not story.get("available"):
        return
    game = scene.get("game") or {}
    game["officialStory"] = story
    game_context = game.get("gameContext") or {}
    game_context["officialStory"] = story
    game["gameContext"] = game_context
    analysis = scene.get("analysis") or {}
    signals = analysis.get("signals") or {}
    signals["storySignals"] = story.get("summarySignals") or []
    brief = _story_brief(story, phase=str(analysis.get("mode") or "pregame"))
    if brief:
        signals["storyBrief"] = brief
    analysis["signals"] = signals
    scene["analysis"] = analysis


def build_pregame_collection(
    *,
    tz: str | None,
    date_text: str | None,
    lang: str,
    matchups: list[dict[str, str]] | None = None,
    zh_locale: str | None = None,
) -> dict[str, Any]:
    report = build_scene_report(tz=tz, date_text=date_text, team=None, lang=lang, zh_locale=zh_locale)
    scenes: list[dict[str, Any]] = []
    scope = "multi_all"
    pregame_game_count = sum(1 for game in report["games"] if game.get("statusState") == "pre")
    enable_budget = bool(matchups and len(matchups) > 1) or (not matchups and pregame_game_count > 1)
    with _pregame_multi_budget_scope(enable_budget):
        if matchups:
            scope = "multi_explicit"
            for matchup in matchups:
                resolved = resolve_requested_game(tz=tz, date_text=date_text, team=matchup["team"], opponent=matchup["opponent"])
                resolved_date = str(resolved.get("requestedDate") or report["requestedDate"])
                scene = build_game_scene(tz=tz, date_text=resolved_date, team=matchup["team"], lang=lang, analysis_mode="pregame", zh_locale=zh_locale)
                if not any(existing["game"]["eventId"] == scene["game"]["eventId"] for existing in scenes):
                    scenes.append(scene)
        else:
            for game in report["games"]:
                if game.get("statusState") != "pre":
                    continue
                scene = build_game_scene(tz=tz, date_text=report["requestedDate"], team=game["away"]["abbr"], lang=lang, analysis_mode="pregame", zh_locale=zh_locale)
                scenes.append(scene)
    payload = {
        "intent": "pregame",
        "scope": scope,
        "requestedDate": report["requestedDate"],
        "timezone": report["timezone"],
        "lang": lang,
        "zhLocale": report.get("zhLocale"),
        "games": scenes,
    }
    return payload


def render_pregame_collection_markdown(payload: dict[str, Any]) -> str:
    labels = _pregame_labels(payload["lang"])
    lang = payload["lang"]
    zh_locale = payload.get("zhLocale")
    lines = [
        f"# {labels['title_multi']} ({payload['requestedDate']})",
        f"> {'请求方时区' if lang == 'zh' else 'Requestor Timezone'}: {payload['timezone']}",
        f"> {'请求日期' if lang == 'zh' else 'Requested Date'}: {payload['requestedDate']}",
        "",
    ]
    if not payload["games"]:
        lines.append(f"- {labels['all_games_none']}")
        return "\n".join(lines)
    for scene in payload["games"]:
        game = scene["game"]
        pregame = scene.get("pregame") or {}
        prediction = pregame.get("prediction") or {}
        team_abbrs = [game["away"]["abbr"], game["home"]["abbr"]]
        lines.append(f"## {format_matchup_display(game['away']['abbr'], game['home']['abbr'], lang=lang, zh_locale=zh_locale)}")
        lines.append(f"- {'时间' if lang == 'zh' else 'Time'}: {game['startTimeLocal']}")
        if game.get("venue"):
            lines.append(f"- {'球馆' if lang == 'zh' else 'Venue'}: {game['venue']}")
        for abbr in (game["away"]["abbr"], game["home"]["abbr"]):
            snapshot = (pregame.get("teamForm") or {}).get(abbr) or {}
            if snapshot:
                recent = (snapshot.get("recentForm") or {}).get("record") or "N/A"
                injury_count = (snapshot.get("injuries") or {}).get("count")
                rest_days = (snapshot.get("schedule") or {}).get("restDays")
                rest_text = ("待确认" if lang == "zh" else "Pending") if rest_days is None else str(rest_days)
                form_sentence = _narrative_team_form(_display_team(abbr, lang, zh_locale), recent, rest_text, lang)
                extra = f"伤病人数 {injury_count if injury_count is not None else labels['none']}。" if lang == "zh" else f"Injury count: {injury_count if injury_count is not None else labels['none']}."
                lines.append(f"- {form_sentence} {extra}" if lang == "en" else f"- {form_sentence[:-1]}，{extra}")
        for abbr in (game["away"]["abbr"], game["home"]["abbr"]):
            injuries = pregame.get("injuries") or {}
            items = (injuries.get("compactByTeam") or {}).get(abbr) or (injuries.get("featuredByTeam") or {}).get(abbr) or (injuries.get("byTeam") or {}).get(abbr) or []
            if items:
                localized = [localize_player_line(item, lang) for item in items[:2]]
                if lang == "zh":
                    lines.append(f"- {_display_team(abbr, lang, zh_locale)}的伤病关注点是 {'; '.join(localized)}。")
                else:
                    lines.append(f"- Injury watch for {_display_team(abbr, lang, zh_locale)} centers on {'; '.join(localized)}.")
        if prediction.get("summary"):
            _append_unique_line(lines, _localize_team_mentions(prediction["summary"], lang=lang, zh_locale=zh_locale, team_abbrs=team_abbrs))
        if prediction.get("keyMatchup"):
            key_matchup = _localize_team_mentions(prediction["keyMatchup"], lang=lang, zh_locale=zh_locale, team_abbrs=team_abbrs)
            lines.append(f"- {'关键对位会落在' if lang == 'zh' else 'The matchup should turn on '}{key_matchup}{'' if lang == 'zh' else '.'}")
        localized_prediction_summary = _localize_team_mentions(prediction.get("summary"), lang=lang, zh_locale=zh_locale, team_abbrs=team_abbrs)
        localized_pregame_summary = _localize_team_mentions(pregame.get("summary"), lang=lang, zh_locale=zh_locale, team_abbrs=team_abbrs)
        if localized_pregame_summary and _normalize_comparable_text(localized_pregame_summary) != _normalize_comparable_text(localized_prediction_summary):
            _append_unique_line(lines, localized_pregame_summary)
        lines.append("")
    return "\n".join(lines).rstrip()


def _play_matches_player_focus(play: dict[str, Any], player_focus: str | None) -> bool:
    if not player_focus:
        return True
    focus_identity = normalize_player_identity(player_focus)
    for key in ("playerName", "secondaryPlayerName", "tertiaryPlayerName"):
        if normalize_player_identity(play.get(key)) == focus_identity:
            return True
    return False


def _play_score_suffix(play: dict[str, Any], game: dict[str, Any]) -> str:
    away_score = play.get("awayScore")
    home_score = play.get("homeScore")
    if away_score in (None, "") or home_score in (None, ""):
        return ""
    away_abbr = ((game.get("away") or {}).get("abbr")) or "AWAY"
    home_abbr = ((game.get("home") or {}).get("abbr")) or "HOME"
    return f" ({away_abbr} {away_score}-{home_score} {home_abbr})"


def _render_filtered_play_section(
    scene: dict[str, Any],
    *,
    title: str,
    quarter: int | None = None,
    player_focus: str | None = None,
) -> list[str]:
    lang = scene["report"]["lang"]
    phase_labels = _phase_labels(lang)
    lines = [f"## {title}", ""]
    plays = scene["game"].get("playTimeline") or []
    filtered: list[str] = []
    for play in plays:
        if quarter is not None and int(play.get("period") or 0) != quarter:
            continue
        if not _play_matches_player_focus(play, player_focus):
            continue
        latest_clock = " ".join(
            part
            for part in (
                f"P{play.get('period')}" if play.get("period") else "",
                play.get("clock") or "",
            )
            if part
        ).strip()
        text = str(play.get("text") or play.get("shortDescription") or "").strip()
        if text:
            filtered.append(f"{latest_clock} {text}{_play_score_suffix(play, scene['game'])}".strip())
    if not filtered and quarter is None and not player_focus:
        filtered = list((scene.get("digest") or {}).get("plays") or [])
    if not filtered:
        lines.append(f"- {phase_labels['none']}")
    else:
        if quarter is None and not player_focus and (scene.get("digest") or {}).get("recentRun"):
            matchup = (((scene.get("live") or {}).get("info") or {}).get("matchup") or {})
            team_abbrs = _matchup_team_abbrs(matchup)
            zh_locale = scene["report"].get("zhLocale")
            recent_run = _localize_team_mentions((scene.get("digest") or {}).get("recentRun"), lang=lang, zh_locale=zh_locale, team_abbrs=team_abbrs)
            lines.append(f"- {recent_run}")
        for item in filtered[-8:]:
            lines.append(f"- {item}")
    lines.append("")
    return lines


def _render_scene_focus_markdown(scene: dict[str, Any]) -> str:
    focus_section = scene.get("focusSection")
    if not focus_section:
        return ""
    report = scene["report"]
    labels = report["labels"]
    phase_labels = _phase_labels(report["lang"])
    player_focus = scene.get("playerFocus")
    if scene.get("intent") == "post":
        info = (scene.get("postgame") or {}).get("info") or {}
        matchup = info.get("matchup") or {}
        lines = [
            f"# {phase_labels['post_title']} ({report['requestedDate']})",
            f"> {labels['timezone']}: {report['timezone']}",
            f"> {labels['requested_date']}: {report['requestedDate']}",
            f"> {labels['view']}: game",
            f"> {labels['filter_team']}: {report['teamFilter']}",
            "",
        ]
        lines.extend(_render_info_section(info, labels, phase_labels, zh_locale=report.get("zhLocale")))
        if focus_section == "key_players":
            lines.extend(
                _render_post_key_performances_section(
                    (scene.get("postgame") or {}).get("fullStats") or {"players": {}},
                    (scene.get("postgame") or {}).get("lineups") or {},
                    matchup,
                    phase_labels,
                    lang=report["lang"],
                    player_focus=player_focus,
                    zh_locale=report.get("zhLocale"),
                )
            )
        elif focus_section == "injuries":
            lines.extend(
                _render_injuries_section(
                    (scene.get("postgame") or {}).get("injuries") or {},
                    matchup,
                    labels,
                    phase_labels,
                    zh_locale=report.get("zhLocale"),
                )
            )
        elif focus_section == "fourth_quarter":
            lines.extend(_render_filtered_play_section(scene, title="第四节回合摘要" if report["lang"] == "zh" else "Fourth Quarter Digest", quarter=4, player_focus=player_focus))
        else:
            lines.extend(_render_filtered_play_section(scene, title=phase_labels["play_digest"], player_focus=player_focus))
        _append_provenance_lines(lines, scene)
        return "\n".join(lines)

    info = (scene.get("live") or {}).get("info") or {}
    matchup = info.get("matchup") or {}
    lines = [
        f"# {phase_labels['live_title']} ({report['requestedDate']})",
        f"> {labels['timezone']}: {report['timezone']}",
        f"> {labels['requested_date']}: {report['requestedDate']}",
        f"> {labels['view']}: game",
        f"> {labels['filter_team']}: {report['teamFilter']}",
        "",
    ]
    lines.extend(_render_info_section(info, labels, phase_labels, zh_locale=report.get("zhLocale")))
    if focus_section == "key_players":
        game_context = scene["game"].get("gameContext") or {}
        full_stats = game_context.get("fullStats") or {"available": False, "teams": {}, "players": {}}
        lineups = (scene.get("live") or {}).get("lineups") or {}
        selected_players, _ = _build_live_player_display(full_stats=full_stats, lineups=lineups, matchup=matchup, limit=5)
        lines.extend(
            _render_key_player_lines_section(
                {"players": selected_players},
                matchup,
                labels,
                phase_labels,
                limit=5,
                player_focus=player_focus,
                zh_locale=report.get("zhLocale"),
            )
        )
    elif focus_section == "injuries":
        lines.extend(
            _render_injuries_section(
                (scene.get("live") or {}).get("injuries") or {},
                matchup,
                labels,
                phase_labels,
                zh_locale=report.get("zhLocale"),
            )
        )
    elif focus_section == "fourth_quarter":
        lines.extend(_render_filtered_play_section(scene, title="第四节回合摘要" if report["lang"] == "zh" else "Fourth Quarter Digest", quarter=4, player_focus=player_focus))
    else:
        lines.extend(_render_filtered_play_section(scene, title=phase_labels["play_digest"], player_focus=player_focus))
    _append_provenance_lines(lines, scene)
    return "\n".join(lines)


def render_game_scene_markdown(scene: dict[str, Any]) -> str:
    if scene.get("intent") == "pregame":
        return render_pregame_scene_markdown(scene)
    if scene.get("intent") == "live":
        if scene.get("focusSection"):
            return _render_scene_focus_markdown(scene)
        return render_live_scene_markdown(scene)
    if scene.get("intent") == "post":
        if scene.get("focusSection"):
            return _render_scene_focus_markdown(scene)
        return render_postgame_scene_markdown(scene)
    report = scene["report"]
    game = scene["game"]
    analysis = scene["analysis"]
    labels = report["labels"]
    lines = [
        f"# {labels['title_game']} ({report['requestedDate']})",
        f"> {labels['timezone']}: {report['timezone']}",
        f"> {labels['requested_date']}: {report['requestedDate']}",
        f"> {labels['view']}: game",
        f"> {labels['filter_team']}: {report['teamFilter']}",
        "",
        labels["local_tip"],
        "",
    ]
    lines.extend(render_team_lines(game, labels))
    lines.append("")
    lines.extend(render_detail_blocks(game, labels))
    lines.extend(render_analysis_block(analysis, labels))
    if scene["digest"]["plays"]:
        lines.extend(["", "## 回合摘要" if report["lang"] == "zh" else "## Play Digest", ""])
        for item in scene["digest"]["plays"]:
            lines.append(f"- {item}")
    lines.append("")
    _append_provenance_lines(lines, scene)
    return "\n".join(lines)


def render_day_scene(
    *,
    tz: str | None,
    date_text: str | None,
    lang: str,
    zh_locale: str | None = None,
    phase_filter: str | None = None,
) -> str:
    return render_day_view_markdown(build_day_view(tz=tz, date_text=date_text, lang=lang, zh_locale=zh_locale, phase_filter=phase_filter))


def scene_payload(scene: dict[str, Any]) -> dict[str, Any]:
    game = scene["game"]
    payload = {
        "intent": scene.get("intent") or (scene.get("analysis", {}).get("mode") or "scene"),
        "scope": scene.get("scope") or "single",
        "eventId": game["eventId"],
        "requestedDate": scene["report"]["requestedDate"],
        "timezone": scene["report"]["timezone"],
        "lang": scene["report"]["lang"],
        "zhLocale": scene["report"].get("zhLocale"),
        "statusState": game["statusState"],
        "teams": {
            "away": game["away"],
            "home": game["home"],
        },
        "verifiedPlayers": game.get("verifiedPlayers") or [],
        "rosters": game.get("rosters") or {},
        "analysis": scene["analysis"],
        "digest": scene["digest"],
        "gameContext": game.get("gameContext") or {},
        "context": game.get("context") or {},
        "fullStats": game.get("fullStats") or {"available": False, "teams": {}, "players": {}},
        "meta": game.get("meta") or {"sections": {}},
        "sources": scene["sources"],
        "fallbackLevel": scene["fallbackLevel"],
        "dataFreshness": scene["dataFreshness"],
    }
    if scene.get("pregame"):
        payload["pregame"] = scene["pregame"]
    if scene.get("live"):
        payload["live"] = scene["live"]
    if scene.get("postgame"):
        payload["postgame"] = scene["postgame"]
    return payload
