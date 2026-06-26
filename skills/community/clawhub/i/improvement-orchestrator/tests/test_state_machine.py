"""Tests for the orchestrator state machine and common helpers."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# Add repo root to path so we can import lib.*
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from lib.common import (
    slugify,
    utc_now_iso,
    compact_timestamp,
    protected_target,
    classify_feedback,
    infer_source_kind,
    compute_target_profile,
    read_json,
    write_json,
    KEEP_CATEGORIES,
    EXECUTOR_SUPPORTED_CATEGORIES,
)
from lib.state_machine import (
    ensure_tree,
    next_step_for_stage,
    update_state,
    append_pending_promote,
    append_veto,
)


# --- slugify ---


class TestSlugify:
    def test_simple(self):
        assert slugify("Hello World") == "hello-world"

    def test_special_chars(self):
        assert slugify("my_skill/v2.0") == "my-skill-v2-0"

    def test_empty(self):
        assert slugify("") == "item"

    def test_trailing_special(self):
        assert slugify("---test---") == "test"


# --- timestamp helpers ---


class TestTimestamps:
    def test_utc_now_iso_format(self):
        result = utc_now_iso()
        assert result.endswith("Z")
        assert "T" in result

    def test_compact_timestamp_format(self):
        result = compact_timestamp()
        assert result.endswith("Z")
        assert "T" in result
        assert len(result) == 16  # YYYYMMDDTHHMMSSz


# --- state machine transitions ---


class TestStateMachine:
    def test_proposed_goes_to_critic(self):
        step, owner = next_step_for_stage("proposed")
        assert step == "rank_candidates"
        assert owner == "critic"

    def test_ranked_goes_to_evaluator(self):
        step, owner = next_step_for_stage("ranked")
        assert step == "evaluate_candidate"
        assert owner == "evaluator"

    def test_evaluated_goes_to_executor(self):
        step, owner = next_step_for_stage("evaluated")
        assert step == "execute_candidate"
        assert owner == "executor"

    def test_executed_goes_to_gate(self):
        step, owner = next_step_for_stage("executed")
        assert step == "apply_gate"
        assert owner == "gate"

    def test_gated_keep_cycles_back(self):
        step, owner = next_step_for_stage("gated_keep")
        assert step == "propose_candidates"
        assert owner == "proposer"

    def test_gated_pending_needs_human(self):
        step, owner = next_step_for_stage("gated_pending")
        assert owner == "human"

    def test_gated_revert_goes_to_proposer(self):
        step, owner = next_step_for_stage("gated_revert")
        assert owner == "proposer"

    def test_gated_reject_goes_to_proposer(self):
        step, owner = next_step_for_stage("gated_reject")
        assert owner == "proposer"

    def test_unknown_stage_falls_back(self):
        step, owner = next_step_for_stage("nonexistent")
        assert step == "inspect_state"
        assert owner == "human"


# --- ensure_tree ---


class TestEnsureTree:
    def test_creates_directory_structure(self, tmp_path):
        root = tmp_path / "test_state"
        paths = ensure_tree(root)
        assert paths["root"].exists()
        assert paths["candidate_versions"].is_dir()
        assert paths["rankings"].is_dir()
        assert paths["executions"].is_dir()
        assert paths["state"].is_dir()
        assert paths["receipts"].is_dir()

    def test_creates_state_files(self, tmp_path):
        root = tmp_path / "test_state"
        paths = ensure_tree(root)
        state_dir = paths["state"]
        assert (state_dir / "current_state.json").exists()
        assert (state_dir / "pending_promote.json").exists()
        assert (state_dir / "veto.json").exists()
        assert (state_dir / "last_run.json").exists()

    def test_initial_state_is_idle(self, tmp_path):
        root = tmp_path / "test_state"
        paths = ensure_tree(root)
        state = read_json(paths["state"] / "current_state.json")
        assert state["status"] == "idle"
        assert state["stage"] == "idle"
        assert state["next_owner"] == "proposer"

    def test_idempotent(self, tmp_path):
        root = tmp_path / "test_state"
        ensure_tree(root)
        ensure_tree(root)  # should not raise


# --- update_state ---


class TestUpdateState:
    def test_updates_current_and_last_run(self, tmp_path):
        root = tmp_path / "state"
        ensure_tree(root)
        update_state(
            root,
            run_id="run-001",
            stage="proposed",
            status="completed",
            target_path="/some/skill",
            truth_anchor="/some/artifact.json",
        )
        current = read_json(root / "state" / "current_state.json")
        assert current["current_run_id"] == "run-001"
        assert current["stage"] == "proposed"
        assert current["next_owner"] == "critic"

        last_run = read_json(root / "state" / "last_run.json")
        assert last_run["last_run_id"] == "run-001"
        assert last_run["last_stage"] == "proposed"

    def test_full_cycle(self, tmp_path):
        """Simulate a full Proposer→Critic→Executor→Gate cycle."""
        root = tmp_path / "state"
        ensure_tree(root)

        stages = [
            ("proposed", "completed"),
            ("ranked", "completed"),
            ("evaluated", "completed"),
            ("executed", "completed"),
            ("gated_keep", "completed"),
        ]
        expected_owners = ["critic", "evaluator", "executor", "gate", "proposer"]

        for (stage, status), expected_owner in zip(stages, expected_owners):
            update_state(
                root,
                run_id="run-cycle",
                stage=stage,
                status=status,
                target_path="/skill",
                truth_anchor=f"/artifact-{stage}.json",
            )
            current = read_json(root / "state" / "current_state.json")
            assert current["next_owner"] == expected_owner, f"After {stage}"


# --- pending_promote / veto ---


class TestPendingAndVeto:
    def test_append_pending_promote(self, tmp_path):
        root = tmp_path / "state"
        ensure_tree(root)
        append_pending_promote(root, {"id": "c1", "reason": "hold"})
        append_pending_promote(root, {"id": "c2", "reason": "hold"})
        data = read_json(root / "state" / "pending_promote.json")
        assert len(data["pending"]) == 2
        assert data["last_updated"] is not None

    def test_append_veto(self, tmp_path):
        root = tmp_path / "state"
        ensure_tree(root)
        append_veto(root, {"id": "c3", "reason": "high risk"})
        data = read_json(root / "state" / "veto.json")
        assert len(data["vetoes"]) == 1


# --- protected_target ---


class TestProtectedTarget:
    def test_trading_is_protected(self):
        assert protected_target("/skills/trading-bot") is True

    def test_gateway_is_protected(self):
        assert protected_target("/infra/gateway-config") is True

    def test_normal_skill_not_protected(self):
        assert protected_target("/skills/summarize") is False


# --- classify_feedback ---


class TestClassifyFeedback:
    def test_basic_classification(self):
        entries = [
            {"snippet": "This test case fails on edge cases"},
            {"snippet": "The workflow step is unclear"},
            {"snippet": "Add a usage example for beginners"},
        ]
        result = classify_feedback(entries)
        assert len(result["tests"]) >= 1
        assert len(result["workflow"]) >= 1
        assert len(result["examples"]) >= 1


# --- infer_source_kind ---


class TestInferSourceKind:
    def test_feedback(self):
        assert infer_source_kind(Path(".feedback/note.md")) == "feedback"

    def test_learnings(self):
        assert infer_source_kind(Path("learnings/2024.md")) == "learnings"

    def test_memory(self):
        assert infer_source_kind(Path("memory/state.json")) == "memory"

    def test_generic(self):
        assert infer_source_kind(Path("README.md")) == "source"


# --- compute_target_profile ---


class TestComputeTargetProfile:
    def test_directory_profile(self, tmp_path):
        (tmp_path / "README.md").write_text("# Test")
        (tmp_path / "references").mkdir()
        profile = compute_target_profile(tmp_path)
        assert profile["exists"] is True
        assert profile["kind"] == "directory"
        assert profile["has_references"] is True
        assert len(profile["markdown_files"]) >= 1

    def test_missing_path(self, tmp_path):
        profile = compute_target_profile(tmp_path / "nonexistent")
        assert profile["exists"] is False
        assert profile["kind"] == "missing"


# --- constants consistency ---


class TestConstants:
    def test_keep_is_subset_of_executor_supported(self):
        assert KEEP_CATEGORIES.issubset(EXECUTOR_SUPPORTED_CATEGORIES)
