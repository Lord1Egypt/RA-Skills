"""Property-based test: Depth command 更新 state.

Feature: llm-booster-skill, Property 7: Depth command 更新 state
Validates: Requirements 2.3, 4.4
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

valid_depth = st.integers(min_value=1, max_value=4)

# Invalid depth values: integers outside 1-4 range
invalid_depth_int = st.one_of(
    st.integers(max_value=0),
    st.integers(min_value=5),
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_state_manager(depth: int = 4) -> SkillStateManager:
    config = BoosterConfig(enabled=True, thinkingDepth=depth)
    return SkillStateManager(config)


def _make_handler(depth: int = 4) -> CLICommandHandler:
    sm = _make_state_manager(depth)
    return CLICommandHandler(sm)


# ---------------------------------------------------------------------------
# Property 7: Depth command 更新 state
# ---------------------------------------------------------------------------


class TestDepthCommandUpdatesStateProperty:
    """**Validates: Requirements 2.3, 4.4**"""

    @settings(max_examples=100)
    @given(new_depth=valid_depth)
    def test_valid_depth_updates_state_manager(self, new_depth: int) -> None:
        """For any valid depth N (1-4), calling set_depth should update
        thinking_depth to N."""
        sm = _make_state_manager()
        sm.set_depth(new_depth)
        assert sm.thinking_depth == new_depth

    @settings(max_examples=100)
    @given(new_depth=valid_depth)
    def test_valid_depth_reflected_in_get_status(self, new_depth: int) -> None:
        """After set_depth(N), get_status().thinking_depth should equal N."""
        sm = _make_state_manager()
        sm.set_depth(new_depth)
        status = sm.get_status()
        assert status.thinking_depth == new_depth

    @settings(max_examples=100)
    @given(new_depth=valid_depth)
    def test_depth_cli_command_updates_state(self, new_depth: int) -> None:
        """Running '/booster depth N' via CLICommandHandler should update
        the underlying state manager's thinking_depth to N."""
        handler = _make_handler()
        result = handler.handle(f"/booster depth {new_depth}")
        assert result.success is True
        assert handler._state_manager.thinking_depth == new_depth

    @settings(max_examples=100)
    @given(new_depth=valid_depth)
    def test_depth_cli_command_status_reflects_change(self, new_depth: int) -> None:
        """After '/booster depth N', a subsequent '/booster status' should
        reflect the new depth value."""
        handler = _make_handler()
        handler.handle(f"/booster depth {new_depth}")
        status_result = handler.handle("/booster status")
        assert str(new_depth) in status_result.message

    @settings(max_examples=100)
    @given(invalid_depth=invalid_depth_int)
    def test_invalid_depth_does_not_change_state(self, invalid_depth: int) -> None:
        """For any depth outside 1-4, set_depth should NOT change
        thinking_depth from its original value."""
        original_depth = 2
        sm = _make_state_manager(depth=original_depth)
        sm.set_depth(invalid_depth)
        assert sm.thinking_depth == original_depth

    @settings(max_examples=100)
    @given(invalid_depth=invalid_depth_int)
    def test_invalid_depth_cli_does_not_change_state(self, invalid_depth: int) -> None:
        """Running '/booster depth <invalid>' should NOT update state."""
        original_depth = 3
        handler = _make_handler(depth=original_depth)
        result = handler.handle(f"/booster depth {invalid_depth}")
        assert result.success is False
        assert handler._state_manager.thinking_depth == original_depth
