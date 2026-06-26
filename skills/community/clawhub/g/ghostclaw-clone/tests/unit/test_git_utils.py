"""Unit tests for ghostclaw.core.git_utils."""

import json
from unittest.mock import patch, MagicMock
from ghostclaw.core.git_utils import (
    get_git_diff,
    get_staged_diff,
    get_unstaged_diff,
    _parse_changed_files,
    has_uncommitted_changes,
    get_current_branch,
    get_current_sha,
    DiffResult,
)


def test_parse_changed_files():
    diff = """--- a/file1.py
+++ b/file1.py
@@ -1,5 +1,5 @@
--- a/file2.py
+++ b/file2.py
@@ -10,7 +10,7 @@
"""
    files = _parse_changed_files(diff)
    assert files == ["file1.py", "file2.py"]


@patch("subprocess.run")
def test_get_git_diff(mock_run):
    mock_run.return_value = MagicMock(stdout="--- a/module.py\n+++ b/module.py\n")
    result = get_git_diff(base_ref="main")
    assert result.against == "main"
    assert "module.py" in result.files_changed
    assert "--- a/module.py" in result.raw_diff


@patch("subprocess.run")
def test_get_staged_diff(mock_run):
    mock_run.return_value = MagicMock(stdout="--- a/staged.py\n+++ b/staged.py\n")
    result = get_staged_diff()
    assert result.against == "HEAD (staged)"
    assert "staged.py" in result.files_changed


@patch("subprocess.run")
def test_get_unstaged_diff(mock_run):
    mock_run.return_value = MagicMock(stdout="--- a/unstaged.py\n+++ b/unstaged.py\n")
    result = get_unstaged_diff()
    assert result.against == "index (unstaged)"
    assert "unstaged.py" in result.files_changed


@patch("subprocess.run")
def test_has_uncommitted_changes_true(mock_run):
    mock_run.return_value = MagicMock(stdout=" M file.py\n")
    assert has_uncommitted_changes() is True


@patch("subprocess.run")
def test_has_uncommitted_changes_false(mock_run):
    mock_run.return_value = MagicMock(stdout="")
    assert has_uncommitted_changes() is False


@patch("subprocess.run")
def test_get_current_branch(mock_run):
    mock_run.return_value = MagicMock(stdout="feature-branch\n")
    assert get_current_branch() == "feature-branch"


@patch("subprocess.run")
def test_get_current_branch_detached(mock_run):
    # First call returns HEAD, second returns SHA
    mock_run.side_effect = [
        MagicMock(stdout="HEAD\n"),
        MagicMock(stdout="abc123def456\n"),
    ]
    assert get_current_branch() == "abc123de"  # truncated to 8 chars


@patch("subprocess.run")
def test_get_current_sha(mock_run):
    mock_run.return_value = MagicMock(stdout="deadbeef1234567890\n")
    assert get_current_sha() == "deadbeef1234567890"
