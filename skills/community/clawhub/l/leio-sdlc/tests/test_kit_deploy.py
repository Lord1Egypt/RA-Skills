import unittest
import subprocess
import tempfile
import os

class TestKitDeploy(unittest.TestCase):
    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
    def test_kit_deploy_execution_order(self):
        with tempfile.TemporaryDirectory() as tempdir:
            log_file = os.path.join(tempdir, "execution.log")
            
            # Create dummy scripts that will be called
            with open(os.path.join(tempdir, "deploy.sh"), "w") as f:
                f.write(f"#!/bin/bash\necho 'deploy-sdlc' >> {log_file}\n")
            os.chmod(os.path.join(tempdir, "deploy.sh"), 0o755)
            
            os.makedirs(os.path.join(tempdir, "skills", "pm-skill"), exist_ok=True)
            with open(os.path.join(tempdir, "skills", "pm-skill", "deploy.sh"), "w") as f:
                f.write(f"#!/bin/bash\necho 'deploy-pm' >> {log_file}\n")
            os.chmod(os.path.join(tempdir, "skills", "pm-skill", "deploy.sh"), 0o755)
            
            

            # Copy the kit deploy script to the tempdir to run it
            kit_deploy_src = os.path.join(self.project_root, "kit-deploy.sh")
            kit_deploy_dest = os.path.join(tempdir, "kit-deploy.sh")
            with open(kit_deploy_src, "r") as f_src, open(kit_deploy_dest, "w") as f_dest:
                f_dest.write(f_src.read())
            os.chmod(kit_deploy_dest, 0o755)
            
            env = os.environ.copy()
            # Intercept openclaw calls
            env["PATH"] = f"{tempdir}:{env['PATH']}"
            with open(os.path.join(tempdir, "openclaw"), "w") as f:
                f.write(f"#!/bin/bash\necho \"mock-openclaw $*\" >> {log_file}\n")
            os.chmod(os.path.join(tempdir, "openclaw"), 0o755)
            
            # Clear HOME_MOCK so openclaw runs
            if "HOME_MOCK" in env:
                del env["HOME_MOCK"]
                
            subprocess.run(["bash", "kit-deploy.sh"], cwd=tempdir, env=env, capture_output=True, text=True)
            
            self.assertTrue(os.path.exists(log_file), "Execution log was not created")
            with open(log_file, "r") as f:
                lines = f.read().strip().split("\n")
                
            self.assertEqual(len(lines), 3)
            self.assertEqual(lines[0], "deploy-sdlc")
            # The order of pm and auditor might vary depending on glob, but both should be there
            self.assertTrue("deploy-pm" in lines[1:2])
            
            self.assertEqual(lines[2], "mock-openclaw gateway restart")

if __name__ == '__main__':
    unittest.main()
