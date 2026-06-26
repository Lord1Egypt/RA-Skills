import unittest
import os
import sys
import tempfile
import subprocess
import shutil

class TestReviewerContextIsolation(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.script_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'spawn_reviewer.py')
        
        self.pr_file = os.path.join(self.temp_dir, "PR_003.md")
        with open(self.pr_file, "w") as f:
            f.write("# Dummy PR\n")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_context_isolation_headers_exist(self):
        # We run the script in test mode to just capture the prompt it generates.
        env = os.environ.copy()
        env["SDLC_TEST_MODE"] = "true"
        
        cmd = [
            sys.executable, self.script_path,
            "--pr-file", self.pr_file,
            "--diff-target", "HEAD",
            "--workdir", self.temp_dir,
            "--global-dir", self.temp_dir,
            "--override-diff-file", "dummy.diff"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=self.temp_dir)
        
        # In test mode, it writes tests/tool_calls.log with the task_string
        log_path = os.path.join(self.temp_dir, "tests", "tool_calls.log")
        self.assertTrue(os.path.exists(log_path), "tool_calls.log was not created")
        
        with open(log_path, "r") as f:
            prompt_content = f.read()
            
        # Verify the headers exist and are separated
        self.assertIn("--- TARGET FOR REVIEW (CURRENT CODE CHANGES) ---", prompt_content)
        self.assertIn("--- READ-ONLY REFERENCE HISTORY (PREVIOUSLY MERGED) ---", prompt_content)
        self.assertIn("strictly read-only reference material", prompt_content)
        self.assertIn("All security checks, redlines, and logic validations MUST be strictly applied ONLY to this file", prompt_content)

if __name__ == '__main__':
    unittest.main()
