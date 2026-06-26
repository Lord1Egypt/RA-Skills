#!/usr/bin/env python3
"""Fetch top trending searches on Google in the last 24h via Google Trends RSS."""

import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

GEO = sys.argv[1].upper() if len(sys.argv) > 1 else "US"
COUNT = int(sys.argv[2]) if len(sys.argv) > 2 else 20
URL = f"https://trends.google.com/trending/rss?geo={GEO}"

NS = {"ht": "https://trends.google.com/trending/rss"}

def fetch_feed(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; google-trending-skill/1.0)"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read()

def parse_items(data: bytes) -> list[dict]:
    root = ET.fromstring(data)
    items = []
    for item in root.findall(".//item"):
        title_el = item.find("title")
        traffic_el = item.find("ht:approx_traffic", NS)
        pubdate_el = item.find("pubDate")
        link_el = item.find("link")
        news_items = []
        for ni in item.findall("ht:news_item", NS):
            ni_title = ni.findtext("ht:news_item_title", default="", namespaces=NS)
            ni_url = ni.findtext("ht:news_item_url", default="", namespaces=NS)
            ni_source = ni.findtext("ht:news_item_source", default="", namespaces=NS)
            if ni_title:
                news_items.append({"title": ni_title, "url": ni_url, "source": ni_source})
        items.append({
            "title": title_el.text if title_el is not None else "?",
            "traffic": traffic_el.text if traffic_el is not None else "N/A",
            "pubdate": pubdate_el.text if pubdate_el is not None else "",
            "link": link_el.text if link_el is not None else "",
            "news": news_items[:2],
        })
    return items[:COUNT]

def main():
    print(f"🔥 Google Trending Searches — Last 24h  [{GEO}]")
    print(f"   {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print("━" * 52)
    try:
        data = fetch_feed(URL)
    except urllib.error.URLError as e:
        print(f"Error fetching feed: {e}", file=sys.stderr)
        sys.exit(1)

    items = parse_items(data)
    if not items:
        print("No trending items found.")
        sys.exit(0)

    for i, item in enumerate(items, 1):
        print(f"\n{i:>2}. {item['title']}")
        print(f"    🔍 {item['traffic']} searches")
        if item["pubdate"]:
            print(f"    🕒 {item['pubdate']}")
        for news in item["news"]:
            src = f"  [{news['source']}]" if news["source"] else ""
            print(f"    📰 {news['title'][:80]}{src}")
        if item["link"]:
            print(f"    🔗 {item['link']}")

    print(f"\n{'─'*52}")
    print(f"Source: trends.google.com  |  geo={GEO}  |  top {len(items)}")

if __name__ == "__main__":
    main()
