"""
test_media_watcher.py — Unit tests for media_watcher.py

Architecture: Python returns *data*. There is no LLM call inside this module —
the agent (whichever model OpenClaw is configured with) reads images directly
using its native vision capability. These tests reflect that.

Covers:
  - file_hash() determinism
  - load_state() / save_state(): file locking, atomic write, missing file
  - classify_image(): caption-based receipt/snack/skip/unclassified
  - Hash deduplication in scan_and_process()
"""
import hashlib
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

# Stub Google deps before import
for mod in ("google", "google.oauth2", "google.oauth2.credentials",
            "google.auth", "google.auth.transport", "google.auth.transport.requests",
            "googleapiclient", "googleapiclient.discovery"):
    sys.modules.setdefault(mod, MagicMock())

with patch("core.keychain_secrets.load_google_secrets", return_value=None), \
     patch("core.config_loader._load_config") as _mc:
    from conftest import MINIMAL_CONFIG
    from core.config_loader import Config
    _mc.return_value = Config(MINIMAL_CONFIG)
    import features.dining.media_watcher as media_watcher


# ─── file_hash ────────────────────────────────────────────────────────────────

class TestFileHash:
    def test_deterministic_for_same_content(self, tmp_path):
        f = tmp_path / "test.jpg"
        f.write_bytes(b"hello world")
        assert media_watcher.file_hash(str(f)) == media_watcher.file_hash(str(f))

    def test_different_content_different_hash(self, tmp_path):
        f1 = tmp_path / "a.jpg"; f1.write_bytes(b"aaa")
        f2 = tmp_path / "b.jpg"; f2.write_bytes(b"bbb")
        assert media_watcher.file_hash(str(f1)) != media_watcher.file_hash(str(f2))

    def test_matches_expected_md5(self, tmp_path):
        data = b"receipt"
        f = tmp_path / "r.jpg"; f.write_bytes(data)
        assert media_watcher.file_hash(str(f)) == hashlib.md5(data).hexdigest()


# ─── load_state / save_state ─────────────────────────────────────────────────

class TestLoadState:
    def test_returns_defaults_when_file_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(media_watcher, "STATE_FILE",
                            str(tmp_path / "no_such_file.json"))
        assert media_watcher.load_state() == {"processed": [], "last_run_month": ""}

    def test_reads_existing_state(self, tmp_path, monkeypatch):
        data = {"processed": ["abc123"], "last_run_month": "2026-03"}
        sf = tmp_path / "state.json"; sf.write_text(json.dumps(data))
        monkeypatch.setattr(media_watcher, "STATE_FILE", str(sf))
        state = media_watcher.load_state()
        assert state["processed"] == ["abc123"]
        assert state["last_run_month"] == "2026-03"

    def test_corrupt_file_returns_defaults(self, tmp_path, monkeypatch):
        sf = tmp_path / "state.json"; sf.write_text("{not valid json")
        monkeypatch.setattr(media_watcher, "STATE_FILE", str(sf))
        assert media_watcher.load_state() == {"processed": [], "last_run_month": ""}


class TestSaveState:
    def test_saves_state_atomically(self, tmp_path, monkeypatch):
        sf = tmp_path / "household" / "state.json"
        sf.parent.mkdir(parents=True, exist_ok=True)
        monkeypatch.setattr(media_watcher, "STATE_FILE", str(sf))
        media_watcher.save_state({"processed": ["hash1", "hash2"], "last_run_month": "2026-03"})
        assert sf.exists()
        assert json.loads(sf.read_text())["processed"] == ["hash1", "hash2"]

    def test_overwrite_existing_state(self, tmp_path, monkeypatch):
        sf = tmp_path / "household" / "state.json"
        sf.parent.mkdir(parents=True, exist_ok=True)
        sf.write_text(json.dumps({"processed": ["old"], "last_run_month": "2026-02"}))
        monkeypatch.setattr(media_watcher, "STATE_FILE", str(sf))
        media_watcher.save_state({"processed": ["new"], "last_run_month": "2026-03"})
        assert json.loads(sf.read_text())["processed"] == ["new"]


# ─── classify_image (keyword-only, no LLM) ───────────────────────────────────

