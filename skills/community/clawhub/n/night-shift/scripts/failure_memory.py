"""Failure memory — classify and track failures to avoid repeating mistakes."""

from __future__ import annotations
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

# Auto-detect workspace root
_SKILL_DIR = Path(__file__).resolve().parent.parent  # skills/night-shift/
_WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", _SKILL_DIR.parent.parent))  # ~/.openclaw/workspace
_DATA_DIR = _WORKSPACE / "data" / "night-shift"

FAILURE_TYPES = [
    "context_overflow",
    "verification_failed",
    "hallucinated_progress",
    "wrong_approach",
    "dependency_missing",
    "timeout",
    "budget_exceeded",
    "git_conflict",
    "integration_gap",
    "oom_kill",
    "lock_conflict",
    "cursor_hang",
    "subagent_error",
    "unknown",
]

DEFAULT_PATH = _DATA_DIR / "failure-memory.json"


class FailureMemory:
    """Classify failures and detect similar past failures."""

    def __init__(self, path: Path = DEFAULT_PATH):
        self.path = path
        self.failures: list[dict] = []
        self._load()

    def prompt_hash(self, prompt: str) -> str:
        """Deterministic SHA256 hash (not Python hash() — that's non-deterministic)."""
        return hashlib.sha256(prompt.encode()).hexdigest()[:16]

    def log_failure(
        self,
        plan_id: str,
        phase_id: int,
        error_type: str,
        details: str = "",
        prompt: str = "",
        attempt: int = 0,
    ):
        if error_type not in FAILURE_TYPES:
            error_type = "unknown"
        failure = {
            "plan_id": plan_id,
            "phase_id": phase_id,
            "error_type": error_type,
            "details": details[:1000],
            "prompt_hash": self.prompt_hash(prompt) if prompt else "",
            "attempt": attempt,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.failures.append(failure)
        self._save()

    def get_similar_failures(self, prompt: str) -> list[dict]:
        """Find past failures with similar prompts."""
        h = self.prompt_hash(prompt)
        return [f for f in self.failures if f.get("prompt_hash") == h]

    def get_failures_for_plan(self, plan_id: str) -> list[dict]:
        return [f for f in self.failures if f["plan_id"] == plan_id]

    def get_failure_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for f in self.failures:
            t = f["error_type"]
            counts[t] = counts.get(t, 0) + 1
        return counts

    def should_skip_retry(self, prompt: str, max_attempts: int = 2) -> bool:
        """Check if this prompt has already failed max_attempts times."""
        similar = self.get_similar_failures(prompt)
        return len(similar) >= max_attempts

    def _load(self):
        if self.path.exists():
            try:
                self.failures = json.loads(self.path.read_text())
            except (json.JSONDecodeError, IOError):
                self.failures = []

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.failures, indent=2))
