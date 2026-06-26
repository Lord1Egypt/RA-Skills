#!/usr/bin/env python3
"""Direct NBA.com provider helpers for NBA_TR."""

from __future__ import annotations

import html
import json
import os
import re
import socket
import ssl
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from cache_store import cached_json_fetch
from nba_common import NBAReportError
from nba_story_summarizer import build_story_brief, build_story_full_summary
from nba_teams import ENGLISH_TEAM_ALIASES, canonicalize_team_abbr

DEFAULT_STATS_BASE_URL = "https://stats.nba.com/stats"
DEFAULT_LIVE_BASE_URL = "https://cdn.nba.com/static/json/liveData"
DEFAULT_STATIC_BASE_URL = "https://cdn.nba.com/static/json/staticData"
DEFAULT_WEB_BASE_URL = "https://www.nba.com"
USER_AGENT = "nba-tr-openclaw/2.0"
DEFAULT_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": USER_AGENT,
    "Referer": "https://www.nba.com/",
    "Origin": "https://www.nba.com",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true",
}
_LEAGUE_SCHEDULE_MEMORY_CACHE: dict[str, tuple[dict[str, Any], str]] = {}


def resolve_web_base_url(base_url: str | None = None) -> str:
    return (base_url or os.environ.get("NBA_TR_NBA_WEB_BASE_URL") or DEFAULT_WEB_BASE_URL).rstrip("/")


def resolve_stats_base_url(base_url: str | None = None) -> str:
    return (base_url or os.environ.get("NBA_TR_NBA_STATS_BASE_URL") or DEFAULT_STATS_BASE_URL).rstrip("/")


def resolve_live_base_url(base_url: str | None = None) -> str:
    return (base_url or os.environ.get("NBA_TR_NBA_BASE_URL") or DEFAULT_LIVE_BASE_URL).rstrip("/")


def resolve_static_base_url(base_url: str | None = None) -> str:
    return (base_url or os.environ.get("NBA_TR_NBA_STATIC_BASE_URL") or DEFAULT_STATIC_BASE_URL).rstrip("/")


def _request_json(url: str, timeout_seconds: int) -> dict[str, Any]:
    request = urllib.request.Request(url, headers=DEFAULT_HEADERS, method="GET")
    context = ssl.create_default_context()
    with urllib.request.urlopen(request, timeout=timeout_seconds, context=context) as response:
        return json.loads(response.read().decode("utf-8"))


def _fetch_json(url: str, timeout_seconds: int = 20) -> dict[str, Any]:
    try:
        return _request_json(url, timeout_seconds)
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")
        raise NBAReportError(body_text or f"HTTP {exc.code}", status=exc.code, kind="nba_http_error") from exc
    except (urllib.error.URLError, TimeoutError, socket.timeout, ssl.SSLError, json.JSONDecodeError) as exc:
        raise NBAReportError(f"无法连接 NBA 数据源: {exc}", kind="nba_connection_failed") from exc


def _request_text(url: str, timeout_seconds: int) -> str:
    request = urllib.request.Request(
        url,
        headers={**DEFAULT_HEADERS, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
        method="GET",
    )
    context = ssl.create_default_context()
    with urllib.request.urlopen(request, timeout=timeout_seconds, context=context) as response:
        return response.read().decode("utf-8", errors="replace")


def _fetch_text(url: str, timeout_seconds: int = 20) -> str:
    try:
        return _request_text(url, timeout_seconds)
    except urllib.error.HTTPError as exc:
        raise NBAReportError(f"HTTP {exc.code}", status=exc.code, kind="nba_http_error") from exc
    except (urllib.error.URLError, TimeoutError, socket.timeout, ssl.SSLError, UnicodeDecodeError) as exc:
        raise NBAReportError(f"无法连接 NBA 页面数据源: {exc}", kind="nba_connection_failed") from exc


def _build_url(base_url: str, endpoint: str, params: dict[str, str]) -> str:
    query = urllib.parse.urlencode(params)
    return f"{base_url}/{endpoint}?{query}" if query else f"{base_url}/{endpoint}"


def unavailable_game_story(reason: str, *, url: str | None = None) -> dict[str, Any]:
    return {
        "available": False,
        "sourceLabel": "NBA.com",
        "url": url or "",
        "reason": reason,
        "headline": "",
        "date": "",
        "byline": "",
        "bytitle": "",
        "storyType": "",
        "summarySignals": [],
        "storySummary": {"pregame": {"zh": "", "en": ""}, "post": {"zh": "", "en": ""}},
        "storyBrief": {},
        "storyFullSummary": {},
        "gameRecap": {},
    }


def nba_game_url(game_id: str, away_abbr: str, home_abbr: str, *, base_url: str | None = None) -> str:
    web_base = resolve_web_base_url(base_url)
    away = canonicalize_team_abbr(away_abbr).lower()
    home = canonicalize_team_abbr(home_abbr).lower()
    return f"{web_base}/game/{away}-vs-{home}-{game_id}"


NEXT_DATA_RE = re.compile(r'<script[^>]+id=["\']__NEXT_DATA__["\'][^>]*>(?P<payload>.*?)</script>', re.DOTALL)


def _extract_next_data(document: str) -> dict[str, Any]:
    match = NEXT_DATA_RE.search(document)
    if not match:
        raise NBAReportError("NBA.com 页面缺少 __NEXT_DATA__。", kind="not_found")
    raw = match.group("payload")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        try:
            return json.loads(html.unescape(raw))
        except json.JSONDecodeError as exc:
            raise NBAReportError("NBA.com __NEXT_DATA__ 解析失败。", kind="parse_error") from exc


def _walk_dicts(value: Any) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    if isinstance(value, dict):
        results.append(value)
        for child in value.values():
            results.extend(_walk_dicts(child))
    elif isinstance(value, list):
        for child in value:
            results.extend(_walk_dicts(child))
    return results


def _find_story_container(payload: dict[str, Any]) -> dict[str, Any] | None:
    for item in _walk_dicts(payload):
        story = item.get("story")
        if not isinstance(story, dict):
            continue
        header = story.get("header") or {}
        content = story.get("content") or []
        if isinstance(header, dict) and (header.get("headline") or content):
            return item
    return None


def _find_game_recap(payload: dict[str, Any]) -> dict[str, Any]:
    for item in _walk_dicts(payload):
        recap = item.get("gameRecap")
        if isinstance(recap, dict) and (recap.get("title") or recap.get("excerpt")):
            return {
                "title": str(recap.get("title") or ""),
                "url": str(recap.get("permalink") or ""),
                "excerpt": str(recap.get("excerpt") or ""),
            }
    return {}


def _find_page_game_id(payload: dict[str, Any]) -> str:
    for item in _walk_dicts(payload):
        for key in ("gameId", "gameID", "game_id"):
            value = str(item.get(key) or "").strip()
            if value.isdigit() and len(value) >= 7:
                return value
    return ""


def _mentions_team(text: str, abbr: str) -> bool:
    aliases = ENGLISH_TEAM_ALIASES.get(canonicalize_team_abbr(abbr), [abbr])
    lowered = f" {text.lower()} "
    for alias in aliases:
        escaped = re.escape(str(alias).lower())
        if re.search(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])", lowered):
            return True
    return False


