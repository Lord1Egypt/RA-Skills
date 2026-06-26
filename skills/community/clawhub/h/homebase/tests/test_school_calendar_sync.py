"""
test_school_calendar_sync.py — Smoke tests for school_calendar_sync.py

After the OpenClaw agentic refactor, school_calendar_sync.py only owns PDF
text extraction. The old per-school attribution / event-formatting / sync
logic was moved up to the agent layer — the OpenClaw agent composes school
summaries itself from the raw PDF text + Gmail metadata.

These tests cover the surviving Python surface only.
"""
from __future__ import annotations

import sys
import types
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

# Stub external deps so import never touches the network
for _mod in (
    "google", "google.oauth2", "google.oauth2.credentials",
    "google.auth", "google.auth.transport", "google.auth.transport.requests",
    "googleapiclient", "googleapiclient.discovery",
):
    sys.modules.setdefault(_mod, types.ModuleType(_mod))

import features.school.school_calendar_sync as scs


class TestExtractPdfText:
    def test_returns_empty_string_on_import_error(self):
        """No pypdf installed → return '' instead of crashing the cron job."""
        with patch.dict(sys.modules, {"pypdf": None}):
            result = scs.extract_pdf_text_from_bytes(b"fake pdf bytes")
        assert isinstance(result, str)

    def test_returns_empty_string_on_invalid_bytes(self):
        """Garbage bytes must not raise — extractor swallows + returns ''."""
        result = scs.extract_pdf_text_from_bytes(b"not a pdf")
        assert isinstance(result, str)
        assert result == ""

    def test_returns_empty_string_on_empty_bytes(self):
        result = scs.extract_pdf_text_from_bytes(b"")
        assert result == ""


class TestCollectPdfParts:
    def test_finds_top_level_pdf(self):
        out: list = []
        scs._collect_pdf_parts({"mimeType": "application/pdf", "filename": "f.pdf"}, out)
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
        scs._collect_pdf_parts(payload, out)
        assert len(out) == 2

    def test_ignores_non_pdf(self):
        out: list = []
        scs._collect_pdf_parts({"mimeType": "image/jpeg"}, out)
        assert out == []
