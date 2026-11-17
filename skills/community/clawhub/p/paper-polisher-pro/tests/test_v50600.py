# -*- coding: utf-8 -*-
"""v5.6.0 契约测试（test_v50600——十进制固定位命名）：
LLM 腔第 7 查 / 判例库 / 负结果（检测器只报不计分）/ 问题汇总工件。"""
import json
import unittest
from pathlib import Path

try:
    from tests._common import SCRIPTS
except ImportError:
    from _common import SCRIPTS
import pp_style_norm as sn

PKG = Path(__file__).resolve().parent.parent


class TestLlmJargon(unittest.TestCase):
    JARGON_TEXT = ("免疫系统的某一个零件出厂即缺失，机会性病原最先破门。家族史是探针，"
                   "把这条主线收拢并非易事。先兜底再根治的思路需要克制。六张面孔背后是同一机制，"
                   "一网打尽并不现实。风湿科是第一站，把治疗窗口前移至关重要。"
                   "综上所述，检出结果要把另一面讲透，免疫力失守就会塌方。")

    def test_tiered_detection(self):
        r = sn.style_norm(self.JARGON_TEXT, checks=["llm_jargon"])
        checks = [f for f in r["findings"] if f["check"] == "llm_jargon"]
        tiers = set()
        for f in checks:
            if "L1" in f["advice"]:
                tiers.add("L1")
            if "L2" in f["advice"]:
                tiers.add("L2")
            if "L3" in f["advice"]:
                tiers.add("L3")
        self.assertIn("L1", tiers, f"L1 应命中: {r['findings']}")
        self.assertIn("L2", tiers)
        self.assertIn("L3", tiers)

    def test_case_library_contrast(self):
        r = sn.style_norm(self.JARGON_TEXT, checks=["llm_jargon"])
        l1 = [f for f in r["findings"] if f["check"] == "llm_jargon" and "L1" in f["advice"]]
        if any("判例对照" in f["advice"] for f in l1):
            self.assertIn("→", "".join(f["advice"] for f in l1))

    def test_clean_academic_no_finding(self):
        r = sn.style_norm("研究显示该方案与显著改善相关，其机制在于抑制炎症通路。"
                          "目前认为应尽早干预，建议纳入随访观察。临床意义在于为指南提供依据。",
                          checks=["llm_jargon"])
        self.assertEqual(len(r["findings"]), 0, f"白名单句式误报: {r['findings']}")

    def test_cases_bank_loads(self):
        d = json.load(open(PKG / "references" / "style_guard_cases.json", encoding="utf-8"))
        self.assertGreaterEqual(len(d.get("cases", [])), 18)
        self.assertTrue(d.get("whitelist_styles"))


class TestNegativeResultDisclosure(unittest.TestCase):
    def test_detector_reports_hits_without_scoring(self):
        import sys
        sys.path.insert(0, str(PKG / "scripts"))
        import ai_detector
        rep = ai_detector.detect(self.JARGON_TEXT, lang="zh")
        self.assertTrue(rep.jargon_hits, "应报告命中")
        self.assertEqual(rep.jargon_bonus, 0.0, "负结果裁决：不计分")

    JARGON_TEXT = ("免疫系统的某一个零件出厂即缺失，机会性病原最先破门。家族史是探针，"
                   "把这条主线收拢并非易事。先兜底再根治的思路需要克制。六张面孔背后是同一机制，"
                   "一网打尽并不现实。风湿科是第一站，把治疗窗口前移至关重要。"
                   "综上所述，检出结果要把另一面讲透，免疫力失守就会塌方。")

    def test_artifact_shipped(self):
        d = json.load(open(PKG / "eval" / "results" / "archive" / "meddocs_20261014.json", encoding="utf-8"))
        self.assertIn("negative_result", d)
        self.assertEqual(d["negative_result"]["decision"].find("回退"), 0)
        self.assertGreaterEqual(len(d.get("docs", [])), 5)


if __name__ == "__main__":
    unittest.main()
