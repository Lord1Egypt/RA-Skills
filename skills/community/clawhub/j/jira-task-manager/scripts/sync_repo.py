#!/usr/bin/env python3

import sys
import json
import subprocess
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from find_repo import find_repo


def run_git(repo_path, args):
    result = subprocess.run(
        ["git"] + args,
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def get_default_branch(repo_path):
    code, out, _ = run_git(repo_path, ["symbolic-ref", "refs/remotes/origin/HEAD", "--short"])
    if code == 0:
        return out.replace("origin/", "").strip()
    for name in ["main", "master"]:
        code, _, _ = run_git(repo_path, ["rev-parse", "--verify", f"origin/{name}"])
        if code == 0:
            return name
    return "main"


def find_branches(repo_path, issue_key):
    _, output, _ = run_git(repo_path, ["branch", "-a"])
    key = issue_key.upper()
    branches = [b.strip().lstrip("* ") for b in output.splitlines() if b.strip()]
    return [b for b in branches if key in b.upper()]


def sync_repo(issue_key, branch_name=None):
    repo_result = find_repo(issue_key)
    if not repo_result["success"] or not repo_result.get("repo_path"):
        return {
            "success": False,
            "error": "Could not find local repo for this issue.",
            "find_repo_result": repo_result,
        }

    repo_path = repo_result["repo_path"]

    code, _, err = run_git(repo_path, ["fetch", "--all", "--prune"])
    if code != 0:
        return {"success": False, "error": f"git fetch failed: {err}"}

    if branch_name:
        _, out, _ = run_git(repo_path, ["branch", "-a"])
        all_branches = [b.strip().lstrip("* ") for b in out.splitlines() if b.strip()]
        matches = [b for b in all_branches if b == branch_name or b.endswith(f"/{branch_name}")]
    else:
        matches = find_branches(repo_path, issue_key)

    local_matches = [b for b in matches if not b.startswith("remotes/")]
    remote_matches = [b for b in matches if b.startswith("remotes/")]

    branch_created = False

    if local_matches:
        branch = local_matches[0]
        code, _, err = run_git(repo_path, ["checkout", branch])
        if code != 0:
            return {"success": False, "error": f"git checkout failed: {err}"}
        run_git(repo_path, ["pull"])

    elif remote_matches:
        remote_ref = remote_matches[0]
        branch = remote_ref.replace("remotes/origin/", "")
        code, _, err = run_git(repo_path, ["checkout", "-b", branch, "--track", remote_ref])
        if code != 0:
            return {"success": False, "error": f"git checkout failed: {err}"}

    else:
        default_branch = get_default_branch(repo_path)
        run_git(repo_path, ["checkout", default_branch])
        run_git(repo_path, ["pull"])
        branch = branch_name if branch_name else f"feature/{issue_key.upper()}"
        code, _, err = run_git(repo_path, ["checkout", "-b", branch])
        if code != 0:
            return {"success": False, "error": f"git checkout -b failed: {err}"}
        branch_created = True

    _, current_branch, _ = run_git(repo_path, ["rev-parse", "--abbrev-ref", "HEAD"])
    _, last_commit, _ = run_git(repo_path, ["log", "--oneline", "-1"])

    return {
        "success": True,
        "issue_key": issue_key.upper(),
        "repo_path": repo_path,
        "branch": current_branch,
        "branch_created": branch_created,
        "last_commit": last_commit,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("issue_key")
    parser.add_argument("--branch", default=None)
    args = parser.parse_args()
    print(json.dumps(sync_repo(args.issue_key, args.branch), indent=2))

