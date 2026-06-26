"""
test_morning_briefing.py — Unit tests for morning_briefing.py

Covers:
  - format_briefing_message(): all sections, weather insertion, no-event day
  - has_dropoff_today(): title and description matching
  - Locked meal plan fallback logic (integration-style with mocks)
  - generate_positive_message(): success path and fallback
  - Regression: weather_text is inserted ABOVE drop-off section
"""
import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

# ── Prevent module-level side effects ────────────────────────────────────────

# Minimal google stubs so import never touches the network
for mod in ("google", "google.oauth2", "google.oauth2.credentials",
            "google.auth", "google.auth.transport", "google.auth.transport.requests",
            "googleapiclient", "googleapiclient.discovery"):
    sys.modules.setdefault(mod, MagicMock())


from conftest import MockSnackManager, SAMPLE_MEAL_SUGGESTIONS  # noqa: E402


# Import the module under test
with patch("core.keychain_secrets.load_google_secrets", return_value=None), \
     patch("core.config_loader._load_config") as _mock_cfg:
    from conftest import MINIMAL_CONFIG
    from core.config_loader import Config
    _mock_cfg.return_value = Config(MINIMAL_CONFIG)
    import features.briefing.morning_briefing as morning_briefing  # noqa: E402


# ─── format_briefing_message ──────────────────────────────────────────────────

