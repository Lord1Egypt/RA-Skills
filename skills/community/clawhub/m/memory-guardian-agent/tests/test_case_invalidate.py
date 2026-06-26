"""Tests for case_invalidate — case invalidation lifecycle."""

import json
import os
import pytest

from case_invalidate import (
    check_invalidations,
    get_review_queue,
    get_status,
    _find_memory,
    _cap_frozen,
)


@pytest.fixture
def meta_path(tmp_path):
    p = str(tmp_path / "meta.json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        json.dump({
            "version": "0.4.2",
            "memories": [],
            "conflicts": [],
            "security_rules": [],
            "entities": {},
            "invalidation_queue": [],
            "frozen_cases": [],
        }, f)
    return p


class TestFindMemory:
    def test_found(self):
        mem = {"id": "mem_1", "content": "test"}
        assert _find_memory({"memories": [mem]}, "mem_1") is mem

    def test_not_found(self):
        assert _find_memory({"memories": []}, "nonexistent") is None


class TestCheckInvalidations:
    def test_empty_queue(self, meta_path):
        result = check_invalidations(meta_path)
        assert isinstance(result, dict)


class TestGetReviewQueue:
    def test_empty(self, meta_path):
        queue = get_review_queue(meta_path)
        assert queue == []


class TestGetStatus:
    def test_empty(self, meta_path):
        result = get_status(meta_path)
        assert isinstance(result, dict)


class TestCapFrozen:
    def test_under_cap(self):
        meta = {
            "memories": [{"id": f"f_{i}", "status": "frozen", "frozen_at": f"2026-01-{i+1:02d}"} for i in range(3)]
        }
        _cap_frozen(meta)
        assert len([m for m in meta["memories"] if m["status"] == "frozen"]) == 3

    def test_over_cap(self):
        meta = {
            "memories": [{"id": f"f_{i}", "status": "frozen", "frozen_at": f"2026-01-{i+1:02d}"} for i in range(100)]
        }
        _cap_frozen(meta)
        frozen_count = len([m for m in meta["memories"] if m["status"] == "frozen"])
        assert frozen_count <= 50
