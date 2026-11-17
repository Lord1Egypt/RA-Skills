"""
test_trip_detector.py — Smoke tests for trip_detector.py

Covers:
  - infer_environment_tags(): keyword → environment tag mapping
  - load_kid_profiles() / save_kid_profiles(): roundtrip I/O
  - log_kid_observation(): appends observation with correct fields
  - get_kid_profile(): returns readable summary / 'no profile' message
  - load_sent_log() / save_sent_log(): roundtrip I/O
  - list_candidate_events(): returns non-recurring events with sent_key/already_sent
  - geocode_location(): graceful failure returns None
"""
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


import features.trips.trip_detector as td


# ─── Helpers ─────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def isolated_paths(tmp_path):
    """Redirect all file I/O to a temp directory."""
    with patch.object(td, "HOUSEHOLD_DIR", str(tmp_path)), \
         patch.object(td, "PROFILES_PATH", str(tmp_path / "kid_profiles.json")), \
         patch.object(td, "SENT_PATH", str(tmp_path / "trip_prep_sent.json")):
        yield tmp_path


# ─── infer_environment_tags ───────────────────────────────────────────────────

class TestInferEnvironmentTags:
    def test_mountain_trip(self):
        tags = td.infer_environment_tags("Big Bear Weekend", "Big Bear Lake, CA")
        assert "mountain" in tags
        assert "cold" in tags

    def test_beach_trip(self):
        tags = td.infer_environment_tags("Beach Day", "Laguna Beach, CA")
        assert "beach" in tags
        assert "sunny" in tags

    def test_desert_trip(self):
        tags = td.infer_environment_tags("Palm Springs Getaway", "Palm Springs, CA")
        assert "desert" in tags
        assert "hot" in tags

    def test_unknown_location_returns_empty(self):
        tags = td.infer_environment_tags("Visit grandma", "")
        assert isinstance(tags, list)

    def test_multiple_tags_combined(self):
        # "drive to big bear" → should get both mountain and long_drive
        tags = td.infer_environment_tags("Drive to Big Bear", "")
        assert "mountain" in tags
        assert "long_drive" in tags


# ─── Profile I/O ─────────────────────────────────────────────────────────────

class TestKidProfiles:
    def test_empty_profiles_returns_empty_dict(self):
        profiles = td.load_kid_profiles()
        assert profiles == {}

    def test_save_and_load_roundtrip(self, isolated_paths):
        data = {"Ana": {"observations": [{"id": "abc", "text": "likes mountains"}]}}
        td.save_kid_profiles(data)
        loaded = td.load_kid_profiles()
        assert loaded == data

    def test_log_observation_creates_profile(self):
        result = td.log_kid_observation("Ana", "gets car sick on long drives",
                                         category="health", tags=["long_drive"])
        assert "Ana" in result
        profiles = td.load_kid_profiles()
        assert "Ana" in profiles
        assert len(profiles["Ana"]["observations"]) == 1
        obs = profiles["Ana"]["observations"][0]
        assert obs["text"] == "gets car sick on long drives"
        assert obs["category"] == "health"
        assert "long_drive" in obs["tags"]

    def test_log_observation_appends(self):
        td.log_kid_observation("Ana", "first obs")
        td.log_kid_observation("Ana", "second obs")
        profiles = td.load_kid_profiles()
        assert len(profiles["Ana"]["observations"]) == 2

    def test_get_kid_profile_no_data(self):
        result = td.get_kid_profile("Ana")
        assert "No profile" in result or "no profile" in result.lower()

    def test_get_kid_profile_with_data(self):
        td.log_kid_observation("Ana", "likes the beach")
        result = td.get_kid_profile("Ana")
        assert "Ana" in result
        assert "likes the beach" in result


# ─── Sent log I/O ────────────────────────────────────────────────────────────

class TestSentLog:
    def test_empty_sent_log(self):
        log = td.load_sent_log()
        assert log == {}

    def test_save_and_load_sent_log(self):
        data = {"event123:2026-04-01": {"title": "Big Bear", "sent_at": "2026-03-28T09:00:00"}}
        td.save_sent_log(data)
        loaded = td.load_sent_log()
        assert loaded == data


# ─── list_candidate_events ───────────────────────────────────────────────────

