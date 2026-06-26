#!/usr/bin/env python3
"""
EHunt Etsy 商品查询 — LinkFox Skill
POST JSON 到 tool-gateway（默认路径段见 DEFAULT_PATH）。

Usage:
  python ehunt_etsy_product_query.py '{"searchKey": "mug", "currencyCode": "USD", "page": 1, "pageSize": 20}'

环境变量：
  LINKFOXAGENT_API_KEY   必填，网关鉴权
  LINKFOX_EHUNT_PRODUCT_QUERY_PATH  可选，覆盖默认路径段
"""

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = os.environ.get(
    "LINKFOX_TOOL_GATEWAY_BASE", "https://tool-gateway.linkfox.com"
).rstrip("/")
DEFAULT_PATH = "ehunt/productQuery"
API_PATH = os.environ.get("LINKFOX_EHUNT_PRODUCT_QUERY_PATH", DEFAULT_PATH).strip("/")


def get_api_key() -> str:
    key = os.environ.get("LINKFOXAGENT_API_KEY")
    if not key:
        print(
            "未配置 API Key。请先申请并设置环境变量：\n"
            "  export LINKFOXAGENT_API_KEY=<your-key>\n"
            "申请说明见飞书文档（与其他 linkfox-* skill 一致）。",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def call_api(params: dict) -> dict:
    api_key = get_api_key()
    url = f"{BASE_URL}/{API_PATH}"
    data = json.dumps(params).encode("utf-8")
    req = Request(
        url,
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
        return {"error": f"HTTP {e.code}: {e.reason}", "details": body, "url": url}
    except URLError as e:
        return {"error": f"Connection failed: {e.reason}", "url": url}


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: ehunt_etsy_product_query.py '<JSON 参数>'\n"
            "Example: ehunt_etsy_product_query.py '{\"searchKey\": \"poster\", \"page\": 1}'",
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        params = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}", file=sys.stderr)
        sys.exit(1)
    result = call_api(params)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
