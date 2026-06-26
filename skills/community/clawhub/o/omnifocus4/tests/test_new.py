"""
Tests for new and expanded commands not present in the original SKILL.md.

Covers: summary, project-tree, project-search, folder, root,
        tag-summary, tag-family, available, review,
        and the new fields added to existing task/project records.
"""

import json
import pytest
from unittest.mock import patch

from omnifocus import dispatch
from conftest import (
    make_osascript_result,
    TASK_1,
    TASK_2,
    TASK_3,
    PROJECT_WORK,
    PROJECT_ERRANDS,
    PROJECT_HABITS,
    FOLDER_PROFESSIONAL,
    FOLDER_PERSONAL,
    TAG_FOCUS,
    TAG_REVIEW,
)


# ---------------------------------------------------------------------------
# Helpers (duplicated locally for readability)
# ---------------------------------------------------------------------------

def run_cmd(argv, mock_result, capsys):
    with patch("subprocess.run", return_value=mock_result):
        dispatch(argv)
    return json.loads(capsys.readouterr().out)


def run_cmd_expect_error(argv, mock_result, capsys):
    with patch("subprocess.run", return_value=mock_result):
        with pytest.raises(SystemExit) as exc_info:
            dispatch(argv)
    assert exc_info.value.code == 1
    return json.loads(capsys.readouterr().out)


# ---------------------------------------------------------------------------
# summary
# ---------------------------------------------------------------------------

class TestSummary:
    SUMMARY_DATA = {
        "projects": 3,
        "tasks": 15,
        "flagged": 2,
        "due": 4,
        "available": 10,
        "completed": 5,
        "inbox": 1,
    }

    def test_returns_counts(self, capsys):
        result = run_cmd(["summary"], make_osascript_result(self.SUMMARY_DATA), capsys)
        for key in ("projects", "tasks", "flagged", "due", "available", "completed", "inbox"):
            assert key in result, f"Missing key: {key}"

    def test_values_are_integers(self, capsys):
        result = run_cmd(["summary"], make_osascript_result(self.SUMMARY_DATA), capsys)
        assert result["projects"] == 3
        assert result["tasks"] == 15
        assert result["inbox"] == 1


# ---------------------------------------------------------------------------
# project-tree
# ---------------------------------------------------------------------------

