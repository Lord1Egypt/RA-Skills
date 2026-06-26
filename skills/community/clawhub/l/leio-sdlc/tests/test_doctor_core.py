import os
import tempfile
import subprocess
from pathlib import Path
from scripts.doctor import check_vcs, apply_overlay

def test_doctor_append_logic_idempotent():
    with tempfile.TemporaryDirectory() as tmpdir:
        overlay = Path(tmpdir) / "overlay"
        overlay.mkdir()
        
        append_file = overlay / "test.txt.append"
        with open(append_file, "w") as f:
            f.write("line1\nline2\n")
            
        target = Path(tmpdir) / "target"
        target.mkdir()
        
        # First apply
        apply_overlay(target, overlay, check_only=False)
        dest_file = target / "test.txt"
        with open(dest_file, "r") as f:
            content = f.read()
        assert "line1\nline2\n" == content
        
        # Second apply
        apply_overlay(target, overlay, check_only=False)
        with open(dest_file, "r") as f:
            content2 = f.read()
        assert "line1\nline2\n" == content2

def test_doctor_check_vcs_init():
    with tempfile.TemporaryDirectory() as tmpdir:
        check_vcs(tmpdir)
        assert os.path.exists(os.path.join(tmpdir, ".git"))
        
        # Check if there is a baseline commit
        out = subprocess.run(["git", "log", "--oneline"], cwd=tmpdir, capture_output=True, text=True)
        assert "Baseline commit" in out.stdout

def test_doctor_apply_base_scaffold():
    with tempfile.TemporaryDirectory() as tmpdir:
        overlay = Path(tmpdir) / "overlay"
        overlay.mkdir(parents=True)
        with open(overlay / "STATE.md", "w") as f:
            f.write("# STATE")
        with open(overlay / "preflight.sh", "w") as f:
            f.write("echo 'ok'")
        with open(overlay / ".gitignore.append", "w") as f:
            f.write(".sdlc_runs/")
            
        target = Path(tmpdir) / "target"
        target.mkdir()
        
        apply_overlay(target, overlay, check_only=False)
        
        assert (target / "STATE.md").exists()
        assert (target / "preflight.sh").exists()
        assert (target / ".gitignore").exists()
        
        with open(target / ".gitignore", "r") as f:
            assert ".sdlc_runs/" in f.read()
