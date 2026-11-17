#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V1.5 功能测试
覆盖：引擎统计、动态降级、UA 可配、新模块（page_fetcher/exporters/summarizer）、
      TF-IDF 相关度、配置修复验证、引擎改版 mock 回归
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
from cache import SearchCache, build_cache_from_config
from ranking import (
    relevance_score, domain_score, domain_of,
    HIGH_QUALITY_DOMAINS, LOW_QUALITY_DOMAINS, _relevance_tfidf,
)
from http_client import get_user_agent_pool, pick_user_agent, USER_AGENT_POOL


# ============================================================
# 引擎统计与动态降级
# ============================================================

class TestEngineStats(unittest.TestCase):
    """引擎统计记录与成功率查询"""

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix='.db')
        self.cache = SearchCache(db_path=self.db_path, ttl=3600, max_size_mb=10)

    def tearDown(self):
        self.cache.close()
        try:
            os.unlink(self.db_path)
        except OSError:
            pass

    def test_record_success(self):
        self.cache.record_engine_result('baidu', True)
        self.cache.record_engine_result('baidu', True)
        self.cache.record_engine_result('baidu', False)
        rate = self.cache.get_engine_success_rate('baidu')
        self.assertAlmostEqual(rate, 2 / 3, places=2)

    def test_record_failure(self):
        self.cache.record_engine_result('bing', False)
        self.cache.record_engine_result('bing', False)
        rate = self.cache.get_engine_success_rate('bing')
        self.assertAlmostEqual(rate, 0.0, places=2)

    def test_unknown_engine_returns_neutral(self):
        rate = self.cache.get_engine_success_rate('never_used')
        self.assertEqual(rate, 0.5)

    def test_rank_engines_by_success(self):
        # baidu: 2/3 成功率
        self.cache.record_engine_result('baidu', True)
        self.cache.record_engine_result('baidu', True)
        self.cache.record_engine_result('baidu', False)
        # bing: 1/2 成功率
        self.cache.record_engine_result('bing', True)
        self.cache.record_engine_result('bing', False)
        # searxng: 1/1 成功率
        self.cache.record_engine_result('searxng', True)

        engines = ['baidu', 'bing', 'searxng']
        ranked = self.cache.rank_engines_by_success(engines)
        # searxng 最高应排最前
        self.assertEqual(ranked[0], 'searxng')

    def test_rank_empty_engines(self):
        self.assertEqual(self.cache.rank_engines_by_success([]), [])


# ============================================================
# UA 池可配置化
# ============================================================

class TestUserAgentConfigurable(unittest.TestCase):
    """UA 池支持用户追加"""

    def test_default_pool(self):
        pool = get_user_agent_pool()
        self.assertEqual(pool, USER_AGENT_POOL)
        self.assertGreaterEqual(len(pool), 8)

    def test_custom_pool(self):
        custom = ["MyCustomUA/1.0", "AnotherAgent/2.0"]
        pool = get_user_agent_pool({"user_agent_pool": custom})
        self.assertEqual(len(pool), len(custom) + len(USER_AGENT_POOL))
        self.assertEqual(pool[0], "MyCustomUA/1.0")

    def test_custom_pool_skipped_when_empty(self):
        pool = get_user_agent_pool({"user_agent_pool": []})
        self.assertEqual(pool, USER_AGENT_POOL)

    def test_pick_from_custom_pool(self):
        custom = ["MyCustomUA/1.0"]
        pool = get_user_agent_pool({"user_agent_pool": custom})
        picked = pick_user_agent(pool=pool)
        self.assertIn(picked, pool)

    def test_fixed_ua_takes_precedence(self):
        self.assertEqual(pick_user_agent(fixed="Fixed/1.0"), "Fixed/1.0")


# ============================================================
# TF-IDF 相关度
# ============================================================

class TestTFIDFRelevance(unittest.TestCase):
    """TF-IDF 相关度评分（jieba 分词）"""

    def test_tfidf_identical_text(self):
        score = _relevance_tfidf("python 教程", "python 教程", "python 教程 入门")
        self.assertGreater(score, 0.5)

    def test_tfidf_unrelated_text(self):
        score = _relevance_tfidf("python 教程", "股票 投资 理财", "基金 收益")
        self.assertLess(score, 0.3)

    def test_tfidf_empty_query(self):
        score = _relevance_tfidf("", "some title", "some snippet")
        self.assertEqual(score, 0.0)

    def test_tfidf_english(self):
        score = _relevance_tfidf("python tutorial", "python tutorial", "learn python")
        self.assertGreater(score, 0.3)

    def test_relevance_score_cjk_prefers_tfidf(self):
        # 含中文时应使用 TF-IDF（有 jieba 时）
        score = relevance_score("python 装饰器", "python 装饰器 详解", "python 装饰器 用法")
        self.assertGreater(score, 0.0)

    def test_relevance_score_english_uses_simple(self):
        score = relevance_score("python tutorial", "Python Tutorial", "Learn Python")
        self.assertGreater(score, 0.0)


