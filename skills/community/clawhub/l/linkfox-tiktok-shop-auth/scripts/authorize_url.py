#!/usr/bin/env python3
"""
TikTok Shop ERP Authorization URL - LinkFox Skill (appType fixed to erp)
Calls the /tiktokShop/authorizeUrl endpoint to generate an authorization URL.

Usage:
  python authorize_url.py '{"shopName": "My Shop", "region": "us"}'
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
API_ENDPOINT = f"{API_BASE_URL}/tiktokShop/authorizeUrl"


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
    """Call the authorization URL API."""
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
    # Optional: shopName / region. appType is always forced to erp.
    params = {}
    if len(sys.argv) >= 2:
        try:
            params = json.loads(sys.argv[1])
        except json.JSONDecodeError as e:
            print(f"Invalid parameter format: {e}", file=sys.stderr)
            sys.exit(1)

    # Normalize shopName if present (display label only).
    if "shopName" in params and isinstance(params["shopName"], str):
        params["shopName"] = params["shopName"].strip()

    params = enforce_erp_app_type(params)
    result = call_api(params)
    emit_result(result, lf_inline_flag())

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
