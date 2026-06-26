import unittest
import subprocess
import tempfile
import os
import glob

class TestDeployExcludes(unittest.TestCase):
    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
    def test_deploy_excludes_tests(self):
        with tempfile.TemporaryDirectory() as tempdir:
            mock_home = os.path.join(tempdir, "home")
            os.makedirs(mock_home, exist_ok=True)
            
            env = os.environ.copy()
            env["HOME_MOCK"] = mock_home
            
            deploy_script = os.path.join(self.project_root, "deploy.sh")
            res = subprocess.run(["bash", deploy_script, "--no-restart"], env=env, cwd=self.project_root, capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, f"Deploy failed: {res.stderr}\n{res.stdout}")
            
            prod_dir = os.path.join(mock_home, ".openclaw", "skills", "leio-sdlc")
            self.assertTrue(os.path.exists(prod_dir), "Prod dir not created")
            self.assertFalse(os.path.exists(os.path.join(prod_dir, "tests")), "tests/ directory should be excluded")

    def test_deploy_excludes_sdlc_runs(self):
        with tempfile.TemporaryDirectory() as tempdir:
            mock_home = os.path.join(tempdir, "home")
            os.makedirs(mock_home, exist_ok=True)
            
            # Create dummy .sdlc and .sdlc_runs
            os.makedirs(os.path.join(self.project_root, ".sdlc"), exist_ok=True)
            os.makedirs(os.path.join(self.project_root, ".sdlc_runs"), exist_ok=True)
            
            # Append .sdlc_runs to .gitignore or .release_ignore to ensure it's excluded if not already,
            # wait, .gitignore usually contains .sdlc_runs/. The PRD says:
            # "NOT copy the `.sdlc/` or `.sdlc_runs/` directories to the destination"
            
            env = os.environ.copy()
            env["HOME_MOCK"] = mock_home
            
            deploy_script = os.path.join(self.project_root, "deploy.sh")
            res = subprocess.run(["bash", deploy_script, "--no-restart"], env=env, cwd=self.project_root, capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, f"Deploy failed: {res.stderr}\n{res.stdout}")
            
            prod_dir = os.path.join(mock_home, ".openclaw", "skills", "leio-sdlc")
            self.assertTrue(os.path.exists(prod_dir), "Prod dir not created")
            self.assertFalse(os.path.exists(os.path.join(prod_dir, ".sdlc")), ".sdlc/ directory should be excluded")
            self.assertFalse(os.path.exists(os.path.join(prod_dir, ".sdlc_runs")), ".sdlc_runs/ directory should be excluded")
            
            # clean up
            try:
                os.rmdir(os.path.join(self.project_root, ".sdlc"))
                os.rmdir(os.path.join(self.project_root, ".sdlc_runs"))
            except:
                pass