def _story_matches_expected_matchup(story: dict[str, Any], away_abbr: str | None, home_abbr: str | None) -> bool:
    if not away_abbr or not home_abbr:
        return True
    text = _story_text(story)
    return _mentions_team(text, away_abbr) and _mentions_team(text, home_abbr)


PLAYER_SCORE_RE = re.compile(
    r"(?P<name>[A-Z][A-Za-z.'\u2019-]+(?:\s+[A-Z][A-Za-z.'\u2019-]+){0,3})\s+(?:scored|had|finished with)\s+(?:a [^,.;]*? )?(?P<points>\d{1,2})\s+points?",
)
RUN_SPURT_RE = re.compile(
    r"(?P<winner>[A-Z][A-Za-z.'\u2019& -]+?)\s+(?:broke it open|pulled away|seized control)\s+with\s+(?:a|an)\s+(?P<run>\d{1,2}-\d{1,2})\s+run",
    re.IGNORECASE,
)
SHOOTING_EDGE_RE = re.compile(
    r"(?P<team>[A-Z][A-Za-z.'\u2019& -]+?)\s+thrived by hitting\s+(?P<team_pct>\d{1,2}\.\d)%.*?holding\s+the\s+(?P<opp>[A-Z][A-Za-z.'\u2019& -]+?)\s+to\s+(?P<opp_pct>\d{1,2}\.\d)%\s+shooting",
    re.IGNORECASE,
)
WON_SERIES_RE = re.compile(
    r"(?P<team>[A-Z][A-Za-z.'\u2019& -]+?)\s+has won\s+(?P<wins>\w+)\s+of\s+the\s+(?P<games>\w+)\s+games?\s+with\s+(?P<opp>[A-Z][A-Za-z.'\u2019& -]+?)\s+this year",
    re.IGNORECASE,
)
MISSED_MATCHUPS_RE = re.compile(
    r"(?P<player>[A-Z][A-Za-z.'\u2019-]+(?:\s+[A-Z][A-Za-z.'\u2019-]+){0,3})\s+missed all\s+(?P<count>\w+)\s+contests?\s+with injuries",
    re.IGNORECASE,
)
PLAY_IN_CLINCH_RE = re.compile(
    r"The\s+(?P<team>[A-Z][A-Za-z.'\u2019& -]+?)\s*\([^)]*\)\s+clinched the\s+(?P<seed>\w+)\s+seed.*?win over\s+(?P<opp>[A-Z][A-Za-z.'\u2019& -]+?)\s+.*?play-?in tournament",
    re.IGNORECASE,
)
FIRST_TRIP_RE = re.compile(
    r"That victory allowed\s+(?P<team>[A-Z][A-Za-z.'\u2019& -]+?)\s+to earn (?:its|their)\s+first trip to the playoffs since\s+(?P<year>\d{4})",
    re.IGNORECASE,
)
SPLIT_MEETINGS_RE = re.compile(
    r"(?P<team_a>[A-Z][A-Za-z.'\u2019& -]+?)\s+and\s+(?P<team_b>[A-Z][A-Za-z.'\u2019& -]+?)\s+split their regular-season meetings",
    re.IGNORECASE,
)
CHANGED_LOOK_RE = re.compile(
    r"(?P<team_a>[A-Z][A-Za-z.'\u2019& -]+?)\s+and\s+(?P<team_b>[A-Z][A-Za-z.'\u2019& -]+?)\s+met during the regular season,\s+but both teams have a different look",
    re.IGNORECASE,
)
HEADLINE_PLAY_IN_RE = re.compile(r"fresh off (?:a )?play-?in win,\s*(?P<team>.+?)\s+take on\s+(?P<opp>.+)$", re.IGNORECASE)
HEADLINE_RENEW_RE = re.compile(r"(?P<team_a>.+?),\s*(?P<team_b>.+?)\s+renew acquaintances in series opener$", re.IGNORECASE)
HEADLINE_UNDERAPP_RE = re.compile(r"[\"'“”]?(?P<tag>underappreciated)[\"'“”]?\s+(?P<team>.+?)\s+open playoffs against\s+(?P<opp>.+)$", re.IGNORECASE)
HEADLINE_FACE_RE = re.compile(r"(?P<team>.+?)\s+face\s+(?P<focus>.+?),\s*(?P<opp>.+?)\s+to open playoffs$", re.IGNORECASE)
HEADLINE_SCORE_RE = re.compile(r"(?P<player>.+?)\s+scores?\s+(?P<points>\d+)\s+as\s+(?P<winner>.+?)\s+beat\s+(?P<loser>.+)$", re.IGNORECASE)


