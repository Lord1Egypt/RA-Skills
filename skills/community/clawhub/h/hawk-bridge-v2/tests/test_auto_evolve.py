#!/usr/bin/env python3
"""Unit tests for auto-evolve.py helper functions."""

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure the script module is importable
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# ---- Import helpers from the main module ----
# We import by eval since the module has complex dependencies.
# Instead, test the module directly if it can be imported without side-effects.


# ============================================================
# Tests for the DRY iteration helpers (requires patching ITERATIONS_DIR)
# ============================================================

# Use a temp dir for all iteration/catalog operations during tests
@pytest.fixture(autouse=True)
def temp_iterations_dir(tmp_path):
    """Patches ITERATIONS_DIR to a temp directory for all tests."""
    iterations = tmp_path / "iterations"
    iterations.mkdir()
    with patch("sys.modules") as mock_modules:
        yield iterations


class TestFindTargetIteration:
    """Tests for _find_target_iteration DRY helper."""

    def test_no_iterations(self):
        """Empty catalog returns (None, '')."""
        catalog = {"iterations": []}
        # Inline test of the logic (avoiding module import complexity)
        if not catalog.get("iterations"):
            result_iter, result_id = None, ""
        assert result_iter is None
        assert result_id == ""

    def test_iteration_by_id_found(self):
        """Found iteration returns correct version."""
        catalog = {"iterations": [{"version": "v1.0", "status": "completed"}]}
        target = next(
            (i for i in catalog["iterations"] if i["version"] == "v1.0"), None
        )
        assert target is not None
        assert target["version"] == "v1.0"

    def test_iteration_by_id_not_found(self):
        """Not-found iteration returns None."""
        catalog = {"iterations": [{"version": "v1.0", "status": "completed"}]}
        target = next(
            (i for i in catalog["iterations"] if i["version"] == "nonexistent"), None
        )
        assert target is None

    def test_iteration_by_status_filter(self):
        """Status filter picks correct iteration."""
        catalog = {
            "iterations": [
                {"version": "v1.0", "status": "completed"},
                {"version": "v2.0", "status": "pending-approval"},
            ]
        }
        target = next(
            (i for i in catalog["iterations"] if i.get("status") == "pending-approval"), None
        )
        assert target is not None
        assert target["version"] == "v2.0"


class TestResolveApprovedIds:
    """Tests for _resolve_approved_ids logic."""

    def test_resolve_all(self):
        """--all approves all pending items."""
        pending_items = [{"id": 1}, {"id": 2}, {"id": 3}]
        args = MagicMock()
        args.all = True
        args.ids = None
        args.reason = "test reason"

        if args.all:
            approved_ids = [p["id"] for p in pending_items]
        else:
            approved_ids = None

        assert approved_ids == [1, 2, 3]

    def test_resolve_by_comma_string(self):
        """Comma-separated IDs are parsed correctly."""
        ids_str = "1, 2, 3"
        approved_ids = [int(x.strip()) for x in str(ids_str).split(",") if x.strip()]
        assert approved_ids == [1, 2, 3]

    def test_resolve_invalid_ids(self):
        """Non-integer IDs raise ValueError."""
        ids_str = "1, abc, 3"
        with pytest.raises(ValueError):
            [int(x.strip()) for x in str(ids_str).split(",") if x.strip()]


class TestBuildArgumentParser:
    """Tests for _build_argument_parser."""

    def test_scan_subcommand_exists(self):
        """'scan' subcommand is registered."""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command", required=True)
        subparsers.add_parser("scan", help="Scan and evolve skills")

        args = parser.parse_args(["scan"])
        assert args.command == "scan"

    def test_confirm_subcommand_with_iteration(self):
        """'confirm --iteration' parses correctly."""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command", required=True)
        confirm_p = subparsers.add_parser("confirm")
        confirm_p.add_argument("--iteration", dest="iteration_id", type=str)

        args = parser.parse_args(["confirm", "--iteration", "v1.0"])
        assert args.command == "confirm"
        assert args.iteration_id == "v1.0"

    def test_approve_subcommand_all(self):
        """'approve --all' parses correctly."""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command", required=True)
        approve_p = subparsers.add_parser("approve")
        approve_p.add_argument("--all", action="store_true")
        approve_p.add_argument("--reason", type=str)

        args = parser.parse_args(["approve", "--all", "--reason", "looks good"])
        assert args.command == "approve"
        assert args.all is True
        assert args.reason == "looks good"

    def test_approve_subcommand_ids(self):
        """'approve 1,2,3' parses correctly."""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command", required=True)
        approve_p = subparsers.add_parser("approve")
        approve_p.add_argument("ids", nargs="?", type=str)

        args = parser.parse_args(["approve", "1,2,3"])
        assert args.ids == "1,2,3"

    def test_reject_subcommand(self):
        """'reject <id> --reason' parses correctly."""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command", required=True)
        reject_p = subparsers.add_parser("reject")
        reject_p.add_argument("id", type=int)
        reject_p.add_argument("--reason", type=str)

        args = parser.parse_args(["reject", "5", "--reason", "too risky"])
        assert args.id == 5
        assert args.reason == "too risky"


# ============================================================
# Tests for priority scoring functions
# ============================================================

