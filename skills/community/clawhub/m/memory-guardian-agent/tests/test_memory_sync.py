"""Tests for memory_sync — file-to-meta.json synchronization."""

import json
import os
import pytest
from datetime import datetime, timedelta

from memory_sync import (
    get_cooldown_minutes,
    _file_needs_sync,
    _dir_needs_sync,
    _extract_paragraphs,
    _assign_importance,
    process_inbox,
)


class TestGetCooldownMinutes:
    def test_zero_failures(self):
        assert get_cooldown_minutes(0) == 30

    def test_exponential_backoff(self):
        c1 = get_cooldown_minutes(1)
        c2 = get_cooldown_minutes(2)
        assert c2 > c1

    def test_capped(self):
        from memory_sync import _COOLDOWN_MAX_MINUTES
        c = get_cooldown_minutes(100)
        assert c <= _COOLDOWN_MAX_MINUTES


class TestFileNeedsSync:
    def test_no_last_sync(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("content")
        # No last_sync_at → needs sync (first time)
        assert _file_needs_sync(str(f)) is True

    def test_old_file_needs_sync(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("content")
        old = (datetime.now() - timedelta(hours=2)).isoformat()
        assert _file_needs_sync(str(f), last_sync_at=old) is True

    def test_recent_file_no_sync(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("content")
        recent = datetime.now().isoformat()
        assert _file_needs_sync(str(f), last_sync_at=recent) is False


class TestDirNeedsSync:
    def test_no_last_sync(self, tmp_path):
        d = tmp_path / "test_dir"
        d.mkdir()
        assert _dir_needs_sync(str(d)) is True

    def test_nonexistent_dir(self, tmp_path):
        assert _dir_needs_sync(str(tmp_path / "nonexistent")) is False


class TestExtractParagraphs:
    def test_basic(self):
        text = "paragraph one\n\nparagraph two\n\nparagraph three"
        paras = _extract_paragraphs(text, min_length=5)
        assert len(paras) >= 2

    def test_short_paragraphs_filtered(self):
        text = "ab\n\ncd\n\nef"
        paras = _extract_paragraphs(text, min_length=5)
        assert len(paras) == 0

    def test_empty(self):
        assert _extract_paragraphs("", min_length=5) == []


class TestAssignImportance:
    def test_known_heading(self):
        assert _assign_importance("人设与偏好") == 0.9

    def test_project_heading(self):
        assert _assign_importance("项目：memory-guardian") == 0.8

    def test_unknown_heading(self):
        imp = _assign_importance("未知标题")
        assert 0.3 <= imp <= 0.7


# ─── New tests for uncovered functions ───────────────────────

class TestProcessInbox:
    def test_processes_timed_out(self, tmp_path):
        import json
        from datetime import datetime, timedelta
        from mg_utils import CST
        old_ts = (datetime.now(CST) - timedelta(days=10)).isoformat()
        meta = {
            "memories": [{
                "id": "m1",
                "memory_id": "mem_abc12345",
                "needs_review": True,
                "needs_review_since": old_ts,
                "needs_review_timeout": "7d",
            }],
        }
        p = str(tmp_path / "meta.json")
        with open(p, "w") as f:
            json.dump(meta, f)
        result = process_inbox(p)
        assert result["processed"] == 1
        assert result["details"][0]["action"] == "timed_out_to_inbox"

    def test_skips_not_timed_out(self, tmp_path):
        import json
        from datetime import datetime, timedelta
        from mg_utils import CST
        recent_ts = (datetime.now(CST) - timedelta(days=1)).isoformat()
        meta = {
            "memories": [{
                "id": "m1",
                "needs_review": True,
                "needs_review_since": recent_ts,
                "needs_review_timeout": "7d",
            }],
        }
        p = str(tmp_path / "meta.json")
        with open(p, "w") as f:
            json.dump(meta, f)
        result = process_inbox(p)
        assert result["processed"] == 0

    def test_missing_meta_file(self, tmp_path):
        result = process_inbox(str(tmp_path / "nonexistent.json"))
        assert result["processed"] == 0

    def test_skips_no_needs_review(self, tmp_path):
        import json
        meta = {
            "memories": [{
                "id": "m1",
                "needs_review": False,
            }],
        }
        p = str(tmp_path / "meta.json")
        with open(p, "w") as f:
            json.dump(meta, f)
        result = process_inbox(p)
        assert result["processed"] == 0
