import os
import subprocess
import json
import tempfile
import unittest

class TestCreatePrContract(unittest.TestCase):
    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.job_dir = os.path.join(self.workdir, "job_dir")
        os.makedirs(self.job_dir)
        
        # We need TEMPLATES/PR_Contract.md.template in the right place relative to the script
        # The script resolves it as: os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "TEMPLATES", "PR_Contract.md.template")
        # Which points to /root/.openclaw/workspace/projects/leio-sdlc/TEMPLATES/PR_Contract.md.template
        # So we can just call the script directly.
        self.script_path = "/root/.openclaw/workspace/projects/leio-sdlc/scripts/create_pr_contract.py"
        self.config_template_path = "/root/.openclaw/workspace/projects/leio-sdlc/config/sdlc_config.json.template"

    def test_only_scaffold_creates_file_with_header(self):
        cmd = [
            "python3", self.script_path,
            "--only-scaffold",
            "--workdir", self.workdir,
            "--job-dir", self.job_dir,
            "--title", "Test PR"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")
        
        files = os.listdir(self.job_dir)
        self.assertEqual(len(files), 1)
        pr_file = os.path.join(self.job_dir, files[0])
        
        with open(pr_file, "r") as f:
            content = f.read()
            
        self.assertTrue(content.startswith("status: open"))
        self.assertIn("PR-001: Test PR", content)

    def test_config_template_contains_retry_limits(self):
        self.assertTrue(os.path.exists(self.config_template_path))
        with open(self.config_template_path, "r") as f:
            config = json.load(f)
            
        self.assertIn("YELLOW_RETRY_LIMIT", config)
        self.assertEqual(config["YELLOW_RETRY_LIMIT"], 3)
        self.assertIn("RED_RETRY_LIMIT", config)
        self.assertEqual(config["RED_RETRY_LIMIT"], 2)

if __name__ == "__main__":
    unittest.main()