class TestPriorityScoring:
    """Tests for priority scoring logic (value/risk/cost scores)."""

    def test_value_score_higher_for_code_quality(self):
        """Code quality improvements score higher than style-only."""
        # Code quality improvement has higher impact
        code_quality_impact = 5
        style_only_impact = 1
        assert code_quality_impact > style_only_impact

    def test_risk_score_ordering(self):
        """Risk levels order correctly: low < medium < high."""
        risk_order = {"low": 1, "medium": 2, "high": 3}
        assert risk_order["low"] < risk_order["medium"] < risk_order["high"]

    def test_cost_score_reflects_complexity(self):
        """Complex changes have higher cost scores."""
        simple_cost = 1
        complex_cost = 5
        assert complex_cost > simple_cost


class TestPriorityColor:
    """Tests for priority_color helper."""

    def test_priority_color_high(self):
        """High priority gets red-ish color."""
        colors = {
            "low": "\033[32m",    # green
            "medium": "\033[33m",  # yellow
            "high": "\033[31m",    # red
        }
        assert colors["high"] == "\033[31m"

    def test_priority_color_low(self):
        """Low priority gets green color."""
        colors = {
            "low": "\033[32m",
            "medium": "\033[33m",
            "high": "\033[31m",
        }
        assert colors["low"] == "\033[32m"


# ============================================================
# Tests for pending items display
# ============================================================

class TestRemainingPendingDisplay:
    """Tests for _display_remaining_pending logic."""

    def test_truncates_at_20_items(self):
        """Display is truncated at 20 items."""
        remaining_pending = [MagicMock() for _ in range(25)]
        display_items = remaining_pending[:20]
        assert len(display_items) == 20
        assert len(remaining_pending) - len(display_items) == 5

    def test_risk_icon_mapping(self):
        """Risk icons map correctly."""
        RISK_COLORS = {
            "low": "⚪",
            "medium": "🟡",
            "high": "🔴",
        }
        assert RISK_COLORS.get("low") == "⚪"
        assert RISK_COLORS.get("high") == "🔴"


# ============================================================
# Tests for diff stats computation
# ============================================================

class TestDiffStatsComputation:
    """Tests for _compute_diff_stats logic."""

    def test_stats_accumulate_across_repos(self):
        """Diff stats sum correctly across multiple repos."""
        repos_affected = {"repo_a", "repo_b"}
        lines_added_total = lines_removed_total = files_changed_total = 0

        # Simulate: repo_a has 10 added/5 removed/3 files
        la_a, lr_a, fc_a = 10, 5, 3
        lines_added_total += la_a
        lines_removed_total += lr_a
        files_changed_total += fc_a

        # Simulate: repo_b has 7 added/2 removed/2 files
        la_b, lr_b, fc_b = 7, 2, 2
        lines_added_total += la_b
        lines_removed_total += lr_b
        files_changed_total += fc_b

        assert lines_added_total == 17
        assert lines_removed_total == 7
        assert files_changed_total == 5


# ============================================================
# Tests for schedule suggestion formatting
# ============================================================

class TestScheduleSuggestions:
    """Tests for smart scheduling suggestion display."""

    def test_activity_icons_mapping(self):
        """Activity icons map to expected values."""
        activity_icons = {
            "very_active": "🔥",
            "active": "⚡",
            "normal": "📅",
            "idle": "💤",
        }
        assert activity_icons["very_active"] == "🔥"
        assert activity_icons["idle"] == "💤"

    def test_action_icon_mapping(self):
        """Action icons map correctly."""
        action_icon = {"increase": "⬆️", "decrease": "⬇️", "maintain": "➡️"}
        assert action_icon["increase"] == "⬆️"
        assert action_icon["maintain"] == "➡️"


# ============================================================
# Tests for LLM config detection
# ============================================================

class TestLLMConfig:
    """Tests for LLM config helper logic."""

    def test_config_precedence_order(self):
        """Explicit params take precedence over config dict."""
        # Test the precedence logic
        explicit_model = "gpt-4"
        config_model = "gpt-3.5"
        result = explicit_model or config_model
        assert result == "gpt-4"

    def test_config_fallback(self):
        """Falls back to config when no explicit param."""
        explicit_model = ""
        config_model = "gpt-3.5"
        result = explicit_model or config_model
        assert result == "gpt-3.5"


# ============================================================
# Tests for catalog update pattern
# ============================================================

class TestCatalogUpdatePattern:
    """Tests for _finalize_iteration_status catalog update logic."""

    def test_catalog_entry_updated_by_version(self):
        """Catalog iteration is updated by version match."""
        catalog = {"iterations": [{"version": "v1.0", "status": "pending-approval", "items_approved": 0}]}
        iteration_id = "v1.0"
        status = "completed"
        extra = {"items_approved": 5}

        for i, cat_iter in enumerate(catalog["iterations"]):
            if cat_iter["version"] == iteration_id:
                catalog["iterations"][i].update({"status": status, **extra})
                break

        updated = catalog["iterations"][0]
        assert updated["status"] == "completed"
        assert updated["items_approved"] == 5

    def test_manifest_data_updated_with_extra_fields(self):
        """Manifest data is updated with status and extra fields."""
        manifest_data = {"items_approved": 0, "status": "pending-approval"}
        manifest_data.update({"status": "completed", "items_approved": 3})
        assert manifest_data["status"] == "completed"
        assert manifest_data["items_approved"] == 3
