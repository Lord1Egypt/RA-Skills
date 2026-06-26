"""
Baseline regression tests for all commands documented in SKILL.md.

Tests mock subprocess.run — no live OmniFocus instance required.
Each test:
  1. Primes mock_osascript with realistic fixture data.
  2. Calls dispatch() with the appropriate argv.
  3. Asserts on stdout JSON structure and values.
"""

import json
import pytest
from unittest.mock import patch, MagicMock

from omnifocus import dispatch
from conftest import (
    make_osascript_result,
    make_osascript_error,
    TASK_1,
    TASK_2,
    TASK_3,
    TASK_COMPLETED,
    INBOX_TASK,
    PROJECT_WORK,
    PROJECT_ERRANDS,
    PROJECT_HABITS,
    FOLDER_PROFESSIONAL,
    FOLDER_PERSONAL,
    TAG_FOCUS,
    TAG_HOME,
    TAG_REVIEW,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run_cmd(argv, mock_result, capsys):
    """Prime mock, run dispatch, return parsed stdout."""
    with patch("subprocess.run", return_value=mock_result):
        dispatch(argv)
    out = capsys.readouterr().out
    return json.loads(out)


def run_cmd_expect_error(argv, mock_result, capsys):
    """Run dispatch expecting a sys.exit(1); return the printed error dict."""
    with patch("subprocess.run", return_value=mock_result):
        with pytest.raises(SystemExit) as exc_info:
            dispatch(argv)
    assert exc_info.value.code == 1
    out = capsys.readouterr().out
    return json.loads(out)


# ---------------------------------------------------------------------------
# READ: inbox
# ---------------------------------------------------------------------------

class TestInbox:
    def test_returns_list(self, capsys):
        result = run_cmd(
            ["inbox"],
            make_osascript_result([INBOX_TASK]),
            capsys,
        )
        assert isinstance(result, list)

    def test_task_fields(self, capsys):
        result = run_cmd(
            ["inbox"],
            make_osascript_result([INBOX_TASK]),
            capsys,
        )
        assert len(result) == 1
        t = result[0]
        assert t["id"] == INBOX_TASK["id"]
        assert t["name"] == INBOX_TASK["name"]
        assert "flagged" in t
        assert "tags" in t

    def test_empty_inbox(self, capsys):
        result = run_cmd(["inbox"], make_osascript_result([]), capsys)
        assert result == []

    def test_osascript_failure(self, capsys):
        err_mock = MagicMock()
        err_mock.returncode = 1
        err_mock.stdout = ""
        err_mock.stderr = "OmniFocus not running"
        with patch("subprocess.run", return_value=err_mock):
            with pytest.raises(SystemExit):
                dispatch(["inbox"])
        out = capsys.readouterr().out
        data = json.loads(out)
        assert "error" in data


# ---------------------------------------------------------------------------
# READ: folders
# ---------------------------------------------------------------------------

class TestFolders:
    def test_returns_list(self, capsys):
        result = run_cmd(
            ["folders"],
            make_osascript_result([FOLDER_PROFESSIONAL, FOLDER_PERSONAL]),
            capsys,
        )
        assert isinstance(result, list)
        assert len(result) == 2

    def test_folder_fields(self, capsys):
        result = run_cmd(
            ["folders"],
            make_osascript_result([FOLDER_PROFESSIONAL]),
            capsys,
        )
        f = result[0]
        assert f["id"] == FOLDER_PROFESSIONAL["id"]
        assert f["name"] == FOLDER_PROFESSIONAL["name"]
        assert "projectCount" in f

    def test_new_fields_present(self, capsys):
        """Folders now include parent and folderCount — additive."""
        result = run_cmd(
            ["folders"],
            make_osascript_result([FOLDER_PROFESSIONAL]),
            capsys,
        )
        f = result[0]
        assert "parent" in f
        assert "folderCount" in f


# ---------------------------------------------------------------------------
# READ: projects
# ---------------------------------------------------------------------------

class TestProjects:
    def test_all_projects(self, capsys):
        result = run_cmd(
            ["projects"],
            make_osascript_result([PROJECT_WORK, PROJECT_ERRANDS]),
            capsys,
        )
        assert isinstance(result, list)
        assert len(result) == 2

    def test_project_fields(self, capsys):
        result = run_cmd(
            ["projects"],
            make_osascript_result([PROJECT_WORK]),
            capsys,
        )
        p = result[0]
        for key in ("id", "name", "folder", "taskCount", "status"):
            assert key in p, f"Missing key: {key}"

    def test_new_fields_present(self, capsys):
        """availableTaskCount, flagged, completed, due, defer, note are additive."""
        result = run_cmd(
            ["projects"],
            make_osascript_result([PROJECT_WORK]),
            capsys,
        )
        p = result[0]
        for key in ("availableTaskCount", "flagged", "completed"):
            assert key in p, f"Missing key: {key}"

    def test_projects_filtered_by_folder(self, capsys):
        result = run_cmd(
            ["projects", "Personal"],
            make_osascript_result([PROJECT_ERRANDS, PROJECT_HABITS]),
            capsys,
        )
        assert isinstance(result, list)
        assert len(result) == 2

    def test_folder_not_found(self, capsys):
        result = run_cmd_expect_error(
            ["projects", "NoSuchFolder"],
            make_osascript_result({"error": "Folder not found: NoSuchFolder"}),
            capsys,
        )
        assert "error" in result


# ---------------------------------------------------------------------------
# READ: tasks
# ---------------------------------------------------------------------------

class TestTasks:
    def test_tasks_in_project(self, capsys):
        result = run_cmd(
            ["tasks", "Work"],
            make_osascript_result([TASK_1, TASK_COMPLETED]),
            capsys,
        )
        assert isinstance(result, list)
        assert len(result) == 2

    def test_task_fields(self, capsys):
        result = run_cmd(
            ["tasks", "Work"],
            make_osascript_result([TASK_1]),
            capsys,
        )
        t = result[0]
        for key in ("id", "name", "note", "flagged", "completed",
                    "deferDate", "dueDate", "project", "tags", "repeat"):
            assert key in t, f"Missing key: {key}"

    def test_new_task_fields(self, capsys):
        """available, effectiveDueDate, completionDate, estimatedMinutes, folder."""
        result = run_cmd(
            ["tasks", "Work"],
            make_osascript_result([TASK_1]),
            capsys,
        )
        t = result[0]
        for key in ("available", "effectiveDueDate", "completionDate",
                    "estimatedMinutes", "folder"):
            assert key in t, f"Missing key: {key}"

    def test_missing_project_arg(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["tasks"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)

    def test_project_not_found(self, capsys):
        result = run_cmd_expect_error(
            ["tasks", "NoSuchProject"],
            make_osascript_result({"error": "Project not found: NoSuchProject"}),
            capsys,
        )
        assert "error" in result


# ---------------------------------------------------------------------------
# READ: tags
# ---------------------------------------------------------------------------

class TestTags:
    def test_returns_list(self, capsys):
        result = run_cmd(
            ["tags"],
            make_osascript_result([TAG_FOCUS, TAG_HOME, TAG_REVIEW]),
            capsys,
        )
        assert isinstance(result, list)
        assert len(result) == 3

    def test_tag_fields(self, capsys):
        result = run_cmd(
            ["tags"],
            make_osascript_result([TAG_FOCUS]),
            capsys,
        )
        t = result[0]
        assert t["id"] == TAG_FOCUS["id"]
        assert t["name"] == TAG_FOCUS["name"]

    def test_new_tag_fields(self, capsys):
        """parent, childCount, taskCount, availableTaskCount are additive."""
        result = run_cmd(
            ["tags"],
            make_osascript_result([TAG_REVIEW]),
            capsys,
        )
        t = result[0]
        for key in ("parent", "childCount", "taskCount", "availableTaskCount"):
            assert key in t, f"Missing key: {key}"


# ---------------------------------------------------------------------------
# READ: today
# ---------------------------------------------------------------------------

class TestToday:
    def test_returns_list(self, capsys):
        result = run_cmd(
            ["today"],
            make_osascript_result([TASK_1]),
            capsys,
        )
        assert isinstance(result, list)

    def test_task_shape(self, capsys):
        result = run_cmd(
            ["today"],
            make_osascript_result([TASK_1]),
            capsys,
        )
        t = result[0]
        assert "id" in t and "name" in t

    def test_empty(self, capsys):
        result = run_cmd(["today"], make_osascript_result([]), capsys)
        assert result == []


# ---------------------------------------------------------------------------
# READ: flagged
# ---------------------------------------------------------------------------

class TestFlagged:
    def test_returns_list(self, capsys):
        result = run_cmd(
            ["flagged"],
            make_osascript_result([TASK_1]),
            capsys,
        )
        assert isinstance(result, list)

    def test_flagged_task(self, capsys):
        result = run_cmd(
            ["flagged"],
            make_osascript_result([TASK_1]),
            capsys,
        )
        assert result[0]["flagged"] is True

    def test_empty(self, capsys):
        result = run_cmd(["flagged"], make_osascript_result([]), capsys)
        assert result == []


# ---------------------------------------------------------------------------
# READ: search
# ---------------------------------------------------------------------------

class TestSearch:
    def test_returns_matches(self, capsys):
        result = run_cmd(
            ["search", "quarterly"],
            make_osascript_result([TASK_1]),
            capsys,
        )
        assert isinstance(result, list)
        assert len(result) == 1

    def test_no_results(self, capsys):
        result = run_cmd(
            ["search", "xyzzy"],
            make_osascript_result([]),
            capsys,
        )
        assert result == []

    def test_multi_word_query(self, capsys):
        result = run_cmd(
            ["search", "quarterly", "report"],
            make_osascript_result([TASK_1]),
            capsys,
        )
        assert isinstance(result, list)

    def test_missing_query(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["search"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


# ---------------------------------------------------------------------------
# READ: info
# ---------------------------------------------------------------------------

class TestInfo:
    def test_returns_single_task(self, capsys):
        result = run_cmd(
            ["info", TASK_1["id"]],
            make_osascript_result(TASK_1),
            capsys,
        )
        assert result["id"] == TASK_1["id"]
        assert result["name"] == TASK_1["name"]

    def test_all_fields(self, capsys):
        result = run_cmd(
            ["info", TASK_1["id"]],
            make_osascript_result(TASK_1),
            capsys,
        )
        for key in ("id", "name", "note", "flagged", "completed",
                    "deferDate", "dueDate", "project", "tags", "repeat"):
            assert key in result, f"Missing key: {key}"

    def test_not_found(self, capsys):
        result = run_cmd_expect_error(
            ["info", "nonexistent"],
            make_osascript_result({"error": "Task not found: nonexistent"}),
            capsys,
        )
        assert "error" in result

    def test_missing_id_arg(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["info"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


# ---------------------------------------------------------------------------
# CREATE: add
# ---------------------------------------------------------------------------

class TestAdd:
    def test_add_to_inbox(self, capsys):
        result = run_cmd(
            ["add", "Buy milk"],
            make_osascript_result({"success": True, "task": INBOX_TASK}),
            capsys,
        )
        assert result["success"] is True
        assert "task" in result

    def test_add_to_project(self, capsys):
        task = {**TASK_2}
        result = run_cmd(
            ["add", "Buy groceries", "Errands"],
            make_osascript_result({"success": True, "task": task}),
            capsys,
        )
        assert result["success"] is True

    def test_project_not_found(self, capsys):
        result = run_cmd_expect_error(
            ["add", "Task", "NoSuchProject"],
            make_osascript_result({"error": "Project not found: NoSuchProject"}),
            capsys,
        )
        assert "error" in result

    def test_missing_name_arg(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["add"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


# ---------------------------------------------------------------------------
# CREATE: newproject
# ---------------------------------------------------------------------------

class TestNewProject:
    def test_creates_project(self, capsys):
        result = run_cmd(
            ["newproject", "New Project"],
            make_osascript_result({"success": True, "project": PROJECT_WORK}),
            capsys,
        )
        assert result["success"] is True
        assert "project" in result

    def test_creates_in_folder(self, capsys):
        result = run_cmd(
            ["newproject", "New Project", "Professional"],
            make_osascript_result({"success": True, "project": PROJECT_WORK}),
            capsys,
        )
        assert result["success"] is True

    def test_folder_not_found(self, capsys):
        result = run_cmd_expect_error(
            ["newproject", "P", "NoFolder"],
            make_osascript_result({"error": "Folder not found: NoFolder"}),
            capsys,
        )
        assert "error" in result

    def test_missing_name_arg(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["newproject"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


# ---------------------------------------------------------------------------
# CREATE: newfolder
# ---------------------------------------------------------------------------

class TestNewFolder:
    def test_creates_folder(self, capsys):
        result = run_cmd(
            ["newfolder", "New Area"],
            make_osascript_result({
                "success": True,
                "folder": {"id": "xx1", "name": "New Area"},
            }),
            capsys,
        )
        assert result["success"] is True
        assert result["folder"]["name"] == "New Area"

    def test_missing_name_arg(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["newfolder"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


# ---------------------------------------------------------------------------
# CREATE: newtag
# ---------------------------------------------------------------------------

class TestNewTag:
    def test_creates_new_tag(self, capsys):
        result = run_cmd(
            ["newtag", "urgent"],
            make_osascript_result({
                "success": True,
                "tag": {"id": "t1", "name": "urgent"},
                "created": True,
            }),
            capsys,
        )
        assert result["success"] is True
        assert result.get("created") is True

    def test_returns_existing_tag(self, capsys):
        result = run_cmd(
            ["newtag", "focus"],
            make_osascript_result({
                "success": True,
                "tag": {"id": TAG_FOCUS["id"], "name": "focus"},
                "existed": True,
            }),
            capsys,
        )
        assert result["success"] is True
        assert result.get("existed") is True

    def test_missing_name_arg(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["newtag"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


# ---------------------------------------------------------------------------
# MODIFY: complete / uncomplete
# ---------------------------------------------------------------------------

class TestComplete:
    def test_complete(self, capsys):
        completed = {**TASK_1, "completed": True, "available": False}
        result = run_cmd(
            ["complete", TASK_1["id"]],
            make_osascript_result({"success": True, "task": completed}),
            capsys,
        )
        assert result["success"] is True
        assert result["task"]["completed"] is True

    def test_not_found(self, capsys):
        result = run_cmd_expect_error(
            ["complete", "bad_id"],
            make_osascript_result({"error": "Task not found: bad_id"}),
            capsys,
        )
        assert "error" in result

    def test_missing_id(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["complete"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


class TestUncomplete:
    def test_uncomplete(self, capsys):
        incomplete = {**TASK_COMPLETED, "completed": False}
        result = run_cmd(
            ["uncomplete", TASK_COMPLETED["id"]],
            make_osascript_result({"success": True, "task": incomplete}),
            capsys,
        )
        assert result["success"] is True
        assert result["task"]["completed"] is False

    def test_missing_id(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["uncomplete"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


# ---------------------------------------------------------------------------
# MODIFY: delete
# ---------------------------------------------------------------------------

class TestDelete:
    def test_delete(self, capsys):
        result = run_cmd(
            ["delete", TASK_1["id"]],
            make_osascript_result({
                "success": True,
                "deleted": {"id": TASK_1["id"], "name": TASK_1["name"]},
            }),
            capsys,
        )
        assert result["success"] is True
        assert result["deleted"]["id"] == TASK_1["id"]
        assert result["deleted"]["name"] == TASK_1["name"]

    def test_not_found(self, capsys):
        result = run_cmd_expect_error(
            ["delete", "bad_id"],
            make_osascript_result({"error": "Task not found: bad_id"}),
            capsys,
        )
        assert "error" in result

    def test_missing_id(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["delete"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


# ---------------------------------------------------------------------------
# MODIFY: rename
# ---------------------------------------------------------------------------

class TestRename:
    def test_rename(self, capsys):
        renamed = {**TASK_1, "name": "Review annual report"}
        result = run_cmd(
            ["rename", TASK_1["id"], "Review annual report"],
            make_osascript_result({"success": True, "task": renamed}),
            capsys,
        )
        assert result["success"] is True
        assert result["task"]["name"] == "Review annual report"

    def test_rename_multi_word(self, capsys):
        renamed = {**TASK_1, "name": "A much longer task name"}
        result = run_cmd(
            ["rename", TASK_1["id"], "A", "much", "longer", "task", "name"],
            make_osascript_result({"success": True, "task": renamed}),
            capsys,
        )
        assert result["task"]["name"] == "A much longer task name"

    def test_missing_args(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["rename", TASK_1["id"]])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


# ---------------------------------------------------------------------------
# MODIFY: note / setnote
# ---------------------------------------------------------------------------

class TestNote:
    def test_append_note(self, capsys):
        noted = {**TASK_2, "note": "New note text"}
        result = run_cmd(
            ["note", TASK_2["id"], "New note text"],
            make_osascript_result({"success": True, "task": noted}),
            capsys,
        )
        assert result["success"] is True
        assert result["task"]["note"] == "New note text"

    def test_missing_args(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["note", TASK_1["id"]])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


class TestSetNote:
    def test_replace_note(self, capsys):
        noted = {**TASK_1, "note": "Completely new note"}
        result = run_cmd(
            ["setnote", TASK_1["id"], "Completely new note"],
            make_osascript_result({"success": True, "task": noted}),
            capsys,
        )
        assert result["success"] is True
        assert result["task"]["note"] == "Completely new note"


# ---------------------------------------------------------------------------
# MODIFY: defer / due
# ---------------------------------------------------------------------------

class TestDefer:
    def test_set_defer(self, capsys):
        deferred = {**TASK_2, "deferDate": "2026-05-01"}
        result = run_cmd(
            ["defer", TASK_2["id"], "2026-05-01"],
            make_osascript_result({"success": True, "task": deferred}),
            capsys,
        )
        assert result["success"] is True
        assert result["task"]["deferDate"] == "2026-05-01"

    def test_missing_args(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["defer", TASK_1["id"]])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


class TestDue:
    def test_set_due(self, capsys):
        due = {**TASK_2, "dueDate": "2026-04-15"}
        result = run_cmd(
            ["due", TASK_2["id"], "2026-04-15"],
            make_osascript_result({"success": True, "task": due}),
            capsys,
        )
        assert result["success"] is True
        assert result["task"]["dueDate"] == "2026-04-15"

    def test_missing_args(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["due", TASK_1["id"]])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


# ---------------------------------------------------------------------------
# MODIFY: flag
# ---------------------------------------------------------------------------

class TestFlag:
    def test_flag_true(self, capsys):
        flagged = {**TASK_2, "flagged": True}
        result = run_cmd(
            ["flag", TASK_2["id"], "true"],
            make_osascript_result({"success": True, "task": flagged}),
            capsys,
        )
        assert result["success"] is True
        assert result["task"]["flagged"] is True

    def test_flag_false(self, capsys):
        unflagged = {**TASK_1, "flagged": False}
        result = run_cmd(
            ["flag", TASK_1["id"], "false"],
            make_osascript_result({"success": True, "task": unflagged}),
            capsys,
        )
        assert result["task"]["flagged"] is False

    def test_flag_default_true(self, capsys):
        """flag <id> with no second arg defaults to true."""
        flagged = {**TASK_2, "flagged": True}
        result = run_cmd(
            ["flag", TASK_2["id"]],
            make_osascript_result({"success": True, "task": flagged}),
            capsys,
        )
        assert result["task"]["flagged"] is True

    def test_missing_id(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["flag"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


# ---------------------------------------------------------------------------
# MODIFY: tag / untag
# ---------------------------------------------------------------------------

class TestTag:
    def test_add_tag(self, capsys):
        tagged = {**TASK_2, "tags": ["home", "urgent"]}
        result = run_cmd(
            ["tag", TASK_2["id"], "urgent"],
            make_osascript_result({"success": True, "task": tagged}),
            capsys,
        )
        assert result["success"] is True
        assert "urgent" in result["task"]["tags"]

    def test_missing_args(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["tag", TASK_1["id"]])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


class TestUntag:
    def test_remove_tag(self, capsys):
        untagged = {**TASK_1, "tags": ["finance"]}
        result = run_cmd(
            ["untag", TASK_1["id"], "focus"],
            make_osascript_result({"success": True, "task": untagged}),
            capsys,
        )
        assert result["success"] is True
        assert "focus" not in result["task"]["tags"]

    def test_tag_not_found(self, capsys):
        result = run_cmd_expect_error(
            ["untag", TASK_1["id"], "nonexistent"],
            make_osascript_result({"error": "Tag not found: nonexistent"}),
            capsys,
        )
        assert "error" in result

    def test_missing_args(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["untag", TASK_1["id"]])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


# ---------------------------------------------------------------------------
# MODIFY: move
# ---------------------------------------------------------------------------

class TestMove:
    def test_move(self, capsys):
        moved = {**TASK_2, "project": "Work", "folder": "Professional"}
        result = run_cmd(
            ["move", TASK_2["id"], "Work"],
            make_osascript_result({"success": True, "task": moved}),
            capsys,
        )
        assert result["success"] is True
        assert result["task"]["project"] == "Work"

    def test_project_not_found(self, capsys):
        result = run_cmd_expect_error(
            ["move", TASK_1["id"], "NoProject"],
            make_osascript_result({"error": "Project not found: NoProject"}),
            capsys,
        )
        assert "error" in result

    def test_missing_args(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["move", TASK_1["id"]])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


# ---------------------------------------------------------------------------
# REPEAT: repeat / unrepeat
# ---------------------------------------------------------------------------

class TestRepeat:
    def test_set_fixed_weekly(self, capsys):
        with_repeat = {
            **TASK_3,
            "repeat": {"method": "fixed", "recurrence": "FREQ=WEEKLY;INTERVAL=1"},
        }
        result = run_cmd(
            ["repeat", TASK_3["id"], "fixed", "1", "weeks"],
            make_osascript_result({"success": True, "task": with_repeat}),
            capsys,
        )
        assert result["success"] is True
        assert result["task"]["repeat"] is not None
        assert "WEEKLY" in result["task"]["repeat"]["recurrence"]

    def test_set_due_after_completion_daily(self, capsys):
        with_repeat = {
            **TASK_2,
            "repeat": {"method": "due-after-completion", "recurrence": "FREQ=DAILY;INTERVAL=2"},
        }
        result = run_cmd(
            ["repeat", TASK_2["id"], "due-after-completion", "2", "days"],
            make_osascript_result({"success": True, "task": with_repeat}),
            capsys,
        )
        assert result["success"] is True

    def test_invalid_method(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["repeat", TASK_1["id"], "badmethod", "1", "weeks"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)

    def test_invalid_unit(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["repeat", TASK_1["id"], "fixed", "1", "fortnights"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)

    def test_missing_args(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["repeat", TASK_1["id"], "fixed", "1"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


class TestUnrepeat:
    def test_unrepeat(self, capsys):
        cleared = {**TASK_3, "repeat": None}
        result = run_cmd(
            ["unrepeat", TASK_3["id"]],
            make_osascript_result({"success": True, "task": cleared}),
            capsys,
        )
        assert result["success"] is True
        assert result["task"]["repeat"] is None

    def test_missing_id(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["unrepeat"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)


# ---------------------------------------------------------------------------
# Help
# ---------------------------------------------------------------------------

class TestHelp:
    def test_help_command(self, capsys):
        dispatch(["help"])
        out = json.loads(capsys.readouterr().out)
        assert "commands" in out

    def test_no_args_returns_help(self, capsys):
        dispatch([])
        out = json.loads(capsys.readouterr().out)
        assert "commands" in out

    def test_unknown_command(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["doesnotexist"])
        out = capsys.readouterr().out
        assert "error" in json.loads(out)
