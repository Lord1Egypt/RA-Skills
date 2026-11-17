#!/usr/bin/env python3
"""
TikTok Video Creator Authorization URL - LinkFox Skill
Calls the /tiktokVideo/authorizeUrl endpoint to generate a creator authorization URL.

Usage:
  python authorize_url.py '{"displayName": "My Channel", "region": "global"}'
"""

import json
import os
import sys
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


API_BASE_URL = os.environ.get(
    "TIKTOK_VIDEO_API_BASE_URL", "https://tool-gateway.linkfox.com"
)
API_ENDPOINT = f"{API_BASE_URL}/tiktokVideo/authorizeUrl"


def get_api_key():
    key = os.environ.get("LINKFOXAGENT_API_KEY")
    if not key:
        print(
            "API Key not configured. Please set the environment variable:\n"
            "  export LINKFOXAGENT_API_KEY=your-key-here",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def call_api(params: dict) -> dict:
    api_key = get_api_key()
    data = json.dumps(params).encode("utf-8")

    req = Request(
        API_ENDPOINT,
        data=data,
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json",
            "User-Agent": "LinkFox-Skill/1.0",
        },
        method="POST",
    )

    try:
        with urlopen(req, timeout=150) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        return {"error": f"HTTP {e.code}: {e.reason}", "details": body}
    except URLError as e:
        return {"error": f"Connection failed: {e.reason}"}


def main():
    params = {}
    if len(sys.argv) >= 2:
        try:
            params = json.loads(sys.argv[1])
        except json.JSONDecodeError as e:
            print(f"Invalid parameter format: {e}", file=sys.stderr)
            sys.exit(1)

    if "displayName" in params and isinstance(params["displayName"], str):
        params["displayName"] = params["displayName"].strip()

    result = call_api(params)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if "authorizeUrl" in result:
        print("\n✓ Authorization URL generated successfully!", file=sys.stderr)
        print(
            "Please open the following URL in your browser to authorize "
            "(valid for ~1 hour):",
            file=sys.stderr,
        )
        print(f"\n  {result['authorizeUrl']}\n", file=sys.stderr)


if __name__ == "__main__":
    main()
