import os
import sys
import subprocess
import pytest
import time
from unittest.mock import patch, MagicMock

# Assuming orchestrator is importable or we can test it using subprocess / module import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

def test_invalid_strategy():
    result = subprocess.run(
        [sys.executable, "scripts/orchestrator.py", "--enable-exec-from-workspace", "--workdir", ".", "--prd-file", "dummy.md", "--coder-session-strategy", "invalid-strategy"],
        capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "argument --coder-session-strategy: invalid choice: 'invalid-strategy'" in result.stderr

def test_missing_workdir():
    result = subprocess.run(
        [sys.executable, "scripts/orchestrator.py", "--enable-exec-from-workspace", "--prd-file", "dummy.md"],
        capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "the following arguments are required: --workdir" in result.stderr

@patch('orchestrator.teardown_coder_session')
@patch('orchestrator.subprocess.run')
@patch('orchestrator.safe_git_checkout')
@patch('orchestrator.glob.glob')
@patch('orchestrator.os.path.exists')
@patch('orchestrator.set_pr_status')
@patch('fcntl.flock')
@patch('shutil.copytree')
@patch('orchestrator.open')
@patch('git_utils.check_git_boundary')
def test_always_strategy(mock_check_git, mock_open, mock_copytree, mock_flock, mock_set_pr_status, mock_exists, mock_glob, mock_safe_checkout, mock_run, mock_teardown):
    os.environ["SDLC_BYPASS_BRANCH_CHECK"] = "1"
    os.environ["SDLC_TEST_MODE"] = "true"
    import orchestrator
    
    mock_exists.return_value = True
    mock_glob.return_value = ["dummy_pr.md"]
    mock_open.return_value.__enter__.return_value.read.return_value = "status: in_progress\n"
    
    def mock_run_impl(*args, **kwargs):
        if "status" in args[0] and "--porcelain" in args[0]:
            return MagicMock(stdout="", returncode=0)
        if "rev-parse" in args[0] and "--abbrev-ref" in args[0]:
            return MagicMock(stdout="master\n", returncode=0)
        if "spawn_coder.py" in args[0]:
            return MagicMock(returncode=1) # Fail once to trigger State 5 path
        return MagicMock(returncode=0)
    mock_run.side_effect = mock_run_impl
    
    with patch('sys.argv', ['orchestrator.py', '--force-replan', 'true', '--enable-exec-from-workspace', '--workdir', '.', '--prd-file', 'dummy.md', '--channel', 'test', '--coder-session-strategy', 'always', '--max-prs-to-process', '1']):
        try:
            orchestrator.main()
        except SystemExit:
            pass
            
    mock_teardown.assert_called_with(os.path.abspath("."))
    
@patch('orchestrator.teardown_coder_session')
@patch('orchestrator.subprocess.run')
@patch('orchestrator.safe_git_checkout')
@patch('orchestrator.glob.glob')
@patch('orchestrator.os.path.exists')
@patch('orchestrator.set_pr_status')
@patch('fcntl.flock')
@patch('shutil.copytree')
@patch('orchestrator.open')
@patch('git_utils.check_git_boundary')
def test_per_pr_strategy(mock_check_git, mock_open, mock_copytree, mock_flock, mock_set_pr_status, mock_exists, mock_glob, mock_safe_checkout, mock_run, mock_teardown):
    os.environ["SDLC_BYPASS_BRANCH_CHECK"] = "1"
    os.environ["SDLC_TEST_MODE"] = "true"
    import orchestrator
    
    mock_exists.return_value = True
    mock_glob.return_value = ["dummy_pr.md"]
    mock_open.return_value.__enter__.return_value.read.return_value = "status: in_progress\n"
    
    def mock_run_impl(*args, **kwargs):
        if "status" in args[0] and "--porcelain" in args[0]:
            return MagicMock(stdout="", returncode=0)
        if "rev-parse" in args[0] and "--abbrev-ref" in args[0]:
            return MagicMock(stdout="master\n", returncode=0)
        return MagicMock(returncode=0)
    mock_run.side_effect = mock_run_impl

    with patch('sys.argv', ['orchestrator.py', '--force-replan', 'true', '--enable-exec-from-workspace', '--workdir', '.', '--prd-file', 'dummy.md', '--channel', 'test', '--coder-session-strategy', 'per-pr', '--max-prs-to-process', '1']):
        try:
            orchestrator.main()
        except SystemExit:
            pass
            
    mock_teardown.assert_called_with(os.path.abspath("."))

@patch('orchestrator.teardown_coder_session')
@patch('orchestrator.subprocess.run')
@patch('orchestrator.safe_git_checkout')
@patch('orchestrator.glob.glob')
@patch('orchestrator.os.path.exists')
@patch('orchestrator.set_pr_status')
@patch('fcntl.flock')
@patch('shutil.copytree')
@patch('orchestrator.open')
@patch('git_utils.check_git_boundary')
def test_on_escalation_strategy(mock_check_git, mock_open, mock_copytree, mock_flock, mock_set_pr_status, mock_exists, mock_glob, mock_safe_checkout, mock_run, mock_teardown):
    os.environ["SDLC_BYPASS_BRANCH_CHECK"] = "1"
    os.environ["SDLC_TEST_MODE"] = "true"
    import orchestrator
    
    mock_exists.return_value = True
    mock_glob.return_value = ["dummy_pr.md"]
    mock_open.return_value.__enter__.return_value.read.return_value = "status: in_progress\n"
    
    def mock_run_impl(*args, **kwargs):
        if "status" in args[0] and "--porcelain" in args[0]:
            return MagicMock(stdout="", returncode=0)
        if "rev-parse" in args[0] and "--abbrev-ref" in args[0]:
            return MagicMock(stdout="master\n", returncode=0)
        if "spawn_coder.py" in args[0]:
            return MagicMock(returncode=1) # Fail to trigger escalation
        return MagicMock(returncode=0)
        
    mock_run.side_effect = mock_run_impl
    
    with patch('sys.argv', ['orchestrator.py', '--force-replan', 'true', '--enable-exec-from-workspace', '--workdir', '.', '--prd-file', 'dummy.md', '--channel', 'test', '--coder-session-strategy', 'on-escalation', '--max-prs-to-process', '1']):
        try:
            orchestrator.main()
        except SystemExit:
            pass
            
    mock_teardown.assert_called_with(os.path.abspath("."))
