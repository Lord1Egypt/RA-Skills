# -*- coding: utf-8 -*-
"""v6.3.0 契约测试（test_v60300）：FAQ 独立档案 / pp.py faq 检索 / SKILL 瘦身 / pp_errors 指针。"""
import os
import subprocess
import sys
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))
import _docs
SCRIPTS = PKG / "scripts"
PY = sys.executable


def _run(*args, timeout=60, env_extra=None):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    return subprocess.run([PY, *map(str, args)], capture_output=True,
                          text=True, timeout=timeout, cwd=str(PKG), env=env)


class TestFaqFile(unittest.TestCase):
    """独立 FAQ 档案：内容完整性。"""

    def test_faq_file_exists_and_grouped(self):
        f = PKG / "references" / "faq.md"
        self.assertTrue(f.is_file())
        t = f.read_text(encoding="utf-8")
        for kw in ("判定与边界", "具体技术问题", "PDF", "熔断", "退出码", "AST"):
            self.assertIn(kw, t, f"FAQ 缺: {kw}")

    def test_skill_keeps_top3_and_link(self):
        for doc in _docs.DOCS:
            t = (PKG / doc).read_text(encoding="utf-8")
            self.assertIn("references/faq.md", t, f"{doc} 缺 FAQ 链接")
            self.assertIn("100", t)  # 高频第一条仍在


class TestFaqSearch(unittest.TestCase):
    """pp.py faq 检索：关键词命中与兜底。"""

    def test_keyword_hit_curated(self):
        r = _run(SCRIPTS / "pp.py", "faq", "PDF")
        self.assertEqual(r.returncode, 0)
        self.assertIn("不支持 PDF", r.stdout, "PDF 应命中精选条目")

    def test_keyword_hit_exitcode(self):
        r = _run(SCRIPTS / "pp.py", "faq", "退出码")
        self.assertEqual(r.returncode, 0)
        self.assertIn("0/1/2/3", r.stdout)

    def test_no_hit_fallback(self):
        r = _run(SCRIPTS / "pp.py", "faq", "zzzqqq")
        self.assertEqual(r.returncode, 0)
        self.assertIn("references/faq.md", r.stdout)

    def test_registered_in_help(self):
        r = _run(SCRIPTS / "pp.py")
        self.assertIn("faq", r.stdout)


class TestErrorsFaqPointer(unittest.TestCase):
    """pp_errors 联动：错误输出带 FAQ 指针。"""

    def test_friendly_error_has_faq_pointer(self):
        r = _run(SCRIPTS / "ai_detector.py", "/tmp/definitely_not_here_630.txt")
        self.assertEqual(r.returncode, 2)
        self.assertIn("pp.py faq", r.stderr)


if __name__ == "__main__":
    unittest.main()
