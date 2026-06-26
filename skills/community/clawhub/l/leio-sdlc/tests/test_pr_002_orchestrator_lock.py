import os
import subprocess
import time
import unittest

class TestOrchestratorLock(unittest.TestCase):
    def test_concurrent_orchestrator_blocked(self):
        workdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        orchestrator_path = os.path.join(workdir, "scripts", "orchestrator.py")
        
        # We start a background orchestrator that sleeps
        env = os.environ.copy()
        env["SDLC_BYPASS_BRANCH_CHECK"] = "1"
        env["SDLC_TEST_MODE"] = "true"
        
        # Start first instance
        proc1 = subprocess.Popen(
            ["python3", orchestrator_path, "--force-replan", "true", "--enable-exec-from-workspace", "--workdir", workdir, "--prd-file", "dummy", "--test-sleep"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            cwd=workdir
        )
        
        # Give it a moment to acquire the lock
        time.sleep(0.5)
        
        # Start second instance
        proc2 = subprocess.Popen(
            ["python3", orchestrator_path, "--force-replan", "true", "--enable-exec-from-workspace", "--workdir", workdir, "--prd-file", "dummy"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            cwd=workdir
        )
        
        stdout2, stderr2 = proc2.communicate()
        output = stdout2.decode() + stderr2.decode()
        
        # Wait for the first one to finish
        proc1.terminate()
        stdout1, stderr1 = proc1.communicate()
        
        self.assertEqual(proc2.returncode, 1)
        self.assertIn("[FATAL] Another SDLC pipeline is currently running. Concurrent execution is blocked.", output)

if __name__ == "__main__":
    unittest.main()
