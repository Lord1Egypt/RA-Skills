"""
Tests for core/gcal.py — the one boundary between homebase and Google.

Everything here is about the command line gcal builds and how it reads what
comes back. gcal is read-only since 2026-10-22.

--all-pages is asserted deliberately rather than incidentally, because it
fails silently when missing: gog defaults to --max=10, and without it a busy
fortnight returns ten events and the rest read as cancelled.
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