class TestClassifyImage:
    def test_receipt_via_filename(self, tmp_path):
        f = tmp_path / "receipt_2026.jpg"; f.write_bytes(b"fake")
        assert media_watcher.classify_image(str(f)) == "receipt"

    def test_receipt_via_caption_keyword(self, tmp_path):
        f = tmp_path / "photo.jpg"; f.write_bytes(b"fake")
        (tmp_path / "photo.txt").write_text("We went to a great restaurant")
        assert media_watcher.classify_image(str(f)) == "receipt"

    def test_snack_via_filename(self, tmp_path):
        f = tmp_path / "snack_schedule.jpg"; f.write_bytes(b"fake")
        assert media_watcher.classify_image(str(f)) == "snack"

    def test_snack_via_caption(self, tmp_path):
        f = tmp_path / "image.jpg"; f.write_bytes(b"fake")
        (tmp_path / "image.txt").write_text("morning snack this week")
        assert media_watcher.classify_image(str(f)) == "snack"

    def test_skip_trigger_returns_skip(self, tmp_path):
        f = tmp_path / "photo.jpg"; f.write_bytes(b"fake")
        (tmp_path / "photo.txt").write_text("selfie with family")
        assert media_watcher.classify_image(str(f)) == "skip"

    def test_screenshot_returns_skip(self, tmp_path):
        f = tmp_path / "screenshot.jpg"; f.write_bytes(b"fake")
        assert media_watcher.classify_image(str(f)) == "skip"

    def test_no_caption_returns_unclassified(self, tmp_path):
        """Captionless images go to 'unclassified' for the agent to inspect with vision."""
        f = tmp_path / "mystery.jpg"; f.write_bytes(b"fake image data")
        assert media_watcher.classify_image(str(f)) == "unclassified"

    def test_invoice_keyword_in_caption(self, tmp_path):
        f = tmp_path / "img.jpg"; f.write_bytes(b"fake")
        (tmp_path / "img.txt").write_text("food invoice for dinner")
        assert media_watcher.classify_image(str(f)) == "receipt"


# ─── Hash deduplication ───────────────────────────────────────────────────────

class TestHashDeduplication:
    def test_already_processed_image_is_skipped(self, tmp_path, monkeypatch):
        media_dir = tmp_path / "inbound"; media_dir.mkdir()
        img = media_dir / "photo.jpg"; img.write_bytes(b"some image data")
        known_hash = hashlib.md5(b"some image data").hexdigest()

        state_file = tmp_path / "household" / "state.json"
        state_file.parent.mkdir()
        state_file.write_text(json.dumps({"processed": [known_hash], "last_run_month": ""}))

        monkeypatch.setattr(media_watcher, "MEDIA_DIR", str(media_dir))
        monkeypatch.setattr(media_watcher, "STATE_FILE", str(state_file))

        with patch.object(media_watcher, "classify_image") as mock_classify, \
             patch.object(media_watcher, "send_rating_reminders", return_value=None), \
             patch.object(media_watcher, "should_skip_snacks_this_month", return_value=True), \
             patch.object(media_watcher, "save_state"):
            media_watcher.scan_and_process()

        mock_classify.assert_not_called()

    def test_new_image_is_processed_and_hash_stored(self, tmp_path, monkeypatch):
        media_dir = tmp_path / "inbound"; media_dir.mkdir()
        img = media_dir / "photo.jpg"; img.write_bytes(b"brand new image")

        state_file = tmp_path / "household" / "state.json"
        state_file.parent.mkdir()
        state_file.write_text(json.dumps({"processed": [], "last_run_month": ""}))

        monkeypatch.setattr(media_watcher, "MEDIA_DIR", str(media_dir))
        monkeypatch.setattr(media_watcher, "STATE_FILE", str(state_file))

        with patch.object(media_watcher, "classify_image", return_value="unclassified") as mock_classify, \
             patch.object(media_watcher, "send_rating_reminders", return_value=None), \
             patch.object(media_watcher, "should_skip_snacks_this_month", return_value=True), \
             patch.object(media_watcher, "save_state") as mock_save:
            result = media_watcher.scan_and_process()

        mock_classify.assert_called_once()
        saved_state = mock_save.call_args[0][0]
        assert len(saved_state["processed"]) == 1
        assert len(result["unclassified"]) == 1


# ─── scan_and_process result shape ───────────────────────────────────────────

class TestScanResultShape:
    def test_returns_no_media_dir_status(self, tmp_path, monkeypatch):
        monkeypatch.setattr(media_watcher, "MEDIA_DIR", str(tmp_path / "nope"))
        result = media_watcher.scan_and_process()
        assert result["status"] == "no_media_dir"

    def test_classifies_receipt_into_receipts_bucket(self, tmp_path, monkeypatch):
        media_dir = tmp_path / "inbound"; media_dir.mkdir()
        img = media_dir / "receipt_dinner.jpg"; img.write_bytes(b"x")
        state_file = tmp_path / "household" / "state.json"
        state_file.parent.mkdir()
        state_file.write_text(json.dumps({"processed": [], "last_run_month": ""}))

        monkeypatch.setattr(media_watcher, "MEDIA_DIR", str(media_dir))
        monkeypatch.setattr(media_watcher, "STATE_FILE", str(state_file))

        with patch.object(media_watcher, "send_rating_reminders", return_value=None), \
             patch.object(media_watcher, "should_skip_snacks_this_month", return_value=True):
            result = media_watcher.scan_and_process()

        assert len(result["receipts"]) == 1
        assert result["receipts"][0]["file"] == "receipt_dinner.jpg"
