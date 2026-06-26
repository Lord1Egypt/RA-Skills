"""
test_restaurant_tracker.py — Unit tests for restaurant_tracker.py

Covers:
  - log_visit(): creates visit record, sets pending rating, saves
  - load_data() / save_data(): file locking, atomic write, missing file defaults
  - add_rating(): individual rating, aggregate calculation, removes from pending
  - detect_meal_type(): text-keyword and time-based detection
  - get_recommendations(): score-based ranking, meal type filter
  - format_visit_confirmation(): output structure
"""
import fcntl
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

for mod in ("google", "google.oauth2", "google.oauth2.credentials",
            "google.auth", "google.auth.transport", "google.auth.transport.requests",
            "googleapiclient", "googleapiclient.discovery"):
    sys.modules.setdefault(mod, MagicMock())

with patch("core.keychain_secrets.load_google_secrets", return_value=None), \
     patch("core.config_loader._load_config") as _mc:
    from conftest import MINIMAL_CONFIG
    from core.config_loader import Config
    _mc.return_value = Config(MINIMAL_CONFIG)
    import features.dining.restaurant_tracker as restaurant_tracker


# ─── Helpers ──────────────────────────────────────────────────────────────────

def fresh_data_file(tmp_path):
    """Return path to a fresh restaurants.json inside tmp_path/household/."""
    hh = tmp_path / "household"; hh.mkdir(exist_ok=True)
    return str(tmp_path / "household" / "restaurants.json")


# ─── load_data / save_data ────────────────────────────────────────────────────

class TestLoadData:
    def test_returns_empty_structure_when_file_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(restaurant_tracker, "DATA_FILE", fresh_data_file(tmp_path))
        data = restaurant_tracker.load_data()
        assert data == {"visits": [], "pending_ratings": {}}

    def test_reads_existing_data(self, tmp_path, monkeypatch, sample_restaurants_data):
        path = fresh_data_file(tmp_path)
        monkeypatch.setattr(restaurant_tracker, "DATA_FILE", path)
        with open(path, "w") as f:
            json.dump(sample_restaurants_data, f)
        data = restaurant_tracker.load_data()
        assert len(data["visits"]) == 1
        assert data["visits"][0]["restaurant"] == "Breakfast Republic"

    def test_creates_household_dir_if_missing(self, tmp_path, monkeypatch):
        path = str(tmp_path / "new_hh" / "restaurants.json")
        monkeypatch.setattr(restaurant_tracker, "DATA_FILE", path)
        data = restaurant_tracker.load_data()
        assert data == {"visits": [], "pending_ratings": {}}
        assert os.path.exists(os.path.dirname(path))


class TestSaveData:
    def test_saves_and_reloads(self, tmp_path, monkeypatch):
        path = fresh_data_file(tmp_path)
        monkeypatch.setattr(restaurant_tracker, "DATA_FILE", path)
        payload = {"visits": [{"id": 1, "restaurant": "Test Place"}], "pending_ratings": {}}
        restaurant_tracker.save_data(payload)
        with open(path) as f:
            loaded = json.load(f)
        assert loaded["visits"][0]["restaurant"] == "Test Place"

    def test_atomic_write_no_partial_file(self, tmp_path, monkeypatch):
        """No .tmp file should remain after save_data completes."""
        path = fresh_data_file(tmp_path)
        monkeypatch.setattr(restaurant_tracker, "DATA_FILE", path)
        restaurant_tracker.save_data({"visits": [], "pending_ratings": {}})
        tmp_files = list(Path(tmp_path / "household").glob("*.tmp"))
        assert tmp_files == [], f"Leftover tmp files: {tmp_files}"


# ─── detect_meal_type ─────────────────────────────────────────────────────────

class TestDetectMealType:
    def test_detects_breakfast_from_text(self):
        assert restaurant_tracker.detect_meal_type("eggs and pancakes") == "breakfast"

    def test_detects_lunch_from_text(self):
        assert restaurant_tracker.detect_meal_type("midday lunch") == "lunch"

    def test_detects_dinner_from_text(self):
        assert restaurant_tracker.detect_meal_type("dinner with family") == "dinner"

    def test_detects_from_time_morning(self):
        assert restaurant_tracker.detect_meal_type(time_str="08:00") == "breakfast"

    def test_detects_from_time_lunch(self):
        assert restaurant_tracker.detect_meal_type(time_str="12:30") == "lunch"

    def test_detects_from_time_dinner(self):
        assert restaurant_tracker.detect_meal_type(time_str="18:00") == "dinner"

    def test_defaults_to_time_of_day_when_no_keywords(self):
        # Should not raise; returns one of breakfast/lunch/dinner
        result = restaurant_tracker.detect_meal_type("random text without keywords")
        assert result in ("breakfast", "lunch", "dinner")


# ─── log_visit ────────────────────────────────────────────────────────────────

