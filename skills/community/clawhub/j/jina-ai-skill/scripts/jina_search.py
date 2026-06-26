#!/usr/bin/env python3
"""
Jina Search - Search the web via s.jina.ai and return markdown results
Usage: python3 jina_search.py <query> [--json] [--results N]
"""

import sys
import os
import urllib.request
import urllib.parse
import json

def search(query, as_json=False, max_results=5):
    api_key = os.environ.get("JINA_API_KEY", "")
    encoded_query = urllib.parse.quote(query)
    endpoint = f"https://s.jina.ai/{encoded_query}"

    headers = {
        "Accept": "application/json" if as_json else "text/plain",
        "X-Return-Format": "markdown",
        "User-Agent": "Mozilla/5.0",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    req = urllib.request.Request(endpoint, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")

    if as_json:
        data = json.loads(body)
        # Trim to max_results if data is a list
        if isinstance(data, dict) and "data" in data:
            data["data"] = data["data"][:max_results]
        return data
    return body

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 jina_search.py <query> [--json] [--results N]")
        sys.exit(1)

    args = sys.argv[1:]
    as_json = "--json" in args
    if "--json" in args:
        args.remove("--json")

    max_results = 5
    if "--results" in args:
        idx = args.index("--results")
        max_results = int(args[idx + 1])
        args.pop(idx + 1)
        args.pop(idx)

    query = " ".join(args)

    result = search(query, as_json=as_json, max_results=max_results)

    if as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(result)
