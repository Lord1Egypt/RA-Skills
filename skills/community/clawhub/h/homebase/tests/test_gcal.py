"""
Tests for core/gcal.py — the one boundary between homebase and Google.

Everything here is about the command line gcal builds and how it reads what
comes back. The domain rules that decide *what* to ask for (inclusive vs
exclusive end dates, span preservation, which match wins) live one layer up in
calendar_manager and are tested in test_calendar_manager.py.

Two flags are asserted deliberately rather than incidentally, because both
fail silently when missing and both have already cost this workspace real data
elsewhere:

  --all-pages  gog defaults to --max=10; without it a busy fortnight returns
               ten events and the rest read as cancelled.
  --force      gog refuses to delete non-interactively without it and reports
               the refusal on a SUCCESSFUL exit, so a caller sees "deleted".
"""

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from core import gcal


def _run(stdout="{}", returncode=0, stderr=""):
    """Patch subprocess.run and hand back the mock so tests can read argv."""
    result = MagicMock(stdout=stdout, stderr=stderr, returncode=returncode)
    return patch("subprocess.run", return_value=result)


def _argv(mock):
    return mock.call_args.args[0]


# ─── list_events ─────────────────────────────────────────────────────────────

class TestListEvents:
    def test_always_paginates(self):
        """The whole reason this module owns the flag."""
        with _run(json.dumps({"events": []})) as run:
            gcal.list_events("cal-1", "2026-09-01", "2026-09-30")
        assert "--all-pages" in _argv(run)

    def test_requests_the_fields_consumers_need(self):
        with _run(json.dumps({"events": []})) as run:
            gcal.list_events("cal-1", "2026-09-01", "2026-09-30")
        argv = _argv(run)
        fields = argv[argv.index("--fields") + 1]
        # items(...) form is required for a list response; a bare field list is
        # rejected with "Invalid field selection id".
        assert fields.startswith("items(")
        # nextPageToken must be named or --all-pages has no token to follow.
        assert "nextPageToken" in fields
        # recurringEventId is what lets trip_detector skip recurring events.
        assert "recurringEventId" in fields

    def test_passes_the_calendar_and_window(self):
        with _run(json.dumps({"events": []})) as run:
            gcal.list_events("cal-1", "2026-09-01", "2026-09-30")
        argv = _argv(run)
        assert argv[:3] == [gcal.GOG_BIN, "calendar", "events"]
        assert argv[3] == "cal-1"
        assert argv[argv.index("--from") + 1] == "2026-09-01"
        assert argv[argv.index("--to") + 1] == "2026-09-30"

    def test_query_only_sent_when_given(self):
        with _run(json.dumps({"events": []})) as run:
            gcal.list_events("cal-1", "a", "b")
        assert "--query" not in _argv(run)

        with _run(json.dumps({"events": []})) as run:
            gcal.list_events("cal-1", "a", "b", query="Ana")
        argv = _argv(run)
        assert argv[argv.index("--query") + 1] == "Ana"

    def test_returns_the_events_list(self):
        payload = {"events": [{"id": "e1"}, {"id": "e2"}]}
        with _run(json.dumps(payload)):
            assert len(gcal.list_events("c", "a", "b")) == 2

    def test_missing_events_key_is_an_empty_list(self):
        with _run("{}"):
            assert gcal.list_events("c", "a", "b") == []

    def test_a_failure_raises_rather_than_returning_empty(self):
        """An empty calendar and a failed lookup mean opposite things to a
        caller deciding whether to drop cached events."""
        with _run(stdout="", returncode=1, stderr="quota exceeded"):
            with pytest.raises(gcal.GogError) as e:
                gcal.list_events("c", "a", "b")
        assert "quota exceeded" in str(e.value)


# ─── create_event ────────────────────────────────────────────────────────────