class TestLogVisit:
    def test_creates_visit_with_required_fields(self, tmp_path, monkeypatch):
        path = fresh_data_file(tmp_path)
        monkeypatch.setattr(restaurant_tracker, "DATA_FILE", path)
        monkeypatch.setattr(restaurant_tracker, "FAMILY_MEMBERS",
                            {"+11111111111": "Harsh", "+12222222222": "Sushmita"})
        visit = restaurant_tracker.log_visit(
            restaurant="Snooze",
            date="2026-03-27",
            meal_type="breakfast",
            items=["pancakes", "eggs"],
            total=42.0,
            source="manual"
        )
        assert visit["restaurant"] == "Snooze"
        assert visit["date"] == "2026-03-27"
        assert visit["meal_type"] == "breakfast"
        assert visit["items"] == ["pancakes", "eggs"]
        assert visit["total"] == 42.0
        assert visit["source"] == "manual"
        assert visit["rating"] is None

    def test_title_cases_restaurant_name(self, tmp_path, monkeypatch):
        path = fresh_data_file(tmp_path)
        monkeypatch.setattr(restaurant_tracker, "DATA_FILE", path)
        monkeypatch.setattr(restaurant_tracker, "FAMILY_MEMBERS", {})
        visit = restaurant_tracker.log_visit("breakfast republic")
        assert visit["restaurant"] == "Breakfast Republic"

    def test_sets_pending_ratings(self, tmp_path, monkeypatch):
        path = fresh_data_file(tmp_path)
        monkeypatch.setattr(restaurant_tracker, "DATA_FILE", path)
        monkeypatch.setattr(restaurant_tracker, "FAMILY_MEMBERS",
                            {"+1": "Harsh", "+2": "Sushmita"})
        visit = restaurant_tracker.log_visit("Test Place")
        data = restaurant_tracker.load_data()
        pending = data["pending_ratings"].get(str(visit["id"]))
        assert pending is not None
        assert "Harsh" in pending["pending_for"]
        assert "Sushmita" in pending["pending_for"]

    def test_persists_to_file(self, tmp_path, monkeypatch):
        path = fresh_data_file(tmp_path)
        monkeypatch.setattr(restaurant_tracker, "DATA_FILE", path)
        monkeypatch.setattr(restaurant_tracker, "FAMILY_MEMBERS", {})
        restaurant_tracker.log_visit("Noodle Bar")
        data = restaurant_tracker.load_data()
        assert any(v["restaurant"] == "Noodle Bar" for v in data["visits"])

    def test_auto_uses_today_when_no_date(self, tmp_path, monkeypatch):
        path = fresh_data_file(tmp_path)
        monkeypatch.setattr(restaurant_tracker, "DATA_FILE", path)
        monkeypatch.setattr(restaurant_tracker, "FAMILY_MEMBERS", {})
        visit = restaurant_tracker.log_visit("Sushi Bar")
        assert visit["date"] == datetime.now().strftime("%Y-%m-%d")


# ─── add_rating ───────────────────────────────────────────────────────────────

class TestAddRating:
    def _setup_with_visit(self, tmp_path, monkeypatch, rating=None):
        """Create a data file with one visit and return its id."""
        path = fresh_data_file(tmp_path)
        monkeypatch.setattr(restaurant_tracker, "DATA_FILE", path)
        monkeypatch.setattr(restaurant_tracker, "FAMILY_MEMBERS",
                            {"+1": "Harsh", "+2": "Sushmita"})
        visit = restaurant_tracker.log_visit(
            "Breakfast Republic", date="2026-03-20",
            meal_type="breakfast"
        )
        return visit["id"]

    def test_happy_path_adds_rating(self, tmp_path, monkeypatch):
        vid = self._setup_with_visit(tmp_path, monkeypatch)
        ok, name = restaurant_tracker.add_rating(
            visit_id=vid, rating=4, notes="Great food", sender="+1"
        )
        assert ok is True
        assert name == "Breakfast Republic"
        data = restaurant_tracker.load_data()
        v = data["visits"][0]
        assert v["individual_ratings"]["Harsh"]["rating"] == 4
        assert v["rating"] == 4.0

    def test_aggregate_rating_is_average(self, tmp_path, monkeypatch):
        vid = self._setup_with_visit(tmp_path, monkeypatch)
        restaurant_tracker.add_rating(visit_id=vid, rating=4, sender="+1")
        restaurant_tracker.add_rating(visit_id=vid, rating=2, sender="+2")
        data = restaurant_tracker.load_data()
        assert data["visits"][0]["rating"] == 3.0

    def test_rejects_rating_out_of_range(self, tmp_path, monkeypatch):
        self._setup_with_visit(tmp_path, monkeypatch)
        ok, msg = restaurant_tracker.add_rating(rating=6, sender="+1")
        assert ok is False

    def test_rejects_zero_rating(self, tmp_path, monkeypatch):
        self._setup_with_visit(tmp_path, monkeypatch)
        ok, msg = restaurant_tracker.add_rating(rating=0, sender="+1")
        assert ok is False

    def test_removes_from_pending_when_all_rated(self, tmp_path, monkeypatch):
        vid = self._setup_with_visit(tmp_path, monkeypatch)
        restaurant_tracker.add_rating(visit_id=vid, rating=4, sender="+1")
        restaurant_tracker.add_rating(visit_id=vid, rating=5, sender="+2")
        data = restaurant_tracker.load_data()
        assert str(vid) not in data["pending_ratings"]

    def test_returns_false_when_no_visits(self, tmp_path, monkeypatch):
        path = fresh_data_file(tmp_path)
        monkeypatch.setattr(restaurant_tracker, "DATA_FILE", path)
        monkeypatch.setattr(restaurant_tracker, "FAMILY_MEMBERS", {"+1": "Harsh"})
        ok, msg = restaurant_tracker.add_rating(rating=4, sender="+1")
        assert ok is False


