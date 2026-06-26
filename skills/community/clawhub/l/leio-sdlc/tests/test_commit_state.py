import os
import subprocess
import pytest
import sys

def test_commit_state_validates_files(tmp_path):
    # Setup mock git repo
    os.chdir(tmp_path)
    subprocess.run(["git", "init"])
    
    with open("main.py", "w") as f:
        f.write("print('hello')")
        
    script_path = "/root/.openclaw/workspace/projects/leio-sdlc/scripts/commit_state.py"
    
    # Try to commit source code
    result = subprocess.run(["python3", script_path, "--files", "main.py"], capture_output=True, text=True)
    
    assert result.returncode == 1
    assert "[FATAL] commit_state.py can only be used for state and PRD files. Source code changes must go through the SDLC pipeline." in result.stdout

def test_orchestrator_rejects_uncommitted_state(tmp_path):
    os.chdir(tmp_path)
    subprocess.run(["git", "init"])
    with open("PRD_uncommitted.md", "w") as f:
        f.write("uncommitted")
        
    orchestrator_script = "/root/.openclaw/workspace/projects/leio-sdlc/scripts/orchestrator.py"
    result = subprocess.run(["python3", orchestrator_script, "--enable-exec-from-workspace", "--workdir", str(tmp_path), "--prd-file", "PRD_uncommitted.md", "--force-replan", "true"], capture_output=True, text=True)
    
    assert result.returncode == 1
    assert "Workspace contains uncommitted state files." in result.stdout
    assert "python3 ~/.openclaw/skills/leio-sdlc/scripts/commit_state.py" in result.stdout

def test_commit_state_success(tmp_path):
    # Setup mock git repo
    os.chdir(tmp_path)
    subprocess.run(["git", "init"])
    subprocess.run(["git", "config", "user.email", "test@example.com"])
    subprocess.run(["git", "config", "user.name", "Test User"])
    
    os.makedirs("docs/PRDs", exist_ok=True)
    
    with open("STATE.md", "w") as f:
        f.write("state")
        
    with open("docs/PRDs/PRD_001_Test.md", "w") as f:
        f.write("prd")
        
    script_path = "/root/.openclaw/workspace/projects/leio-sdlc/scripts/commit_state.py"
    
    # Commit state files
    result = subprocess.run(["python3", script_path, "--files", "STATE.md", "docs/PRDs/PRD_001_Test.md"], capture_output=True, text=True)
    
    assert result.returncode == 0
    assert "Successfully baselined PRD/state files." in result.stdout

def test_pre_commit_hook_output(tmp_path):
    os.chdir(tmp_path)
    subprocess.run(["git", "init"])
    subprocess.run(["git", "config", "user.email", "test@example.com"])
    subprocess.run(["git", "config", "user.name", "Test User"])
    
    with open(".sdlc_guardrail", "w") as f:
        f.write("")
        
    subprocess.run(["git", "add", ".sdlc_guardrail"])
    subprocess.run(["git", "commit", "-m", "init"])
    
    os.makedirs(".sdlc_hooks", exist_ok=True)
    subprocess.run(["cp", "/root/.openclaw/workspace/projects/leio-sdlc/.sdlc_hooks/pre-commit", ".sdlc_hooks/"])
    subprocess.run(["git", "config", "core.hooksPath", ".sdlc_hooks"])
    
    with open("test.txt", "w") as f:
        f.write("test")
    subprocess.run(["git", "add", "test.txt"])
    
    result = subprocess.run(["git", "commit", "-m", "test"], capture_output=True, text=True)
    
    assert result.returncode == 1
    assert "python3 ~/.openclaw/skills/leio-sdlc/scripts/commit_state.py --files <path_to_files>" in result.stdout or "python3 ~/.openclaw/skills/leio-sdlc/scripts/commit_state.py --files <path_to_files>" in result.stderr
    # Setup mock git repo
    os.chdir(tmp_path)
    subprocess.run(["git", "init"])
    
    with open("STATE.md", "w") as f:
        f.write("state")
        
    # Create fake lock file
    os.makedirs(".git", exist_ok=True)
    with open(".git/index.lock", "w") as f:
        f.write("")
        
    script_path = "/root/.openclaw/workspace/projects/leio-sdlc/scripts/commit_state.py"
    
    # Try to commit with lock file present
    result = subprocess.run(["python3", script_path, "--files", "STATE.md"], capture_output=True, text=True)
    
    assert result.returncode == 1
    assert "[FATAL] Git index is locked. Please wait or remove .git/index.lock if a previous process crashed." in result.stdout
