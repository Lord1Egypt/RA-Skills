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
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch


sys.path.insert(0, str(Path(__file__).parent.parent))


with patch("core.config_loader._load_config") as _mc:
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
                            {"+11111111111": "Alex", "+12222222222": "Sam"})
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
                            {"+1": "Alex", "+2": "Sam"})
        visit = restaurant_tracker.log_visit("Test Place")
        data = restaurant_tracker.load_data()
        pending = data["pending_ratings"].get(str(visit["id"]))
        assert pending is not None
        assert "Alex" in pending["pending_for"]
        assert "Sam" in pending["pending_for"]

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


# ─── log_visit: merge on (date, restaurant) ───────────────────────────────────
#
# Regression cover for 2026-08-22. The evening calendar sync auto-logged a
# Bamboo Bistro dinner at 20:15 with no items and no total; the receipt photo
# arrived at 23:35. log_visit() appended unconditionally, so obeying the
# "receipt → log_restaurant_visit" rule would have written a second visit and
# a second rating prompt for one dinner.

class TestLogVisitMerge:
    def _tracker(self, tmp_path, monkeypatch):
        monkeypatch.setattr(restaurant_tracker, "DATA_FILE",
                            fresh_data_file(tmp_path))
        monkeypatch.setattr(restaurant_tracker, "FAMILY_MEMBERS",
                            {"+1": "Alex", "+2": "Sam"})

    def test_receipt_merges_into_calendar_visit(self, tmp_path, monkeypatch):
        self._tracker(tmp_path, monkeypatch)
        first = restaurant_tracker.log_visit(
            "Bamboo Bistro", date="2026-08-22", meal_type="dinner",
            source="calendar"
        )
        merged = restaurant_tracker.log_visit(
            "Bamboo Bistro", date="2026-08-22", meal_type="dinner",
            items=["Chicken Dumplings", "Seafood Fried Rice"], total=477.72,
            source="manual"
        )
        data = restaurant_tracker.load_data()
        assert len(data["visits"]) == 1
        assert merged["id"] == first["id"]
        assert data["visits"][0]["items"] == ["Chicken Dumplings",
                                              "Seafood Fried Rice"]
        assert data["visits"][0]["total"] == 477.72

    def test_merge_does_not_duplicate_pending_ratings(self, tmp_path, monkeypatch):
        self._tracker(tmp_path, monkeypatch)
        restaurant_tracker.log_visit("Bamboo Bistro", date="2026-08-22",
                                     source="calendar")
        restaurant_tracker.log_visit("Bamboo Bistro", date="2026-08-22",
                                     total=477.72)
        data = restaurant_tracker.load_data()
        assert len(data["pending_ratings"]) == 1

    def test_merge_matches_regardless_of_name_case(self, tmp_path, monkeypatch):
        self._tracker(tmp_path, monkeypatch)
        restaurant_tracker.log_visit("Bamboo Bistro", date="2026-08-22")
        restaurant_tracker.log_visit("bamboo bistro", date="2026-08-22",
                                     total=477.72)
        data = restaurant_tracker.load_data()
        assert len(data["visits"]) == 1
        assert data["visits"][0]["total"] == 477.72

    def test_merge_never_blanks_existing_detail(self, tmp_path, monkeypatch):
        """A calendar sync running after the receipt must not erase it."""
        self._tracker(tmp_path, monkeypatch)
        restaurant_tracker.log_visit("Bamboo Bistro", date="2026-08-22",
                                     items=["Chicken Curry"], total=477.72)
        restaurant_tracker.log_visit("Bamboo Bistro", date="2026-08-22",
                                     source="calendar")
        data = restaurant_tracker.load_data()
        assert len(data["visits"]) == 1
        assert data["visits"][0]["items"] == ["Chicken Curry"]
        assert data["visits"][0]["total"] == 477.72

    def test_same_restaurant_different_day_stays_separate(self, tmp_path, monkeypatch):
        self._tracker(tmp_path, monkeypatch)
        restaurant_tracker.log_visit("Bamboo Bistro", date="2026-08-22")
        restaurant_tracker.log_visit("Bamboo Bistro", date="2026-08-23")
        data = restaurant_tracker.load_data()
        assert len(data["visits"]) == 2

    def test_merge_marker_is_not_persisted(self, tmp_path, monkeypatch):
        self._tracker(tmp_path, monkeypatch)
        restaurant_tracker.log_visit("Bamboo Bistro", date="2026-08-22")
        merged = restaurant_tracker.log_visit("Bamboo Bistro",
                                              date="2026-08-22", total=477.72)
        assert merged["_merged"] is True
        data = restaurant_tracker.load_data()
        assert "_merged" not in data["visits"][0]

    def test_merge_preserves_ratings_already_given(self, tmp_path, monkeypatch):
        self._tracker(tmp_path, monkeypatch)
        visit = restaurant_tracker.log_visit("Bamboo Bistro", date="2026-08-22",
                                             source="calendar")
        restaurant_tracker.add_rating(visit_id=visit["id"], rating=5, sender="+1")
        restaurant_tracker.log_visit("Bamboo Bistro", date="2026-08-22",
                                     total=477.72)
        data = restaurant_tracker.load_data()
        assert len(data["visits"]) == 1
        assert data["visits"][0]["individual_ratings"]["Alex"]["rating"] == 5


