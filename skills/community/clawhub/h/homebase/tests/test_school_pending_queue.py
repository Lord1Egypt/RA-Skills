"""
test_school_pending_queue.py — dedup + propose-then-confirm for school emails.

The school email flow must not auto-create calendar events. The agent
dedups via `check_calendar_for_date`, stages events in
`save_pending_school_events`, and only calls the calendar when the family
replies "yes" via `confirm_pending_school_events`. These tests cover the
state machine, not the Gmail / Google Calendar transport.
"""
from __future__ import annotations

import json
import sys
import types
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


import tools  # noqa: E402


@pytest.fixture
def pending_file(tmp_skill_dir, monkeypatch):
    """Redirect the pending queue to a tmp file and return its path."""
    p = tmp_skill_dir / "calendar_data" / "pending_school_events.json"
    monkeypatch.setattr(tools, "_PENDING_SCHOOL_EVENTS_FILE", str(p))
    return p


# ── save + get round-trip ─────────────────────────────────────────────────────


class TestSavePendingSchoolEvents:
    def test_save_writes_entry_but_does_not_call_calendar(self, pending_file):
        with patch("features.calendar.calendar_manager.create_event") as m_create:
            result = tools.save_pending_school_events(
                email_id="msg-abc",
                events=[{"title": "Ana — Spring Picnic", "date": "2026-05-03"}],
            )
        assert "✅" in result
        assert "pending confirmation" in result
        m_create.assert_not_called()  # never touch calendar on save
        data = json.loads(pending_file.read_text())
        assert "msg-abc" in data
        assert data["msg-abc"]["events"][0]["title"] == "Ana — Spring Picnic"
        assert "proposed_at" in data["msg-abc"]

    def test_save_rejects_empty_events(self, pending_file):
        result = tools.save_pending_school_events(email_id="msg-1", events=[])
        assert result.startswith("❌")
        assert not pending_file.exists()

    def test_save_rejects_missing_email_id(self, pending_file):
        result = tools.save_pending_school_events(email_id="", events=[{"title": "x", "date": "2026-01-01"}])
        assert result.startswith("❌")

    def test_save_rejects_event_missing_title_or_date(self, pending_file):
        bad = tools.save_pending_school_events(
            email_id="msg-1", events=[{"title": "ok", "date": "2026-01-01"}, {"title": "bad"}]
        )
        assert bad.startswith("❌")

    def test_save_overwrites_same_email_id(self, pending_file):
        tools.save_pending_school_events("msg-1", [{"title": "v1", "date": "2026-01-01"}])
        tools.save_pending_school_events("msg-1", [{"title": "v2", "date": "2026-01-02"}])
        data = json.loads(pending_file.read_text())
        assert len(data["msg-1"]["events"]) == 1
        assert data["msg-1"]["events"][0]["title"] == "v2"


class TestGetPendingSchoolEvents:
    def test_get_empty_when_file_missing(self, pending_file):
        assert json.loads(tools.get_pending_school_events()) == {}

    def test_get_returns_saved_entries(self, pending_file):
        tools.save_pending_school_events("msg-1", [{"title": "t", "date": "2026-01-01"}])
        data = json.loads(tools.get_pending_school_events())
        assert "msg-1" in data

    def test_get_purges_stale_entries(self, pending_file):
        # Manually write a stale entry (>3 days old)
        from datetime import datetime, timedelta
        stale_ts = (datetime.now() - timedelta(days=10)).isoformat()
        pending_file.write_text(json.dumps({
            "old-msg": {"proposed_at": stale_ts, "events": [{"title": "gone", "date": "2025-01-01"}]},
            "fresh-msg": {"proposed_at": datetime.now().isoformat(), "events": [{"title": "keep", "date": "2026-01-01"}]},
        }))
        data = json.loads(tools.get_pending_school_events())
        assert "old-msg" not in data
        assert "fresh-msg" in data


# ── confirm = only path that creates calendar events ─────────────────────────


