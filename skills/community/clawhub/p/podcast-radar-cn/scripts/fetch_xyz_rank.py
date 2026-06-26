#!/usr/bin/env python3
"""Fetch and normalize ranking data from 中文播客榜."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen

USER_AGENT = "podcast-radar-cn/0.1 (+https://github.com/XiaohuoluFM/xhlfm-skills)"

ENDPOINTS = {
    "hot-episodes": "https://xyzrank.com/api/episodes",
    "hot-podcasts": "https://xyzrank.com/api/podcasts",
    "new-episodes": "https://xyzrank.com/api/new-episodes",
    "new-podcasts": "https://xyzrank.com/api/new-podcasts",
}

TOPIC_KEYWORDS = [
    "AI",
    "科技",
    "商业",
    "创业",
    "投资",
    "职场",
    "管理",
    "社会",
    "文化",
    "历史",
    "女性",
    "教育",
    "健康",
    "情感",
    "喜剧",
    "幽默",
    "电影",
    "音乐",
    "媒体",
    "国际",
    "旅行",
    "体育",
    "艺术",
]

FORMAT_HINTS = {
    "对话": "对话",
    "对谈": "对谈",
    "访谈": "访谈",
    "串台": "串台",
    "问答": "问答",
    "复盘": "复盘",
    "盘点": "盘点",
    "故事": "故事",
    "观察": "观察",
    "独白": "独白",
    "聊天": "聊天",
    "圆桌": "圆桌",
}

EPISODE_MARKER_PATTERNS = [
    re.compile(r"\bS(?P<season>\d+)\s*E(?P<episode>\d+)\b", re.IGNORECASE),
    re.compile(r"\bEP(?:ISODE)?\s*(?P<number>\d+)\b", re.IGNORECASE),
    re.compile(r"\bVol\.?\s*(?P<number>\d+)\b", re.IGNORECASE),
    re.compile(r"第\s*(?P<number>\d+)\s*[期集]"),
]

GUEST_CAPTURE_PATTERNS = [
    re.compile(r"(?:对话|对谈|访谈|with)\s*([^｜|:：!！?？]+)", re.IGNORECASE),
    re.compile(r"嘉宾[:：]\s*([^｜|!！?？]+)"),
    re.compile(r"[—-]{2,}\s*([^｜|:：!！?？]+)$"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch ranking data from 中文播客榜 and normalize it for podcast-radar-cn."
    )
    parser.add_argument(
        "--list",
        choices=sorted(ENDPOINTS),
        default="hot-podcasts",
        help="Ranking list to fetch.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Number of filtered items to return.",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=50,
        help="Page size used against the ranking API.",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Initial API offset.",
    )
    parser.add_argument(
        "--max-fetch",
        type=int,
        default=150,
        help="Maximum number of raw items to scan before stopping.",
    )
    parser.add_argument(
        "--genre",
        action="append",
        default=[],
        help="Filter by genre. May be repeated.",
    )
    parser.add_argument(
        "--query",
        help="Case-insensitive substring filter across title, show name, authors, and title signals.",
    )
    parser.add_argument(
        "--freshness-days-max",
        type=float,
        help="Only keep items whose freshness-days field is <= this value.",
    )
    parser.add_argument(
        "--min-play-count",
        type=int,
        help="Minimum play-count signal. Uses playCount for episodes and avgPlayCount for podcasts.",
    )
    parser.add_argument(
        "--min-comment-count",
        type=int,
        help="Minimum comment-count signal. Uses commentCount for episodes and avgCommentCount for podcasts.",
    )
    parser.add_argument(
        "--min-subscription",
        type=int,
        help="Minimum subscription signal. Uses subscription for episodes; ignored for podcasts without data.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the JSON output.",
    )
    return parser.parse_args()


def fetch_json(url: str) -> Dict[str, Any]:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def dedupe_preserve(items: Iterable[str]) -> List[str]:
    seen = set()
    result: List[str] = []
    for item in items:
        value = item.strip()
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def split_title_head(title: str) -> str:
    return re.split(r"[｜|:：!！?？]", title, maxsplit=1)[0].strip()


def extract_episode_markers(title: str) -> List[Dict[str, Any]]:
    markers: List[Dict[str, Any]] = []
    for pattern in EPISODE_MARKER_PATTERNS:
        for match in pattern.finditer(title):
            groups = {key: value for key, value in match.groupdict().items() if value is not None}
            marker: Dict[str, Any] = {"raw": match.group(0)}
            for key, value in groups.items():
                marker[key] = int(value)
            markers.append(marker)
    return markers


def extract_guest_hints(title: str) -> List[str]:
    hints: List[str] = []
    head = split_title_head(title)

    if "×" in head:
        hints.extend(part.strip(" ，,、") for part in head.split("×"))
    if "x" in head.lower():
        parts = re.split(r"\s+[xX]\s+", head)
        if len(parts) > 1:
            hints.extend(part.strip(" ，,、") for part in parts)

    for pattern in GUEST_CAPTURE_PATTERNS:
        for match in pattern.finditer(title):
            captured = match.group(1)
            hints.extend(re.split(r"[、,/，,]", captured))

    cleaned = [hint.strip() for hint in hints if hint and len(hint.strip()) <= 24]
    return dedupe_preserve(cleaned)


def extract_format_hints(title: str) -> List[str]:
    return [label for keyword, label in FORMAT_HINTS.items() if keyword in title]


def extract_topic_keywords(title: str) -> List[str]:
    lower_title = title.lower()
    matched: List[str] = []
    for keyword in TOPIC_KEYWORDS:
        if keyword.lower() in lower_title:
            matched.append(keyword)
    return matched


def make_title_signals(title: str) -> Dict[str, Any]:
    episode_markers = extract_episode_markers(title)
    guest_hints = extract_guest_hints(title)
    format_hints = extract_format_hints(title)
    topic_keywords = extract_topic_keywords(title)

    summary: List[str] = []
    if episode_markers:
        summary.append("标题含期号线索")
    if guest_hints:
        summary.append("标题含嘉宾或对谈线索")
    if format_hints:
        summary.append("标题含节目形式线索")
    if topic_keywords:
        summary.append("标题含主题关键词")

    return {
        "episodeMarkers": episode_markers,
        "guestHints": guest_hints,
        "formatHints": format_hints,
        "topicKeywords": topic_keywords,
        "summary": summary,
    }


def normalize_links(links: List[Dict[str, Any]]) -> Dict[str, str]:
    normalized: Dict[str, str] = {}
    for entry in links or []:
        name = entry.get("name")
        url = entry.get("url")
        if name and url:
            normalized[name] = url
    return normalized


def normalize_episode(item: Dict[str, Any], source_list: str) -> Dict[str, Any]:
    return {
        "kind": "episode",
        "sourceList": source_list,
        "rank": item.get("rank"),
        "title": item.get("title"),
        "podcastExternalId": item.get("podcastID"),
        "podcastName": item.get("podcastName"),
        "genre": item.get("primaryGenreName") or "未分类",
        "playCount": item.get("playCount"),
        "commentCount": item.get("commentCount"),
        "subscriptionCount": item.get("subscription"),
        "durationMinutes": item.get("duration"),
        "postTime": item.get("postTime"),
        "freshnessDays": item.get("lastReleaseDateDayCount"),
        "episodeUrl": item.get("link"),
        "logoUrl": item.get("logoURL"),
        "openSignal": item.get("openRate"),
        "totalEpisodesCount": item.get("totalEpisodesCount"),
        "titleSignals": make_title_signals(item.get("title", "")),
    }


def normalize_podcast(item: Dict[str, Any], source_list: str) -> Dict[str, Any]:
    links = normalize_links(item.get("links") or [])
    return {
        "kind": "podcast",
        "sourceList": source_list,
        "rank": item.get("rank"),
        "externalId": item.get("id"),
        "title": item.get("name"),
        "podcastName": item.get("name"),
        "genre": item.get("primaryGenreName") or "未分类",
        "authors": item.get("authorsText"),
        "trackCount": item.get("trackCount"),
        "avgDurationMinutes": item.get("avgDuration"),
        "avgPlayCount": item.get("avgPlayCount"),
        "avgCommentCount": item.get("avgCommentCount"),
        "avgOpenSignal": item.get("avgOpenRate"),
        "freshnessDays": item.get("lastReleaseDateDayCount"),
        "lastReleaseDate": item.get("lastReleaseDate"),
        "firstEpisodePostTime": item.get("firstEpisodePostTime"),
        "links": links,
        "xyzUrl": links.get("xyz"),
        "appleUrl": links.get("apple"),
        "websiteUrl": links.get("website"),
        "rssUrl": links.get("rss"),
    }


def normalize_item(item: Dict[str, Any], source_list: str) -> Dict[str, Any]:
    if source_list.endswith("episodes"):
        return normalize_episode(item, source_list)
    return normalize_podcast(item, source_list)


def matches_filters(item: Dict[str, Any], args: argparse.Namespace) -> bool:
    if args.genre:
        requested_genres = {genre.strip().lower() for genre in args.genre if genre.strip()}
        if (item.get("genre") or "").lower() not in requested_genres:
            return False

    if args.freshness_days_max is not None:
        freshness = item.get("freshnessDays")
        if freshness is None or freshness > args.freshness_days_max:
            return False

    if args.min_play_count is not None:
        play_count = item.get("playCount", item.get("avgPlayCount"))
        if play_count is None or play_count < args.min_play_count:
            return False

    if args.min_comment_count is not None:
        comment_count = item.get("commentCount", item.get("avgCommentCount"))
        if comment_count is None or comment_count < args.min_comment_count:
            return False

    if args.min_subscription is not None:
        subscription = item.get("subscriptionCount")
        if subscription is None and item.get("kind") == "podcast":
            pass
        elif subscription is None or subscription < args.min_subscription:
            return False

    if args.query:
        haystacks = [
            item.get("title") or "",
            item.get("podcastName") or "",
            item.get("authors") or "",
            " ".join(item.get("titleSignals", {}).get("guestHints", [])),
            " ".join(item.get("titleSignals", {}).get("topicKeywords", [])),
            " ".join(item.get("titleSignals", {}).get("formatHints", [])),
        ]
        query = args.query.lower()
        if not any(query in haystack.lower() for haystack in haystacks):
            return False

    return True


def build_url(source_list: str, offset: int, limit: int) -> str:
    query = urlencode({"offset": offset, "limit": limit})
    return f"{ENDPOINTS[source_list]}?{query}"


def main() -> int:
    args = parse_args()

    if args.limit <= 0:
        raise SystemExit("--limit must be > 0")
    if args.page_size <= 0:
        raise SystemExit("--page-size must be > 0")
    if args.max_fetch <= 0:
        raise SystemExit("--max-fetch must be > 0")

    items: List[Dict[str, Any]] = []
    total: Optional[int] = None
    raw_scanned = 0
    offset = args.offset

    while raw_scanned < args.max_fetch and len(items) < args.limit:
        page_limit = min(args.page_size, args.max_fetch - raw_scanned)
        payload = fetch_json(build_url(args.list, offset, page_limit))
        if total is None:
            total = payload.get("total")

        raw_items = payload.get("items") or []
        if not raw_items:
            break

        for raw_item in raw_items:
            normalized = normalize_item(raw_item, args.list)
            if matches_filters(normalized, args):
                items.append(normalized)
                if len(items) >= args.limit:
                    break

        raw_scanned += len(raw_items)
        offset += len(raw_items)

        if len(raw_items) < page_limit:
            break

    response = {
        "sourceList": args.list,
        "requestedLimit": args.limit,
        "returnedCount": len(items),
        "rawScanned": raw_scanned,
        "sourceTotal": total,
        "appliedFilters": {
            "genres": args.genre,
            "query": args.query,
            "freshnessDaysMax": args.freshness_days_max,
            "minPlayCount": args.min_play_count,
            "minCommentCount": args.min_comment_count,
            "minSubscription": args.min_subscription,
        },
        "items": items,
    }

    if args.pretty:
        json.dump(response, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        json.dump(response, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