class TestCreateEvent:
    def test_all_day_sets_the_flag_and_no_timezone(self):
        with _run() as run:
            gcal.create_event("cal", "Trip", "2026-08-01", "2026-08-02",
                              all_day=True, timezone="America/Los_Angeles")
        argv = _argv(run)
        assert "--all-day" in argv
        # A timezone alongside date-only bounds is what turns an all-day event
        # into a timed one.
        assert "--timezone" not in argv

    def test_timed_sends_the_timezone(self):
        with _run() as run:
            gcal.create_event("cal", "Dentist", "2026-08-01T14:00:00",
                              "2026-08-01T15:00:00",
                              timezone="America/Los_Angeles")
        argv = _argv(run)
        assert "--all-day" not in argv
        assert argv[argv.index("--timezone") + 1] == "America/Los_Angeles"

    def test_blank_description_and_location_are_omitted(self):
        with _run() as run:
            gcal.create_event("cal", "T", "a", "b", description="", location="")
        argv = _argv(run)
        assert "--description" not in argv
        assert "--location" not in argv

    def test_description_and_location_passed_when_present(self):
        with _run() as run:
            gcal.create_event("cal", "T", "a", "b",
                              description="Pack sunscreen", location="Seattle, WA")
        argv = _argv(run)
        assert argv[argv.index("--description") + 1] == "Pack sunscreen"
        assert argv[argv.index("--location") + 1] == "Seattle, WA"


# ─── delete_event ────────────────────────────────────────────────────────────

class TestDeleteEvent:
    def test_always_forces(self):
        """Without --force gog refuses and still exits 0, so the caller would
        read a refusal as a successful delete."""
        with _run() as run:
            gcal.delete_event("cal", "e1")
        assert "--force" in _argv(run)

    def test_already_gone_is_success(self):
        for code in ("404", "410", "notFound"):
            with _run(stdout="", returncode=1, stderr=f"error {code}"):
                gcal.delete_event("cal", "e1")   # must not raise

    def test_a_real_failure_still_raises(self):
        with _run(stdout="", returncode=1, stderr="500 backend error"):
            with pytest.raises(gcal.GogError):
                gcal.delete_event("cal", "e1")


# ─── update_event ────────────────────────────────────────────────────────────

class TestUpdateEvent:
    def test_only_sends_what_changed(self):
        with _run() as run:
            gcal.update_event("cal", "e1", summary="New title")
        argv = _argv(run)
        assert argv[argv.index("--summary") + 1] == "New title"
        assert "--from" not in argv
        assert "--to" not in argv

    def test_all_day_move_sets_the_flag(self):
        with _run() as run:
            gcal.update_event("cal", "e1", start="2026-09-14", end="2026-09-15",
                              all_day=True)
        argv = _argv(run)
        assert "--all-day" in argv
        assert "--timezone" not in argv


# ─── failure modes ───────────────────────────────────────────────────────────

class TestFailureModes:
    def test_non_interactive_and_json_always(self):
        """A prompt under launchd is a hang, not a question."""
        with _run(json.dumps({"events": []})) as run:
            gcal.list_events("c", "a", "b")
        argv = _argv(run)
        assert "--no-input" in argv
        assert "--json" in argv

    def test_missing_binary_is_a_clear_error(self):
        with patch("subprocess.run", side_effect=FileNotFoundError()):
            with pytest.raises(gcal.GogError) as e:
                gcal.list_events("c", "a", "b")
        assert "not found on PATH" in str(e.value)

    def test_timeout_is_a_clear_error(self):
        with patch("subprocess.run",
                   side_effect=subprocess.TimeoutExpired(cmd="gog", timeout=60)):
            with pytest.raises(gcal.GogError) as e:
                gcal.list_events("c", "a", "b")
        assert "timed out" in str(e.value)

    def test_unparseable_output_is_a_clear_error(self):
        with _run(stdout="Syncing with Google..."):
            with pytest.raises(gcal.GogError) as e:
                gcal.list_events("c", "a", "b")
        assert "unparseable JSON" in str(e.value)
