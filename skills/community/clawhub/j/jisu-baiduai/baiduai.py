#!/usr/bin/env python3
"""
BaiduAI intelligent search generation skill for OpenClaw.
基于百度千帆「智能搜索生成」 API：
https://cloud.baidu.com/doc/qianfan-api/s/Hmbu8m06u
"""

import json
import os
import sys
from typing import Any

import requests


CHAT_URL = "https://qianfan.baidubce.com/v2/ai_search/chat/completions"


def _build_body(req: dict) -> dict:
    """
    将简单 JSON 请求转换为智能搜索生成 API 的请求体。

    主要支持字段：
    - query: string, 必填，用户问题
    - model: string, 必填，模型名称，如 "ernie-4.5-turbo-32k" 或 "deepseek-r1,ernie-4.5-turbo-128k"
    - search_source: string, 可选，默认 "baidu_search_v2"
    - resource_type_filter: array<object>, 可选，覆盖资源过滤
    - top_k: int, 可选，快捷设置 web 结果条数（只在未显式设置 resource_type_filter 时生效）
    - types: array<string>, 可选，资源类型列表（web/image/video），只在未显式设置 resource_type_filter 时生效
    - search_recency_filter: string, 可选，week/month/semiyear/year
    - site: string, 可选，仅在一个站点内搜索
    - search_filter: object, 可选，直接透传 search_filter
    - search_mode: string, 可选，auto/required/disabled
    - enable_deep_search: bool, 可选，是否开启深度搜索
    - enable_reasoning: bool, 可选，仅 DeepSeek-R1、文心 X1 生效
    - response_format: string, 可选，auto/text/rich_text
    - temperature, top_p: float, 可选，采样参数
    - stream: bool, 可选，是否使用流式（本脚本仍以非流式方式接收）
    其余复杂字段（additional_knowledge 等）可通过 raw_body 直接覆盖。
    """
    if "raw_body" in req and isinstance(req["raw_body"], dict):
        return req["raw_body"]

    query = (req.get("query") or "").strip()
    if not query:
        return {"error": "missing_param", "message": "query is required"}

    model = (req.get("model") or "").strip()
    if not model:
        return {"error": "missing_param", "message": "model is required"}

    body: dict[str, Any] = {
        "messages": [
            {
                "role": "user",
                "content": query,
            }
        ],
        "model": model,
        "search_source": (req.get("search_source") or "baidu_search_v2").strip() or "baidu_search_v2",
    }

    # resource_type_filter：若用户未显式传入，则用 types/top_k 简化构造
    if "resource_type_filter" in req and req["resource_type_filter"]:
        body["resource_type_filter"] = req["resource_type_filter"]
    else:
        types = req.get("types") or ["web"]
        if not isinstance(types, list):
            types = ["web"]
        top_k = req.get("top_k", 10)
        try:
            top_k_int = int(top_k)
        except Exception:
            top_k_int = 10
        rtf = []
        for t in types:
            tt = str(t).strip()
            if not tt:
                continue
            rtf.append({"type": tt, "top_k": top_k_int})
        if rtf:
            body["resource_type_filter"] = rtf

    # search_filter：支持简化 site，并允许透传
    search_filter: dict[str, Any] = req.get("search_filter") or {}
    site = (req.get("site") or "").strip()
    if site:
        if not isinstance(search_filter, dict):
            search_filter = {}
        match = search_filter.get("match") or {}
        match["site"] = site
        search_filter["match"] = match
    if search_filter:
        body["search_filter"] = search_filter

    search_recency_filter = (req.get("search_recency_filter") or "").strip()
    if search_recency_filter:
        body["search_recency_filter"] = search_recency_filter

    # 直通的一些常用参数
    passthrough_keys = [
        "instruction",
        "temperature",
        "top_p",
        "search_mode",
        "enable_deep_search",
        "enable_reasoning",
        "response_format",
        "stream",
        "enable_followup_queries",
        "enable_corner_markers",
        "safety_level",
        "enable_web_page_safety",
        "max_completion_tokens",
        "max_refer_search_items",
        "enable_entity_selection_search",
    ]
    for k in passthrough_keys:
        if k in req and req[k] is not None:
            body[k] = req[k]

    # 允许用户直接传 additional_knowledge 等高级字段
    for k in ("additional_knowledge", "user_profile", "search_items_postprocess"):
        if k in req and req[k] is not None:
            body[k] = req[k]

    config_id = (req.get("config_id") or "").strip()
    if config_id:
        body["config_id"] = config_id

    return body


def baiduai_search(api_key: str, req: dict) -> Any:
    body = _build_body(req)
    if isinstance(body, dict) and body.get("error"):
        return body

    headers = {
        "X-Appbuilder-Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(CHAT_URL, headers=headers, json=body, timeout=40)
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
            "  baiduai.py ask '{\"query\":\"近日油价调整消息。\",\"model\":\"ernie-4.5-turbo-32k\"}'\n"
            "  baiduai.py ask '{\"query\":\"北京有哪些景点\",\"model\":\"ernie-4.5-turbo-32k\",\"search_recency_filter\":\"year\"}'",
            file=sys.stderr,
        )
        sys.exit(1)

    api_key = os.getenv("BAIDU_API_KEY")
    if not api_key:
        print("Error: BAIDU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].strip().lower()
    req = _read_json_arg()

    if cmd == "ask":
        result = baiduai_search(api_key, req)
    else:
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

