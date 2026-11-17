#!/usr/bin/env python3
"""
TikTok Shop ERP Token Refresh - LinkFox Skill (appType fixed to erp)

OPTIONAL manual refresh via /tiktokShop/refreshToken.

Business APIs should NOT call this first: /tiktokShop/developerProxy already
auto-refreshes on HTTP 401 / token expired|invalid and retries once.

Usage:
  python refresh_token.py '{"openId": "7010736057180325637"}'
"""

import json
import os
import sys
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

from _erp_auth import enforce_erp_app_type
from _lf_output import emit_result, lf_inline_flag


API_BASE_URL = (
    os.environ.get("LINKFOX_TOOL_GATEWAY")
    or os.environ.get("TIKTOK_SHOP_API_BASE_URL")
    or "https://tool-gateway.linkfox.com"
).rstrip("/")
API_ENDPOINT = f"{API_BASE_URL}/tiktokShop/refreshToken"


def get_api_key():
    """
获取配置在环境变量的API Key。
如果获取不到，按 SKILL.md 的 **## 解决认证和积分问题** 处理。
"""
    key = os.environ.get("LINKFOX_AGENT_API_KEY") or os.environ.get("LINKFOXAGENT_API_KEY")
    if not key:
        print(
            "API Key 未配置",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def call_api(params: dict) -> dict:
    """Call the refresh token API."""
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
        print("Error: 'openId' parameter is required (seller open_id)", file=sys.stderr)
        sys.exit(1)

    params = enforce_erp_app_type(params)
    result = call_api(params)

    # Mask tokens in output for security.
    if "accessToken" in result:
        result["accessToken"] = mask(result["accessToken"])
    if "refreshToken" in result:
        result["refreshToken"] = mask(result["refreshToken"])

    emit_result(result, lf_inline_flag())

    if "message" in result:
        print(f"\n✓ {result['message']}", file=sys.stderr)
        print(
            "Note: tokens are masked here; full tokens are stored in the database. "
            "Business APIs do not need this call — developerProxy auto-refreshes on 401. "
            "If refresh_token has expired, re-run the authorizeUrl flow.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