def _story_text(story: dict[str, Any]) -> str:
    header = story.get("header") or {}
    parts = [str(header.get("headline") or "")]
    parts.extend(str(item or "") for item in (story.get("content") or []))
    return " ".join(part for part in parts if part).strip()


def _story_sentences(story: dict[str, Any], game_recap: dict[str, Any] | None = None) -> list[str]:
    sentences: list[str] = []
    headline = str((story.get("header") or {}).get("headline") or "").strip()
    if headline:
        sentences.append(headline)
    for item in story.get("content") or []:
        text = str(item or "").strip()
        if text:
            sentences.append(text)
    excerpt = str((game_recap or {}).get("excerpt") or "").strip()
    if excerpt:
        sentences.append(excerpt)
    return sentences


def _clean_story_sentence(text: str) -> str:
    cleaned = re.sub(r"^[A-Z .'-]+\([A-Z]{2}\)\s+", "", str(text or "").strip())
    return re.sub(r"\s+", " ", cleaned).strip()


def _number_word_to_int(token: str) -> int | None:
    if not token:
        return None
    if token.isdigit():
        return int(token)
    mapping = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }
    return mapping.get(token.strip().lower())


def _push_summary_piece(pieces: list[dict[str, str]], zh: str, en: str) -> None:
    candidate_zh = str(zh or "").strip()
    candidate_en = str(en or "").strip()
    if not candidate_zh and not candidate_en:
        return
    if any(piece.get("zh") == candidate_zh or piece.get("en") == candidate_en for piece in pieces):
        return
    pieces.append({"zh": candidate_zh, "en": candidate_en})


def _trim_terminal_punctuation(text: str, *, lang: str) -> str:
    if lang == "zh":
        return re.sub(r"[。；，\s]+$", "", text.strip())
    return re.sub(r"[.;,\s]+$", "", text.strip())


def _join_summary_pieces(pieces: list[dict[str, str]], *, limit: int = 2) -> dict[str, str]:
    selected = pieces[:limit]
    zh_parts = [_trim_terminal_punctuation(piece["zh"], lang="zh") for piece in selected if piece.get("zh")]
    en_parts = [_trim_terminal_punctuation(piece["en"], lang="en") for piece in selected if piece.get("en")]
    zh = "；".join(part for part in zh_parts if part)
    en = ". ".join(part for part in en_parts if part)
    if zh:
        zh += "。"
    if en:
        en += "."
    return {"zh": zh, "en": en}


def _clean_story_subject(text: str) -> str:
    return re.sub(r"^(?:but|and)\s+", "", str(text or "").strip(), flags=re.IGNORECASE)


def _extract_pregame_body_points(sentences: list[str]) -> list[dict[str, str]]:
    pieces: list[dict[str, str]] = []
    body = [_clean_story_sentence(sentence) for sentence in sentences[1:] if _clean_story_sentence(sentence)]
    first_trip_year = ""
    for sentence in body:
        first_trip_match = FIRST_TRIP_RE.search(sentence)
        if first_trip_match:
            first_trip_year = first_trip_match.group("year").strip()
    for sentence in body:
        lowered = sentence.lower()
        play_in_match = PLAY_IN_CLINCH_RE.search(sentence)
        if play_in_match:
            team = play_in_match.group("team").strip()
            opp = play_in_match.group("opp").strip()
            year_tail = f"，也是球队自 {first_trip_year} 年以来首次重返季后赛" if first_trip_year else ""
            _push_summary_piece(
                pieces,
                f"NBA.com 提到 {team} 通过附加赛击败 {opp} 拿到季后赛席位{year_tail}。",
                f"NBA.com highlights {team} coming through the play-in against {opp} to secure its playoff berth{f' and first trip back since {first_trip_year}' if first_trip_year else ''}.",
            )
        won_match = WON_SERIES_RE.search(sentence)
        missed_match = MISSED_MATCHUPS_RE.search(sentence)
        if won_match and missed_match:
            team = won_match.group("team").strip()
            opp = won_match.group("opp").strip()
            wins = _number_word_to_int(won_match.group("wins")) or won_match.group("wins").strip()
            games = _number_word_to_int(won_match.group("games")) or won_match.group("games").strip()
            player = _clean_story_subject(missed_match.group("player"))
            _push_summary_piece(
                pieces,
                f"NBA.com 提到 {team} 常规赛 {games} 次交手赢下 {wins} 场，而 {player} 当时因伤全部缺席，这次对位背景和前面完全不同。",
                f"NBA.com notes that {team} won {wins} of the {games} regular-season meetings, but {player} missed all of them with injuries, making this matchup materially different.",
            )
        split_match = SPLIT_MEETINGS_RE.search(sentence)
        if split_match:
            team_a = split_match.group("team_a").strip()
            team_b = split_match.group("team_b").strip()
            _push_summary_piece(
                pieces,
                f"NBA.com 提到 {team_a} 和 {team_b} 常规赛交手平分秋色，这场系列赛首战没有明显历史优势方。",
                f"NBA.com notes that {team_a} and {team_b} split their regular-season meetings, leaving no clear historical edge entering Game 1.",
            )
        changed_look_match = CHANGED_LOOK_RE.search(sentence)
        if changed_look_match:
            team_a = changed_look_match.group("team_a").strip()
            team_b = changed_look_match.group("team_b").strip()
            _push_summary_piece(
                pieces,
                f"NBA.com 强调 {team_a} 和 {team_b} 虽然常规赛交过手，但进入系列赛后已经是完全不同的阵容版本。",
                f"NBA.com emphasizes that {team_a} and {team_b} may have met in the regular season, but the playoff version of this matchup now looks materially different.",
            )
        if "availability will shape the key matchup" in lowered or "availability" in lowered:
            _push_summary_piece(
                pieces,
                "NBA.com 认为阵容可用性和轮换变化会直接决定这场比赛的关键对位。",
                "NBA.com argues that availability and rotation changes will directly shape the key matchup.",
            )
    return pieces


