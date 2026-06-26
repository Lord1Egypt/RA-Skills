"""Tests for migration scripts."""

import json
import os
import pytest

from migrate_to_v042 import step_p0_0, step_p0_1, step_p0_2, step_p0_3
from migrate_v03_to_v04 import migrate_entry
from migrate_bootstrap_to_case import map_memory_to_case, _build_trigger_pattern, _build_context
from migrate_retag import step_fields, step_dirs, step_verify, backup_meta, parse_args


# ─── migrate_to_v042 ─────────────────────────────────────────

class TestMigrateToV042:
    def _make_meta(self):
        return {
            "version": "0.4.1",
            "memories": [
                {"id": "mem_1", "content": "test content", "importance": 0.5,
                 "tags": ["项目"], "status": "active", "created_at": "2026-01-01T00:00:00+08:00"},
            ],
            "conflicts": [],
            "security_rules": [],
            "entities": {},
        }

    def test_p0_0_runs(self):
        meta = self._make_meta()
        step_p0_0(meta, dry_run=False)
        assert "memories" in meta

    def test_p0_1_runs(self):
        meta = self._make_meta()
        step_p0_1(meta, dry_run=False)
        assert "memories" in meta

    def test_p0_2_runs(self):
        meta = self._make_meta()
        step_p0_2(meta, dry_run=False)
        assert "memories" in meta

    def test_p0_3_updates_version(self):
        meta = self._make_meta()
        step_p0_0(meta, dry_run=False)
        step_p0_1(meta, dry_run=False)
        step_p0_2(meta, dry_run=False)
        step_p0_3(meta, dry_run=False)
        assert meta["version"] == "0.4.2"

    def test_dry_run_no_changes(self):
        meta = self._make_meta()
        old_version = meta["version"]
        step_p0_0(meta, dry_run=True)
        assert meta["version"] == old_version


# ─── migrate_v03_to_v04 ──────────────────────────────────────

class TestMigrateV03ToV04:
    def test_migrate_basic_entry(self):
        mem = {
            "id": "mem_1",
            "content": "test",
            "importance": 0.5,
            "created_at": "2026-01-01",
        }
        result = migrate_entry(mem)
        assert "confidence" in result
        assert "reversibility" in result
        assert "cost_factors" in result

    def test_preserves_existing_fields(self):
        mem = {"id": "mem_1", "content": "test", "custom_field": "value"}
        result = migrate_entry(mem)
        assert result.get("custom_field") == "value"


# ─── migrate_bootstrap_to_case ───────────────────────────────

class TestMigrateBootstrapToCase:
    def test_build_trigger_pattern(self):
        memory = {"content": "记住用户偏好设置", "tags": ["偏好"]}
        pattern = _build_trigger_pattern(memory, "用户偏好")
        assert isinstance(pattern, str)

    def test_build_context(self):
        memory = {"content": "记住用户偏好设置"}
        ctx = _build_context(memory, "偏好", "记住用户偏好设置")
        assert isinstance(ctx, str)

    def test_map_memory_to_case(self):
        memory = {
            "id": "mem_1",
            "content": "记住用户偏好设置",
            "tags": ["偏好", "bootstrapped"],
            "importance": 0.9,
            "created_at": "2026-01-01T00:00:00+08:00",
        }
        case = map_memory_to_case(memory, generated_id="case_test123")
        assert case["id"] == "case_test123"
        assert "trigger_pattern" in case


# ─── migrate_retag ───────────────────────────────────────────

class TestMigrateRetag:
    def test_step_fields_adds_memory_id(self):
        meta = {
            "version": "0.4.2",
            "memories": [
                {"id": "mem_1", "content": "test content", "tags": ["项目"],
                 "status": "active", "importance": 0.5},
            ],
        }
        step_fields(meta, dry_run=False)
        mem = meta["memories"][0]
        assert "memory_id" in mem
        assert "file_path" in mem

    def test_backup_meta(self, tmp_path):
        meta_path = str(tmp_path / "meta.json")
        with open(meta_path, "w") as f:
            json.dump({"version": "0.4.2", "memories": []}, f)
        backup = backup_meta(meta_path, dry_run=False)
        assert backup is not None
        assert os.path.exists(backup)

    def test_backup_dry_run(self, tmp_path):
        meta_path = str(tmp_path / "meta.json")
        with open(meta_path, "w") as f:
            json.dump({"version": "0.4.2", "memories": []}, f)
        backup = backup_meta(meta_path, dry_run=True)
        assert backup is True


# ─── New tests for uncovered functions ───────────────────────

class TestStepDirs:
    def test_creates_directories(self, tmp_path):
        workspace = str(tmp_path)
        result = step_dirs(workspace, dry_run=False)
        assert result is True
        import os
        assert os.path.isdir(os.path.join(workspace, "memory/project"))

    def test_dry_run(self, tmp_path):
        workspace = str(tmp_path)
        result = step_dirs(workspace, dry_run=True)
        assert result is True
        # Directories should NOT be created in dry_run
        assert not os.path.isdir(os.path.join(workspace, "memory/project"))


class TestStepVerify:
    def test_passes_after_migration(self, tmp_path):
        meta = {
            "version": "0.4.5",
            "schema_version": "v0.4.5",
            "memories": [{
                "id": "m1",
                "memory_id": "mem_abc12345_0001",
                "content": "test content for migration",
                "tags": ["project"],
                "file_path": "memory/project/mem_abc12345_0001.md",
                "tags_locked": False,
                "classification_confidence": None,
                "classification_context": "migrated from v0.4.4",
                "inbox_reason": None,
                "signal_level": None,
                "reactivation_count": 0,
                "last_reactivated": None,
                "trigger_words": [],
                "needs_review": False,
                "needs_review_since": None,
                "needs_review_timeout": "7d",
                "review_result": None,
                "reviewed_at": None,
                "version": 0,
                "access_signals": [],
            }],
        }
        step_dirs(str(tmp_path), dry_run=False)
        result = step_verify(meta, str(tmp_path), dry_run=False)
        assert result is True

    def test_fails_for_missing_fields(self, tmp_path):
        meta = {
            "version": "0.4.4",
            "memories": [{"id": "m1"}],
        }
        result = step_verify(meta, str(tmp_path), dry_run=True)
        assert result is False


class TestParseArgs:
    def test_default_args(self):
        import sys
        old_argv = sys.argv
        try:
            sys.argv = ["migrate_retag.py", "--workspace", "/tmp/test"]
            args = parse_args()
            assert args.workspace == "/tmp/test"
            assert args.dry_run is False
        finally:
            sys.argv = old_argv

    def test_dry_run_flag(self):
        import sys
        old_argv = sys.argv
        try:
            sys.argv = ["migrate_retag.py", "--workspace", "/tmp/test", "--dry-run"]
            args = parse_args()
            assert args.dry_run is True
        finally:
            sys.argv = old_argv
