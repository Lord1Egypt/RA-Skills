# -*- coding: utf-8 -*-
"""pp_style_norm 学术写作规范自查契约。"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

try:
    from tests._common import SCRIPTS
except ImportError:
    from _common import SCRIPTS
import pp_style_norm as sn

# 富问题样本（覆盖四查）
BAD_TEXT = (
    "本研究纳入了156例患者，其中五例随访脱落。所有患者均接受 5 mg 剂量治疗，"
    "另取 10mg 作为对照组。SLE 患者的 CRP 水平明显升高，CRP 与病情活动度相关。"
    "结果表明 SLE 组 50％ 达标，百分之三十部分缓解。"
    "计量资料采用ｔ检验，Ｐ<0.05 为差异有统计学意义。"
    "用量为 5 μg 与 2 µg 两组对比,结果如下。"
)
CLEAN_TEXT = (
    "本研究纳入156例患者，其中5例随访脱落。所有患者均接受5 mg剂量治疗。"
    "系统性疾病患者的炎症标志物（C反应蛋白，CRP）水平明显升高。"
    "结果显示62%的患者达到主要终点。采用t检验分析，差异有统计学意义。"
)


class TestChecks(unittest.TestCase):
    def test_bad_text_fires_all_four(self):
        r = sn.style_norm(BAD_TEXT)
        checks = {f["check"] for f in r["findings"]}
        self.assertEqual(checks, {"fullwidth", "numbers", "abbrev", "units"})
        for f in r["findings"]:
            self.assertTrue(f["advice"])
            self.assertIn(f["severity"], ("suggest", "inconsistent"))

    def test_clean_text_few_findings(self):
        r = sn.style_norm(CLEAN_TEXT)
        # 干净样本：不应有 fullwidth 全角字母数字与 μ 混用类 finding
        types = {(f["check"], f["advice"][:10]) for f in r["findings"]}
        self.assertNotIn("fullwidth", {c for c, _ in types}, f"干净样本误报全半角: {r['findings']}")

    def test_no_score_by_contract(self):
        r = sn.style_norm(BAD_TEXT)
        for k in ("score", "risk", "verdict", "overall"):
            self.assertNotIn(k, r, f"规范自查不应出现判定类字段: {k}")

    def test_mu_variants_detected(self):
        r = sn.style_norm("剂量 5 μg 与 2 µg。剂量 5 μg 组。剂量 2 µg 组。")
        self.assertTrue(any(f["check"] == "units" and "U+" in str(f["examples"])
                            for f in r["findings"]), r["findings"])

    def test_invalid_input_and_checks(self):
        with self.assertRaises(ValueError):
            sn.style_norm("")
        with self.assertRaises(ValueError):
            sn.style_norm("正常文本" * 20, checks=["no_such_check"])

    def test_sdk_parity(self):
        import pp_api
        r = pp_api.style_norm(BAD_TEXT)
        self.assertIn("finding_count", r)

    def test_cli_json_and_short(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "t.txt"
            p.write_text(BAD_TEXT, encoding="utf-8")
            out = subprocess.run([sys.executable, str(SCRIPTS / "pp_style_norm.py"),
                                  str(p), "--json"],
                                 capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(out.returncode, 0, out.stderr)
            d = json.loads(out.stdout)
            self.assertIn("findings", d)
            self.assertIn("integrity_notice", d)


if __name__ == "__main__":
    unittest.main()
