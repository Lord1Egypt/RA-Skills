#!/usr/bin/env python3
"""
knowledge.py -- Knowledge base crawler for hum.

Reads source definitions from knowledge/index.md (markdown tables) and dispatches
each source to the appropriate handler (rss / sitemap / youtube / podcast).

Saves full articles as markdown files in knowledge/<source_key>/.

Usage:
    python3 -m feed.source.knowledge --list
    python3 -m feed.source.knowledge <source_key>
    python3 -m feed.source.knowledge --all
    python3 -m feed.source.knowledge <source_key> --max 5
    python3 -m feed.source.knowledge <source_key> --recrawl

Requirements:
    pip3 install trafilatura feedparser python-slugify requests lxml_html_clean \
                 youtube-transcript-api
"""

import re
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Dict

_SCRIPTS_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_SCRIPTS_ROOT))

from config import load_config
from feed.source.handlers.common import KNOWLEDGE_DIR, INDEX_FILE, source_dir
from feed.source.handlers import rss, sitemap, youtube_transcript, podcast

HANDLERS = {
    "rss": rss.crawl,
    "sitemap": sitemap.crawl,
    "youtube": youtube_transcript.crawl,
    "podcast": podcast.crawl,
}


# -- index.md parser ---------------------------------------------------------

REQUIRED_COLS = {"key", "handler", "feed url"}


def _normalise_header(s: str) -> str:
    return s.strip().lower().replace("&", "and")


def _parse_tables(md: str) -> List[Dict[str, str]]:
    """Walk a markdown file and yield dicts for every row of every pipe-table
    that has Key, Handler, and Feed URL columns with non-empty values."""
    rows: List[Dict[str, str]] = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if "|" in line and i + 1 < len(lines) and re.match(r"^\s*\|?[\s\-:|]+\|[\s\-:|]+", lines[i + 1]):
            header_cells = [c.strip() for c in line.strip().strip("|").split("|")]
            headers = [_normalise_header(h) for h in header_cells]
            if not REQUIRED_COLS.issubset(set(headers)):
                i += 2
                continue
            j = i + 2
            while j < len(lines) and "|" in lines[j] and lines[j].strip().startswith("|"):
                cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                if len(cells) != len(headers):
                    j += 1
                    continue
                row = {headers[k]: cells[k] for k in range(len(headers))}
                row = {k: v.strip("`").strip() for k, v in row.items()}
                if row.get("key") and row.get("handler") and row.get("feed url"):
                    rows.append(row)
                j += 1
            i = j
            continue
        i += 1
    return rows


def _row_to_source(row: Dict[str, str]) -> Dict[str, str]:
    """Normalise a parsed row into the source dict handlers expect."""
    key = row["key"]
    handler = row["handler"].lower()
    url = row["feed url"]
    name = (
        row.get("name")
        or row.get("source")
        or row.get("name / source")
        or key
    )
    author = row.get("author") or name
    return {
        "key": key,
        "name": name,
        "author": author,
        "handler": handler,
        "url": url,
    }


def load_sources() -> List[Dict[str, str]]:
    """Parse index.md and return the list of crawlable source dicts."""
    if not INDEX_FILE.exists():
        print(f"! index file not found: {INDEX_FILE}")
        return []
    md = INDEX_FILE.read_text(encoding="utf-8")
    rows = _parse_tables(md)
    sources = []
    seen_keys = set()
    for row in rows:
        src = _row_to_source(row)
        if src["key"] in seen_keys:
            continue
        seen_keys.add(src["key"])
        sources.append(src)
    return sources


# -- Dispatcher ---------------------------------------------------------------

def crawl_source(source: dict, max_articles: int = 0, recrawl: bool = False) -> int:
    handler = HANDLERS.get(source["handler"])
    if not handler:
        print(f"   ! unknown handler: {source['handler']} (source: {source['key']})")
        return 0
    print(f"\n-- {source['name']} ({source['key']}) [{source['handler']}]")
    try:
        return handler(source, max_articles=max_articles, recrawl=recrawl)
    except Exception as e:
        print(f"   ! handler crashed: {e}")
        return 0


def crawl_all(sources: List[Dict[str, str]], max_articles: int = 0, recrawl: bool = False, max_workers: int = 6) -> int:
    """Crawl all sources in parallel and return total new articles saved."""
    total = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(crawl_source, s, max_articles, recrawl): s for s in sources}
        for future in as_completed(futures):
            try:
                total += future.result()
            except Exception as e:
                src = futures[future]
                print(f"   ! [{src['key']}] unexpected error: {e}")
    return total