def _extract_post_body_points(sentences: list[str]) -> list[dict[str, str]]:
    pieces: list[dict[str, str]] = []
    body = [_clean_story_sentence(sentence) for sentence in sentences[1:] if _clean_story_sentence(sentence)]
    short_handed = any("without their top two scorers" in sentence.lower() or "short-handed" in sentence.lower() for sentence in body)
    for sentence in body:
        run_match = RUN_SPURT_RE.search(sentence)
        if run_match:
            winner = re.sub(r"^(before|after)\s+", "", run_match.group("winner").strip(), flags=re.IGNORECASE)
            run = run_match.group("run").strip()
            _push_summary_piece(
                pieces,
                f"NBA.com 复盘认为 {winner} 靠一波 {run} 的攻势拉开比赛，这是胜负转折点。",
                f"NBA.com frames the turning point around {winner} using a {run} run to break the game open.",
            )
        shooting_match = SHOOTING_EDGE_RE.search(sentence)
        if shooting_match:
            team = shooting_match.group("team").strip()
            opp = shooting_match.group("opp").strip()
            team_pct = shooting_match.group("team_pct").strip()
            opp_pct = shooting_match.group("opp_pct").strip()
            short_handed_text = "，而且还是在主力得分点不整的情况下" if short_handed else ""
            _push_summary_piece(
                pieces,
                f"NBA.com 复盘强调 {team} 靠 {team_pct}% 对 {opp_pct}% 的投篮命中率差和防守压制拉开比赛{short_handed_text}。",
                f"NBA.com emphasizes that {team} opened the gap through a {team_pct}% to {opp_pct}% shooting edge and defensive control{', even while short-handed' if short_handed else ''}.",
            )
        lowered = sentence.lower()
        if "after halftime" in lowered and ("efficiency" in lowered or "shooting" in lowered):
            _push_summary_piece(
                pieces,
                "NBA.com 复盘把半场后的投篮效率差距视为比赛拉开的关键。",
                "NBA.com treats the post-halftime shooting-efficiency gap as the key reason the game opened up.",
            )
        if "during the spurt" in lowered and ("3-pointers" in lowered or "3-pointers" in lowered):
            _push_summary_piece(
                pieces,
                f"NBA.com 特别点出 {sentence}",
                f"NBA.com specifically highlights that {sentence}",
            )
    return pieces


def _story_mentions_availability(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in ("injury", "availability", "available", "questionable", "out", "return", "returned", "lineup"))


def _story_mentions_previous_meetings(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in ("split their regular-season meetings", "split their meetings", "regular-season meetings", "met during the regular season"))


def _story_mentions_changed_lineups(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in ("different look", "changed lineups", "lineup changes", "different lineups"))


def build_story_summary(story: dict[str, Any], game_recap: dict[str, Any] | None = None) -> dict[str, dict[str, str]]:
    headline = str((story.get("header") or {}).get("headline") or "").strip()
    text = _story_text(story)
    sentences = _story_sentences(story, game_recap)
    summary = {
        "pregame": {"zh": "", "en": ""},
        "post": {"zh": "", "en": ""},
    }
    pregame_body_pieces = _extract_pregame_body_points(sentences)
    post_body_pieces = _extract_post_body_points(sentences)

    if pregame_body_pieces:
        summary["pregame"] = _join_summary_pieces(pregame_body_pieces)

    play_in_match = HEADLINE_PLAY_IN_RE.match(headline)
    if play_in_match and not summary["pregame"]["zh"]:
        team = play_in_match.group("team").strip()
        opp = play_in_match.group("opp").strip()
        summary["pregame"] = {
            "zh": f"NBA.com 把 {team} 刚从附加赛突围、马上挑战 {opp} 作为赛前主线。",
            "en": f"NBA.com frames the pregame angle around {team} coming out of the play-in and immediately facing {opp}.",
        }

    renew_match = HEADLINE_RENEW_RE.match(headline)
    if renew_match and not summary["pregame"]["zh"]:
        team_a = renew_match.group("team_a").strip()
        team_b = renew_match.group("team_b").strip()
        summary["pregame"] = {
            "zh": f"NBA.com 把 {team_a} 和 {team_b} 在系列赛首战再度碰面作为赛前主线。",
            "en": f"NBA.com frames the pregame storyline around {team_a} and {team_b} meeting again in the series opener.",
        }

    under_match = HEADLINE_UNDERAPP_RE.match(headline)
    if under_match and not summary["pregame"]["zh"]:
        team = under_match.group("team").strip()
        opp = under_match.group("opp").strip()
        summary["pregame"] = {
            "zh": f"NBA.com 把被低估的 {team} 开启对阵 {opp} 的季后赛作为赛前主线。",
            "en": f"NBA.com frames the pregame angle around an underappreciated {team} opening the playoffs against {opp}.",
        }

    face_match = HEADLINE_FACE_RE.match(headline)
    if face_match and not summary["pregame"]["zh"]:
        team = face_match.group("team").strip()
        focus = face_match.group("focus").strip()
        opp = face_match.group("opp").strip()
        summary["pregame"] = {
            "zh": f"NBA.com 把 {team} 首战就要面对 {focus} 和 {opp} 作为赛前焦点。",
            "en": f"NBA.com frames the pregame focus around {team} opening the playoffs against {focus} and {opp}.",
        }

    if not summary["pregame"]["zh"] and _story_mentions_changed_lineups(text):
        summary["pregame"] = {
            "zh": "NBA.com 强调这组对阵和常规赛相比已经是不同阵容版本。",
            "en": "NBA.com emphasizes that this matchup now looks different from the regular-season version because of lineup changes.",
        }

    if not summary["pregame"]["zh"] and _story_mentions_previous_meetings(text):
        summary["pregame"] = {
            "zh": "NBA.com 提到双方常规赛交手难分高下，这会直接影响这场前瞻判断。",
            "en": "NBA.com points to the teams' tight regular-season meetings as a key part of the preview.",
        }

    if not summary["pregame"]["zh"] and _story_mentions_availability(text):
        summary["pregame"] = {
            "zh": "NBA.com 把文章重点放在阵容可用性和轮换变化上。",
            "en": "NBA.com centers the preview on availability and rotation changes.",
        }

    score_match = HEADLINE_SCORE_RE.match(headline)
    if score_match:
        player = score_match.group("player").strip()
        points = score_match.group("points").strip()
        scorer_match = PLAYER_SCORE_RE.search(text)
        if scorer_match and len(scorer_match.group("name").strip()) > len(player):
            player = scorer_match.group("name").strip()
        post_zh = f"NBA.com 把 {player} 的 {points} 分表现列为复盘主线。"
        post_en = f"NBA.com frames the recap around {player}'s {points}-point performance."
        if "short-handed" in text.lower():
            post_zh = f"NBA.com 把 {player} 的 {points} 分表现和球队在阵容吃紧下赢球列为复盘主线。"
            post_en = f"NBA.com frames the recap around {player}'s {points} points and a short-handed win."
        _push_summary_piece(post_body_pieces, post_zh, post_en)
    else:
        scorer_match = PLAYER_SCORE_RE.search(text)
        if scorer_match:
            player = scorer_match.group("name").strip()
            points = scorer_match.group("points").strip()
            _push_summary_piece(
                post_body_pieces,
                f"NBA.com 把 {player} 的 {points} 分表现列为复盘主线。",
                f"NBA.com frames the recap around {player}'s {points}-point performance.",
            )

    if post_body_pieces:
        summary["post"] = _join_summary_pieces(post_body_pieces)

    if not summary["post"]["zh"]:
        scorer_match = PLAYER_SCORE_RE.search(text)
        if scorer_match:
            player = scorer_match.group("name").strip()
            points = scorer_match.group("points").strip()
            summary["post"] = {
                "zh": f"NBA.com 把 {player} 的 {points} 分表现列为复盘主线。",
                "en": f"NBA.com frames the recap around {player}'s {points}-point performance.",
            }

    if not summary["post"]["zh"] and _story_mentions_availability(text):
        summary["post"] = {
            "zh": "NBA.com 复盘里重点提到了阵容可用性和轮换变化的影响。",
            "en": "NBA.com's recap emphasizes the effect of availability and rotation changes.",
        }

    if not summary["post"]["zh"] and any("shoot" in sentence.lower() or "efficiency" in sentence.lower() for sentence in sentences):
        summary["post"] = {
            "zh": "NBA.com 复盘把投篮效率列为比赛走势的重要解释线索。",
            "en": "NBA.com's recap points to shooting efficiency as a major explanation for the result.",
        }

    return summary


