#!/usr/bin/env python3
"""
JisuAPI Agent skill for OpenClaw.
基于极速数据 Agent API：自然语言搜索工具 + 执行调用 + 统计。
文档：https://www.jisuapi.com/agent/docs/
"""

import json
import os
import sys
from typing import Any, Dict, Optional

import requests


BASE_URL = "https://api.jisuapi.com/agent"
TIMEOUT = 30


def _headers(appkey: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {appkey}",
        "Content-Type": "application/json",
    }


def _normalize_response(data: dict) -> dict:
    """兼容文档 result 与网关 data 两种成功载荷字段。"""
    if not isinstance(data, dict):
        return data
    if data.get("status") != 0:
        return data
    if "result" not in data and "data" in data:
        out = dict(data)
        out["result"] = data["data"]
        return out
    return data


def _post(appkey: str, path: str, body: Optional[dict] = None) -> dict:
    url = f"{BASE_URL}/{path.lstrip('/')}"
    try:
        resp = requests.post(url, headers=_headers(appkey), json=body or {}, timeout=TIMEOUT)
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

    data = _normalize_response(data)
    if data.get("status") != 0:
        return {
            "error": "api_error",
            "code": data.get("status"),
            "message": data.get("msg"),
            "raw": data,
        }
    return data


def _get(appkey: str, path: str, params: Optional[dict] = None) -> dict:
    url = f"{BASE_URL}/{path.lstrip('/')}"
    clean = {k: v for k, v in (params or {}).items() if v not in (None, "")}
    try:
        resp = requests.get(url, headers=_headers(appkey), params=clean, timeout=TIMEOUT)
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

    data = _normalize_response(data)
    if data.get("status") != 0:
        return {
            "error": "api_error",
            "code": data.get("status"),
            "message": data.get("msg"),
            "raw": data,
        }
    return data


def search_tools(appkey: str, req: dict) -> dict:
    """
    POST /agent/search — 自然语言搜索可用工具。
    必填 query；可选 limit(默认5,最大20)、category、search_mode(auto|llm|keyword)。
    """
    query = (req.get("query") or "").strip()
    category = (req.get("category") or "").strip()
    if not query and not category:
        return {"error": "missing_param", "message": "query or category is required"}

    body: Dict[str, Any] = {}
    if query:
        body["query"] = query
    if category:
        body["category"] = category
    if req.get("limit") is not None:
        body["limit"] = req["limit"]
    if req.get("search_mode"):
        body["search_mode"] = req["search_mode"]

    return _post(appkey, "search", body)


def execute_tool(appkey: str, req: dict) -> dict:
    """
    POST /agent/execute — 执行指定工具。
    必填 tool_id、params；可选 search_id、idempotency_key。
    """
    tool_id = (req.get("tool_id") or "").strip()
    if not tool_id:
        return {"error": "missing_param", "message": "tool_id is required"}

    params = req.get("params")
    if params is None:
        params = req.get("parameters")
    if params is None:
        params = {}
    if not isinstance(params, dict):
        return {"error": "missing_param", "message": "params must be an object"}

    body: Dict[str, Any] = {"tool_id": tool_id, "params": params}
    if req.get("search_id"):
        body["search_id"] = req["search_id"]
    if req.get("idempotency_key"):
        body["idempotency_key"] = req["idempotency_key"]

    return _post(appkey, "execute", body)


