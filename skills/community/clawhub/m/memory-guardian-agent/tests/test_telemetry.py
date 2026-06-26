"""Tests for mg_events.telemetry — telemetry storage and reporting."""

import json
import os
import pytest

from mg_events.telemetry import (
    telemetry_path,
    _default_module_stats,
    load_telemetry,
    save_telemetry,
    record_module_run,
    build_report,
    ZERO_INPUT_BREAK_THRESHOLD,
)


@pytest.fixture
def workspace(tmp_path):
    return str(tmp_path)


class TestTelemetryPath:
    def test_returns_expected_path(self, workspace):
        path = telemetry_path(workspace)
        assert path.endswith(".memory-guardian/telemetry.json")
        assert path.startswith(workspace)


class TestDefaultModuleStats:
    def test_structure(self):
        stats = _default_module_stats()
        assert stats["runs"] == 0
        assert stats["hits"] == 0
        assert stats["misses"] == 0
        assert stats["zero_input_streak"] == 0
        assert stats["pipeline_break_candidate"] is False

    def test_returns_new_dict_each_time(self):
        s1 = _default_module_stats()
        s2 = _default_module_stats()
        s1["runs"] = 5
        assert s2["runs"] == 0


class TestLoadTelemetry:
    def test_empty_workspace(self, workspace):
        result = load_telemetry(workspace)
        assert result["schema_version"] == "v0.4.2"
        assert result["modules"] == {}

    def test_existing_file(self, workspace):
        path = telemetry_path(workspace)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = {"schema_version": "v0.4.2", "modules": {"test": {"runs": 3}}}
        with open(path, "w") as f:
            json.dump(data, f)
        result = load_telemetry(workspace)
        assert result["modules"]["test"]["runs"] == 3


class TestSaveTelemetry:
    def test_creates_file(self, workspace):
        state = {"schema_version": "v0.4.2", "modules": {}}
        save_telemetry(workspace, state)
        path = telemetry_path(workspace)
        assert os.path.exists(path)
        with open(path) as f:
            loaded = json.load(f)
        assert loaded["schema_version"] == "v0.4.2"


class TestRecordModuleRun:
    def test_first_hit(self, workspace):
        stats = record_module_run(workspace, "test_mod", input_count=5, output_count=2)
        assert stats["runs"] == 1
        assert stats["hits"] == 1
        assert stats["misses"] == 0
        assert stats["input_total"] == 5
        assert stats["output_total"] == 2
        assert stats["zero_input_streak"] == 0
        assert stats["pipeline_break_candidate"] is False

    def test_miss_increments_streak(self, workspace):
        record_module_run(workspace, "m1", input_count=0, output_count=0)
        stats = record_module_run(workspace, "m1", input_count=0, output_count=0)
        assert stats["misses"] == 2
        assert stats["zero_input_streak"] == 2
        assert stats["max_zero_input_streak"] == 2

    def test_hit_resets_zero_streak(self, workspace):
        record_module_run(workspace, "m2", input_count=0)
        record_module_run(workspace, "m2", input_count=0)
        stats = record_module_run(workspace, "m2", input_count=1)
        assert stats["zero_input_streak"] == 0
        assert stats["max_zero_input_streak"] == 2

    def test_break_candidate_threshold(self, workspace):
        for _ in range(ZERO_INPUT_BREAK_THRESHOLD):
            record_module_run(workspace, "m3", input_count=0)
        stats = record_module_run(workspace, "m3", input_count=0)
        assert stats["pipeline_break_candidate"] is True

    def test_explicit_hit_false(self, workspace):
        stats = record_module_run(workspace, "m4", input_count=5, hit=False)
        assert stats["misses"] == 1
        assert stats["hits"] == 0

    def test_explicit_hit_true(self, workspace):
        stats = record_module_run(workspace, "m5", input_count=0, hit=True)
        assert stats["hits"] == 1
        assert stats["misses"] == 0
        assert stats["zero_input_streak"] == 0

    def test_negative_input_clamped(self, workspace):
        stats = record_module_run(workspace, "m6", input_count=-5, output_count=-3)
        assert stats["input_total"] == 0
        assert stats["output_total"] == 0

    def test_last_run_at_set(self, workspace):
        stats = record_module_run(workspace, "m7", input_count=1)
        assert stats["last_run_at"] is not None


class TestBuildReport:
    def test_empty_workspace(self, workspace):
        report = build_report(workspace)
        assert report["modules"] == {}
        assert report["break_candidates"] == []
        assert "generated_at" in report

    def test_with_data(self, workspace):
        for i in range(ZERO_INPUT_BREAK_THRESHOLD + 1):
            record_module_run(workspace, "breaker", input_count=0)
        record_module_run(workspace, "healthy", input_count=3, output_count=2)
        report = build_report(workspace)
        assert "breaker" in report["break_candidates"]
        assert "healthy" not in report["break_candidates"]
