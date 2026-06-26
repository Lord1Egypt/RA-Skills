#!/usr/bin/env python3
"""Deterministic NBA.com story summarizer for NBA_TR.

The module converts NBA.com game-page story text into short structured
signals. It intentionally avoids copying article bodies into public output.
"""

from __future__ import annotations

import re
from typing import Any


SCORE_RE = re.compile(
    r"(?P<player>[A-Z][A-Za-z.'\u2019-]+(?:\s+[A-Z][A-Za-z.'\u2019-]+){0,3})\s+"
    r"(?:scored|had|finished with)\s+(?:a [^,.;]*? )?(?P<points>\d{1,2})\s+points?",
)
FACTOR_SCORE_RE = re.compile(
    r"(?P<player>[A-Z][A-Za-z.'\u2019-]+(?:\s+[A-Z][A-Za-z.'\u2019-]+){0,3})\s+was one of .*? with\s+(?P<points>\d{1,2})\s+points",
    re.IGNORECASE,
)
PLAY_IN_SEED_RE = re.compile(
    r"(?P<team>[A-Z][A-Za-z.'\u2019& -]+?)\s+come into .*? after knocking off the "
    r"(?P<opp>[A-Z][A-Za-z.'\u2019& -]+?)\s+in the play-?in .*? to earn the No\.?\s*(?P<seed>\d+)\s+seed",
    re.IGNORECASE,
)
PLAY_IN_SCORE_RE = re.compile(
    r"(?P<team>[A-Z][A-Za-z.'\u2019& -]+?)\s+bounced back with a\s+(?P<score>\d{2,3}-\d{2,3})\s+.*?win over the "
    r"(?P<opp>[A-Z][A-Za-z.'\u2019& -]+)",
    re.IGNORECASE,
)
REST_WEEK_RE = re.compile(r"(?P<team>The\s+)?(?P<name>[A-Z][A-Za-z.'\u2019& -]+?)\s+haven't played in a week", re.IGNORECASE)
REPEAT_CHAMP_RE = re.compile(r"(?P<team>The\s+)?(?P<name>[A-Z][A-Za-z.'\u2019& -]+?)\s+are looking to become .*? repeat as champions", re.IGNORECASE)
TOP_SEED_RE = re.compile(
    r"(?P<team>The\s+)?(?P<name>[A-Z][A-Za-z.'\u2019& -]+?)\s+had the best record .*? top seed after winning\s+(?P<wins>\d+)\s+games",
    re.IGNORECASE,
)
UNDERAPP_RE = re.compile(r"(?:So,\s+)?(?:the\s+)?(?P<name>[A-Z][A-Za-z.'\u2019& -]+?),[^.]*?right to feel underappreciated", re.IGNORECASE)
SEED_OPP_RE = re.compile(r"against No\.?\s*(?P<seed>\d+)\s+seed\s+(?P<opp>[A-Z][A-Za-z.'\u2019& -]+)", re.IGNORECASE)
DIFFERENT_LOOK_RE = re.compile(r"(?:each|both)\s+teams?\s+(?:will\s+)?have a different look", re.IGNORECASE)
SPLIT_FOUR_RE = re.compile(r"(?P<a>[A-Z][A-Za-z.'\u2019& -]+?)\s+and\s+(?P<b>[A-Z][A-Za-z.'\u2019& -]+?)\s+split their four games", re.IGNORECASE)
TATUM_RETURN_RE = re.compile(r"(?P<team>[A-Z][A-Za-z.'\u2019& -]+?)\s+.*?after\s+Jayson Tatum returned", re.IGNORECASE)
GEORGE_ABSENCE_RE = re.compile(r"didn't face .*? with Paul George in the lineup|Paul George.*?missed games", re.IGNORECASE)
DEF_RATING_RE = re.compile(
    r"(?:The\s+)?(?P<a>[A-Z][A-Za-z.'\u2019& -]+?)\s+had the NBA's best defensive rating.*?(?P<a_rating>\d{3}\.\d).*?"
    r"while\s+(?:the\s+)?(?P<b>[A-Z][A-Za-z.'\u2019& -]+?)\s+were ninth at\s+(?P<b_rating>\d{3}\.\d)",
    re.IGNORECASE,
)
TURNOVER_POINTS_RE = re.compile(
    r"(?P<team>[A-Z][A-Za-z.'\u2019& -]+?)\s+scored\s+(?P<points>\d{1,2})\s+points off .*? turnovers.*?"
    r"(?P<opp>[A-Z][A-Za-z.'\u2019& -]+?)\s+led the league with\s+(?P<opp_points>\d{1,2}\.\d)",
    re.IGNORECASE,
)
SERIES_RECORD_RE = re.compile(
    r"(?P<team>The\s+)?(?P<name>[A-Z][A-Za-z.'\u2019& -]+?)\s+won\s+(?P<wins>\w+)\s+of\s+the\s+(?P<games>\w+)\s+regular-season matchups",
    re.IGNORECASE,
)
REFERENCE_LIMIT_RE = re.compile(r"will bear little resemblance|sat most of their starters", re.IGNORECASE)
QUESTIONABLE_RE = re.compile(r"(?P<team>[A-Z][A-Za-z.'\u2019& -]+?)\s+was without\s+(?P<players>.+?)\.\s+Both are listed as questionable", re.IGNORECASE)
SHOOTING_EDGE_RE = re.compile(
    r"(?P<team>[A-Z][A-Za-z.'\u2019& -]+?)\s+thrived by hitting\s+(?P<team_pct>\d{1,2}\.\d)%.*?holding\s+the\s+"
    r"(?P<opp>[A-Z][A-Za-z.'\u2019& -]+?)\s+to\s+(?P<opp_pct>\d{1,2}\.\d)%\s+shooting",
    re.IGNORECASE,
)
RUN_RE = re.compile(
    r"(?P<team>[A-Z][A-Za-z.'\u2019& -]+?)\s+(?:broke it open|pulled away|seized control)\s+with\s+(?:a|an)\s+(?P<run>\d{1,2}-\d{1,2})\s+run",
    re.IGNORECASE,
)
NEVER_TRAILED_RE = re.compile(r"(?P<team>[A-Z][A-Za-z.'\u2019& -]+?)\s+never trailed", re.IGNORECASE)
LEAD_BUILD_RE = re.compile(r"building (?:as much as )?a[n]?\s+(?P<lead>\d{1,2})-point lead", re.IGNORECASE)
THREES_MADE_RE = re.compile(r"connected on\s+(?P<count>\d{1,2})\s+3-pointers", re.IGNORECASE)
THREE_POINT_STRUGGLE_RE = re.compile(
    r"(?P<team>[A-Z][A-Za-z.'\u2019& -]+?)\s+(?:was|went)\s+(?P<made>\d{1,2})\s+of\s+(?P<attempts>\d{1,2})\s+from\s+3",
    re.IGNORECASE,
)
SURGE_RE = re.compile(r"went on a\s+(?P<run>\d{1,2}-\d{1,2})\s+surge", re.IGNORECASE)
HALFTIME_LEAD_RE = re.compile(r"(?:extended the advantage to|led)\s+(?P<score>\d{2,3}-\d{2,3})\s+at halftime", re.IGNORECASE)
MINUTES_DEPTH_RE = re.compile(
    r"(?P<count>\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten)\s+(?:[A-Z][A-Za-z.'\u2019& -]+?\s+)?players saw at least\s+(?P<minutes>\d{1,2})\s+minutes",
    re.IGNORECASE,
)
HOME_POSTSEASON_SKID_RE = re.compile(
    r"(?P<team>[A-Z][A-Za-z.'\u2019& -]+?)\s+has dropped\s+(?P<count>\d{1,2})\s+straight home games in the postseason",
    re.IGNORECASE,
)
EARLY_START_RE = re.compile(
    r"led\s+(?P<lead>\d{1,2}-\d{1,2})\s+midway through the first quarter after holding\s+(?P<opp>[A-Z][A-Za-z.'\u2019& -]+?)\s+to\s+"
    r"(?P<made>\d{1,2})-of-(?P<attempts>\d{1,2})\s+shooting with\s+(?P<turnovers>\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+turnovers",
    re.IGNORECASE,
)


