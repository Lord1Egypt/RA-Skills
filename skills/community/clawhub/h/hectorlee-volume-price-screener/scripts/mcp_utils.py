#!/usr/bin/env python3
"""MCP 工具函数 — tdx_data_provider / intraday 共享

提供: MCP 握手、SSE 解析、工具调用。消除 ~60 行重复代码。
"""

import json
import os
import time
from typing import Optional, Dict, Any

import requests

MCP_PROXY = "http://127.0.0.1:57400/mcp"

# 从 WorkBuddy 环境获取 auth header
def _load_auth_headers() -> Dict[str, str]:
    try:
        cfg = json.loads(os.environ.get("CODEBUDDY_MCP_CONFIG", "{}"))
        return dict(cfg["mcpServers"]["connector-proxy"]["headers"])
    except Exception:
        return {}

MCP_AUTH_HEADERS = _load_auth_headers()
REQUEST_TIMEOUT = 30


def parse_sse(text: str) -> Optional[dict]:
    """解析 SSE (Server-Sent Events) 格式响应"""
    if not text:
        return None
    for line in text.strip().split("\n"):
        line = line.strip()
        if line.startswith("data:"):
            data_str = line[5:].strip()
            if data_str:
                try:
                    return json.loads(data_str)
                except json.JSONDecodeError:
                    continue
    return None


class McpClient:
    """MCP JSON-RPC 客户端（单例、线程安全）

    用法:
        client = McpClient.get()
        result = client.call_tool("tdx-connector_tdx_kline", {"code": "688981", ...})
    """

    _instance: Optional["McpClient"] = None

    def __init__(self):
        self._session: Optional[requests.Session] = None
        self._initialized = False
        self._request_id = 0

    @classmethod
    def get(cls) -> "McpClient":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def session(self) -> Optional[requests.Session]:
        return self._session

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def init(self) -> bool:
        if self._initialized and self._session is not None:
            return True

        self._session = requests.Session()
        self._session.headers.update(MCP_AUTH_HEADERS)
        self._session.headers["Accept"] = "application/json, text/event-stream"

        try:
            resp = self._session.post(MCP_PROXY, json={
                "jsonrpc": "2.0", "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "volume-price-screener", "version": "3.5"},
                },
                "id": self._next_id(),
            }, timeout=10)
            if resp.status_code != 200:
                return False

            sid = resp.headers.get("mcp-session-id", "")
            if sid:
                self._session.headers["mcp-session-id"] = sid

            # initialized notification
            self._session.post(MCP_PROXY, json={
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
            }, timeout=5)

            self._initialized = True
            return True
        except Exception:
            return False

    def call_tool(self, tool_name: str, arguments: dict,
                  max_retries: int = 2) -> Optional[dict]:
        if not self.init() or self._session is None:
            return None

        for attempt in range(max_retries + 1):
            try:
                resp = self._session.post(MCP_PROXY, json={
                    "jsonrpc": "2.0", "method": "tools/call",
                    "params": {"name": tool_name, "arguments": arguments},
                    "id": self._next_id(),
                }, timeout=REQUEST_TIMEOUT)

                if resp.status_code == 400 and "not initialized" in resp.text.lower():
                    self._initialized = False
                    self.init()
                    time.sleep(0.5)
                    continue

                if resp.status_code not in (200, 202, 204):
                    if attempt < max_retries:
                        time.sleep(1)
                    continue

                text = resp.text.strip()
                if not text:
                    continue

                parsed = parse_sse(text)
                if parsed is None:
                    try:
                        parsed = json.loads(text)
                    except json.JSONDecodeError:
                        if attempt < max_retries:
                            time.sleep(1)
                        continue
                        return None

                if "error" in parsed:
                    if attempt < max_retries:
                        time.sleep(1)
                    continue
                    return None

                result = parsed.get("result", parsed)
                if not isinstance(result, dict):
                    result = parsed

                content = result.get("content", [])
                if content and len(content) > 0:
                    c = content[0]
                    if c.get("type") == "text":
                        raw = c["text"]
                        brace = raw.find("{")
                        if brace >= 0:
                            try:
                                return json.loads(raw[brace:])
                            except json.JSONDecodeError:
                                pass
                        return {"raw_text": raw}
                return result

            except Exception:
                if attempt < max_retries:
                    time.sleep(1)
                continue

        return None
