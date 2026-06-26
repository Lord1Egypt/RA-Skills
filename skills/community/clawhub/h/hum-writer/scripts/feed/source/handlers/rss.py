"""RSS/Atom feed handler -- the workhorse for Substacks, WordPress, Ghost, etc."""

import time
import feedparser

from .common import (
    DELAY,
    existing_urls,
    source_dir,
    parse_date,
    make_filename,
    extract_article,
    build_frontmatter,
)


def crawl(source: dict, max_articles: int = 0, recrawl: bool = False) -> int:
    key = source["key"]
    name = source["name"]
    author = source["author"]
    feed_url = source["url"]

    out_dir = source_dir(key)
    out_dir.mkdir(parents=True, exist_ok=True)

    already = set() if recrawl else existing_urls(key)
    if already:
        print(f"   {len(already)} articles already saved -- skipping those")

    feed = feedparser.parse(feed_url)
    entries = feed.entries
    if not entries:
        print(f"   ! could not fetch RSS: {feed_url}")
        return 0

    print(f"   {len(entries)} entries in feed")

    saved = 0
    for entry in entries:
        if max_articles and saved >= max_articles:
            break

        url = entry.get("link", "")
        if not url or url in already:
            continue

        title = entry.get("title", "Untitled")
        date = parse_date(entry)
        filename = make_filename(date, url)
        dest = out_dir / filename

        if not recrawl and dest.exists():
            continue

        print(f"   -> {title[:60]}")
        content = extract_article(url, key)
        if not content:
            print(f"     skipped (no content extracted)")
            time.sleep(DELAY)
            continue

        fm = build_frontmatter(title, date, url, key, name, author)
        dest.write_text(fm + content, encoding="utf-8")
        saved += 1
        time.sleep(DELAY)

    print(f"   done: {saved} new articles saved")
    return saved