def _clean(text: Any) -> str:
    value = re.sub(r"\s+", " ", str(text or "")).strip()
    return re.sub(r"^[A-Z .'-]+\([A-Z]{2}\)\s+", "", value)


def _team_name(value: str) -> str:
    text = re.sub(r"^(?:so,|while|and|but|the|The)\s+", "", str(value or "").strip(), flags=re.IGNORECASE).strip()
    text = re.sub(r"\s+-\s+which\b.*$", "", text, flags=re.IGNORECASE).strip()
    return text


def _looks_like_placeholder_subject(value: str) -> bool:
    token = str(value or "").strip().lower()
    return token in {"who", "they", "it", "he", "she", "we", "i"}


def _number_word(value: str) -> str:
    mapping = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "ten": "10",
    }
    return mapping.get(str(value or "").lower(), str(value or ""))


def _sentences(story: dict[str, Any], game_recap: dict[str, Any] | None) -> list[str]:
    header = story.get("header") or {}
    rows = [header.get("headline") or ""]
    rows.extend(story.get("content") or [])
    recap = game_recap or {}
    rows.extend([recap.get("title") or "", recap.get("excerpt") or ""])
    return [_clean(row) for row in rows if _clean(row)]


def _push(pieces: list[dict[str, Any]], *, theme: str, priority: int, zh: str, en: str) -> None:
    if not zh and not en:
        return
    if any(item.get("theme") == theme or item.get("zh") == zh for item in pieces):
        return
    pieces.append({"theme": theme, "priority": priority, "zh": zh.strip(), "en": en.strip()})


