#!/usr/bin/env python3
"""Fetch top stories from the Hacker News RSS feed."""

import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from argparse import ArgumentParser
from urllib.error import URLError
from urllib.parse import urlparse

HN_RSS_URL = "https://hnrss.org/frontpage"


def fetch_hn_stories(limit: int = 20) -> list:
    try:
        req = urllib.request.Request(
            HN_RSS_URL,
            headers={"User-Agent": "hn-morning-brief/1.0"},
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
    except URLError as e:
        print(json.dumps({"error": f"Failed to fetch HN RSS: {e}"}))
        sys.exit(1)

    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        print(json.dumps({"error": f"Failed to parse RSS XML: {e}"}))
        sys.exit(1)

    channel = root.find("channel")
    if channel is None:
        print(json.dumps({"error": "No channel found in RSS feed"}))
        sys.exit(1)

    items = []
    for item in channel.findall("item")[:limit]:
        title = (item.findtext("title") or "").strip()
        article_url = (item.findtext("link") or "").strip()
        hn_url = (item.findtext("comments") or "").strip()
        description = (item.findtext("description") or "").strip()
        author = (item.findtext("{http://purl.org/dc/elements/1.1/}creator") or "").strip()

        # Parse points and comment count from description HTML
        # e.g. <p>Points: 426</p>  <p># Comments: 225</p>
        points_match = re.search(r"Points:\s*(\d+)", description)
        comments_match = re.search(r"#\s*Comments:\s*(\d+)", description)
        points = int(points_match.group(1)) if points_match else 0
        num_comments = int(comments_match.group(1)) if comments_match else 0

        domain = ""
        if article_url:
            try:
                domain = urlparse(article_url).netloc.replace("www.", "")
            except Exception:
                pass

        # Some HN items (Ask HN, Show HN) link directly to HN — use hn_url as article_url
        if not article_url and hn_url:
            article_url = hn_url

        items.append({
            "title": title,
            "article_url": article_url,
            "hn_url": hn_url,
            "domain": domain,
            "author": author,
            "points": points,
            "num_comments": num_comments,
        })

    return items


def main():
    parser = ArgumentParser(description="Fetch top Hacker News stories from RSS")
    parser.add_argument("--limit", type=int, default=20, help="Number of stories to fetch (default: 20)")
    args = parser.parse_args()

    stories = fetch_hn_stories(args.limit)
    print(json.dumps(stories, indent=2))


if __name__ == "__main__":
    main()
