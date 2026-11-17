#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
事实核查层测试（V1.8 新增）
覆盖：论断拆分、TF-IDF 相似度、三级标注、无源论断剔除、配置覆盖
"""

import os
import sys
import unittest

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
        # 至少有一个 sufficient 或 partial
        labels = [c["label"] for c in result["claims"]]
        self.assertTrue(any(l in ("sufficient", "partial") for l in labels))

    def test_unsupported_claim_removed(self):
        from fact_checker import fact_check
        answer = "量子计算利用量子比特进行并行计算 [1]。\n量子火锅是四川名菜 [2]。"
        result = fact_check(answer, self.sources, {"fact_check": {"remove_unsupported": True}})
        # "量子火锅" 应该被标记为无源并被移除
        removed_text = " ".join(result["removed_claims"])
        self.assertIn("量子火锅", removed_text)

    def test_unsupported_claim_kept_when_configured(self):
        from fact_checker import fact_check
        answer = "量子计算利用量子比特 [1]。\n量子火锅是名菜 [1]。"
        result = fact_check(answer, self.sources, {"fact_check": {"remove_unsupported": False}})
        # 无源但保留
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
        text = "第一句。第二句！第三句？第四句"
        sents = _split_sentences(text)
        self.assertEqual(len(sents), 4)

    def test_split_claims(self):
        from fact_checker import _split_claims
        answer = "论断一 [1]。\n论断二 [1][2]。\n论断三。"
        claims = _split_claims(answer)
        self.assertGreaterEqual(len(claims), 2)

    def test_format_report(self):
        from fact_checker import fact_check, format_fact_check_report
        answer = "量子计算利用量子比特 [1]。"
        result = fact_check(answer, self.sources, {})
        report = format_fact_check_report(result)
        self.assertIn("事实核查报告", report)
        self.assertIn("论断总数", report)

    def test_cosine_similarity(self):
        from fact_checker import _cosine_similarity, _extract_tfidf_vector
        v1 = _extract_tfidf_vector("量子计算 量子比特")
        v2 = _extract_tfidf_vector("量子计算 量子比特")
        sim = _cosine_similarity(v1, v2)
        self.assertGreater(sim, 0.9)  # 完全相同应接近 1.0

    def test_cosine_similarity_different(self):
        from fact_checker import _cosine_similarity, _extract_tfidf_vector
        v1 = _extract_tfidf_vector("量子计算 物理")
        v2 = _extract_tfidf_vector("红烧肉 菜谱")
        sim = _cosine_similarity(v1, v2)
        self.assertLess(sim, 0.3)  # 完全不同应接近 0


class TestFactCheckerThresholds(unittest.TestCase):
    """阈值配置测试"""

    def test_custom_threshold(self):
        from fact_checker import fact_check
        sources = [(1, "https://a.com", "量子计算利用量子比特进行计算。")]
        answer = "量子计算利用量子比特 [1]。"
        # 提高 sufficient 阈值，原本 sufficient 的变成 partial
        result = fact_check(answer, sources, {
            "fact_check": {"sufficient_threshold": 0.99}
        })
        labels = [c["label"] for c in result["claims"]]
        # 极高阈值下不太可能 sufficient
        self.assertNotIn("sufficient", labels)


if __name__ == "__main__":
    unittest.main(verbosity=2)
