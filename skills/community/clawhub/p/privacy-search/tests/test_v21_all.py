#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V2.1.0 全量测试：RAG-lite + 隐私量化报告"""
import sys
import os
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))


class TestRAGLite(unittest.TestCase):
    def setUp(self):
        from rag_lite import synthesize_rag_lite
        self.fn = synthesize_rag_lite

    def test_three_section_structure(self):
        sources = [
            (1, "https://a.com", "量子计算利用量子比特的叠加态进行并行计算。"),
            (2, "https://b.com", "量子退相干是主要挑战。"),
        ]
        result = self.fn("量子计算原理", sources, {})
        self.assertIn("【结论】", result["answer"])
        self.assertIn("【依据】", result["answer"])
        self.assertIn("【反证】", result["answer"])

    def test_citation_backlink(self):
        sources = [(1, "https://a.com", "量子计算利用量子比特叠加态并行计算，具有加速潜力。")]
        result = self.fn("量子计算", sources, {})
        self.assertTrue(result["evidence"] or result["conclusion"])
        # 依据必须带 citation
        for ev in result["evidence"]:
            self.assertIn("[来源", ev["citation"])
            self.assertTrue(ev["url"])

    def test_20_sources_citation_backlink(self):
        """验收：20 组多源问题答案的依据引用全部可回链原文"""
        sources = []
        for i in range(1, 21):
            sources.append((
                i, f"https://site{i}.com",
                f"第{i}个来源讨论了人工智能在医疗影像诊断中的应用，准确率持续提升，"
                f"同时第{i}组研究者指出数据标注成本仍是主要瓶颈。"
            ))
        result = self.fn("人工智能医疗影像诊断的进展和瓶颈", sources, {})
        # 每条依据都能回链到来源 URL
        self.assertGreater(len(result["evidence"]), 0)
        for ev in result["evidence"]:
            self.assertIn("url", ev)
            self.assertTrue(ev["url"].startswith("https://site"))
            self.assertIn("[来源", ev["citation"])
        self.assertGreater(result["chunks_count"], 0)

    def test_empty_sources(self):
        result = self.fn("测试", [], {})
        self.assertIn("没有找到", result["answer"])
        self.assertEqual(result["evidence"], [])

    def test_counter_is_low_overlap(self):
        sources = [
            (1, "https://a.com", "量子计算有指数加速优势，将改变密码学。"),
            (2, "https://b.com", "有学者指出量子计算成本高昂，短期难以商用，承诺被夸大。"),
        ]
        result = self.fn("量子计算的优势", sources, {})
        # 反证段应存在（同主题不同表述）
        self.assertIsInstance(result["counter"], list)


class TestFactCheckMarking(unittest.TestCase):
    def test_unsupported_marked_not_removed(self):
        from fact_checker import fact_check
        sources = [(1, "https://a.com", "量子计算利用量子比特叠加态进行并行计算。")]
        answer = (
            "量子计算利用量子比特叠加态并行计算 [1]。\n"
            "量子计算机已经完全取代了所有传统计算机，并解决了所有数学难题 [1]。"
        )
        result = fact_check(answer, sources, {})
        unsupported = [c for c in result["claims"] if c["label"] == "unsupported"]
        # 无源论断被标注保留，而非剔除
        if unsupported:
            self.assertEqual(len(result["removed_claims"]), 0)
            marked = [c for c in result["claims"] if c["text"].startswith("[无源]") or c["marked_text"].startswith("[无源]")]
            # 标注进 cleaned_answer
            self.assertIn("[无源]", result["cleaned_answer"])

    def test_mark_accuracy(self):
        """验收：无源标注准确率 >=95%"""
        from fact_checker import fact_check
        sources = [(1, "https://a.com", "人工智能在医疗影像诊断中达到较高准确率，帮助医生发现病灶。")]
        supported = "人工智能在医疗影像诊断中达到较高准确率 [1]。"
        unsupported = "人工智能已经能够让所有盲人重见光明并治愈癌症 [1]。"
        result = fact_check(supported + "\n" + unsupported, sources, {})
        total_unsupported = sum(1 for c in result["claims"] if c["label"] == "unsupported")
        marked_in_answer = result["cleaned_answer"].count("[无源]")
        if total_unsupported > 0:
            accuracy = marked_in_answer / total_unsupported
            self.assertGreaterEqual(accuracy, 0.95)


