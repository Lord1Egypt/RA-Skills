"""
test_calendar_aggregator_sync.py — sync_with_google_calendar() event titling.

An event with no `summary` (e.g. a work calendar whose admin policy strips
titles from synced busy blocks) syncs with the literal title "Untitled".
These events are deliberately KEPT in the shared calendar cache — conflict
checks against real busy time (e.g. the morning briefing's schedule view)
still need their time slot to avoid treating a real, if unlabeled, meeting
as free. It's the *display* layers (morning briefing, get_events_for_date,
get_next_event — see their own test files) that filter "Untitled" out
before anything reaches the user.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from features.calendar.calendar_aggregator import FamilyCalendarAggregator


def _mock_google_events(items):
    """Patch the single gog call the aggregator makes, returning `items`.

    One seam since 2026-09-07. This used to need two patches — the credential
    builder and googleapiclient's `build()` — because the aggregator
    constructed its own Google service. It now calls core.gcal.list_events and
    owns no credentials at all.

    `items` are Google-shaped (start/end as {'dateTime'} or {'date'}), which is
    what gog returns verbatim, so the fixtures below did not have to change.
    """
    return patch("core.gcal.list_events", return_value=items)


class TestUntitledEventsKeptInCache:
    def test_event_with_no_summary_syncs_as_untitled(self, tmp_skill_dir):
        agg = FamilyCalendarAggregator(str(tmp_skill_dir))
        agg.config["supported_calendars"] = [
            {"name": "Work Calendar", "type": "google", "id": "work@x.com", "enabled": True}
        ]

        items = [
            {"id": "e1", "start": {"dateTime": "2026-08-01T09:00:00"}, "end": {"dateTime": "2026-08-01T10:00:00"}},
            {"id": "e2", "summary": "", "start": {"dateTime": "2026-08-01T11:00:00"}, "end": {"dateTime": "2026-08-01T12:00:00"}},
            {"id": "e3", "summary": "Board meeting", "start": {"dateTime": "2026-08-01T14:00:00"}, "end": {"dateTime": "2026-08-01T15:00:00"}},
        ]
        with _mock_google_events(items):
            agg.sync_with_google_calendar()

        titles = {e["title"] for e in agg.calendar.values()}
        assert titles == {"Untitled", "Board meeting"}
        # The time slot is still there for busy-block/conflict checks.
        assert agg.calendar["e1"]["time"] == "09:00"
        assert agg.calendar["e2"]["time"] == "11:00"


class TestSyncFreshnessTTL:
    """The TTL short-circuit returns True — the same value a real sync returns
    — without contacting Google at all. Callers cannot tell the two apart, and
    none of it had a test: the marker guard, the force bypass, and the
    detect_restaurants opt-in were all unexercised."""

    def _one_calendar(self, agg):
        agg.config["supported_calendars"] = [
            {"name": "Family Calendar", "type": "google", "id": "f@x.com", "enabled": True}
        ]

    def test_a_fresh_marker_skips_the_api_call(self, tmp_skill_dir):
        agg = FamilyCalendarAggregator(str(tmp_skill_dir))
        self._one_calendar(agg)
        agg._record_sync()
        with _mock_google_events([]) as fetch:
            assert agg.sync_with_google_calendar() is True
        fetch.assert_not_called()

    def test_force_bypasses_a_fresh_marker(self, tmp_skill_dir):
        agg = FamilyCalendarAggregator(str(tmp_skill_dir))
        self._one_calendar(agg)
        agg._record_sync()
        with _mock_google_events([]) as fetch:
            agg.sync_with_google_calendar(force=True)
        fetch.assert_called()

    def test_a_total_outage_does_not_mark_the_sync_fresh(self, tmp_skill_dir):
        """Otherwise one outage suppresses every retry for the whole TTL."""
        agg = FamilyCalendarAggregator(str(tmp_skill_dir))
        self._one_calendar(agg)
        with patch("core.gcal.list_events", side_effect=Exception("503")):
            agg.sync_with_google_calendar()
        assert not os.path.exists(agg.sync_marker_file)

    def test_a_partial_outage_does_not_mark_the_sync_fresh(self, tmp_skill_dir):
        """Freshness has to mean EVERY enabled calendar is fresh. With a
        per-calendar token refresh, one failing while the other succeeds is the
        plausible case, and `any_succeeded` then served a cache holding stale
        data for the failed calendar to every non-forced reader."""
        agg = FamilyCalendarAggregator(str(tmp_skill_dir))
        agg.config["supported_calendars"] = [
            {"name": "Family Calendar", "type": "google", "id": "f@x.com", "enabled": True},
            {"name": "Work Calendar", "type": "google", "id": "w@x.com", "enabled": True},
        ]
        # First calendar returns cleanly, second raises: the mixed case that
        # `any_succeeded` used to mark fresh.
        with patch("core.gcal.list_events", side_effect=[[], Exception("503")]):
            agg.sync_with_google_calendar()
        assert not os.path.exists(agg.sync_marker_file)

    def test_a_corrupt_marker_falls_open_to_a_real_sync(self, tmp_skill_dir):
        """The marker is a disposable cache. A shape it cannot read must mean
        "sync now", not AttributeError out of every calendar tool."""
        agg = FamilyCalendarAggregator(str(tmp_skill_dir))
        self._one_calendar(agg)
        with open(agg.sync_marker_file, "w") as f:
            f.write('"not a dict"')
        assert agg._seconds_since_sync() is None
        with _mock_google_events([]) as fetch:
            agg.sync_with_google_calendar()
        fetch.assert_called()


class TestRestaurantDetectionIsOptIn:
    """_detect_restaurant_events is a WRITE. It used to run on every sync, so
    asking "what's on today" appended to restaurants.json."""

    def test_a_read_only_sync_does_not_write_restaurants(self, tmp_skill_dir):
        agg = FamilyCalendarAggregator(str(tmp_skill_dir))
        agg.config["supported_calendars"] = []
        with patch.object(agg, "_detect_restaurant_events") as det:
            agg.sync_with_google_calendar(force=True)
        det.assert_not_called()

    def test_opting_in_runs_detection(self, tmp_skill_dir):
        agg = FamilyCalendarAggregator(str(tmp_skill_dir))
        agg.config["supported_calendars"] = []
        with patch.object(agg, "_detect_restaurant_events") as det:
            agg.sync_with_google_calendar(force=True, detect_restaurants=True)
        det.assert_called_once()


class TestDisabledCalendarsAreEvicted:
    """Disabling a calendar must remove its events, not merely stop refreshing
    them.

    The per-calendar invalidation is deliberately narrow: it drops only events
    from calendars it actually synced, so one calendar failing does not empty
    the briefing. The gap that left was that a DISABLED calendar is never
    synced, so nothing ever dropped its rows. Turning off the work calendar on
    2026-09-07 stopped 225 events being refreshed and removed none of them —
    they would have aged in the cache indefinitely, still visible to every
    reader.
    """

    def test_events_from_a_disabled_calendar_are_dropped(self, tmp_skill_dir):
        agg = FamilyCalendarAggregator(str(tmp_skill_dir))
        agg.config["supported_calendars"] = [
            {"name": "Family Calendar", "type": "google", "id": "f@x.com", "enabled": True},
            {"name": "Work Calendar", "type": "google", "id": "w@x.com", "enabled": False},
        ]
        # A leftover from when Work was enabled.
        agg.calendar["old"] = {
            "id": "old", "title": "Standup", "date": "2026-09-07",
            "calendar_source": "Work Calendar",
        }
        with _mock_google_events([]):
            agg.sync_with_google_calendar(force=True)
        assert "old" not in agg.calendar, "disabled calendar's events survived"

    def test_events_from_an_enabled_calendar_are_untouched_by_eviction(self, tmp_skill_dir):
        """Eviction keys on configuration, not on whether a sync succeeded —
        a calendar that is enabled but failing keeps its cached events."""
        agg = FamilyCalendarAggregator(str(tmp_skill_dir))
        agg.config["supported_calendars"] = [
            {"name": "Family Calendar", "type": "google", "id": "f@x.com", "enabled": True},
        ]
        agg.calendar["keep"] = {
            "id": "keep", "title": "Dentist", "date": "2026-10-30",   # outside the window
            "calendar_source": "Family Calendar",
        }
        with patch("core.gcal.list_events", side_effect=Exception("503")):
            agg.sync_with_google_calendar(force=True)
        assert "keep" in agg.calendar, "a failing calendar lost its cache"