class TestConfirmPendingSchoolEvents:
    def test_confirm_creates_events_and_clears_queue(self, pending_file):
        tools.save_pending_school_events("msg-1", [
            {"title": "Ana — Picnic", "date": "2026-05-03"},
            {"title": "Ana — Field Day", "date": "2026-05-10", "time": "09:00"},
        ])
        with patch("features.calendar.calendar_manager.create_event") as m_create:
            m_create.return_value = {"id": "evt-x"}
            result = tools.confirm_pending_school_events(email_id="msg-1")

        assert m_create.call_count == 2
        # All-day call: time_str=None, is_all_day=True
        all_day_call = m_create.call_args_list[0]
        assert all_day_call.kwargs["time_str"] is None
        assert all_day_call.kwargs["is_all_day"] is True
        # Timed call: time_str="09:00", is_all_day=False
        timed_call = m_create.call_args_list[1]
        assert timed_call.kwargs["time_str"] == "09:00"
        assert timed_call.kwargs["is_all_day"] is False

        assert "✅" in result
        assert "Added 2 event(s)" in result
        # Queue cleared
        assert json.loads(pending_file.read_text()) == {}

    def test_confirm_all_when_email_id_empty(self, pending_file):
        tools.save_pending_school_events("msg-1", [{"title": "a", "date": "2026-01-01"}])
        tools.save_pending_school_events("msg-2", [{"title": "b", "date": "2026-01-02"}])
        with patch("features.calendar.calendar_manager.create_event") as m_create:
            m_create.return_value = {"id": "x"}
            result = tools.confirm_pending_school_events()
        assert m_create.call_count == 2
        assert json.loads(pending_file.read_text()) == {}
        assert "Added 2" in result

    def test_confirm_nothing_pending(self, pending_file):
        result = tools.confirm_pending_school_events(email_id="nope")
        assert "No pending" in result

    def test_confirm_unknown_email_id(self, pending_file):
        tools.save_pending_school_events("msg-1", [{"title": "t", "date": "2026-01-01"}])
        result = tools.confirm_pending_school_events(email_id="missing")
        assert "No pending events for email missing" in result
        # Original entry still there
        assert "msg-1" in json.loads(pending_file.read_text())

    def test_confirm_reports_partial_failure(self, pending_file):
        tools.save_pending_school_events("msg-1", [
            {"title": "ok", "date": "2026-01-01"},
            {"title": "boom", "date": "2026-01-02"},
        ])
        calls = {"n": 0}

        def flaky(**kw):
            calls["n"] += 1
            if kw["title"] == "boom":
                raise RuntimeError("calendar down")
            return {"id": "evt"}

        with patch("features.calendar.calendar_manager.create_event", side_effect=flaky):
            result = tools.confirm_pending_school_events(email_id="msg-1")

        assert "Added 1 event(s)" in result
        assert "1 failed" in result
        assert "boom" in result


# ── reject drops without touching the calendar ───────────────────────────────


class TestRejectPendingSchoolEvents:
    def test_reject_drops_entry_without_calling_calendar(self, pending_file):
        tools.save_pending_school_events("msg-1", [{"title": "t", "date": "2026-01-01"}])
        with patch("features.calendar.calendar_manager.create_event") as m_create:
            result = tools.reject_pending_school_events(email_id="msg-1")
        m_create.assert_not_called()
        assert "🗑️" in result
        assert json.loads(pending_file.read_text()) == {}

    def test_reject_all_when_email_id_empty(self, pending_file):
        tools.save_pending_school_events("msg-1", [{"title": "a", "date": "2026-01-01"}])
        tools.save_pending_school_events("msg-2", [{"title": "b", "date": "2026-01-02"}])
        result = tools.reject_pending_school_events()
        assert json.loads(pending_file.read_text()) == {}
        assert "2 pending event(s)" in result

    def test_reject_nothing_pending(self, pending_file):
        assert "No pending" in tools.reject_pending_school_events(email_id="x")


# ── dedup: check_calendar_for_date queries + formats, agent judges match ─────


class TestDispatcher:
    def test_new_tools_are_registered(self, pending_file):
        """execute_tool must route the new tool names to their implementations."""
        tools.save_pending_school_events("msg-1", [{"title": "t", "date": "2026-01-01"}])

        # get_pending_school_events via dispatcher
        out = tools.execute_tool("get_pending_school_events", {})
        assert "msg-1" in out

        # reject_pending_school_events via dispatcher
        out = tools.execute_tool("reject_pending_school_events", {"email_id": "msg-1"})
        assert "🗑️" in out

        # save_pending_school_events via dispatcher
        out = tools.execute_tool(
            "save_pending_school_events",
            {"email_id": "msg-2", "events": [{"title": "x", "date": "2026-01-01"}]},
        )
        assert "✅" in out

        # confirm_pending_school_events via dispatcher
        with patch("features.calendar.calendar_manager.create_event") as m_create:
            m_create.return_value = {"id": "e"}
            out = tools.execute_tool("confirm_pending_school_events", {"email_id": "msg-2"})
        assert "Added 1" in out