# ============================================================
# 域名表扩展验证
# ============================================================

class TestDomainScoring(unittest.TestCase):
    """域名质量打分扩展"""

    def test_zhihu_is_high_quality(self):
        self.assertEqual(domain_score("https://www.zhihu.com/question/123"), 1.0)

    def test_github_is_high_quality(self):
        self.assertEqual(domain_score("https://github.com/user/repo"), 1.0)

    def test_baijiahao_is_low_quality(self):
        self.assertEqual(domain_score("https://baijiahao.baidu.com/s?id=123"), -1.0)

    def test_unknown_domain_is_neutral(self):
        self.assertEqual(domain_score("https://example.com/page"), 0.0)

    def test_redirect_url_is_downweighted(self):
        score = domain_score("https://www.baidu.com/link?url=http://example.com")
        self.assertEqual(score, -0.5)

    def test_high_quality_set_not_empty(self):
        self.assertGreaterEqual(len(HIGH_QUALITY_DOMAINS), 20)

    def test_low_quality_set_not_empty(self):
        self.assertGreaterEqual(len(LOW_QUALITY_DOMAINS), 10)


# ============================================================
# 引擎改版 mock 回归测试
# ============================================================

class TestEngineRedesignMock(unittest.TestCase):
    """
    模拟引擎改版后选择器失效的场景
    验证诊断系统能正确检测并给出提示
    """

    def test_baidu_redesign_blocked(self):
        """百度改版后跳转验证页"""
        from engine_selectors import is_blocked_page
        html = '<html><body>百度安全验证</body></html>'
        self.assertTrue(is_blocked_page('baidu', html))

    def test_baidu_normal_page(self):
        """百度正常页面不被误判"""
        from engine_selectors import is_blocked_page
        html = '<html><body>搜索结果：python 教程</body></html>'
        self.assertFalse(is_blocked_page('baidu', html))

    def test_bing_redesign_blocked(self):
        """必应改版后出现验证码"""
        from engine_selectors import is_blocked_page
        html = '<html><body>Our systems have detected unusual traffic</body></html>'
        self.assertTrue(is_blocked_page('bing', html))

    def test_diagnose_partial_triggers_on_few_results(self):
        """结果数远低于期望时触发 PARTIAL 诊断"""
        from engine_selectors import diagnose_partial, ParseDiagnosis
        # 期望 10 条，只拿到 2 条（低于 1/3 阈值）
        diag = diagnose_partial('baidu', '<html>results</html>', 2, 10)
        self.assertEqual(diag, ParseDiagnosis.PARTIAL)

    def test_diagnose_ok_on_sufficient_results(self):
        """结果数充足时判为 OK"""
        from engine_selectors import diagnose_partial, ParseDiagnosis
        diag = diagnose_partial('baidu', '<html>results</html>', 5, 10)
        self.assertEqual(diag, ParseDiagnosis.OK)


# ============================================================
# page_fetcher 模块测试
# ============================================================

class TestPageFetcher(unittest.TestCase):
    """网页正文抓取模块"""

    def test_extract_text_empty_html(self):
        from page_fetcher import extract_text
        self.assertIsNone(extract_text(""))

    def test_extract_text_regex_fallback(self):
        """测试正则兜底提取"""
        from page_fetcher import _extract_text_regex
        html = '<html><body><p>这是第一段正文内容，足够长以满足最小长度要求。</p><p>这是第二段正文内容，也足够长。</p></body></html>'
        result = _extract_text_regex(html)
        self.assertIsNotNone(result)
        self.assertIn("第一段", result)

    def test_fetch_and_extract_returns_tuple(self):
        """fetch_and_extract 返回 (html, text) 元组"""
        from page_fetcher import fetch_and_extract
        # 不实际发起网络调用，只验证接口
        # 使用 mock 测试
        with patch('page_fetcher.fetch_page', return_value=None):
            result = fetch_and_extract("https://example.com")
            self.assertEqual(result, (None, None))


