"""
Shared fixtures and helpers for OmniFocus skill tests.

All tests mock subprocess.run so no live OmniFocus instance is needed.
The mock intercepts the osascript call and returns pre-canned JSON.
"""

import json
import sys
import os
from unittest.mock import patch, MagicMock
import pytest

# Ensure scripts/ is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))


@pytest.fixture(autouse=True)
def default_yolo_prefs(tmp_path, monkeypatch):
    """
    By default all tests run with write auth in yolo mode so the guard
    never fires. test_auth.py overrides this with its own isolated_prefs
    fixture that writes specific mode/approved settings per test.
    """
    import omnifocus
    monkeypatch.setattr(omnifocus, "PREFS_DIR",  tmp_path)
    monkeypatch.setattr(omnifocus, "PREFS_FILE", tmp_path / "prefs.json")
    omnifocus._save_prefs({"mode": "yolo", "approved": []})


def make_osascript_result(data):
    """
    Build a mock CompletedProcess whose stdout is JSON.stringify-equivalent
    of `data` — i.e. the raw string OmniFocus would return via evaluate javascript.
    """
    mock = MagicMock()
    mock.returncode = 0
    mock.stdout = json.dumps(data)
    mock.stderr = ""
    return mock


def make_osascript_error(message):
    """Build a mock CompletedProcess that simulates an OmniFocus JS error."""
    mock = MagicMock()
    mock.returncode = 1
    mock.stdout = ""
    mock.stderr = message
    return mock


@pytest.fixture
def mock_osascript():
    """
    Fixture that patches subprocess.run.

    Usage:
        def test_something(mock_osascript, capsys):
            mock_osascript.return_value = make_osascript_result({"key": "val"})
            dispatch(["inbox"])
            out = capsys.readouterr().out
            assert json.loads(out) == [...]
    """
    with patch("subprocess.run") as mock_run:
        yield mock_run


# ---------------------------------------------------------------------------
# Fixture data — realistic OmniFocus objects
# ---------------------------------------------------------------------------

TASK_1 = {
    "id": "aAbBcC1",
    "name": "Review quarterly report",
    "note": "Check figures on slide 4",
    "flagged": True,
    "completed": False,
    "available": True,
    "deferDate": None,
    "dueDate": "2026-04-10",
    "effectiveDueDate": "2026-04-10",
    "completionDate": None,
    "estimatedMinutes": 30,
    "project": "Work",
    "folder": "Professional",
    "tags": ["focus", "finance"],
    "repeat": None,
}

TASK_2 = {
    "id": "dDeEfF2",
    "name": "Buy groceries",
    "note": None,
    "flagged": False,
    "completed": False,
    "available": True,
    "deferDate": None,
    "dueDate": None,
    "effectiveDueDate": None,
    "completionDate": None,
    "estimatedMinutes": None,
    "project": "Errands",
    "folder": "Personal",
    "tags": ["home"],
    "repeat": None,
}

TASK_3 = {
    "id": "gGhHiI3",
    "name": "Weekly review",
    "note": "GTD weekly review process",
    "flagged": False,
    "completed": False,
    "available": True,
    "deferDate": None,
    "dueDate": None,
    "effectiveDueDate": None,
    "completionDate": None,
    "estimatedMinutes": 60,
    "project": "Habits",
    "folder": "Personal",
    "tags": ["review"],
    "repeat": {"method": "fixed", "recurrence": "FREQ=WEEKLY;INTERVAL=1"},
}

TASK_COMPLETED = {
    "id": "jJkKlL4",
    "name": "Send invoice",
    "note": None,
    "flagged": False,
    "completed": True,
    "available": False,
    "deferDate": None,
    "dueDate": "2026-04-01",
    "effectiveDueDate": "2026-04-01",
    "completionDate": "2026-04-01",
    "estimatedMinutes": None,
    "project": "Work",
    "folder": "Professional",
    "tags": [],
    "repeat": None,
}

INBOX_TASK = {
    "id": "mMnNoO5",
    "name": "Process new email",
    "note": None,
    "flagged": False,
    "completed": False,
    "available": True,
    "deferDate": None,
    "dueDate": None,
    "effectiveDueDate": None,
    "completionDate": None,
    "estimatedMinutes": None,
    "project": None,
    "folder": None,
    "tags": [],
    "repeat": None,
}

PROJECT_WORK = {
    "id": "pPqQrR6",
    "name": "Work",
    "folder": "Professional",
    "status": "active",
    "flagged": False,
    "completed": False,
    "due": None,
    "defer": None,
    "note": None,
    "taskCount": 3,
    "availableTaskCount": 2,
}

PROJECT_ERRANDS = {
    "id": "sStTuU7",
    "name": "Errands",
    "folder": "Personal",
    "status": "active",
    "flagged": False,
    "completed": False,
    "due": None,
    "defer": None,
    "note": None,
    "taskCount": 1,
    "availableTaskCount": 1,
}

PROJECT_HABITS = {
    "id": "vVwWxX8",
    "name": "Habits",
    "folder": "Personal",
    "status": "active",
    "flagged": False,
    "completed": False,
    "due": None,
    "defer": None,
    "note": None,
    "taskCount": 1,
    "availableTaskCount": 1,
}

FOLDER_PROFESSIONAL = {
    "id": "yYzZ0A9",
    "name": "Professional",
    "parent": None,
    "folderCount": 0,
    "projectCount": 1,
}

FOLDER_PERSONAL = {
    "id": "bBcCdD0",
    "name": "Personal",
    "parent": None,
    "folderCount": 0,
    "projectCount": 2,
}

TAG_FOCUS = {
    "id": "eFgGhH1",
    "name": "focus",
    "parent": None,
    "childCount": 0,
    "taskCount": 1,
    "availableTaskCount": 1,
}

TAG_HOME = {
    "id": "iIjJkK2",
    "name": "home",
    "parent": None,
    "childCount": 0,
    "taskCount": 1,
    "availableTaskCount": 1,
}

TAG_REVIEW = {
    "id": "lLmMnN3",
    "name": "review",
    "parent": None,
    "childCount": 2,
    "taskCount": 3,
    "availableTaskCount": 3,
}
