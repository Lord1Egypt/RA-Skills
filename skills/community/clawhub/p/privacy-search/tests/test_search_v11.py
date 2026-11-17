#!/usr/bin/env python3
"""
V1.1 新引擎测试
测试 Yandex/Startpage/Qwant/Brave 适配器和错误分类功能
"""

import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import sys
import os

# 不生成 __pycache__（死规则 13）
sys.dont_write_bytecode = True

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from search import (
    YandexAdapter, StartpageAdapter, QwantAdapter, BraveAdapter,
    EngineManager, SearchOrchestrator, STRICT_FALLBACK_ENGINES,
    classify_error, ErrorCategory, ClassifiedError,
    format_error_report,
)


class TestNewEngines(unittest.TestCase):
    """测试 V1.1 新增的 4 个国内备选引擎"""

    def test_yandex_adapter_name(self):
        adapter = YandexAdapter()
        self.assertEqual(adapter.name, "yandex")

    def test_startpage_adapter_name(self):
        adapter = StartpageAdapter()
        self.assertEqual(adapter.name, "startpage")

    def test_qwant_adapter_name(self):
        adapter = QwantAdapter()
        self.assertEqual(adapter.name, "qwant")

    def test_brave_adapter_name(self):
        adapter = BraveAdapter()
        self.assertEqual(adapter.name, "brave")

    def test_yandex_request_params(self):
        """Yandex 适配器请求参数验证"""
        async def _test():
            adapter = YandexAdapter()
            mock_response = AsyncMock()
            mock_response.text = AsyncMock(return_value="<html><body></body></html>")
            mock_response.status = 200
            mock_session = AsyncMock()
            mock_session.get = MagicMock()
            mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
            mock_session.get.return_value.__aexit__ = AsyncMock(return_value=False)
            await adapter.search(mock_session, "test query")
            call_args = mock_session.get.call_args
            url = call_args[0][0]
            self.assertIn("text=test", url.replace("+", "%20"))  # query 参数
        
        asyncio.run(_test())

    def test_normal_mode_keeps_cookie_policy(self):
        """normal 模式不强制移除 Cookie，但仍带 User-Agent"""
        from privacy import PrivacyManager

        pm = PrivacyManager({"privacy": {"default_mode": "normal"}})
        pm.set_mode_silent("normal")
        ctx = pm.build_request_context()
        self.assertIn("User-Agent", ctx.headers)

    def test_all_engines_share_privacy_headers(self):
        """
        全部引擎共享同一套隐私请求头

        V1.1 时各适配器自行拼装 headers，只有部分带 DNT。
        V1.2 收归统一出口后，隐私设置对所有引擎一致生效。
        """
        from privacy import PrivacyManager
        from engines_registry import all_engine_names

        pm = PrivacyManager({"privacy": {"default_mode": "strict"}})
        pm.set_mode_silent("strict")
        ctx = pm.build_request_context()

        self.assertEqual(ctx.headers.get("DNT"), "1")
        self.assertNotIn("Cookie", ctx.headers)
        self.assertNotIn("Referer", ctx.headers)

        # 该上下文不区分引擎，对全部 10 个引擎适用
        self.assertEqual(len(all_engine_names()), 10)

    def test_adapters_build_url(self):
        """适配器只需构造 URL，查询词应被正确编码"""
        for adapter in (YandexAdapter(), StartpageAdapter(), QwantAdapter(), BraveAdapter()):
            url = adapter.build_url("test query", 10)
            self.assertTrue(url.startswith("http"), f"{adapter.name} URL 应为绝对地址")
            self.assertNotIn(" ", url, f"{adapter.name} URL 不应含未编码空格")


