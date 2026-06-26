"""
test_trip_detector.py — Smoke tests for trip_detector.py

Covers:
  - infer_environment_tags(): keyword → environment tag mapping
  - load_kid_profiles() / save_kid_profiles(): roundtrip I/O
  - log_kid_observation(): appends observation with correct fields
  - get_kid_profile(): returns readable summary / 'no profile' message
  - load_sent_log() / save_sent_log(): roundtrip I/O
  - find_upcoming_trips(): keyword detection, location detection, multi-day detection
  - geocode_location(): graceful failure returns None
  - _fallback_trip_prep(): returns non-empty message without LLM
"""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

# Stub external dependencies
for mod in ("google", "google.oauth2", "google.oauth2.credentials",
            "google.auth", "google.auth.transport", "google.auth.transport.requests",
            "googleapiclient", "googleapiclient.discovery"):
    import types as _types
    sys.modules.setdefault(mod, _types.ModuleType(mod))

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
        data = {"Amyra": {"observations": [{"id": "abc", "text": "likes mountains"}]}}
        td.save_kid_profiles(data)
        loaded = td.load_kid_profiles()
        assert loaded == data

    def test_log_observation_creates_profile(self):
        result = td.log_kid_observation("Amyra", "gets car sick on long drives",
                                         category="health", tags=["long_drive"])
        assert "Amyra" in result
        profiles = td.load_kid_profiles()
        assert "Amyra" in profiles
        assert len(profiles["Amyra"]["observations"]) == 1
        obs = profiles["Amyra"]["observations"][0]
        assert obs["text"] == "gets car sick on long drives"
        assert obs["category"] == "health"
        assert "long_drive" in obs["tags"]

    def test_log_observation_appends(self):
        td.log_kid_observation("Amyra", "first obs")
        td.log_kid_observation("Amyra", "second obs")
        profiles = td.load_kid_profiles()
        assert len(profiles["Amyra"]["observations"]) == 2

    def test_get_kid_profile_no_data(self):
        result = td.get_kid_profile("Amyra")
        assert "No profile" in result or "no profile" in result.lower()

    def test_get_kid_profile_with_data(self):
        td.log_kid_observation("Amyra", "likes the beach")
        result = td.get_kid_profile("Amyra")
        assert "Amyra" in result
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


# ─── find_upcoming_trips ─────────────────────────────────────────────────────

class TestFindUpcomingTrips:
    def _make_cal_service(self, events: list) -> MagicMock:
        svc = MagicMock()
        svc.events.return_value.list.return_value.execute.return_value = {"items": events}
        return svc

    def _future_date(self, days: int) -> str:
        return (datetime.now(timezone.utc) + timedelta(days=days)).strftime("%Y-%m-%d")

    def test_keyword_in_title_detected(self):
        dt = self._future_date(2)
        event = {
            "id": "e1", "summary": "Big Bear Trip",
            "location": "",
            "start": {"date": dt}, "end": {"date": dt},
        }
        svc = self._make_cal_service([event])
        trips = td.find_upcoming_trips(svc, days_ahead=4)
        assert len(trips) == 1
        assert trips[0]["title"] == "Big Bear Trip"

    def test_location_field_detected(self):
        dt = self._future_date(1)
        event = {
            "id": "e2", "summary": "Grandma visit",
            "location": "San Diego, CA",
            "start": {"date": dt}, "end": {"date": dt},
        }
        svc = self._make_cal_service([event])
        trips = td.find_upcoming_trips(svc, days_ahead=4)
        assert len(trips) == 1
        assert trips[0]["location"] == "San Diego, CA"

    def test_multi_day_event_detected(self):
        start = self._future_date(1)
        end = self._future_date(3)
        event = {
            "id": "e3", "summary": "Family visit",
            "location": "",
            "start": {"date": start}, "end": {"date": end},
        }
        svc = self._make_cal_service([event])
        trips = td.find_upcoming_trips(svc, days_ahead=4)
        assert len(trips) == 1

    def test_plain_single_day_no_keyword_not_detected(self):
        dt = self._future_date(1)
        event = {
            "id": "e4", "summary": "Dentist appointment",
            "location": "",
            "start": {"date": dt}, "end": {"date": dt},
        }
        svc = self._make_cal_service([event])
        trips = td.find_upcoming_trips(svc, days_ahead=4)
        assert len(trips) == 0

    def test_empty_calendar_returns_empty(self):
        svc = self._make_cal_service([])
        trips = td.find_upcoming_trips(svc, days_ahead=4)
        assert trips == []


# ─── geocode_location ─────────────────────────────────────────────────────────

class TestGeocodeLocation:
    def test_empty_location_returns_none(self):
        result = td.geocode_location("")
        assert result is None

    def test_network_failure_returns_none(self):
        with patch("urllib.request.urlopen", side_effect=Exception("no network")):
            result = td.geocode_location("Big Bear Lake, CA")
        assert result is None


# ─── _fallback_trip_prep ─────────────────────────────────────────────────────

class TestFallbackTripPrep:
    def test_returns_non_empty_message(self):
        trip = {
            "title": "Big Bear Cabin",
            "start_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=4)).strftime("%Y-%m-%d"),
            "location": "Big Bear Lake, CA",
        }
        weather = {
            "temp_low": 35,
            "temp_high": 55,
            "condition": "Partly cloudy",
            "humidity": 30,
        }
        result = td._fallback_trip_prep(trip, weather, ["mountain", "cold"], {})
        assert "Big Bear" in result
        assert "35" in result or "55" in result

    def test_works_without_weather(self):
        trip = {
            "title": "Beach Day",
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": datetime.now().strftime("%Y-%m-%d"),
            "location": "Laguna Beach",
        }
        result = td._fallback_trip_prep(trip, None, ["beach"], {})
        assert "Beach Day" in result
