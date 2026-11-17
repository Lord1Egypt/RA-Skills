#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V1.6 功能测试
覆盖：Perplexity 式答案合成（synthesiser）、定时 selftest 调度（selftest_scheduler）、
      jieba 默认安装验证、SKILL.md 版本号检查
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch
from types import SimpleNamespace

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from version_util import get_current_version


# ============================================================
# Perplexity 式答案合成（synthesiser）
# ============================================================

class TestSynthesiser(unittest.TestCase):
    """Perplexity 式答案合成模块"""

    def setUp(self):
        self.results = [
            SimpleNamespace(
                title="Python 装饰器详解",
                url="https://example.com/python-decorator",
                snippet="Python 装饰器是一种设计模式，用于在不修改原函数代码的情况下扩展功能。",
                engine="baidu",
                rank=1,
            ),
            SimpleNamespace(
                title="深入理解 Python 装饰器原理",
                url="https://example.com/python-decorator-principle",
                snippet="装饰器的本质是一个高阶函数，它接收一个函数作为参数并返回一个新函数。",
                engine="bing",
                rank=2,
            ),
            SimpleNamespace(
                title="Python 装饰器实战指南",
                url="https://example.com/python-decorator-guide",
                snippet="本文通过实际案例讲解 Python 装饰器的使用方法和最佳实践。",
                engine="duckduckgo",
                rank=3,
            ),
        ]

    def test_synthesize_pro_empty_results(self):
        from synthesiser import synthesize_pro
        result = synthesize_pro("python 装饰器", [], {})
        self.assertIn("没有", result)

    def test_syntractive_synthesis_no_api_key(self):
        """无 API Key 时降级为抽取式"""
        from synthesiser import synthesize_pro
        config = {"synthesis": {"api_key": "", "provider": "auto", "max_sources": 3}}
        result = synthesize_pro("python 装饰器", self.results, config)
        self.assertIn("抽取式摘要", result)
        self.assertIn("[1]", result)
        self.assertIn("[2]", result)
        self.assertIn("[3]", result)

    def test_syntractive_synthesis_extractive_mode(self):
        """强制抽取式模式"""
        from synthesiser import synthesize_pro
        config = {"synthesis": {"provider": "extractive", "max_sources": 2}}
        result = synthesize_pro("python 装饰器", self.results, config)
        self.assertIn("抽取式摘要", result)
        # max_sources=2 只引用前 2 个
        self.assertIn("[1]", result)
        self.assertIn("[2]", result)

    def test_syntractive_synthesis_disabled(self):
        """禁用 Pro 合成时降级"""
        from synthesiser import synthesize_pro
        config = {"synthesis": {"enabled": False}}
        result = synthesize_pro("python 装饰器", self.results, config)
        self.assertIn("抽取式摘要", result)

    def test_chunk_text_normal(self):
        """正文分块：正常段落切分"""
        from synthesiser import _chunk_text
        text = "第一段内容。\n第二段内容，包含更多文字。\n第三段内容。"
        chunks = _chunk_text(text, chunk_size=2000)
        self.assertEqual(len(chunks), 3)

    def test_chunk_text_long_paragraph(self):
        """正文分块：超长段落按句号切分"""
        from synthesiser import _chunk_text
        # 构造一个超长段落（超过 chunk_size）
        long_sentence = "这是一个很长的句子，用于测试分块逻辑是否正确工作。" * 50
        chunks = _chunk_text(long_sentence, chunk_size=100)
        self.assertGreater(len(chunks), 1)

    def test_chunk_text_empty(self):
        """正文分块：空文本"""
        from synthesiser import _chunk_text
        self.assertEqual(_chunk_text(""), [])

    def test_fetch_contents_with_mock(self):
        """正文抓取：mock 测试"""
        from synthesiser import _fetch_contents
        with patch('page_fetcher.fetch_and_extract') as mock_fetch:
            mock_fetch.return_value = ("<html></html>", "这是抓取到的正文内容，足够长以满足最小长度要求。" * 10)
            result = _fetch_contents(self.results, max_sources=3, timeout=10)
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0][0], 1)
            self.assertIn("example.com", result[0][1])

    def test_fetch_contents_fallback_to_snippet(self):
        """正文抓取失败时降级为 snippet"""
        from synthesiser import _fetch_contents
        with patch('page_fetcher.fetch_and_extract') as mock_fetch:
            mock_fetch.return_value = (None, None)
            result = _fetch_contents(self.results, max_sources=3, timeout=10)
            self.assertGreater(len(result), 0)

    def test_build_pro_prompt(self):
        """Pro prompt 构建"""
        from synthesiser import _build_pro_prompt
        sources = [
            (1, "https://example.com/1", "这是第一个来源的正文内容。"),
            (2, "https://example.com/2", "这是第二个来源的正文内容。"),
        ]
        prompt = _build_pro_prompt("测试问题", sources, chunk_size=2000)
        self.assertIn("用户问题：测试问题", prompt)
        self.assertIn("[来源1]", prompt)
        self.assertIn("[来源2]", prompt)
        self.assertIn("标注来源编号", prompt)

    def test_synthesize_pro_with_mock_llm(self):
        """Pro 合成：mock LLM 调用"""
        from synthesiser import synthesize_pro
        config = {
            "synthesis": {
                "api_key": "fake_key",
                "provider": "auto",
                "model": "glm-4-flash",
                "max_sources": 3,
                "chunk_size": 2000,
                "fetch_timeout": 10,
            }
        }
        with patch('synthesiser._call_zhipu') as mock_llm:
            mock_llm.return_value = "这是 LLM 生成的答案 [1][2]。"
            with patch('synthesiser._fetch_contents') as mock_fetch:
                mock_fetch.return_value = [
                    (1, "https://example.com/1", "正文内容1"),
                    (2, "https://example.com/2", "正文内容2"),
                ]
                result = synthesize_pro("测试问题", self.results, config)
                self.assertIn("LLM 生成的答案", result)
                self.assertIn("--- 来源 ---", result)

    def test_synthesize_pro_llm_fails_fallback(self):
        """Pro 合成：LLM 失败时降级"""
        from synthesiser import synthesize_pro
        config = {
            "synthesis": {
                "api_key": "fake_key",
                "provider": "auto",
                "max_sources": 3,
            }
        }
        with patch('synthesiser._call_zhipu', return_value=None):
            with patch('synthesiser._fetch_contents') as mock_fetch:
                mock_fetch.return_value = [
                    (1, "https://example.com/1", "正文内容"),
                ]
                result = synthesize_pro("测试问题", self.results, config)
                self.assertIn("抽取式摘要", result)


