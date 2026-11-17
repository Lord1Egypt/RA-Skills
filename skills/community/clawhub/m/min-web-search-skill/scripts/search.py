#!/usr/bin/env python3
"""
min-web-search: Bing web search, no API key required.

Works on Linux / macOS / Windows (anywhere Python 3.8+ is available).
Uses Bing's public RSS endpoint — no authentication, no rate-limit keys.

Usage:
    python search.py "query"
    python search.py "query" --max 5
    python search.py "query" --json
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

BING_RSS = "https://www.bing.com/search?q={query}&format=rss"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def search(query: str, max_results: int = 5, timeout: int = 10) -> dict:
    """Search Bing via RSS and return parsed results."""
    url = BING_RSS.format(query=urllib.parse.quote(query))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            xml_data = resp.read().decode("utf-8")
    except (urllib.error.URLError, OSError) as e:
        return {"success": False, "error": str(e)}

    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        return {"success": False, "error": f"XML parse error: {e}"}

    results = []
    for item in root.findall(".//item"):
        title_el = item.find("title")
        link_el = item.find("link")
        desc_el = item.find("description")
        if title_el is None or link_el is None:
            continue
        title = (title_el.text or "").strip()
        link = (link_el.text or "").strip()
        snippet = ""
        if desc_el is not None and desc_el.text:
            snippet = re.sub(r"<[^>]+>", "", desc_el.text).strip()
        if title and link:
            results.append({"title": title, "url": link, "snippet": snippet})
        if len(results) >= max_results:
            break

    if not results:
        return {"success": False, "error": "No results returned"}
    return {"success": True, "query": query, "results": results}


def main() -> int:
    parser = argparse.ArgumentParser(description="Bing web search (no API key)")
    parser.add_argument("query", help="search query")
    parser.add_argument("--max", type=int, default=5, help="max results (default 5)")
    parser.add_argument("--json", action="store_true", help="output JSON")
    args = parser.parse_args()

    result = search(args.query, max_results=args.max)

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    elif result["success"]:
        for i, r in enumerate(result["results"], 1):
            print(f"{i}. {r['title']}")
            print(f"   {r['url']}")
            if r["snippet"]:
                print(f"   {r['snippet'][:200]}")
            print()
    else:
        print(f"ERROR: {result['error']}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
