# -*- coding: utf-8 -*-
"""v5.4.0 契约：期刊口径 2.0 学科语境 / 保鲜状态 / 二进制输入护栏。"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

try:
    from tests._common import AI_TEXT, SCRIPTS
except ImportError:
    from _common import AI_TEXT, SCRIPTS
from ai_detector import detect_discipline, journal_profile_data
import ai_detector


class TestDiscipline(unittest.TestCase):
    MED = "本研究纳入156例患者，临床随访评估疗效，对照组给予常规治疗，随访终点为复发。"
    ENG = "本文提出一种深度学习算法，在公开数据集上仿真验证，模型精度提升，传感器网络同步优化。"
    SOC = "本文通过问卷调查与访谈研究社会政策对教育管理的影响，采用回归分析检验制度效应。"

    def test_classification(self):
        self.assertEqual(detect_discipline(self.MED), "medical")
        self.assertEqual(detect_discipline(self.ENG), "engineering")
        self.assertEqual(detect_discipline(self.SOC), "social")

    def test_general_fallback(self):
        self.assertEqual(detect_discipline("这是一段没有学科特征的普通文本。"), "general")

    def test_override(self):
        self.assertEqual(detect_discipline(self.MED, override="social"), "social")
        self.assertEqual(detect_discipline(self.MED, override="nope"), "medical")

    def test_context_covers_all(self):
        for d in ("medical", "engineering", "social", "general"):
            self.assertTrue(ai_detector._DISCIPLINE_CONTEXT[d].strip())


class TestJournalProfile20(unittest.TestCase):
    def test_fields_present(self):
        rep = ai_detector.detect(AI_TEXT, lang="zh")
        jp = journal_profile_data(rep, AI_TEXT)
        for k in ("discipline", "discipline_context", "reference_line_discipline_note",
                  "suspected_paragraph_pct", "suspected_char_weighted_pct", "reference_line"):
            self.assertIn(k, jp)
        self.assertEqual(jp["discipline"], "medical")  # AI 样例为医学语境

    def test_cli_json_pure_and_override(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "t.txt"
            p.write_text(AI_TEXT, encoding="utf-8")
            for extra in ([], ["--discipline", "social"]):
                out = subprocess.run([sys.executable, str(SCRIPTS / "ai_detector.py"),
                                      str(p), "--profile", "journal", "--format", "json"] + extra,
                                     capture_output=True, text=True, encoding="utf-8")
                self.assertEqual(out.returncode, 0, out.stderr[-200:])
                d = json.loads(out.stdout)  # 纯 JSON 可解析
                jp = d["journal_precheck"]
                self.assertIn("discipline_context", jp)
                if extra:
                    self.assertEqual(jp["discipline"], "social")


class TestFreshnessStatus(unittest.TestCase):
    def test_status_contract(self):
        import io
        import contextlib
        import freshness_refresh as fr
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = fr.status(json_out=True)
        self.assertEqual(rc, 0)
        d = json.loads(buf.getvalue())
        for k in ("last_refresh", "latest_eval_record", "baseline_drift",
                  "baselines_expected", "due_for_refresh"):
            self.assertIn(k, d)
        self.assertNotIn(1, [0])  # no-op sanity
        self.assertEqual(d["baselines_expected"]["fused_oldgen"], 0.9998)

    def test_cli_status(self):
        out = subprocess.run([sys.executable, str(SCRIPTS / "freshness_refresh.py"),
                              "--status", "--json"],
                             capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(out.returncode, 0, out.stderr[-200:])
        d = json.loads(out.stdout)
        self.assertIn("due_for_refresh", d)


class TestBinaryGuard(unittest.TestCase):
    def test_pdf_rejected_with_advice(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "f.pdf"
            p.write_bytes(b"%PDF-1.4 fake")
            from docx_text import read_text_any, DocxError
            with self.assertRaises(DocxError) as cm:
                read_text_any(p)
            self.assertIn("PDF", str(cm.exception))
            self.assertIn("docx", str(cm.exception))

    def test_all_entries_clean_error(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "f.pdf"
            p.write_bytes(b"%PDF-1.4 fake")
            for script in ("pp_fix_suggest.py", "pp_style_norm.py", "pp_workflow.py",
                           "ai_detector.py"):
                out = subprocess.run([sys.executable, str(SCRIPTS / script), str(p)],
                                     capture_output=True, text=True, encoding="utf-8")
                # ai_detector 既有惯例坏输入 exit 1，其余入口 2——统一断言「非零+干净+有指引」
                self.assertNotEqual(out.returncode, 0, f"{script} rc=0")
                self.assertNotIn("Traceback", out.stderr, f"{script} 抛栈")
                self.assertIn("PDF", out.stderr)


if __name__ == "__main__":
    unittest.main()
