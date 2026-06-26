"""
test_briefing_hardening.py — Tests for the hardened morning briefing pipeline.

Covers:
  - Output validation (validate_briefing_data)
  - Reliability tracker (_record_reliability)
  - Config regression (calendar ID not personal, primary_email_id present)
  - Weather regression (output includes temperature)
  - Briefing data contract (both kids, correct date)
  - Preflight checks (mocked)
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# conftest.py patches keychain and adds SKILL_DIR to sys.path


# ── Output Validation ────────────────────────────────────────────────────────

class TestValidateBriefingData:

    def test_valid_data_no_warnings(self, tmp_skill_dir):
        from features.briefing.morning_briefing import validate_briefing_data
        data = {
            "date": datetime.now().strftime("%A, %B %d"),
            "weather": "🌤️ *Weather*\n  Clear sky, 72°F (High 80°F / Low 58°F)",
            "events": [{"title": "Swim class", "time": "10:40", "calendar_source": "Family Calendar"}],
            "meal_suggestions": {
                "amyra": {"breakfast": "Eggs", "lunch": "Sandwich", "side": "Fruit"},
                "reyansh": {"breakfast": "Oats", "lunch": "Khichdi", "side": "Banana"},
            },
        }
        with patch("features.briefing.morning_briefing._load_primary_email_id", return_value="personal@gmail.com"):
            warnings = validate_briefing_data(data)
        assert warnings == []

    def test_weather_none_warns(self):
        from features.briefing.morning_briefing import validate_briefing_data
        data = {
            "date": datetime.now().strftime("%A, %B %d"),
            "weather": None,
            "events": [],
            "meal_suggestions": {"amyra": {}, "reyansh": {}},
        }
        with patch("features.briefing.morning_briefing._load_primary_email_id", return_value=""):
            warnings = validate_briefing_data(data)
        assert any("weather data unavailable" in w for w in warnings)

    def test_weather_missing_temperature_warns(self):
        from features.briefing.morning_briefing import validate_briefing_data
        data = {
            "date": datetime.now().strftime("%A, %B %d"),
            "weather": "Cloudy conditions expected",
            "events": [],
            "meal_suggestions": {"amyra": {}, "reyansh": {}},
        }
        with patch("features.briefing.morning_briefing._load_primary_email_id", return_value=""):
            warnings = validate_briefing_data(data)
        assert any("missing temperature" in w for w in warnings)

    def test_missing_kid_warns(self):
        from features.briefing.morning_briefing import validate_briefing_data
        data = {
            "date": datetime.now().strftime("%A, %B %d"),
            "weather": "72°F",
            "events": [],
            "meal_suggestions": {"amyra": {}},  # reyansh missing
        }
        with patch("features.briefing.morning_briefing._load_primary_email_id", return_value=""):
            warnings = validate_briefing_data(data)
        assert any("reyansh" in w for w in warnings)

    def test_wrong_date_warns(self):
        from features.briefing.morning_briefing import validate_briefing_data
        data = {
            "date": "Monday, January 01",
            "weather": "72°F",
            "events": [],
            "meal_suggestions": {"amyra": {}, "reyansh": {}},
        }
        with patch("features.briefing.morning_briefing._load_primary_email_id", return_value=""):
            warnings = validate_briefing_data(data)
        assert any("date mismatch" in w for w in warnings)

    def test_personal_calendar_event_warns(self):
        from features.briefing.morning_briefing import validate_briefing_data
        data = {
            "date": datetime.now().strftime("%A, %B %d"),
            "weather": "72°F",
            "events": [
                {"title": "Personal dentist", "calendar_source": "personal@gmail.com"},
            ],
            "meal_suggestions": {"amyra": {}, "reyansh": {}},
        }
        with patch("features.briefing.morning_briefing._load_primary_email_id", return_value="personal@gmail.com"):
            warnings = validate_briefing_data(data)
        assert any("personal calendar" in w for w in warnings)

    def test_events_not_list_warns(self):
        from features.briefing.morning_briefing import validate_briefing_data
        data = {
            "date": datetime.now().strftime("%A, %B %d"),
            "weather": "72°F",
            "events": "not a list",
            "meal_suggestions": {"amyra": {}, "reyansh": {}},
        }
        with patch("features.briefing.morning_briefing._load_primary_email_id", return_value=""):
            warnings = validate_briefing_data(data)
        assert any("not a list" in w for w in warnings)


# ── Reliability Tracker ──────────────────────────────────────────────────────

class TestReliabilityTracker:

    def test_creates_tracker_on_first_run(self, tmp_skill_dir):
        from features.briefing.morning_briefing import _record_reliability
        with patch("features.briefing.morning_briefing.SKILL_DIR", str(tmp_skill_dir)):
            data = {"weather": "72°F", "events": [], "meal_suggestions": {"amyra": {}, "reyansh": {}}}
            _record_reliability(data, [])

        tracker_path = tmp_skill_dir / "household" / "briefing_reliability.json"
        assert tracker_path.exists()
        tracker = json.loads(tracker_path.read_text())
        assert len(tracker["days"]) == 1
        assert tracker["days"][0]["status"] == "ok"

    def test_degraded_when_warnings(self, tmp_skill_dir):
        from features.briefing.morning_briefing import _record_reliability
        with patch("features.briefing.morning_briefing.SKILL_DIR", str(tmp_skill_dir)):
            data = {"weather": None, "events": [], "meal_suggestions": {"amyra": {}, "reyansh": {}}}
            _record_reliability(data, ["weather data unavailable"])

        tracker_path = tmp_skill_dir / "household" / "briefing_reliability.json"
        tracker = json.loads(tracker_path.read_text())
        assert tracker["days"][0]["status"] == "degraded"
        assert tracker["days"][0]["components"]["weather"] is False

    def test_no_duplicate_same_date(self, tmp_skill_dir):
        from features.briefing.morning_briefing import _record_reliability
        with patch("features.briefing.morning_briefing.SKILL_DIR", str(tmp_skill_dir)):
            data = {"weather": "72°F", "events": [], "meal_suggestions": {"amyra": {}, "reyansh": {}}}
            _record_reliability(data, [])
            _record_reliability(data, [])

        tracker_path = tmp_skill_dir / "household" / "briefing_reliability.json"
        tracker = json.loads(tracker_path.read_text())
        today = datetime.now().strftime("%Y-%m-%d")
        today_entries = [d for d in tracker["days"] if d["date"] == today]
        assert len(today_entries) == 1


# ── Config Regression Tests ──────────────────────────────────────────────────

class TestConfigRegressions:

    def test_calendar_id_not_personal_email(self):
        """Regression: config.json calendar.id must NOT be a plain @gmail.com address."""
        from core.config_loader import config
        primary = config._data.get("calendar", {}).get("primary_email_id", "")
        assert config.calendar_id != primary, \
            "calendar.id still points at personal email — must be the group calendar ID"
        assert not config.calendar_id.endswith("@gmail.com"), \
            f"calendar.id looks like a personal Gmail: {config.calendar_id}"

    def test_calendar_id_is_group_calendar(self):
        """The calendar ID should be a group calendar (contains @group.calendar.google.com)."""
        from core.config_loader import config
        assert "@group.calendar.google.com" in config.calendar_id or \
               config.calendar_id == "testcal@group.calendar.google.com", \
            f"calendar.id doesn't look like a group calendar: {config.calendar_id}"


# ── Weather Regression ───────────────────────────────────────────────────────

class TestWeatherRegression:

    def test_weather_briefing_includes_temperature(self):
        """Regression: get_weather_briefing() must include °F for clothing suggestions."""
        from features.briefing.weather import get_weather_briefing
        with patch("features.briefing.weather.fetch_weather") as mock_fetch:
            mock_fetch.return_value = {
                "temp_current": 72,
                "temp_feels_like": 70,
                "temp_high": 80,
                "temp_low": 58,
                "condition": "Clear sky",
                "wind_speed": 5,
                "humidity": 45,
                "rain_chance": 10,
            }
            result = get_weather_briefing()
        assert result is not None
        assert "°F" in result or "°" in result, \
            f"Weather output missing temperature: {result}"

    def test_weather_briefing_returns_none_on_failure(self):
        from features.briefing.weather import get_weather_briefing
        with patch("features.briefing.weather.fetch_weather", return_value=None):
            result = get_weather_briefing()
        assert result is None


# ── Briefing Data Contract ───────────────────────────────────────────────────

class TestBriefingDataContract:

    def test_briefing_data_has_both_kids(self):
        """Both Amyra and Reyansh must appear in meal suggestions."""
        from features.briefing.morning_briefing import validate_briefing_data
        data = {
            "date": datetime.now().strftime("%A, %B %d"),
            "weather": "72°F",
            "events": [],
            "meal_suggestions": {"amyra": {}, "reyansh": {}},
        }
        with patch("features.briefing.morning_briefing._load_primary_email_id", return_value=""):
            warnings = validate_briefing_data(data)
        kid_warnings = [w for w in warnings if "missing for" in w]
        assert kid_warnings == [], f"Kids missing from meals: {kid_warnings}"

    def test_briefing_date_matches_today(self):
        from features.briefing.morning_briefing import validate_briefing_data
        today = datetime.now().strftime("%A, %B %d")
        data = {
            "date": today,
            "weather": "72°F",
            "events": [],
            "meal_suggestions": {"amyra": {}, "reyansh": {}},
        }
        with patch("features.briefing.morning_briefing._load_primary_email_id", return_value=""):
            warnings = validate_briefing_data(data)
        date_warnings = [w for w in warnings if "date mismatch" in w]
        assert date_warnings == [], f"Date mismatch: {date_warnings}"


# ── Preflight Checks (mocked) ───────────────────────────────────────────────

class TestPreflightChecks:

    def test_config_integrity_passes(self, tmp_skill_dir):
        from features.briefing.briefing_preflight import check_config_integrity
        with patch("features.briefing.briefing_preflight.SKILL_DIR", tmp_skill_dir):
            # Re-import config_loader with the test config
            import importlib
            import core.config_loader as config_loader
            orig_path = config_loader.SKILL_DIR
            config_loader.SKILL_DIR = str(tmp_skill_dir)
            try:
                config_loader.config = config_loader._load_config()
                ok, msg = check_config_integrity()
            finally:
                config_loader.SKILL_DIR = orig_path
                config_loader.config = config_loader._load_config()
        assert ok, f"Config integrity failed: {msg}"

    def test_calendar_freshness_missing_cache(self, tmp_skill_dir):
        from features.briefing.briefing_preflight import check_calendar_freshness
        with patch("features.briefing.briefing_preflight.SKILL_DIR", tmp_skill_dir):
            ok, msg = check_calendar_freshness()
        assert not ok
        assert "No cached calendar" in msg or "cleared" in msg

    def test_weather_api_check(self):
        from features.briefing.briefing_preflight import check_weather_api
        with patch("features.briefing.weather.fetch_weather") as mock:
            mock.return_value = {"temp_current": 70}
            ok, msg = check_weather_api()
        assert ok
        assert "70°F" in msg
