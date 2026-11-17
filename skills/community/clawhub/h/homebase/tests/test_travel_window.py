"""
test_travel_window.py — "Is the household away, and where?"

The stakes here are asymmetric, and the tests are weighted to match. A missed
trip costs one briefing that describes the wrong city. A *false* trip redirects
a family's weather to somewhere they have never been, silently, for as many
days as the phantom event spans — so most of what follows is about what must
NOT trigger travel mode.

Covers:
  - get_travel_window(): boundaries, day/of arithmetic, last_day
  - destination resolution: location field wins over title parsing
  - false-positive guards: timed events, ordinary all-day events, near-misses
  - _inclusive_end_date(): Google's exclusive all-day end date
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from features.trips.travel_window import (  # noqa: E402
    get_travel_window,
    _match_travel_event,
    _clean_destination,
)


# ─── Helpers ─────────────────────────────────────────────────────────────────

def ev(title, date, end_date=None, time="All day", location=""):
    return {
        "title":    title,
        "date":     date,
        "end_date": end_date or date,
        "time":     time,
        "location": location,
    }


SEATTLE = ev("Trip to Seattle", "2026-08-29", "2026-09-06", location="Seattle, WA")


# ─── The window ──────────────────────────────────────────────────────────────

def test_away_across_the_whole_span():
    for date in ("2026-08-29", "2026-09-01", "2026-09-06"):
        assert get_travel_window(date, [SEATTLE])["away"] is True, date


def test_home_on_the_days_either_side():
    """The bug that made this necessary: an off-by-one here is a wrong briefing."""
    assert get_travel_window("2026-08-28", [SEATTLE]) == {"away": False}
    assert get_travel_window("2026-09-07", [SEATTLE]) == {"away": False}


def test_day_of_arithmetic_is_inclusive_and_one_based():
    assert get_travel_window("2026-08-29", [SEATTLE])["day"] == 1
    assert get_travel_window("2026-09-01", [SEATTLE])["day"] == 4
    assert get_travel_window("2026-09-06", [SEATTLE])["day"] == 9
    assert get_travel_window("2026-09-01", [SEATTLE])["of"] == 9


def test_last_day_only_on_the_final_day():
    assert get_travel_window("2026-09-05", [SEATTLE])["last_day"] is False
    assert get_travel_window("2026-09-06", [SEATTLE])["last_day"] is True


def test_single_day_trip_is_day_one_of_one_and_also_last():
    out = get_travel_window("2026-09-01", [ev("Trip to Ojai", "2026-09-01")])
    assert (out["day"], out["of"], out["last_day"]) == (1, 1, True)


def test_event_missing_end_date_is_treated_as_single_day():
    """Events cached before end_date existed must degrade, not crash."""
    stale = {"title": "Trip to Seattle", "date": "2026-08-29", "time": "All day",
             "location": "Seattle, WA"}
    assert get_travel_window("2026-08-29", [stale])["away"] is True
    assert get_travel_window("2026-08-30", [stale]) == {"away": False}


# ─── Destination resolution ──────────────────────────────────────────────────

def test_location_field_wins_over_the_title():
    """A structured location geocodes; a title fragment may not."""
    out = get_travel_window(
        "2026-09-01",
        [ev("Trip to Seattle for Ammu's birthday", "2026-09-01", location="Seattle, WA")],
    )
    assert out["destination"] == "Seattle, WA"


def test_destination_parsed_from_title_when_location_is_blank():
    out = get_travel_window("2026-09-01", [ev("Trip to Big Bear", "2026-09-01")])
    assert out["destination"] == "Big Bear"


def test_trailing_qualifier_stripped_from_parsed_destination():
    assert _clean_destination("Seattle (family)") == "Seattle"
    assert _clean_destination("Portland - work") == "Portland"


def test_destinationless_pattern_still_reports_away():
    """'Out of town' names no place, but home content is still wrong."""
    out = get_travel_window("2026-09-01", [ev("Out of town", "2026-09-01")])
    assert out["away"] is True
    assert out["destination"] == ""


@pytest.mark.parametrize("title,expected", [
    ("Trip to Seattle",     "Seattle"),
    ("Seattle trip",        "Seattle"),
    ("Travel to Vancouver", "Vancouver"),
    ("Vacation in Kauai",   "Kauai"),
])
def test_accepted_title_shapes(title, expected):
    assert _match_travel_event(ev(title, "2026-09-01")) == expected


# ─── False-positive guards ───────────────────────────────────────────────────

def test_timed_event_never_triggers_travel_mode():
    """The flight is an appointment; the trip is the span around it."""
    flight = ev("Flight UA2316 LAX to SEA", "2026-08-29", time="12:40",
                location="Seattle, WA")
    assert get_travel_window("2026-08-29", [flight]) == {"away": False}


def test_a_timed_event_titled_like_a_trip_is_still_not_a_trip():
    timed = ev("Trip to Seattle", "2026-09-01", "2026-09-03", time="09:00",
               location="Seattle, WA")
    assert get_travel_window("2026-09-01", [timed]) == {"away": False}


@pytest.mark.parametrize("title", [
    "Weekend farmers market",
    "Summer Camp - Foam Party",
    "Ben Water Day",
    "Visit from Dadi",
    "Ana's field trip permission slip due",
    "Low-fiber diet starts (Sam, 3 days pre-procedure)",
])
def test_ordinary_all_day_events_do_not_trigger_travel_mode(title):
    """
    Every one of these is real or realistic for this calendar. 'Weekend' and
    'visit' are in trip_detector's wide net on purpose; they must not be in
    this one.
    """
    assert _match_travel_event(ev(title, "2026-09-01")) is None
    assert get_travel_window("2026-09-01", [ev(title, "2026-09-01")]) == {"away": False}


def test_untitled_event_is_ignored():
    assert _match_travel_event(ev("", "2026-09-01")) is None


def test_earliest_matching_trip_wins_when_two_overlap():
    """Deterministic rather than dict-order dependent."""
    a = ev("Trip to Seattle", "2026-08-29", "2026-09-06", location="Seattle, WA")
    b = ev("Trip to Portland", "2026-09-02", "2026-09-04", location="Portland, OR")
    assert get_travel_window("2026-09-03", [b, a])["destination"] == "Seattle, WA"


# ─── Google's exclusive end date ─────────────────────────────────────────────

def test_inclusive_end_date_rolls_back_all_day_events():
    from features.calendar.calendar_aggregator import FamilyCalendarAggregator as F
    # Aug 29 - Sep 6 inclusive arrives from Google as end.date == Sep 7.
    assert F._inclusive_end_date("2026-08-29", "2026-09-07") == "2026-09-06"


def test_inclusive_end_date_leaves_timed_events_alone():
    from features.calendar.calendar_aggregator import FamilyCalendarAggregator as F
    assert F._inclusive_end_date(
        "2026-08-29T12:40:00-07:00", "2026-08-29T15:10:00-07:00"
    ) == "2026-08-29"


def test_inclusive_end_date_falls_back_to_start_when_end_is_missing():
    from features.calendar.calendar_aggregator import FamilyCalendarAggregator as F
    assert F._inclusive_end_date("2026-08-29", "") == "2026-08-29"
    assert F._inclusive_end_date("2026-08-29", "not-a-date") == "2026-08-29"


# ─── Departure day is a home morning ─────────────────────────────────────────

def test_departure_day_keeps_home_weather():
    """
    Day 1 they wake up in Irvine and fly out at midday. A 6:05 AM briefing that
    morning is read in their own kitchen, so the forecast must stay home's —
    the trip window is already open, which is why `away` alone cannot decide
    this.
    """
    out = get_travel_window("2026-08-29", [SEATTLE])
    assert out["away"] is True
    assert out["departure_day"] is True
    assert out["at_destination"] is False
    assert out["weather_location"] == ""
    assert out["destination"] == "Seattle, WA"


def test_second_day_onward_uses_destination_weather():
    out = get_travel_window("2026-08-30", [SEATTLE])
    assert out["at_destination"] is True
    assert out["weather_location"] == "Seattle, WA"


def test_return_day_still_uses_destination_weather():
    """Not symmetrical with departure: they wake up there and fly home midday."""
    out = get_travel_window("2026-09-06", [SEATTLE])
    assert out["last_day"] is True
    assert out["at_destination"] is True
    assert out["weather_location"] == "Seattle, WA"


def test_single_day_trip_never_leaves_home_weather():
    """A day trip is a home morning by definition — there is no night away."""
    out = get_travel_window("2026-09-01", [ev("Trip to Ojai", "2026-09-01")])
    assert out["at_destination"] is False
    assert out["weather_location"] == ""


# ─── The trip event is a state, not an appointment ───────────────────────────

def test_event_id_is_surfaced_for_timeline_filtering():
    """
    Consumers drop this event from the day's timeline. Matching is by id, not
    title, so an unrelated event sharing the name is never swallowed with it.
    """
    trip = dict(SEATTLE, id="abc123")
    assert get_travel_window("2026-09-01", [trip])["event_id"] == "abc123"


def test_event_id_is_empty_string_when_the_event_has_no_id():
    """A hand-built event still yields a filterable (falsy) value, not a crash."""
    assert get_travel_window("2026-09-01", [ev("Trip to Ojai", "2026-09-01")])["event_id"] == ""
