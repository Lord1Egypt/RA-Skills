#!/usr/bin/env python3
"""Tests for the improvement-executor execute module."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

# repo root for lib.common imports
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
REPO_ROOT = _REPO_ROOT

_execute_path = REPO_ROOT / "skills" / "improvement-executor" / "scripts" / "execute.py"
_spec = importlib.util.spec_from_file_location("execute", _execute_path)
execute = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(execute)


# ---------------------------------------------------------------------------
# capture_execution_trace
# ---------------------------------------------------------------------------


class TestCaptureExecutionTrace:
    def test_basic_structure(self):
        candidate = {
            "id": "cand-01-readme",
            "category": "docs",
            "target_path": "/tmp/skill/README.md",
            "execution_plan": {"action": "append_markdown_section"},
        }
        result = {
            "status": "success",
            "modified": True,
            "diff_summary": {"reason": "appended section", "added_lines": 4},
        }
        trace = execute.capture_execution_trace(candidate, result)

        assert trace["type"] == "execution_trace"
        assert trace["candidate_id"] == "cand-01-readme"
        assert trace["category"] == "docs"
        assert trace["target_path"] == "/tmp/skill/README.md"
        assert trace["action"] == "append_markdown_section"
        assert trace["execution_status"] == "success"
        assert trace["modified"] is True
        assert trace["diff_summary"]["added_lines"] == 4
        assert trace["error"] is None
        assert "timestamp" in trace

    def test_with_error(self):
        candidate = {"id": "cand-02-ref", "category": "reference"}
        result = {"status": "failed", "modified": False}
        trace = execute.capture_execution_trace(
            candidate, result, error="file not found"
        )
        assert trace["error"] == "file not found"
        assert trace["execution_status"] == "failed"

    def test_missing_fields_default_gracefully(self):
        trace = execute.capture_execution_trace({}, {})
        assert trace["candidate_id"] == "unknown"
        assert trace["category"] == "unknown"
        assert trace["action"] == "unknown"
        assert trace["execution_status"] == "unknown"
        assert trace["modified"] is False


# ---------------------------------------------------------------------------
# append_markdown_section
# ---------------------------------------------------------------------------


class TestAppendMarkdownSection:
    def test_appends_new_section(self, tmp_path):
        md_file = tmp_path / "README.md"
        md_file.write_text("# My Skill\n\nSome content.\n", encoding="utf-8")

        plan = {
            "section_heading": "## Operator Notes",
            "content_lines": [
                "This skill is advisory.",
                "Pair with external tooling.",
            ],
        }
        result = execute.append_markdown_section(md_file, plan)

        assert result["status"] == "success"
        assert result["modified"] is True
        assert result["diff_summary"]["added_lines"] == 4  # heading + blank + 2 lines
        after = md_file.read_text(encoding="utf-8")
        assert "## Operator Notes" in after
        assert "- This skill is advisory." in after
        assert "- Pair with external tooling." in after

    def test_no_change_when_section_exists(self, tmp_path):
        md_file = tmp_path / "README.md"
        md_file.write_text(
            "# My Skill\n\n## Operator Notes\n\n- Already here.\n",
            encoding="utf-8",
        )

        plan = {
            "section_heading": "## Operator Notes",
            "content_lines": ["New line."],
        }
        result = execute.append_markdown_section(md_file, plan)

        assert result["status"] == "no_change"
        assert result["modified"] is False
        assert result["diff_summary"]["added_lines"] == 0

    def test_diff_is_valid_unified_diff(self, tmp_path):
        md_file = tmp_path / "test.md"
        md_file.write_text("# Title\n", encoding="utf-8")

        plan = {
            "section_heading": "## New Section",
            "content_lines": ["Line one."],
        }
        result = execute.append_markdown_section(md_file, plan)

        assert result["diff"].startswith("---")
        assert "@@" in result["diff"]
        assert "+## New Section" in result["diff"]


# ---------------------------------------------------------------------------
# replace_markdown_section
# ---------------------------------------------------------------------------


class TestReplaceMarkdownSection:
    def test_replaces_existing_section(self, tmp_path):
        md_file = tmp_path / "README.md"
        md_file.write_text(
            "# Title\n\n## Notes\n\n- Old note 1.\n- Old note 2.\n\n## Footer\n\nEnd.\n",
            encoding="utf-8",
        )
        plan = {
            "section_heading": "## Notes",
            "content_lines": ["New note A.", "New note B.", "New note C."],
        }
        result = execute.replace_markdown_section(md_file, plan)

        assert result["status"] == "success"
        assert result["modified"] is True
        assert result["diff_summary"]["reason"] == "replaced_section"
        assert result["diff_summary"]["changed_lines"] == 3

        after = md_file.read_text(encoding="utf-8")
        assert "- New note A." in after
        assert "Old note 1" not in after
        assert "## Footer" in after

    def test_section_not_found(self, tmp_path):
        md_file = tmp_path / "README.md"
        md_file.write_text("# Title\n\nSome content.\n", encoding="utf-8")
        plan = {"section_heading": "## Nonexistent", "content_lines": ["X"]}
        result = execute.replace_markdown_section(md_file, plan)

        assert result["status"] == "no_change"
        assert "not found" in result["diff_summary"]["reason"]

    def test_replaces_last_section(self, tmp_path):
        md_file = tmp_path / "README.md"
        md_file.write_text(
            "# Title\n\n## Last Section\n\n- Old line.\n",
            encoding="utf-8",
        )
        plan = {"section_heading": "## Last Section", "content_lines": ["Replaced."]}
        result = execute.replace_markdown_section(md_file, plan)

        assert result["status"] == "success"
        assert "- Replaced." in md_file.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# insert_before_section
# ---------------------------------------------------------------------------


class TestInsertBeforeSection:
    def test_inserts_before_heading(self, tmp_path):
        md_file = tmp_path / "README.md"
        md_file.write_text(
            "# Title\n\n## Section A\n\nContent A.\n",
            encoding="utf-8",
        )
        plan = {
            "section_heading": "## Section A",
            "content_lines": ["Inserted line 1.", "Inserted line 2."],
        }
        result = execute.insert_before_section(md_file, plan)

        assert result["status"] == "success"
        after = md_file.read_text(encoding="utf-8")
        assert after.index("Inserted line 1") < after.index("## Section A")

    def test_section_not_found(self, tmp_path):
        md_file = tmp_path / "README.md"
        md_file.write_text("# Title\n", encoding="utf-8")
        plan = {"section_heading": "## Missing", "content_lines": ["X"]}
        result = execute.insert_before_section(md_file, plan)

        assert result["status"] == "no_change"


# ---------------------------------------------------------------------------
# update_yaml_frontmatter
# ---------------------------------------------------------------------------


class TestUpdateYamlFrontmatter:
    def test_updates_existing_frontmatter(self, tmp_path):
        md_file = tmp_path / "SKILL.md"
        md_file.write_text(
            "---\ntitle: My Skill\nversion: 1\n---\n\n# Body\n",
            encoding="utf-8",
        )
        plan = {"frontmatter_updates": {"version": 2, "author": "auto"}}
        result = execute.update_yaml_frontmatter(md_file, plan)

        assert result["status"] == "success"
        after = md_file.read_text(encoding="utf-8")
        assert "version: 2" in after
        assert "author: auto" in after
        assert "# Body" in after

    def test_no_frontmatter(self, tmp_path):
        md_file = tmp_path / "SKILL.md"
        md_file.write_text("# No Frontmatter\n\nJust body.\n", encoding="utf-8")
        plan = {"frontmatter_updates": {"title": "test"}}
        result = execute.update_yaml_frontmatter(md_file, plan)

        assert result["status"] == "no_change"
        assert "no frontmatter" in result["diff_summary"]["reason"]

    def test_malformed_frontmatter(self, tmp_path):
        md_file = tmp_path / "SKILL.md"
        md_file.write_text("---\ntitle: broken", encoding="utf-8")
        plan = {"frontmatter_updates": {"title": "fixed"}}
        result = execute.update_yaml_frontmatter(md_file, plan)

        assert result["status"] == "no_change"


# ---------------------------------------------------------------------------
# ACTION_HANDLERS dispatch
# ---------------------------------------------------------------------------


class TestActionDispatch:
    def test_all_actions_registered(self):
        for name in [
            "append_markdown_section",
            "replace_markdown_section",
            "insert_before_section",
            "update_yaml_frontmatter",
        ]:
            assert name in execute.ACTION_HANDLERS

    def test_handlers_are_callable(self):
        for name, handler in execute.ACTION_HANDLERS.items():
            assert callable(handler), f"{name} handler is not callable"

    def test_unknown_action_not_in_table(self):
        assert execute.ACTION_HANDLERS.get("delete_file") is None

