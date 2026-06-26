#!/usr/bin/env python3
"""Tests for the evaluate module's core functions."""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add paths for imports
_SKILL_ROOT = Path(__file__).resolve().parents[1]
_REPO_ROOT = _SKILL_ROOT.parents[2]
sys.path.insert(0, str(_SKILL_ROOT / "scripts"))
sys.path.insert(0, str(_REPO_ROOT))

from evaluate import (
    load_task_suite,
    preflight_check,
    compute_results,
    compute_pass_rate,
    extract_candidate_skill,
    _validate_suite_schema,
    BASELINE_ABORT_THRESHOLD,
)


class TestLoadTaskSuite:
    def test_valid_suite(self, tmp_path):
        suite_file = tmp_path / "suite.yaml"
        suite_file.write_text(
            "skill_id: test-skill\n"
            'version: "1.0"\n'
            "tasks:\n"
            "  - id: t1\n"
            "    description: test\n"
            "    prompt: do something\n"
            "    judge:\n"
            "      type: contains\n"
            '      expected: ["hello"]\n'
        )
        suite = load_task_suite(suite_file)
        assert suite["skill_id"] == "test-skill"
        assert len(suite["tasks"]) == 1
        assert suite["tasks"][0]["id"] == "t1"

    def test_missing_skill_id(self, tmp_path):
        suite_file = tmp_path / "suite.yaml"
        suite_file.write_text(
            'version: "1.0"\n'
            "tasks:\n"
            "  - id: t1\n"
            "    prompt: do something\n"
            "    judge:\n"
            "      type: contains\n"
            '      expected: ["hello"]\n'
        )
        with pytest.raises(AssertionError, match="skill_id"):
            load_task_suite(suite_file)

    def test_wrong_version(self, tmp_path):
        suite_file = tmp_path / "suite.yaml"
        suite_file.write_text(
            "skill_id: test\n"
            'version: "2.0"\n'
            "tasks:\n"
            "  - id: t1\n"
            "    prompt: do\n"
            "    judge:\n"
            "      type: contains\n"
            '      expected: ["x"]\n'
        )
        with pytest.raises(AssertionError, match="version"):
            load_task_suite(suite_file)

    def test_duplicate_task_ids(self, tmp_path):
        suite_file = tmp_path / "suite.yaml"
        suite_file.write_text(
            "skill_id: test\n"
            'version: "1.0"\n'
            "tasks:\n"
            "  - id: t1\n"
            "    prompt: do\n"
            "    judge:\n"
            "      type: contains\n"
            '      expected: ["x"]\n'
            "  - id: t1\n"
            "    prompt: do again\n"
            "    judge:\n"
            "      type: contains\n"
            '      expected: ["y"]\n'
        )
        with pytest.raises(AssertionError, match="duplicate"):
            load_task_suite(suite_file)

    def test_empty_tasks(self, tmp_path):
        suite_file = tmp_path / "suite.yaml"
        suite_file.write_text(
            "skill_id: test\n"
            'version: "1.0"\n'
            "tasks: []\n"
        )
        with pytest.raises(AssertionError, match="not be empty"):
            load_task_suite(suite_file)

    def test_unknown_judge_type(self, tmp_path):
        suite_file = tmp_path / "suite.yaml"
        suite_file.write_text(
            "skill_id: test\n"
            'version: "1.0"\n'
            "tasks:\n"
            "  - id: t1\n"
            "    prompt: do\n"
            "    judge:\n"
            "      type: magic\n"
        )
        with pytest.raises(AssertionError, match="unknown judge type"):
            load_task_suite(suite_file)

    def test_contains_missing_expected(self, tmp_path):
        suite_file = tmp_path / "suite.yaml"
        suite_file.write_text(
            "skill_id: test\n"
            'version: "1.0"\n'
            "tasks:\n"
            "  - id: t1\n"
            "    prompt: do\n"
            "    judge:\n"
            "      type: contains\n"
        )
        with pytest.raises(AssertionError, match="expected"):
            load_task_suite(suite_file)

    def test_pytest_non_fixture_path(self, tmp_path):
        suite_file = tmp_path / "suite.yaml"
        suite_file.write_text(
            "skill_id: test\n"
            'version: "1.0"\n'
            "tasks:\n"
            "  - id: t1\n"
            "    prompt: do\n"
            "    judge:\n"
            "      type: pytest\n"
            "      test_file: evil/path.py\n"
        )
        with pytest.raises(AssertionError, match="fixtures/"):
            load_task_suite(suite_file)


