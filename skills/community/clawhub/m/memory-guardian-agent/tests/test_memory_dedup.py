"""Tests for memory_dedup — memory deduplication."""

import pytest
from memory_dedup import cosine_sim, combined_distance, classify_zone, find_nearest_neighbor


class TestCosineSim:
    def test_identical(self):
        assert cosine_sim({"a": 1, "b": 0}, {"a": 1, "b": 0}) == pytest.approx(1.0)

    def test_orthogonal(self):
        assert cosine_sim({"a": 1}, {"b": 1}) == pytest.approx(0.0)

    def test_partial(self):
        sim = cosine_sim({"a": 1, "b": 1}, {"a": 1, "b": 0})
        assert 0 < sim < 1


class TestClassifyZone:
    def test_near_duplicate(self):
        zone = classify_zone(0.05)
        assert zone == "absorb"  # low distance = near_duplicate mapped to absorb

    def test_possible_duplicate(self):
        zone = classify_zone(0.3)
        assert zone == "derive"

    def test_unique(self):
        zone = classify_zone(0.8)
        assert zone == "suspend"


class TestFindNearestNeighbor:
    def test_finds_nearest(self):
        memories = [
            {"id": "mem_1", "content": "hello world"},
            {"id": "mem_2", "content": "completely different"},
            {"id": "mem_3", "content": "hello world test"},
        ]
        idx, dist = find_nearest_neighbor(0, memories, None)
        assert idx in (0, 2)  # nearest to mem_1
        assert dist >= 0
