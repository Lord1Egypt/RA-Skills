#!/usr/bin/env python3
"""
TikTok Video Token Refresh - LinkFox Skill
Calls the /tiktokVideo/refreshToken endpoint to refresh the access token.

Usage:
  python refresh_token.py '{"openId": "7010736057180325637"}'
"""

import json
import os
import sys
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


API_BASE_URL = os.environ.get(
    "TIKTOK_VIDEO_API_BASE_URL", "https://tool-gateway.linkfox.com"
)
API_ENDPOINT = f"{API_BASE_URL}/tiktokVideo/refreshToken"


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


def mask(token):
    if isinstance(token, str) and len(token) > 10:
        return token[:10] + "..."
    return token


def main():
    if len(sys.argv) < 2:
        print("Usage: refresh_token.py '<JSON parameters>'", file=sys.stderr)
        print(
            'Example: refresh_token.py \'{"openId": "7010736057180325637"}\'',
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        params = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"Invalid parameter format: {e}", file=sys.stderr)
        sys.exit(1)

    open_id = params.get("openId")
    if not isinstance(open_id, str) or not open_id.strip():
        print("Error: 'openId' parameter is required (creator open_id)", file=sys.stderr)
        sys.exit(1)

    result = call_api(params)

    if "accessToken" in result:
        result["accessToken"] = mask(result["accessToken"])
    if "refreshToken" in result:
        result["refreshToken"] = mask(result["refreshToken"])

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if "message" in result:
        print(f"\n✓ {result['message']}", file=sys.stderr)
        print(
            "Note: tokens are masked here; full tokens are stored in the database. "
            "If refresh_token has expired, re-run the authorizeUrl flow.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
