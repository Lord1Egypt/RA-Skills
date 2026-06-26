import os
import sys
import tempfile
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
import orchestrator

def test_orchestrator_creates_baseline_commit_file():
    with tempfile.TemporaryDirectory() as td:
        workdir = os.path.join(td, "workdir")
        global_dir = os.path.join(td, "global")
        os.makedirs(workdir)
        os.makedirs(os.path.join(workdir, ".git"))
        os.makedirs(global_dir)
        prd_file = os.path.join(td, "dummy.md")
        with open(prd_file, "w") as f: f.write("dummy")

        target_project_name = os.path.basename(os.path.abspath(workdir))
        job_dir = os.path.abspath(os.path.join(global_dir, ".sdlc_runs", target_project_name, "dummy"))

        test_args = [
            "orchestrator.py",
            "--workdir", workdir,
            "--global-dir", global_dir,
            "--prd-file", prd_file,
            "--force-replan", "true", "--enable-exec-from-workspace",
            "--channel", "slack:C123"
        ]

        def fake_subprocess_run(cmd, *args, **kwargs):
            res = MagicMock()
            res.returncode = 0
            res.stdout = ""
            
            if cmd == ["git", "rev-parse", "HEAD"]:
                res.stdout = "mocked_hash_12345\n"
            elif "branch" in cmd:
                res.stdout = "master\n"
            return res

        def fake_dpopen(cmd, *args, **kwargs):
            if "spawn_planner.py" in str(cmd):
                os.makedirs(job_dir, exist_ok=True)
                with open(os.path.join(job_dir, "PR_001.md"), "w") as f:
                    f.write("dummy")
                proc = MagicMock()
                proc.returncode = 0
                return proc
            raise KeyboardInterrupt("Stop orchestrator loop")

        with patch("sys.argv", test_args), \
             patch("subprocess.run", side_effect=fake_subprocess_run), \
             patch("orchestrator.dpopen", side_effect=fake_dpopen), \
             patch("orchestrator.notify_channel"), patch("git_utils.check_git_boundary"):
            
            try:
                orchestrator.main()
            except (KeyboardInterrupt, SystemExit):
                pass
            
            baseline_file = os.path.join(job_dir, "baseline_commit.txt")
            assert os.path.exists(baseline_file), "baseline_commit.txt should be created"
            with open(baseline_file, "r") as f:
                content = f.read()
            assert content.strip() == "mocked_hash_12345"

def test_orchestrator_does_not_overwrite_existing_baseline():
    with tempfile.TemporaryDirectory() as td:
        workdir = os.path.join(td, "workdir")
        global_dir = os.path.join(td, "global")
        os.makedirs(workdir)
        os.makedirs(os.path.join(workdir, ".git"))
        os.makedirs(global_dir)
        prd_file = os.path.join(td, "dummy.md")
        with open(prd_file, "w") as f: f.write("dummy")

        target_project_name = os.path.basename(os.path.abspath(workdir))
        job_dir = os.path.abspath(os.path.join(global_dir, ".sdlc_runs", target_project_name, "dummy"))
        os.makedirs(job_dir)
        
        baseline_file = os.path.join(job_dir, "baseline_commit.txt")
        with open(baseline_file, "w") as f:
            f.write("existing_hash_99999")
            
        with open(os.path.join(job_dir, "PR_001.md"), "w") as f:
            f.write("dummy")

        test_args = [
            "orchestrator.py",
            "--workdir", workdir,
            "--global-dir", global_dir,
            "--prd-file", prd_file,
            "--force-replan", "false", "--enable-exec-from-workspace",
            "--channel", "slack:C123"
        ]

        def fake_subprocess_run(cmd, *args, **kwargs):
            res = MagicMock()
            res.returncode = 0
            res.stdout = ""
            
            if cmd == ["git", "rev-parse", "HEAD"]:
                res.stdout = "new_hash_11111\n"
            elif "branch" in cmd:
                res.stdout = "master\n"
            return res

        def fake_dpopen(cmd, *args, **kwargs):
            if "spawn_planner.py" in str(cmd):
                proc = MagicMock()
                proc.returncode = 0
                return proc
            raise KeyboardInterrupt("Stop orchestrator loop")

        with patch("sys.argv", test_args), \
             patch("subprocess.run", side_effect=fake_subprocess_run), \
             patch("orchestrator.dpopen", side_effect=fake_dpopen), \
             patch("orchestrator.notify_channel"), patch("git_utils.check_git_boundary"):
            
            try:
                orchestrator.main()
            except (KeyboardInterrupt, SystemExit):
                pass
            
            assert os.path.exists(baseline_file)
            with open(baseline_file, "r") as f:
                content = f.read()
            assert content.strip() == "existing_hash_99999", "Existing baseline file should not be overwritten"