# ─── add_rating ───────────────────────────────────────────────────────────────

class TestAddRating:
    def _setup_with_visit(self, tmp_path, monkeypatch, rating=None):
        """Create a data file with one visit and return its id."""
        path = fresh_data_file(tmp_path)
        monkeypatch.setattr(restaurant_tracker, "DATA_FILE", path)
        monkeypatch.setattr(restaurant_tracker, "FAMILY_MEMBERS",
                            {"+1": "Alex", "+2": "Sam"})
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
        assert v["individual_ratings"]["Alex"]["rating"] == 4
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
        monkeypatch.setattr(restaurant_tracker, "FAMILY_MEMBERS", {"+1": "Alex"})
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

    def test_says_logged_for_a_new_visit(self):
        visit = {
            "restaurant": "Snooze", "date": "2026-03-27",
            "meal_type": "breakfast", "items": [], "total": None,
            "rating": None
        }
        assert "Logged" in restaurant_tracker.format_visit_confirmation(visit)

    def test_says_updated_when_merged_into_existing_visit(self):
        visit = {
            "restaurant": "Bamboo Bistro", "date": "2026-08-22",
            "meal_type": "dinner", "items": ["Chicken Curry"], "total": 477.72,
            "rating": None, "_merged": True
        }
        result = restaurant_tracker.format_visit_confirmation(visit)
        assert "Updated" in result
        assert "Logged" not in result

    def test_omits_rating_prompt_when_already_rated(self):
        visit = {
            "restaurant": "Bamboo Bistro", "date": "2026-08-22",
            "meal_type": "dinner", "items": [], "total": 477.72,
            "rating": 5.0, "individual_ratings": {"Alex": {"rating": 5}},
            "_merged": True
        }
        result = restaurant_tracker.format_visit_confirmation(visit)
        assert "rate" not in result.lower()


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
        monkeypatch.setattr(restaurant_tracker, "FAMILY_MEMBERS", {"+1": "Alex"})
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
        monkeypatch.setattr(restaurant_tracker, "FAMILY_MEMBERS", {"+1": "Alex"})
        restaurant_tracker.log_visit("Good Place", meal_type="dinner")
        restaurant_tracker.log_visit("Great Place", meal_type="dinner")
        restaurant_tracker.add_rating(restaurant="Good Place", rating=3, sender="+1")
        restaurant_tracker.add_rating(restaurant="Great Place", rating=5, sender="+1")
        recs = restaurant_tracker.get_recommendations()
        assert recs[0]["name"] == "Great Place"


# ─── check_calendar_for_restaurants ──────────────────────────────────────────
#
# This function had no test coverage at all, and had quietly filled
# restaurants.json with friends' names: 10 of the 18 distinct "restaurants" on
# disk were entries like "With Rohan And Meera" (from "Dinner with Rohan and Meera") or "Arjun And Leela'S" (from "Dinner at Arjun and Leela's" — a
# house, not a restaurant). They then fed get_top_restaurants back to the
# family as places worth eating. The cases below mirror the real titles,
# with the names changed — what they exercise is the grammatical shape.