def _story_signal_exists(signals: list[dict[str, str]], kind: str) -> bool:
    return any(signal.get("kind") == kind for signal in signals)


def extract_story_signals(story: dict[str, Any], game_recap: dict[str, Any] | None = None) -> list[dict[str, str]]:
    text = _story_text(story)
    if game_recap and game_recap.get("excerpt"):
        text = f"{text} {game_recap['excerpt']}"
    lowered = text.lower()
    signals: list[dict[str, str]] = []

    scorer_match = PLAYER_SCORE_RE.search(text)
    if scorer_match:
        signals.append(
            {
                "kind": "standout_scorer",
                "subject": scorer_match.group("name").strip(),
                "value": scorer_match.group("points").strip(),
            }
        )
    if any(token in lowered for token in ("short-handed", "without their top", "without its top", "missing so much firepower")):
        signals.append({"kind": "short_handed", "subject": "", "value": ""})
    if any(token in lowered for token in ("injury absence", "late scratch", "injured", "injury", "out indefinitely")):
        signals.append({"kind": "availability", "subject": "", "value": ""})
    if any(token in lowered for token in ("series opener", "game 1", "first-round", "first round", "playoff")):
        signals.append({"kind": "series_context", "subject": "", "value": ""})
    if any(token in lowered for token in ("split their four", "met four times", "regular season", "last matchups")):
        signals.append({"kind": "previous_matchups", "subject": "", "value": ""})
    if any(token in lowered for token in ("shooting", "shot poorly", "field", "3-point", "3s", "3-pointers")):
        signals.append({"kind": "efficiency", "subject": "", "value": ""})
    if any(token in lowered for token in ("returned", "different look", "lineup", "core group", "challenge")) and not _story_signal_exists(signals, "matchup_watch"):
        signals.append({"kind": "matchup_watch", "subject": "", "value": ""})
    return signals[:4]


def _story_from_container(
    container: dict[str, Any],
    *,
    url: str,
    payload: dict[str, Any],
    expected_game_id: str | None = None,
    away_abbr: str | None = None,
    home_abbr: str | None = None,
) -> dict[str, Any]:
    story = container.get("story") or {}
    header = story.get("header") or {}
    game_recap = _find_game_recap(payload)
    page_game_id = _find_page_game_id(payload)
    if expected_game_id and page_game_id and str(expected_game_id).strip() != page_game_id:
        return unavailable_game_story("story_mismatch", url=url)
    if not _story_matches_expected_matchup(story, away_abbr, home_abbr):
        return unavailable_game_story("story_mismatch", url=url)
    content = [str(item or "").strip() for item in (story.get("content") or []) if str(item or "").strip()]
    return {
        "available": True,
        "sourceLabel": "NBA.com",
        "url": url,
        "gameId": page_game_id or str(expected_game_id or ""),
        "headline": str(header.get("headline") or ""),
        "date": str(story.get("date") or ""),
        "byline": str(header.get("byline") or ""),
        "bytitle": str(header.get("bytitle") or ""),
        "storyType": str(story.get("storyType") or container.get("storyType") or ""),
        "summarySignals": extract_story_signals(story, game_recap),
        "storySummary": build_story_summary(story, game_recap),
        "storyBrief": build_story_brief(story, game_recap, source_label="NBA.com", url=url),
        "storyFullSummary": build_story_full_summary(story, game_recap, source_label="NBA.com", url=url),
        "gameRecap": game_recap,
        "content": content,
    }


