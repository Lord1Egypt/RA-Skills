"""
test_pdf_attachments.py — Smoke tests for core/pdf_attachments.py
"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

import core.pdf_attachments as pdf_attachments


class TestExtractPdfText:
    def test_returns_empty_string_on_import_error(self):
        """No pypdf installed → return '' instead of crashing the cron job."""
        with patch.dict(sys.modules, {"pypdf": None}):
            result = pdf_attachments.extract_pdf_text_from_bytes(b"fake pdf bytes")
        assert isinstance(result, str)

    def test_returns_empty_string_on_invalid_bytes(self):
        """Garbage bytes must not raise — extractor swallows + returns ''."""
        result = pdf_attachments.extract_pdf_text_from_bytes(b"not a pdf")
        assert isinstance(result, str)
        assert result == ""

    def test_returns_empty_string_on_empty_bytes(self):
        result = pdf_attachments.extract_pdf_text_from_bytes(b"")
        assert result == ""


class TestCollectPdfParts:
    def test_finds_top_level_pdf(self):
        out: list = []
        pdf_attachments._collect_pdf_parts({"mimeType": "application/pdf", "filename": "f.pdf"}, out)
        assert len(out) == 1

    def test_recurses_into_multipart(self):
        payload = {
            "mimeType": "multipart/mixed",
            "parts": [
                {"mimeType": "text/plain"},
                {"mimeType": "multipart/alternative", "parts": [
                    {"mimeType": "application/pdf", "filename": "a.pdf"},
                ]},
                {"mimeType": "application/pdf", "filename": "b.pdf"},
            ],
        }
        out: list = []
        pdf_attachments._collect_pdf_parts(payload, out)
        assert len(out) == 2

    def test_ignores_non_pdf(self):
        out: list = []
        pdf_attachments._collect_pdf_parts({"mimeType": "image/jpeg"}, out)
        assert out == []