class TestCheckCalendarForRestaurants:
    def _titles(self, *titles):
        return [{"title": t, "date": "2026-08-01", "time": "19:00"} for t in titles]

    def test_extracts_a_venue_named_after_at(self):
        found = restaurant_tracker.check_calendar_for_restaurants(
            self._titles("Dinner at Din Tai Fung")
        )
        assert [f["restaurant"] for f in found] == ["Din Tai Fung"]
        assert found[0]["source"] == "calendar"
        assert found[0]["date"] == "2026-08-01"

    def test_company_is_not_a_venue(self):
        """Regression: 'dinner with X' produced a restaurant called 'With X'."""
        found = restaurant_tracker.check_calendar_for_restaurants(self._titles(
            "Dinner with Rohan and Meera",
            "Dinner with Anil and Roshni",
            "Lunch with Tara and Vikram",
            "BBQ with Manav and Ishita",
        ))
        assert found == []

    def test_a_friends_house_is_not_a_restaurant(self):
        """Regression: 'Dinner at <two names>'s' is someone's home."""
        found = restaurant_tracker.check_calendar_for_restaurants(self._titles(
            "Dinner at Kabir and Nisha's",
            "Dinner at Arjun and Leela's",
            "Lunch at Devan and Anjali's",
            "Dinner at Simran and Omar's",
        ))
        assert found == []

    def test_a_real_restaurant_ending_in_possessive_survives(self):
        """The home filter keys on the conjunction, not the apostrophe —
        otherwise it would eat Denny's and Applebee's."""
        found = restaurant_tracker.check_calendar_for_restaurants(self._titles(
            "Breakfast at Denny's", "Dinner at Applebee's",
        ))
        assert [f["restaurant"] for f in found] == ["Denny's", "Applebee's"]

    def test_trailing_company_after_a_venue_is_dropped(self):
        found = restaurant_tracker.check_calendar_for_restaurants(
            self._titles("Dinner at with the Nolans")
        )
        assert found == []

    def test_meal_type_comes_from_the_title(self):
        found = restaurant_tracker.check_calendar_for_restaurants(
            self._titles("Breakfast at Snooze")
        )
        assert found[0]["meal_type"] == "breakfast"

    def test_unrelated_events_are_ignored(self):
        found = restaurant_tracker.check_calendar_for_restaurants(self._titles(
            "Ana swim class", "Trip to Seattle", "Costco run",
            "Dentist appointment",
        ))
        assert found == []


class TestVenueSplitterRejectsNonVenues:
    """Regression: the locative " at " splitter closed the "dinner with X"
    class and opened a "dinner at <time>" one. `Dinner at 6pm` is an ordinary
    calendar title and was logged as a restaurant called "6Pm"; these names
    reach the family through get_top_restaurants."""

    NOT_VENUES = [
        "Dinner at 6pm", "Lunch at 12:30", "Cafe meeting at 3pm",
        "Restaurant week starts at noon", "Lunch at work", "Lunch at home",
        "Dinner at 7", "Breakfast at midnight",
    ]

    def test_a_time_or_a_generic_place_is_not_a_venue(self):
        for title in self.NOT_VENUES:
            found = restaurant_tracker.check_calendar_for_restaurants(
                [{"title": title, "date": "2026-09-02"}])
            assert found == [], f"{title!r} was logged as {found}"

    def test_a_real_venue_still_lands(self):
        found = restaurant_tracker.check_calendar_for_restaurants(
            [{"title": "Dinner at Bamboo Bistro", "date": "2026-09-02"}])
        assert [f["restaurant"] for f in found] == ["Bamboo Bistro"]

    def test_an_apostrophe_survives_titlecasing(self):
        """str.title() produced "Denny'S", and that mangled name is what was
        stored and handed back to the family."""
        found = restaurant_tracker.check_calendar_for_restaurants(
            [{"title": "Dinner at Denny's", "date": "2026-09-02"}])
        assert [f["restaurant"] for f in found] == ["Denny's"]


class TestVisitIdsDoNotCollideWithPendingRatings:
    """pending_ratings is keyed on the visit id. A length-derived id — or a
    max() over visits alone — can hand out an id a live pending entry still
    holds, overwriting another restaurant's pending rating."""

    def test_a_new_visit_does_not_reuse_a_live_pending_key(self, tmp_path, monkeypatch):
        monkeypatch.setattr(restaurant_tracker, "DATA_FILE", fresh_data_file(tmp_path))
        a = restaurant_tracker.log_visit("Alpha", date="2026-08-01")
        b = restaurant_tracker.log_visit("Beta", date="2026-08-02")

        # The top visit is removed while its pending rating survives, which is
        # the shape the live restaurants.json is already in.
        data = restaurant_tracker.load_data()
        data["visits"] = [v for v in data["visits"] if v["id"] != b["id"]]
        restaurant_tracker.save_data(data)
        assert str(b["id"]) in restaurant_tracker.load_data()["pending_ratings"]

        c = restaurant_tracker.log_visit("Gamma", date="2026-08-03")
        assert c["id"] != b["id"], "the new visit clobbered a live pending rating"
        assert c["id"] != a["id"]