def fetch_nba_game_story_url(
    url: str,
    *,
    timeout_seconds: int = 20,
    expected_game_id: str | None = None,
    away_abbr: str | None = None,
    home_abbr: str | None = None,
) -> dict[str, Any]:
    expected_key = "|".join(str(value or "") for value in (expected_game_id, away_abbr, home_abbr))
    payload, _freshness = cached_json_fetch(
        namespace="nba:game_story",
        key=f"v6:{url}:{expected_key}",
        ttl_seconds=900,
        max_payload_bytes=400_000,
        fetcher=lambda: _fetch_nba_game_story_url_uncached(
            url,
            timeout_seconds=timeout_seconds,
            expected_game_id=expected_game_id,
            away_abbr=away_abbr,
            home_abbr=home_abbr,
        ),
    )
    return payload


def _fetch_nba_game_story_url_uncached(
    url: str,
    *,
    timeout_seconds: int,
    expected_game_id: str | None = None,
    away_abbr: str | None = None,
    home_abbr: str | None = None,
) -> dict[str, Any]:
    try:
        document = _fetch_text(url, timeout_seconds=timeout_seconds)
        payload = _extract_next_data(document)
        container = _find_story_container(payload)
        if not container:
            return unavailable_game_story("missing_story", url=url)
        return _story_from_container(
            container,
            url=url,
            payload=payload,
            expected_game_id=expected_game_id,
            away_abbr=away_abbr,
            home_abbr=home_abbr,
        )
    except NBAReportError as exc:
        return unavailable_game_story(exc.kind, url=url)


def fetch_nba_game_story(
    game_id: str,
    away_abbr: str,
    home_abbr: str,
    *,
    base_url: str | None = None,
    timeout_seconds: int = 20,
) -> dict[str, Any]:
    if not game_id:
        return unavailable_game_story("missing_game_id")
    url = nba_game_url(game_id, away_abbr, home_abbr, base_url=base_url)
    return fetch_nba_game_story_url(
        url,
        timeout_seconds=timeout_seconds,
        expected_game_id=game_id,
        away_abbr=away_abbr,
        home_abbr=home_abbr,
    )


def public_game_story_payload(story: dict[str, Any] | None) -> dict[str, Any]:
    if not story:
        return unavailable_game_story("unavailable")
    return {
        key: value
        for key, value in story.items()
        if key not in {"content"}
    }


def fetch_scoreboard(date_text: str, *, base_url: str | None = None, timeout_seconds: int = 20) -> dict[str, Any]:
    stats_base = resolve_stats_base_url(base_url)
    month, day, year = date_text[5:7], date_text[8:10], date_text[0:4]
    url = _build_url(
        stats_base,
        "scoreboardv2",
        {
            "GameDate": f"{month}/{day}/{year}",
            "LeagueID": "00",
            "DayOffset": "0",
        },
    )
    payload, freshness = cached_json_fetch(
        namespace="nba:scoreboard",
        key=date_text,
        ttl_seconds=120,
        fetcher=lambda: _fetch_json(url, timeout_seconds),
    )
    return {
        "baseUrl": stats_base,
        "endpoint": "scoreboardv2",
        "request": {"date": date_text},
        "data": payload,
        "dataFreshness": freshness,
    }


def fetch_team_roster(
    team_id: str,
    *,
    season: str | None = None,
    base_url: str | None = None,
    timeout_seconds: int = 20,
) -> dict[str, Any]:
    stats_base = resolve_stats_base_url(base_url)
    target_season = season or os.environ.get("NBA_TR_NBA_SEASON", "2025-26")
    url = _build_url(
        stats_base,
        "commonteamroster",
        {
            "TeamID": team_id,
            "Season": target_season,
            "LeagueID": "00",
        },
    )
    payload, freshness = cached_json_fetch(
        namespace="nba:team_roster",
        key=f"{team_id}:{target_season}",
        ttl_seconds=3600,
        fetcher=lambda: _fetch_json(url, timeout_seconds),
    )
    return {
        "baseUrl": stats_base,
        "endpoint": "commonteamroster",
        "request": {"team": team_id, "season": target_season},
        "data": payload,
        "dataFreshness": freshness,
    }


def fetch_team_player_averages(
    team_id: str,
    *,
    season: str | None = None,
    base_url: str | None = None,
    timeout_seconds: int = 20,
) -> dict[str, Any]:
    stats_base = resolve_stats_base_url(base_url)
    target_season = season or os.environ.get("NBA_TR_NBA_SEASON", "2025-26")
    url = _build_url(
        stats_base,
        "leaguedashplayerstats",
        {
            "College": "",
            "Conference": "",
            "Country": "",
            "DateFrom": "",
            "DateTo": "",
            "Division": "",
            "DraftPick": "",
            "DraftYear": "",
            "GameScope": "",
            "GameSegment": "",
            "Height": "",
            "LastNGames": "0",
            "LeagueID": "00",
            "Location": "",
            "MeasureType": "Base",
            "Month": "0",
            "OpponentTeamID": "0",
            "Outcome": "",
            "PORound": "0",
            "PaceAdjust": "N",
            "PerMode": "PerGame",
            "Period": "0",
            "PlayerExperience": "",
            "PlayerPosition": "",
            "PlusMinus": "N",
            "Rank": "N",
            "Season": target_season,
            "SeasonSegment": "",
            "SeasonType": "Regular Season",
            "ShotClockRange": "",
            "StarterBench": "",
            "TeamID": team_id,
            "TwoWay": "0",
            "VsConference": "",
            "VsDivision": "",
            "Weight": "",
        },
    )
    payload, freshness = cached_json_fetch(
        namespace="nba:team_player_averages",
        key=f"{team_id}:{target_season}",
        ttl_seconds=1800,
        fetcher=lambda: _fetch_json(url, timeout_seconds),
    )
    return {
        "baseUrl": stats_base,
        "endpoint": "leaguedashplayerstats",
        "request": {"team": team_id, "season": target_season},
        "data": payload,
        "dataFreshness": freshness,
    }


