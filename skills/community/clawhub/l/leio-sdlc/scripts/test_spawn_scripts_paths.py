import unittest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spawn_coder

class TestSpawnScriptsPaths(unittest.TestCase):
    @patch('builtins.open')
    @patch('spawn_coder.openclaw_agent_call')
    def test_spawn_coder_playbook_path(self, mock_agent_call, mock_open):
        from scripts import spawn_coder
        
        # Inject fake arguments
        test_args = ["spawn_coder.py", "--pr-file", "dummy.md", "--prd-file", "dummy.md", "--workdir", "/tmp/fake_workdir", "--global-dir", "/tmp/fake_global_dir"]
        with patch.object(sys, 'argv', test_args):
            try:
                spawn_coder.main()
            except Exception:
                pass # Ignore exit or side effects, we only care about the open() calls
                
        # Assert that builtins.open was NOT called with the fake global dir for playbooks
        for call in mock_open.call_args_list:
            path = call[0][0]
            if "playbook" in path:
                self.assertNotIn("/tmp/fake_global_dir", path, f"Red Status: Attempted to read playbook from fake global dir: {path}")

if __name__ == '__main__':
    unittest.main()
