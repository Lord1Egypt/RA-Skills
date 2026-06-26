import sys
import subprocess
import pytest
from pathlib import Path
import os

def test_orchestrator_fail_fast_on_non_compliant_project(tmp_path):
    workdir = tmp_path / "workdir"
    workdir.mkdir()
    os.system(f"git init {workdir}")
    # Run orchestrator, doctor should fail because no templates exist
    orch_script = Path(__file__).parent.parent / "scripts" / "orchestrator.py"
    
    # We will invoke orchestrator directly and check stderr/stdout
    res = subprocess.run([sys.executable, str(orch_script), "--workdir", str(workdir), "--prd-file", "PRD.md", "--channel", "test", "--force-replan", "false", "--enable-exec-from-workspace"], capture_output=True, text=True, env={**os.environ, "SDLC_TEST_MODE": "true"})
    
    assert res.returncode != 0
    assert "Project is not SDLC compliant" in res.stdout or "Project is not SDLC compliant" in res.stderr

def test_orchestrator_proceeds_on_compliant_project(tmp_path):
    workdir = tmp_path / "workdir"
    workdir.mkdir()
    os.system(f"git init {workdir}")
    
    # Needs a baseline commit or git init will complain about branches
    subprocess.run(["git", "commit", "--allow-empty", "-m", "init"], cwd=str(workdir))
    
    # Need to manually create the mock template directory inside the skill, but we use the real one for orchestrator test
    # The real templates exist because of PR-001
    
    doctor_script = Path(__file__).parent.parent / "scripts" / "doctor.py"
    res1 = subprocess.run([sys.executable, str(doctor_script), str(workdir), "--fix"], capture_output=True, text=True)
    assert res1.returncode == 0
    
    # We must explicitly stage and commit the scaffold files created by doctor
    subprocess.run(["git", "add", "."], cwd=str(workdir))
    subprocess.run(["git", "commit", "-m", "scaffold"], cwd=str(workdir))
    
    # We also need to touch PRD.md to avoid "validate_prd_is_committed" crash
    # Oh wait, orchestrator.py will crash because PRD.md is missing. Let's see if the doctor check happens before.
    # Ah, doctor check is right at the top! So PRD check comes later.
    # But wait, doctor.py check runs apply_overlay with check_only.
    # Let's verify what doctor.py check returns for workdir.
    
    res2 = subprocess.run([sys.executable, str(doctor_script), str(workdir), "--check"], capture_output=True, text=True)
    print("Doctor check output:", res2.stdout)
    assert res2.returncode == 0
    
    orch_script = Path(__file__).parent.parent / "scripts" / "orchestrator.py"
    res = subprocess.run([sys.executable, str(orch_script), "--workdir", str(workdir), "--prd-file", "PRD.md", "--channel", "test", "--force-replan", "false", "--enable-exec-from-workspace", "--test-sleep"], capture_output=True, text=True, env={**os.environ, "SDLC_TEST_MODE": "true"})
    
    # Should not print the compliant error
    assert "Project is not SDLC compliant" not in res.stdout
    assert "Project is not SDLC compliant" not in res.stderr