def fetch_live_boxscore(game_id: str, *, base_url: str | None = None, timeout_seconds: int = 20) -> dict[str, Any]:
    live_base = resolve_live_base_url(base_url)
    url = f"{live_base}/boxscore/boxscore_{game_id}.json"
    payload, freshness = cached_json_fetch(
        namespace="nba:boxscore",
        key=game_id,
        ttl_seconds=30,
        fetcher=lambda: _fetch_json(url, timeout_seconds),
    )
    return {
        "baseUrl": live_base,
        "endpoint": "boxscore",
        "request": {"gameId": game_id},
        "data": payload,
        "dataFreshness": freshness,
    }


def fetch_play_by_play(game_id: str, *, base_url: str | None = None, timeout_seconds: int = 20) -> dict[str, Any]:
    live_base = resolve_live_base_url(base_url)
    url = f"{live_base}/playbyplay/playbyplay_{game_id}.json"
    payload, freshness = cached_json_fetch(
        namespace="nba:play_by_play",
        key=game_id,
        ttl_seconds=15,
        fetcher=lambda: _fetch_json(url, timeout_seconds),
    )
    return {
        "baseUrl": live_base,
        "endpoint": "playbyplay",
        "request": {"gameId": game_id},
        "data": payload,
        "dataFreshness": freshness,
    }


def extract_scoreboard_games(payload: dict[str, Any]) -> list[dict[str, Any]]:
    games: list[dict[str, Any]] = []
    result_sets = payload.get("resultSets") or []
    rows_by_name = {entry.get("name"): entry for entry in result_sets if isinstance(entry, dict)}
    headers = rows_by_name.get("GameHeader", {}).get("headers") or []
    rows = rows_by_name.get("GameHeader", {}).get("rowSet") or []
    for row in rows:
        record = {headers[index]: row[index] for index in range(min(len(headers), len(row)))}
        home_abbr = canonicalize_team_abbr(record.get("HOME_TEAM_ABBREVIATION"))
        away_abbr = canonicalize_team_abbr(record.get("VISITOR_TEAM_ABBREVIATION"))
        games.append(
            {
                "gameId": str(record.get("GAME_ID") or ""),
                "gameCode": str(record.get("GAMECODE") or ""),
                "homeAbbr": home_abbr,
                "awayAbbr": away_abbr,
                "statusText": str(record.get("GAME_STATUS_TEXT") or ""),
            }
        )
    if games:
        return games

    scoreboard = payload.get("scoreboard") or {}
    for game in scoreboard.get("games") or []:
        home_team = game.get("homeTeam") or {}
        away_team = game.get("awayTeam") or {}
        games.append(
            {
                "gameId": str(game.get("gameId") or ""),
                "gameCode": str(game.get("gameCode") or ""),
                "homeAbbr": canonicalize_team_abbr(home_team.get("teamTricode") or home_team.get("teamCode")),
                "awayAbbr": canonicalize_team_abbr(away_team.get("teamTricode") or away_team.get("teamCode")),
                "statusText": str((game.get("gameStatusText") or game.get("gameStatus")) or ""),
            }
        )
    return games


def find_game_id_by_matchup(
    date_text: str,
    away_abbr: str,
    home_abbr: str,
    *,
    base_url: str | None = None,
    timeout_seconds: int = 20,
) -> str | None:
    payload = fetch_scoreboard(date_text, base_url=base_url, timeout_seconds=timeout_seconds)["data"]
    for game in extract_scoreboard_games(payload):
        if game["awayAbbr"] == canonicalize_team_abbr(away_abbr) and game["homeAbbr"] == canonicalize_team_abbr(home_abbr):
            return game["gameId"] or None
    return None


def fetch_league_schedule(*, base_url: str | None = None, timeout_seconds: int = 15) -> dict[str, Any]:
    static_base = resolve_static_base_url(base_url)
    url = f"{static_base}/scheduleLeagueV2_1.json"
    if url in _LEAGUE_SCHEDULE_MEMORY_CACHE:
        payload, freshness = _LEAGUE_SCHEDULE_MEMORY_CACHE[url]
        return {
            "baseUrl": static_base,
            "endpoint": "scheduleLeagueV2_1",
            "data": payload,
            "dataFreshness": freshness,
        }
    payload, freshness = cached_json_fetch(
        namespace="nba:league_schedule",
        key=url,
        ttl_seconds=21_600,
        max_payload_bytes=16_000_000,
        fetcher=lambda: _fetch_json(url, timeout_seconds),
    )
    _LEAGUE_SCHEDULE_MEMORY_CACHE[url] = (payload, freshness)
    return {
        "baseUrl": static_base,
        "endpoint": "scheduleLeagueV2_1",
        "data": payload,
        "dataFreshness": freshness,
    }


def find_game_id_by_schedule(
    date_text: str,
    away_abbr: str,
    home_abbr: str,
    *,
    base_url: str | None = None,
    timeout_seconds: int = 15,
) -> str | None:
    away = canonicalize_team_abbr(away_abbr)
    home = canonicalize_team_abbr(home_abbr)
    payload = fetch_league_schedule(base_url=base_url, timeout_seconds=timeout_seconds)["data"]
    target_prefix = f"{date_text[5:7]}/{date_text[8:10]}/{date_text[0:4]}" if re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_text or "") else ""
    for game_date in ((payload.get("leagueSchedule") or {}).get("gameDates") or []):
        if target_prefix and not str(game_date.get("gameDate") or "").startswith(target_prefix):
            continue
        for game in game_date.get("games") or []:
            away_team = game.get("awayTeam") or {}
            home_team = game.get("homeTeam") or {}
            if canonicalize_team_abbr(away_team.get("teamTricode")) == away and canonicalize_team_abbr(home_team.get("teamTricode")) == home:
                return str(game.get("gameId") or "") or None
    return None


