"""Property-based test: Unknown CLI command 返回 help message.

Feature: llm-booster-skill, Property 10: Unknown CLI command 返回 help message
Validates: Requirements 4.5
"""

from __future__ import annotations

import os
import sys

from hypothesis import given, settings, strategies as st, assume

# Ensure the skill package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from cli_handler import CLICommandHandler
from models import BoosterConfig
from state_manager import SkillStateManager

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

KNOWN_COMMANDS = {"enable", "disable", "status", "depth", "help"}

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Generate random strings that are NOT one of the known subcommands.
# We use text() and filter out known commands (case-insensitive).
unknown_command = st.text(min_size=1).filter(
    lambda s: s.strip().lower() not in KNOWN_COMMANDS
    and not s.strip().lower().startswith("/booster")
    and len(s.strip()) > 0
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_handler() -> CLICommandHandler:
    config = BoosterConfig(enabled=True, thinkingDepth=4)
    sm = SkillStateManager(config)
    return CLICommandHandler(sm)


# ---------------------------------------------------------------------------
# Property 10: Unknown CLI command 返回 help message
# ---------------------------------------------------------------------------


class TestUnknownCommandReturnsHelpProperty:
    """**Validates: Requirements 4.5**"""

    @settings(max_examples=100)
    @given(cmd=unknown_command)
    def test_unknown_command_returns_help_listing_all_subcommands(self, cmd: str) -> None:
        """For any string that is not a known subcommand, the CLI handler
        should return a help message that lists all available subcommands."""
        handler = _make_handler()
        result = handler.handle(cmd)

        for known in KNOWN_COMMANDS:
            assert known in result.message, (
                f"Help message missing '{known}' for unknown command {cmd!r}. "
                f"Got: {result.message}"
            )

    @settings(max_examples=100)
    @given(cmd=unknown_command)
    def test_unknown_command_with_booster_prefix_returns_help(self, cmd: str) -> None:
        """For any unknown command passed with /booster prefix, the CLI handler
        should still return a help message listing all subcommands."""
        handler = _make_handler()
        result = handler.handle(f"/booster {cmd}")

        for known in KNOWN_COMMANDS:
            assert known in result.message, (
                f"Help message missing '{known}' for '/booster {cmd}'. "
                f"Got: {result.message}"
            )

    @settings(max_examples=100)
    @given(cmd=unknown_command)
    def test_unknown_command_result_is_successful(self, cmd: str) -> None:
        """The help message returned for unknown commands should have
        success=True (it's a valid help response, not an error)."""
        handler = _make_handler()
        result = handler.handle(cmd)
        assert result.success is True