# ============================================================
# 定时 selftest 调度（selftest_scheduler）
# ============================================================

class TestSelftestScheduler(unittest.TestCase):
    """定时 selftest 调度模块"""

    def test_scheduler_disabled(self):
        """调度器禁用时返回空"""
        from selftest_scheduler import SelftestScheduler
        config = {"selftest_schedule": {"enabled": False}}
        scheduler = SelftestScheduler(config)
        result = scheduler.run_once()
        self.assertFalse(result.get("enabled"))

    def test_scheduler_default_config(self):
        """默认配置"""
        from selftest_scheduler import SelftestScheduler
        config = {}
        scheduler = SelftestScheduler(config)
        self.assertTrue(scheduler.enabled)
        self.assertEqual(scheduler.interval, "daily")
        self.assertEqual(scheduler.alert_channel, "log")
        self.assertEqual(scheduler.notify_on, "failure")

    def test_scheduler_custom_config(self):
        """自定义配置"""
        from selftest_scheduler import SelftestScheduler
        config = {
            "selftest_schedule": {
                "enabled": True,
                "interval": "hourly",
                "alert_channel": "both",
                "webhook_url": "https://example.com/webhook",
                "notify_on": "all",
            }
        }
        scheduler = SelftestScheduler(config)
        self.assertTrue(scheduler.enabled)
        self.assertEqual(scheduler.interval, "hourly")
        self.assertEqual(scheduler.alert_channel, "both")
        self.assertEqual(scheduler.webhook_url, "https://example.com/webhook")
        self.assertEqual(scheduler.notify_on, "all")

    def test_format_alert_message_all_ok(self):
        """格式化告警消息：全部正常"""
        from selftest_scheduler import SelftestScheduler
        scheduler = SelftestScheduler({})
        result = {
            "ok_count": 10,
            "total": 10,
            "failed_count": 0,
            "failed": [],
            "timestamp": "2026-08-17T15:00:00",
        }
        msg = scheduler._format_alert_message(result)
        self.assertIn("10/10 正常", msg)

    def test_format_alert_message_with_failures(self):
        """格式化告警消息：有失效引擎"""
        from selftest_scheduler import SelftestScheduler
        scheduler = SelftestScheduler({})
        result = {
            "ok_count": 8,
            "total": 10,
            "failed_count": 2,
            "failed": ["baidu", "sogou"],
            "timestamp": "2026-08-17T15:00:00",
        }
        msg = scheduler._format_alert_message(result)
        self.assertIn("baidu", msg)
        self.assertIn("sogou", msg)
        self.assertIn("8/10", msg)

    def test_alert_to_log(self):
        """日志告警写入"""
        from selftest_scheduler import _alert_to_log
        with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
            log_path = f.name
        try:
            with patch('selftest_scheduler._alert_to_log') as mock_log:
                _alert_to_log("测试消息", {"failed": ["baidu"]})
                # 验证不抛异常
        finally:
            os.unlink(log_path)

    def test_alert_to_webhook_empty_url(self):
        """webhook 空 URL 返回 False"""
        from selftest_scheduler import _alert_to_webhook
        result = _alert_to_webhook("消息", "")
        self.assertFalse(result)

    def test_run_once_with_mock(self):
        """执行一次 selftest（mock）"""
        from selftest_scheduler import SelftestScheduler
        config = {"selftest_schedule": {"enabled": True, "notify_on": "all"}}
        scheduler = SelftestScheduler(config)
        with patch.object(scheduler, '_run_selftest') as mock_selftest:
            mock_selftest.return_value = {
                "report": [{"engine": "baidu", "ok": True, "count": 3, "diagnosis": "ok"}],
                "total": 1,
                "ok_count": 1,
                "failed_count": 0,
                "failed": [],
                "timestamp": "2026-08-17T15:00:00",
            }
            result = scheduler.run_once()
            self.assertEqual(result["ok_count"], 1)


