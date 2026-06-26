#!/usr/bin/env python3
"""
Baidu Web Search skill for OpenClaw.
基于百度千帆「百度搜索」 API：
https://cloud.baidu.com/doc/qianfan-api/s/Wmbq4z7e5
"""

import json
import os
import sys
from typing import Any

import requests


SEARCH_URL = "https://qianfan.baidubce.com/v2/ai_search/web_search"


def _build_body(req: dict) -> dict:
    """
    将简单的 JSON 请求转换为百度搜索 API 请求体。

    支持字段：
    - query: string, 必填，搜索关键词
    - edition: string, 可选，standard / lite
    - top_k: int, 可选，网页返回条数，默认 20
    - sites: array<string>, 可选，仅在指定站点中搜索
    - search_recency_filter: string, 可选，week/month/semiyear/year
    - safe_search: bool, 可选
    - raw_resource_type_filter: object, 可选，直接覆盖 resource_type_filter
    - search_filter: object, 可选，直接传递给 search_filter
    """
    query = (req.get("query") or "").strip()
    if not query:
        return {"error": "missing_param", "message": "query is required"}

    edition = (req.get("edition") or "").strip()
    top_k = req.get("top_k", 20)
    try:
        top_k_int = int(top_k)
    except Exception:
        top_k_int = 20

    body: dict[str, Any] = {
        "messages": [
            {
                "role": "user",
                "content": query,
            }
        ],
        "search_source": "baidu_search_v2",
    }

    if edition:
        body["edition"] = edition

    # resource_type_filter：默认只取网页
    if "raw_resource_type_filter" in req and req["raw_resource_type_filter"]:
        body["resource_type_filter"] = req["raw_resource_type_filter"]
    else:
        body["resource_type_filter"] = [{"type": "web", "top_k": top_k_int}]

    # search_filter：简化封装 site -> match.site
    search_filter: dict[str, Any] = req.get("search_filter") or {}
    sites = req.get("sites")
    if sites:
        if not isinstance(search_filter, dict):
            search_filter = {}
        match = search_filter.get("match") or {}
        match["site"] = sites
        search_filter["match"] = match
    if search_filter:
        body["search_filter"] = search_filter

    search_recency_filter = (req.get("search_recency_filter") or "").strip()
    if search_recency_filter:
        body["search_recency_filter"] = search_recency_filter

    if "safe_search" in req:
        body["safe_search"] = bool(req["safe_search"])

    config_id = (req.get("config_id") or "").strip()
    if config_id:
        body["config_id"] = config_id

    return body


def baidu_search(api_key: str, req: dict) -> Any:
    body = _build_body(req)
    if isinstance(body, dict) and body.get("error"):
        return body

    headers = {
        # 文档示例使用 X-Appbuilder-Authorization 头
        "X-Appbuilder-Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(SEARCH_URL, headers=headers, json=body, timeout=20)
    except Exception as e:
        return {"error": "request_failed", "message": str(e)}

    if resp.status_code != 200:
        return {
            "error": "http_error",
            "status_code": resp.status_code,
            "body": resp.text,
        }

    try:
        data = resp.json()
    except Exception:
        return {"error": "invalid_json", "body": resp.text}

    # 错误响应示例中包含 code/message
    if isinstance(data, dict) and data.get("code"):
        return {
            "error": "api_error",
            "code": data.get("code"),
            "message": data.get("message"),
            "request_id": data.get("requestId") or data.get("request_id"),
        }

    return data


def _read_json_arg() -> dict:
    if len(sys.argv) < 3 or not sys.argv[2].strip():
        return {}
    raw = sys.argv[2]
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(obj, dict):
        print("Error: JSON body must be an object.", file=sys.stderr)
        sys.exit(1)
    return obj


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  baidu.py search '{\"query\":\"北京有哪些旅游景区\"}'\n"
            "  baidu.py search '{\"query\":\"北京天气\",\"top_k\":5,\"search_recency_filter\":\"week\"}'",
            file=sys.stderr,
        )
        sys.exit(1)

    api_key = os.getenv("BAIDU_API_KEY")
    if not api_key:
        print("Error: BAIDU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].strip().lower()
    req = _read_json_arg()

    if cmd == "search":
        result = baidu_search(api_key, req)
    else:
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

