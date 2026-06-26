import os
import subprocess
import json
import shutil
import time
import fcntl

def test_lock_acquisition_and_manifest():
    test_dir = os.path.abspath("tests/test_lock_run")
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    # Mock PRD with Affected_Projects
    prd_path = os.path.join(test_dir, "PRD_TEST.md")
    with open(prd_path, "w") as f:
        f.write("---\nAffected_Projects: [ProjectAlpha, ProjectBeta]\n---\n# Test PRD")
    
    # Copy scripts to test dir or just run from here with mock workdir
    # We need to test the logic inside orchestrator.py
    # Since I'm a "Fat Coder", I'll write a standalone unit test for the logic I just added.
    
    import sys
    sys.path.insert(0, os.path.join(os.getcwd(), "scripts"))
    from orchestrator import parse_affected_projects, acquire_global_locks
    
    print("Testing parse_affected_projects...")
    projects = parse_affected_projects(prd_path)
    assert projects == ["ProjectAlpha", "ProjectBeta"], f"Expected [ProjectAlpha, ProjectBeta], got {projects}"
    print("✅ Parsing successful.")
    
    print("Testing acquire_global_locks...")
    lock_dir = os.path.expanduser("~/.openclaw/workspace/locks")
    if os.path.exists(lock_dir):
        # Clean up existing locks for these names to ensure fresh run
        for p in projects:
            lp = os.path.join(lock_dir, f"{p}.lock")
            if os.path.exists(lp): os.remove(lp)
            
    locks, fds = acquire_global_locks(projects, test_dir)
    assert len(locks) == 2
    assert os.path.exists(os.path.join(test_dir, ".sdlc_lock_manifest.json"))
    
    with open(os.path.join(test_dir, ".sdlc_lock_manifest.json"), "r") as f:
        manifest = json.load(f)
    assert len(manifest["locks"]) == 2
    print("✅ Lock acquisition and manifest creation successful.")
    
    # Test Rollback
    print("Testing rollback...")
    # Create a conflicting lock manually
    conflict_project = "ConflictProj"
    conflict_path = os.path.join(lock_dir, f"{conflict_project}.lock")
    cfd = os.open(conflict_path, os.O_CREAT | os.O_RDWR)
    fcntl.flock(cfd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    
    try:
        # This should fail and exit(1)
        # We wrap in try/except because we expect sys.exit(1)
        acquire_global_locks(["NewProj", conflict_project], test_dir)
    except SystemExit as e:
        assert e.code == 1
        # Check that NewProj.lock was removed (rollback)
        assert not os.path.exists(os.path.join(lock_dir, "NewProj.lock"))
        print("✅ Rollback successful.")
    finally:
        os.close(cfd)
        if os.path.exists(conflict_path): os.remove(conflict_path)

if __name__ == "__main__":
    try:
        test_lock_acquisition_and_manifest()
        print("\nALL LOCK TESTS PASSED")
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
