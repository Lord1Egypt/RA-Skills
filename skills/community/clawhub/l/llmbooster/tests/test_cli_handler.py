"""Unit tests for CLICommandHandler."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from cli_handler import CLICommandHandler
from models import BoosterConfig
from state_manager import SkillStateManager


def _make_handler(enabled=True, depth=4) -> CLICommandHandler:
    config = BoosterConfig(enabled=enabled, thinkingDepth=depth)
    sm = SkillStateManager(config)
    return CLICommandHandler(sm)


class TestEnable:
    def test_enable_returns_success(self):
        handler = _make_handler(enabled=False)
        result = handler.handle("enable")
        assert result.success is True
        assert "enabled" in result.message.lower()

    def test_enable_with_prefix(self):
        handler = _make_handler(enabled=False)
        result = handler.handle("/booster enable")
        assert result.success is True
        assert "enabled" in result.message.lower()

    def test_enable_updates_state(self):
        handler = _make_handler(enabled=False)
        handler.handle("enable")
        assert handler._state_manager.enabled is True


class TestDisable:
    def test_disable_returns_success(self):
        handler = _make_handler(enabled=True)
        result = handler.handle("disable")
        assert result.success is True
        assert "disabled" in result.message.lower()

    def test_disable_with_prefix(self):
        handler = _make_handler(enabled=True)
        result = handler.handle("/booster disable")
        assert result.success is True
        assert "disabled" in result.message.lower()

    def test_disable_updates_state(self):
        handler = _make_handler(enabled=True)
        handler.handle("disable")
        assert handler._state_manager.enabled is False


class TestStatus:
    def test_status_contains_enabled(self):
        handler = _make_handler(enabled=True, depth=3)
        result = handler.handle("status")
        assert result.success is True
        assert "enabled" in result.message.lower()

    def test_status_contains_depth(self):
        handler = _make_handler(depth=2)
        result = handler.handle("status")
        assert "2" in result.message

    def test_status_contains_tasks_processed(self):
        handler = _make_handler()
        result = handler.handle("status")
        assert "0" in result.message

    def test_status_with_prefix(self):
        handler = _make_handler()
        result = handler.handle("/booster status")
        assert result.success is True


class TestDepth:
    def test_depth_valid_value(self):
        handler = _make_handler(depth=1)
        result = handler.handle("depth 3")
        assert result.success is True
        assert "3" in result.message
        assert handler._state_manager.thinking_depth == 3

    def test_depth_with_prefix(self):
        handler = _make_handler()
        result = handler.handle("/booster depth 2")
        assert result.success is True
        assert handler._state_manager.thinking_depth == 2

    def test_depth_no_argument(self):
        handler = _make_handler()
        result = handler.handle("depth")
        assert result.success is False
        assert "1" in result.message and "4" in result.message

    def test_depth_non_numeric(self):
        handler = _make_handler()
        result = handler.handle("depth abc")
        assert result.success is False
        assert "1" in result.message and "4" in result.message

    def test_depth_out_of_range_high(self):
        handler = _make_handler(depth=2)
        result = handler.handle("depth 5")
        assert result.success is False
        assert handler._state_manager.thinking_depth == 2

    def test_depth_out_of_range_low(self):
        handler = _make_handler(depth=2)
        result = handler.handle("depth 0")
        assert result.success is False
        assert handler._state_manager.thinking_depth == 2


class TestHelp:
    def test_help_lists_subcommands(self):
        handler = _make_handler()
        result = handler.handle("help")
        assert result.success is True
        for cmd in CLICommandHandler.KNOWN_COMMANDS:
            assert cmd in result.message

    def test_help_with_prefix(self):
        handler = _make_handler()
        result = handler.handle("/booster help")
        assert result.success is True


class TestUnknownCommand:
    def test_unknown_returns_help(self):
        handler = _make_handler()
        result = handler.handle("foobar")
        for cmd in CLICommandHandler.KNOWN_COMMANDS:
            assert cmd in result.message

    def test_empty_string_returns_help(self):
        handler = _make_handler()
        result = handler.handle("")
        for cmd in CLICommandHandler.KNOWN_COMMANDS:
            assert cmd in result.message

    def test_only_prefix_returns_help(self):
        handler = _make_handler()
        result = handler.handle("/booster")
        for cmd in CLICommandHandler.KNOWN_COMMANDS:
            assert cmd in result.message