class TestListCandidateEvents:
    def _make_cal_service(self, events: list) -> list:
        """Hands back the events unchanged.

        list_candidate_events took a Google service and fetched for itself
        until 2026-09-07; it now takes already-fetched events, so there is no
        service to fake. Kept under the old name because eleven call sites use
        it and the fixtures they build are the point, not the plumbing.
        """
        return events

    def _future_date(self, days: int) -> str:
        return (datetime.now(timezone.utc) + timedelta(days=days)).strftime("%Y-%m-%d")

    def test_non_recurring_event_returned_regardless_of_location(self):
        """Any non-recurring event is a candidate — agent makes the trip-vs-not call."""
        dt = self._future_date(1)
        event = {
            "id": "e1", "summary": "Notary appointment",
            "location": "Irvine, CA",
            "start": {"date": dt}, "end": {"date": dt},
        }
        svc = self._make_cal_service([event])
        candidates = td.list_candidate_events(svc)
        assert len(candidates) == 1
        assert candidates[0]["title"] == "Notary appointment"

    def test_non_recurring_event_without_location_returned(self):
        """No-location, no-keyword events still surface — agent decides."""
        dt = self._future_date(1)
        event = {
            "id": "e2", "summary": "Lunch",
            "location": "",
            "start": {"date": dt}, "end": {"date": dt},
        }
        svc = self._make_cal_service([event])
        candidates = td.list_candidate_events(svc)
        assert len(candidates) == 1

    def test_recurring_event_without_trip_keyword_skipped(self):
        """A recurring activity (e.g., swim class) is NOT a candidate."""
        dt = self._future_date(1)
        event = {
            "id": "e3", "summary": "Ana and Ben Swim Class",
            "location": "Waterworks Aquatics, Irvine",
            "start": {"dateTime": f"{dt}T10:40:00-07:00"},
            "end": {"dateTime": f"{dt}T11:10:00-07:00"},
            "recurringEventId": "abc123_recurring",
        }
        svc = self._make_cal_service([event])
        candidates = td.list_candidate_events(svc)
        assert candidates == []

    def test_recurring_event_with_trip_keyword_kept(self):
        """A recurring 'Annual cabin trip' IS still a candidate."""
        dt = self._future_date(1)
        event = {
            "id": "e4", "summary": "Annual cabin trip",
            "location": "Big Bear Lake, CA",
            "start": {"date": dt}, "end": {"date": dt},
            "recurringEventId": "def456_recurring",
        }
        svc = self._make_cal_service([event])
        candidates = td.list_candidate_events(svc)
        assert len(candidates) == 1

    def test_event_without_title_skipped(self):
        dt = self._future_date(1)
        event = {
            "id": "e5", "summary": "",
            "location": "Somewhere",
            "start": {"date": dt}, "end": {"date": dt},
        }
        svc = self._make_cal_service([event])
        candidates = td.list_candidate_events(svc)
        assert candidates == []

    def test_empty_calendar_returns_empty(self):
        svc = self._make_cal_service([])
        candidates = td.list_candidate_events(svc)
        assert candidates == []

    def test_already_sent_flag_true_when_in_log(self):
        dt = self._future_date(1)
        event = {
            "id": "e6", "summary": "Big Bear Trip",
            "location": "Big Bear Lake, CA",
            "start": {"date": dt}, "end": {"date": dt},
        }
        td.save_sent_log({f"e6:{dt}": {"title": "Big Bear Trip", "sent_at": "x", "start_date": dt}})
        svc = self._make_cal_service([event])
        candidates = td.list_candidate_events(svc)
        assert len(candidates) == 1
        assert candidates[0]["already_sent"] is True

    def test_already_sent_flag_false_for_new_event(self):
        dt = self._future_date(1)
        event = {
            "id": "e7", "summary": "Beach Day",
            "location": "Laguna",
            "start": {"date": dt}, "end": {"date": dt},
        }
        svc = self._make_cal_service([event])
        candidates = td.list_candidate_events(svc)
        assert candidates[0]["already_sent"] is False

    def test_multiday_flag_true_for_multiday_all_day(self):
        start = self._future_date(1)
        end = self._future_date(3)
        event = {
            "id": "e8", "summary": "Cabin getaway",
            "location": "Tahoe",
            "start": {"date": start}, "end": {"date": end},
        }
        svc = self._make_cal_service([event])
        candidates = td.list_candidate_events(svc)
        assert candidates[0]["multiday"] is True

    def test_multiday_flag_false_for_single_day(self):
        dt = self._future_date(1)
        event = {
            "id": "e9", "summary": "Lunch meeting",
            "location": "Office",
            "start": {"date": dt}, "end": {"date": dt},
        }
        svc = self._make_cal_service([event])
        candidates = td.list_candidate_events(svc)
        assert candidates[0]["multiday"] is False

    def test_sent_key_format(self):
        dt = self._future_date(1)
        event = {
            "id": "abc-123", "summary": "Some Event",
            "location": "Anywhere",
            "start": {"date": dt}, "end": {"date": dt},
        }
        svc = self._make_cal_service([event])
        candidates = td.list_candidate_events(svc)
        assert candidates[0]["sent_key"] == f"abc-123:{dt}"


# ─── geocode_location ─────────────────────────────────────────────────────────

class TestGeocodeLocation:
    def test_empty_location_returns_none(self):
        result = td.geocode_location("")
        assert result is None

    def test_network_failure_returns_none(self):
        with patch("urllib.request.urlopen", side_effect=Exception("no network")):
            result = td.geocode_location("Big Bear Lake, CA")
        assert result is None
