#!/usr/bin/env python3
"""
TikTok 达人（Creator）接口代理 - LinkFox Skill
经 LinkFox 网关 /tiktokShop/developerProxy 转发至紫鸟 → TikTok Shop 达人(affiliate_creator)接口。

Usage:
  python creator_proxy.py '{"path": "affiliate_creator/202508/profiles", "method": "GET", "ttsAccessToken": "TTP_xxx"}'

参数（JSON）：
  path           必填，TikTok Shop API 相对路径（不含 tiktok-proxy 前缀），如 affiliate_creator/202508/profiles
  method         必填，GET / POST / PUT / DELETE
  ttsAccessToken 必填，达人 access_token（user_type=1，由 linkfox-tiktok-auth 以 appType=creator 授权获得）
  queryString    可选，查询字符串（不含 ?）
  body           可选，POST/PUT 请求体（JSON 字符串）
  appType        可选，代理侧应用类型；达人接口默认/须传 creator
  region         可选，默认 global
  contentType    可选，默认 application/json

环境变量：
  LINKFOXAGENT_API_KEY        必填，网关鉴权
  TIKTOK_SHOP_API_BASE_URL    可选，覆盖网关根 URL
"""

import json
import os
import sys
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


API_BASE_URL = os.environ.get(
    "TIKTOK_SHOP_API_BASE_URL", "https://tool-gateway.linkfox.com"
)
API_ENDPOINT = f"{API_BASE_URL}/tiktokShop/developerProxy"


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
        with urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        return {"error": f"HTTP {e.code}: {e.reason}", "details": body}
    except URLError as e:
        return {"error": f"Connection failed: {e.reason}"}


def main():
    if len(sys.argv) < 2:
        print("Usage: creator_proxy.py '<JSON parameters>'", file=sys.stderr)
        print(
            'Example: creator_proxy.py \'{"path": "affiliate_creator/202508/profiles", '
            '"method": "GET", "ttsAccessToken": "TTP_xxx"}\'',
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        params = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"Invalid parameter format: {e}", file=sys.stderr)
        sys.exit(1)

    for field in ("path", "method", "ttsAccessToken"):
        val = params.get(field)
        if not isinstance(val, str) or not val.strip():
            print(f"Error: '{field}' parameter is required", file=sys.stderr)
            sys.exit(1)

    # 达人(affiliate_creator)接口须以 appType=creator 走代理；未显式指定时默认 creator。
    params.setdefault("appType", "creator")

    result = call_api(params)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
