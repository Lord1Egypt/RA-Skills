"""Podcast handler -- Apple Podcasts ID (or RSS URL) -> episode shownotes."""

import re
import time
import requests
import feedparser

from .common import (
    DELAY,
    HEADERS,
    source_dir,
    existing_urls,
    make_filename,
    build_frontmatter,
)


def _resolve_feed_url(ref: str) -> str:
    """Accept an Apple Podcasts ID or a full RSS URL; return the RSS URL."""
    ref = ref.strip()
    if ref.startswith("http"):
        return ref
    # Apple lookup for a bare numeric ID
    if ref.isdigit():
        try:
            r = requests.get(
                "https://itunes.apple.com/lookup",
                params={"id": ref},
                headers=HEADERS,
                timeout=15,
            )
            data = r.json()
            results = data.get("results", [])
            if results:
                feed = results[0].get("feedUrl")
                if feed:
                    return feed
        except Exception as e:
            print(f"   ! Apple lookup failed: {e}")
    return ref


_HTML_TAGS = re.compile(r"<[^>]+>")

def _strip_html(s: str) -> str:
    return _HTML_TAGS.sub("", s or "").strip()


def crawl(source: dict, max_articles: int = 0, recrawl: bool = False) -> int:
    key = source["key"]
    name = source["name"]
    author = source["author"]
    feed_url = _resolve_feed_url(source["url"])

    out_dir = source_dir(key)
    out_dir.mkdir(parents=True, exist_ok=True)

    already = set() if recrawl else existing_urls(key)
    if already:
        print(f"   {len(already)} episodes already saved -- skipping those")

    print(f"   feed: {feed_url}")
    feed = feedparser.parse(feed_url)
    entries = feed.entries
    if not entries:
        print(f"   ! could not fetch podcast feed")
        return 0

    print(f"   {len(entries)} episodes in feed")

    saved = 0
    for entry in entries:
        if max_articles and saved >= max_articles:
            break

        url = entry.get("link", "") or entry.get("id", "")
        if not url or url in already:
            continue

        title = entry.get("title", "Untitled")

        # Date
        date = ""
        for attr in ("published_parsed", "updated_parsed"):
            t = getattr(entry, attr, None)
            if t:
                from datetime import datetime as _dt
                date = _dt(*t[:3]).strftime("%Y-%m-%d")
                break
        if not date:
            from datetime import date as _date
            date = _date.today().strftime("%Y-%m-%d")

        filename = make_filename(date, url)
        dest = out_dir / filename
        if not recrawl and dest.exists():
            continue

        # Body -- description / summary / content, HTML stripped
        description = ""
        for attr in ("content", "summary_detail", "summary"):
            v = entry.get(attr)
            if isinstance(v, list) and v:
                description = v[0].get("value", "") if isinstance(v[0], dict) else str(v[0])
                break
            elif isinstance(v, dict):
                description = v.get("value", "")
                break
            elif isinstance(v, str):
                description = v
                break
        description = _strip_html(description)

        # Audio URL
        audio_url = None
        for enc in entry.get("enclosures", []) or []:
            if isinstance(enc, dict) and enc.get("href"):
                audio_url = enc["href"]
                break

        # Episode number
        episode = entry.get("itunes_episode") or entry.get("episode") or None

        if not description:
            print(f"   -> skipped: {title[:60]} (no description)")
            continue

        print(f"   -> {title[:60]}")
        body = f"## Shownotes\n\n{description}\n"

        extra = {}
        if audio_url:
            extra["audio_url"] = audio_url
        if episode:
            extra["episode"] = episode

        fm = build_frontmatter(
            title, date, url, key, name, author,
            extra=extra or None,
        )
        dest.write_text(fm + body, encoding="utf-8")
        saved += 1
        time.sleep(DELAY)

    print(f"   done: {saved} new episodes saved")
    return saved
