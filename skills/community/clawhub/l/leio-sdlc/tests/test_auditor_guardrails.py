import os
import subprocess
import sys

def test_auditor_rejects_missing_hardcoded_content(tmp_path):
    os.chdir(tmp_path)
    prd_path = tmp_path / "PRD.md"
    prd_path.write_text("# PRD\n1. Context & Problem\n2. Requirements & User Stories\n3. Architecture & Technical Strategy\n4. Acceptance Criteria\n5. Overall Test Strategy\n6. Framework Modifications")
    
    script_path = "/root/.openclaw/workspace/projects/leio-sdlc/scripts/spawn_auditor.py"
    
    # Run auditor script
    env = os.environ.copy()
    env["SDLC_TEST_MODE"] = "true"
    result = subprocess.run([
        "python3", script_path, 
        "--prd-file", str(prd_path), 
        "--workdir", str(tmp_path), 
        "--channel", "test", 
        "--enable-exec-from-workspace"
    ], capture_output=True, text=True, env=env)
    
    assert "REJECTED: The PRD mentions specific text/messages but fails to list them in 'Section 7. Hardcoded Content'" in result.stdout

def test_auditor_rejects_invalid_template(tmp_path):
    os.chdir(tmp_path)
    prd_path = tmp_path / "PRD.md"
    prd_path.write_text("# Feral PRD\nMissing headers")
    
    script_path = "/root/.openclaw/workspace/projects/leio-sdlc/scripts/spawn_auditor.py"
    
    env = os.environ.copy()
    env["SDLC_TEST_MODE"] = "true"
    result = subprocess.run([
        "python3", script_path, 
        "--prd-file", str(prd_path), 
        "--workdir", str(tmp_path), 
        "--channel", "test", 
        "--enable-exec-from-workspace"
    ], capture_output=True, text=True, env=env)
    
    assert "REJECTED: PRD structure does not match the mandatory template" in result.stdout

def test_leio_auditor_removed():
    assert not os.path.exists("/root/.openclaw/workspace/projects/leio-sdlc/skills/leio-auditor")
