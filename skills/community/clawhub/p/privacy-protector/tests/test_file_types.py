#!/usr/bin/env python3

import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
import sys

sys.path.insert(0, str(SCRIPTS_DIR))

from modeio_redact.workflow import file_types  # noqa: E402


class TestFileTypes(unittest.TestCase):
    def test_supported_extensions_include_core_text_and_structured_types(self):
        self.assertIn(".txt", file_types.SUPPORTED_FILE_EXTENSIONS)
        self.assertIn(".md", file_types.SUPPORTED_FILE_EXTENSIONS)
        self.assertIn(".json", file_types.SUPPORTED_FILE_EXTENSIONS)
        self.assertIn(".csv", file_types.SUPPORTED_FILE_EXTENSIONS)
        self.assertIn(".docx", file_types.SUPPORTED_FILE_EXTENSIONS)
        self.assertIn(".pdf", file_types.SUPPORTED_FILE_EXTENSIONS)

    def test_extension_support_lookup_is_case_insensitive(self):
        self.assertTrue(file_types.is_supported_extension(".JSON"))
        self.assertTrue(file_types.is_supported_extension(".Md"))

    def test_marker_style_mapping(self):
        self.assertEqual(
            file_types.marker_style_for_extension(".txt"),
            file_types.MAP_MARKER_STYLE_HASH,
        )
        self.assertEqual(
            file_types.marker_style_for_extension(".md"),
            file_types.MAP_MARKER_STYLE_HTML_COMMENT,
        )
        self.assertEqual(
            file_types.marker_style_for_extension(".json"),
            file_types.MAP_MARKER_STYLE_NONE,
        )
        self.assertEqual(
            file_types.marker_style_for_extension(".pdf"),
            file_types.MAP_MARKER_STYLE_NONE,
        )

    def test_handler_mapping(self):
        self.assertEqual(file_types.handler_key_for_extension(".txt"), file_types.HANDLER_TEXT)
        self.assertEqual(file_types.handler_key_for_extension(".docx"), file_types.HANDLER_DOCX)
        self.assertEqual(file_types.handler_key_for_extension(".pdf"), file_types.HANDLER_PDF)

    def test_deanonymize_support_mapping(self):
        self.assertTrue(file_types.supports_deanonymize_for_extension(".txt"))
        self.assertTrue(file_types.supports_deanonymize_for_extension(".docx"))
        self.assertFalse(file_types.supports_deanonymize_for_extension(".pdf"))

    def test_pdf_level_support_includes_all_levels(self):
        self.assertTrue(file_types.is_level_supported_for_extension(".pdf", "lite"))
        self.assertTrue(file_types.is_level_supported_for_extension(".pdf", "dynamic"))
        self.assertTrue(file_types.is_level_supported_for_extension(".pdf", "strict"))
        self.assertTrue(file_types.is_level_supported_for_extension(".pdf", "crossborder"))


if __name__ == "__main__":
    unittest.main()