def extract_roster_players(payload: dict[str, Any]) -> list[dict[str, str]]:
    players: list[dict[str, str]] = []
    result_sets = payload.get("resultSets") or []
    row_set = None
    headers = None
    for entry in result_sets:
        if isinstance(entry, dict) and (entry.get("name") == "CommonTeamRoster" or not headers):
            headers = entry.get("headers") or headers
            row_set = entry.get("rowSet") or row_set
    if headers and row_set:
        for row in row_set:
            record = {headers[index]: row[index] for index in range(min(len(headers), len(row)))}
            display_name = str(record.get("PLAYER") or "").strip()
            if display_name:
                players.append(
                    {
                        "id": str(record.get("PLAYER_ID") or ""),
                        "displayName": display_name,
                        "shortName": display_name,
                        "jersey": str(record.get("NUM") or ""),
                        "position": str(record.get("POSITION") or ""),
                    }
                )
        return players

    game = payload.get("game") or {}
    for side_key in ("homeTeam", "awayTeam"):
        for player in ((game.get(side_key) or {}).get("players") or []):
            name = player.get("name") or player.get("familyName")
            if name:
                players.append(
                    {
                        "id": str(player.get("personId") or ""),
                        "displayName": str(name),
                        "shortName": str(name),
                        "jersey": str(player.get("jerseyNum") or ""),
                        "position": str(player.get("position") or ""),
                    }
                )
    return players


def extract_play_actions(payload: dict[str, Any]) -> list[dict[str, Any]]:
    game = payload.get("game") or {}
    actions = game.get("actions") or payload.get("actions") or []
    results: list[dict[str, Any]] = []
    for item in actions:
        player_name = item.get("playerName") or item.get("personName") or ""
        results.append(
            {
                "actionNumber": item.get("actionNumber"),
                "clock": str((item.get("clock") or "")).removeprefix("PT"),
                "period": item.get("period") or item.get("periodNumber"),
                "description": item.get("description") or item.get("actionType") or "",
                "homeScore": item.get("scoreHome"),
                "awayScore": item.get("scoreAway"),
                "teamId": str(item.get("teamId") or ""),
                "playerName": str(player_name),
            }
        )
    return results


def _float_or_none(value: Any) -> float | None:
    try:
        if value in (None, ""):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def extract_team_player_averages(payload: dict[str, Any]) -> dict[str, dict[str, float | None]]:
    result_sets = payload.get("resultSets") or payload.get("resultSet") or []
    if isinstance(result_sets, dict):
        result_sets = [result_sets]
    if not result_sets:
        return {}
    first = next((entry for entry in result_sets if isinstance(entry, dict)), None)
    if not first:
        return {}
    headers = first.get("headers") or []
    rows = first.get("rowSet") or []
    results: dict[str, dict[str, float | None]] = {}
    for row in rows:
        record = {headers[index]: row[index] for index in range(min(len(headers), len(row)))}
        name = str(record.get("PLAYER_NAME") or record.get("PLAYER") or "").strip()
        if not name:
            continue
        results[name] = {
            "MIN": _float_or_none(record.get("MIN")),
            "PTS": _float_or_none(record.get("PTS")),
            "REB": _float_or_none(record.get("REB")),
            "AST": _float_or_none(record.get("AST")),
            "STL": _float_or_none(record.get("STL")),
            "BLK": _float_or_none(record.get("BLK")),
            "TOV": _float_or_none(record.get("TOV")),
            "FG_PCT": _float_or_none(record.get("FG_PCT")),
            "FG3_PCT": _float_or_none(record.get("FG3_PCT")),
            "FT_PCT": _float_or_none(record.get("FT_PCT")),
            "GP": _float_or_none(record.get("GP")),
        }
    return results


def extract_boxscore_players(payload: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    game = payload.get("game") or {}
    result: dict[str, list[dict[str, Any]]] = {}
    for side_key in ("awayTeam", "homeTeam"):
        side = game.get(side_key) or {}
        abbr = canonicalize_team_abbr(side.get("teamTricode") or side.get("teamCode"))
        team_players: list[dict[str, Any]] = []
        for player in side.get("players") or []:
            name = player.get("name") or player.get("familyName")
            if not name:
                continue
            stats_raw = player.get("statistics") or {}
            team_players.append(
                {
                    "displayName": str(name),
                    "starter": bool(player.get("starter")),
                    "stats": {
                        "points": stats_raw.get("points") or player.get("points"),
                        "rebounds": stats_raw.get("reboundsTotal") or player.get("rebounds"),
                        "assists": stats_raw.get("assists") or player.get("assists"),
                        "minutes": stats_raw.get("minutesCalculated") or stats_raw.get("minutes") or player.get("minutes"),
                    },
                }
            )
        if abbr:
            result[abbr] = team_players
    return result


def extract_live_boxscore_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    """从 NBA Live boxscore payload 中提取实时比赛快照（比分、节次、时钟）。"""
    game = payload.get("game") or {}

    away_team = game.get("awayTeam") or {}
    home_team = game.get("homeTeam") or {}

    away_score = away_team.get("score")
    home_score = home_team.get("score")

    # 解析比赛时钟：NBA Live 格式通常是 "PT08M47.00S"
    raw_clock = game.get("gameClock") or game.get("gameTimeQtr") or ""
    display_clock = ""
    if raw_clock:
        # 去掉 PT 前缀和 S 后缀，转成 MM:SS 格式
        import re as _re
        m = _re.match(r"PT(?P<min>\d+)M(?P<sec>[\d.]+)S", raw_clock)
        if m:
            minutes = int(m.group("min"))
            seconds = int(float(m.group("sec")))
            display_clock = f"{minutes}:{seconds:02d}"
        else:
            display_clock = raw_clock

    return {
        "awayScore": away_score,
        "homeScore": home_score,
        "awayScoreSource": "explicit" if away_score is not None else "none",
        "homeScoreSource": "explicit" if home_score is not None else "none",
        "period": game.get("period"),
        "displayClock": display_clock,
    }