class TestFormatBriefingMessage:
    """Tests for the main formatter — the heart of morning_briefing.py."""

    def _default_snacks(self):
        return MockSnackManager(school_closed=False, briefing_text="")

    def test_contains_date_header(self, sample_meals):
        snacks = self._default_snacks()
        result = morning_briefing.format_briefing_message([], sample_meals, [], snacks)
        assert "Morning Briefing" in result

    def test_no_events_shows_free_day_message(self, sample_meals):
        snacks = self._default_snacks()
        result = morning_briefing.format_briefing_message([], sample_meals, [], snacks)
        assert "No events today" in result

    def test_events_are_listed(self, sample_events, sample_meals):
        snacks = self._default_snacks()
        result = morning_briefing.format_briefing_message(
            sample_events, sample_meals, [], snacks
        )
        assert "Doctor appointment" in result
        assert "Drop off Amyra" in result

    def test_event_time_formatted_as_ampm(self, sample_meals):
        """14:30 should become 2:30 PM."""
        events = [{"title": "Meeting", "time": "14:30"}]
        snacks = self._default_snacks()
        result = morning_briefing.format_briefing_message(events, sample_meals, [], snacks)
        assert "2:30 PM" in result

    def test_allday_event_shows_all_day(self, sample_meals):
        events = [{"title": "Holiday", "time": "00:00"}]
        snacks = self._default_snacks()
        result = morning_briefing.format_briefing_message(events, sample_meals, [], snacks)
        assert "All day" in result

    def test_dropoff_section_appears_when_dropoffs_present(self, sample_meals):
        snacks = self._default_snacks()
        dropoffs = [{"title": "Drop off Amyra", "time": "08:30"}]
        result = morning_briefing.format_briefing_message(
            [], sample_meals, dropoffs, snacks
        )
        assert "DROP-OFF TODAY" in result
        assert "Drop off Amyra" in result

    def test_no_dropoff_section_when_empty(self, sample_meals):
        snacks = self._default_snacks()
        result = morning_briefing.format_briefing_message([], sample_meals, [], snacks)
        assert "DROP-OFF TODAY" not in result

    def test_weather_text_inserted_when_provided(self, sample_meals):
        """Regression: weather_text must appear in output when passed."""
        snacks = self._default_snacks()
        weather = "🌤️ *Weather*\n  Sunny, 72°F"
        result = morning_briefing.format_briefing_message(
            [], sample_meals, [], snacks, weather_text=weather
        )
        assert "Sunny, 72°F" in result

    def test_weather_text_appears_before_dropoff(self, sample_meals):
        """Regression: weather must be ABOVE drop-off section."""
        snacks = self._default_snacks()
        weather = "🌤️ *Weather*\n  Sunny"
        dropoffs = [{"title": "Drop off Amyra", "time": "08:30"}]
        result = morning_briefing.format_briefing_message(
            [], sample_meals, dropoffs, snacks, weather_text=weather
        )
        weather_pos  = result.index("Sunny")
        dropoff_pos  = result.index("DROP-OFF")
        assert weather_pos < dropoff_pos, "Weather should appear before drop-off section"

    def test_no_weather_section_when_none(self, sample_meals):
        snacks = self._default_snacks()
        result = morning_briefing.format_briefing_message(
            [], sample_meals, [], snacks, weather_text=None
        )
        assert "Weather" not in result

    def test_meal_plan_section_present(self, sample_meals):
        snacks = self._default_snacks()
        result = morning_briefing.format_briefing_message([], sample_meals, [], snacks)
        assert "Kids Meal Plan" in result
        assert "Amyra" in result
        assert "Reyansh" in result
        assert sample_meals["amyra"]["breakfast"] in result
        assert sample_meals["reyansh"]["lunch"] in result

    def test_amyra_note_shown_when_present(self, sample_meals):
        snacks = self._default_snacks()
        sample_meals["amyra"]["note"] = "⚠️ No eggs at lunch"
        result = morning_briefing.format_briefing_message([], sample_meals, [], snacks)
        assert "No eggs at lunch" in result

    def test_positive_message_shown(self, sample_meals):
        snacks = self._default_snacks()
        result = morning_briefing.format_briefing_message(
            [], sample_meals, [], snacks, positive_message="Test message today!"
        )
        assert "Test message today!" in result

    def test_snack_section_shown_on_school_day(self, sample_meals):
        snacks = MockSnackManager(school_closed=False, briefing_text="🍎 Snack: Apple slices")
        result = morning_briefing.format_briefing_message([], sample_meals, [], snacks)
        assert "Apple slices" in result

    def test_snack_section_hidden_on_school_closure(self, sample_meals):
        snacks = MockSnackManager(school_closed=True, briefing_text="🍎 Snack: Apple slices")
        result = morning_briefing.format_briefing_message([], sample_meals, [], snacks)
        assert "Apple slices" not in result

    def test_full_output_structure(self, sample_meals):
        """Smoke test: full message should contain all major sections in order."""
        snacks = MockSnackManager(school_closed=False, briefing_text="🍎 Today's snack")
        weather = "🌤️ *Weather*\n  Warm"
        dropoffs = [{"title": "Drop off Amyra", "time": "08:30"}]

        result = morning_briefing.format_briefing_message(
            [{"title": "Event", "time": "10:00"}],
            sample_meals,
            dropoffs,
            snacks,
            positive_message="Great day ahead",
            weather_text=weather
        )

        sections = ["Weather", "DROP-OFF", "Today's Events", "Kids Meal Plan", "Great day ahead"]
        positions = [result.index(s) for s in sections]
        assert positions == sorted(positions), "Sections out of order"


# ─── has_dropoff_today ────────────────────────────────────────────────────────

class TestHasDropoffToday:
    def test_detects_drop_off_in_title(self):
        events = [{"title": "Drop off Amyra at school", "description": ""}]
        result = morning_briefing.has_dropoff_today(events)
        assert len(result) == 1

    def test_detects_drop_dash_off_in_title(self):
        events = [{"title": "Drop-off reminder", "description": ""}]
        result = morning_briefing.has_dropoff_today(events)
        assert len(result) == 1

    def test_detects_one_word_dropoff_in_title(self):
        """One-word 'dropoff' is a common spelling and should also match."""
        events = [{"title": "Dropoff Amyra", "description": ""}]
        result = morning_briefing.has_dropoff_today(events)
        assert len(result) == 1

    def test_detects_one_word_dropoff_in_description(self):
        events = [{"title": "School day", "description": "Reyansh dropoff at 8am"}]
        result = morning_briefing.has_dropoff_today(events)
        assert len(result) == 1

    def test_detects_dropoff_in_description(self):
        events = [{"title": "School day", "description": "Don't forget drop off!"}]
        result = morning_briefing.has_dropoff_today(events)
        assert len(result) == 1

    def test_no_dropoff_events_returns_empty(self):
        events = [
            {"title": "Doctor appointment", "description": "Regular checkup"},
            {"title": "Grocery run", "description": "Costco"},
        ]
        result = morning_briefing.has_dropoff_today(events)
        assert result == []

    def test_empty_events_returns_empty(self):
        assert morning_briefing.has_dropoff_today([]) == []

    def test_case_insensitive(self):
        events = [{"title": "DROP OFF AMYRA", "description": ""}]
        result = morning_briefing.has_dropoff_today(events)
        assert len(result) == 1


