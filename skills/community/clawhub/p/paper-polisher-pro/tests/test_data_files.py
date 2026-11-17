# -*- coding: utf-8 -*-
"""数据文件完整性：阈值/融合配置/模式库/术语库/评测数字锚点。"""
import json
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent


class TestDataFiles(unittest.TestCase):
    def test_para_thresholds_loads(self):
        d = json.load(open(PKG / "references" / "para_thresholds.json", encoding="utf-8"))
        self.assertIn("recommended_high", d)
        self.assertIn("honest_conclusion", d)

    def test_fusion_config_loads(self):
        d = json.load(open(PKG / "references" / "fusion_config.json", encoding="utf-8"))
        self.assertIn("thresholds", d)

    def test_zh_patterns_nonempty(self):
        d = json.load(open(PKG / "references" / "ai_patterns_zh.json", encoding="utf-8"))
        cats = d.get("categories", {})
        self.assertGreaterEqual(len(cats), 15)
        for name in ("ai_cliches", "filler_phrases", "sentence_structure"):
            self.assertIn(name, cats)

    def test_terminology_loads(self):
        d = json.load(open(PKG / "data" / "terminology.json", encoding="utf-8"))
        n = len(d) if isinstance(d, list) else len(d.get("terms", d))
        self.assertGreater(n, 2000, f"术语库条目异常: {n}")


class TestVersionConsistency(unittest.TestCase):
    """版本一致性读运行时真值互证（不硬编码版本号——每日 1-2 更新节奏下防脆断言）。"""

    def test_frontmatter_matches_skill_json(self):
        import re
        import json
        head = (PKG / "SKILL.md").read_text(encoding="utf-8")[:4000]
        v_md = re.search(r"^version:\s*(\S+)", head, re.M).group(1)
        v_json = json.load(open(PKG / "skill.json", encoding="utf-8"))["version"]
        self.assertEqual(v_md, v_json, f"SKILL.md({v_md}) != skill.json({v_json})")
        self.assertGreaterEqual(int(v_md.split(".")[0]), 5)

    def test_changelog_has_current_entry(self):
        import re
        import json
        t = (PKG / "CHANGELOG.md").read_text(encoding="utf-8")
        v_json = json.load(open(PKG / "skill.json", encoding="utf-8"))["version"]
        self.assertIn(v_json, t[:3000], f"CHANGELOG 顶部缺当前版本 {v_json}")


if __name__ == "__main__":
    unittest.main()
