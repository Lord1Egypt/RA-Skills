#!/usr/bin/env python3
"""Tests for the improvement-executor rollback module."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

# repo root for lib.common imports
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
REPO_ROOT = _REPO_ROOT

_rollback_path = REPO_ROOT / "skills" / "improvement-executor" / "scripts" / "rollback.py"
_spec = importlib.util.spec_from_file_location("rollback", _rollback_path)
rollback = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rollback)


# ---------------------------------------------------------------------------
# rollback_from_receipt
# ---------------------------------------------------------------------------


class TestRollbackFromReceipt:
    """Test receipt-based rollback."""

    def _make_receipt(self, tmp_path, *, decision="revert", execution_path=None):
        """Create a minimal receipt JSON."""
        receipt = {
            "decision": decision,
            "run_id": "run-001",
            "candidate_id": "cand-001",
        }
        if execution_path:
            receipt["truth_anchor"] = {"execution_path": str(execution_path)}
        receipt_path = tmp_path / "receipt.json"
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        return receipt_path

    def _make_execution(self, tmp_path, backup_path, target_path, rollback_pointer="ptr-abc"):
        """Create a minimal execution artifact JSON."""
        execution = {
            "result": {
                "rollback_pointer": {
                    "backup_path": str(backup_path),
                    "target_path": str(target_path),
                    "method": "restore_backup_file",
                },
            },
            "truth_anchor": str(tmp_path / "execution.json"),
        }
        exec_path = tmp_path / "execution.json"
        exec_path.write_text(json.dumps(execution), encoding="utf-8")
        return exec_path

    def test_skip_when_decision_is_keep(self, tmp_path):
        receipt_path = self._make_receipt(tmp_path, decision="keep")
        result = rollback.rollback_from_receipt(receipt_path)
        assert result["status"] == "skipped"
        assert "keep" in result["reason"].lower()

    def test_error_when_no_execution_path(self, tmp_path):
        receipt_path = self._make_receipt(tmp_path, decision="revert")
        result = rollback.rollback_from_receipt(receipt_path)
        assert result["status"] == "error"
        assert "execution" in result["reason"].lower() or "Cannot find" in result["reason"]

    def test_error_when_backup_file_missing(self, tmp_path):
        target = tmp_path / "target.md"
        target.write_text("current content", encoding="utf-8")
        backup = tmp_path / "nonexistent_backup.md"
        exec_path = self._make_execution(tmp_path, backup, target)
        receipt_path = self._make_receipt(tmp_path, decision="revert", execution_path=exec_path)

        result = rollback.rollback_from_receipt(receipt_path)
        assert result["status"] == "error"
        assert "not found" in result["reason"].lower()

    def test_successful_rollback(self, tmp_path):
        target = tmp_path / "target.md"
        target.write_text("modified content", encoding="utf-8")
        backup = tmp_path / "backup.md"
        backup.write_text("original content", encoding="utf-8")
        exec_path = self._make_execution(tmp_path, backup, target)
        receipt_path = self._make_receipt(tmp_path, decision="revert", execution_path=exec_path)

        result = rollback.rollback_from_receipt(receipt_path, dry_run=False)
        assert result["status"] == "success"
        assert result["dry_run"] is False
        # Target should be restored
        assert target.read_text(encoding="utf-8") == "original content"

    def test_rollback_pointer_in_result(self, tmp_path):
        target = tmp_path / "target.md"
        target.write_text("v2", encoding="utf-8")
        backup = tmp_path / "backup.md"
        backup.write_text("v1", encoding="utf-8")
        exec_path = self._make_execution(tmp_path, backup, target)
        receipt_path = self._make_receipt(tmp_path, decision="revert", execution_path=exec_path)

        result = rollback.rollback_from_receipt(receipt_path, dry_run=False)
        assert result["rollback_pointer"] is not None
        assert result["rollback_pointer"]["target_path"] == str(target)


# ---------------------------------------------------------------------------
# rollback_from_backup
# ---------------------------------------------------------------------------


class TestRollbackFromBackup:
    """Test direct backup-based rollback."""

    def test_error_when_backup_missing(self, tmp_path):
        result = rollback.rollback_from_backup(
            str(tmp_path / "missing.bak"),
            str(tmp_path / "target.md"),
        )
        assert result["status"] == "error"
        assert "not found" in result["reason"].lower()

    def test_successful_restore(self, tmp_path):
        backup = tmp_path / "backup.md"
        backup.write_text("original", encoding="utf-8")
        target = tmp_path / "target.md"
        target.write_text("changed", encoding="utf-8")

        result = rollback.rollback_from_backup(str(backup), str(target), dry_run=False)
        assert result["status"] == "success"
        assert target.read_text(encoding="utf-8") == "original"
        assert result["restored_from"] == str(backup)

    def test_creates_pre_rollback_backup(self, tmp_path):
        backup = tmp_path / "backup.md"
        backup.write_text("original", encoding="utf-8")
        target = tmp_path / "target.md"
        target.write_text("changed", encoding="utf-8")

        result = rollback.rollback_from_backup(str(backup), str(target), dry_run=False)
        assert "pre_rollback_backup" in result
        pre_rb = Path(result["pre_rollback_backup"])
        assert pre_rb.exists()
        assert pre_rb.read_text(encoding="utf-8") == "changed"


# ---------------------------------------------------------------------------
# Dry-run mode
# ---------------------------------------------------------------------------


class TestDryRun:
    """Dry-run should report success without modifying files."""

    def test_dry_run_does_not_modify_target(self, tmp_path):
        backup = tmp_path / "backup.md"
        backup.write_text("original", encoding="utf-8")
        target = tmp_path / "target.md"
        target.write_text("modified", encoding="utf-8")

        result = rollback.rollback_from_backup(str(backup), str(target), dry_run=True)
        assert result["status"] == "dry_run"
        assert result["dry_run"] is True
        # Target must be unchanged
        assert target.read_text(encoding="utf-8") == "modified"
        # No pre-rollback backup should be created
        assert "pre_rollback_backup" not in result

    def test_dry_run_receipt_does_not_modify_target(self, tmp_path):
        target = tmp_path / "target.md"
        target.write_text("v2", encoding="utf-8")
        backup = tmp_path / "backup.md"
        backup.write_text("v1", encoding="utf-8")

        execution = {
            "result": {
                "rollback_pointer": {
                    "backup_path": str(backup),
                    "target_path": str(target),
                    "method": "restore_backup_file",
                },
            },
            "truth_anchor": str(tmp_path / "exec.json"),
        }
        exec_path = tmp_path / "exec.json"
        exec_path.write_text(json.dumps(execution), encoding="utf-8")

        receipt = {
            "decision": "revert",
            "truth_anchor": {"execution_path": str(exec_path)},
        }
        receipt_path = tmp_path / "receipt.json"
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

        result = rollback.rollback_from_receipt(receipt_path, dry_run=True)
        assert result["status"] == "dry_run"
        assert result["dry_run"] is True
        assert target.read_text(encoding="utf-8") == "v2"
