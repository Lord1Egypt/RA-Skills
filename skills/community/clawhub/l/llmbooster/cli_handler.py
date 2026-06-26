"""CLI Command Handler for LLMBooster skill."""

from __future__ import annotations

import json
from pathlib import Path
from models import CommandResult
from state_manager import SkillStateManager


class CLICommandHandler:
    """Parse and dispatch /booster subcommands.

    Supports: enable, disable, status, stats, depth <N>, help.
    """

    KNOWN_COMMANDS = ["enable", "disable", "status", "stats", "depth", "help"]
    STATS_FILE = Path(__file__).parent / "booster_stats.json"

    def __init__(self, state_manager: SkillStateManager) -> None:
        self._state_manager = state_manager

    def handle(self, command_str: str) -> CommandResult:
        """Parse command string and dispatch to appropriate handler.

        Accepts formats like "/booster enable", "/booster depth 3",
        "enable", "depth 3".
        Unknown subcommand → return help message.
        """
        parts = command_str.strip().split()

        # Strip leading "/booster" prefix if present
        if parts and parts[0].lower() == "/booster":
            parts = parts[1:]

        if not parts:
            return self._help()

        subcommand = parts[0].lower()

        if subcommand == "enable":
            return self._enable()
        elif subcommand == "disable":
            return self._disable()
        elif subcommand == "status":
            return self._status()
        elif subcommand == "stats":
            return self._stats()
        elif subcommand == "depth":
            return self._depth(parts[1:])
        elif subcommand == "help":
            return self._help()
        else:
            return self._help()

    def _enable(self) -> CommandResult:
        message = self._state_manager.set_enabled(True)
        return CommandResult(success=True, message=message)

    def _disable(self) -> CommandResult:
        message = self._state_manager.set_enabled(False)
        return CommandResult(success=True, message=message)

    def _status(self) -> CommandResult:
        status = self._state_manager.get_status()
        state_label = "enabled" if status.enabled else "disabled"
        message = (
            f"LLMBooster is {state_label}.\n"
            f"Thinking depth: {status.thinking_depth}\n"
            f"Tasks processed: {status.tasks_processed}"
        )
        return CommandResult(success=True, message=message)

    def _stats(self) -> CommandResult:
        """Show detailed usage statistics."""
        status = self._state_manager.get_status()

        # Load persisted stats
        stats_data = {}
        if self.STATS_FILE.exists():
            try:
                stats_data = json.loads(self.STATS_FILE.read_text())
            except json.JSONDecodeError:
                pass

        state_label = "enabled" if status.enabled else "disabled"
        last_used = stats_data.get("last_used", "never")

        message = (
            f"📊 **BoosterStatistics**\n"
            f"───────────────────────\n"
            f"Status: {state_label}\n"
            f"Thinking Depth: {status.thinking_depth}\n"
            f"Tasks Processed: {status.tasks_processed}\n"
            f"Last Used: {last_used}\n"
            f"───────────────────────\n"
            f"Depth Guide:\n"
            f"  1 = Plan only (quick)\n"
            f"  2 = Plan → Draft (fast)\n"
            f"  3 = + Self-Critique (balanced)\n"
            f"  4 = + Refine (complete)"
        )
        return CommandResult(success=True, message=message)

    def _depth(self, args: list[str]) -> CommandResult:
        if not args:
            return CommandResult(
                success=False,
                message="Invalid depth. Please provide a value between 1 and 4.",
            )

        try:
            value = int(args[0])
        except ValueError:
            return CommandResult(
                success=False,
                message="Invalid depth. Please provide a value between 1 and 4.",
            )

        result_message = self._state_manager.set_depth(value)
        success = self._state_manager.thinking_depth == value
        return CommandResult(success=success, message=result_message)

    def _help(self) -> CommandResult:
        message = (
            "Available commands:\n"
            "  /booster enable   - Enable LLMBooster\n"
            "  /booster disable  - Disable LLMBooster\n"
            "  /booster status   - Show current status\n"
            "  /booster stats    - Show usage statistics\n"
            "  /booster depth <N> - Set thinking depth (1-4)\n"
            "  /booster help     - Show this help message"
        )
        return CommandResult(success=True, message=message)
