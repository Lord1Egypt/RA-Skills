"""
test_morning_briefing.py — Unit tests for morning_briefing.py

Covers:
  - has_dropoff_today(): title and description matching
  - Locked meal plan fallback logic (integration-style with mocks)
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch


sys.path.insert(0, str(Path(__file__).parent.parent))

# ── Prevent module-level side effects ────────────────────────────────────────


from conftest import MockSnackManager, SAMPLE_MEAL_SUGGESTIONS  # noqa: E402


# Import the module under test
with patch("core.config_loader._load_config") as _mock_cfg:
    from conftest import MINIMAL_CONFIG
    from core.config_loader import Config
    _mock_cfg.return_value = Config(MINIMAL_CONFIG)
    import features.briefing.morning_briefing as morning_briefing  # noqa: E402


# ─── has_dropoff_today ────────────────────────────────────────────────────────

class TestHasDropoffToday:
    def test_detects_drop_off_in_title(self):
        events = [{"title": "Drop off Ana at school", "description": ""}]
        result = morning_briefing.has_dropoff_today(events)
        assert len(result) == 1

    def test_detects_drop_dash_off_in_title(self):
        events = [{"title": "Drop-off reminder", "description": ""}]
        result = morning_briefing.has_dropoff_today(events)
        assert len(result) == 1

    def test_detects_one_word_dropoff_in_title(self):
        """One-word 'dropoff' is a common spelling and should also match."""
        events = [{"title": "Dropoff Ana", "description": ""}]
        result = morning_briefing.has_dropoff_today(events)
        assert len(result) == 1

    def test_detects_one_word_dropoff_in_description(self):
        events = [{"title": "School day", "description": "Ben dropoff at 8am"}]
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
        events = [{"title": "DROP OFF ANA", "description": ""}]
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
            "ana":   {"breakfast": "LOCKED BREAKFAST", "lunch": "Locked Lunch", "side": "Fruit", "note": ""},
            "ben": {"breakfast": "Locked R bfast",   "lunch": "Locked khichdi", "side": "Soft banana", "note": ""},
        }
        patches, meals_mock = self._patches(tmp_skill_dir)
        with patch("features.meals.weekly_meal_planner.get_todays_meals_from_locked_plan",
                   return_value=locked):
            with _apply_patches(patches):
                data = morning_briefing.get_briefing_data()
        assert data["meal_suggestions"]["ana"]["breakfast"] == "LOCKED BREAKFAST"
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


# ─── snack_warning is not gated on snack_text ─────────────────────────────────

class TestSnackWarningIsUngated:
    """
    Regression: `snack_warning` used to be computed as

        should_warn_about_missing_schedule() if not snack_text else None

    which reads like "don't nag when we clearly have a schedule". It never
    suppressed the missing-current-month warning — a snack for today is the
    very key that makes that month "loaded" — and it always suppressed the
    end-of-month "send next month's photo" reminder, whose entire window is
    ordinary school days with snacks. September 2026's reminder was built and
    discarded on every run of its window.

    The warning is the school asking for something. It travels regardless of
    what today's snack looks like.
    """

    def _patches(self, tmp_skill_dir, snacks_mock):
        calendar_mock = MagicMock()
        calendar_mock.get_events_for_today.return_value = []
        calendar_mock.sync_with_google_calendar.return_value = None
        meals_mock = MagicMock()
        meals_mock.get_meal_suggestions.return_value = SAMPLE_MEAL_SUGGESTIONS
        return [
            patch("features.briefing.morning_briefing.SKILL_DIR", str(tmp_skill_dir)),
            patch("features.briefing.morning_briefing.FamilyCalendarAggregator", return_value=calendar_mock),
            patch("features.briefing.morning_briefing.MealTracker", return_value=meals_mock),
            patch("features.briefing.morning_briefing.SnackManager", return_value=snacks_mock),
            patch("features.briefing.morning_briefing.get_weather_briefing", return_value=None),
        ]

    def _data(self, tmp_skill_dir, snacks_mock):
        with _apply_patches(self._patches(tmp_skill_dir, snacks_mock)):
            return morning_briefing.get_briefing_data()

    def test_warning_survives_a_day_that_has_a_snack(self, tmp_skill_dir):
        warning = ("📸 *Heads up* — please send the snack schedule photo "
                   "for September when it's posted at school.")
        snacks = MockSnackManager(briefing_text="🍎 *School Snacks Today*\n  Morning: Goldfish",
                                  warning=warning)
        data = self._data(tmp_skill_dir, snacks)
        assert data["snack_warning"] == warning
        assert data["snack"].startswith("🍎 *School Snacks Today*")

    def test_warning_travels_when_there_is_no_snack(self, tmp_skill_dir):
        warning = "📸 *Snack schedule missing for August*\nPlease send a photo."
        snacks = MockSnackManager(briefing_text="", warning=warning)
        data = self._data(tmp_skill_dir, snacks)
        assert data["snack_warning"] == warning

    def test_no_warning_stays_none(self, tmp_skill_dir):
        snacks = MockSnackManager(briefing_text="🍎 *School Snacks Today*\n  Morning: Goldfish",
                                  warning="")
        data = self._data(tmp_skill_dir, snacks)
        assert not data["snack_warning"]

    def test_warning_is_not_duplicated_into_the_snack_field(self, tmp_skill_dir):
        # The other half of the fix: format_for_briefing() no longer returns a
        # warning in place of snack text, so the two fields cannot both carry
        # it and the message cannot say it twice.
        warning = ("📸 *Heads up* — please send the snack schedule photo "
                   "for September when it's posted at school.")
        snacks = MockSnackManager(briefing_text=None, warning=warning)
        data = self._data(tmp_skill_dir, snacks)
        assert data["snack_warning"] == warning
        assert not data["snack"]

    def test_warning_survives_a_closed_school_day(self, tmp_skill_dir):
        # School closed means no snack, but the school can still be waiting on
        # next month's photo.
        warning = ("📸 *Heads up* — please send the snack schedule photo "
                   "for September when it's posted at school.")
        snacks = MockSnackManager(school_closed=True, briefing_text="ignored",
                                  warning=warning)
        data = self._data(tmp_skill_dir, snacks)
        assert data["snack_warning"] == warning
        assert not data["snack"]


class TestBriefingOptsIntoRestaurantDetection:
    """The calendar->restaurant auto-log is opt-in now, and the receipt-merge
    path in log_visit depends on the briefing having done it: a dinner already
    on the calendar gets logged here so a receipt photographed later that
    night merges into that visit instead of creating a second one. An edit
    dropping either kwarg would break that silently."""

    def test_get_briefing_data_forces_a_sync_and_asks_for_detection(self, tmp_skill_dir):
        calendar_mock = MagicMock()
        calendar_mock.get_events_for_today.return_value = []
        calendar_mock.sync_with_google_calendar.return_value = None
        meals_mock = MagicMock()
        meals_mock.get_meal_suggestions.return_value = SAMPLE_MEAL_SUGGESTIONS
        patches = [
            patch("features.briefing.morning_briefing.SKILL_DIR", str(tmp_skill_dir)),
            patch("features.briefing.morning_briefing.FamilyCalendarAggregator",
                  return_value=calendar_mock),
            patch("features.briefing.morning_briefing.MealTracker", return_value=meals_mock),
            patch("features.briefing.morning_briefing.SnackManager",
                  return_value=MockSnackManager()),
            patch("features.briefing.morning_briefing.get_weather_briefing", return_value=None),
        ]
        with _apply_patches(patches):
            morning_briefing.get_briefing_data()
        calendar_mock.sync_with_google_calendar.assert_called_once_with(
            detect_restaurants=True, force=True)
