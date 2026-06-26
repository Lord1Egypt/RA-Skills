import os
import subprocess
import tempfile
import pytest

def test_independent_symmetrical_rollbacks():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    with tempfile.TemporaryDirectory() as mock_home:
        env = os.environ.copy()
        env["HOME_MOCK"] = mock_home
        
        # 1. Run first deployment
        deploy_script = os.path.join(repo_root, "kit-deploy.sh")
        res = subprocess.run(["bash", deploy_script], env=env, cwd=repo_root, capture_output=True, text=True)
        assert res.returncode == 0, f"First kit-deploy.sh failed: {res.stderr}"

        # 2. Run second deployment to create the backup archives of the first installation
        res = subprocess.run(["bash", deploy_script], env=env, cwd=repo_root, capture_output=True, text=True)
        assert res.returncode == 0, f"Second kit-deploy.sh failed: {res.stderr}"
        
        # Modify installed files slightly to verify rollback overwrites them
        skills_dir = os.path.join(mock_home, ".openclaw", "skills")
        for skill in ["leio-sdlc", "pm-skill"]:
            skill_path = os.path.join(skills_dir, skill)
            marker = os.path.join(skill_path, "MODIFIED_MARKER")
            with open(marker, "w") as f:
                f.write("modified")
                
        # 3. Run rollbacks
        scripts = [
            ("leio-sdlc", os.path.join(repo_root, "rollback.sh")),
            ("pm-skill", os.path.join(repo_root, "skills", "pm-skill", "rollback.sh")),
            
        ]
        
        for skill_name, script_path in scripts:
            assert os.path.exists(script_path), f"{script_path} does not exist"
            # Ensure --no-restart is supported and runs successfully
            res = subprocess.run(["bash", script_path, "--no-restart"], env=env, cwd=repo_root, capture_output=True, text=True)
            assert res.returncode == 0, f"Rollback failed for {skill_name}:\nSTDOUT: {res.stdout}\nSTDERR: {res.stderr}"
            
            # Verify marker is gone (rollback replaced the directory from tarball)
            skill_path = os.path.join(skills_dir, skill_name)
            marker = os.path.join(skill_path, "MODIFIED_MARKER")
            assert not os.path.exists(marker), f"Rollback did not restore {skill_name} cleanly (marker still exists)"
            
            # Ensure basic structure exists
            if skill_name == "leio-sdlc":
                assert os.path.exists(os.path.join(skill_path, "scripts", "orchestrator.py"))
            elif skill_name == "pm-skill":
                assert os.path.exists(os.path.join(skill_path, "scripts", "pm.py"))
            