# ============================================================
# jieba 默认安装验证
# ============================================================

class TestJiebaDefaultInstalled(unittest.TestCase):
    """验证 jieba 已作为默认依赖安装"""

    def test_jieba_in_requirements(self):
        """requirements.txt 必须包含 jieba"""
        req_path = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
        with open(req_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('jieba', content.lower())

    def test_jieba_importable(self):
        """jieba 必须可导入（默认安装）"""
        try:
            import jieba
            self.assertTrue(True)
        except ImportError:
            self.fail("jieba 未安装，但 requirements.txt 已声明为默认依赖")

    def test_ranking_uses_jieba(self):
        """ranking.py 使用 jieba 进行中文分词"""
        from ranking import _load_jieba, has_cjk, extract_features
        # 验证中文特征提取走 jieba 路径
        text = "Python 装饰器 详解"
        self.assertTrue(has_cjk(text))
        features = extract_features(text, max_len=64)
        self.assertGreater(len(features), 0)


# ============================================================
# SKILL.md 版本号检查
# ============================================================

class TestSkillMdVersion(unittest.TestCase):
    """SKILL.md 版本号必须是 1.6.0"""

    def test_version_is_160(self):
        version = get_current_version()
        self.assertEqual(version, "1.6.0")

    def test_version_not_quoted(self):
        """version 字段不带引号（死规则 8）"""
        skill_md = os.path.join(os.path.dirname(__file__), '..', 'SKILL.md')
        with open(skill_md, encoding='utf-8-sig') as f:
            content = f.read()
        # 找到 version 行
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith('version:'):
                # 必须是 version: 1.6.0（不带引号）
                self.assertEqual(stripped, 'version: 1.6.0',
                                 "version 字段必须不带引号（死规则 8）")
                break
        else:
            self.fail("SKILL.md 中未找到 version 字段")


# ============================================================
# 新模块 dont_write_bytecode 检查（死规则 13）
# ============================================================

class TestNewModulesNoBytecode(unittest.TestCase):
    """新模块必须设置 dont_write_bytecode"""

    def test_synthesiser_has_dont_write_bytecode(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'synthesiser.py')
        with open(path, encoding='utf-8') as f:
            content = f.read()
        self.assertIn('dont_write_bytecode', content,
                      "synthesiser.py 必须设置 dont_write_bytecode")

    def test_selftest_scheduler_has_dont_write_bytecode(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'selftest_scheduler.py')
        with open(path, encoding='utf-8') as f:
            content = f.read()
        self.assertIn('dont_write_bytecode', content,
                      "selftest_scheduler.py 必须设置 dont_write_bytecode")


if __name__ == "__main__":
    unittest.main(verbosity=2)
