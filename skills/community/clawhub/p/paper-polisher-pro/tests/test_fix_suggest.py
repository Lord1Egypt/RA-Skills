# -*- coding: utf-8 -*-
"""pp_fix_suggest 句子级改写建议契约。"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

try:
    from tests._common import AI_TEXT, HUMAN_TEXT, SCRIPTS
except ImportError:  # 直跑模式（-s tests）
    from _common import AI_TEXT, HUMAN_TEXT, SCRIPTS
import pp_fix_suggest as fx


class TestAnalyze(unittest.TestCase):
    def test_ai_text_flagged(self):
        results, stats, lang = fx.analyze(AI_TEXT, lang="zh")
        self.assertEqual(lang, "zh")
        self.assertGreaterEqual(stats["flagged_sentences"], 3)
        self.assertGreater(stats["flag_ratio"], 0.3)

    def test_human_text_clean(self):
        results, stats, _ = fx.analyze(HUMAN_TEXT, lang="zh")
        self.assertEqual(stats["flagged_sentences"], 0)

    def test_types_are_canonical(self):
        results, _, _ = fx.analyze(AI_TEXT, lang="zh")
        valid = set(fx.ADVICE.keys())
        for r in results:
            for x in r["issues"]:
                self.assertIn(x["type"], valid, f"未知 type: {x['type']}")

    def test_no_duplicate_type_per_sentence(self):
        results, _, _ = fx.analyze(AI_TEXT, lang="zh")
        for r in results:
            types = [x["type"] for x in r["issues"]]
            self.assertEqual(len(types), len(set(types)), f"同句重复 type: {types}")

    def test_advice_nonempty_for_every_type(self):
        for t, advice in fx.ADVICE.items():
            self.assertTrue(advice.strip(), f"{t} 缺改写策略")


class TestJsonContract(unittest.TestCase):
    def test_cli_json(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8") as f:
            f.write(AI_TEXT)
            p = f.name
        try:
            out = subprocess.run([sys.executable, str(SCRIPTS / "pp_fix_suggest.py"),
                                  p, "--json", "--top", "2"],
                                 capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(out.returncode, 0, out.stderr)
            d = json.loads(out.stdout)
            self.assertLessEqual(len(d["suggestions"]), 2)
            self.assertIn("integrity_notice", d)
            self.assertIn("stats", d)
            for s in d["suggestions"]:
                self.assertIn("sentence", s)
                for i in s["issues"]:
                    self.assertIn("advice", i)
        finally:
            Path(p).unlink(missing_ok=True)

    def test_short_text_refused(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8") as f:
            f.write("太短了。")
            p = f.name
        try:
            out = subprocess.run([sys.executable, str(SCRIPTS / "pp_fix_suggest.py"), p],
                                 capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(out.returncode, 2)
            self.assertIn("100", out.stderr)
        finally:
            Path(p).unlink(missing_ok=True)

    def test_demo_runs(self):
        out = subprocess.run([sys.executable, str(SCRIPTS / "pp_fix_suggest.py"), "--demo"],
                             capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("样例 A", out.stdout)
        self.assertIn("样例 B", out.stdout)


if __name__ == "__main__":
    unittest.main()
