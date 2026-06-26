import sys
import os
import unittest
import subprocess

class TestDebugCLI(unittest.TestCase):
    def setUp(self):
        self.orchestrator_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "orchestrator.py"))

    def test_debug_flag_produces_trace_output(self):
        # We expect a debug print (like "DEBUG: Workdir:") if --debug is enabled.
        # We also pass --enable-exec-from-workspace to bypass the directory check.
        cmd = [
            sys.executable, self.orchestrator_path, 
            "--force-replan", "true", "--workdir", ".", 
            "--prd-file", "missing.md",
            "--enable-exec-from-workspace",
            "--debug"
        ]
        
        env = os.environ.copy()
        if "SDLC_BYPASS_BRANCH_CHECK" in env:
            del env["SDLC_BYPASS_BRANCH_CHECK"]

        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        
        # It should NOT complain about unrecognized arguments.
        self.assertNotIn("unrecognized arguments: --debug", result.stderr)
        
        # It should produce the debug dlog trace.
        combined_output = result.stdout + result.stderr
        self.assertIn("DEBUG", combined_output)

    def test_no_debug_flag_is_silent(self):
        # Without --debug, the dlog trace should be silent.
        cmd = [
            sys.executable, self.orchestrator_path, 
            "--force-replan", "true", "--workdir", ".", 
            "--prd-file", "missing.md",
            "--enable-exec-from-workspace"
        ]
        
        env = os.environ.copy()
        if "SDLC_BYPASS_BRANCH_CHECK" in env:
            del env["SDLC_BYPASS_BRANCH_CHECK"]

        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        
        combined_output = result.stdout + result.stderr
        self.assertNotIn("DEBUG:", combined_output)

if __name__ == "__main__":
    unittest.main()
