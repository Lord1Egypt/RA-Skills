# -*- coding: utf-8 -*-
"""pp_rewrite_check 改写效果回归验证契约。"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

try:
    from tests._common import AI_TEXT, HUMAN_TEXT, SCRIPTS
except ImportError:
    from _common import AI_TEXT, HUMAN_TEXT, SCRIPTS
import pp_rewrite_check as rc


class TestRewriteCheck(unittest.TestCase):
    def test_full_rewrite_moves_band(self):
        # 演示对：AI 感原稿(98.1/high) → 具体化重写(30.4/low)，已实测稳定迁移
        r = rc.rewrite_check(rc._DEMO_ORIG, rc._DEMO_REV, lang="zh")
        d = r["document"]
        self.assertGreater(d["original_score"], d["revised_score"])
        self.assertTrue(d["risk_moved"])
        self.assertEqual(d["revised_risk"], "low")
        self.assertTrue(r["integrity_notice"])

    def test_identical_text_zero_delta(self):
        r = rc.rewrite_check(HUMAN_TEXT, HUMAN_TEXT, lang="zh")
        self.assertEqual(r["document"]["delta"], 0.0)
        self.assertFalse(r["document"]["risk_moved"])
        self.assertEqual(r["features"]["original_total"], r["features"]["revised_total"])

    def test_feature_delta_keys(self):
        r = rc.rewrite_check(AI_TEXT, HUMAN_TEXT, lang="zh")
        for x in r["features"]["delta_by_type"]:
            for k in ("type", "original", "revised", "change"):
                self.assertIn(k, x)

    def test_invalid_input_raises(self):
        with self.assertRaises(ValueError):
            rc.rewrite_check("", HUMAN_TEXT)
        with self.assertRaises(ValueError):
            rc.rewrite_check(AI_TEXT, "   ")

    def test_sdk_parity(self):
        import pp_api
        r = pp_api.rewrite_check(AI_TEXT, HUMAN_TEXT)
        self.assertIn("document", r)

    def test_cli_json_and_short_refusal(self):
        with tempfile.TemporaryDirectory() as td:
            po = Path(td) / "o.txt"
            pr = Path(td) / "r.txt"
            ps = Path(td) / "s.txt"
            po.write_text(AI_TEXT, encoding="utf-8")
            pr.write_text(HUMAN_TEXT, encoding="utf-8")
            ps.write_text("太短", encoding="utf-8")
            out = subprocess.run([sys.executable, str(SCRIPTS / "pp_rewrite_check.py"),
                                  str(po), str(pr), "--json"],
                                 capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(out.returncode, 0, out.stderr)
            d = json.loads(out.stdout)
            self.assertIn("edit_extent", d)
            bad = subprocess.run([sys.executable, str(SCRIPTS / "pp_rewrite_check.py"),
                                  str(ps), str(pr)],
                                 capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(bad.returncode, 2)
            self.assertIn("100", bad.stderr)

    def test_demo_runs(self):
        out = subprocess.run([sys.executable, str(SCRIPTS / "pp_rewrite_check.py"), "--demo"],
                             capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("改写效果对比", out.stdout)


if __name__ == "__main__":
    unittest.main()
