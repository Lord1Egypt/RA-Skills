#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V1.8 综合测试（不依赖 pytest，使用标准库 unittest）
"""

import os
import sys
import unittest
from types import SimpleNamespace

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestFactChecker(unittest.TestCase):
    """事实核查层核心功能"""

    def setUp(self):
        self.sources = [
            (1, "https://a.com", "量子计算利用量子比特的叠加态进行并行计算。与传统计算机相比，量子计算机在特定问题上具有指数级加速潜力。"),
            (2, "https://b.com", "目前量子计算机面临的主要挑战是量子退相干问题。科学家正在研发纠错码来解决这一难题。"),
        ]

    def test_basic_sufficient_match(self):
        from fact_checker import fact_check
        answer = "量子计算利用量子比特进行并行计算 [1]。"
        result = fact_check(answer, self.sources, {})
        labels = [c["label"] for c in result["claims"]]
        self.assertTrue(any(l in ("sufficient", "partial") for l in labels))

    def test_unsupported_claim_removed(self):
        from fact_checker import fact_check
        answer = "量子计算利用量子比特进行并行计算 [1]。\n量子火锅是四川名菜 [2]。"
        result = fact_check(answer, self.sources, {"fact_check": {"remove_unsupported": True}})
        removed_text = " ".join(result["removed_claims"])
        self.assertIn("量子火锅", removed_text)

    def test_unsupported_claim_kept_when_configured(self):
        from fact_checker import fact_check
        answer = "量子计算利用量子比特 [1]。\n量子火锅是名菜 [1]。"
        result = fact_check(answer, self.sources, {"fact_check": {"remove_unsupported": False}})
        self.assertEqual(len(result["removed_claims"]), 0)
        labels = [c["label"] for c in result["claims"]]
        self.assertIn("unsupported", labels)

    def test_source_count(self):
        from fact_checker import fact_check
        answer = "量子计算利用量子比特 [1]。"
        result = fact_check(answer, self.sources, {})
        self.assertEqual(result["source_count"], 2)

    def test_empty_sources(self):
        from fact_checker import fact_check
        answer = "量子计算利用量子比特 [1]。"
        result = fact_check(answer, [], {})
        self.assertEqual(result["source_count"], 0)

    def test_empty_answer(self):
        from fact_checker import fact_check
        result = fact_check("", self.sources, {})
        self.assertEqual(result["claims"], [])

    def test_check_method_note_present(self):
        from fact_checker import fact_check
        answer = "量子计算利用量子比特 [1]。"
        result = fact_check(answer, self.sources, {})
        self.assertIn("TF-IDF", result["check_method"])

    def test_split_sentences(self):
        from fact_checker import _split_sentences
        text = "第一句。第二句！第三句？第四句。"
        sents = _split_sentences(text)
        self.assertEqual(len(sents), 4)

    def test_cosine_similarity(self):
        from fact_checker import _cosine_similarity, _extract_tfidf_vector
        v1 = _extract_tfidf_vector("量子计算 量子比特")
        v2 = _extract_tfidf_vector("量子计算 量子比特")
        sim = _cosine_similarity(v1, v2)
        self.assertGreater(sim, 0.9)

    def test_cosine_similarity_different(self):
        from fact_checker import _cosine_similarity, _extract_tfidf_vector
        v1 = _extract_tfidf_vector("量子计算 物理")
        v2 = _extract_tfidf_vector("红烧肉 菜谱")
        sim = _cosine_similarity(v1, v2)
        self.assertLess(sim, 0.3)


class TestQueryParser(unittest.TestCase):
    """高级检索语法解析"""

    def test_parse_site(self):
        from query_parser import parse_query
        clean, sf = parse_query("python教程 site:github.com")
        self.assertEqual(clean, "python教程")
        self.assertEqual(sf.site, "github.com")

    def test_parse_filetype(self):
        from query_parser import parse_query
        clean, sf = parse_query("报告 filetype:pdf")
        self.assertEqual(clean, "报告")
        self.assertEqual(sf.filetype, "pdf")

    def test_parse_after_year(self):
        from query_parser import parse_query
        clean, sf = parse_query("AI新闻 after:2024")
        self.assertEqual(clean, "AI新闻")
        self.assertEqual(sf.after, "2024")

    def test_parse_after_full_date(self):
        from query_parser import parse_query
        clean, sf = parse_query("新闻 after:2024-06-15")
        self.assertEqual(sf.after, "2024-06-15")

    def test_parse_before(self):
        from query_parser import parse_query
        clean, sf = parse_query("历史 before:2020")
        self.assertEqual(clean, "历史")
        self.assertEqual(sf.before, "2020")

    def test_parse_bang(self):
        from query_parser import parse_query
        clean, sf = parse_query("!w 量子计算")
        self.assertEqual(clean, "量子计算")
        self.assertEqual(sf.bang, "!w")

    def test_parse_combined(self):
        from query_parser import parse_query
        clean, sf = parse_query("量子计算 site:mit.edu after:2024")
        self.assertEqual(clean, "量子计算")
        self.assertEqual(sf.site, "mit.edu")
        self.assertEqual(sf.after, "2024")

    def test_parse_no_syntax(self):
        from query_parser import parse_query
        clean, sf = parse_query("普通搜索词")
        self.assertEqual(clean, "普通搜索词")
        self.assertFalse(sf.has_filters)

    def test_parse_empty_query(self):
        from query_parser import parse_query
        clean, sf = parse_query("")
        self.assertEqual(clean, "")
        self.assertFalse(sf.has_filters)

    def test_baidu_supports_site(self):
        from query_parser import engine_supports_syntax
        self.assertTrue(engine_supports_syntax("baidu", "site"))

    def test_qwant_not_supports_site(self):
        from query_parser import engine_supports_syntax
        self.assertFalse(engine_supports_syntax("qwant", "site"))

    def test_searxng_supports_time(self):
        from query_parser import engine_supports_syntax
        self.assertTrue(engine_supports_syntax("searxng", "after"))

    def test_get_unsupported(self):
        from query_parser import get_unsupported_syntax, parse_query
        _, sf = parse_query("test site:example.com filetype:pdf")
        unsupported = get_unsupported_syntax("qwant", sf)
        self.assertIn("site", unsupported)
        self.assertIn("filetype", unsupported)

    def test_filter_by_site(self):
        from query_parser import filter_results_locally, parse_query
        _, sf = parse_query("test site:example.com")
        results = [
            SimpleNamespace(url="https://example.com/a"),
            SimpleNamespace(url="https://other.com/b"),
        ]
        filtered, notices = filter_results_locally(results, sf, "qwant")
        self.assertEqual(len(filtered), 1)
        self.assertIn("example.com", filtered[0].url)

    def test_filter_by_filetype(self):
        from query_parser import filter_results_locally, parse_query
        _, sf = parse_query("test filetype:pdf")
        results = [
            SimpleNamespace(url="https://a.com/doc.pdf"),
            SimpleNamespace(url="https://b.com/page.html"),
        ]
        filtered, notices = filter_results_locally(results, sf, "qwant")
        self.assertEqual(len(filtered), 1)

    def test_filter_no_syntax_returns_original(self):
        from query_parser import filter_results_locally, parse_query
        _, sf = parse_query("普通词")
        results = [SimpleNamespace(url="https://a.com")]
        filtered, notices = filter_results_locally(results, sf, "baidu")
        self.assertEqual(len(filtered), 1)

    def test_syntax_table_contains_advanced(self):
        from query_parser import get_query_syntax_table
        table = get_query_syntax_table()
        self.assertIn("after:", table)
        self.assertIn("site:", table)
        self.assertIn("filetype:", table)


class TestVerticalSearch(unittest.TestCase):
    """垂直搜索配置与排序"""

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

    def test_news_ranking_overrides_freshness(self):
        from vertical_search import get_vertical_config
        cfg = get_vertical_config("news")
        overrides = cfg.get("ranking_overrides", {})
        self.assertGreater(overrides.get("freshness", 0), 1.0)

    def test_apply_ranking_with_empty_results(self):
        from vertical_search import apply_vertical_ranking
        result = apply_vertical_ranking([], "news")
        self.assertEqual(result, [])

    def test_add_academic_suffix(self):
        from vertical_search import add_academic_suffix
        result = add_academic_suffix("quantum computing")
        self.assertIn("论文", result)

    def test_no_duplicate_suffix(self):
        from vertical_search import add_academic_suffix
        result = add_academic_suffix("quantum computing 论文")
        self.assertEqual(result.count("论文"), 1)

    def test_build_fallback_for_news(self):
        from vertical_search import build_vertical_fallback_engines
        engines = build_vertical_fallback_engines("news")
        self.assertTrue(len(engines) > 0)

    def test_format_empty_results(self):
        from vertical_search import format_vertical_results
        result = format_vertical_results([], "news")
        self.assertIn("没有", result)

    def test_format_normal_results(self):
        from vertical_search import format_vertical_results
        r = SimpleNamespace(
            title="测试标题", url="https://test.com", snippet="snippet",
            engine="baidu", score=5.0, engines=["baidu"], engine_set=["baidu"], rank=1,
        )
        result = format_vertical_results([r], "news", "测试")
        self.assertIn("测试标题", result)
        self.assertIn("测试", result)


class TestIntegration(unittest.TestCase):
    """集成测试"""

    def test_query_parser_to_filter_pipeline(self):
        from query_parser import parse_query, filter_results_locally
        query = "量子计算 site:mit.edu after:2024"
        clean, sf = parse_query(query)
        self.assertEqual(clean, "量子计算")
        self.assertEqual(sf.site, "mit.edu")
        self.assertEqual(sf.after, "2024")

        results = [
            SimpleNamespace(url="https://mit.edu/quantum", title="Quantum", snippet="after 2024 research", publish_date="2025-01-01"),
            SimpleNamespace(url="https://other.com/old", title="Old", snippet="before 2024", publish_date="2020-01-01"),
        ]
        filtered, notices = filter_results_locally(results, sf)
        self.assertEqual(len(filtered), 1)

    def test_fact_check_with_empty_answer(self):
        from fact_checker import fact_check
        result = fact_check("", [], {})
        self.assertEqual(result["source_count"], 0)
        self.assertEqual(result["claims"], [])

    def test_vertical_config_completeness(self):
        from vertical_search import VERTICAL_CONFIGS
        for vt in ["news", "realtime", "academic", "image"]:
            self.assertIn(vt, VERTICAL_CONFIGS)
            cfg = VERTICAL_CONFIGS[vt]
            self.assertIn("engines", cfg)
            self.assertIn("ranking_overrides", cfg)
            self.assertTrue(len(cfg["engines"]) > 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
