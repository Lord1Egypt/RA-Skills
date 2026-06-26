"""Property-based test: Status output 包含所有必要資訊.

Feature: llm-booster-skill, Property 9: Status output 包含所有必要資訊
Validates: Requirements 4.3
"""

from __future__ import annotations

import os
import sys

from hypothesis import given, settings, strategies as st

# Ensure the skill package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from cli_handler import CLICommandHandler
from models import BoosterConfig
from state_manager import SkillStateManager

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

enabled_st = st.booleans()
thinking_depth_st = st.integers(min_value=1, max_value=4)
tasks_processed_st = st.integers(min_value=0, max_value=10_000)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_state_manager(
    enabled: bool, thinking_depth: int, tasks_processed: int
) -> SkillStateManager:
    config = BoosterConfig(enabled=enabled, thinkingDepth=thinking_depth)
    sm = SkillStateManager(config)
    sm.tasks_processed = tasks_processed
    return sm


# ---------------------------------------------------------------------------
# Property 9: Status output 包含所有必要資訊
# ---------------------------------------------------------------------------


class TestStatusOutputContainsAllInfoProperty:
    """**Validates: Requirements 4.3**"""

    @settings(max_examples=100)
    @given(
        enabled=enabled_st,
        thinking_depth=thinking_depth_st,
        tasks_processed=tasks_processed_st,
    )
    def test_get_status_contains_all_values(
        self, enabled: bool, thinking_depth: int, tasks_processed: int
    ) -> None:
        """For any state combination, get_status() should return a StatusInfo
        that contains the correct enabled state, thinking depth, and tasks
        processed count."""
        sm = _make_state_manager(enabled, thinking_depth, tasks_processed)
        status = sm.get_status()

        assert status.enabled == enabled
        assert status.thinking_depth == thinking_depth
        assert status.tasks_processed == tasks_processed

    @settings(max_examples=100)
    @given(
        enabled=enabled_st,
        thinking_depth=thinking_depth_st,
        tasks_processed=tasks_processed_st,
    )
    def test_cli_status_message_contains_enabled_state(
        self, enabled: bool, thinking_depth: int, tasks_processed: int
    ) -> None:
        """The CLI '/booster status' message should contain a representation
        of the enabled state (either 'enabled' or 'disabled')."""
        sm = _make_state_manager(enabled, thinking_depth, tasks_processed)
        handler = CLICommandHandler(sm)
        result = handler.handle("/booster status")

        expected_label = "enabled" if enabled else "disabled"
        assert expected_label in result.message

    @settings(max_examples=100)
    @given(
        enabled=enabled_st,
        thinking_depth=thinking_depth_st,
        tasks_processed=tasks_processed_st,
    )
    def test_cli_status_message_contains_thinking_depth(
        self, enabled: bool, thinking_depth: int, tasks_processed: int
    ) -> None:
        """The CLI '/booster status' message should contain the current
        thinking depth value."""
        sm = _make_state_manager(enabled, thinking_depth, tasks_processed)
        handler = CLICommandHandler(sm)
        result = handler.handle("/booster status")

        assert str(thinking_depth) in result.message

    @settings(max_examples=100)
    @given(
        enabled=enabled_st,
        thinking_depth=thinking_depth_st,
        tasks_processed=tasks_processed_st,
    )
    def test_cli_status_message_contains_tasks_processed(
        self, enabled: bool, thinking_depth: int, tasks_processed: int
    ) -> None:
        """The CLI '/booster status' message should contain the tasks
        processed count."""
        sm = _make_state_manager(enabled, thinking_depth, tasks_processed)
        handler = CLICommandHandler(sm)
        result = handler.handle("/booster status")

        assert str(tasks_processed) in result.message
