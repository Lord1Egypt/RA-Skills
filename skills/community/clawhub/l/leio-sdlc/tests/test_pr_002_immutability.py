import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Force scripts into path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
import orchestrator

class TestPR002Immutability(unittest.TestCase):
    def setUp(self):
        os.environ["SDLC_BYPASS_BRANCH_CHECK"] = "1"
        os.environ["SDLC_TEST_MODE"] = "true"

    @patch('orchestrator.subprocess.run')
    def test_set_pr_status_no_git_tracking(self, mock_run):
        # PRD 1060: Verification that set_pr_status no longer calls git add/commit
        pr_file = "/tmp/dummy_pr.md"
        with open(pr_file, "w") as f:
            f.write("status: open\nslice_depth: 1")
    
        try:
            orchestrator.set_pr_status(pr_file, "in_progress")
    
            # Check that subprocess.run was NOT called with git add or commit
            for call in mock_run.call_args_list:
                if call and len(call[0]) > 0:
                    cmd = call[0][0]
                    self.assertFalse("git" in cmd and ("add" in cmd or "commit" in cmd))
            
            with open(pr_file, "r") as f:
                self.assertIn("status: in_progress", f.read())
        finally:
            if os.path.exists(pr_file):
                os.remove(pr_file)

if __name__ == '__main__':
    unittest.main()
