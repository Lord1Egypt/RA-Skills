"""Subagent runner — execute a phase via Cursor CLI (agent binary).

The Cursor CLI is our most reliable autonomous code executor because:
1. Full tool access (read, write, edit, exec, search)
2. Smart model routing (auto mode = $0 input cost)
3. Proven reliability for multi-file edits
4. Runs autonomously with --trust flag
5. JSON output mode for structured results

This replaces the broken unified-router/cursor method with direct CLI invocation.

Usage:
    Called by phase_runner.py when execution_method="subagent" or "cursor"
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# Auto-detect workspace root
_SKILL_DIR = Path(__file__).resolve().parent.parent  # skills/night-shift/
_WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", _SKILL_DIR.parent.parent))  # ~/.openclaw/workspace
_DATA_DIR = _WORKSPACE / "data" / "night-shift"

WORKSPACE = _WORKSPACE
CURSOR_CLI = Path(os.environ.get("CURSOR_CLI", shutil.which("agent") or "/usr/local/bin/agent"))


@dataclass
class SubagentResult:
    success: bool
    output: str
    error: str
    duration_seconds: float
    files_changed: list[str]
    tokens_used: Optional[int] = None


def run_phase_cursor_cli(
    phase_prompt: str,
    worktree_path: str,
    plan_id: str = "",
    phase_id: int = 0,
    timeout: int = 600,
    model: str = "auto",
) -> SubagentResult:
    """Execute a phase by running Cursor CLI (agent binary) in the worktree.

    The Cursor CLI gets:
    - The phase prompt as its task
    - The worktree as its working directory
    - Full tool access via --trust flag
    - JSON output mode for structured results

    Args:
        phase_prompt: What the phase should do
        worktree_path: Git worktree directory
        plan_id: Night shift plan ID (for logging)
        phase_id: Phase number (for logging)
        timeout: Max execution time in seconds
        model: Model to use (default: auto = free routing)

    Returns:
        SubagentResult with execution details
    """
    start = time.time()

    if not CURSOR_CLI.exists():
        return SubagentResult(
            success=False,
            output="",
            error=f"Cursor CLI not found at {CURSOR_CLI}",
            duration_seconds=0,
            files_changed=[],
        )

    # Build the full prompt with context
    full_prompt = f"""You are executing Phase {phase_id} of Night Shift plan "{plan_id}".

WORKING DIRECTORY: {worktree_path}
You MUST work in this directory. All file operations must be relative to this path.

YOUR TASK:
{phase_prompt}

IMPORTANT RULES:
1. Read existing files FIRST to understand the codebase structure
2. Use the edit tool for modifications (preserves existing content)
3. Make MINIMAL, TARGETED changes — don't rewrite entire files
4. After making changes, verify they work (run tests, check imports)
5. If the task is unclear or impossible, explain why in your response

When done, summarize what you changed."""

    # Write prompt to temp file (avoids shell escaping issues)
    prompt_file = Path(f"/tmp/ns-prompt-{plan_id}-{phase_id}.txt")
    prompt_file.write_text(full_prompt)

    try:
        # Run Cursor CLI
        result = subprocess.run(
            [
                str(CURSOR_CLI),
                "-p", str(prompt_file),
                "--model", model,
                "--trust",
                "--output-format", "json",
            ],
            capture_output=True,
            text=True,
            timeout=timeout + 30,
            cwd=worktree_path,
            env={**os.environ},
        )

        elapsed = time.time() - start

        # Clean up prompt file
        prompt_file.unlink(missing_ok=True)

        output = result.stdout[:15000] if result.stdout else ""
        error = result.stderr[:2000] if result.stderr else ""

        # Determine success from Cursor CLI's own assessment
        # Cursor returns JSON: {"subtype": "success", "is_error": false}
        cursor_success = False
        if result.returncode == 0 and output:
            try:
                cursor_output = json.loads(output)
                cursor_success = (
                    cursor_output.get("subtype") == "success"
                    and not cursor_output.get("is_error", True)
                )
            except (json.JSONDecodeError, Exception):
                cursor_success = result.returncode == 0

        # Detect file changes for reporting (not gating)
        # Don't gate on file changes because:
        #   1. Cursor sandbox blocks git, changes may not show in git status
        #   2. Some phases are analysis/research with no file changes
        #   3. Executor verification is the real quality gate
        files_changed = _detect_changes(worktree_path)
        success = cursor_success

        return SubagentResult(
            success=success,
            output=output,
            error=error,
            duration_seconds=elapsed,
            files_changed=files_changed,
            tokens_used=None,  # Cursor handles token tracking
        )

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        prompt_file.unlink(missing_ok=True)
        # Check if partial changes were made
        files_changed = _detect_changes(worktree_path)
        return SubagentResult(
            success=False,
            output="",
            error=f"Cursor CLI timed out after {timeout}s ({len(files_changed)} files partially changed)",
            duration_seconds=elapsed,
            files_changed=files_changed,
        )
    except Exception as e:
        elapsed = time.time() - start
        prompt_file.unlink(missing_ok=True)
        return SubagentResult(
            success=False,
            output="",
            error=f"Cursor CLI error: {e}",
            duration_seconds=elapsed,
            files_changed=[],
        )


def _detect_changes(worktree_path: str) -> list[str]:
    """Detect all changed files in the worktree (modified + untracked)."""
    changes = []

    # Modified files
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            changes.extend(f for f in result.stdout.strip().split("\n") if f)
    except Exception:
        pass

    # Staged files
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--cached"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            changes.extend(f for f in result.stdout.strip().split("\n") if f)
    except Exception:
        pass

    # Untracked files
    try:
        result = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            changes.extend(f for f in result.stdout.strip().split("\n") if f)
    except Exception:
        pass

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for f in changes:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    return unique