class TestPreflightCheck:
    def test_no_claude_without_mock(self, tmp_path):
        suite_file = tmp_path / "suite.yaml"
        suite_file.write_text(
            "skill_id: test\n"
            'version: "1.0"\n'
            "tasks:\n"
            "  - id: t1\n"
            "    prompt: do\n"
            "    judge:\n"
            "      type: contains\n"
            '      expected: ["x"]\n'
        )
        with patch("shutil.which", return_value=None):
            with pytest.raises(AssertionError, match="claude CLI"):
                preflight_check(suite_file, mock=False)

    def test_mock_skips_claude_check(self, tmp_path):
        suite_file = tmp_path / "suite.yaml"
        suite_file.write_text(
            "skill_id: test\n"
            'version: "1.0"\n'
            "tasks:\n"
            "  - id: t1\n"
            "    prompt: do\n"
            "    judge:\n"
            "      type: contains\n"
            '      expected: ["x"]\n'
        )
        # Should not raise even without claude CLI
        preflight_check(suite_file, mock=True)

    def test_missing_suite_file(self, tmp_path):
        with pytest.raises(AssertionError, match="not found"):
            preflight_check(tmp_path / "nonexistent.yaml", mock=True)


class TestComputeResults:
    def test_pass_when_candidate_better(self):
        result = compute_results(0.8, 0.7)
        assert result["verdict"] == "pass"
        assert result["delta"] == 0.1
        assert result["execution_pass_rate"] == 0.8
        assert result["baseline_pass_rate"] == 0.7

    def test_pass_when_equal(self):
        result = compute_results(0.7, 0.7)
        assert result["verdict"] == "pass"
        assert result["delta"] == 0.0

    def test_fail_when_candidate_worse(self):
        result = compute_results(0.5, 0.7)
        assert result["verdict"] == "fail"
        assert result["delta"] == -0.2

    def test_zero_baseline(self):
        result = compute_results(0.5, 0.0)
        assert result["verdict"] == "pass"
        assert result["delta"] == 0.5


class TestComputePassRate:
    def test_all_passed(self):
        results = [{"passed": True}, {"passed": True}, {"passed": True}]
        assert compute_pass_rate(results) == 1.0

    def test_none_passed(self):
        results = [{"passed": False}, {"passed": False}]
        assert compute_pass_rate(results) == 0.0

    def test_mixed(self):
        results = [{"passed": True}, {"passed": False}, {"passed": True}, {"passed": False}]
        assert compute_pass_rate(results) == 0.5

    def test_empty(self):
        assert compute_pass_rate([]) == 0.0


class TestExtractCandidateSkill:
    def test_found(self):
        artifact = {
            "scored_candidates": [
                {"id": "c1", "score": 7.0, "content": "# Skill"},
                {"id": "c2", "score": 5.0, "content": "# Other"},
            ]
        }
        c = extract_candidate_skill(artifact, "c1")
        assert c["id"] == "c1"
        assert c["content"] == "# Skill"

    def test_not_found(self):
        artifact = {"scored_candidates": [{"id": "c1", "score": 7.0}]}
        with pytest.raises(ValueError, match="not found"):
            extract_candidate_skill(artifact, "c99")

    def test_empty_candidates(self):
        artifact = {"scored_candidates": []}
        with pytest.raises(ValueError, match="not found"):
            extract_candidate_skill(artifact, "c1")


class TestBaselineShortCircuit:
    def test_threshold_constant(self):
        """Verify the baseline abort threshold is reasonable."""
        assert BASELINE_ABORT_THRESHOLD == 0.2
        assert 0 < BASELINE_ABORT_THRESHOLD < 1
