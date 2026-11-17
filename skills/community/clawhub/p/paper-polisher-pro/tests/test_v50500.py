# -*- coding: utf-8 -*-
"""v5.5.0 契约测试（test_v50500——十进制固定位命名防撞名）：
术语一致性检查 / workflow findings ledger / desc 首行与 Skip-when。"""
import json
import unittest
from pathlib import Path

try:
    from tests._common import AI_TEXT, SCRIPTS
except ImportError:
    from _common import AI_TEXT, SCRIPTS
import pp_style_norm as sn

PKG = Path(__file__).resolve().parent.parent
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))
import _docs


class TestTermVariantsBank(unittest.TestCase):
    def test_bank_loads(self):
        d = json.load(open(PKG / "references" / "term_variants.json", encoding="utf-8"))
        self.assertGreaterEqual(len(d.get("groups", [])), 20)
        for g in d["groups"]:
            self.assertIn("variants", g)
            self.assertGreaterEqual(len(g["variants"]), 2)

    def test_mixing_detected(self):
        r = sn.style_norm("本研究纳入156例患者，病人均签署知情同意。患者随访12个月，病人无失访。",
                          checks=["consistency"])
        self.assertGreaterEqual(len(r["findings"]), 1)
        f = r["findings"][0]
        self.assertEqual(f["check"], "consistency")
        self.assertIn("患者", str(f["examples"]))
        self.assertIn("统一", f["advice"])

    def test_uniform_text_no_finding(self):
        r = sn.style_norm("本研究纳入156例患者，患者均签署知情同意，患者随访12个月。",
                          checks=["consistency"])
        self.assertEqual(len(r["findings"]), 0)

    def test_no_score_fields(self):
        r = sn.style_norm("患者与病人混用测试文本，包括包含重叠用词示例，与％和%的样本。")
        for k in ("score", "risk", "verdict"):
            self.assertNotIn(k, r)


class TestFindingsLedger(unittest.TestCase):
    def test_ledger_statuses(self):
        import sys
        sys.path.insert(0, str(SCRIPTS))
        import pp_workflow
        r = pp_workflow.workflow(AI_TEXT)
        items = r["findings_ledger"]["items"]
        self.assertGreaterEqual(len(items), 5)
        for it in items:
            self.assertIn(it["status"], ("answered", "partially", "unresolved"))
        md = pp_workflow.to_markdown(r)
        self.assertIn("Findings Ledger", md)


class TestDescFirstLine(unittest.TestCase):
    def test_demand_words_head120(self):
        t = _docs.zh_text()
        import re
        m = re.search(r"description: >-?\n((?:  .+\n)+)", t)
        desc = " ".join(x.strip() for x in m.group(1).splitlines())
        self.assertIn("论文润色", desc[:120])
        self.assertIn("AI率", desc[:120])
        self.assertNotIn("Paper Polisher Pro", desc[:60])

    def test_skip_when_present_both_langs(self):
        zh = _docs.zh_text()
        en = (PKG / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("不适用", zh)
        self.assertIn("Not for:", en)
        self.assertIn("doc-holmes", en)   # 负触发器指到对应工具
        self.assertIn("paper-rewriter", en)


if __name__ == "__main__":
    unittest.main()
