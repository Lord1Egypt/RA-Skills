# -*- coding: utf-8 -*-
"""v7.4.0 契约测试（test_v70400）：results 物理分层 / 口径指针 / pp_api SDK 四能力。"""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
SCRIPTS = PKG / "scripts"

sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(PKG / "tests"))
import _docs  # noqa: E402


class TestPhysicalSeparation(unittest.TestCase):
    def test_top_level_only_current(self):
        """非缓存顶层 json 必须恰为 3 现行基线，其余全在 archive/。

        score_cache.json 是运行缓存（打包视图可排除）——形态自适应断言。"""
        top = {x.name for x in (PKG / "eval" / "results").glob("*.json")}
        self.assertEqual(top - {"score_cache.json"},
                         {"golden_detection.json", "v35ctl_gen2026.json",
                          "v35ctl_oldgen.json"})
        arch = list((PKG / "eval" / "results" / "archive").glob("*.json"))
        self.assertGreaterEqual(len(arch), 25)

    def test_current_md_declares_physical_layer(self):
        t = (PKG / "eval" / "results" / "CURRENT.md").read_text(encoding="utf-8")
        self.assertIn("物理分层", t)
        self.assertIn("archive/", t)

    def test_version_era_pointer(self):
        sk = (PKG / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue("Caliber navigation" in sk or "口径导航" in sk,
                        "现行口径指针缺失（双语任一）")
        self.assertIn("CURRENT.md", sk)


class TestSdkParity(unittest.TestCase):
    _TEXT = ("值得注意的是，随着人工智能技术的快速发展，其在医疗领域的应用日益受到关注。"
             "具体而言，AI 不仅能够提高诊断效率，而且可以优化治疗方案的制定。"
             "然而，与此同时，我们在享受技术红利的同时也面临着诸多挑战。"
             "在一定程度上，数据安全问题的存在对行业发展产生了一定的制约。"
             "综上所述，本研究为该领域的进一步探索提供了一定的参考价值。")

    def test_fix_suggest_structure(self):
        import pp_api
        r = pp_api.fix_suggest(self._TEXT)
        self.assertGreaterEqual(len(r["suggestions"]), 3)
        s0 = r["suggestions"][0]
        self.assertIn("type", s0["issues"][0])
        self.assertIn("advice", s0["issues"][0])
        self.assertIn("不构成任何合规判定", r["notice"])

    def test_fix_suggest_input_validation(self):
        import pp_api
        with self.assertRaises(ValueError):
            pp_api.fix_suggest("")
        with self.assertRaises(ValueError):
            pp_api.fix_suggest(None)

    def test_evidence_sections_structure(self):
        import pp_api
        r = pp_api.evidence_sections(self._TEXT)
        self.assertIn(r["meta"]["overall_risk"], ("high", "medium", "low"))
        titles = [s["title"] for s in r["sections"]]
        self.assertTrue(any("特征证据" in x for x in titles))
        self.assertIn("不构成", r["integrity_notice"])

    def test_scenarios_filter_and_full(self):
        import pp_api
        full = pp_api.scenarios()
        self.assertGreaterEqual(len(full), 18)
        hit = pp_api.scenarios("测AI率")
        self.assertEqual(hit[0]["scene_zh"], "测 AI 率")
        none = pp_api.scenarios("zzzz-not-a-scene")
        self.assertEqual(none, [])

    def test_term_project_validation(self):
        import pp_api
        with self.assertRaises(ValueError):
            pp_api.term_project("/no/such/dir")
        d = Path(tempfile.mkdtemp(prefix="ppp7400_"))
        (d / "only.md").write_text("足够长的文本内容。" * 40, encoding="utf-8")
        with self.assertRaises(ValueError):
            pp_api.term_project(str(d))  # 单文件目录 → ValueError（不 SystemExit 泄漏）


if __name__ == "__main__":
    unittest.main()
