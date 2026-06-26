"""Git worktree manager — isolated branches per plan."""

from __future__ import annotations
import os
import subprocess
import shutil
from pathlib import Path

# Auto-detect workspace root
_SKILL_DIR = Path(__file__).resolve().parent.parent  # skills/night-shift/
_WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", _SKILL_DIR.parent.parent))  # ~/.openclaw/workspace
_DATA_DIR = _WORKSPACE / "data" / "night-shift"

WORKSPACE = _WORKSPACE
WORKTREES_DIR = _DATA_DIR / "worktrees"


def create_worktree(plan_id: str, base_branch: str = "master") -> tuple[bool, str]:
    """Create an isolated git worktree for a plan.
    Returns (success, worktree_path)."""
    worktree_path = WORKTREES_DIR / plan_id

    branch = f"night-shift/{plan_id}"

    # Clean up existing worktree if present (must remove BEFORE deleting branch)
    if worktree_path.exists():
        subprocess.run(
            ["git", "worktree", "remove", str(worktree_path), "--force"],
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
        )
        shutil.rmtree(worktree_path, ignore_errors=True)

    # Prune stale worktree refs so branch deletion succeeds
    subprocess.run(
        ["git", "worktree", "prune"], cwd=WORKSPACE, capture_output=True, text=True
    )

    WORKTREES_DIR.mkdir(parents=True, exist_ok=True)

    # Now safe to delete the branch
    subprocess.run(
        ["git", "branch", "-D", branch], cwd=WORKSPACE, capture_output=True, text=True
    )

    # Create worktree with new branch
    result = subprocess.run(
        ["git", "worktree", "add", "-b", branch, str(worktree_path), base_branch],
        cwd=WORKSPACE,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return False, f"git worktree add failed: {result.stderr}"

    # Fix permissions for 'coder' user (Claude Code runs as coder via su)
    # Must chmod o+x on entire path chain so coder can traverse
    for dir_path in [
        WORKSPACE,
        WORKSPACE / "data",
        WORKSPACE / "data" / "night-shift",
        worktree_path,
    ]:
        if dir_path.exists():
            subprocess.run(
                ["chmod", "o+x", str(dir_path)], capture_output=True, text=True
            )
    subprocess.run(
        ["chown", "-R", "coder:coder", str(worktree_path)],
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["chmod", "-R", "755", str(worktree_path)], capture_output=True, text=True
    )

    # Allow root to run git commands on coder-owned worktree
    # (git refuses "dubious ownership" otherwise)
    subprocess.run(
        ["git", "config", "--global", "--add", "safe.directory", str(worktree_path)],
        capture_output=True,
        text=True,
    )

    return True, str(worktree_path)


def remove_worktree(plan_id: str) -> bool:
    """Remove a worktree (but keep the branch for review)."""
    worktree_path = WORKTREES_DIR / plan_id

    if worktree_path.exists():
        result = subprocess.run(
            ["git", "worktree", "remove", str(worktree_path), "--force"],
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            # Fallback: manual cleanup
            shutil.rmtree(worktree_path, ignore_errors=True)

    # Prune stale worktree references
    subprocess.run(
        ["git", "worktree", "prune"], cwd=WORKSPACE, capture_output=True, text=True
    )

    return not (worktree_path.exists())


def commit_phase(plan_id: str, phase_id: int, title: str) -> tuple[bool, str]:
    """Commit current changes in the worktree with a phase summary message."""
    worktree_path = WORKTREES_DIR / plan_id
    if not worktree_path.exists():
        return False, f"Worktree not found: {worktree_path}"

    message = f"Phase {phase_id}: {title}"

    # Stage all changes
    subprocess.run(
        ["git", "add", "-A"], cwd=worktree_path, capture_output=True, text=True
    )

    # Check if there are changes to commit
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
    )
    if not status.stdout.strip():
        return True, "No changes to commit"

    # Commit (skip pre-commit hooks — worktree has full repo copy which
    # triggers skill/cron validation hooks on unrelated files)
    result = subprocess.run(
        ["git", "commit", "-m", message, "--allow-empty", "--no-verify"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return False, f"git commit failed: {result.stderr}"

    # Get commit hash
    hash_result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
    )

    commit_hash = (
        hash_result.stdout.strip() if hash_result.returncode == 0 else "unknown"
    )
    return True, commit_hash


def reset_phase(plan_id: str) -> bool:
    """Reset worktree to previous commit (gnhf pattern: reset-on-fail)."""
    worktree_path = WORKTREES_DIR / plan_id
    if not worktree_path.exists():
        return False

    # Reset to previous commit
    subprocess.run(
        ["git", "reset", "--hard", "HEAD~1"],
        cwd=worktree_path,
        capture_output=True,
        text=True,
    )

    # Clean untracked files
    subprocess.run(
        ["git", "clean", "-fd"], cwd=worktree_path, capture_output=True, text=True
    )

    return True


def get_branch_commits(plan_id: str) -> list[dict]:
    """Get only plan-specific commits (not master history)."""
    branch = f"night-shift/{plan_id}"
    result = subprocess.run(
        ["git", "log", f"master..{branch}", "--oneline", "--format=%h %s"],
        cwd=WORKSPACE,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []

    commits = []
    for line in result.stdout.strip().split("\n"):
        if line:
            parts = line.split(" ", 1)
            commits.append(
                {"hash": parts[0], "message": parts[1] if len(parts) > 1 else ""}
            )
    return commits


def get_diff_stats(plan_id: str) -> str:
    """Get diff stats for a plan branch vs master."""
    branch = f"night-shift/{plan_id}"
    result = subprocess.run(
        ["git", "diff", "--stat", f"master...{branch}"],
        cwd=WORKSPACE,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def cleanup_old_worktrees(max_age_hours: int = 72):
    """Remove worktrees older than max_age_hours (but keep branches)."""
    if not WORKTREES_DIR.exists():
        return

    import time

    now = time.time()
    max_age_seconds = max_age_hours * 3600

    for entry in WORKTREES_DIR.iterdir():
        if entry.is_dir():
            try:
                age = now - entry.stat().st_mtime
                if age > max_age_seconds:
                    remove_worktree(entry.name)
            except OSError:
                pass


def list_worktrees() -> list[dict]:
    """List all active worktrees."""
    result = subprocess.run(
        ["git", "worktree", "list", "--porcelain"],
        cwd=WORKSPACE,
        capture_output=True,
        text=True,
    )
    worktrees = []
    current = {}
    for line in result.stdout.split("\n"):
        if line.startswith("worktree "):
            if current:
                worktrees.append(current)
            current = {"path": line.split(" ", 1)[1]}
        elif line.startswith("branch "):
            ref = line.split(" ", 1)[1]
            current["branch"] = ref.replace("refs/heads/", "")
    if current:
        worktrees.append(current)
    return worktrees