def _join(items: list[str], limit: int) -> str:
    selected = [item.rstrip("。.; ") for item in items if item][:limit]
    if not selected:
        return ""
    return "；".join(selected) + "。"


def _compact(pieces: list[dict[str, Any]], *, lang: str, limit: int = 2) -> str:
    key = "zh" if lang == "zh" else "en"
    return _join([str(piece.get(key) or "") for piece in pieces], limit)


def _extract_pregame(story: dict[str, Any], game_recap: dict[str, Any] | None) -> list[dict[str, Any]]:
    pieces: list[dict[str, Any]] = []
    rows = _sentences(story, game_recap)
    text = " ".join(rows)
    for row in rows:
        lowered = row.lower()
        if "after halftime" in lowered and ("shooting efficiency" in lowered or "efficiency" in lowered):
            _push(
                pieces,
                theme="post_halftime_efficiency",
                priority=100,
                zh="半场后的投篮效率差距成了比赛拉开的主要原因",
                en="The recap treats the post-halftime shooting-efficiency gap as the main separator",
            )
        if match := PLAY_IN_SEED_RE.search(row):
            team = _team_name(match.group("team"))
            opp = _team_name(match.group("opp"))
            seed = match.group("seed")
            _push(
                pieces,
                theme="play_in_path",
                priority=100,
                zh=f"{team} 刚在附加赛击败 {opp}，以西部 {seed} 号种子身份进入首轮",
                en=f"{team} just beat {opp} in the play-in and entered the first round as the No. {seed} seed",
            )
        if match := PLAY_IN_SCORE_RE.search(row):
            team = _team_name(match.group("team"))
            opp = _team_name(match.group("opp"))
            score = match.group("score")
            _push(
                pieces,
                theme="play_in_bounce_back",
                priority=82,
                zh=f"{team} 在附加赛首战失去大比分领先后反弹，以 {score} 击败 {opp}",
                en=f"{team} recovered from a blown play-in lead by beating {opp} {score}",
            )
        if match := REST_WEEK_RE.search(row):
            team = _team_name(match.group("name"))
            _push(
                pieces,
                theme="rest_edge",
                priority=96,
                zh=f"{team} 进入系列赛首战前已经休息一周，赛程体能背景明显不同",
                en=f"{team} had a full week off before Game 1, creating a clear rest-context difference",
            )
        if match := (SCORE_RE.search(row) or FACTOR_SCORE_RE.search(row)):
            player = match.group("player").strip()
            points = match.group("points")
            if "advancing" in row.lower() or "victory" in row.lower() or "win" in row.lower():
                _push(
                    pieces,
                    theme="play_in_standout",
                    priority=94,
                    zh=f"{player} 上一场拿到 {points} 分，是球队附加赛突围的重要推手",
                    en=f"{player}'s {points}-point game was a major driver of the play-in advance",
                )
        if match := REPEAT_CHAMP_RE.search(row):
            team = _team_name(match.group("name"))
            _push(
                pieces,
                theme="repeat_championship",
                priority=92,
                zh=f"{team} 带着卫冕目标进入季后赛，官方报道把经验和心态列为背景",
                en=f"{team} enters the playoffs pursuing a repeat title, with experience and mindset as part of the setup",
            )
        if match := TOP_SEED_RE.search(row):
            team = _team_name(match.group("name"))
            wins = match.group("wins")
            _push(
                pieces,
                theme="top_seed_profile",
                priority=100,
                zh=f"{team} 常规赛长期处在东部头名位置，并以 {wins} 胜和东部头号种子身份进入季后赛",
                en=f"{team} spent much of the season atop the East and enters the playoffs as a {wins}-win No. 1 seed",
            )
        if "pistons" in row.lower() and "underappreciated" in row.lower():
            _push(
                pieces,
                theme="underappreciated",
                priority=97,
                zh="尽管排名和战绩占优，Detroit Pistons 仍被官方报道写成外界评价偏低的一方",
                en="Despite the record and seed, Detroit Pistons are framed as still feeling underappreciated",
            )
        elif match := UNDERAPP_RE.search(row):
            team = _team_name(match.group("name"))
            _push(
                pieces,
                theme="underappreciated",
                priority=97,
                zh=f"尽管排名和战绩占优，{team} 仍被官方报道写成外界评价偏低的一方",
                en=f"Despite the record and seed, {team} is framed as still feeling underappreciated",
            )
        if "don't live and die by other people's expectations" in row.lower() or "pistons basketball" in row.lower():
            _push(
                pieces,
                theme="team_mindset",
                priority=86,
                zh="官方报道引用球队态度：他们更关注自己的比赛方式，而不是外界预期",
                en="The story frames the team's mindset around its own style rather than outside expectations",
            )
        if match := SEED_OPP_RE.search(row):
            opp = _team_name(match.group("opp"))
            seed = match.group("seed")
            _push(
                pieces,
                theme="opponent_seed",
                priority=84,
                zh=f"{opp} 以 {seed} 号种子身份挑战高位种子，系列赛定位很清楚",
                en=f"{opp} enters as the No. {seed} seed challenging a higher-seeded opponent",
            )
        if DIFFERENT_LOOK_RE.search(row):
            _push(
                pieces,
                theme="changed_lineups",
                priority=100,
                zh="官方报道强调双方常规赛虽交手多次，但进入首轮时阵容版本已经明显不同",
                en="The story stresses that the regular-season meetings are less clean because both teams now look different",
            )
        if match := SPLIT_FOUR_RE.search(row):
            team_a = _team_name(match.group("a"))
            team_b = _team_name(match.group("b"))
            _push(
                pieces,
                theme="split_series",
                priority=88,
                zh=f"{team_a} 和 {team_b} 常规赛四次交手平分秋色，但多数交手发生在赛季早段",
                en=f"{team_a} and {team_b} split four regular-season games, but most came early in the season",
            )
        if TATUM_RETURN_RE.search(row) or "tatum returned" in row.lower():
            _push(
                pieces,
                theme="tatum_return",
                priority=95,
                zh="Jayson Tatum 复出改变了凯尔特人的季后赛版本，也削弱了常规赛交手参考价值",
                en="Jayson Tatum's return changes Boston's playoff version and weakens the regular-season comparison",
            )
        if GEORGE_ABSENCE_RE.search(row):
            _push(
                pieces,
                theme="paul_george_context",
                priority=93,
                zh="Paul George 在部分常规赛交手中缺席或不在阵中，这让双方首轮对位样本更复杂",
                en="Paul George missed or was absent from parts of the regular-season matchup sample, complicating the preview",
            )
    for row in rows:
        if match := DEF_RATING_RE.search(row):
            a = _team_name(match.group("a"))
            b = _team_name(match.group("b"))
            _push(
                pieces,
                theme="defense",
                priority=90,
                zh=f"这组系列赛带有强防守底色：{a} 防守效率联盟第一，{b} 也排在第九",
                en=f"The series has a strong defensive frame: {a} ranked first in defensive rating and {b} ninth",
            )
        if match := TURNOVER_POINTS_RE.search(row):
            team = _team_name(match.group("team"))
            opp = _team_name(match.group("opp"))
            _push(
                pieces,
                theme="turnovers",
                priority=89,
                zh=f"失误转化会是关键：{team} 上一场靠对手失误拿到 {match.group('points')} 分，{opp} 常规赛同样擅长利用失误",
                en=f"Turnover conversion matters: {team} just scored {match.group('points')} off turnovers, while {opp} also lived off those chances",
            )
        if match := SERIES_RECORD_RE.search(row):
            team = _team_name(match.group("name"))
            _push(
                pieces,
                theme="head_to_head_context",
                priority=87,
                zh=f"{team} 常规赛 { _number_word(match.group('games')) } 次交手赢下 { _number_word(match.group('wins')) } 场，但这个样本仍需要结合轮休背景看",
                en=f"{team} won { _number_word(match.group('wins')) } of { _number_word(match.group('games')) } regular-season meetings, though that sample needs lineup context",
            )
    if REFERENCE_LIMIT_RE.search(text):
        _push(
            pieces,
            theme="sample_limit",
            priority=85,
            zh="常规赛收官战分差参考价值有限，因为双方季后赛位置已定且大量主力轮休",
            en="The regular-season finale is a limited reference point because playoff positions were set and starters largely sat",
        )
    if match := QUESTIONABLE_RE.search(text):
        team = _team_name(match.group("team"))
        players = re.sub(r"\s*\([^)]*\)", "", match.group("players"))
        _push(
            pieces,
            theme="availability",
            priority=86,
            zh=f"{team} 仍有 {players} 的出战状态需要确认",
            en=f"{team} still has availability questions around {players}",
        )
    return sorted(pieces, key=lambda item: int(item["priority"]), reverse=True)


