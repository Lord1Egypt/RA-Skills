#!/usr/bin/env python3
"""
fetch_feeds.py — Fetch RSS/Atom feeds and extract articles within a time window.

Reads a JSON list of feed objects from stdin (output of parse_opml.py) or from
a file argument, and outputs a JSON array of article objects to stdout.

Usage:
    # From parse_opml.py output:
    python3 parse_opml.py feeds.opml | python3 fetch_feeds.py [options]

    # Or pass a JSON file:
    python3 fetch_feeds.py --feeds feeds.json [options]

Options:
    --hours N        Only include articles published in the last N hours (default: 24)
    --keywords K     Comma-separated keywords to filter by (title/summary match, case-insensitive)
    --feeds FILE     JSON file with feed list (instead of stdin)
    --timeout N      HTTP timeout in seconds per feed (default: 10)

Output (stdout): JSON array of article dicts:
    {
      "title": str,
      "url": str,
      "published": str (ISO 8601),
      "summary": str,
      "feed_title": str,
      "feed_url": str,
      "category": str
    }
"""

import sys
import json
import argparse
import time
import re
import html
from datetime import datetime, timezone, timedelta
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import xml.etree.ElementTree as ET

# Atom namespace
ATOM_NS = "http://www.w3.org/2005/Atom"
CONTENT_NS = "http://purl.org/rss/1.0/modules/content/"
DC_NS = "http://purl.org/dc/elements/1.1/"


def strip_html(text: str) -> str:
    """Remove HTML tags and decode entities."""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def parse_date(date_str: str) -> datetime | None:
    """Parse RFC 2822 or ISO 8601 dates to UTC datetime."""
    if not date_str:
        return None
    date_str = date_str.strip()

    # Try common formats
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",   # RFC 2822
        "%a, %d %b %Y %H:%M:%S %Z",   # RFC 2822 with tz name
        "%Y-%m-%dT%H:%M:%S%z",         # ISO 8601 with offset
        "%Y-%m-%dT%H:%M:%SZ",          # ISO 8601 UTC
        "%Y-%m-%dT%H:%M:%S",           # ISO 8601 naive
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except ValueError:
            continue

    # Handle timezone abbreviations like "GMT", "EST", etc.
    try:
        # Strip tz name and treat as UTC fallback
        cleaned = re.sub(r"\s+[A-Z]{2,5}$", "", date_str)
        dt = datetime.strptime(cleaned, "%a, %d %b %Y %H:%M:%S")
        return dt.replace(tzinfo=timezone.utc)
    except ValueError:
        pass

    return None


