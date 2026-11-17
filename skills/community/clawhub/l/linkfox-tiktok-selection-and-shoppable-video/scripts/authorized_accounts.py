#!/usr/bin/env python3
"""
TikTok Video Authorized Accounts List - LinkFox Skill
Calls the /tiktokVideo/authorizedAccounts endpoint to list authorized creator accounts.

Usage:
  python authorized_accounts.py
"""

import json
import os
import sys
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


API_BASE_URL = os.environ.get(
    "LINKFOX_TOOL_GATEWAY", "https://tool-gateway.linkfox.com"
)
API_ENDPOINT = f"{API_BASE_URL}/tiktokVideo/authorizedAccounts"


def get_api_key():
    """
获取配置在环境变量的API Key。
如果获取不到，按 SKILL.md 的 **## 解决认证和积分问题** 处理。
"""
    key = os.environ.get("LINKFOXAGENT_API_KEY")
    if not key:
        print(
            "API Key 未配置",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def call_api() -> dict:
    api_key = get_api_key()

    req = Request(
        API_ENDPOINT,
        data=b"{}",
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
    result = call_api()
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if "accounts" in result:
        accounts = result.get("accounts", [])
        total = result.get("total", 0)
        print(f"\n✓ Found {total} authorized account(s):", file=sys.stderr)
        for account in accounts:
            print(
                f"  - {account.get('displayName', 'N/A')} "
                f"(openId={account.get('openId')}) "
                f"[region={account.get('region')}, userType={account.get('userType')}]",
                file=sys.stderr,
            )


if __name__ == "__main__":
    main()
