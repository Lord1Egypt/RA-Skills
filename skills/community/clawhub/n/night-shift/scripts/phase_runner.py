"""Phase runner — execute a phase via Unified-Router (GLM-5.1, Cursor, Opus), shell, or subagent."""

from __future__ import annotations
import subprocess
import shlex
import json
import os
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

# Auto-detect workspace root
_SKILL_DIR = Path(__file__).resolve().parent.parent  # skills/night-shift/
_WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", _SKILL_DIR.parent.parent))  # ~/.openclaw/workspace
_DATA_DIR = _WORKSPACE / "data" / "night-shift"


@dataclass
class PhaseResult:
    success: bool
    output: str
    error: str
    duration_seconds: float
    execution_method: (
        str  # "subagent", "cursor" (unified-router), "claude-code", "shell"
    )
    tokens_used: Optional[int] = None
    duration_ms: Optional[int] = None  # Added for Claude Code (milliseconds)


def build_phase_prompt(
    plan_title: str,
    plan_id: str,
    phase_id: int,
    phase_title: str,
    phase_prompt: str,
    worktree_path: str,
    branch: str,
    previous_outputs: Optional[list[str]] = None,
    verification_type: str = "none",
    verification_config: Optional[dict] = None,
) -> str:
    """Build a structured prompt for the phase executor."""
    prev_section = ""
    if previous_outputs:
        prev_section = "\nPrevious phases produced:\n" + "\n".join(
            f"  - Phase {i + 1}: {out}" for i, out in enumerate(previous_outputs)
        )

    verify_section = ""
    if verification_type != "none":
        verify_section = f"\nVerification after completion: {verification_type}"
        if verification_config:
            verify_section += f" checking {json.dumps(verification_config)}"

    return f"""You are executing Phase {phase_id} of Plan "{plan_title}".
Branch: {branch}
Working directory: {worktree_path}
{prev_section}

Your task: {phase_prompt}
{verify_section}

DO NOT modify files outside: {worktree_path}
On success: commit with message "Phase {phase_id}: {phase_title}"
If you cannot complete the task, explain what went wrong."""


def run_phase_cursor(
    phase_prompt: str,
    worktree_path: str,
    timeout: int = 300,
) -> PhaseResult:
    """Run a phase via Unified-Router (GLM-5.1, Cursor, Opus fallback)."""
    router_bin = str(_WORKSPACE / "skills" / "unified-router" / "run.sh")
    if not os.path.exists(router_bin):
        return PhaseResult(
            success=False,
            output="",
            error="Unified-router not found at skills/unified-router/run.sh",
            duration_seconds=0,
            execution_method="unified-router",
        )

    import time

    start = time.time()

    try:
        # Call unified-router, which routes to GLM-5.1/Cursor/Opus
        result = subprocess.run(
            ["bash", router_bin, phase_prompt],
            capture_output=True,
            text=True,
            timeout=timeout + 30,
            env={**os.environ},
            cwd=worktree_path,
        )
        elapsed = time.time() - start

        # Parse unified-router JSON output
        # Format: {"provider": "zai", "model": "glm-5-turbo", "result": "...", "cost_entry": {...}, "truncated": bool}
        output = result.stdout[:10000]  # Default fallback
        tokens_used = None
        router_provider = "?"
        router_model = "?"

        try:
            router_output = json.loads(result.stdout)
            output = router_output.get("result", "")
            cost_info = router_output.get("cost_entry", {})
            tokens_used = cost_info.get("tokens", 0)
            router_provider = router_output.get("provider", "?")
            router_model = router_output.get("model", "?")

            # Check for truncation warning
            if router_output.get("truncated", False):
                output += "\n\n[Output truncated by unified-router - see logs/cursor-usage/router-outputs/]"
        except (json.JSONDecodeError, Exception):
            # Keep default values (output already set to stdout[:10000])
            pass

        return PhaseResult(
            success=(result.returncode == 0),
            output=output[:10000],
            error=result.stderr[:2000] if result.stderr else "",
            duration_seconds=elapsed,
            execution_method=f"unified-router ({router_provider}:{router_model})",
            tokens_used=tokens_used,
        )
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        return PhaseResult(
            success=False,
            output="",
            error=f"Unified-router timed out after {timeout}s",
            duration_seconds=elapsed,
            execution_method="unified-router",
        )
    except Exception as e:
        return PhaseResult(
            success=False,
            output="",
            error=f"Unified-router error: {e}",
            duration_seconds=0,
            execution_method="unified-router",
        )


