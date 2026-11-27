"""
test_school_calendar_sync.py — Smoke tests for school_calendar_sync.py

After the OpenClaw agentic refactor, school_calendar_sync.py only owns PDF
text extraction and image attachment download. The old per-school
attribution / event-formatting / sync logic was moved up to the agent layer.

These tests cover the surviving Python surface only.
"""
from __future__ import annotations

import base64
import os
import sys
import time
import types
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))


import features.school.school_calendar_sync as scs


class TestCollectImageParts:
    def test_finds_top_level_image(self):
        out: list = []
        scs._collect_image_parts({"mimeType": "image/jpeg", "filename": "photo.jpg"}, out)
        assert len(out) == 1

    def test_recurses_into_multipart(self):
        payload = {
            "mimeType": "multipart/mixed",
            "parts": [
                {"mimeType": "text/plain"},
                {"mimeType": "image/png", "filename": "a.png"},
                {"mimeType": "multipart/related", "parts": [
                    {"mimeType": "image/jpeg", "filename": "b.jpg"},
                ]},
            ],
        }
        out: list = []
        scs._collect_image_parts(payload, out)
        assert len(out) == 2

    def test_ignores_non_image(self):
        out: list = []
        scs._collect_image_parts({"mimeType": "application/pdf"}, out)
        assert out == []


class TestDownloadImageAttachments:
    def test_downloads_inline_data(self, tmp_path):
        """Image with inline base64 data is saved to disk."""
        img_bytes = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
        payload = {
            "mimeType": "image/png",
            "filename": "newsletter.png",
            "body": {"data": base64.urlsafe_b64encode(img_bytes).decode()},
        }
        paths = scs.download_image_attachments("msg123", payload, str(tmp_path))
        assert len(paths) == 1
        assert os.path.isfile(paths[0])
        with open(paths[0], "rb") as f:
            assert f.read() == img_bytes

    def test_downloads_attachment_by_id(self, tmp_path):
        """Image with attachmentId is fetched through core.gmail (gog)."""
        img_bytes = b"\xff\xd8\xff" + b"\x00" * 50
        payload = {
            "mimeType": "image/jpeg",
            "filename": "photo.jpg",
            "body": {"attachmentId": "att_abc"},
        }
        with patch("core.gmail.get_attachment", return_value=img_bytes):
            paths = scs.download_image_attachments("msg456", payload, str(tmp_path))
        assert len(paths) == 1
        assert os.path.isfile(paths[0])

    def test_skips_when_no_data(self, tmp_path):
        """Part with neither attachmentId nor data is skipped."""
        payload = {"mimeType": "image/jpeg", "body": {}}
        paths = scs.download_image_attachments("msg789", payload, str(tmp_path))
        assert paths == []

    def test_returns_empty_for_no_image_parts(self, tmp_path):
        """Non-image payload returns empty list."""
        payload = {"mimeType": "text/plain", "body": {"data": "dGVzdA=="}}
        paths = scs.download_image_attachments("msg000", payload, str(tmp_path))
        assert paths == []


class TestCleanupOldAttachments:
    def test_removes_old_files(self, tmp_path):
        old_file = tmp_path / "old_image.jpg"
        old_file.write_bytes(b"old")
        # Set mtime to 10 days ago
        old_time = time.time() - (10 * 86400)
        os.utime(old_file, (old_time, old_time))

        new_file = tmp_path / "new_image.jpg"
        new_file.write_bytes(b"new")

        scs.cleanup_old_attachments(str(tmp_path), max_age_days=7)
        assert not old_file.exists()
        assert new_file.exists()

    def test_handles_nonexistent_dir(self):
        scs.cleanup_old_attachments("/nonexistent/dir/12345")


class TestMimeToExt:
    def test_known_types(self):
        assert scs._mime_to_ext("image/jpeg") == ".jpg"
        assert scs._mime_to_ext("image/png") == ".png"
        assert scs._mime_to_ext("image/gif") == ".gif"

    def test_unknown_defaults_to_jpg(self):
        assert scs._mime_to_ext("image/tiff") == ".jpg"
