# -*- coding: utf-8 -*-
"""v5.7.0 契约测试（test_v50700）：输出样例随包 / CHANGELOG 横幅 / 版本历史去冗 / 第 7 查命中句定位。"""
import json
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent


class TestSampleOutputs(unittest.TestCase):
    def test_samples_exist_and_parse(self):
        out = PKG / "examples" / "outputs"
        for name, keys in (
            ("detect_sample.json", ("overall_ai_score", "risk_bands", "integrity_notice")),
            ("style_norm_llm_jargon_sample.json", ("findings",)),
            ("fix_suggest_sample.json", ("stats", "suggestions")),
        ):
            d = json.load(open(out / name, encoding="utf-8"))
            for k in keys:
                self.assertIn(k, d, f"{name} 缺 {k}")

    def test_samples_readme(self):
        r = (PKG / "examples" / "outputs" / "README.md").read_text(encoding="utf-8")
        self.assertIn("真实引擎", r)


class TestProgressiveDeclutter(unittest.TestCase):
    def test_changelog_banner(self):
        t = (PKG / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("只想快速上手", t)
        self.assertIn("单一来源", t) or self.assertIn("single source", t)

    def test_skill_history_slimmed(self):
        import sys as _s
        _s.path.insert(0, str(PKG / "tests"))
        import _docs
        t = (PKG / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue("see `CHANGELOG.md`" in t or "完整历史在 `CHANGELOG.md`" in t,
                        "版本历史收敛指针缺失（双语任一）")
        self.assertNotIn("- **v5.4.1 (2026-10-14)**", t)  # 旧版本条目已收敛


class TestSentenceLocating(unittest.TestCase):
    def test_llm_jargon_sentences(self):
        import sys
        sys.path.insert(0, str(PKG / "scripts"))
        import pp_style_norm as sn
        text = "免疫系统的某一个零件出厂即缺失，机会性病原最先破门。先兜底再根治需要克制。综上所述要一网打尽。"
        r = sn.style_norm(text, checks=["llm_jargon"])
        l1 = [f for f in r["findings"] if f["check"] == "llm_jargon" and "L1" in f["advice"]]
        self.assertGreaterEqual(len(l1), 1)
        self.assertTrue(l1[0].get("sentences"), "应附命中句")


if __name__ == "__main__":
    unittest.main()
