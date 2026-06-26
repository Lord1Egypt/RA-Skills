import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

class TestPathDecoupling(unittest.TestCase):

    @patch("agent_driver.open", create=True)
    def test_spawn_scripts_template_resolution(self, mock_open):
        from agent_driver import build_prompt, RUNTIME_DIR
        build_prompt("planner")
        
        # SDLC_ROOT is os.path.dirname(RUNTIME_DIR)
        sdlc_root = os.path.dirname(RUNTIME_DIR)
        expected_global_config = os.path.join(sdlc_root, "config", "prompts.json")
        
        # Check if calls to open contain the expected global absolute path
        found_global = False
        for call in mock_open.call_args_list:
            path_arg = call[0][0]
            if path_arg == expected_global_config:
                found_global = True
            self.assertTrue(os.path.isabs(path_arg), f"Path {path_arg} is not absolute")
        
        self.assertTrue(found_global, f"Did not find expected global config path: {expected_global_config}")

    @patch("spawn_planner.os.path.isfile", return_value=True)
    @patch("spawn_planner.os.path.getsize", return_value=100)
    @patch("spawn_planner.build_prompt", return_value="mock prompt")
    @patch("spawn_planner.invoke_agent")
    @patch("spawn_planner.open", create=True)
    @patch("spawn_planner.os.makedirs")
    @patch("sys.argv", ["spawn_planner.py", "--prd-file", "dummy.md", "--workdir", ".", "--run-dir", "/tmp/run"])
    def test_spawn_scripts_output_isolation(self, mock_makedirs, mock_open, mock_invoke, mock_build, mock_getsize, mock_isfile):
        from spawn_planner import main
        try:
            main()
        except SystemExit:
            pass
        # Assert that files are written to run_dir
        for call in mock_open.call_args_list:
            path_arg = call[0][0]
            mode_arg = call[0][1] if len(call[0]) > 1 else 'r'
            if mode_arg == 'w' and "PR_Slice" in path_arg:
                self.assertTrue(path_arg.startswith("/tmp/run"), f"Output {path_arg} is not in run_dir")

if __name__ == "__main__":
    unittest.main()
