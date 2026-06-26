#!/usr/bin/env python3
import os
import sys
import shutil
import unittest
import subprocess
from pathlib import Path

# Absolute path to the SDLC framework directory (leio-sdlc root)
SDLC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestScaffolding(unittest.TestCase):
    def setUp(self):
        # Create a clean mock workspace for each test
        self.mock_workdir = os.path.join(SDLC_DIR, "tests", "mock_scaffold_project")
        if os.path.exists(self.mock_workdir):
            shutil.rmtree(self.mock_workdir)
        os.makedirs(self.mock_workdir)
        
        # Create a dummy PRD file inside the mock workdir
        self.prd_file = os.path.join(self.mock_workdir, "dummy_prd.md")
        with open(self.prd_file, "w") as f:
            f.write("# Dummy PRD")
            
    def tearDown(self):
        # Clean up mock workdir
        if os.path.exists(self.mock_workdir):
            shutil.rmtree(self.mock_workdir)

    def test_scaffolding_files_inherited(self):
        # Run spawn_planner.py in the mock workdir
        # We must set SDLC_TEST_MODE=true to skip the real agent call
        # and ensure the script doesn't actually try to talk to OpenClaw
        env = os.environ.copy()
        env["SDLC_TEST_MODE"] = "true"
        
        planner_script = os.path.join(SDLC_DIR, "scripts", "spawn_planner.py")
        
        # Command: python3 scripts/spawn_planner.py --prd-file dummy_prd.md --workdir .
        result = subprocess.run(
            [sys.executable, planner_script, "--prd-file", "dummy_prd.md", "--workdir", "."],
            cwd=self.mock_workdir,
            env=env,
            capture_output=True,
            text=True
        )
        
        # Check that the script ran successfully
        self.assertEqual(result.returncode, 0, f"Planner script failed: {result.stderr}")
        
        # Verify that the scaffolding files were created
        self.assertTrue(os.path.exists(os.path.join(self.mock_workdir, ".sdlc_guardrail")), ".sdlc_guardrail not scaffolded")
        self.assertTrue(os.path.exists(os.path.join(self.mock_workdir, ".gitignore")), ".gitignore not scaffolded")
        self.assertTrue(os.path.exists(os.path.join(self.mock_workdir, ".release_ignore")), ".release_ignore not scaffolded")
        
        # Check that the inherited .sdlc_guardrail contains something from the source
        with open(os.path.join(self.mock_workdir, ".sdlc_guardrail"), "r") as f:
            content = f.read()
            self.assertIn(".sdlc_runs/", content)

if __name__ == "__main__":
    unittest.main()
