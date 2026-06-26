"""Skill State Manager for LLMBooster."""

from __future__ import annotations

import json
from pathlib import Path
from models import BoosterConfig, StatusInfo


class SkillStateManager:
    """Manages LLMBooster's runtime state.

    Including enabled/disabled, current thinkingDepth, session statistics.
    Persists statistics to booster_stats.json for tracking across sessions.
    """

    STATS_FILE = Path(__file__).parent / "booster_stats.json"

    def __init__(self, config: BoosterConfig) -> None:
        self.enabled: bool = config.enabled
        self.thinking_depth: int = config.thinkingDepth
        self.tasks_processed: int = 0
        self._load_stats()

    def _load_stats(self) -> None:
        """Load persisted statistics from file."""
        if self.STATS_FILE.exists():
            try:
                data = json.loads(self.STATS_FILE.read_text())
                self.tasks_processed = data.get("tasks_processed", 0)
            except (json.JSONDecodeError, KeyError):
                self.tasks_processed = 0

    def _save_stats(self) -> None:
        """Save statistics to file."""
        from datetime import datetime
        data = {
            "tasks_processed": self.tasks_processed,
            "last_used": datetime.now().isoformat(),
            "thinking_depth": self.thinking_depth,
        }
        self.STATS_FILE.write_text(json.dumps(data, indent=2))

    def set_enabled(self, enabled: bool) -> str:
        """Toggle enabled state, return confirmation message."""
        self.enabled = enabled
        state_label = "enabled" if enabled else "disabled"
        return f"LLMBooster {state_label}."

    def set_depth(self, depth: int) -> str:
        """Set thinking depth (1-4), return confirmation or error message."""
        if not isinstance(depth, int) or isinstance(depth, bool) or depth < 1 or depth > 4:
            return "Invalid depth. Please provide a value between 1 and 4."
        self.thinking_depth = depth
        self._save_stats()
        return f"Thinking depth set to {depth}."

    def get_status(self) -> StatusInfo:
        """Return current state snapshot."""
        return StatusInfo(
            enabled=self.enabled,
            thinking_depth=self.thinking_depth,
            tasks_processed=self.tasks_processed,
        )

    def increment_tasks(self) -> None:
        """Increment counter after task completion and persist to file."""
        self.tasks_processed += 1
        self._save_stats()
