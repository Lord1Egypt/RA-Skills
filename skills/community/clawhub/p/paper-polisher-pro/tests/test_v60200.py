# -*- coding: utf-8 -*-
"""v6.2.0 契约测试（test_v60200）：rewrite-check 双栏对照 HTML / html-report 信号细节节。"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
SCRIPTS = PKG / "scripts"
PY = sys.executable


def _run(*args, timeout=180):
    return subprocess.run([PY, *map(str, args)], capture_output=True,
                          text=True, timeout=timeout, cwd=str(PKG))


class TestRewriteHtml(unittest.TestCase):
    """头牌：改写对照双栏 HTML。"""

    @classmethod
    def setUpClass(cls):
        cls.dir = Path(tempfile.mkdtemp(prefix="rc62_"))
        sys.path.insert(0, str(SCRIPTS))
        import pp_rewrite_check as rc
        (cls.dir / "orig.txt").write_text(rc._DEMO_ORIG, encoding="utf-8")
        (cls.dir / "rev.txt").write_text(rc._DEMO_REV, encoding="utf-8")
        # 注入探针：原稿带脚本片段，验证转义
        evil = cls.dir / "evil.txt"
        evil.write_text(rc._DEMO_ORIG + "\n<script>alert(1)</script>", encoding="utf-8")
        cls.html = cls.dir / "cmp.html"
        r = _run(SCRIPTS / "pp_rewrite_check.py", cls.dir / "orig.txt",
                 cls.dir / "rev.txt", "--html", cls.html)
        assert r.returncode == 0, r.stderr[-300:]
        cls.evil_html = cls.dir / "evil.html"
        r2 = _run(SCRIPTS / "pp_rewrite_check.py", evil, cls.dir / "rev.txt",
                  "--html", cls.evil_html)
        assert r2.returncode == 0, r2.stderr[-300:]

    def test_html_sections(self):
        html = self.html.read_text(encoding="utf-8")
        for kw in ("逐段对照", "风险带", "特征类型增减", "学术诚信", "分数变化"):
            self.assertIn(kw, html, f"对照 HTML 缺: {kw}")
        self.assertNotIn("<script src", html)
        self.assertNotIn("@import", html)

    def test_xss_escaped(self):
        html = self.evil_html.read_text(encoding="utf-8")
        self.assertNotIn("<script>alert", html)

    def test_json_excerpts_added(self):
        r = _run(SCRIPTS / "pp_rewrite_check.py", self.dir / "orig.txt",
                 self.dir / "rev.txt", "--json")
        self.assertEqual(r.returncode, 0, r.stderr[-300:])
        d = json.loads(r.stdout)
        rows = d["paragraphs"]
        self.assertTrue(any(row.get("original_excerpt") for row in rows),
                        "para_rows 缺 original_excerpt 字段")


class TestReportHtmlSignals(unittest.TestCase):
    """html-report 信号细节节（语域/混写/篇章/LLM 腔，有值才渲染）。"""

    def test_signal_section(self):
        out = Path(tempfile.mkdtemp(prefix="sig_")) / "wf.html"
        r = _run(SCRIPTS / "pp_report_html.py",
                 PKG / "examples" / "outputs" / "workflow_sample.json", "-o", out)
        self.assertEqual(r.returncode, 0, r.stderr[-300:])
        html = out.read_text(encoding="utf-8")
        self.assertIn("信号细节", html)
        self.assertNotIn("<script src", html)


if __name__ == "__main__":
    unittest.main()
