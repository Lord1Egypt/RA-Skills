#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Server 功能测试（V1.7 新增）
覆盖：JSON-RPC 2.0 协议处理、工具 schema、工具调用、降级逻辑、超时控制
"""

import asyncio
import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch
from types import SimpleNamespace

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


# ============================================================
# JSON-RPC 2.0 协议处理测试
# ============================================================

class TestJsonRpcProtocol(unittest.TestCase):
    """JSON-RPC 2.0 消息读写"""

    def test_make_response(self):
        from mcp_server import _make_response
        resp = _make_response(1, {"key": "value"})
        self.assertEqual(resp["jsonrpc"], "2.0")
        self.assertEqual(resp["id"], 1)
        self.assertEqual(resp["result"]["key"], "value")

    def test_make_error(self):
        from mcp_server import _make_error
        err = _make_error(1, -32600, "Invalid request")
        self.assertEqual(err["jsonrpc"], "2.0")
        self.assertEqual(err["id"], 1)
        self.assertEqual(err["error"]["code"], -32600)
        self.assertEqual(err["error"]["message"], "Invalid request")

    def test_make_error_with_data(self):
        from mcp_server import _make_error
        err = _make_error(1, -32603, "Internal error", {"detail": "stack trace"})
        self.assertEqual(err["error"]["data"]["detail"], "stack trace")


# ============================================================
# MCP 协议方法测试
# ============================================================

class TestMcpProtocol(unittest.TestCase):
    """MCP 协议方法处理"""

    def test_handle_initialize(self):
        from mcp_server import _handle_initialize
        result = _handle_initialize({})
        self.assertIn("protocolVersion", result)
        self.assertIn("capabilities", result)
        self.assertIn("serverInfo", result)
        self.assertEqual(result["serverInfo"]["name"], "privacy-search")
        self.assertIn("version", result["serverInfo"])

    def test_handle_tools_list(self):
        from mcp_server import _handle_tools_list
        result = _handle_tools_list({}, {})
        self.assertIn("tools", result)
        tool_names = [t["name"] for t in result["tools"]]
        self.assertIn("search", tool_names)
        self.assertIn("synthesize", tool_names)
        self.assertIn("fetch", tool_names)

    def test_handle_tools_list_schema_format(self):
        from mcp_server import _handle_tools_list
        result = _handle_tools_list({}, {})
        for tool in result["tools"]:
            self.assertIn("name", tool)
            self.assertIn("description", tool)
            self.assertIn("inputSchema", tool)
            self.assertIn("type", tool["inputSchema"])
            self.assertIn("properties", tool["inputSchema"])

    def test_handle_request_initialize(self):
        from mcp_server import _handle_request
        request = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        response = _handle_request(request, {})
        self.assertEqual(response["id"], 1)
        self.assertIn("result", response)

    def test_handle_request_tools_list(self):
        from mcp_server import _handle_request
        request = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
        response = _handle_request(request, {})
        self.assertEqual(response["id"], 2)
        self.assertIn("tools", response["result"])

    def test_handle_request_unknown_method(self):
        from mcp_server import _handle_request
        request = {"jsonrpc": "2.0", "id": 3, "method": "unknown/method", "params": {}}
        response = _handle_request(request, {})
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32601)

    def test_handle_request_initialized_notification(self):
        from mcp_server import _handle_request
        request = {"jsonrpc": "2.0", "method": "notifications/initialized"}
        response = _handle_request(request, {})
        self.assertIsNone(response)  # 通知消息无需响应


# ============================================================
# 工具 Schema 测试
# ============================================================

class TestToolSchema(unittest.TestCase):
    """工具 schema 定义"""

    def test_search_schema_has_required_fields(self):
        from mcp_server import _get_tools_schema
        schema = _get_tools_schema({})
        search_tool = next(t for t in schema if t["name"] == "search")
        self.assertIn("query", search_tool["inputSchema"]["properties"])
        self.assertIn("query", search_tool["inputSchema"]["required"])

    def test_synthesize_schema_has_required_fields(self):
        from mcp_server import _get_tools_schema
        schema = _get_tools_schema({})
        synth_tool = next(t for t in schema if t["name"] == "synthesize")
        self.assertIn("query", synth_tool["inputSchema"]["properties"])
        self.assertIn("query", synth_tool["inputSchema"]["required"])

    def test_fetch_schema_has_required_fields(self):
        from mcp_server import _get_tools_schema
        schema = _get_tools_schema({})
        fetch_tool = next(t for t in schema if t["name"] == "fetch")
        self.assertIn("url", fetch_tool["inputSchema"]["properties"])
        self.assertIn("url", fetch_tool["inputSchema"]["required"])

    def test_search_schema_engines_enum(self):
        from mcp_server import _get_tools_schema
        schema = _get_tools_schema({})
        search_tool = next(t for t in schema if t["name"] == "search")
        engines_prop = search_tool["inputSchema"]["properties"]["engines"]
        self.assertEqual(engines_prop["type"], "array")

    def test_search_schema_privacy_enum(self):
        from mcp_server import _get_tools_schema
        schema = _get_tools_schema({})
        search_tool = next(t for t in schema if t["name"] == "search")
        privacy_prop = search_tool["inputSchema"]["properties"]["privacy"]
        self.assertEqual(privacy_prop["enum"], ["normal", "strict"])

    def test_tools_filter_config(self):
        """mcp_server.tools 可缩减暴露的工具子集"""
        from mcp_server import _get_tools_schema
        config = {"mcp_server": {"tools": ["search"]}}
        schema = _get_tools_schema(config)
        self.assertEqual(len(schema), 1)
        self.assertEqual(schema[0]["name"], "search")

    def test_tools_filter_none_returns_all(self):
        """mcp_server.tools 未配置时返回全部工具"""
        from mcp_server import _get_tools_schema
        schema = _get_tools_schema({})
        self.assertEqual(len(schema), 3)

    def test_tools_call_respects_filter(self):
        """tools/call 时未暴露的工具返回 METHOD_NOT_FOUND"""
        from mcp_server import _handle_tools_call
        config = {"mcp_server": {"tools": ["search"]}}
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(_handle_tools_call(
            {"name": "fetch", "arguments": {"url": "https://example.com"}},
            config
        ))
        self.assertIn("error", result)
        self.assertEqual(result["error"]["code"], -32601)
        loop.close()


# ============================================================
# search 工具调用测试
# ============================================================

class TestSearchTool(unittest.TestCase):
    """search 工具"""

    def test_search_empty_query(self):
        from mcp_server import _tool_search
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(_tool_search({"query": ""}, {}))
        self.assertIn("error", result)
        loop.close()

    def test_search_with_mock(self):
        from mcp_server import _tool_search
        with patch('search.SearchOrchestrator') as MockOrch:
            mock_instance = MagicMock()
            async def _mock_search(**kw): return []
            mock_instance.search = _mock_search
            mock_instance.notices = []
            mock_instance.cache_hit = False
            MockOrch.return_value = mock_instance
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(_tool_search({"query": "test", "num": 3}, {}))
            self.assertIn("results", result)
            self.assertIn("count", result)
            loop.close()


# ============================================================
# synthesize 工具调用测试
# ============================================================

class TestSynthesizeTool(unittest.TestCase):
    """synthesize 工具"""

    def test_synthesize_empty_query(self):
        from mcp_server import _tool_synthesize
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(_tool_synthesize({"query": ""}, {}))
        self.assertIn("error", result)
        loop.close()

    def test_synthesize_with_mock(self):
        from mcp_server import _tool_synthesize
        with patch('synthesiser.synthesize_pro') as mock_synth:
            mock_synth.return_value = "测试答案 [1]"
            with patch('search.SearchOrchestrator') as MockOrch:
                mock_instance = MagicMock()
                async def _mock_search(**kw): return []
                mock_instance.search = _mock_search
                mock_instance.notices = []
                mock_instance.cache_hit = False
                MockOrch.return_value = mock_instance
                loop = asyncio.new_event_loop()
                result = loop.run_until_complete(_tool_synthesize({"query": "测试", "max_sources": 3}, {}))
                self.assertIn("answer", result)
                loop.close()


# ============================================================
# fetch 工具调用测试
# ============================================================

class TestFetchTool(unittest.TestCase):
    """fetch 工具"""

    def test_fetch_empty_url(self):
        from mcp_server import _tool_fetch
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(_tool_fetch({"url": ""}, {}))
        self.assertIn("error", result)
        loop.close()

    def test_fetch_with_mock(self):
        from mcp_server import _tool_fetch
        with patch('page_fetcher.fetch_and_extract') as mock_fetch:
            mock_fetch.return_value = ("<html></html>", "正文内容")
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(_tool_fetch({"url": "https://example.com"}, {}))
            self.assertTrue(result["success"])
            self.assertEqual(result["text"], "正文内容")
            loop.close()

    def test_fetch_failure_with_mock(self):
        from mcp_server import _tool_fetch
        with patch('page_fetcher.fetch_and_extract') as mock_fetch:
            mock_fetch.return_value = (None, None)
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(_tool_fetch({"url": "https://example.com"}, {}))
            self.assertFalse(result["success"])
            loop.close()

    def test_fetch_exception_with_mock(self):
        from mcp_server import _tool_fetch
        with patch('page_fetcher.fetch_and_extract') as mock_fetch:
            mock_fetch.side_effect = Exception("网络错误")
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(_tool_fetch({"url": "https://example.com"}, {}))
            self.assertFalse(result["success"])
            self.assertIn("网络错误", result["error"])
            loop.close()


# ============================================================
# 超时与降级测试
# ============================================================

class TestTimeoutAndDegradation(unittest.TestCase):
    """超时控制与降级逻辑"""

    def test_timeout_error_handling(self):
        from mcp_server import _handle_tools_call, _TOOL_HANDLERS
        original = _TOOL_HANDLERS.get("search")
        try:
            async def _mock_timeout(*args, **kwargs):
                raise asyncio.TimeoutError
            _TOOL_HANDLERS["search"] = _mock_timeout
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(_handle_tools_call(
                {"name": "search", "arguments": {"query": "test"}},
                {"mcp_server": {"timeout": 1}}
            ))
            self.assertIn("error", result)
            self.assertIn("超时", result["error"]["message"])
            loop.close()
        finally:
            _TOOL_HANDLERS["search"] = original

    def test_internal_error_handling(self):
        from mcp_server import _handle_tools_call, _TOOL_HANDLERS
        original = _TOOL_HANDLERS.get("search")
        try:
            async def _mock_error(*args, **kwargs):
                raise Exception("未知错误")
            _TOOL_HANDLERS["search"] = _mock_error
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(_handle_tools_call(
                {"name": "search", "arguments": {"query": "test"}},
                {"mcp_server": {"timeout": 30}}
            ))
            self.assertIn("error", result)
            self.assertIn("未知错误", result["error"]["message"])
            loop.close()
        finally:
            _TOOL_HANDLERS["search"] = original

    def test_unknown_tool_error(self):
        from mcp_server import _handle_tools_call
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(_handle_tools_call(
            {"name": "unknown_tool", "arguments": {}},
            {}
        ))
        self.assertIn("error", result)
        self.assertEqual(result["error"]["code"], -32601)
        loop.close()


# ============================================================
# dont_write_bytecode 检查（死规则 13）
# ============================================================

class TestNoBytecode(unittest.TestCase):
    """新模块必须设置 dont_write_bytecode"""

    def test_mcp_server_has_dont_write_bytecode(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'mcp_server.py')
        with open(path, encoding='utf-8') as f:
            content = f.read()
        self.assertIn('dont_write_bytecode', content,
                      "mcp_server.py 必须设置 dont_write_bytecode")


if __name__ == "__main__":
    unittest.main(verbosity=2)
