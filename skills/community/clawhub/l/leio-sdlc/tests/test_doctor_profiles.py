import os
import tempfile
import subprocess
from pathlib import Path
from scripts.doctor import check_vcs, apply_overlay

def test_doctor_apply_skill_profile():
    with tempfile.TemporaryDirectory() as tmpdir:
        overlay = Path(tmpdir) / "overlay"
        overlay.mkdir(parents=True)
        with open(overlay / "deploy.sh", "w") as f:
            f.write("echo 'ok'")
        with open(overlay / "SKILL.md", "w") as f:
            f.write("# SKILL")
        with open(overlay / ".release_ignore.append", "w") as f:
            f.write("tests/")
            
        target = Path(tmpdir) / "target"
        target.mkdir()
        
        apply_overlay(target, overlay, check_only=False)
        
        assert (target / "deploy.sh").exists()
        assert (target / "SKILL.md").exists()
        assert (target / ".release_ignore").exists()
        
        with open(target / ".release_ignore", "r") as f:
            assert "tests/" in f.read()

def test_doctor_enforce_git_lock():
    # Since enforce_git_lock is handled in main, we can invoke doctor as a subprocess
    # or just test the logic directly
    import subprocess
    import sys
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create the hook template so doctor can find it
        # We need to run doctor.py --fix --enforce-git-lock on this tmpdir
        target = Path(tmpdir) / "target"
        target.mkdir()
        
        doctor_script = Path(__file__).parent.parent / "scripts" / "doctor.py"
        
        # We need to run python script
        res = subprocess.run([sys.executable, str(doctor_script), str(target), "--fix", "--enforce-git-lock"], capture_output=True)
        
        assert res.returncode == 0
        assert (target / ".git" / "hooks" / "pre-commit").exists()
        assert os.access(target / ".git" / "hooks" / "pre-commit", os.X_OK)
