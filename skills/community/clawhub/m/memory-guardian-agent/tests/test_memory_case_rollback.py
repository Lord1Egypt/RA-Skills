"""Tests for memory_case_rollback — case versioning and rollback."""

import json
import os
import pytest
from datetime import datetime, timedelta

from memory_case_rollback import (
    _days_since,
    _find_case,
    _find_all_versions,
    create_version_entry,
    compute_failure_signals,
)


class TestDaysSince:
    def test_recent(self):
        from mg_utils import CST
        ts = (datetime.now(CST) - timedelta(hours=1)).isoformat()
        days = _days_since(ts)
        assert days < 1

    def test_old(self):
        from mg_utils import CST
        ts = (datetime.now(CST) - timedelta(days=10)).isoformat()
        days = _days_since(ts)
        assert 9 <= days <= 11

    def test_none(self):
        assert _days_since(None) == float('inf')

    def test_naive_raises(self):
        # Naive datetime without timezone → inf
        ts = "2026-04-06T12:00:00"
        assert _days_since(ts) == float('inf')


class TestFindCase:
    def test_found(self):
        case = {"id": "case_1", "situation": "test"}
        meta = {"memories": [case]}
        assert _find_case(meta, "case_1") is case

    def test_not_found(self):
        assert _find_case({"memories": []}, "nonexistent") is None


class TestFindAllVersions:
    def test_finds_versions(self):
        case = {"id": "case_1", "situation": "original"}
        v1 = {"id": "case_1_v1", "case_id": "case_1", "version": 1}
        meta = {"memories": [case, v1]}
        versions = _find_all_versions(meta, "case_1")
        assert len(versions) >= 1


class TestComputeFailureSignals:
    def test_returns_dict(self):
        mem = {"id": "case_1", "failure_conditions": []}
        signals = compute_failure_signals({"memories": [mem]}, "case_1")
        assert isinstance(signals, dict)
        assert "failure_rate" in signals

    def test_with_failures(self):
        mem = {"id": "case_1", "failure_conditions": [{"intent": "test", "count": 3}]}
        signals = compute_failure_signals({"memories": [mem]}, "case_1")
        assert isinstance(signals, dict)


# ─── New tests for uncovered functions ───────────────────────

from memory_case_rollback import (
    rollback_case,
    sweep_deprecated,
)


class TestRollbackCase:
    def test_rollback_success(self):
        v1 = {"id": "case_v1", "version": 1, "deprecated": True,
               "version_group": "grp_1", "status": "archived"}
        v2 = {"id": "case_v2", "version": 2, "deprecated": False,
               "prev_version": "case_v1", "version_group": "grp_1", "status": "active"}
        meta = {"memories": [v1, v2]}
        success, msg, chain = rollback_case(meta, "case_v2", reason="test reason")
        assert success is True
        assert v2["deprecated"] is True
        assert v1["deprecated"] is False
        assert len(chain) == 2

    def test_rollback_no_prev_version(self):
        v1 = {"id": "case_v1", "version": 1, "deprecated": False, "status": "active"}
        meta = {"memories": [v1]}
        success, msg, chain = rollback_case(meta, "case_v1")
        assert success is False
        assert "No previous version" in msg

    def test_rollback_not_found(self):
        meta = {"memories": []}
        success, msg, chain = rollback_case(meta, "nonexistent")
        assert success is False
        assert "not found" in msg

    def test_rollback_records_version_log(self):
        v1 = {"id": "case_v1", "version": 1, "deprecated": True,
               "version_group": "grp_1"}
        v2 = {"id": "case_v2", "version": 2, "deprecated": False,
               "prev_version": "case_v1", "version_group": "grp_1"}
        meta = {"memories": [v1, v2]}
        rollback_case(meta, "case_v2", reason="revert")
        assert "version_log" in v1
        assert v1["version_log"][0]["action"] == "rollback"


class TestSweepDeprecated:
    def test_sweeps_old_deprecated(self, tmp_path):
        import json
        from datetime import datetime, timedelta
        from mg_utils import CST
        old_ts = (datetime.now(CST) - timedelta(days=35)).isoformat()
        meta = {
            "memories": [{
                "id": "case_1", "deprecated": True,
                "deprecated_at": old_ts, "version": 1,
            }]
        }
        p = str(tmp_path / "meta.json")
        with open(p, "w") as f:
            json.dump(meta, f)
        archived = sweep_deprecated(meta, dry_run=False, meta_path=p)
        assert len(archived) == 1
        assert meta["memories"][0]["status"] == "archived"

    def test_keeps_recent_deprecated(self, tmp_path):
        import json
        from datetime import datetime, timedelta
        from mg_utils import CST
        recent_ts = (datetime.now(CST) - timedelta(days=5)).isoformat()
        meta = {
            "memories": [{
                "id": "case_1", "deprecated": True,
                "deprecated_at": recent_ts, "version": 1,
            }]
        }
        p = str(tmp_path / "meta.json")
        with open(p, "w") as f:
            json.dump(meta, f)
        archived = sweep_deprecated(meta, dry_run=False, meta_path=p)
        assert len(archived) == 0

    def test_dry_run_no_write(self, tmp_path):
        import json
        from datetime import datetime, timedelta
        from mg_utils import CST
        old_ts = (datetime.now(CST) - timedelta(days=100)).isoformat()
        meta = {
            "memories": [{
                "id": "case_1", "deprecated": True,
                "deprecated_at": old_ts, "version": 2,
            }]
        }
        p = str(tmp_path / "meta.json")
        with open(p, "w") as f:
            json.dump(meta, f)
        archived = sweep_deprecated(meta, dry_run=True)
        assert len(archived) == 1
        # Status should NOT be changed in dry_run
        assert meta["memories"][0].get("status") != "archived"

    def test_no_deprecated_cases(self):
        meta = {"memories": [{"id": "case_1", "deprecated": False}]}
        archived = sweep_deprecated(meta, dry_run=False)
        assert len(archived) == 0
