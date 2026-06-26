"""
Tests for write authorization guard.

All prefs file I/O is redirected to tmp_path via the isolated_prefs fixture.
No live OmniFocus instance required.
"""

import json
import pytest
from unittest.mock import patch

import omnifocus
from omnifocus import dispatch, WRITE_COMMANDS, _load_prefs, _save_prefs
from conftest import make_osascript_result, TASK_1, INBOX_TASK


# ---------------------------------------------------------------------------
# Fixture: redirect prefs file to tmp_path
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def isolated_prefs(tmp_path, monkeypatch):
    monkeypatch.setattr(omnifocus, "PREFS_DIR",  tmp_path)
    monkeypatch.setattr(omnifocus, "PREFS_FILE", tmp_path / "prefs.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def write_prefs(prefs: dict):
    """Write prefs directly (bypasses the guard for test setup)."""
    _save_prefs(prefs)


def run_write_cmd(argv, mock_result, capsys):
    """Run a write command with a mocked osascript result."""
    with patch("subprocess.run", return_value=mock_result):
        dispatch(argv)
    return json.loads(capsys.readouterr().out)


def run_write_cmd_expect_exit(argv, capsys, code=None):
    """Run a command expecting sys.exit; return parsed stdout."""
    with pytest.raises(SystemExit) as exc_info:
        dispatch(argv)
    if code is not None:
        assert exc_info.value.code == code, (
            f"Expected exit code {code}, got {exc_info.value.code}"
        )
    return json.loads(capsys.readouterr().out)


# ---------------------------------------------------------------------------
# Mode: yolo — no prompting
# ---------------------------------------------------------------------------

class TestYolo:
    def test_write_proceeds_without_prompt(self, capsys):
        write_prefs({"mode": "yolo", "approved": []})
        result = run_write_cmd(
            ["complete", TASK_1["id"]],
            make_osascript_result({"success": True, "task": {**TASK_1, "completed": True}}),
            capsys,
        )
        assert result["success"] is True

    def test_all_write_cmds_pass(self, capsys):
        """Spot-check a variety of write commands in yolo mode."""
        write_prefs({"mode": "yolo", "approved": []})
        task_result = make_osascript_result({"success": True, "task": TASK_1})
        for cmd, args in [
            ("add",        ["My task"]),
            ("flag",       [TASK_1["id"], "true"]),
            ("tag",        [TASK_1["id"], "urgent"]),
        ]:
            with patch("subprocess.run", return_value=task_result):
                dispatch([cmd] + args)
            out = json.loads(capsys.readouterr().out)
            assert "error" not in out, f"Command '{cmd}' errored in yolo mode: {out}"


# ---------------------------------------------------------------------------
# Mode: once — unapproved
# ---------------------------------------------------------------------------

class TestOnceUnapproved:
    def test_blocks_unapproved_write(self, capsys):
        write_prefs({"mode": "once", "approved": []})
        result = run_write_cmd_expect_exit(["complete", TASK_1["id"]], capsys, code=2)
        assert result["auth_required"] is True

    def test_response_includes_cmd(self, capsys):
        write_prefs({"mode": "once", "approved": []})
        result = run_write_cmd_expect_exit(["delete", TASK_1["id"]], capsys, code=2)
        assert result["cmd"] == "delete"

    def test_response_includes_mode(self, capsys):
        write_prefs({"mode": "once", "approved": []})
        result = run_write_cmd_expect_exit(["rename", TASK_1["id"], "New name"], capsys, code=2)
        assert result["mode"] == "once"

    def test_response_includes_how_to_proceed(self, capsys):
        write_prefs({"mode": "once", "approved": []})
        result = run_write_cmd_expect_exit(["flag", TASK_1["id"]], capsys, code=2)
        assert "how_to_proceed" in result

    def test_default_prefs_blocks(self, capsys):
        """No prefs file at all — defaults to once, should block."""
        omnifocus.PREFS_FILE.unlink(missing_ok=True)
        result = run_write_cmd_expect_exit(["complete", TASK_1["id"]], capsys, code=2)
        assert result["auth_required"] is True

    def test_authorized_flag_ignored_in_once_mode(self, capsys):
        """--authorized does not bypass once-mode approval requirement."""
        write_prefs({"mode": "once", "approved": []})
        result = run_write_cmd_expect_exit(
            ["--authorized", "complete", TASK_1["id"]], capsys, code=2
        )
        assert result["auth_required"] is True


# ---------------------------------------------------------------------------
# Mode: once — after approve
# ---------------------------------------------------------------------------

class TestOnceApproved:
    def test_proceeds_after_approve(self, capsys):
        write_prefs({"mode": "once", "approved": ["complete"]})
        result = run_write_cmd(
            ["complete", TASK_1["id"]],
            make_osascript_result({"success": True, "task": {**TASK_1, "completed": True}}),
            capsys,
        )
        assert result["success"] is True

    def test_other_cmd_still_blocked(self, capsys):
        """Approving 'complete' does not unblock 'delete'."""
        write_prefs({"mode": "once", "approved": ["complete"]})
        result = run_write_cmd_expect_exit(["delete", TASK_1["id"]], capsys, code=2)
        assert result["auth_required"] is True

    def test_multiple_approved_cmds(self, capsys):
        write_prefs({"mode": "once", "approved": ["complete", "flag", "tag"]})
        for cmd, args, mock in [
            ("complete", [TASK_1["id"]],           {"success": True, "task": TASK_1}),
            ("flag",     [TASK_1["id"], "true"],    {"success": True, "task": TASK_1}),
            ("tag",      [TASK_1["id"], "urgent"],  {"success": True, "task": TASK_1}),
        ]:
            with patch("subprocess.run", return_value=make_osascript_result(mock)):
                dispatch([cmd] + args)
            out = json.loads(capsys.readouterr().out)
            assert out["success"] is True, f"'{cmd}' failed: {out}"


# ---------------------------------------------------------------------------
# Mode: every
# ---------------------------------------------------------------------------

class TestEvery:
    def test_blocks_without_flag(self, capsys):
        write_prefs({"mode": "every", "approved": []})
        result = run_write_cmd_expect_exit(["complete", TASK_1["id"]], capsys, code=2)
        assert result["auth_required"] is True
        assert result["mode"] == "every"

    def test_proceeds_with_authorized_flag(self, capsys):
        write_prefs({"mode": "every", "approved": []})
        result = run_write_cmd(
            ["complete", TASK_1["id"], "--authorized"],
            make_osascript_result({"success": True, "task": {**TASK_1, "completed": True}}),
            capsys,
        )
        assert result["success"] is True

    def test_flag_before_command(self, capsys):
        write_prefs({"mode": "every", "approved": []})
        result = run_write_cmd(
            ["--authorized", "complete", TASK_1["id"]],
            make_osascript_result({"success": True, "task": {**TASK_1, "completed": True}}),
            capsys,
        )
        assert result["success"] is True

    def test_approved_list_ignored_in_every_mode(self, capsys):
        """approved list has no effect in every mode — flag is always required."""
        write_prefs({"mode": "every", "approved": ["complete"]})
        result = run_write_cmd_expect_exit(["complete", TASK_1["id"]], capsys, code=2)
        assert result["auth_required"] is True


# ---------------------------------------------------------------------------
# prefs command
# ---------------------------------------------------------------------------

class TestPrefsCommand:
    def test_show_returns_defaults(self, capsys):
        """When no prefs file exists, show returns the built-in defaults."""
        omnifocus.PREFS_FILE.unlink(missing_ok=True)
        dispatch(["prefs", "show"])
        result = json.loads(capsys.readouterr().out)
        assert result["mode"] == "once"
        assert result["approved"] == []

    def test_show_no_subcommand(self, capsys):
        dispatch(["prefs"])
        result = json.loads(capsys.readouterr().out)
        assert "mode" in result

    def test_set_yolo(self, capsys):
        dispatch(["prefs", "set", "yolo"])
        result = json.loads(capsys.readouterr().out)
        assert result["success"] is True
        assert result["mode"] == "yolo"
        dispatch(["prefs", "show"])
        state = json.loads(capsys.readouterr().out)
        assert state["mode"] == "yolo"

    def test_set_every(self, capsys):
        dispatch(["prefs", "set", "every"])
        json.loads(capsys.readouterr().out)
        dispatch(["prefs", "show"])
        state = json.loads(capsys.readouterr().out)
        assert state["mode"] == "every"

    def test_set_invalid_mode_exits_1(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            dispatch(["prefs", "set", "mayhem"])
        assert exc_info.value.code == 1
        assert "error" in json.loads(capsys.readouterr().out)

    def test_set_missing_arg_exits_1(self, capsys):
        with pytest.raises(SystemExit):
            dispatch(["prefs", "set"])
        assert "error" in json.loads(capsys.readouterr().out)

    def test_approve_adds_to_list(self, capsys):
        write_prefs({"mode": "once", "approved": []})
        dispatch(["prefs", "approve", "complete"])
        result = json.loads(capsys.readouterr().out)
        assert result["success"] is True
        assert "complete" in result["approved"]

    def test_approve_persists(self, capsys):
        write_prefs({"mode": "once", "approved": []})
        dispatch(["prefs", "approve", "complete"])
        capsys.readouterr()
        dispatch(["prefs", "show"])
        state = json.loads(capsys.readouterr().out)
        assert "complete" in state["approved"]

    def test_approve_idempotent(self, capsys):
        write_prefs({"mode": "once", "approved": ["complete"]})
        dispatch(["prefs", "approve", "complete"])
        result = json.loads(capsys.readouterr().out)
        assert result["approved"].count("complete") == 1

    def test_approve_unknown_cmd_exits_1(self, capsys):
        write_prefs({"mode": "once", "approved": []})
        with pytest.raises(SystemExit) as exc_info:
            dispatch(["prefs", "approve", "notacommand"])
        assert exc_info.value.code == 1
        assert "error" in json.loads(capsys.readouterr().out)

    def test_revoke_removes_cmd(self, capsys):
        write_prefs({"mode": "once", "approved": ["complete", "flag"]})
        dispatch(["prefs", "revoke", "complete"])
        result = json.loads(capsys.readouterr().out)
        assert "complete" not in result["approved"]
        assert "flag" in result["approved"]

    def test_revoke_nonexistent_is_safe(self, capsys):
        write_prefs({"mode": "once", "approved": []})
        dispatch(["prefs", "revoke", "complete"])
        result = json.loads(capsys.readouterr().out)
        assert result["success"] is True

    def test_reset_clears_approvals(self, capsys):
        write_prefs({"mode": "once", "approved": ["complete", "delete", "flag"]})
        dispatch(["prefs", "reset"])
        capsys.readouterr()
        dispatch(["prefs", "show"])
        state = json.loads(capsys.readouterr().out)
        assert state["approved"] == []
        assert state["mode"] == "once"

    def test_unknown_subcommand_exits_1(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            dispatch(["prefs", "bogus"])
        assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# Read commands are never guarded
# ---------------------------------------------------------------------------

class TestReadCommandsUnguarded:
    @pytest.mark.parametrize("cmd,args,mock_data", [
        ("inbox",   [],           [INBOX_TASK]),
        ("today",   [],           [TASK_1]),
        ("flagged", [],           [TASK_1]),
        ("summary", [],           {"projects": 3, "tasks": 15, "flagged": 2,
                                   "due": 4, "available": 10, "completed": 5, "inbox": 1}),
    ])
    def test_read_never_blocked_in_every_mode(self, cmd, args, mock_data, capsys):
        write_prefs({"mode": "every", "approved": []})
        with patch("subprocess.run", return_value=make_osascript_result(mock_data)):
            dispatch([cmd] + args)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert "auth_required" not in data


# ---------------------------------------------------------------------------
# Resilience: corrupted / missing prefs
# ---------------------------------------------------------------------------

class TestPrefsResilience:
    def test_corrupt_prefs_defaults_to_once_blocks(self, tmp_path, monkeypatch, capsys):
        import omnifocus as om
        pf = tmp_path / "prefs.json"
        pf.write_text("{not valid json")
        monkeypatch.setattr(om, "PREFS_FILE", pf)
        monkeypatch.setattr(om, "PREFS_DIR",  tmp_path)
        result = run_write_cmd_expect_exit(["complete", TASK_1["id"]], capsys, code=2)
        assert result["auth_required"] is True

    def test_missing_approved_key_no_crash(self, tmp_path, monkeypatch, capsys):
        import omnifocus as om
        pf = tmp_path / "prefs.json"
        pf.write_text('{"mode": "once"}')
        monkeypatch.setattr(om, "PREFS_FILE", pf)
        monkeypatch.setattr(om, "PREFS_DIR",  tmp_path)
        # Should block cleanly, not crash
        result = run_write_cmd_expect_exit(["complete", TASK_1["id"]], capsys, code=2)
        assert result["auth_required"] is True

    def test_invalid_mode_value_defaults_to_once(self, tmp_path, monkeypatch, capsys):
        import omnifocus as om
        pf = tmp_path / "prefs.json"
        pf.write_text('{"mode": "chaos", "approved": []}')
        monkeypatch.setattr(om, "PREFS_FILE", pf)
        monkeypatch.setattr(om, "PREFS_DIR",  tmp_path)
        result = run_write_cmd_expect_exit(["complete", TASK_1["id"]], capsys, code=2)
        assert result["auth_required"] is True


# ---------------------------------------------------------------------------
# --authorized flag does not pollute command args
# ---------------------------------------------------------------------------

class TestAuthorizedFlagStripping:
    def test_flag_stripped_from_rename_args(self, capsys):
        """--authorized must not become the new task name in rename."""
        write_prefs({"mode": "every", "approved": []})
        renamed = {**TASK_1, "name": "New name"}
        result = run_write_cmd(
            ["rename", TASK_1["id"], "New name", "--authorized"],
            make_osascript_result({"success": True, "task": renamed}),
            capsys,
        )
        assert result["success"] is True
        assert result["task"]["name"] == "New name"

    def test_flag_stripped_from_note_args(self, capsys):
        write_prefs({"mode": "every", "approved": []})
        noted = {**TASK_1, "note": "actual note"}
        result = run_write_cmd(
            ["--authorized", "note", TASK_1["id"], "actual note"],
            make_osascript_result({"success": True, "task": noted}),
            capsys,
        )
        assert result["success"] is True