class TestErrorClassification(unittest.TestCase):
    """测试错误分类功能"""

    def test_network_timeout(self):
        import aiohttp
        err = classify_error("test_engine", aiohttp.ServerTimeoutError("timeout"))
        self.assertEqual(err.category, ErrorCategory.NETWORK)
        self.assertEqual(err.engine, "test_engine")
        self.assertTrue(any("网络" in ts for ts in err.troubleshooting))

    def test_network_connection_error(self):
        err = classify_error("baidu", TimeoutError("connection timed out"))
        self.assertEqual(err.category, ErrorCategory.NETWORK)

    def test_config_key_error(self):
        err = classify_error("test", KeyError("missing_key"))
        self.assertEqual(err.category, ErrorCategory.CONFIG)
        self.assertTrue(any("config.yaml" in ts for ts in err.troubleshooting))

    def test_config_value_error(self):
        err = classify_error("test", ValueError("invalid value"))
        self.assertEqual(err.category, ErrorCategory.CONFIG)

    def test_engine_parser_error(self):
        err = classify_error("baidu", Exception("HTML parser error: cannot find 'div.result'"))
        self.assertEqual(err.category, ErrorCategory.ENGINE)
        self.assertTrue(any("页面结构" in ts for ts in err.troubleshooting))

    def test_generic_exception_is_engine(self):
        """通用 Exception 应归类为引擎错误"""
        err = classify_error("unknown", Exception("something went wrong"))
        self.assertEqual(err.category, ErrorCategory.ENGINE)


class TestFormatErrorReport(unittest.TestCase):
    """测试错误报告格式化"""

    def test_empty_errors(self):
        report = format_error_report([])
        self.assertEqual(report, "")

    def test_network_error_report(self):
        errors = [
            classify_error("baidu", TimeoutError("connection timed out")),
            classify_error("bing", ConnectionRefusedError("connection refused")),
        ]
        report = format_error_report(errors)
        self.assertIn("网络", report)
        self.assertIn("baidu", report)
        self.assertIn("bing", report)

    def test_mixed_error_report(self):
        errors = [
            classify_error("baidu", KeyError("missing")),
            classify_error("bing", TimeoutError("connection timed out")),
        ]
        report = format_error_report(errors)
        self.assertIn("配置", report)
        self.assertIn("网络", report)


class TestEngineManager(unittest.TestCase):
    """测试引擎管理器"""

    def test_init_all_engines(self):
        """EngineManager 现接收 SearXNG base_url，按名取适配器"""
        em = EngineManager("http://127.0.0.1:8888")
        for name in ("yandex", "startpage", "qwant", "brave", "duckduckgo", "searxng"):
            self.assertIsNotNone(em.get_adapter(name), f"{name} 适配器应存在")

    def test_registry_covers_all_adapters(self):
        """注册表与适配器实现必须一一对应，避免清单漂移"""
        from engines_registry import all_engine_names

        em = EngineManager("http://127.0.0.1:8888")
        for name in all_engine_names():
            self.assertIsNotNone(
                em.get_adapter(name),
                f"注册表声明了 {name} 但没有对应适配器实现",
            )

    def test_strict_fallback_engines_list(self):
        """验证 strict 模式备用引擎列表包含国内可用引擎"""
        for name in ("yandex", "startpage", "qwant", "brave", "duckduckgo"):
            self.assertIn(name, STRICT_FALLBACK_ENGINES)
        # 隐私保护不足的引擎不得出现在 strict 备选中
        for name in ("baidu", "bing", "sogou", "360"):
            self.assertNotIn(name, STRICT_FALLBACK_ENGINES)


class TestSearchOrchestratorErrors(unittest.TestCase):
    """测试编排器错误收集"""

    def test_orchestrator_has_error_list(self):
        config = {
            "searxng": {"host": "127.0.0.1", "port": 8888},
            "search": {"default_engines": ["baidu"]},
            "privacy": {"default_mode": "normal"},
        }
        orch = SearchOrchestrator(config)
        self.assertIsInstance(orch.classified_errors, list)

    def test_error_list_starts_empty(self):
        config = {
            "searxng": {"host": "127.0.0.1", "port": 8888},
            "search": {"default_engines": []},
            "privacy": {"default_mode": "strict", "strict": {"allowed_engines": []}},
        }
        orch = SearchOrchestrator(config)
        self.assertEqual(len(orch.classified_errors), 0)


if __name__ == "__main__":
    unittest.main()
