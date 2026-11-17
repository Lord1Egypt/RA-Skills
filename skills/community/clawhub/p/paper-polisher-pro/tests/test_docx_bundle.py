# -*- coding: utf-8 -*-
"""docx_text 与 pp_report_bundle 契约（v5.3.0）。"""
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

try:
    from tests._common import AI_TEXT, SCRIPTS
except ImportError:
    from _common import AI_TEXT, SCRIPTS
import docx_text

_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def _make_docx(path, paras):
    body = "".join(
        f'<w:p xmlns:w="{_W}"><w:r><w:t xml:space="preserve">{x}</w:t></w:r></w:p>'
        for x in paras)
    doc = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           f'<w:document xmlns:w="{_W}">{body}</w:document>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", '<?xml version="1.0"?><Types/>')
        z.writestr("word/document.xml", doc)


class TestDocxText(unittest.TestCase):
    def test_extract_paragraphs(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "t.docx"
            _make_docx(p, ["第一段内容。", "第二段内容。", "第三段内容。"])
            t = docx_text.docx_to_text(p)
            self.assertIn("第一段内容", t)
            self.assertIn("第三段内容", t)
            self.assertIn("\n\n", t)  # 段落间保留空行

    def test_fake_docx_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "fake.docx"
            p.write_text("not a zip")
            with self.assertRaises(docx_text.DocxError):
                docx_text.docx_to_text(p)

    def test_missing_document_part_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "x.docx"
            with zipfile.ZipFile(p, "w") as z:
                z.writestr("other.xml", "<x/>")
            with self.assertRaises(docx_text.DocxError):
                docx_text.docx_to_text(p)

    def test_read_text_any_dispatch(self):
        with tempfile.TemporaryDirectory() as td:
            dx = Path(td) / "a.docx"
            _make_docx(dx, ["Word 正文。"])
            tx = Path(td) / "b.txt"
            tx.write_text("纯文本内容。", encoding="utf-8")
            self.assertIn("Word 正文", docx_text.read_text_any(dx))
            self.assertIn("纯文本内容", docx_text.read_text_any(tx))


class TestDetectorDocx(unittest.TestCase):
    def test_single_file_detect_docx(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "d.docx"
            _make_docx(p, [AI_TEXT])
            out = subprocess.run([sys.executable, str(SCRIPTS / "ai_detector.py"),
                                  str(p), "--format", "json"],
                                 capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(out.returncode, 0, out.stderr[-300:])
            d = json.loads(out.stdout)
            self.assertIn("overall_ai_score", d)

    def test_batch_collects_docx(self):
        with tempfile.TemporaryDirectory() as td:
            _make_docx(Path(td) / "w.docx", [AI_TEXT])
            (Path(td) / "n.txt").write_text("这不是一篇足够长的文本。" * 20, encoding="utf-8")
            out = subprocess.run([sys.executable, str(SCRIPTS / "ai_detector.py"),
                                  "--batch", td, "--csv", str(Path(td) / "s.csv")],
                                 capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(out.returncode, 0, out.stderr[-300:])
            csv_text = (Path(td) / "s.csv").read_text(encoding="utf-8-sig")
            self.assertIn("w.docx", csv_text)
            self.assertIn("n.txt", csv_text)


class TestBundle(unittest.TestCase):
    def test_build_bundle_docx(self):
        import pp_report_bundle as rb
        with tempfile.TemporaryDirectory() as td:
            dx = Path(td) / "t.docx"
            _make_docx(dx, [AI_TEXT])
            r = rb.build_bundle(str(dx), outdir=td)
            bdir = Path(r["bundle_dir"])
            for name in ("README.md", "workflow.md", "workflow.json",
                         "fix_suggest.txt", "style_norm.txt"):
                self.assertTrue((bdir / name).exists(), f"缺 {name}")
            manifest = (bdir / "README.md").read_text(encoding="utf-8")
            self.assertIn("阅读顺序", manifest)
            self.assertIn("学术诚信", manifest)
            self.assertFalse((bdir / "_input.txt").exists(), "临时输入应清理")

    def test_short_refusal(self):
        import pp_report_bundle as rb
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "s.txt"
            p.write_text("太短", encoding="utf-8")
            with self.assertRaises(ValueError):
                rb.build_bundle(str(p), outdir=td)

    def test_cli(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "t.txt"
            p.write_text(AI_TEXT, encoding="utf-8")
            out = subprocess.run([sys.executable, str(SCRIPTS / "pp_report_bundle.py"),
                                  str(p), "--outdir", td],
                                 capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(out.returncode, 0, out.stderr[-300:])
            self.assertIn("自查包", out.stdout)


if __name__ == "__main__":
    unittest.main()
