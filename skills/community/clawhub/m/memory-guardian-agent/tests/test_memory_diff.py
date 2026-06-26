"""Tests for memory_diff — diff between memory snapshots."""

import json
import os
import pytest

from memory_diff import hash_file, rule_diff


class TestHashFile:
    def test_consistent_hash(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("hello world")
        h1 = hash_file(str(f))
        h2 = hash_file(str(f))
        assert h1 == h2

    def test_different_content(self, tmp_path):
        f1 = tmp_path / "a.txt"
        f2 = tmp_path / "b.txt"
        f1.write_text("content A")
        f2.write_text("content B")
        assert hash_file(str(f1)) != hash_file(str(f2))


class TestRuleDiff:
    def test_identical(self):
        result = rule_diff("same content", "same content")
        assert len(result["changes"]) == 0

    def test_different(self):
        result = rule_diff("old content here", "new content here")
        assert isinstance(result, dict)
        assert "changes" in result
        assert "annotations" in result


# ─── New tests for uncovered functions ───────────────────────

from memory_diff import load_snapshot


class TestLoadSnapshot:
    def test_existing_file(self, tmp_path):
        f = tmp_path / "snap.md"
        f.write_text("snapshot content here")
        text = load_snapshot(str(f))
        assert text == "snapshot content here"

    def test_missing_file(self, tmp_path):
        text = load_snapshot(str(tmp_path / "nonexistent.md"))
        assert text is None

    def test_empty_file(self, tmp_path):
        f = tmp_path / "empty.md"
        f.write_text("")
        text = load_snapshot(str(f))
        assert text == ""
