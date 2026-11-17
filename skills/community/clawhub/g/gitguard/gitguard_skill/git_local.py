"""Thin wrappers around local `git` CLI calls. No network access required."""
from __future__ import annotations

import subprocess
from datetime import datetime, timezone


def _run(repo_path: str, args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, *args],
            capture_output=True, text=True, timeout=30, check=False,
        )
        return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return ""


def is_git_repo(repo_path: str) -> bool:
    return _run(repo_path, ["rev-parse", "--is-inside-work-tree"]) == "true"


def uncommitted_changes_count(repo_path: str) -> int:
    out = _run(repo_path, ["status", "--porcelain"])
    if not out:
        return 0
    return len([l for l in out.splitlines() if l and not l.startswith("??")])


def untracked_files_count(repo_path: str) -> int:
    out = _run(repo_path, ["status", "--porcelain"])
    if not out:
        return 0
    return len([l for l in out.splitlines() if l.startswith("??")])


def days_since_last_commit(repo_path: str) -> int:
    out = _run(repo_path, ["log", "-1", "--format=%ct"])
    if not out.isdigit():
        return -1
    commit_time = datetime.fromtimestamp(int(out), tz=timezone.utc)
    return (datetime.now(timezone.utc) - commit_time).days


def list_branches(repo_path: str) -> list[dict]:
    """Return per-branch metadata: last commit date, staleness, ahead/behind main."""
    raw = _run(repo_path, [
        "for-each-ref", "--format=%(refname:short)|%(committerdate:unix)|%(upstream:track)",
        "refs/heads/",
    ])
    branches = []
    if not raw:
        return branches
    default_branch = _run(repo_path, ["symbolic-ref", "--short", "HEAD"]) or "main"
    for line in raw.splitlines():
        parts = line.split("|")
        if len(parts) < 2:
            continue
        name, ts = parts[0], parts[1]
        track = parts[2] if len(parts) > 2 else ""
        if not ts.isdigit():
            continue
        commit_time = datetime.fromtimestamp(int(ts), tz=timezone.utc)
        days_stale = (datetime.now(timezone.utc) - commit_time).days

        ahead, behind = 0, 0
        if "ahead" in track:
            try:
                ahead = int(track.split("ahead")[1].split(",")[0].strip().strip("]"))
            except (ValueError, IndexError):
                pass
        if "behind" in track:
            try:
                behind = int(track.split("behind")[1].strip().strip("]"))
            except (ValueError, IndexError):
                pass

        merged_out = _run(repo_path, ["branch", "--merged", default_branch])
        is_merged = any(name == b.strip().lstrip("* ").strip() for b in merged_out.splitlines())

        branches.append({
            "name": name,
            "days_stale": days_stale,
            "is_merged": is_merged,
            "ahead": ahead,
            "behind": behind,
        })
    return branches


def recent_commits(repo_path: str, limit: int = 30) -> list[tuple[str, str]]:
    """Return list of (short_sha, full_message)."""
    sep = "\x1e"  # record separator, unlikely to appear in commit messages
    out = _run(repo_path, ["log", f"-{limit}", f"--pretty=format:%h{sep}%B\x1d"])
    if not out:
        return []
    commits = []
    for chunk in out.split("\x1d"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if sep not in chunk:
            continue
        sha, msg = chunk.split(sep, 1)
        commits.append((sha.strip(), msg.strip()))
    return commits
