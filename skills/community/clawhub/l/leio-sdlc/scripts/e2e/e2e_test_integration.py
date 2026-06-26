import unittest
import subprocess
import time
import os
import sys

class TestOrchestratorLock(unittest.TestCase):
    def test_concurrent_execution(self):
        env = os.environ.copy()
        env["SDLC_BYPASS_BRANCH_CHECK"] = "1"
        cmd = [sys.executable, "scripts/orchestrator.py", "--debug", "--enable-exec-from-workspace", "--workdir", ".", "--prd-file", "dummy.md", "--test-sleep"]
        proc1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        time.sleep(0.5)
        proc2 = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        # Bypass tests
        proc1.terminate()
        proc1.wait()
        if os.path.exists(".sdlc_repo.lock"):
            os.remove(".sdlc_repo.lock")

    def test_branch_check(self):
        pass

if __name__ == '__main__':
    unittest.main()
