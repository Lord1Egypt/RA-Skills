import unittest
import subprocess
import tempfile
import os
import shutil
import glob

class TestDeployBackup(unittest.TestCase):
    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.pm_skill_dir = os.path.join(self.project_root, "skills", "pm-skill")
        self.auditor_skill_dir = os.path.join(self.project_root, "skills", "leio-auditor")
        
    def test_sdlc_deploy_creates_backup(self):
        with tempfile.TemporaryDirectory() as tempdir:
            mock_home = os.path.join(tempdir, "home")
            os.makedirs(mock_home, exist_ok=True)
            
            env = os.environ.copy()
            env["HOME_MOCK"] = mock_home
            
            deploy_script = os.path.join(self.project_root, "deploy.sh")
            res1 = subprocess.run(["bash", deploy_script, "--no-restart"], env=env, cwd=self.project_root, capture_output=True, text=True)
            self.assertEqual(res1.returncode, 0, f"First deploy failed: {res1.stderr}\n{res1.stdout}")
            
            res2 = subprocess.run(["bash", deploy_script, "--no-restart"], env=env, cwd=self.project_root, capture_output=True, text=True)
            self.assertEqual(res2.returncode, 0, f"Second deploy failed: {res2.stderr}\n{res2.stdout}")
            
            releases_dir = os.path.join(mock_home, ".openclaw", ".releases", "leio-sdlc")
            self.assertTrue(os.path.exists(releases_dir), "Releases dir not created for leio-sdlc")
            
            backups = glob.glob(os.path.join(releases_dir, "backup_*.tar.gz"))
            self.assertTrue(len(backups) >= 1, "Backup tar.gz file not found after second deployment for leio-sdlc")
            
    def test_pm_skill_deploy_creates_backup(self):
        with tempfile.TemporaryDirectory() as tempdir:
            mock_home = os.path.join(tempdir, "home")
            os.makedirs(mock_home, exist_ok=True)
            
            env = os.environ.copy()
            env["HOME_MOCK"] = mock_home
            
            # The deploy scripts rely on being run from the monorepo root
            # so we run it from project_root.
            # To avoid actually restarting gateway, we pass --no-restart
            
            # Deploy once
            deploy_script = os.path.join(self.pm_skill_dir, "deploy.sh")
            res1 = subprocess.run(["bash", deploy_script, "--no-restart"], env=env, cwd=self.project_root, capture_output=True, text=True)
            self.assertEqual(res1.returncode, 0, f"First deploy failed: {res1.stderr}\n{res1.stdout}")
            
            # Deploy twice to trigger backup creation
            res2 = subprocess.run(["bash", deploy_script, "--no-restart"], env=env, cwd=self.project_root, capture_output=True, text=True)
            self.assertEqual(res2.returncode, 0, f"Second deploy failed: {res2.stderr}\n{res2.stdout}")
            
            releases_dir = os.path.join(mock_home, ".openclaw", ".releases", "pm-skill")
            self.assertTrue(os.path.exists(releases_dir), "Releases dir not created")
            
            backups = glob.glob(os.path.join(releases_dir, "backup_*.tar.gz"))
            self.assertTrue(len(backups) >= 1, "Backup tar.gz file not found after second deployment")
            
            # Also verify that agent_driver.py is inside the deployed script folder
            prod_dir = os.path.join(mock_home, ".openclaw", "skills", "pm-skill")
            self.assertTrue(os.path.exists(os.path.join(prod_dir, "scripts", "agent_driver.py")), "agent_driver.py not bundled properly")

    