class TestProjectTree:
    TREE_DATA = {
        "found": True,
        "project": PROJECT_WORK,
        "count": 3,
        "items": [
            {"type": "task", "depth": 0, **TASK_1},
            {"type": "task", "depth": 1, **TASK_2},
            {"type": "task", "depth": 0, **TASK_3},
        ],
    }

    def test_found(self, capsys):
        result = run_cmd(["project-tree", "Work"], make_osascript_result(self.TREE_DATA), capsys)
        assert result["found"] is True
        assert result["project"]["name"] == "Work"

    def test_items_have_depth(self, capsys):
        result = run_cmd(["project-tree", "Work"], make_osascript_result(self.TREE_DATA), capsys)
        assert "items" in result
        for item in result["items"]:
            assert "depth" in item
            assert "type" in item
            assert item["type"] == "task"

    def test_not_found(self, capsys):
        result = run_cmd_expect_error(
            ["project-tree", "NoProject"],
            make_osascript_result({"found": False, "name": "NoProject"}),
            capsys,
        )
        assert "error" in result

    def test_missing_name_arg(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["project-tree"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)

    def test_custom_limit(self, capsys):
        """Passes limit arg without error."""
        run_cmd(
            ["project-tree", "Work", "10"],
            make_osascript_result({**self.TREE_DATA, "count": 1, "items": [self.TREE_DATA["items"][0]]}),
            capsys,
        )


# ---------------------------------------------------------------------------
# project-search
# ---------------------------------------------------------------------------

class TestProjectSearch:
    SEARCH_DATA = {
        "count": 2,
        "items": [PROJECT_WORK, PROJECT_HABITS],
    }

    def test_returns_count_and_items(self, capsys):
        result = run_cmd(
            ["project-search", "work"],
            make_osascript_result(self.SEARCH_DATA),
            capsys,
        )
        assert "count" in result
        assert "items" in result
        assert result["count"] == 2

    def test_empty_results(self, capsys):
        result = run_cmd(
            ["project-search", "xyzzy"],
            make_osascript_result({"count": 0, "items": []}),
            capsys,
        )
        assert result["count"] == 0
        assert result["items"] == []

    def test_missing_term_arg(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["project-search"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


# ---------------------------------------------------------------------------
# folder (detail)
# ---------------------------------------------------------------------------

class TestFolderDetail:
    FOLDER_DATA = {
        "found": True,
        "folder": {"id": FOLDER_PERSONAL["id"], "name": "Personal"},
        "folderCount": 0,
        "projectCount": 2,
        "count": 2,
        "items": [
            {"type": "project", **PROJECT_ERRANDS},
            {"type": "project", **PROJECT_HABITS},
        ],
    }

    def test_found(self, capsys):
        result = run_cmd(
            ["folder", "Personal"],
            make_osascript_result(self.FOLDER_DATA),
            capsys,
        )
        assert result["found"] is True
        assert result["folder"]["name"] == "Personal"

    def test_items_have_type(self, capsys):
        result = run_cmd(
            ["folder", "Personal"],
            make_osascript_result(self.FOLDER_DATA),
            capsys,
        )
        for item in result["items"]:
            assert "type" in item

    def test_counts(self, capsys):
        result = run_cmd(
            ["folder", "Personal"],
            make_osascript_result(self.FOLDER_DATA),
            capsys,
        )
        assert result["projectCount"] == 2
        assert result["folderCount"] == 0

    def test_not_found(self, capsys):
        result = run_cmd_expect_error(
            ["folder", "NoFolder"],
            make_osascript_result({"found": False, "name": "NoFolder"}),
            capsys,
        )
        assert "error" in result

    def test_missing_name_arg(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["folder"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


# ---------------------------------------------------------------------------
# root
# ---------------------------------------------------------------------------

class TestRoot:
    ROOT_DATA = {
        "count": 3,
        "items": [
            {"type": "folder", **FOLDER_PROFESSIONAL},
            {"type": "folder", **FOLDER_PERSONAL},
            {"type": "project", **PROJECT_WORK},  # hypothetical unfiled project
        ],
    }

    def test_returns_count_and_items(self, capsys):
        result = run_cmd(["root"], make_osascript_result(self.ROOT_DATA), capsys)
        assert "count" in result
        assert "items" in result

    def test_items_have_type(self, capsys):
        result = run_cmd(["root"], make_osascript_result(self.ROOT_DATA), capsys)
        for item in result["items"]:
            assert "type" in item
            assert item["type"] in ("folder", "project")

    def test_custom_limit(self, capsys):
        run_cmd(
            ["root", "10"],
            make_osascript_result({"count": 1, "items": [self.ROOT_DATA["items"][0]]}),
            capsys,
        )


# ---------------------------------------------------------------------------
# tag-summary
# ---------------------------------------------------------------------------

class TestTagSummary:
    SUMMARY_DATA = {
        "found": True,
        "tag": {"id": TAG_REVIEW["id"], "name": "review"},
        "total": 1,
        "byFolder": {"Personal": 1},
        "byProject": {"Personal :: Habits": 1},
        "items": [TASK_3],
    }

    def test_found(self, capsys):
        result = run_cmd(
            ["tag-summary", "review"],
            make_osascript_result(self.SUMMARY_DATA),
            capsys,
        )
        assert result["found"] is True
        assert result["tag"]["name"] == "review"

    def test_has_aggregates(self, capsys):
        result = run_cmd(
            ["tag-summary", "review"],
            make_osascript_result(self.SUMMARY_DATA),
            capsys,
        )
        assert "byFolder" in result
        assert "byProject" in result
        assert "total" in result
        assert "items" in result

    def test_not_found(self, capsys):
        result = run_cmd_expect_error(
            ["tag-summary", "nosuchTag"],
            make_osascript_result({"found": False, "name": "nosuchTag"}),
            capsys,
        )
        assert "error" in result

    def test_missing_name_arg(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["tag-summary"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


# ---------------------------------------------------------------------------
# tag-family
# ---------------------------------------------------------------------------

class TestTagFamily:
    FAMILY_DATA = {
        "found": True,
        "family": "review",
        "matchingTags": ["review", "weekly-review", "monthly-review"],
        "byTag": {"review": 3, "weekly-review": 2, "monthly-review": 1},
        "availableByTag": {"review": 3, "weekly-review": 2, "monthly-review": 1},
        "totalTasks": 4,
        "items": [TASK_1, TASK_2, TASK_3],
    }

    def test_found(self, capsys):
        result = run_cmd(
            ["tag-family", "review"],
            make_osascript_result(self.FAMILY_DATA),
            capsys,
        )
        assert result["found"] is True
        assert result["family"] == "review"

    def test_has_tag_breakdown(self, capsys):
        result = run_cmd(
            ["tag-family", "review"],
            make_osascript_result(self.FAMILY_DATA),
            capsys,
        )
        assert "matchingTags" in result
        assert "byTag" in result
        assert "availableByTag" in result
        assert "totalTasks" in result
        assert "items" in result

    def test_matching_tags_list(self, capsys):
        result = run_cmd(
            ["tag-family", "review"],
            make_osascript_result(self.FAMILY_DATA),
            capsys,
        )
        assert isinstance(result["matchingTags"], list)
        assert "review" in result["matchingTags"]

    def test_not_found(self, capsys):
        result = run_cmd_expect_error(
            ["tag-family", "nosuchTag"],
            make_osascript_result({"found": False, "name": "nosuchTag"}),
            capsys,
        )
        assert "error" in result

    def test_missing_name_arg(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["tag-family"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


# ---------------------------------------------------------------------------
# available
# ---------------------------------------------------------------------------

class TestAvailable:
    AVAILABLE_DATA = {
        "count": 2,
        "items": [TASK_1, TASK_2],
    }

    def test_returns_count_and_items(self, capsys):
        result = run_cmd(
            ["available"],
            make_osascript_result(self.AVAILABLE_DATA),
            capsys,
        )
        assert "count" in result
        assert "items" in result
        assert result["count"] == 2

    def test_all_items_have_available_field(self, capsys):
        result = run_cmd(
            ["available"],
            make_osascript_result(self.AVAILABLE_DATA),
            capsys,
        )
        for item in result["items"]:
            assert "available" in item

    def test_custom_limit(self, capsys):
        run_cmd(
            ["available", "1"],
            make_osascript_result({"count": 1, "items": [TASK_1]}),
            capsys,
        )

    def test_empty(self, capsys):
        result = run_cmd(
            ["available"],
            make_osascript_result({"count": 0, "items": []}),
            capsys,
        )
        assert result["count"] == 0


# ---------------------------------------------------------------------------
# review
# ---------------------------------------------------------------------------

class TestReview:
    REVIEW_DATA = {
        "count": 3,
        "items": [PROJECT_WORK, PROJECT_ERRANDS, PROJECT_HABITS],
    }

    def test_returns_count_and_items(self, capsys):
        result = run_cmd(
            ["review"],
            make_osascript_result(self.REVIEW_DATA),
            capsys,
        )
        assert "count" in result
        assert "items" in result
        assert result["count"] == 3

    def test_projects_have_task_counts(self, capsys):
        result = run_cmd(
            ["review"],
            make_osascript_result(self.REVIEW_DATA),
            capsys,
        )
        for p in result["items"]:
            assert "taskCount" in p
            assert "availableTaskCount" in p

    def test_projects_have_status(self, capsys):
        result = run_cmd(
            ["review"],
            make_osascript_result(self.REVIEW_DATA),
            capsys,
        )
        for p in result["items"]:
            assert "status" in p

    def test_custom_limit(self, capsys):
        run_cmd(
            ["review", "1"],
            make_osascript_result({"count": 1, "items": [PROJECT_WORK]}),
            capsys,
        )


# ---------------------------------------------------------------------------
# New task record fields (verified across multiple commands)
# ---------------------------------------------------------------------------

class TestNewTaskFields:
    """
    Verify that new fields exist on task records returned by all
    commands that produce task lists.
    """
    NEW_FIELDS = ("available", "effectiveDueDate", "completionDate",
                  "estimatedMinutes", "folder")

    @pytest.mark.parametrize("cmd,extra_args,fixture", [
        (["inbox"],         [],          [TASK_1]),
        (["today"],         [],          [TASK_1]),
        (["flagged"],       [],          [TASK_1]),
        (["search", "q"],   [],          [TASK_1]),
        (["tasks", "Work"], [],          [TASK_1]),
    ])
    def test_new_fields_on_list_commands(self, cmd, extra_args, fixture, capsys):
        result = run_cmd(cmd + extra_args, make_osascript_result(fixture), capsys)
        assert isinstance(result, list)
        if result:
            for field in self.NEW_FIELDS:
                assert field in result[0], (
                    f"Field '{field}' missing from '{cmd[0]}' task record"
                )

    def test_info_has_new_fields(self, capsys):
        result = run_cmd(
            ["info", TASK_1["id"]],
            make_osascript_result(TASK_1),
            capsys,
        )
        for field in self.NEW_FIELDS:
            assert field in result, f"Field '{field}' missing from info task record"


# ---------------------------------------------------------------------------
# Repeat field in task records
# ---------------------------------------------------------------------------

class TestRepeatField:
    def test_repeat_none(self, capsys):
        result = run_cmd(
            ["info", TASK_1["id"]],
            make_osascript_result({**TASK_1, "repeat": None}),
            capsys,
        )
        assert result["repeat"] is None

    def test_repeat_present(self, capsys):
        result = run_cmd(
            ["info", TASK_3["id"]],
            make_osascript_result(TASK_3),
            capsys,
        )
        assert result["repeat"] is not None
        assert "method" in result["repeat"]
        assert "recurrence" in result["repeat"]

    def test_repeat_recurrence_format(self, capsys):
        result = run_cmd(
            ["info", TASK_3["id"]],
            make_osascript_result(TASK_3),
            capsys,
        )
        assert "FREQ=" in result["repeat"]["recurrence"]


# ---------------------------------------------------------------------------
# Date field format
# ---------------------------------------------------------------------------

class TestDateFormat:
    """All date fields must be either null or ISO YYYY-MM-DD strings."""

    DATE_FIELDS = ("dueDate", "deferDate", "effectiveDueDate", "completionDate")

    def test_task_dates_are_iso_or_null(self, capsys):
        result = run_cmd(
            ["info", TASK_1["id"]],
            make_osascript_result(TASK_1),
            capsys,
        )
        import re
        iso_re = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        for field in self.DATE_FIELDS:
            val = result.get(field)
            if val is not None:
                assert iso_re.match(val), (
                    f"Date field '{field}' has non-ISO value: {val!r}"
                )
