#!/usr/bin/env python3
"""
Jina Reader - Fetch a URL and return its markdown content via r.jina.ai
Usage: python3 jina_read.py <url> [--no-images] [--json]
"""

import sys
import os
import urllib.request
import urllib.parse
import json

def read_url(url, no_images=False, as_json=False):
    api_key = os.environ.get("JINA_API_KEY", "")
    endpoint = f"https://r.jina.ai/{url}"

    headers = {
        "X-Return-Format": "markdown",
        "User-Agent": "Mozilla/5.0",
    }
    if as_json:
        headers["Accept"] = "application/json"
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    if no_images:
        headers["X-Remove-Selector"] = "img"

    req = urllib.request.Request(endpoint, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")

    if as_json:
        data = json.loads(body)
        return data
    return body

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 jina_read.py <url> [--no-images] [--json]")
        sys.exit(1)

    url = sys.argv[1]
    no_images = "--no-images" in sys.argv
    as_json = "--json" in sys.argv

    result = read_url(url, no_images=no_images, as_json=as_json)

    if as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(result)