def _extract_post(story: dict[str, Any], game_recap: dict[str, Any] | None) -> list[dict[str, Any]]:
    pieces: list[dict[str, Any]] = []
    rows = _sentences(story, game_recap)
    text = " ".join(rows)
    if "after halftime" in text.lower() and ("shooting efficiency" in text.lower() or "efficiency" in text.lower()):
        _push(
            pieces,
            theme="post_halftime_efficiency",
            priority=100,
            zh="半场后的投篮效率差距成了比赛拉开的主要原因",
            en="The recap treats the post-halftime shooting-efficiency gap as the main separator",
        )
    for row in rows:
        if match := SHOOTING_EDGE_RE.search(row):
            team = _team_name(match.group("team"))
            opp = _team_name(match.group("opp"))
            zh_tail = "，而且是在阵容短缺背景下做到的" if "short-handed" in text.lower() else ""
            en_tail = ", and did it while short-handed" if "short-handed" in text.lower() else ""
            _push(
                pieces,
                theme="shooting_edge",
                priority=100,
                zh=f"{team} 靠 {match.group('team_pct')}% 对 {opp} {match.group('opp_pct')}% 的投篮效率差和防守压制拉开比赛{zh_tail}",
                en=f"{team} separated through a {match.group('team_pct')}% to {match.group('opp_pct')}% shooting edge and defensive control{en_tail}",
            )
        if match := RUN_RE.search(row):
            team = _team_name(re.sub(r"^(?:before|after)\s+", "", match.group("team").strip(), flags=re.IGNORECASE))
            _push(
                pieces,
                theme="decisive_run",
                priority=95,
                zh=f"{team} 的 {match.group('run')} 攻势被官方报道写成比赛拉开的关键段落",
                en=f"{team}'s {match.group('run')} run is treated as the stretch that opened the game",
            )
        if match := NEVER_TRAILED_RE.search(row):
            team = _team_name(match.group("team"))
            if _looks_like_placeholder_subject(team):
                continue
            lead_match = LEAD_BUILD_RE.search(row)
            threes_match = THREES_MADE_RE.search(row)
            zh = f"{team} 从开场后就一直掌控比赛"
            en = f"{team} controlled the game from the opening stretch and never trailed"
            if lead_match:
                zh += f"，一度把优势扩大到 {lead_match.group('lead')} 分"
                en += f", building the lead to {lead_match.group('lead')}"
            if threes_match:
                zh += f"，外线还投进了 {threes_match.group('count')} 记三分"
                en += f" while knocking down {threes_match.group('count')} threes"
            _push(
                pieces,
                theme="wire_to_wire_control",
                priority=99,
                zh=zh,
                en=en,
            )
        if match := SURGE_RE.search(row):
            _push(
                pieces,
                theme="decisive_surge",
                priority=97,
                zh=f"比赛是在一波 {match.group('run')} 的攻势后被迅速拉开的",
                en=f"The game swung open during a {match.group('run')} surge",
            )
        if match := HALFTIME_LEAD_RE.search(row):
            _push(
                pieces,
                theme="halftime_gap",
                priority=96,
                zh=f"比赛到半场 {match.group('score')} 时，走势已经基本定下来了",
                en=f"The recap treats the {match.group('score')} halftime score as the point where control was established",
            )
        if match := THREE_POINT_STRUGGLE_RE.search(row):
            team = _team_name(match.group("team"))
            _push(
                pieces,
                theme="shooting_struggle",
                priority=95,
                zh=f"{team} 外线只有 {match.group('made')} 中 {match.group('attempts')}，进攻从外线开始失速",
                en=f"{team} went just {match.group('made')} of {match.group('attempts')} from three and never found enough perimeter offense",
            )
        if match := MINUTES_DEPTH_RE.search(row):
            count = _number_word(match.group("count"))
            _push(
                pieces,
                theme="rotation_depth",
                priority=92,
                zh=f"赢球一方轮换铺得很开，共有 {count} 人至少打了 {match.group('minutes')} 分钟",
                en=f"The recap also highlights depth, with {count} players logging at least {match.group('minutes')} minutes",
            )
        if match := HOME_POSTSEASON_SKID_RE.search(row):
            team = _team_name(match.group("team"))
            _push(
                pieces,
                theme="home_postseason_skid",
                priority=96,
                zh=f"{team} 的主场季后赛连败还在延续，这也是文中反复提到的背景",
                en=f"{team}'s home playoff skid is still running, and the recap treats it as part of the story frame",
            )
        if match := EARLY_START_RE.search(row):
            opp = _team_name(match.group("opp"))
            turnovers = _number_word(match.group("turnovers"))
            _push(
                pieces,
                theme="fast_start_defense",
                priority=95,
                zh=f"赢球一方开场就打出 {match.group('lead')}，同时把 {opp} 压到仅 {match.group('made')}-{match.group('attempts')} 投篮并逼出 {turnovers} 次失误",
                en=f"The winner jumped out {match.group('lead')} early while holding {opp} to {match.group('made')}-{match.group('attempts')} shooting and forcing {turnovers} turnovers",
            )
    scorer = next((match for row in rows if (match := SCORE_RE.search(row))), None)
    if scorer:
        player = scorer.group("player").strip()
        points = scorer.group("points")
        _push(
            pieces,
            theme="standout_scorer",
            priority=90,
            zh=f"{player} 的 {points} 分表现也被放在最显眼的位置",
            en=f"{player}'s {points}-point performance is the central individual recap thread",
        )
    if "short-handed" in text.lower() or "without their top" in text.lower() or "without its top" in text.lower():
        _push(
            pieces,
            theme="short_handed",
            priority=90,
            zh="胜方是在阵容吃紧、主力得分点不整的背景下完成赢球",
            en="The win came with a short-handed roster and missing scoring options",
        )
    if "injury absence" in text.lower() or "injured" in text.lower() or "injury" in text.lower():
        _push(
            pieces,
            theme="availability",
            priority=86,
            zh="伤病和球员可用性是解释这场比赛配置的重要背景",
            en="Injury and availability context is part of the official recap frame",
        )
    if "game 1" in text.lower() or "series opener" in text.lower() or "first-round" in text.lower():
        _push(
            pieces,
            theme="series_context",
            priority=60,
            zh="这场比赛仍被放在系列赛首战语境下解读",
            en="The game is framed through a Game 1 and first-round series-opening lens",
        )
    return sorted(pieces, key=lambda item: int(item["priority"]), reverse=True)


