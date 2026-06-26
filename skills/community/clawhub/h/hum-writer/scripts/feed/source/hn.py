#!/usr/bin/env python3
from __future__ import annotations
"""
hn.py — Hacker News feed source via Algolia HN Search API.

Fetches front page and Show HN stories with:
  - Engagement filter (points > 2)
  - Comment enrichment for top stories (parallel, top 5 by default)
  - Deduplication by objectID

No API key needed — Algolia HN search is publicly accessible.

Usage:
    python3 -m feed.source.hn                        # front page + Show HN
    python3 -m feed.source.hn --type front_page     # front page only
    python3 -m feed.source.hn --type show_hn        # Show HN only
    python3 -m feed.source.hn --output /tmp/hn_feed.json
"""

import argparse
import html
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode
from typing import Any
import urllib.request
import urllib.error

_SCRIPTS_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_SCRIPTS_ROOT))

from config import load_config
from feed.source.x import classify

_CFG = load_config()

ALGOLIA_BASE = "https://hn.algolia.com/api/v1"
ALGOLIA_SEARCH_URL = f"{ALGOLIA_BASE}/search"
ALGOLIA_ITEM_URL = f"{ALGOLIA_BASE}/items"

# Enrich top N stories with comments
ENRICH_LIMIT = 5


def _get(url: str, timeout: int = 15) -> dict:
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def _strip_html(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r'<p>', '\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()


def fetch_algolia(tag: str, hits_per_page: int = 30, days_back: int = 7) -> list[dict]:
    """Fetch stories from Algolia, filtered by date and minimum engagement (points > 2)."""
    since = int(time.time()) - (days_back * 86400)
    params = {
        "tags": tag,
        "hitsPerPage": hits_per_page,
        "numericFilters": f"created_at_i>{since},points>2",
    }
    url = f"{ALGOLIA_SEARCH_URL}?{urlencode(params)}"
    try:
        return _get(url).get("hits", [])
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
        # Fallback without numeric filter, client-side date + points filter
        fallback_url = f"{ALGOLIA_SEARCH_URL}?tags={tag}&hitsPerPage={hits_per_page}"
        try:
            hits = _get(fallback_url).get("hits", [])
            cutoff = int(time.time()) - (days_back * 86400)
            return [h for h in hits if h.get("created_at_i", 0) > cutoff and (h.get("points") or 0) > 2]
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as exc:
            print(f"[hn] Error fetching {tag}: {exc}", file=sys.stderr)
            return []


def _fetch_comments(object_id: str, max_comments: int = 5) -> dict[str, Any]:
    """Fetch top-level comments for a story, sorted by points."""
    try:
        data = _get(f"{ALGOLIA_ITEM_URL}/{object_id}", timeout=15)
    except Exception:
        return {"comments": [], "comment_insights": []}

    children = [c for c in data.get("children", []) if c.get("text") and c.get("author")]
    children.sort(key=lambda c: c.get("points") or 0, reverse=True)

    comments = []
    insights = []
    for c in children[:max_comments]:
        text = _strip_html(c.get("text", ""))
        excerpt = text[:300] + "..." if len(text) > 300 else text
        comments.append({
            "author": c.get("author", ""),
            "text": excerpt,
            "points": c.get("points") or 0,
        })
        first = text.split(". ")[0].split("\n")[0][:200]
        if first:
            insights.append(first)

    return {"comments": comments, "comment_insights": insights}


def enrich_top_stories(items: list[dict], limit: int = ENRICH_LIMIT) -> list[dict]:
    """Fetch comments for top N stories by points, in parallel."""
    if not items:
        return items

    by_points = sorted(range(len(items)), key=lambda i: items[i].get("likes", 0), reverse=True)
    to_enrich = by_points[:limit]

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(_fetch_comments, items[i]["object_id"]): i for i in to_enrich}
        for future in as_completed(futures):
            idx = futures[future]
            try:
                result = future.result(timeout=15)
                items[idx]["top_comments"] = result["comments"]
                items[idx]["comment_insights"] = result["comment_insights"]
            except Exception:
                items[idx]["top_comments"] = []
                items[idx]["comment_insights"] = []

    return items


def parse_story(hit: dict, story_type: str) -> dict | None:
    url = hit.get("url", "")
    object_id = hit.get("objectID", "")
    if not url:
        url = f"https://news.ycombinator.com/item?id={object_id}"

    title = hit.get("title", "") or hit.get("story_text", "")[:100]
    if not title:
        return None

    text = hit.get("comment_text", "") or ""
    if story_type == "show_hn" and not text:
        text = title

    author = hit.get("author", "unknown")
    points = hit.get("points", 0) or 0
    num_comments = hit.get("num_comments", 0) or 0
    created = hit.get("created_at", "")
    try:
        date_str = datetime.fromisoformat(created.replace("Z", "+00:00")).strftime("%Y-%m-%d")
    except (ValueError, AttributeError):
        date_str = created[:10] if created else ""

    topics = classify(f"{title}\n{text[:500]}")

    return {
        "source": "hn",
        "author": f"@{author}" if author else "@hn",
        "display_name": author or "Hacker News",
        "content": (text or title)[:500],
        "post_type": "story",
        "title": title,
        "url": url,
        "discussion_url": f"https://news.ycombinator.com/item?id={object_id}",
        "topics": topics,
        "timestamp": created,
        "likes": points,
        "replies": num_comments,
        "views": points * 100,
        "object_id": object_id,
        "top_comments": [],
        "comment_insights": [],
    }


def fetch_hn(story_type: str = "both", hits_per_page: int = 30, days_back: int = 7) -> list[dict]:
    """Fetch HN stories, enrich top stories with comments, return sorted by points."""
    items: list[dict] = []

    if story_type in ("front_page", "both"):
        for hit in fetch_algolia("front_page", hits_per_page, days_back):
            item = parse_story(hit, "front_page")
            if item:
                items.append(item)

    if story_type in ("show_hn", "both"):
        for hit in fetch_algolia("show_hn", hits_per_page, days_back):
            item = parse_story(hit, "show_hn")
            if item:
                items.append(item)

    # Deduplicate by object ID
    seen: set = set()
    unique: list[dict] = []
    for item in items:
        oid = item.get("object_id", "")
        if oid and oid not in seen:
            seen.add(oid)
            unique.append(item)

    unique.sort(key=lambda x: x.get("likes", 0) or 0, reverse=True)

    # Enrich top stories with comments
    unique = enrich_top_stories(unique)

    return unique


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Hacker News stories via Algolia API")
    parser.add_argument("--type", choices=["front_page", "show_hn", "both"], default="both")
    parser.add_argument("--hits-per-page", type=int, default=30)
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--output", default=str(_CFG["feed_raw"] / "hn_feed.json"))
    args = parser.parse_args()

    print(f"[HN] Fetching — {args.type}, last {args.days} days...", file=sys.stderr)
    items = fetch_hn(args.type, args.hits_per_page, args.days)
    print(f"[HN] Got {len(items)} stories (top {ENRICH_LIMIT} enriched with comments)", file=sys.stderr)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(items, indent=2), encoding="utf-8")
    print(json.dumps(items, indent=2))


if __name__ == "__main__":
    main()