# ─── format_visit_confirmation ────────────────────────────────────────────────

class TestFormatVisitConfirmation:
    def test_contains_restaurant_name(self):
        visit = {
            "restaurant": "Snooze AM Eatery",
            "date": "2026-03-27",
            "meal_type": "breakfast",
            "items": ["pancakes", "eggs Benedict"],
            "total": 55.00,
            "rating": None
        }
        result = restaurant_tracker.format_visit_confirmation(visit)
        assert "Snooze AM Eatery" in result

    def test_shows_items(self):
        visit = {
            "restaurant": "Snooze",
            "date": "2026-03-27",
            "meal_type": "breakfast",
            "items": ["pancakes"],
            "total": None,
            "rating": None
        }
        result = restaurant_tracker.format_visit_confirmation(visit)
        assert "pancakes" in result

    def test_shows_total_when_present(self):
        visit = {
            "restaurant": "Snooze",
            "date": "2026-03-27",
            "meal_type": "breakfast",
            "items": [],
            "total": 42.50,
            "rating": None
        }
        result = restaurant_tracker.format_visit_confirmation(visit)
        assert "42.50" in result

    def test_omits_total_when_none(self):
        visit = {
            "restaurant": "Snooze",
            "date": "2026-03-27",
            "meal_type": "breakfast",
            "items": [],
            "total": None,
            "rating": None
        }
        result = restaurant_tracker.format_visit_confirmation(visit)
        assert "$" not in result

    def test_includes_rating_prompt(self):
        visit = {
            "restaurant": "Snooze",
            "date": "2026-03-27",
            "meal_type": "breakfast",
            "items": [],
            "total": None,
            "rating": None
        }
        result = restaurant_tracker.format_visit_confirmation(visit)
        assert "rating" in result.lower() or "rate" in result.lower()


# ─── get_recommendations ──────────────────────────────────────────────────────

class TestGetRecommendations:
    def test_returns_empty_when_no_visits(self, tmp_path, monkeypatch):
        path = fresh_data_file(tmp_path)
        monkeypatch.setattr(restaurant_tracker, "DATA_FILE", path)
        recs = restaurant_tracker.get_recommendations()
        assert recs == []

    def test_filters_by_meal_type(self, tmp_path, monkeypatch):
        path = fresh_data_file(tmp_path)
        monkeypatch.setattr(restaurant_tracker, "DATA_FILE", path)
        monkeypatch.setattr(restaurant_tracker, "FAMILY_MEMBERS", {"+1": "Harsh"})
        restaurant_tracker.log_visit("Breakfast Place", meal_type="breakfast")
        restaurant_tracker.log_visit("Dinner Place", meal_type="dinner")
        restaurant_tracker.add_rating(restaurant="Breakfast Place", rating=5, sender="+1")
        restaurant_tracker.add_rating(restaurant="Dinner Place", rating=5, sender="+1")
        recs = restaurant_tracker.get_recommendations(meal_type="breakfast")
        names = [r["name"] for r in recs]
        assert "Breakfast Place" in names
        assert "Dinner Place" not in names

    def test_higher_rated_ranked_first(self, tmp_path, monkeypatch):
        path = fresh_data_file(tmp_path)
        monkeypatch.setattr(restaurant_tracker, "DATA_FILE", path)
        monkeypatch.setattr(restaurant_tracker, "FAMILY_MEMBERS", {"+1": "Harsh"})
        restaurant_tracker.log_visit("Good Place", meal_type="dinner")
        restaurant_tracker.log_visit("Great Place", meal_type="dinner")
        restaurant_tracker.add_rating(restaurant="Good Place", rating=3, sender="+1")
        restaurant_tracker.add_rating(restaurant="Great Place", rating=5, sender="+1")
        recs = restaurant_tracker.get_recommendations()
        assert recs[0]["name"] == "Great Place"
