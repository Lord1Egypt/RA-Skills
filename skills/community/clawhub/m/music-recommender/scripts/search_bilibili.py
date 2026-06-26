#!/usr/bin/env python3
"""Search Bilibili for a music video.

Usage: python3 search_bilibili.py "<search query>"

Output: BV_ID|TITLE|URL (first result)
"""

import json
import sys
import urllib.parse
import urllib.request


def search_bilibili(query: str) -> str:
    encoded = urllib.parse.quote(query)
    url = f"https://api.bilibili.com/x/web-interface/search/all/v2?keyword={encoded}&page=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.bilibili.com/",
    }
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req, timeout=10)
    data = json.loads(resp.read())

    results = data.get("data", {}).get("result", [])
    for r in results:
        if r.get("result_type") == "video":
            videos = r.get("data", [])
            if videos:
                v = videos[0]
                bvid = v.get("bvid", "")
                title = v.get("title", "").replace('<em class="keyword">', "").replace("</em>", "")
                return f"{bvid}|{title}|https://www.bilibili.com/video/{bvid}"

    return "NOT_FOUND||"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 search_bilibili.py '<query>'", file=sys.stderr)
        sys.exit(1)

    result = search_bilibili(sys.argv[1])
    print(result)