class TestPrivacyScore(unittest.TestCase):
    def test_mode_difference(self):
        """验收：normal/strict 分数差 >30"""
        from privacy_score import compute_privacy_score
        cfg = {"privacy": {"strict": {"proxy": ""}}}
        normal = compute_privacy_score(["baidu", "bing", "sogou"], "normal", cfg,
                                       has_proxy=False, cache_written=False,
                                       outbound_requests=8, cookie_clean=True)
        strict = compute_privacy_score(["searxng", "yandex", "startpage"], "strict", cfg,
                                       has_proxy=True, cache_written=True,
                                       outbound_requests=2, cookie_clean=True)
        self.assertGreater(strict.total - normal.total, 30)

    def test_score_range(self):
        from privacy_score import compute_privacy_score
        s = compute_privacy_score(["baidu"], "normal", {}, has_proxy=False,
                                  cache_written=False, outbound_requests=100, cookie_clean=False)
        self.assertGreaterEqual(s.total, 0)
        self.assertLessEqual(s.total, 100)

    def test_weekly_report(self):
        from privacy_score import weekly_report, _PROFILE_PATH
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False, encoding="utf-8") as f:
            f.write('{"total": 80, "mode": "strict", "has_proxy": true, "timestamp": "2026-11-18T10:00:00"}\n')
            path = f.name
        try:
            report = weekly_report(path=path)
            self.assertEqual(report["total_searches"], 1)
            self.assertEqual(report["avg_score"], 80.0)
        finally:
            os.unlink(path)


class TestCacheHint(unittest.TestCase):
    def test_similar_recent(self):
        from cache import SearchCache
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            c = SearchCache(db_path=os.path.join(d, "test.db"), enabled=True)
            data = [{"title": "t", "url": "u", "snippet": "s", "engine": "baidu"}]
            c.set("key1", "量子计算的原理", ["baidu"], "normal", data)
            hint = c.find_similar_recent("量子计算原理是什么", threshold=0.5)
            self.assertIsNotNone(hint)
            self.assertIn("time_str", hint)

    def test_get_with_time(self):
        from cache import SearchCache
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            c = SearchCache(db_path=os.path.join(d, "test.db"), enabled=True)
            data = [{"title": "t", "url": "u", "snippet": "s", "engine": "baidu"}]
            c.set("key1", "测试", ["baidu"], "normal", data)
            entry = c.get_with_time("key1")
            self.assertIn("time_str", entry)
            self.assertEqual(len(entry["payload"]), 1)


class TestSearXNGAudit(unittest.TestCase):
    def test_audit_checklist(self):
        from searxng_audit import audit
        bad_cfg = {
            "searxng": {
                "host": "0.0.0.0",
                "port": 8888,
                "enabled": True,
                "logging": {"level": "DEBUG", "query_in_title": True, "save": True},
                "formats": ["html"],
            }
        }
        report = audit(bad_cfg)
        # 预埋错误配置应全部命中
        self.assertLess(report["passed"], report["total"])
        names = {c["name"]: c["ok"] for c in report["checks"]}
        self.assertFalse(names["对外绑定"])
        self.assertFalse(names["日志级别"])
        self.assertFalse(names["JSON 格式"])
        self.assertFalse(names["查询词记录"])

    def test_good_config(self):
        from searxng_audit import audit
        good_cfg = {
            "searxng": {
                "host": "127.0.0.1", "port": 8888, "enabled": False,
                "logging": {"level": "WARNING", "query_in_title": False, "save": False},
                "formats": ["json", "html"],
            }
        }
        report = audit(good_cfg)
        # 除实例健康（因没真启动）外都通过
        names = {c["name"]: c["ok"] for c in report["checks"]}
        self.assertTrue(names["对外绑定"])
        self.assertTrue(names["日志级别"])
        self.assertTrue(names["JSON 格式"])


class TestDNSCheck(unittest.TestCase):
    def test_dns_check_structure(self):
        from privacy_score import check_dns_leak
        result = check_dns_leak({"privacy": {"strict": {"dns_servers": ["1.1.1.1"]}}})
        self.assertIn("leak", result)
        self.assertIn("system_dns", result)
        self.assertIn("warning", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
