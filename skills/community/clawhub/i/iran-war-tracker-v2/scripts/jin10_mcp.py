#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金十数据 MCP 客户端（精简版）

用于 Skill 脚本独立调用金十 MCP 服务获取行情和快讯。
不依赖外部项目代码。
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from typing import Any

import httpx


JIN10_SERVER_URL = "https://mcp.jin10.com/mcp"
JIN10_PROTOCOL_VERSION = "2025-11-25"
# 金十公开 token，与 ch-topic-researcher 项目保持一致
JIN10_AUTH_TOKEN = "sk-z3u1AKwr3BZeSlp2l6DGQIx2x_Hq9Emhb-XQsZ0Btes"


class Jin10McpError(RuntimeError):
    pass


@dataclass
class JsonRpcResponse:
    result: dict[str, Any] | None = None
    error: dict[str, Any] | None = None


class Jin10McpClient:
    def __init__(self, server_url: str = JIN10_SERVER_URL, token: str = JIN10_AUTH_TOKEN):
        self.server_url = server_url
        self.token = token
        self.protocol_version = JIN10_PROTOCOL_VERSION
        self._http = httpx.Client(
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
            timeout=30.0,
        )
        self._initialized = False
        self._session_id: str | None = None

    def close(self) -> None:
        self._http.close()

    def ensure_initialized(self) -> None:
        if self._initialized:
            return
        self._request(
            "initialize",
            {
                "protocolVersion": self.protocol_version,
                "capabilities": {},
                "clientInfo": {"name": "iran-war-tracker-skill", "version": "1.2.0"},
            },
        )
        self._notify("notifications/initialized", {})
        self._initialized = True

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        self.ensure_initialized()
        result = self._request("tools/call", {"name": name, "arguments": arguments})
        if result.get("isError") is True:
            raise Jin10McpError(f"Tool business error: {name}")
        return result

    def get_quote(self, code: str) -> dict[str, Any]:
        result = self.call_tool("get_quote", {"code": code})
        return self._extract_structured_content(result)

    def search_flash(self, keyword: str) -> dict[str, Any]:
        result = self.call_tool("search_flash", {"keyword": keyword})
        return self._extract_structured_content(result)

    def search_news(self, keyword: str) -> dict[str, Any]:
        result = self.call_tool("search_news", {"keyword": keyword})
        return self._extract_structured_content(result)

    def list_flash(self, cursor: str | None = None) -> dict[str, Any]:
        arguments: dict[str, Any] = {}
        if cursor:
            arguments["cursor"] = cursor
        result = self.call_tool("list_flash", arguments)
        return self._extract_structured_content(result)

    def _extract_structured_content(self, result: dict[str, Any]) -> dict[str, Any]:
        structured = result.get("structuredContent")
        if isinstance(structured, dict):
            return structured
        raise Jin10McpError("Missing structuredContent in MCP result")

    def _notify(self, method: str, params: dict[str, Any]) -> None:
        payload = {"jsonrpc": "2.0", "method": method, "params": params}
        response = self._http.post(self.server_url, content=json.dumps(payload), headers=self._session_headers())
        response.raise_for_status()

    def _request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        payload = {
            "jsonrpc": "2.0",
            "id": uuid.uuid4().hex,
            "method": method,
            "params": params,
        }
        response = self._http.post(self.server_url, content=json.dumps(payload), headers=self._session_headers())
        response.raise_for_status()
        session_id = response.headers.get("mcp-session-id")
        if session_id:
            self._session_id = session_id
        data = self._decode_response_payload(response)
        if "error" in data:
            raise Jin10McpError(data["error"].get("message") or f"JSON-RPC error: {method}")
        return data.get("result", {})

    def _session_headers(self) -> dict[str, str]:
        if not self._session_id:
            return {}
        return {"mcp-session-id": self._session_id}

    def _decode_response_payload(self, response: httpx.Response) -> dict[str, Any]:
        content_type = (response.headers.get("content-type") or "").lower()
        if "text/event-stream" in content_type:
            return self._parse_sse_jsonrpc(response.text)
        return response.json()

    def _parse_sse_jsonrpc(self, body: str) -> dict[str, Any]:
        data_lines: list[str] = []
        for raw_line in body.splitlines():
            line = raw_line.strip()
            if line.startswith("data:"):
                data_lines.append(line[5:].strip())
        if not data_lines:
            raise Jin10McpError("Missing SSE data payload")
        payload = "\n".join(data_lines)
        return json.loads(payload)


# 金十支持的关注品种代码映射
JIN10_QUOTE_CODES = {
    "BRENT": "UKOIL",      # 布伦特原油
    "GOLD": "XAUUSD",      # 现货黄金
    "NATURAL_GAS": "NGAS", # 天然气
    "USD_CNY": "USDCNH",   # 美元/离岸人民币
}


def fetch_jin10_quotes(codes: list[str] | None = None) -> dict[str, dict[str, Any]]:
    """
    获取金十报价数据。

    Args:
        codes: 金十品种代码列表，如 ["UKOIL", "XAUUSD"]。
               为 None 时使用默认关注列表。

    Returns:
        {code: {name, open, close, high, low, volume, time, ...}}
    """
    target_codes = codes or list(JIN10_QUOTE_CODES.values())
    client = Jin10McpClient()
    results: dict[str, dict[str, Any]] = {}
    try:
        for code in target_codes:
            try:
                payload = client.get_quote(code)
                data = payload.get("data") or {}
                results[code] = {
                    "name": data.get("name") or code,
                    "code": data.get("code") or code,
                    "time": data.get("time") or "",
                    "open": data.get("open"),
                    "close": data.get("close"),
                    "high": data.get("high"),
                    "low": data.get("low"),
                    "volume": data.get("volume"),
                    "ups_price": data.get("ups_price"),
                    "ups_percent": data.get("ups_percent"),
                    "source": "jin10_mcp",
                }
            except Exception as exc:
                results[code] = {"_error": str(exc), "source": "jin10_mcp"}
    finally:
        client.close()
    return results


def fetch_jin10_flash(keyword: str, limit: int | None = None) -> list[dict[str, Any]]:
    """
    搜索金十快讯。

    Args:
        keyword: 搜索关键词，如 "伊朗"。
        limit: 最多返回条数。

    Returns:
        标准化后的快讯列表，每条包含 title, content, time, url。
    """
    client = Jin10McpClient()
    try:
        payload = client.search_flash(keyword)
        items = []
        for row in payload.get("data", {}).get("items", []):
            items.append({
                "title": row.get("title") or row.get("content") or "",
                "content": row.get("content") or row.get("title") or "",
                "time": row.get("time") or row.get("created_at") or "",
                "url": row.get("url") or "",
                "source": "jin10_flash",
            })
        if limit:
            items = items[:limit]
        return items
    finally:
        client.close()


if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    print("=== 金十 MCP 报价测试 ===")
    print(json.dumps(fetch_jin10_quotes(), ensure_ascii=False, indent=2))
    print("\n=== 金十 MCP 快讯测试 (keyword=伊朗) ===")
    print(json.dumps(fetch_jin10_flash("伊朗", limit=3), ensure_ascii=False, indent=2))
