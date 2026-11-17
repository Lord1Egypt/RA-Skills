#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
垂直搜索测试（V1.8 新增）
覆盖：配置获取、排序覆盖、降级逻辑、格式化输出
"""

import os
import sys
import unittest
from types import SimpleNamespace

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


def _make_result(title="test", url="https://example.com", snippet="snippet", engine="baidu", score=5.0):
    """创建模拟搜索结果"""
    return SimpleNamespace(
        title=title,
        url=url,
        snippet=snippet,
        engine=engine,
        score=score,
        engines=[engine],
        engine_set=[engine],
        rank=1,
    )


class TestVerticalConfig(unittest.TestCase):
    """垂直搜索配置"""

    def test_list_vertical_types(self):
        from vertical_search import list_vertical_types
        types = list_vertical_types()
        self.assertIn("news", types)
        self.assertIn("realtime", types)
        self.assertIn("academic", types)
        self.assertIn("image", types)

    def test_get_news_config(self):
        from vertical_search import get_vertical_config
        cfg = get_vertical_config("news")
        self.assertIsNotNone(cfg)
        self.assertIn("engines", cfg)
        self.assertIn("ranking_overrides", cfg)

    def test_get_invalid_config(self):
        from vertical_search import get_vertical_config
        cfg = get_vertical_config("invalid_type")
        self.assertIsNone(cfg)


class TestVerticalRanking(unittest.TestCase):
    """垂直排序覆盖"""

    def test_news_ranking_overrides_freshness(self):
        from vertical_search import apply_vertical_ranking, get_vertical_config
        cfg = get_vertical_config("news")
        overrides = cfg.get("ranking_overrides", {})
        # news 的 freshness 权重应较高
        self.assertGreater(overrides.get("freshness", 0), 1.0)

    def test_apply_ranking_with_empty_results(self):
        from vertical_search import apply_vertical_ranking
        result = apply_vertical_ranking([], "news")
        self.assertEqual(result, [])

    def test_apply_ranking_with_results(self):
        from vertical_search import apply_vertical_ranking
        results = [_make_result(score=1.0), _make_result(score=3.0), _make_result(score=2.0)]
        ranked = apply_vertical_ranking(results, "news")
        self.assertEqual(len(ranked), 3)


class TestAcademicSuffix(unittest.TestCase):
    """学术关键词后缀"""

    def test_add_suffix(self):
        from vertical_search import add_academic_suffix
        result = add_academic_suffix("quantum computing")
        self.assertIn("论文", result)

    def test_no_duplicate_suffix(self):
        from vertical_search import add_academic_suffix
        result = add_academic_suffix("quantum computing 论文")
        # 不应重复添加
        self.assertEqual(result.count("论文"), 1)


class TestFallbackEngines(unittest.TestCase):
    """降级引擎构建"""

    def test_build_fallback_for_news(self):
        from vertical_search import build_vertical_fallback_engines
        engines = build_vertical_fallback_engines("news")
        self.assertTrue(len(engines) > 0)
        # 降级引擎不应包含新闻专用引擎
        for e in engines:
            self.assertNotIn("news", e.lower())

    def test_build_fallback_for_academic(self):
        from vertical_search import build_vertical_fallback_engines
        engines = build_vertical_fallback_engines("academic")
        self.assertTrue(len(engines) > 0)


class TestFormatResults(unittest.TestCase):
    """格式化输出"""

    def test_format_empty_results(self):
        from vertical_search import format_vertical_results
        result = format_vertical_results([], "news")
        self.assertIn("没有", result)

    def test_format_normal_results(self):
        from vertical_search import format_vertical_results
        results = [_make_result(title="测试标题", url="https://test.com")]
        result = format_vertical_results(results, "news", "测试")
        self.assertIn("测试标题", result)
        self.assertIn("测试", result)

    def test_format_academic_with_citations(self):
        from vertical_search import format_vertical_results
        r = _make_result(title="论文标题", url="https://arxiv.org")
        r.citation_count = 100
        r.year = 2024
        result = format_vertical_results([r], "academic", "test")
        self.assertIn("引用", result)
        self.assertIn("年份", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
