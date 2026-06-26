import os
import subprocess
import tempfile
import time
import fcntl

import pytest

@pytest.fixture
def clean_cwd():
    orig_cwd = os.getcwd()
    yield
    os.chdir(orig_cwd)

def test_cleanup_quarantine(clean_cwd):
    with tempfile.TemporaryDirectory() as td:
        os.chdir(td)
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "config", "user.name", "Test"], check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "commit", "--allow-empty", "-m", "init"], check=True)
        
        # Create a branch and a dirty file
        subprocess.run(["git", "checkout", "-b", "feature/toxic_branch"], check=True)
        with open("dirty.txt", "w") as f:
            f.write("bad code")
        
        # Create dummy locks
        with open(".sdlc_repo.lock", "w") as f:
            f.write("locked")
        with open(".coder_session", "w") as f:
            f.write("session123")
            
        dummy_lock_1 = os.path.join(td, "dummy1.lock")
        dummy_lock_2 = os.path.join(td, "dummy2.lock")
        with open(dummy_lock_1, "w") as f:
            f.write("locked")
        with open(dummy_lock_2, "w") as f:
            f.write("locked")
            
        import json
        with open(".sdlc_lock_manifest.json", "w") as f:
            json.dump({"locks": [dummy_lock_1, dummy_lock_2]}, f)
            
        # Run orchestrator cleanup
        orchestrator_path = "/root/.openclaw/workspace/projects/leio-sdlc/scripts/orchestrator.py"
        res = subprocess.run([
            "python3", orchestrator_path, 
            "--workdir", td, 
            "--prd-file", "dummy.md",
            "--cleanup",
            "--enable-exec-from-workspace"
        ], capture_output=True, text=True)
        
        assert res.returncode == 0, f"Cleanup failed: {res.stderr}"
        
        # Assertions
        # 1. Master is checked out
        current_branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
        assert current_branch == "master", f"Branch is {current_branch}, expected master"
        
        # 2. Toxic branch was renamed
        branches = subprocess.run(["git", "branch"], capture_output=True, text=True).stdout
        assert "feature/toxic_branch_crashed_" in branches
        assert "feature/toxic_branch " not in branches
        
        # 3. Locks deleted
        assert not os.path.exists(".sdlc_repo.lock")
        assert not os.path.exists(".coder_session")
        assert not os.path.exists(dummy_lock_1)
        assert not os.path.exists(dummy_lock_2)
        assert not os.path.exists(".sdlc_lock_manifest.json")

def test_cleanup_lock_blocked(clean_cwd):
    with tempfile.TemporaryDirectory() as td:
        os.chdir(td)
        lock_path = os.path.join(td, ".sdlc_repo.lock")
        f = open(lock_path, "w")
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        
        orchestrator_path = "/root/.openclaw/workspace/projects/leio-sdlc/scripts/orchestrator.py"
        res = subprocess.run([
            "python3", orchestrator_path, 
            "--workdir", td, 
            "--prd-file", "dummy.md",
            "--cleanup",
            "--enable-exec-from-workspace"
        ], capture_output=True, text=True)
        
        assert res.returncode == 1
        assert "[FATAL_LOCK]" in res.stdout
        
if __name__ == "__main__":
    # Mocking the fixture behavior for direct script execution
    import contextlib
    @contextlib.contextmanager
    def mock_clean_cwd():
        orig_cwd = os.getcwd()
        try:
            yield
        finally:
            os.chdir(orig_cwd)

    with mock_clean_cwd():
        test_cleanup_quarantine(None)
        test_cleanup_lock_blocked(None)
    print("Cleanup tests passed.")
