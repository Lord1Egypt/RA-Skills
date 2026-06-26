import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add scripts directory to path to allow imports inside orchestrator.py
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import scripts.orchestrator as orchestrator
from utils.singleton_lock import ConcurrentExecutionError

class TestMasterBranchGuardrail(unittest.TestCase):
    @patch('scripts.orchestrator.subprocess.run')
    def test_non_master_branch_exits(self, mock_run):
        def mock_subprocess_run(*args, **kwargs):
            cmd = args[0]
            if isinstance(cmd, list) and cmd == ["git", "branch", "--show-current"]:
                return MagicMock(stdout="feature/test-branch\n")
            if isinstance(cmd, list) and cmd == ["git", "rev-parse", "--show-toplevel"]:
                class Ret:
                    stdout = os.path.abspath(".")
                return Ret()
            if isinstance(cmd, list) and cmd == ["git", "status", "--porcelain"]:
                return MagicMock(stdout="")
            return MagicMock(returncode=0)

        mock_run.side_effect = mock_subprocess_run

        env = os.environ.copy()
        if "SDLC_BYPASS_BRANCH_CHECK" in env:
            del env["SDLC_BYPASS_BRANCH_CHECK"]

        with patch.dict(os.environ, env, clear=True):
            test_args = ["orchestrator.py", "--force-replan", "true", "--enable-exec-from-workspace", "--workdir", ".", "--prd-file", "dummy.md"]
            with patch.object(sys, 'argv', test_args):
                with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
                    with patch('sys.exit') as mock_exit:
                        mock_exit.side_effect = SystemExit(1)
                        with self.assertRaises(SystemExit) as cm:
                            orchestrator.main()
        
                        self.assertEqual(cm.exception.code, 1)
        
                        # Check the print output
                        print_calls = mock_stdout.write.call_args_list
                        output_str = "".join([call[0][0] for call in print_calls])
                        self.assertIn("Orchestrator must be started from the master", output_str)

    @patch('scripts.orchestrator.subprocess.run')
    @patch('scripts.orchestrator.fcntl.flock')
    def test_master_branch_passes(self, mock_flock, mock_run):
        def mock_subprocess_run(*args, **kwargs):
            cmd = args[0]
            if isinstance(cmd, list) and cmd == ["git", "branch", "--show-current"]:
                return MagicMock(stdout="master\n")
            if isinstance(cmd, list) and cmd == ["git", "status", "--porcelain"]:
                return MagicMock(stdout="")
            if isinstance(cmd, list) and cmd == ["git", "rev-parse", "--show-toplevel"]:
                class Ret:
                    stdout = os.path.abspath(".")
                return Ret()
            return MagicMock(returncode=0)

        mock_run.side_effect = mock_subprocess_run
        mock_flock.side_effect = BlockingIOError("Simulated lock error to stop execution gracefully after branch check")

        env = os.environ.copy()
        if "SDLC_BYPASS_BRANCH_CHECK" in env:
            del env["SDLC_BYPASS_BRANCH_CHECK"]

        test_args = ["orchestrator.py", "--force-replan", "true", "--enable-exec-from-workspace", "--workdir", ".", "--prd-file", "dummy.md"]

        with patch.dict(os.environ, env, clear=True):
            with patch.object(sys, 'argv', test_args):
                with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
                    with patch('sys.exit') as mock_exit:
                        mock_exit.side_effect = SystemExit(1)
                        with self.assertRaises(SystemExit) as cm:
                            orchestrator.main()

                        # It should exit due to BlockingIOError (which prints "[FATAL] Another SDLC pipeline is currently running..."), NOT the branch check.
                        print_calls = mock_stdout.write.call_args_list
                        output_str = "".join([call[0][0] for call in print_calls])
                        self.assertNotIn("Orchestrator must be started from the master branch", output_str)
                        self.assertIn("Another SDLC pipeline is currently running", output_str)

if __name__ == '__main__':
    unittest.main()