def run_phase_shell(
    command: str,
    worktree_path: str,
    timeout: int = 120,
) -> PhaseResult:
    """Run a phase as a simple shell command."""
    import time

    start = time.time()

    try:
        args = shlex.split(command)
        if not args:
            return PhaseResult(
                success=False,
                output="",
                error="Empty shell command",
                duration_seconds=0,
                execution_method="shell",
            )
        result = subprocess.run(
            args,
            cwd=worktree_path,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        elapsed = time.time() - start

        return PhaseResult(
            success=result.returncode == 0,
            output=result.stdout[:10000],
            error=result.stderr[:2000],
            duration_seconds=elapsed,
            execution_method="shell",
        )
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        return PhaseResult(
            success=False,
            output="",
            error=f"Shell command timed out after {timeout}s",
            duration_seconds=elapsed,
            execution_method="shell",
        )


def decide_execution_method(
    phase_prompt: str, verification: str, phase_method: str = "claude-code"
) -> str:
    """Determine execution method. Respects explicit phase.execution_method first.

    Priority:
    1. Explicit method from phase config ("claude-code", "cursor", "shell", "subagent")
    2. Verification type hints (tests/build/lint need claude-code or cursor for tool access)
    3. Default: claude-code (more reliable for Night-Shift autonomous execution)
    """
    # Always respect explicit method (unless it's "auto" which triggers smart routing)
    if phase_method and phase_method != "auto":
        return phase_method

    # Smart routing based on verification type only (NOT prompt content)
    if verification in ("run_tests", "run_build", "lint_check"):
        return "claude-code"

    return "claude-code"  # Default to Claude Code for Night-Shift


def run_phase_claude_code(
    phase_prompt: str,
    worktree_path: str,
    timeout: int = 300,
    max_budget_usd: float = 0.50,
) -> PhaseResult:
    """
    Run a phase via Claude Code CLI with auto-approval.

    Uses claude-wrapper.sh which runs Claude Code as 'coder' user
    with --permission-mode bypassPermissions for autonomous execution.

    CRITICAL: Includes safeguards against runaway token consumption
    (safety check) via --max-budget-usd flag.

    Args:
        phase_prompt: The phase task prompt
        worktree_path: Git worktree directory path
        timeout: Timeout in seconds (default 300)
        max_budget_usd: Maximum USD to spend on this phase (default 0.50)

    Returns:
        PhaseResult with execution details and output
    """
    import time

    wrapper_bin = Path(__file__).resolve().parent / "claude-wrapper.sh"

    if not wrapper_bin.exists():
        return PhaseResult(
            success=False,
            output="",
            error="claude-wrapper.sh not found",
            duration_seconds=0,
            execution_method="claude-code-cli (wrapper not found)",
            tokens_used=0,
            duration_ms=0,
        )

    try:
        # Run Claude Code wrapper with max budget safeguard
        start_time = time.time()

        result = subprocess.run(
            [
                str(wrapper_bin),
                worktree_path,
                phase_prompt,
                str(timeout),
                str(max_budget_usd),
            ],
            capture_output=True,
            text=True,
            timeout=timeout + 30,  # Extra buffer for subprocess overhead
        )

        elapsed = time.time() - start_time
        duration_ms = int(elapsed * 1000)

        # Parse Claude Code JSON output
        claude_output = None
        tokens_used = 0

        if result.returncode == 0 and result.stdout:
            try:
                claude_output = json.loads(result.stdout)
                # Extract tokens from Claude Code output structure
                # Claude Code JSON format: {"usage": {"input_tokens": X, "output_tokens": Y}}
                tokens_used = claude_output.get("usage", {}).get(
                    "input_tokens", 0
                ) + claude_output.get("usage", {}).get("output_tokens", 0)
            except json.JSONDecodeError:
                # Output isn't JSON, use raw text
                claude_output = {"raw_output": result.stdout}

        # Check for errors
        if result.returncode != 0:
            return PhaseResult(
                success=False,
                output=result.stdout[:10000] if result.stdout else "",
                error=result.stderr[:2000]
                if result.stderr
                else "Claude Code CLI failed",
                duration_seconds=elapsed,
                execution_method="claude-code-cli (error)",
                tokens_used=tokens_used,
                duration_ms=duration_ms,
            )

        # Check timeout
        if result.returncode == 124:  # timeout command exit code
            return PhaseResult(
                success=False,
                output=result.stdout[:10000] if result.stdout else "",
                error=f"Phase execution timed out after {timeout}s (may be stuck in reasoning loop)",
                duration_seconds=elapsed,
                execution_method="claude-code-cli (timeout)",
                tokens_used=tokens_used,
                duration_ms=duration_ms,
            )

        # Check for budget exceeded (Claude Code returns specific code)
        stderr_lower = result.stderr.lower() if result.stderr else ""
        if "budget" in stderr_lower or "max budget" in stderr_lower:
            return PhaseResult(
                success=False,
                output=result.stdout[:10000] if result.stdout else "",
                error=f"Exceeded max budget of ${max_budget_usd} (runaway token consumption)",
                duration_seconds=elapsed,
                execution_method="claude-code-cli (budget exceeded)",
                tokens_used=tokens_used,
                duration_ms=duration_ms,
            )

        # Success
        output_text = (
            json.dumps(claude_output)
            if claude_output
            else (result.stdout[:10000] if result.stdout else "")
        )
        return PhaseResult(
            success=True,
            output=output_text,
            error=None,
            duration_seconds=elapsed,
            execution_method="claude-code-cli",
            tokens_used=tokens_used,
            duration_ms=duration_ms,
        )

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        return PhaseResult(
            success=False,
            output="",
            error="Phase execution timeout",
            duration_seconds=elapsed,
            execution_method="claude-code-cli (timeout)",
            tokens_used=0,
            duration_ms=elapsed * 1000,
        )
    except Exception as e:
        return PhaseResult(
            success=False,
            output="",
            error=f"Claude Code execution exception: {e}",
            duration_seconds=0,
            execution_method="claude-code-cli (exception)",
            tokens_used=0,
            duration_ms=0,
        )


def run_phase(
    phase_prompt: str,
    worktree_path: str,
    execution_method: str = "subagent",
    timeout: int = 300,
    max_budget_usd: float = 0.50,
    plan_id: str = "",
    phase_id: int = 0,
) -> PhaseResult:
    """
    Run a single phase with the specified execution method.

    Args:
        phase_prompt: The phase task prompt
        worktree_path: Git worktree directory path
        execution_method: Execution method ("subagent", "cursor", "claude-code", "shell")
        timeout: Timeout in seconds (default 300)
        max_budget_usd: Maximum USD to spend (for claude-code only)
        plan_id: Night shift plan ID (for subagent logging)
        phase_id: Phase number (for subagent logging)

    Returns:
        PhaseResult with execution details
    """
    if execution_method == "subagent":
        return run_phase_subagent(
            phase_prompt, worktree_path, plan_id, phase_id, timeout
        )
    elif execution_method == "cursor":
        # Route cursor to subagent (Cursor CLI) instead of broken unified-router
        return run_phase_subagent(
            phase_prompt, worktree_path, plan_id, phase_id, timeout
        )
    elif execution_method == "claude-code":
        return run_phase_claude_code(
            phase_prompt, worktree_path, timeout, max_budget_usd
        )
    elif execution_method == "shell":
        return run_phase_shell(phase_prompt, worktree_path, timeout)
    else:
        return PhaseResult(
            success=False,
            output="",
            error=f"Unsupported execution method: {execution_method}",
            duration_seconds=0,
            execution_method=f"unknown ({execution_method})",
            tokens_used=0,
            duration_ms=0,
        )


def run_phase_subagent(
    phase_prompt: str,
    worktree_path: str,
    plan_id: str = "",
    phase_id: int = 0,
    timeout: int = 600,
) -> PhaseResult:
    """Run a phase via Cursor CLI (agent binary) — the reliable code executor."""
    from subagent_runner import run_phase_cursor_cli

    result = run_phase_cursor_cli(
        phase_prompt=phase_prompt,
        worktree_path=worktree_path,
        plan_id=plan_id,
        phase_id=phase_id,
        timeout=timeout,
        model="auto",
    )

    return PhaseResult(
        success=result.success,
        output=result.output[:10000],
        error=result.error[:2000],
        duration_seconds=result.duration_seconds,
        execution_method=f"cursor-cli ({len(result.files_changed)} files changed)",
        tokens_used=result.tokens_used,
    )
