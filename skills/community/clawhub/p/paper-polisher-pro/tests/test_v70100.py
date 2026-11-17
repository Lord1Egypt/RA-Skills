# -*- coding: utf-8 -*-
"""v7.1.0 契约测试（test_v70100）：自定义术语库 --bank / 标题化石闸 / AUROC 口径锚定。"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
SCRIPTS = PKG / "scripts"


def _make_project():
    d = Path(tempfile.mkdtemp(prefix="ppp7100_"))
    (d / "ch1.md").write_text("本研究纳入类风湿性关节炎患者120例，随访24周。" * 5
                              + "全部病例完成影像学评估。" * 2, encoding="utf-8")
    (d / "ch2.md").write_text("第5章：类风湿关节炎组的骨侵蚀进展显著。" * 5
                              + "统计采用Mann-Whitney U检验。" * 2, encoding="utf-8")
    bank = d / "bank.json"
    bank.write_text(json.dumps([
        {"cn": "类风湿性关节炎", "en": "rheumatoid arthritis",
         "aliases": ["类风湿关节炎"], "source": "课题组内部约定"}],
        ensure_ascii=False), encoding="utf-8")
    return d, bank


class TestCustomBank(unittest.TestCase):
    def test_bank_override_and_flagging(self):
        """自定义库同 cn 覆盖内置：内置标准名反而按项目词表被标记。"""
        d, bank = _make_project()
        src = d / "mixed.md"
        # 混合写法：内置标准名（项目口径=别名）+ 间质性肺炎（项目新增概念）
        src.write_text("本研究纳入类风湿关节炎患者120例。类风湿性关节炎的诊断需评估间质性肺炎。" * 4,
                       encoding="utf-8")
        out = d / "r.json"
        p = subprocess.run([sys.executable, str(SCRIPTS / "term_check.py"),
                            str(src), "--bank", str(bank), "--output", str(out)],
                           capture_output=True, text=True, timeout=300,
                           encoding="utf-8")
        self.assertEqual(p.returncode, 0, p.stderr[-200:])
        self.assertIn("+1 条", p.stderr)
        r = json.loads(out.read_text(encoding="utf-8"))
        flagged = {i["original"]: i["standard"] for i in r["issues"]}
        self.assertEqual(flagged.get("类风湿关节炎"), "类风湿性关节炎")  # 内置标准名在项目口径下被标
        self.assertNotIn("类风湿性关节炎", flagged)  # 项目标准名不受罚

    def test_bank_bad_entries_reported(self):
        d, _ = _make_project()
        bad = d / "bad.json"
        bad.write_text('[{"cn": "合法概念"}, {"en": "no-cn-field"}, "not-a-dict"]',
                       encoding="utf-8")
        src = d / "ch1.md"
        p = subprocess.run([sys.executable, str(SCRIPTS / "term_check.py"),
                            str(src), "--bank", str(bad)],
                           capture_output=True, text=True, timeout=300,
                           encoding="utf-8")
        self.assertEqual(p.returncode, 0)
        self.assertIn("第 2 条缺 cn", p.stderr)
        self.assertIn("第 3 条缺 cn", p.stderr)

    def test_term_project_with_bank(self):
        d, bank = _make_project()
        p = subprocess.run([sys.executable, str(SCRIPTS / "pp_term_consistency.py"),
                            str(d), "--bank", str(bank), "--json"],
                           capture_output=True, text=True, timeout=600,
                           encoding="utf-8")
        self.assertEqual(p.returncode, 0, p.stderr[-200:])
        j = json.loads(p.stdout)
        inc = [m for m in j["matrix"] if m["inconsistent"]]
        self.assertTrue(any(m["concept"] == "类风湿性关节炎" for m in inc),
                        "项目词表概念应进入跨文件矩阵")
        for m in inc:
            if m["concept"] == "类风湿性关节炎":
                self.assertEqual(m["recommend"], "类风湿性关节炎")
                self.assertIn("库标准名", m["basis"])  # 自定义库的标准名即库标准名（语义本就如此）


class TestConsistencyGates(unittest.TestCase):
    def test_title_no_version(self):
        t = (PKG / "SKILL.md").read_text(encoding="utf-8")
        import re
        m = re.search(r"^# (.+)$", t, re.M)
        self.assertIsNotNone(m)
        self.assertIsNone(re.search(r"\bv\d", m.group(1)), f"标题仍带版本: {m.group(1)}")

    def test_auroc_caliber_anchored(self):
        sk = (PKG / "SKILL.md").read_text(encoding="utf-8")
        rd = (PKG / "README.md").read_text(encoding="utf-8")
        self.assertIn("0.9998", sk)
        self.assertIn("0.9998", rd)
        self.assertNotIn("AUROC 1.0（作者侧实测）", rd)


if __name__ == "__main__":
    unittest.main()