def build_story_brief(
    story: dict[str, Any],
    game_recap: dict[str, Any] | None = None,
    *,
    source_label: str = "NBA.com",
    url: str = "",
) -> dict[str, Any]:
    """Build a compact structured summary for an NBA.com story."""
    header = story.get("header") or {}
    headline = str(header.get("headline") or "").strip()
    story_type = str(story.get("storyType") or "").lower()
    phase = "post" if "recap" in story_type else "pregame" if "preview" in story_type else "unknown"
    pieces = _extract_post(story, game_recap) if phase == "post" else _extract_pregame(story, game_recap)
    if not pieces and headline:
        _push(
            pieces,
            theme="headline_fallback",
            priority=1,
            zh=f"{source_label} 的报道标题提供了这场比赛的基础背景：{headline}",
            en=f"{source_label}'s headline provides the basic story frame: {headline}",
        )
    bullets_zh = [str(piece["zh"]) for piece in pieces if piece.get("zh")]
    bullets_en = [str(piece["en"]) for piece in pieces if piece.get("en")]
    return {
        "phase": phase,
        "compactZh": _compact(pieces, lang="zh", limit=2),
        "compactEn": _compact(pieces, lang="en", limit=2),
        "bulletsZh": bullets_zh[:6],
        "bulletsEn": bullets_en[:6],
        "themes": [str(piece["theme"]) for piece in pieces[:8] if piece.get("theme")],
        "sourceLabel": source_label,
        "url": url,
        "headline": headline,
        "confidence": "high" if len(pieces) >= 2 else ("medium" if pieces else "low"),
    }


