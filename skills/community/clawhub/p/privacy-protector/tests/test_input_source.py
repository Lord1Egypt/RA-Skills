#!/usr/bin/env python3

import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
import sys

sys.path.insert(0, str(SCRIPTS_DIR))

from modeio_redact.workflow.input_source import resolve_input_source_context  # noqa: E402

try:  # noqa: E402
    from docx import Document

    HAS_DOCX = True
except ModuleNotFoundError:  # pragma: no cover
    HAS_DOCX = False

try:  # noqa: E402
    import fitz

    HAS_FITZ = True
except ModuleNotFoundError:  # pragma: no cover
    HAS_FITZ = False


class TestInputSource(unittest.TestCase):
    def test_literal_text_input(self):
        context = resolve_input_source_context("Email: alice@example.com")
        self.assertEqual(context.input_type, "text")
        self.assertIsNone(context.input_path)
        self.assertIsNone(context.extension)
        self.assertEqual(context.content, "Email: alice@example.com")

    def test_text_file_input(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8", delete=False) as handle:
            handle.write("Email: alice@example.com")
            path = Path(handle.name)

        try:
            context = resolve_input_source_context(str(path))
        finally:
            path.unlink(missing_ok=True)

        self.assertEqual(context.input_type, "file")
        self.assertEqual(context.extension, ".txt")
        self.assertEqual(context.handler_key, "text")
        self.assertIn("alice@example.com", context.content)

    @unittest.skipUnless(HAS_DOCX, "python-docx is required")
    def test_docx_file_input(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sample.docx"
            document = Document()
            document.add_paragraph("Email: alice@example.com")
            document.save(str(path))

            context = resolve_input_source_context(str(path))

        self.assertEqual(context.input_type, "file")
        self.assertEqual(context.extension, ".docx")
        self.assertEqual(context.handler_key, "docx")
        self.assertIn("alice@example.com", context.content)

    @unittest.skipUnless(HAS_FITZ, "PyMuPDF is required")
    def test_pdf_file_input(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sample.pdf"
            document = fitz.open()
            page = document.new_page()
            page.insert_text((72, 72), "Email: alice@example.com")
            document.save(str(path))
            document.close()

            context = resolve_input_source_context(str(path))

        self.assertEqual(context.input_type, "file")
        self.assertEqual(context.extension, ".pdf")
        self.assertEqual(context.handler_key, "pdf")
        self.assertIn("alice@example.com", context.content)

    def test_unsupported_file_extension(self):
        with tempfile.NamedTemporaryFile("w", suffix=".bin", encoding="utf-8", delete=False) as handle:
            handle.write("x")
            path = Path(handle.name)

        try:
            with self.assertRaises(ValueError):
                resolve_input_source_context(str(path))
        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
