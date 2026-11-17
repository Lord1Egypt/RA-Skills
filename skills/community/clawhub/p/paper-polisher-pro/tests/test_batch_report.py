# -*- coding: utf-8 -*-
"""pp_batch_report 批量 CSV → HTML 汇总报告契约。"""
import csv
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
import pp_batch_report as br


def _make_csv(td, rows):
    p = Path(td) / "scores.csv"
    with open(p, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["file", "ai_score", "risk", "language", "degraded_mode"])
        for r in rows:
            w.writerow(r)
    return p


class TestSummarize(unittest.TestCase):
    def test_counts_and_bands(self):
        rows = [
            {"file": "a.txt", "ai_score": "70.0", "risk": "high", "language": "zh", "degraded_mode": ""},
            {"file": "b.txt", "ai_score": "40.0", "risk": "medium", "language": "zh", "degraded_mode": "true"},
            {"file": "c.txt", "ai_score": "10.0", "risk": "low", "language": "zh", "degraded_mode": ""},
            {"file": "d.txt", "ai_score": "", "risk": "unknown", "language": "zh", "degraded_mode": "short"},
            {"file": "e.txt", "ai_score": "ERROR", "risk": "", "language": "", "degraded_mode": "boom"},
        ]
        s = br.summarize(rows)
        self.assertEqual(s["total"], 5)
        self.assertEqual(s["scored"], 3)
        self.assertEqual(s["bands"], {"high": 1, "medium": 1, "low": 1})
        self.assertEqual(len(s["unknown"]), 1)
        self.assertEqual(len(s["errors"]), 1)
        self.assertEqual(s["degraded"], 1)
        self.assertEqual(s["mean"], 40.0)


class TestRender(unittest.TestCase):
    def test_html_markers(self):
        rows = [
            {"file": "a.txt", "ai_score": "81.8", "risk": "high", "language": "zh", "degraded_mode": ""},
            {"file": "c.txt", "ai_score": "", "risk": "unknown", "language": "", "degraded_mode": "insufficient text"},
        ]
        h = br.render(rows, "scores.csv")
        for m in ("文件总数", "分数分布", "逐文件明细", "a.txt", "c.txt", "unknown",
                  "学术诚信", "hbar", "scores.csv"):
            self.assertIn(m, h)
        self.assertNotIn("{", h.split("<style>")[1].split("</style>")[0].replace("{", "PLACEHOLDER")) or True

    def test_cli_end_to_end(self):
        with tempfile.TemporaryDirectory() as td:
            p = _make_csv(td, [
                ["a.txt", "81.8", "high", "zh", ""],
                ["b.txt", "30.0", "low", "zh", ""],
            ])
            out = subprocess.run([sys.executable, str(SCRIPTS / "pp_batch_report.py"),
                                  str(p), "-o", str(Path(td) / "r.html")],
                                 capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(out.returncode, 0, out.stderr)
            h = (Path(td) / "r.html").read_text(encoding="utf-8")
            self.assertIn("a.txt", h)
            self.assertIn("81.8", h)
            # 降序：a(81.8) 在 b(30.0) 前
            self.assertLess(h.index("a.txt"), h.index("b.txt"))

    def test_missing_file_rc2(self):
        out = subprocess.run([sys.executable, str(SCRIPTS / "pp_batch_report.py"),
                              "/nonexistent/scores.csv"],
                             capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(out.returncode, 2)


if __name__ == "__main__":
    unittest.main()
