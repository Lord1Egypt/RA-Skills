# -*- coding: utf-8 -*-
"""v5.8.1 契约测试（test_v50801）：术语库实战对照扩展 + 匹配机制修复（实战对照表 2026-10-16 领单）。

验收对齐提案：违规词造句必须逐词命中并给出规范名；干净样本不得误伤；
内部编号不入包（泄漏红线）；计数声明与库真实加载量一致。
"""
import json
import sys
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))
import _docs
sys.path.insert(0, str(PKG / "scripts"))


class TestTerminologyExtension(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from term_check import load_terminology
        cls.terms = load_terminology()

    def _issues(self, text):
        from term_check import check_terms
        r = check_terms(text, self.terms)
        d = json.loads(json.dumps(r, default=lambda o: o.__dict__
                                  if hasattr(o, "__dict__") else o,
                                  ensure_ascii=False))
        return d.get("issues", [])

    def test_violation_canary_all_hit(self):
        """违规词造句：附件 A 代表词必须逐词命中且带规范名建议。"""
        bad = ("对龄化复判数据通过第一道门和第二道门两道门禁后，把该指标作为头号盯防指标，"
               "本例画像清晰，临床落点明确，丰富构型为伪像，合成能力爬坡，母源抗体阳性，"
               "按成人口径判读，继续留雷达，做一锤定音检查后临床关闭，无重开口指征，"
               "按年龄带分层三层分写，附评估包与化验单。")
        issues = self._issues(bad)
        hit_originals = {i["original"] for i in issues}
        # 同一规范名的多个别名按最长优先只报一处：允许等价变体命中
        variants = {"头号盯防": ("头号盯防", "头号盯防指标")}
        for w in ("龄化复判", "第一道门", "第二道门", "本例画像", "临床落点",
                  "丰富构型", "爬坡", "母源抗体", "成人口径", "留雷达", "一锤定音检查",
                  "临床关闭", "重开口", "年龄带", "三层分写", "评估包", "化验单"):
            accepted = variants.get(w, (w,))
            self.assertTrue(any(h in hit_originals for h in accepted),
                            f"违规词未命中: {w}（命中集: {sorted(hit_originals)}）")
        for i in issues:
            self.assertTrue(i.get("standard"), f"命中缺规范名建议: {i}")

    def test_clean_text_no_false_hits(self):
        """规范表述样本：不得被别名误伤。"""
        good = ("本研究按年龄特异性参考区间复判，两项关键评估均通过；首要监测指标为 IgA，"
                "判读的临床意义支持可予临床排除，已出具检验报告并安排免疫球蛋白系列随访。")
        issues = self._issues(good)
        hit_originals = {i["original"] for i in issues}
        for w in ("龄化", "门禁", "头号盯防", "画像", "落点", "化验单", "评估包"):
            self.assertNotIn(w, hit_originals, f"规范文本被误伤: {w}")

    def test_no_internal_ids_in_bank(self):
        """泄漏红线：术语库任何字段不得携带内部编号。"""
        raw = (PKG / "data" / "terminology.json").read_text(encoding="utf-8")
        self.assertNotIn("LES-", raw)
        self.assertNotIn("Agent" + "Ops", raw)  # 拼接构造：防打包闸自指命中

    def test_source_fields_normalized(self):
        """实战对照来源字段统一为中性表述（实战对照表 YYYY-MM-DD，无内部编号）。"""
        import re
        d = json.loads((PKG / "data" / "terminology.json").read_text(encoding="utf-8"))
        for t in d:
            s = t.get("source", "")
            if "实战对照表" in s:
                self.assertRegex(s, r"^实战对照表 \d{4}-\d{2}-\d{2}$",
                                 f"source 未归一: {s!r}")

    def test_loaded_count_matches_docs_claim(self):
        """文档计数声明必须等于运行时真实加载量（动态校验，词典增长不再脆断）。"""
        standards = {e["standard"] for e in self.terms.values()}
        claim = f"{len(standards):,}"
        for doc in _docs.DOCS:
            text = (PKG / doc).read_text(encoding="utf-8")
            self.assertIn(claim, text, f"{doc} 计数声明 {claim} 与真实加载量不符")
            self.assertNotIn("2,308", text, f"{doc} 残留旧计数 2,308")


if __name__ == "__main__":
    unittest.main()