def run_query(appkey: str, req: dict) -> dict:
    """
    便捷流程：search → 选 match_score/score 最高工具 → execute。
    请求 JSON：
    {
      "query": "查询手机号归属地",
      "params": {"mobile": "13800138000"},
      "limit": 3,
      "tool_index": 0
    }
    """
    query = (req.get("query") or "").strip()
    if not query:
        return {"error": "missing_param", "message": "query is required"}

    search_req = {
        "query": query,
        "limit": req.get("limit", 5),
    }
    if req.get("category"):
        search_req["category"] = req["category"]
    if req.get("search_mode"):
        search_req["search_mode"] = req["search_mode"]

    search_resp = search_tools(appkey, search_req)
    if search_resp.get("error"):
        return {"step": "search", **search_resp}

    result = search_resp.get("result") or {}
    tools = result.get("tools") or []
    if not tools:
        return {
            "error": "no_tools",
            "message": "未找到匹配的工具",
            "search": search_resp,
        }

    tool_index = int(req.get("tool_index", 0))
    if tool_index < 0 or tool_index >= len(tools):
        tool_index = 0
    tool = tools[tool_index]

    tool_id = tool.get("tool_id") or tool.get("id")
    if not tool_id:
        return {
            "error": "invalid_tool",
            "message": "search result missing tool_id",
            "search": search_resp,
        }

    params = req.get("params") or {}
    if not isinstance(params, dict):
        params = {}

    exec_req = {
        "tool_id": tool_id,
        "params": params,
        "search_id": result.get("search_id"),
    }
    exec_resp = execute_tool(appkey, exec_req)
    if exec_resp.get("error"):
        return {
            "step": "execute",
            "selected_tool": tool,
            "search": search_resp,
            **exec_resp,
        }

    return {
        "selected_tool": tool,
        "search": search_resp,
        "execute": exec_resp,
    }


def query_stats(appkey: str, req: dict) -> dict:
    """POST /agent/stats — 执行统计（免费）。"""
    body = {}
    for key in ("start_date", "end_date", "tool_id", "group_by"):
        if req.get(key) not in (None, ""):
            body[key] = req[key]
    return _post(appkey, "stats", body)


def stats_detail(appkey: str, req: dict) -> dict:
    """GET /agent/stats/detail — 执行明细（免费）。"""
    params = {}
    for key in (
        "date",
        "start_date",
        "end_date",
        "tool_id",
        "success",
        "page",
        "page_size",
    ):
        if req.get(key) not in (None, ""):
            params[key] = req[key]
    return _get(appkey, "stats/detail", params)


def stats_dashboard(appkey: str, req: dict) -> dict:
    """GET /agent/stats/dashboard — 统计仪表盘（免费）。"""
    params = {}
    if req.get("date"):
        params["date"] = req["date"]
    return _get(appkey, "stats/dashboard", params)


def _parse_req(argv: list) -> dict:
    if not argv:
        return {}
    raw = argv[0].strip()
    if not raw:
        return {}
    if raw.startswith("{"):
        try:
            req = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}", file=sys.stderr)
            sys.exit(1)
        if not isinstance(req, dict):
            print("Error: request body must be a JSON object.", file=sys.stderr)
            sys.exit(1)
        return req
    return {"query": raw}


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  agent.py search '{\"query\":\"查询手机号归属地\",\"limit\":5}'\n"
            "  agent.py search 查询手机号归属地\n"
            "  agent.py execute '{\"tool_id\":\"shouji_query\",\"params\":{\"mobile\":\"13800138000\"}}'\n"
            "  agent.py run '{\"query\":\"查询手机号归属地\",\"params\":{\"mobile\":\"13800138000\"}}'\n"
            "  agent.py stats '{\"start_date\":\"2026-06-01\",\"end_date\":\"2026-06-03\"}'\n"
            "  agent.py stats_detail '{\"date\":\"2026-06-01\",\"page\":1,\"page_size\":20}'\n"
            "  agent.py stats_dashboard '{\"date\":\"2026-06-11\"}'",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()
    req = _parse_req(sys.argv[2:])

    if cmd == "search":
        result = search_tools(appkey, req)
    elif cmd == "execute":
        result = execute_tool(appkey, req)
    elif cmd == "run":
        result = run_query(appkey, req)
    elif cmd == "stats":
        result = query_stats(appkey, req)
    elif cmd in ("stats_detail", "detail"):
        result = stats_detail(appkey, req)
    elif cmd in ("stats_dashboard", "dashboard"):
        result = stats_dashboard(appkey, req)
    else:
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
