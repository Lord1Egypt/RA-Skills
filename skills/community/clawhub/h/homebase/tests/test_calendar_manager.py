"""
Tests for features/calendar/calendar_manager.py.

Since 2026-09-07 calendar_manager owns no Google client: it computes what
should change and hands it to core.gcal, which shells out to the `gog` CLI.
These tests assert on what it passes to that boundary — the date arithmetic,
the inclusive/exclusive conversion, the span preservation, the
which-match-wins rules — because that is what this module is actually for.

How gcal turns those arguments into a gog command line is tested in
tests/test_gcal.py, one layer down.

TestServiceMemoization is gone with the thing it tested. It covered
`get_calendar_service` building one memoized service per process so that
confirm_pending_school_events' create-in-a-loop did not force five OAuth
refreshes. There is no service to memoize now; gog authenticates per
invocation. The cost that regression was about is noted in calendar_manager's
Auth section rather than asserted here, because there is no longer a code path
to assert against.
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from features.calendar import calendar_manager as cm


def _created():
    """Patch the create boundary. Returns the mock so callers can read the
    arguments calendar_manager decided on."""
    return patch("core.gcal.create_event", return_value={"id": "evt", "summary": "x"})


def _listing(events):
    return patch("core.gcal.list_events", return_value=events)


# ─── create_event ─────────────────────────────────────────────────────────────

class TestCreateEvent:
    def test_all_day_event_uses_an_exclusive_end(self):
        """
        CONTRACT CHANGE 2026-08-28: this asserted end.date == start.date.

        That was wrong against the Google API, whose all-day `end.date` is
        EXCLUSIVE — equal dates describe a zero-length span. It survived
        because Google normalizes that case for a single day, so single-day
        events looked fine and nothing else was ever attempted. It also made
        multi-day all-day events impossible to express, which is what surfaced
        it: a travel window has to say when it ends.
        """
        with _created() as mk:
            result = cm.create_event(title="Trip", date_str="2026-08-01", is_all_day=True)

        assert result == {"id": "evt", "summary": "x"}
        args, kwargs = mk.call_args
        assert args[0] == cm.CALENDAR_ID
        assert args[1] == "Trip"
        assert args[2] == "2026-08-01"
        assert args[3] == "2026-08-02"
        assert kwargs["all_day"] is True

    def test_multiday_all_day_event_ends_the_day_after_its_last(self):
        """`end_date` is the inclusive last day; Google is told the day after."""
        with _created() as mk:
            cm.create_event(title="Trip to Seattle", date_str="2026-08-29",
                            end_date="2026-09-06", is_all_day=True,
                            location="Seattle, WA")

        args, kwargs = mk.call_args
        assert args[2] == "2026-08-29"
        assert args[3] == "2026-09-07"
        assert kwargs["location"] == "Seattle, WA"

    def test_location_blank_when_not_given(self):
        with _created() as mk:
            cm.create_event(title="Dentist", date_str="2026-08-01", time_str="14:00")
        assert mk.call_args.kwargs["location"] == ""

    def test_end_date_ignored_for_timed_events(self):
        """Timed events get their length from duration_minutes, not end_date."""
        with _created() as mk:
            cm.create_event(title="Call", date_str="2026-08-01", time_str="09:00",
                            duration_minutes=45, end_date="2026-08-09")

        args = mk.call_args.args
        start_dt = datetime.fromisoformat(args[2])
        end_dt = datetime.fromisoformat(args[3])
        assert (end_dt - start_dt) == timedelta(minutes=45)

    def test_timed_event_carries_the_family_timezone(self):
        with _created() as mk:
            cm.create_event(title="Dentist", date_str="2026-08-01",
                            time_str="14:00", duration_minutes=30)

        args, kwargs = mk.call_args
        assert kwargs["timezone"] == cm.TIMEZONE
        assert kwargs.get("all_day", False) is False
        assert args[2].startswith("2026-08-01T14:00")
        start_dt = datetime.fromisoformat(args[2])
        end_dt = datetime.fromisoformat(args[3])
        assert (end_dt - start_dt) == timedelta(minutes=30)

    def test_description_passed_through(self):
        with _created() as mk:
            cm.create_event(title="Trip", date_str="2026-08-01",
                            description="Pack sunscreen")
        assert mk.call_args.kwargs["description"] == "Pack sunscreen"

    def test_description_blank_when_not_given(self):
        with _created() as mk:
            cm.create_event(title="Trip", date_str="2026-08-01")
        assert mk.call_args.kwargs["description"] == ""

    def test_missing_time_str_falls_back_to_all_day(self):
        with _created() as mk:
            cm.create_event(title="Trip", date_str="2026-08-01",
                            is_all_day=False, time_str=None)
        assert mk.call_args.kwargs["all_day"] is True
        assert mk.call_args.args[2] == "2026-08-01"


# ─── delete_event ─────────────────────────────────────────────────────────────

class TestDeleteEvent:
    def test_no_match_returns_false(self):
        with _listing([]), patch("core.gcal.delete_event") as rm:
            success, message = cm.delete_event("dentist")
        assert success is False
        assert "No upcoming event" in message
        rm.assert_not_called()

    def test_single_match_deletes_and_returns_summary(self):
        events = [{"id": "e1", "summary": "Dentist",
                   "start": {"dateTime": "2026-08-01T14:00:00"}}]
        with _listing(events), patch("core.gcal.delete_event") as rm:
            success, message = cm.delete_event("dentist")
        assert success is True
        assert message == "Dentist"
        rm.assert_called_once_with(cm.CALENDAR_ID, "e1")

    def test_multiple_matches_deletes_first_and_flags_others(self):
        events = [
            {"id": "e1", "summary": "Dentist AM",
             "start": {"dateTime": "2026-08-01T09:00:00"}},
            {"id": "e2", "summary": "Dentist PM",
             "start": {"dateTime": "2026-08-01T15:00:00"}},
        ]
        with _listing(events), patch("core.gcal.delete_event") as rm:
            success, message = cm.delete_event("dentist")
        assert success is True
        assert "Dentist AM" in message
        assert "1 other event" in message
        assert "Dentist PM" in message
        rm.assert_called_once_with(cm.CALENDAR_ID, "e1")

    def test_date_filter_narrows_to_no_match(self):
        events = [{"id": "e1", "summary": "Dentist",
                   "start": {"dateTime": "2026-08-01T14:00:00"}}]
        with _listing(events), patch("core.gcal.delete_event") as rm:
            success, message = cm.delete_event("dentist", date_str="2026-09-01")
        assert success is False
        assert "2026-09-01" in message
        rm.assert_not_called()

    def test_date_filter_matches_all_day_event(self):
        events = [{"id": "e1", "summary": "Trip", "start": {"date": "2026-08-01"}}]
        with _listing(events), patch("core.gcal.delete_event"):
            success, message = cm.delete_event("trip", date_str="2026-08-01")
        assert success is True
        assert message == "Trip"


# ─── update_event ─────────────────────────────────────────────────────────────

def _updated(summary="Event"):
    return patch("core.gcal.update_event", return_value={"summary": summary})


class TestUpdateEvent:
    def test_no_match_returns_false(self):
        with _listing([]), _updated():
            success, message = cm.update_event("dentist", new_title="Orthodontist")
        assert success is False
        assert "No upcoming event" in message

    def test_title_only_update(self):
        events = [{"id": "e1", "summary": "Dentist",
                   "start": {"dateTime": "2026-08-01T14:00:00"},
                   "end": {"dateTime": "2026-08-01T15:00:00"}}]
        with _listing(events), _updated("Orthodontist") as up:
            success, message = cm.update_event("dentist", new_title="Orthodontist")
        assert success is True
        assert message == "Orthodontist"
        args, kwargs = up.call_args
        assert args == (cm.CALENDAR_ID, "e1")
        assert kwargs == {"summary": "Orthodontist"}

    def test_date_and_time_update_sets_a_timed_start(self):
        events = [{"id": "e1", "summary": "Dentist",
                   "start": {"dateTime": "2026-08-01T14:00:00"},
                   "end": {"dateTime": "2026-08-01T15:00:00"}}]
        with _listing(events), _updated("Dentist") as up:
            cm.update_event("dentist", new_date="2026-08-02", new_time="10:00")
        kwargs = up.call_args.kwargs
        assert kwargs["start"].startswith("2026-08-02T10:00")
        assert kwargs["timezone"] == cm.TIMEZONE
        assert "all_day" not in kwargs

    def test_date_only_update_stays_all_day(self):
        events = [{"id": "e1", "summary": "Trip",
                   "start": {"date": "2026-08-01"}, "end": {"date": "2026-08-01"}}]
        with _listing(events), _updated("Trip") as up:
            cm.update_event("trip", new_date="2026-08-05")
        kwargs = up.call_args.kwargs
        assert kwargs["start"] == "2026-08-05"
        assert kwargs["all_day"] is True

    def test_multiple_matches_updates_first_and_flags_others(self):
        events = [
            {"id": "e1", "summary": "Dentist AM",
             "start": {"dateTime": "2026-08-01T09:00:00"},
             "end": {"dateTime": "2026-08-01T10:00:00"}},
            {"id": "e2", "summary": "Dentist PM",
             "start": {"dateTime": "2026-08-01T15:00:00"},
             "end": {"dateTime": "2026-08-01T16:00:00"}},
        ]
        with _listing(events), _updated("Checkup") as up:
            success, message = cm.update_event("dentist", new_title="Checkup")
        assert success is True
        assert "1 other event" in message
        up.assert_called_once_with(cm.CALENDAR_ID, "e1", summary="Checkup")


# ─── update_event date handling ──────────────────────────────────────────────

class TestUpdateEventDates:
    """Regression: the new_date-only branch set start and end to the same bare
    {"date": ...}. Google's all-day end.date is EXCLUSIVE — create_event has a
    comment saying so and derives last_day + 1 — so that was a zero-length
    span. It also fired regardless of the original event's type, silently
    turning a timed appointment into an all-day block."""

    def test_all_day_move_uses_an_exclusive_end(self):
        event = {"id": "e1", "summary": "Field trip",
                 "start": {"date": "2026-09-10"}, "end": {"date": "2026-09-11"}}
        with _listing([event]), _updated("Field trip") as up:
            ok, _ = cm.update_event("Field trip", new_date="2026-09-14")
        assert ok
        kwargs = up.call_args.kwargs
        assert kwargs["start"] == "2026-09-14"
        assert kwargs["end"] == "2026-09-15"     # exclusive, not == start

    def test_moving_a_timed_event_keeps_it_timed(self):
        event = {"id": "e2", "summary": "Dentist",
                 "start": {"dateTime": "2026-09-10T16:00:00"},
                 "end":   {"dateTime": "2026-09-10T17:00:00"}}
        with _listing([event]), _updated("Dentist") as up:
            ok, _ = cm.update_event("Dentist", new_date="2026-09-14")
        assert ok
        kwargs = up.call_args.kwargs
        assert "all_day" not in kwargs, "a 4pm appointment became all-day"
        assert kwargs["start"].startswith("2026-09-14T16:00")

    def test_moving_a_timed_event_preserves_its_duration(self):
        event = {"id": "e3", "summary": "Swim meet",
                 "start": {"dateTime": "2026-09-10T09:00:00"},
                 "end":   {"dateTime": "2026-09-10T12:30:00"}}   # 3.5 hours
        with _listing([event]), _updated("Swim meet") as up:
            cm.update_event("Swim meet", new_time="08:00")
        kwargs = up.call_args.kwargs
        assert kwargs["start"].startswith("2026-09-10T08:00")
        assert kwargs["end"].startswith("2026-09-10T11:30")

    def test_retiming_an_all_day_event_makes_it_timed(self):
        event = {"id": "e4", "summary": "Picture day",
                 "start": {"date": "2026-09-10"}, "end": {"date": "2026-09-11"}}
        with _listing([event]), _updated("Picture day") as up:
            cm.update_event("Picture day", new_time="09:15")
        assert up.call_args.kwargs["start"].startswith("2026-09-10T09:15")


class TestUpdateEventPreservesSpan:
    """Regression: the all-day branch hardcoded end = target_date + 1 day and
    discarded the event's real span, so re-dating a multi-day event collapsed
    it to one day. travel_window gates on exactly that span, so a moved 9-day
    `Trip to Seattle` sent the remaining days back to home weather with
    nothing raised. create_event derives its span from `end_date`; this branch
    has no such argument and must read it off the event it is editing."""

    def test_moving_a_multiday_all_day_event_keeps_its_length(self):
        # Aug 29 -> Sep 6 inclusive; Google's exclusive end is Sep 7. Nine days.
        event = {"id": "e9", "summary": "Trip to Seattle",
                 "start": {"date": "2026-08-29"}, "end": {"date": "2026-09-07"}}
        with _listing([event]), _updated("Trip to Seattle") as up:
            cm.update_event("Trip to Seattle", new_date="2026-09-05")
        kwargs = up.call_args.kwargs
        assert kwargs["start"] == "2026-09-05"
        assert kwargs["end"] == "2026-09-14", "a 9-day trip was truncated"

    def test_moving_a_one_day_all_day_event_still_ends_the_next_day(self):
        event = {"id": "e1", "summary": "Field trip",
                 "start": {"date": "2026-09-10"}, "end": {"date": "2026-09-11"}}
        with _listing([event]), _updated("Field trip") as up:
            cm.update_event("Field trip", new_date="2026-09-14")
        assert up.call_args.kwargs["end"] == "2026-09-15"

    def test_a_missing_end_date_falls_back_to_one_day(self):
        event = {"id": "e2", "summary": "Odd event", "start": {"date": "2026-09-10"}}
        with _listing([event]), _updated("Odd event") as up:
            cm.update_event("Odd event", new_date="2026-09-20")
        assert up.call_args.kwargs["end"] == "2026-09-21"
