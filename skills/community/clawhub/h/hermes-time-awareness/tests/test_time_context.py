"""Tests for hermes-time-awareness plugin."""

import time
from datetime import datetime, timezone
from unittest.mock import patch

import sys
from pathlib import Path

# Ensure plugin root is importable
_plugin_root = str(Path(__file__).resolve().parent.parent)
if _plugin_root not in sys.path:
    sys.path.insert(0, _plugin_root)

from time_awareness.time_context import (
    _format_elapsed,
    _get_idle_seconds,
    format_time_context,
    record_user_message,
    _last_user_ts,
    _last_user_ts_lock,
)


class TestFormatElapsed:
    def test_just_now(self):
        assert _format_elapsed(30) == "just now"

    def test_minutes(self):
        assert _format_elapsed(90) == "1m"
        assert _format_elapsed(3599) == "59m"

    def test_hours(self):
        assert _format_elapsed(3600) == "1h"
        assert _format_elapsed(3660) == "1h1m"
        assert _format_elapsed(7200) == "2h"

    def test_days(self):
        assert _format_elapsed(86400) == "1d"
        assert _format_elapsed(90000) == "1d1h"


class TestFormatTimeContext:
    def test_basic_output(self):
        ctx = format_time_context()
        assert ctx.startswith("[time:")
        assert "]" in ctx
        # Should contain date and time
        now = datetime.now()
        assert str(now.year) in ctx

    def test_first_turn_no_idle(self):
        ctx = format_time_context(
            session_id="test",
            conversation_history=[{"role": "user", "content": "hi"}],
            is_first_turn=True,
        )
        assert "idle:" not in ctx

    def test_idle_with_history(self):
        # Simulate a message from 5 minutes ago
        five_min_ago = time.time() - 300
        history = [
            {"role": "user", "content": "first", "timestamp": five_min_ago},
            {"role": "assistant", "content": "reply"},
        ]
        ctx = format_time_context(
            session_id="test-session",
            conversation_history=history,
            is_first_turn=False,
        )
        assert "idle:" in ctx
        assert "5m" in ctx

    def test_no_idle_for_short_gap(self):
        # Message from 10 seconds ago — below 60s threshold
        ten_sec_ago = time.time() - 10
        history = [
            {"role": "user", "content": "first", "timestamp": ten_sec_ago},
            {"role": "assistant", "content": "reply"},
        ]
        ctx = format_time_context(
            session_id="test-session",
            conversation_history=history,
            is_first_turn=False,
        )
        assert "idle:" not in ctx

    def test_never_throws(self):
        # Malformed inputs should return empty string, not raise
        assert isinstance(format_time_context(conversation_history="garbage"), str)
        assert isinstance(format_time_context(conversation_history=[{}]), str)
        assert isinstance(format_time_context(session_id="", conversation_history=None), str)


class TestRecordUserMessage:
    def test_records_timestamp(self):
        with _last_user_ts_lock:
            _last_user_ts.pop("test-abc", None)
        record_user_message("test-abc")
        with _last_user_ts_lock:
            assert "test-abc" in _last_user_ts

    def test_fallback_idle(self):
        # Record a message, then check idle is detected from in-process record
        record_user_message("test-fallback", ts=time.time() - 120)
        history = [{"role": "user", "content": "hi"}]  # No timestamp
        idle = _get_idle_seconds("test-fallback", history)
        assert idle is not None
        assert 115 < idle < 125  # ~120 seconds


class TestHooksIntegration:
    def test_hook_returns_context(self):
        from hooks import on_pre_llm_call
        result = on_pre_llm_call(session_id="test-hook")
        assert isinstance(result, dict)
        if result:  # May be empty if format_time_context fails
            assert "context" in result
            assert result["context"].startswith("[time:")

    def test_hook_never_throws(self):
        from hooks import on_pre_llm_call
        # Should not raise even with bad inputs
        result = on_pre_llm_call(
            session_id="",
            conversation_history=None,
            is_first_turn=True,
        )
        assert isinstance(result, dict)
