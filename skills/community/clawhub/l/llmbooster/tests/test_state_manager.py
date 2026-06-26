"""Unit tests for SkillStateManager."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models import BoosterConfig, StatusInfo
from state_manager import SkillStateManager


class TestSkillStateManagerInit:
    """Tests for __init__ initialization from config."""

    def test_init_from_default_config(self):
        config = BoosterConfig()
        mgr = SkillStateManager(config)
        assert mgr.enabled is True
        assert mgr.thinking_depth == 4
        assert mgr.tasks_processed == 0

    def test_init_from_custom_config(self):
        config = BoosterConfig(enabled=False, thinkingDepth=2, maxRetries=5)
        mgr = SkillStateManager(config)
        assert mgr.enabled is False
        assert mgr.thinking_depth == 2
        assert mgr.tasks_processed == 0


class TestSetEnabled:
    """Tests for set_enabled method."""

    def test_enable(self):
        mgr = SkillStateManager(BoosterConfig(enabled=False))
        result = mgr.set_enabled(True)
        assert mgr.enabled is True
        assert "enabled" in result.lower()

    def test_disable(self):
        mgr = SkillStateManager(BoosterConfig(enabled=True))
        result = mgr.set_enabled(False)
        assert mgr.enabled is False
        assert "disabled" in result.lower()

    def test_returns_string(self):
        mgr = SkillStateManager(BoosterConfig())
        result = mgr.set_enabled(True)
        assert isinstance(result, str)


class TestSetDepth:
    """Tests for set_depth method."""

    def test_valid_depth_1(self):
        mgr = SkillStateManager(BoosterConfig())
        result = mgr.set_depth(1)
        assert mgr.thinking_depth == 1
        assert "1" in result

    def test_valid_depth_4(self):
        mgr = SkillStateManager(BoosterConfig())
        result = mgr.set_depth(4)
        assert mgr.thinking_depth == 4
        assert "4" in result

    def test_invalid_depth_0(self):
        mgr = SkillStateManager(BoosterConfig())
        original = mgr.thinking_depth
        result = mgr.set_depth(0)
        assert mgr.thinking_depth == original
        assert "1" in result and "4" in result

    def test_invalid_depth_5(self):
        mgr = SkillStateManager(BoosterConfig())
        original = mgr.thinking_depth
        result = mgr.set_depth(5)
        assert mgr.thinking_depth == original
        assert "1" in result and "4" in result

    def test_invalid_depth_negative(self):
        mgr = SkillStateManager(BoosterConfig())
        original = mgr.thinking_depth
        result = mgr.set_depth(-1)
        assert mgr.thinking_depth == original

    def test_invalid_depth_bool_rejected(self):
        mgr = SkillStateManager(BoosterConfig())
        original = mgr.thinking_depth
        result = mgr.set_depth(True)
        assert mgr.thinking_depth == original


class TestGetStatus:
    """Tests for get_status method."""

    def test_returns_status_info(self):
        mgr = SkillStateManager(BoosterConfig())
        status = mgr.get_status()
        assert isinstance(status, StatusInfo)

    def test_reflects_current_state(self):
        mgr = SkillStateManager(BoosterConfig(enabled=False, thinkingDepth=2))
        status = mgr.get_status()
        assert status.enabled is False
        assert status.thinking_depth == 2
        assert status.tasks_processed == 0

    def test_reflects_mutations(self):
        mgr = SkillStateManager(BoosterConfig())
        mgr.set_enabled(False)
        mgr.set_depth(2)
        mgr.increment_tasks()
        status = mgr.get_status()
        assert status.enabled is False
        assert status.thinking_depth == 2
        assert status.tasks_processed == 1


class TestIncrementTasks:
    """Tests for increment_tasks method."""

    def test_increments_from_zero(self):
        mgr = SkillStateManager(BoosterConfig())
        mgr.increment_tasks()
        assert mgr.tasks_processed == 1

    def test_increments_multiple_times(self):
        mgr = SkillStateManager(BoosterConfig())
        for _ in range(5):
            mgr.increment_tasks()
        assert mgr.tasks_processed == 5