def fetch_url(url: str, timeout: int) -> bytes | None:
    """Fetch a URL and return raw bytes, or None on error."""
    req = Request(url, headers={"User-Agent": "rss-digest/1.0 (OpenClaw agent)"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except HTTPError as e:
        print(f"  [HTTP {e.code}] {url}", file=sys.stderr)
    except URLError as e:
        print(f"  [URL error] {url}: {e.reason}", file=sys.stderr)
    except Exception as e:
        print(f"  [Error] {url}: {e}", file=sys.stderr)
    return None


def parse_rss(root: ET.Element, feed_title: str, feed_url: str, category: str) -> list[dict]:
    """Parse RSS 2.0 feed."""
    articles = []
    channel = root.find("channel")
    if channel is None:
        return articles

    feed_title = feed_title or (channel.findtext("title") or feed_url)

    for item in channel.findall("item"):
        title = strip_html(item.findtext("title") or "")
        url = (item.findtext("link") or "").strip()
        pub_date = parse_date(item.findtext("pubDate") or item.findtext(f"{{{DC_NS}}}date") or "")
        summary = strip_html(
            item.findtext("description")
            or item.findtext(f"{{{CONTENT_NS}}}encoded")
            or ""
        )
        articles.append({
            "title": title,
            "url": url,
            "published": pub_date.isoformat() if pub_date else "",
            "published_dt": pub_date,
            "summary": summary[:500] if summary else "",
            "feed_title": feed_title,
            "feed_url": feed_url,
            "category": category,
        })
    return articles


def parse_atom(root: ET.Element, feed_title: str, feed_url: str, category: str) -> list[dict]:
    """Parse Atom 1.0 feed."""
    articles = []
    ns = ATOM_NS

    feed_title = feed_title or (root.findtext(f"{{{ns}}}title") or feed_url)

    for entry in root.findall(f"{{{ns}}}entry"):
        title = strip_html(entry.findtext(f"{{{ns}}}title") or "")

        # Prefer alternate link
        url = ""
        for link in entry.findall(f"{{{ns}}}link"):
            rel = link.get("rel", "alternate")
            if rel == "alternate" or not url:
                url = link.get("href", "")

        published_str = (
            entry.findtext(f"{{{ns}}}published")
            or entry.findtext(f"{{{ns}}}updated")
            or ""
        )
        pub_date = parse_date(published_str)

        summary = strip_html(
            entry.findtext(f"{{{ns}}}summary")
            or entry.findtext(f"{{{ns}}}content")
            or ""
        )

        articles.append({
            "title": title,
            "url": url,
            "published": pub_date.isoformat() if pub_date else "",
            "published_dt": pub_date,
            "summary": summary[:500] if summary else "",
            "feed_title": feed_title,
            "feed_url": feed_url,
            "category": category,
        })
    return articles


def parse_feed_xml(raw: bytes, feed_meta: dict) -> list[dict]:
    """Parse raw XML bytes into a list of articles."""
    feed_url = feed_meta.get("xmlUrl", "")
    feed_title = feed_meta.get("title", "")
    category = feed_meta.get("category", "")

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        print(f"  [XML parse error] {feed_url}: {e}", file=sys.stderr)
        return []

    tag = root.tag.lower()
    if "rss" in tag:
        return parse_rss(root, feed_title, feed_url, category)
    elif "feed" in tag or tag == f"{{{ATOM_NS}}}feed":
        return parse_atom(root, feed_title, feed_url, category)
    else:
        # Try both parsers
        articles = parse_rss(root, feed_title, feed_url, category)
        if not articles:
            articles = parse_atom(root, feed_title, feed_url, category)
        return articles


def matches_keywords(article: dict, keywords: list[str]) -> bool:
    """Return True if any keyword appears in title or summary."""
    if not keywords:
        return True
    text = (article.get("title", "") + " " + article.get("summary", "")).lower()
    return any(kw.lower() in text for kw in keywords)


def main():
    parser = argparse.ArgumentParser(description="Fetch RSS/Atom feeds and extract articles.")
    parser.add_argument("--hours", type=int, default=24, help="Time window in hours (default: 24)")
    parser.add_argument("--keywords", type=str, default="", help="Comma-separated filter keywords")
    parser.add_argument("--feeds", type=str, default="", help="JSON file with feed list (default: stdin)")
    parser.add_argument("--timeout", type=int, default=10, help="HTTP timeout per feed (default: 10)")
    args = parser.parse_args()

    # Load feed list
    if args.feeds:
        try:
            with open(args.feeds) as f:
                feeds = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[fetch_feeds] Error loading feeds file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            feeds = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            print(f"[fetch_feeds] JSON decode error from stdin: {e}", file=sys.stderr)
            sys.exit(1)

    if not isinstance(feeds, list) or not feeds:
        print("[fetch_feeds] No feeds to process.", file=sys.stderr)
        print("[]")
        return

    cutoff = datetime.now(timezone.utc) - timedelta(hours=args.hours)
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]

    print(f"[fetch_feeds] Processing {len(feeds)} feed(s), window={args.hours}h, keywords={keywords or 'none'}", file=sys.stderr)

    all_articles = []
    for i, feed_meta in enumerate(feeds, 1):
        url = feed_meta.get("xmlUrl", "").strip()
        if not url:
            continue

        title = feed_meta.get("title", url)
        print(f"  [{i}/{len(feeds)}] {title} ...", file=sys.stderr)

        raw = fetch_url(url, args.timeout)
        if raw is None:
            continue

        articles = parse_feed_xml(raw, feed_meta)

        for art in articles:
            pub_dt = art.pop("published_dt", None)  # remove non-serializable field

            # Time filter: if no date, include by default
            if pub_dt is not None and pub_dt < cutoff:
                continue

            if not matches_keywords(art, keywords):
                continue

            all_articles.append(art)

        # Small delay to be polite
        if i < len(feeds):
            time.sleep(0.2)

    # Sort newest first
    all_articles.sort(key=lambda a: a.get("published", ""), reverse=True)

    print(json.dumps(all_articles, indent=2))
    print(f"[fetch_feeds] Done. {len(all_articles)} article(s) matched.", file=sys.stderr)


if __name__ == "__main__":
    main()
