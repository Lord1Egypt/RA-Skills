#!/usr/bin/env python3
from __future__ import annotations
"""
refresh.py — Crawl feed sources and aggregate results.

Orchestrates crawling across source types:
  - x_feed: fetches X home feed via Bird (filter:follows). Direct API, no browser.
  - x_profile: fetches individual X profiles via Bird (from:handle). Direct API.
  - hn: fetches Hacker News stories via Algolia API.

All sources run as direct API/subprocess calls within one Python process.
No browser automation, no agent-in-the-loop steps.

Respects last_crawled per source for incremental updates.

Usage:
    python3 refresh.py [--type x_feed|x_profile|hn|all]
    python3 refresh.py --type x_feed
    python3 refresh.py --type x_profile
    python3 refresh.py --type hn
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_SCRIPTS_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SCRIPTS_ROOT))

from config import load_config
from feed.schema import normalize_item
from feed.sources import load_sources, save_sources, get_by_type, update_last_crawled
from feed.source.x import (
    profile_instructions as x_profile_instructions,
    fetch_profile_via_bird,
    fetch_home_feed_via_bird,
)
from feed.source.hn import fetch_hn
from feed.source.knowledge import load_sources as load_knowledge_sources, crawl_all as crawl_knowledge, new_articles_as_feed_items
from lib import bird_x as _bird

_CFG = load_config()
DEFAULT_OUTPUT = str(_CFG["feeds_file"])


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_feed_source_config(cfg: dict, sources: dict) -> None:
    """Write feed_source_config.json with per-source settings (e.g. prefer_longform) for the ranker."""
    config = {}
    for source_type in ("x_feed",):
        entries = get_by_type(sources, source_type)
        if entries:
            entry = entries[0]
            config[source_type] = {
                "prefer_longform": entry.get("prefer_longform", False)
            }
    config_path = Path(cfg["feed_dir"]) / "feed_source_config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")


def _merge_into_feeds(feeds_path: Path, new_items: list[dict]) -> None:
    """Merge new feed items into feeds.json, deduplicating by URL."""
    existing: list[dict] = []
    if feeds_path.exists():
        try:
            existing = json.loads(feeds_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            existing = []

    existing_urls = {p.get("url") for p in existing if p.get("url")}
    added = [normalize_item(item) for item in new_items if item.get("url") not in existing_urls]
    merged = [normalize_item(p) for p in existing] + added

    feeds_path.parent.mkdir(parents=True, exist_ok=True)
    feeds_path.write_text(json.dumps(merged, indent=2), encoding="utf-8")


def _expand_threads(items: list[dict]) -> list[dict]:
    """Expand thread-start and article items via Bird direct API calls."""
    expanded = []
    for item in items:
        tweet_id = item.get("tweet_id")

        if item.get("post_type") == "article" and tweet_id:
            article = _bird.fetch_article(tweet_id)
            if article:
                print(f"  Article fetched: {article.get('title', '')[:60]} ({len(article.get('body') or '')} chars)")
                expanded.append({**item, "article": article, "content": article.get("body") or item.get("content", "")})
            else:
                expanded.append(item)

        elif item.get("post_type") == "thread" and tweet_id:
            handle = item["author"].lstrip("@")
            merged = _bird.fetch_thread_as_item(tweet_id, handle, seed_item=item)
            if merged is not item:
                print(f"  Thread expanded: @{handle} ({merged.get('tweet_count', '?')} tweets)")
            expanded.append(merged)

        else:
            expanded.append(item)
    return expanded


def refresh_x_feed(count: int = 100) -> list[dict]:
    """Fetch X home feed via Bird (filter:follows) and merge into feeds.json.

    Uses the single 'x_feed' entry in sources.json (if present) for incremental
    last_crawled tracking. Returns the list of fetched items for reporting.
    """
    feeds_path = Path(_CFG["feeds_file"])
    sources_file = _CFG["sources_file"]
    sources = load_sources(sources_file)
    feed_entries = get_by_type(sources, "x_feed")
    since = feed_entries[0].get("last_crawled") if feed_entries else None
    since_note = f" (since {since})" if since else " (first crawl)"

    items = fetch_home_feed_via_bird(since=since, count=count)
    if items is None:
        print(f"  Bird credentials not configured — skipping x_feed{since_note}")
        return []

    print(f"  Bird: fetched {len(items)} tweets from home feed{since_note}")
    items = _expand_threads(items)
    _merge_into_feeds(feeds_path, items)
    update_last_crawled(sources, "x_feed", "", _now_iso())
    save_sources(sources_file, sources)
    return items


def refresh_x_profiles(sources: dict, output_dir: Path | None = None) -> list[dict]:
    """Crawl all configured X profiles, incrementally.

    Uses Bird (direct API via AUTH_TOKEN/CT0) when credentials are available,
    writing items directly into feeds.json. Falls back to browser automation
    instructions when credentials are absent.

    Returns a list of browser instruction dicts for profiles that needed the
    browser fallback (empty list when Bird handled everything).
    """
    profiles = get_by_type(sources, "x_profile")
    if not profiles:
        print("  No X profile sources configured.")
        return []

    browser_instructions = []
    feeds_path = Path(_CFG["feeds_file"])

    for p in profiles:
        handle = p.get("handle", "")
        if not handle:
            continue
        since = p.get("last_crawled")
        since_note = f" (since {since})" if since else " (first crawl)"

        # Try Bird first (direct API, no browser needed)
        items = fetch_profile_via_bird(handle, since=since)
        if items is not None:
            print(f"  Bird: fetched {len(items)} tweets from @{handle}{since_note}")
            items = _expand_threads(items)
            _merge_into_feeds(feeds_path, items)
            update_last_crawled(sources, "x_profile", handle, _now_iso())
            continue

        # Fallback: emit browser automation instructions
        out = str((output_dir or _CFG["feed_raw"]) / f"x_{handle}.json")
        instr = x_profile_instructions(handle, out, since=since)
        browser_instructions.append(instr)
        print(f"  Browser: prepared instructions for @{handle}{since_note}")
        update_last_crawled(sources, "x_profile", handle, _now_iso())

    return browser_instructions


def refresh_hn(
    output_path: Path,
    story_type: str = "both",
    hits_per_page: int = 30,
    days_back: int = 7,
) -> list[dict]:
    """Fetch HN stories via Algolia API and merge into feeds.json."""
    items = fetch_hn(story_type, hits_per_page, days_back)

    existing: list[dict] = []
    if output_path.exists():
        try:
            existing = json.loads(output_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            existing = []

    non_hn = [p for p in existing if p.get("source") != "hn"]
    merged = non_hn + items

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(merged, indent=2), encoding="utf-8")
    print(f"  Fetched {len(items)} HN stories → {output_path}")
    return items


def refresh_knowledge(max_articles: int = 10) -> list[dict]:
    """Crawl knowledge sources (RSS, sitemaps, YouTube transcripts, podcasts)
    from knowledge/index.md, save full articles to knowledge/, and generate
    feed items from newly crawled articles.

    Default max_articles=10 per source keeps the daily refresh fast.
    Use `python3 -m feed.source.knowledge --all` for full backfills."""
    feeds_path = Path(_CFG["feeds_file"])

    # Get the latest date already in feeds from knowledge source
    existing: list[dict] = []
    if feeds_path.exists():
        try:
            existing = json.loads(feeds_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            existing = []
    knowledge_dates = [
        p.get("timestamp", "") for p in existing
        if p.get("source") == "knowledge" and p.get("timestamp")
    ]
    since = max(knowledge_dates) if knowledge_dates else ""

    # Crawl new articles into knowledge/
    sources = load_knowledge_sources()
    if not sources:
        print("  No knowledge sources found in index.md")
        return []

    total = crawl_knowledge(sources, max_articles=max_articles)
    print(f"  Knowledge: crawled {total} new articles across {len(sources)} sources")

    # Generate feed items from newly crawled articles
    new_items = new_articles_as_feed_items(sources, since=since)
    if new_items:
        _merge_into_feeds(feeds_path, new_items)
        print(f"  Knowledge: {len(new_items)} new feed items merged")

    return new_items


def main():
    parser = argparse.ArgumentParser(description="Refresh feed sources")
    parser.add_argument(
        "--type",
        choices=["x_feed", "x_profile", "hn", "knowledge", "all"],
        default="all",
        help="Source type to crawl (default: all)",
    )
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Output JSON path (HN merges into this file)")

    args = parser.parse_args()

    cfg = _CFG
    sources_file = cfg["sources_file"]
    sources = load_sources(sources_file)
    raw_dir = cfg["feed_raw"]

    results = {}

    # x_feed — Bird filter:follows, direct fetch + merge
    if args.type in ("x_feed", "all"):
        items = refresh_x_feed()
        results["x_feed"] = items
        if args.type == "x_feed":
            print(f"[refresh] x_feed: {len(items)} tweets merged", file=sys.stderr)

    # x_profile — Bird per handle, direct fetch + merge (browser fallback if no creds)
    if args.type in ("x_profile", "all"):
        instructions = refresh_x_profiles(sources, raw_dir)
        results["x_profile"] = instructions
        if args.type == "x_profile":
            print(json.dumps(instructions, indent=2, default=str))

    # hn — Algolia API, direct fetch + merge
    if args.type in ("hn", "all"):
        feeds_path = Path(args.output)
        hn_items = refresh_hn(feeds_path)
        results["hn"] = hn_items
        update_last_crawled(sources, "website", "news.ycombinator.com", _now_iso())
        if args.type == "hn":
            print(json.dumps(hn_items, indent=2))

    # knowledge — RSS, sitemaps, YouTube transcripts, podcasts from index.md
    if args.type in ("knowledge", "all"):
        knowledge_items = refresh_knowledge()
        results["knowledge"] = knowledge_items

    # Write source config for the ranker (prefer_longform etc.)
    write_feed_source_config(cfg, sources)

    # Save updated last_crawled timestamps
    save_sources(sources_file, sources)

    print(f"\nRefresh complete.")
    fetched = []
    if "x_feed" in results and results["x_feed"]:
        fetched.append(f"{len(results['x_feed'])} X home feed tweets")
    if "x_profile" in results and results["x_profile"]:
        fetched.append(f"{len(results['x_profile'])} X profile(s) (browser fallback — no Bird creds)")
    if fetched:
        print(f"Fetched: {', '.join(fetched)}.")
    if "hn" in results:
        print(f"HN: {len(results['hn'])} stories merged into {args.output}.")
    if "knowledge" in results:
        print(f"Knowledge: {len(results['knowledge'])} new feed items from knowledge sources.")

    return results


if __name__ == "__main__":
    main()
