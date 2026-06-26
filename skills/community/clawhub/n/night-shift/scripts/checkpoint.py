"""Checkpoint system — save/restore execution state."""

from __future__ import annotations
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Auto-detect workspace root
_SKILL_DIR = Path(__file__).resolve().parent.parent  # skills/night-shift/
_WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", _SKILL_DIR.parent.parent))  # ~/.openclaw/workspace
_DATA_DIR = _WORKSPACE / "data" / "night-shift"

EXECUTION_DIR = _DATA_DIR / "execution"


class CheckpointManager:
    """Save and restore execution state after each phase."""

    def __init__(self, plan_id: str):
        self.plan_id = plan_id
        self.plan_dir = EXECUTION_DIR / plan_id
        self.plan_dir.mkdir(parents=True, exist_ok=True)

    def save_checkpoint(
        self,
        phase_id: int,
        phase_status: str,
        worktree_path: str,
        tokens_used: int = 0,
        duration_seconds: float = 0,
        result_summary: str = "",
    ) -> str:
        """Save state after a phase. Returns checkpoint file path."""
        git_head = self._get_git_head(worktree_path)
        git_diff = self._get_git_diff(worktree_path)

        checkpoint = {
            "plan_id": self.plan_id,
            "phase_id": phase_id,
            "phase_status": phase_status,
            "git_head": git_head,
            "git_diff": git_diff,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tokens_used": tokens_used,
            "duration_seconds": duration_seconds,
            "result_summary": result_summary[:500],
        }

        path = self.plan_dir / f"checkpoint-phase-{phase_id}.json"
        path.write_text(json.dumps(checkpoint, indent=2))
        return str(path)

    def get_last_checkpoint(self) -> dict | None:
        """Get the most recent checkpoint for this plan."""
        if not self.plan_dir.exists():
            return None
        checkpoints = sorted(self.plan_dir.glob("checkpoint-phase-*.json"))
        if not checkpoints:
            return None
        try:
            return json.loads(checkpoints[-1].read_text())
        except (json.JSONDecodeError, IOError):
            return None

    def get_last_successful_phase(self) -> int | None:
        """Get the phase ID of the last successful phase (to resume from)."""
        if not self.plan_dir.exists():
            return None
        checkpoints = sorted(self.plan_dir.glob("checkpoint-phase-*.json"))
        for cp_path in reversed(checkpoints):
            try:
                data = json.loads(cp_path.read_text())
                if data.get("phase_status") in ("passed", "skipped"):
                    return data["phase_id"]
            except (json.JSONDecodeError, IOError):
                continue
        return None

    def save_phase_output(self, phase_id: int, output: str, error: str = ""):
        """Save raw phase output for debugging."""
        self.plan_dir.mkdir(parents=True, exist_ok=True)  # Safety mkdir
        path = self.plan_dir / f"phase-{phase_id}-output.txt"
        content = f"=== OUTPUT ===\n{output}\n\n=== ERROR ===\n{error}\n"
        path.write_text(content[:50000])

    def _get_git_head(self, worktree_path: str) -> str:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=worktree_path,
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.stdout.strip() if result.returncode == 0 else "unknown"
        except Exception:
            return "unknown"

    def _get_git_diff(self, worktree_path: str) -> str:
        try:
            result = subprocess.run(
                ["git", "diff", "--stat"],
                cwd=worktree_path,
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.stdout.strip() if result.returncode == 0 else ""
        except Exception:
            return ""