def build_story_full_summary(
    story: dict[str, Any],
    game_recap: dict[str, Any] | None = None,
    *,
    source_label: str = "NBA.com",
    url: str = "",
) -> dict[str, Any]:
    """Build a longer structured summary for the official-report intent."""
    header = story.get("header") or {}
    headline = str(header.get("headline") or "").strip()
    story_type = str(story.get("storyType") or "").lower()
    phase = "post" if "recap" in story_type else "pregame" if "preview" in story_type else "unknown"
    pieces = _extract_post(story, game_recap) if phase == "post" else _extract_pregame(story, game_recap)
    if not pieces and headline:
        _push(
            pieces,
            theme="headline_fallback",
            priority=1,
            zh=f"{source_label} 的标题只提供了基础报道背景：{headline}",
            en=f"{source_label}'s headline only provides a basic story frame: {headline}",
        )
    content = [str(item or "").strip() for item in (story.get("content") or []) if str(item or "").strip()]
    bullets_zh = [str(piece["zh"]) for piece in pieces if piece.get("zh")]
    bullets_en = [str(piece["en"]) for piece in pieces if piece.get("en")]
    return {
        "phase": phase,
        "headline": headline,
        "sourceLabel": source_label,
        "url": url,
        "date": str(story.get("date") or ""),
        "byline": str(header.get("byline") or ""),
        "bytitle": str(header.get("bytitle") or ""),
        "storyType": str(story.get("storyType") or ""),
        "paragraphCount": len(content),
        "compactZh": _compact(pieces, lang="zh", limit=3),
        "compactEn": _compact(pieces, lang="en", limit=3),
        "bulletsZh": bullets_zh[:8],
        "bulletsEn": bullets_en[:8],
        "themes": [str(piece["theme"]) for piece in pieces[:10] if piece.get("theme")],
        "confidence": "high" if len(pieces) >= 3 else ("medium" if pieces else "low"),
    }
