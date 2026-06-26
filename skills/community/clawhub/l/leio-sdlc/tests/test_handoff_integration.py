import sys
import os
import unittest
import subprocess
import json
from unittest.mock import patch, MagicMock

# Force scripts into path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
import orchestrator

class TestOrchestratorHandoffIntegration(unittest.TestCase):
    def setUp(self):
        os.environ["SDLC_BYPASS_BRANCH_CHECK"] = "1"
        os.environ["SDLC_TEST_MODE"] = "true"
        self.orig_parse = orchestrator.parse_affected_projects
        orchestrator.parse_affected_projects = lambda x: []
        self.orig_validate = orchestrator.validate_prd_is_committed
        orchestrator.validate_prd_is_committed = lambda x, y: True

    def tearDown(self):
        orchestrator.parse_affected_projects = self.orig_parse
        orchestrator.validate_prd_is_committed = self.orig_validate

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    @patch('subprocess.run')
    @patch('os.path.exists')
    @patch('builtins.print')
    @patch('os.chdir')
    @patch('os.open', return_value=99)
    @patch('fcntl.flock')
    @patch('git_utils.check_git_boundary')
    def test_dirty_workspace(self, mock_check, mock_flock, mock_open, mock_chdir, mock_print, mock_exists, mock_run, mock_exit, mock_args):
        args = MagicMock()
        args.workdir = "/dummy"
        args.prd_file = "dummy.md"
        args.cleanup = False
        args.enable_exec_from_workspace = True
        args.test_sleep = False
        args.global_dir = None
        args.channel = 'slack:C123'
        mock_args.return_value = args

        mock_exists.side_effect = lambda path: True
        
        def mock_run_logic(cmd, *a, **k):
            res = MagicMock()
            if "branch" in cmd and "--show-current" in cmd:
                res.stdout = "master\n"
            elif "status" in cmd and "--porcelain" in cmd:
                # Return dirty
                res.stdout = " M file.txt\n"
            else:
                res.stdout = ""
            res.returncode = 0
            return res

        mock_run.side_effect = mock_run_logic
        mock_exit.side_effect = SystemExit(1)

        try:
            orchestrator.main()
        except SystemExit:
            pass
        
        # Check for the expected print call. 
        # Since we're in the same turn and builtins.print is patched at the same level, 
        # it should capture.
        any_match = any("[FATAL] Dirty Git Workspace detected!" in str(call) for call in mock_print.call_args_list)
        self.assertTrue(any_match, f"Expected print not found in {mock_print.call_args_list}")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    @patch('subprocess.run')
    @patch('os.path.exists')
    @patch('glob.glob')
    @patch('builtins.print')
    @patch('os.chdir')
    @patch('os.open', return_value=99)
    @patch('fcntl.flock')
    @patch('git_utils.check_git_boundary')
    def test_planner_failure(self, mock_check, mock_flock, mock_open, mock_chdir, mock_print, mock_glob, mock_exists, mock_run, mock_exit, mock_args):
        args = MagicMock()
        args.workdir = "/dummy"
        args.prd_file = "dummy.md"
        args.job_dir = "docs/PRs/dummy"
        args.force_replan = False
        args.channel = "slack:C123"
        args.notify_target = None
        args.cleanup = False
        args.enable_exec_from_workspace = True
        args.test_sleep = False
        args.global_dir = None
        args.channel = 'slack:C123'
        mock_args.return_value = args
        
        mock_exists.side_effect = lambda path: True if path in ["/dummy", "dummy.md"] else False
        
        def mock_run_logic(cmd, *a, **k):
            res = MagicMock()
            if "branch" in cmd and "--show-current" in cmd:
                res.stdout = "master\n"
            elif any("spawn_planner.py" in str(c) for c in cmd):
                res.returncode = 1
                return res # Fail planner
            else:
                res.stdout = ""
            res.returncode = 0
            return res

        mock_run.side_effect = mock_run_logic
        mock_exit.side_effect = SystemExit(1)

        try:
            orchestrator.main()
        except SystemExit:
            pass
            
        any_match = any("[FATAL] Planner failed" in str(call) for call in mock_print.call_args_list)
        self.assertTrue(any_match, f"Expected print not found in {mock_print.call_args_list}")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    @patch('subprocess.run')
    @patch('os.path.exists')
    @patch('glob.glob')
    @patch('builtins.print')
    @patch('os.chdir')
    @patch('os.open', return_value=99)
    @patch('fcntl.flock')
    @patch('git_utils.check_git_boundary')
    def test_queue_empty(self, mock_check, mock_flock, mock_open, mock_chdir, mock_print, mock_glob, mock_exists, mock_run, mock_exit, mock_args):
        args = MagicMock()
        args.workdir = "/dummy"
        args.prd_file = "dummy.md"
        args.job_dir = "docs/PRs/dummy"
        args.force_replan = False
        args.channel = "slack:C123"
        args.notify_target = None
        args.max_prs_to_process = 0
        args.coder_session_strategy = "on-escalation"
        args.cleanup = False
        args.enable_exec_from_workspace = True
        args.test_sleep = False
        args.global_dir = None
        args.channel = 'slack:C123'
        mock_args.return_value = args
        
        mock_exists.return_value = True
        mock_glob.return_value = ["/dummy/.sdlc_runs/dummy/PR_001.md"]
        
        def mock_run_logic(cmd, **kwargs):
            res = MagicMock()
            if "branch" in cmd and "--show-current" in cmd:
                res.stdout = "master\n"
            elif cmd == ["git", "status", "--porcelain"]:
                res.stdout = ""
            elif any("get_next_pr.py" in str(c) for c in cmd):
                res.stdout = "[QUEUE_EMPTY]"
            else:
                res.stdout = ""
            res.returncode = 0
            return res
            
        mock_run.side_effect = mock_run_logic
        mock_exit.side_effect = SystemExit(0)
        
        orig_open = open
        def m_open_side_effect(path, *a, **k):
             if ".md" in str(path):
                 m = MagicMock()
                 m.__enter__.return_value.read.return_value = 'status: closed\n'
                 return m
             return orig_open(path, *a, **k)

        with patch('builtins.open', side_effect=m_open_side_effect):
            try:
                orchestrator.main()
            except SystemExit:
                pass
                
        any_match = any("[ACTION REQUIRED FOR MANAGER] UAT Failed" in str(call) for call in mock_print.call_args_list)
        self.assertTrue(any_match, f"Expected print not found in {mock_print.call_args_list}")

if __name__ == '__main__':
    unittest.main()