# ============================================================
# exporters 模块测试
# ============================================================

class TestExporters(unittest.TestCase):
    """结果导出模块"""

    def setUp(self):
        self.results = [
            SimpleNamespace(
                title="Python 教程",
                url="https://example.com/python",
                snippet="Python 入门教程",
                engine="baidu",
                rank=1,
            ),
            SimpleNamespace(
                title="Java 教程",
                url="https://example.com/java",
                snippet="Java 入门教程",
                engine="bing",
                rank=2,
            ),
        ]
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_export_markdown(self):
        from exporters import export_markdown
        path = os.path.join(self.tmpdir, "results.md")
        ok = export_markdown(self.results, path, "测试")
        self.assertTrue(ok)
        self.assertTrue(os.path.exists(path))
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Python 教程", content)
        self.assertIn("Java 教程", content)

    def test_export_html(self):
        from exporters import export_html
        path = os.path.join(self.tmpdir, "results.html")
        ok = export_html(self.results, path, "测试")
        self.assertTrue(ok)
        self.assertTrue(os.path.exists(path))
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("<html", content)
        self.assertIn("Python 教程", content)

    def test_export_unknown_format(self):
        from exporters import auto_export
        ok = auto_export(self.results, os.path.join(self.tmpdir, "results.xyz"))
        self.assertFalse(ok)


# ============================================================
# summarizer 模块测试
# ============================================================

class TestSummarizer(unittest.TestCase):
    """LLM 摘要模块"""

    def test_extractive_summarize_empty(self):
        from summarizer import _extractive_summarize
        result = _extractive_summarize("python", [])
        self.assertIn("没有", result)

    def test_extractive_summarize_normal(self):
        from summarizer import _extractive_summarize
        results = [
            SimpleNamespace(
                title="Python 教程",
                snippet="Python 是一种高级编程语言。它易于学习。",
                engine="baidu",
            ),
        ]
        result = _extractive_summarize("python 教程", results)
        self.assertIn("抽取式摘要", result)
        self.assertIn("Python", result)

    def test_summarize_with_no_api_key_uses_extractive(self):
        """无 API Key 时降级为抽取式"""
        from summarizer import summarize
        results = [
            SimpleNamespace(
                title="测试",
                snippet="这是一个测试摘要。用于测试降级功能。",
                engine="baidu",
            ),
        ]
        config = {"llm_summary": {"api_key": "", "provider": "auto"}}
        result = summarize("测试", results, config)
        self.assertIn("抽取式摘要", result)

    def test_summarize_disabled(self):
        """摘要功能关闭时降级"""
        from summarizer import summarize
        results = [SimpleNamespace(title="t", snippet="s", engine="b")]
        config = {"llm_summary": {"enabled": False}}
        result = summarize("test", results, config)
        self.assertIn("抽取式摘要", result)


# ============================================================
# 配置修复验证
# ============================================================

class TestConfigFixes(unittest.TestCase):
    """验证 V1.5 配置修复"""

    def test_update_check_in_sample_config(self):
        """示例配置包含 update_check 段"""
        import yaml
        cfg_path = os.path.join(os.path.dirname(__file__), '..', 'references', 'config.yaml.example')
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        self.assertIn("update_check", cfg)
        self.assertIn("github_url", cfg["update_check"])
        # 占位符已替换
        self.assertNotIn("your-org", cfg["update_check"]["github_url"])

    def test_request_delay_defaults_consistent(self):
        """request_delay 默认值与示例文件一致（1.0-5.0）"""
        import yaml
        cfg_path = os.path.join(os.path.dirname(__file__), '..', 'references', 'config.yaml.example')
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        self.assertEqual(cfg["search"]["request_delay_min"], 1.0)
        self.assertEqual(cfg["search"]["request_delay_max"], 5.0)


# ============================================================
# SKILL.md 版本号检查
# ============================================================

class TestSkillMdVersion(unittest.TestCase):
    """SKILL.md 版本号必须与当前版本一致"""

    def test_version_matches_current(self):
        """版本号应与 SKILL.md 一致（当前 v1.6.0）"""
        version = get_current_version()
        skill_md = os.path.join(os.path.dirname(__file__), '..', 'SKILL.md')
        with open(skill_md, encoding='utf-8-sig') as f:
            content = f.read()
        self.assertIn(f"version: {version}", content)


if __name__ == "__main__":
    unittest.main()
