"""Tests for memory_violations — violation rule tracking."""

import json
import os
import pytest
from datetime import datetime

from memory_violations import (
    guard_dir,
    events_path,
    health_path,
    context_hash,
    load_events,
    load_health,
    save_health,
    cmd_log,
)


@pytest.fixture
def workspace(tmp_path):
    return str(tmp_path)


class TestGuardDir:
    def test_returns_path(self, workspace):
        d = guard_dir(workspace)
        assert ".memory-guardian" in d

    def test_creates_dir(self, workspace):
        d = guard_dir(workspace)
        os.makedirs(d, exist_ok=True)
        assert os.path.exists(d)


class TestEventsPath:
    def test_returns_path(self, workspace):
        p = events_path(workspace)
        assert "events.json" in p


class TestContextHash:
    def test_consistent(self):
        assert context_hash("test content") == context_hash("test content")

    def test_different_content(self):
        assert context_hash("content A") != context_hash("content B")


class TestLoadEvents:
    def test_empty(self, workspace):
        events = load_events(workspace)
        assert events == []

    def test_with_data(self, workspace):
        p = events_path(workspace)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        data = [{"rule_id": "r1", "event": "test", "at": datetime.now().isoformat()}]
        with open(p, "w") as f:
            json.dump(data, f)
        events = load_events(workspace)
        assert len(events) == 1


class TestSaveHealth:
    def test_saves(self, workspace):
        health = {"rule_1": {"score": 0.8}}
        save_health(workspace, health)
        p = health_path(workspace)
        assert os.path.exists(p)


class TestCmdLog:
    def test_log_event(self, workspace):
        result = cmd_log("test_rule", "test_event", "test context", "warning", workspace)
        events = load_events(workspace)
        assert len(events) >= 1


# ─── New tests for uncovered functions ───────────────────────

from memory_violations import load_health as _load_health_fn


class TestLoadHealth:
    def test_default_when_missing(self, workspace):
        health = load_health(workspace)
        assert isinstance(health, dict)
        assert "rules" in health
        assert health["last_updated"] is None

    def test_loads_existing(self, workspace):
        # save_health was already called in TestSaveHealth above,
        # but let's test independently
        import json
        hp = health_path(workspace)
        os.makedirs(os.path.dirname(hp), exist_ok=True)
        data = {"rules": {"r1": {"total_violations": 5}}, "last_updated": "2026-01-01"}
        with open(hp, "w") as f:
            json.dump(data, f)
        health = load_health(workspace)
        assert health["rules"]["r1"]["total_violations"] == 5