# ─── generate_positive_message ────────────────────────────────────────────────

# NOTE: TestGeneratePositiveMessage was removed during the agentic refactor.
# Positive messages are now composed by the OpenClaw agent at delivery time,
# so there is no Python-side LLM call to test.


# ─── Locked plan fallback in get_briefing_data ───────────────────────────────

class TestLockedMealPlanFallback:
    """
    Regression: When get_todays_meals_from_locked_plan() returns meals, they
    should be used instead of on-the-fly MealTracker suggestions. When it
    raises or returns None, fall back gracefully without crashing the briefing.
    """

    def _patches(self, tmp_skill_dir):
        calendar_mock = MagicMock()
        calendar_mock.get_events_for_today.return_value = []
        calendar_mock.sync_with_google_calendar.return_value = None
        meals_mock = MagicMock()
        meals_mock.get_meal_suggestions.return_value = SAMPLE_MEAL_SUGGESTIONS
        snacks_mock = MockSnackManager()
        return [
            patch("features.briefing.morning_briefing.SKILL_DIR", str(tmp_skill_dir)),
            patch("features.briefing.morning_briefing.FamilyCalendarAggregator", return_value=calendar_mock),
            patch("features.briefing.morning_briefing.MealTracker", return_value=meals_mock),
            patch("features.briefing.morning_briefing.SnackManager", return_value=snacks_mock),
            patch("features.briefing.morning_briefing.get_weather_briefing", return_value=None),
        ], meals_mock

    def test_uses_locked_plan_when_available(self, tmp_skill_dir):
        locked = {
            "amyra":   {"breakfast": "LOCKED BREAKFAST", "lunch": "Locked Lunch", "side": "Fruit", "note": ""},
            "reyansh": {"breakfast": "Locked R bfast",   "lunch": "Locked khichdi", "side": "Soft banana", "note": ""},
        }
        patches, meals_mock = self._patches(tmp_skill_dir)
        with patch("features.meals.weekly_meal_planner.get_todays_meals_from_locked_plan",
                   return_value=locked):
            with _apply_patches(patches):
                data = morning_briefing.get_briefing_data()
        assert data["meal_suggestions"]["amyra"]["breakfast"] == "LOCKED BREAKFAST"
        meals_mock.get_meal_suggestions.assert_not_called()

    def test_falls_back_to_on_the_fly_when_locked_none(self, tmp_skill_dir):
        patches, meals_mock = self._patches(tmp_skill_dir)
        with patch("features.meals.weekly_meal_planner.get_todays_meals_from_locked_plan",
                   return_value=None):
            with _apply_patches(patches):
                morning_briefing.get_briefing_data()
        meals_mock.get_meal_suggestions.assert_called_once()

    def test_falls_back_on_locked_plan_exception(self, tmp_skill_dir):
        patches, meals_mock = self._patches(tmp_skill_dir)
        with patch("features.meals.weekly_meal_planner.get_todays_meals_from_locked_plan",
                   side_effect=RuntimeError("broken")):
            with _apply_patches(patches):
                morning_briefing.get_briefing_data()
        meals_mock.get_meal_suggestions.assert_called_once()


# ─── Helper ───────────────────────────────────────────────────────────────────

from contextlib import contextmanager

@contextmanager
def _apply_patches(patches):
    """Context manager that enters a list of patch objects."""
    entered = []
    try:
        for p in patches:
            entered.append(p.__enter__())
        yield entered
    finally:
        for p in reversed(patches):
            p.__exit__(None, None, None)
