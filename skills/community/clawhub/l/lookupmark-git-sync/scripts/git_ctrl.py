#!/usr/bin/env python3
"""Secure git repository manager for whitelisted repos.

Read-only commands run freely. Write commands require --confirm flag.
Repo list loaded from config file or defaults.

Usage:
    git_ctrl.py status [repo]        # Git status
    git_ctrl.py log [repo] [-n 10]   # Recent commits
    git_ctrl.py diff [repo]          # Unstaged changes
    git_ctrl.py branch [repo]        # List branches
    git_ctrl.py pull [repo] --confirm  # Stash + pull + stash pop
    git_ctrl.py push [repo] --confirm  # Push commits
    git_ctrl.py fetch [repo]         # Fetch without merging
    git_ctrl.py all                  # Status of all repos
"""

import argparse
import json
import os
import subprocess
import sys

# Default repos — can be overridden by config file
DEFAULT_REPOS = {
    "thesis": os.path.expanduser("~/Documenti/github/thesis"),
    "polito": os.path.expanduser("~/Documenti/github/polito"),
}
CONFIG_PATH = os.path.expanduser("~/.config/git-sync/repos.json")

WRITE_COMMANDS = {"pull", "push"}
READ_COMMANDS = {"status", "log", "diff", "branch", "fetch", "show", "remote"}


def load_repos() -> dict:
    """Load repos from config file, falling back to defaults."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                cfg = json.load(f)
            repos = {}
            for name, path in cfg.get("repos", {}).items():
                repos[name] = os.path.expanduser(path)
            if repos:
                return repos
        except Exception:
            pass
    return DEFAULT_REPOS


def resolve_repo(name: str, repos: dict) -> str | None:
    if name in repos:
        return repos[name]
    real = os.path.realpath(os.path.expanduser(name))
    for repo_name, repo_path in repos.items():
        rp = os.path.realpath(repo_path)
        if real == rp or real.startswith(rp + "/"):
            return real
    return None


def run_git(repo_path: str, args: list[str], timeout: int = 30) -> dict:
    cmd = ["git", "-C", repo_path] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {"returncode": result.returncode, "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}
    except subprocess.TimeoutExpired:
        return {"error": f"Command timed out ({timeout}s)"}
    except Exception as e:
        return {"error": str(e)}


def get_status(repo_path: str) -> dict:
    result = run_git(repo_path, ["status", "--short", "--branch"])
    log = run_git(repo_path, ["log", "--oneline", "-5"])
    ahead = run_git(repo_path, ["rev-list", "--count", "@{u}..HEAD"], timeout=5)
    behind = run_git(repo_path, ["rev-list", "--count", "HEAD..@{u}"], timeout=5)
    stash = run_git(repo_path, ["stash", "list"], timeout=5)

    return {
        "path": repo_path,
        "status": result.get("stdout", ""),
        "recent_commits": log.get("stdout", "").splitlines(),
        "ahead": ahead.get("stdout", "?") if "error" not in ahead else "?",
        "behind": behind.get("stdout", "?") if "error" not in behind else "?",
        "stash_count": len(stash.get("stdout", "").splitlines()) if stash.get("stdout") else 0,
    }


def format_status(data: dict, name: str) -> str:
    lines = [f"📂 {name} ({data['path']})"]
    if data.get("status"):
        lines.append(f"  Status: {data['status']}")
    else:
        lines.append("  Status: ✅ clean")
    if data.get("ahead") and data["ahead"] not in ("?", "0"):
        lines.append(f"  ⬆️  {data['ahead']} commits ahead of remote")
    if data.get("behind") and data["behind"] not in ("?", "0"):
        lines.append(f"  ⬇️  {data['behind']} commits behind remote")
    if data.get("stash_count", 0) > 0:
        lines.append(f"  📦 {data['stash_count']} stashed changes")
    if data.get("recent_commits"):
        lines.append("  Recent:")
        for c in data["recent_commits"][:5]:
            lines.append(f"    {c}")
    return "\n".join(lines)


def do_pull(repo_path: str) -> dict:
    """Stash uncommitted changes, pull, then pop stash."""
    # Stash if dirty
    status = run_git(repo_path, ["status", "--porcelain"])
    stashed = False
    if status.get("stdout", "").strip():
        stash_result = run_git(repo_path, ["stash", "--include-untracked"], timeout=30)
        if stash_result.get("returncode") == 0:
            stashed = True

    # Pull with rebase
    pull_result = run_git(repo_path, ["pull", "--rebase"], timeout=60)

    # Pop stash if we stashed
    if stashed:
        pop_result = run_git(repo_path, ["stash", "pop"], timeout=30)
        if pop_result.get("returncode") != 0:
            return {"returncode": 1, "stdout": pull_result.get("stdout", ""),
                    "stderr": f"Pull OK but stash pop failed: {pop_result.get('stderr', '')}"}

    return pull_result


def main():
    parser = argparse.ArgumentParser(description="Secure git repo manager")
    parser.add_argument("command", choices=list(READ_COMMANDS | WRITE_COMMANDS) + ["all"])
    parser.add_argument("repo", nargs="?", default=None)
    parser.add_argument("--confirm", action="store_true")
    parser.add_argument("-n", type=int, default=10)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    repos = load_repos()

    if args.command in WRITE_COMMANDS and not args.confirm:
        print(f"⚠️  '{args.command}' modifies the repo. Add --confirm to proceed.", file=sys.stderr)
        sys.exit(1)

    if args.command == "all" or args.repo == "all":
        results = {}
        for name, path in repos.items():
            if os.path.isdir(path):
                results[name] = get_status(path)
            else:
                results[name] = {"error": "directory not found"}
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for name, data in results.items():
                if "error" in data:
                    print(f"📂 {name}: ❌ {data['error']}")
                else:
                    print(format_status(data, name))
                print()
        return

    repo_name = args.repo or list(repos.keys())[0]
    repo_path = resolve_repo(repo_name, repos)
    if not repo_path:
        print(f"❌ Unknown repo: {repo_name}. Allowed: {', '.join(repos.keys())}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(repo_path):
        print(f"❌ Directory not found: {repo_path}", file=sys.stderr)
        sys.exit(1)

    if args.command == "status":
        data = get_status(repo_path)
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print(format_status(data, repo_name))
    elif args.command == "log":
        result = run_git(repo_path, ["log", "--oneline", f"-{args.n}"])
        print(result.get("stdout", result.get("error", "")))
    elif args.command == "diff":
        result = run_git(repo_path, ["diff", "--stat"])
        print(result.get("stdout", result.get("error", "")))
    elif args.command == "branch":
        result = run_git(repo_path, ["branch", "-a"])
        print(result.get("stdout", result.get("error", "")))
    elif args.command == "fetch":
        result = run_git(repo_path, ["fetch", "--all"], timeout=60)
        print(result.get("stdout") or result.get("stderr") or "✅ Fetch complete")
    elif args.command == "pull" and args.confirm:
        result = do_pull(repo_path)
        if result.get("returncode") == 0:
            print(f"✅ Pull successful (with auto-stash)")
            if result.get("stdout"):
                print(result["stdout"])
        else:
            print(f"❌ Pull failed: {result.get('stderr', result.get('error', ''))}")
    elif args.command == "push" and args.confirm:
        result = run_git(repo_path, ["push"], timeout=60)
        if result.get("returncode") == 0:
            print("✅ Push successful")
            if result.get("stdout"):
                print(result["stdout"])
        else:
            print(f"❌ Push failed: {result.get('stderr', '')}")


if __name__ == "__main__":
    main()
