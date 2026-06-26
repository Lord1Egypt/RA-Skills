#!/usr/bin/env python3
import os
import sys
import json
import argparse
import urllib.request
import urllib.error

ENDPOINTS = {
    "search": "https://google.serper.dev/search",
    "images": "https://google.serper.dev/images",
    "videos": "https://google.serper.dev/videos",
    "places": "https://google.serper.dev/places",
    "maps": "https://google.serper.dev/maps",
    "reviews": "https://google.serper.dev/reviews",
    "news": "https://google.serper.dev/news",
    "shopping": "https://google.serper.dev/shopping",
    "lens": "https://google.serper.dev/lens",
    "scholar": "https://google.serper.dev/scholar",
    "patents": "https://google.serper.dev/patents",
    "autocomplete": "https://google.serper.dev/autocomplete",
}

ALIASES = {
    "web": "search",
    "image": "images",
    "img": "images",
}

def search(query, search_type="search", gl=None, hl=None, tbs=None):
    api_key = os.environ.get("SERPER_API_KEY")
    if not api_key:
        return {"error": "SERPER_API_KEY environment variable not set"}

    search_type = ALIASES.get(search_type, search_type)
    endpoint = ENDPOINTS.get(search_type)
    if not endpoint:
        return {"error": f"Unsupported search type: {search_type}"}

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    payload = {"q": query}
    if gl:
        payload["gl"] = gl
    if hl:
        payload["hl"] = hl
    if tbs:
        payload["tbs"] = tbs

    data = json.dumps(payload).encode("utf-8")

    try:
        req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serper API search")
    parser.add_argument("query", help="search query")
    parser.add_argument(
        "--type",
        default="search",
        choices=sorted(ENDPOINTS.keys()) + sorted(ALIASES.keys()),
        help="search type",
    )
    parser.add_argument("--gl", help="country code (ISO 3166-1 alpha-2)")
    parser.add_argument("--hl", help="language code")
    parser.add_argument("--tbs", help="time range (e.g. past 24 hours, past week)")
    args = parser.parse_args()

    tbs_map = {
        "any time": None,
        "past hour": "qdr:h",
        "past 24 hours": "qdr:d",
        "past week": "qdr:w",
        "past month": "qdr:m",
        "past year": "qdr:y",
    }
    tbs_val = tbs_map.get(args.tbs.lower()) if args.tbs else args.tbs

    result = search(args.query, args.type, gl=args.gl, hl=args.hl, tbs=tbs_val)
    print(json.dumps(result, indent=2, ensure_ascii=False))
