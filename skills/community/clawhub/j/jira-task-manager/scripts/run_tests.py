#!/usr/bin/env python3

import sys
import json
import subprocess
import time
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from find_repo import find_repo, load_config


def detect_test_command(repo_path):
    p = Path(repo_path)
    if (p / "pytest.ini").exists() or (p / "pyproject.toml").exists() or (p / "setup.cfg").exists():
        return ["python", "-m", "pytest", "-v"], 120
    if (p / "package.json").exists():
        return ["npm", "test"], 120
    return None, 120


def run_tests(repo_path, issue_key=None):
    config = load_config()
    repo_conf = config.get("repos", {}).get(repo_path, {})

    if repo_conf.get("test_command"):
        cmd = repo_conf["test_command"]
        timeout = repo_conf.get("test_timeout", 120)
    else:
        cmd, timeout = detect_test_command(repo_path)

    if not cmd:
        return {
            "success": False,
            "error": "No test command found for this repo. Add one to references/repos.json.",
        }

    start = time.time()
    try:
        result = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        elapsed = round(time.time() - start, 1)
        passed = result.returncode == 0
        return {
            "success": True,
            "passed": passed,
            "returncode": result.returncode,
            "duration_seconds": elapsed,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "repo_path": repo_path,
            "command": cmd,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Test timed out after {timeout}s.",
            "repo_path": repo_path,
            "command": cmd,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def run_tests_for_issue(issue_key):
    repo_result = find_repo(issue_key)
    if not repo_result["success"] or not repo_result.get("repo_path"):
        return {
            "success": False,
            "error": "Could not find local repo for this issue.",
            "find_repo_result": repo_result,
        }
    return run_tests(repo_result["repo_path"], issue_key=issue_key)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--issue", help="Issue key, e.g. DS-123")
    group.add_argument("--repo", help="Absolute path to local repo")
    args = parser.parse_args()

    if args.issue:
        result = run_tests_for_issue(args.issue)
    else:
        result = run_tests(args.repo)

    print(json.dumps(result, indent=2))

