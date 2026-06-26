# /// script
# requires-python = ">=3.10"
# dependencies = ["feedparser", "aiohttp"]
# ///
"""Fetch recent articles from Karpathy's curated RSS feeds and output JSON to stdout.

Fetches hn-popular-blogs-2025.opml from GitHub Pages at runtime.
"""

import argparse
import asyncio
import json
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from time import mktime

import aiohttp
import feedparser

_OPML_URL = "https://mesevenjourney.github.io/static/hn-popular-blogs-2025.opml"
MAX_ARTICLES = 20


async def fetch_opml(session: aiohttp.ClientSession) -> list[dict]:
    """Fetch OPML from URL and return list of {text, xmlUrl, htmlUrl}."""
    async with session.get(_OPML_URL, timeout=aiohttp.ClientTimeout(total=30)) as resp:
        resp.raise_for_status()
        body = await resp.text()
    root = ET.fromstring(body)
    feeds = []
    for outline in root.iter("outline"):
        url = outline.get("xmlUrl")
        if url:
            feeds.append({
                "text": outline.get("text", ""),
                "xmlUrl": url,
                "htmlUrl": outline.get("htmlUrl", ""),
            })
    return feeds


async def fetch_feed(session: aiohttp.ClientSession, feed: dict, sem: asyncio.Semaphore, cutoff: datetime) -> list[dict]:
    """Fetch and parse a single RSS/Atom feed, returning articles newer than cutoff."""
    url = feed["xmlUrl"]
    try:
        async with sem:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                body = await resp.text()
    except Exception as e:
        print(f"[WARN] Failed to fetch {feed['text']} ({url}): {e}", file=sys.stderr)
        return []

    try:
        d = feedparser.parse(body)
    except Exception as e:
        print(f"[WARN] Failed to parse {feed['text']}: {e}", file=sys.stderr)
        return []

    articles = []
    for entry in d.entries:
        published = None
        for attr in ("published_parsed", "updated_parsed"):
            t = getattr(entry, attr, None)
            if t:
                try:
                    published = datetime.fromtimestamp(mktime(t), tz=timezone.utc)
                except (OverflowError, OSError, ValueError):
                    continue
                break

        if published is None or published < cutoff:
            continue

        summary = ""
        if hasattr(entry, "summary"):
            summary = entry.summary[:500]

        articles.append({
            "title": getattr(entry, "title", "(no title)"),
            "link": getattr(entry, "link", ""),
            "author": getattr(entry, "author", ""),
            "source": feed["text"],
            "source_url": feed["htmlUrl"],
            "published": published.isoformat(),
            "summary": summary,
        })

    return articles


async def main(hours: int) -> None:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)

    sem = asyncio.Semaphore(20)
    all_articles: list[dict] = []

    async with aiohttp.ClientSession(headers={"User-Agent": "karpathy-curated-rss-brief/1.0"}) as session:
        feeds = await fetch_opml(session)
        print(f"[INFO] Parsed {len(feeds)} feeds from {_OPML_URL}, fetching articles newer than {cutoff.isoformat()}", file=sys.stderr)
        tasks = [fetch_feed(session, f, sem, cutoff) for f in feeds]
        results = await asyncio.gather(*tasks)

    for batch in results:
        all_articles.extend(batch)

    all_articles.sort(key=lambda a: a["published"], reverse=True)
    all_articles = all_articles[:MAX_ARTICLES]
    print(f"[INFO] Found {len(all_articles)} articles in the last {hours}h (capped at {MAX_ARTICLES})", file=sys.stderr)
    json.dump(all_articles, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch recent RSS articles from Karpathy's curated feed list")
    parser.add_argument("--hours", type=int, default=24, help="How many hours back to look (default: 24)")
    args = parser.parse_args()

    asyncio.run(main(args.hours))