# -- Feed item generation -----------------------------------------------------

def new_articles_as_feed_items(sources: List[Dict[str, str]], since: str = "") -> List[dict]:
    """Scan knowledge dirs for articles newer than `since` (ISO date) and return
    them as feed-compatible item dicts for merging into feeds.json."""
    items = []
    for src in sources:
        d = source_dir(src["key"])
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md"), reverse=True):
            try:
                text = f.read_text(errors="ignore")
            except Exception:
                continue
            # Parse frontmatter
            fm_match = re.match(r"^---\n(.+?)\n---", text, re.DOTALL)
            if not fm_match:
                continue
            fm = fm_match.group(1)
            date_m = re.search(r"^date:\s*(.+)$", fm, re.MULTILINE)
            date = date_m.group(1).strip() if date_m else ""
            if since and date and date <= since:
                continue
            title_m = re.search(r'^title:\s*"?(.+?)"?\s*$', fm, re.MULTILINE)
            url_m = re.search(r"^url:\s*(.+)$", fm, re.MULTILINE)
            author_m = re.search(r'^author:\s*"?(.+?)"?\s*$', fm, re.MULTILINE)

            # Determine post_type from handler
            handler = src.get("handler", "rss")
            post_type_map = {"rss": "article", "sitemap": "article", "youtube": "video", "podcast": "podcast"}
            post_type = post_type_map.get(handler, "article")

            # Extract first 300 chars of body as snippet
            body_start = fm_match.end()
            body = text[body_start:body_start + 500].strip()
            # Remove markdown headers
            body = re.sub(r"^#+\s+.*$", "", body, flags=re.MULTILINE).strip()
            snippet = body[:300].rsplit(" ", 1)[0] if len(body) > 300 else body

            items.append({
                "source": "knowledge",
                "author": author_m.group(1).strip() if author_m else src.get("author", ""),
                "title": title_m.group(1).strip() if title_m else f.stem,
                "content": snippet,
                "post_type": post_type,
                "url": url_m.group(1).strip() if url_m else "",
                "timestamp": date,
                "topics": [],
                "likes": 0,
                "retweets": 0,
                "replies": 0,
                "views": 0,
                "knowledge_source": src["key"],
                "knowledge_file": f.name,
            })
    return items


# -- CLI -----------------------------------------------------------------------

def list_sources(sources: List[Dict[str, str]]) -> None:
    print(f"\n{'Key':<22} {'Handler':<10} {'Name':<30} {'Files'}")
    print("-" * 75)
    by_handler: Dict[str, int] = {}
    for src in sources:
        d = source_dir(src["key"])
        count = len(list(d.glob("*.md"))) if d.exists() else 0
        print(f"{src['key']:<22} {src['handler']:<10} {src['name'][:28]:<30} {count}")
        by_handler[src["handler"]] = by_handler.get(src["handler"], 0) + 1
    print("-" * 75)
    print(f"Total: {len(sources)} sources")
    for h, n in sorted(by_handler.items()):
        print(f"  {h}: {n}")


def main():
    parser = argparse.ArgumentParser(
        prog="knowledge",
        description="Hum knowledge base crawler",
    )
    parser.add_argument("source", nargs="?", help="Source key to crawl")
    parser.add_argument("--all", action="store_true", help="Crawl every source in index.md")
    parser.add_argument("--recrawl", action="store_true", help="Re-fetch articles even if already saved")
    parser.add_argument("--max", type=int, default=0, help="Max articles per source")
    parser.add_argument("--list", action="store_true", help="List all sources and file counts")
    args = parser.parse_args()

    sources = load_sources()

    if args.list:
        list_sources(sources)
        return

    if args.all:
        total = crawl_all(sources, max_articles=args.max, recrawl=args.recrawl)
        print(f"\n-- Done. {total} total new articles saved.")
        return

    if args.source:
        matches = [s for s in sources if s["key"] == args.source]
        if not matches:
            print(f"Unknown source '{args.source}'. Run with --list to see available sources.")
            sys.exit(1)
        crawl_source(matches[0], max_articles=args.max, recrawl=args.recrawl)
        return

    parser.print_usage()
    print("\nSpecify a source key, or use --all to crawl every source, or --list to see available sources.")
    sys.exit(1)


if __name__ == "__main__":
    main()
