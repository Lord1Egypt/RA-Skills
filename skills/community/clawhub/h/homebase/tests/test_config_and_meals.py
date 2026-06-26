"""
Tests for config-driven features.
Covers: structured kids[].meals, config-driven meal suggestions,
Kid.emoji_char, _tracked_names, Config.app_name/owner_phone, the catalog
learning + validator path.
"""

import json
import os
import pytest
from unittest.mock import patch, MagicMock

from conftest import MINIMAL_CONFIG


# ── Config accessor tests ────────────────────────────────────────────────────

class TestConfigAccessors:

    def test_app_name_from_config(self, tmp_skill_dir):
        from core.config_loader import Config
        cfg = Config({**MINIMAL_CONFIG, "app": {"name": "Test Homebase"}})
        assert cfg.app_name == "Test Homebase"

    def test_app_name_default(self, tmp_skill_dir):
        from core.config_loader import Config
        cfg = Config({})
        assert cfg.app_name == "Homebase"

    def test_owner_phone(self, tmp_skill_dir):
        from core.config_loader import Config
        cfg = Config({**MINIMAL_CONFIG, "app": {"owner_phone": "+15551234567"}})
        assert cfg.owner_phone == "+15551234567"

    def test_owner_phone_default_empty(self, tmp_skill_dir):
        from core.config_loader import Config
        cfg = Config({})
        assert cfg.owner_phone == ""


# ── Kid emoji tests ──────────────────────────────────────────────────────────

class TestKidEmoji:

    def test_girl_emoji(self, tmp_skill_dir):
        from core.config_loader import Kid
        kid = Kid({"name": "Alice", "emoji": "girl"})
        assert kid.emoji_char == "\U0001F467"  # 👧

    def test_boy_emoji(self, tmp_skill_dir):
        from core.config_loader import Kid
        kid = Kid({"name": "Bob", "emoji": "boy"})
        assert kid.emoji_char == "\U0001F466"  # 👦

    def test_unknown_emoji_fallback(self, tmp_skill_dir):
        from core.config_loader import Kid
        kid = Kid({"name": "Pat", "emoji": "other"})
        assert kid.emoji_char == "\U0001F9D2"  # 🧒

    def test_missing_emoji_fallback(self, tmp_skill_dir):
        from core.config_loader import Kid
        kid = Kid({"name": "Pat"})
        assert kid.emoji == "child"
        assert kid.emoji_char == "\U0001F9D2"


# ── Materializer tests ───────────────────────────────────────────────────────

class TestMaterializeOptions:

    def test_options_only(self, tmp_skill_dir):
        from features.meals.meal_tracker import _materialize_options
        out = _materialize_options({"options": ["A", "B", "C"]})
        assert out == ["A", "B", "C"]

    def test_fixed_dish_with_grains(self, tmp_skill_dir):
        from features.meals.meal_tracker import _materialize_options
        out = _materialize_options({
            "fixed_dish": "Khichdi",
            "rotate_grains": ["rice", "quinoa"],
        })
        assert out == ["Khichdi (rice)", "Khichdi (quinoa)"]

    def test_fixed_dish_combined_with_options(self, tmp_skill_dir):
        from features.meals.meal_tracker import _materialize_options
        out = _materialize_options({
            "fixed_dish": "Khichdi",
            "rotate_grains": ["rice"],
            "options": ["Soft toast"],
        })
        assert out == ["Khichdi (rice)", "Soft toast"]

    def test_empty_returns_empty(self, tmp_skill_dir):
        from features.meals.meal_tracker import _materialize_options
        assert _materialize_options({}) == []


# ── Config-driven meal suggestions ───────────────────────────────────────────

class TestConfigDrivenMealSuggestions:

    # These mirror the live homebase/config.json catalog. The MealTracker
    # singleton config comes from there, not the tmp_skill_dir fixture.
    AMYRA_BF_OPTIONS = ["Scrambled eggs", "Oats", "Jam toast", "Dalia", "Poha", "Upma"]
    AMYRA_LUNCH      = ["Cheese sandwich", "Bread jam", "Egg bites"]
    AMYRA_SIDES      = ["Fruit", "Roasted chana", "Makhana"]

    def test_returns_suggestions_for_all_configured_kids(self, tmp_skill_dir):
        from features.meals.meal_tracker import MealTracker
        tracker = MealTracker(str(tmp_skill_dir))
        suggestions = tracker.get_meal_suggestions()
        assert "amyra" in suggestions
        assert "reyansh" in suggestions

    def test_breakfast_from_config_options(self, tmp_skill_dir):
        from features.meals.meal_tracker import MealTracker
        tracker = MealTracker(str(tmp_skill_dir))
        amyra = tracker.get_meal_suggestions()["amyra"]
        assert amyra["breakfast"] in self.AMYRA_BF_OPTIONS

    def test_lunch_from_config_options(self, tmp_skill_dir):
        from features.meals.meal_tracker import MealTracker
        tracker = MealTracker(str(tmp_skill_dir))
        amyra = tracker.get_meal_suggestions()["amyra"]
        assert amyra["lunch"] in self.AMYRA_LUNCH

    def test_reyansh_lunch_is_from_pool(self, tmp_skill_dir):
        """Reyansh's lunch must come from the resolved pool — every option
        is either a khichdi rotation or an explicit `options` entry like
        Dalia. The test asserts "in the pool" rather than "always khichdi"
        because his real config includes Dalia as an alternate lunch."""
        from features.meals.meal_tracker import MealTracker
        tracker = MealTracker(str(tmp_skill_dir))
        kid = next(k for k in tracker.config.kids if k.name.lower() == "reyansh")
        valid = set(tracker._approved_options_for(kid, "lunch"))
        assert valid, "Reyansh lunch pool should not be empty"
        for _ in range(15):
            r = tracker.get_meal_suggestions()["reyansh"]
            assert r["lunch"] in valid, f"{r['lunch']!r} not in {valid}"

    def test_egg_rule_filtering(self, tmp_skill_dir):
        """When kid had eggs at breakfast, egg items must not appear at lunch."""
        from features.meals.meal_tracker import MealTracker
        tracker = MealTracker(str(tmp_skill_dir))
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        tracker.log_meal("amyra", "breakfast", "Scrambled eggs", today)
        for _ in range(20):
            amyra = tracker.get_meal_suggestions()["amyra"]
            assert "egg" not in amyra["lunch"].lower(), \
                f"Egg item '{amyra['lunch']}' appeared at lunch after eggs for breakfast"

    def test_sides_from_config(self, tmp_skill_dir):
        from features.meals.meal_tracker import MealTracker
        tracker = MealTracker(str(tmp_skill_dir))
        amyra = tracker.get_meal_suggestions()["amyra"]
        assert amyra["side"] in self.AMYRA_SIDES

    def test_empty_meals_returns_tbd(self, tmp_skill_dir):
        """Kid with no meals dict gets TBD suggestions."""
        from features.meals.meal_tracker import MealTracker
        from core.config_loader import Config
        empty_config = Config({
            "family": {"kids": [{"name": "NoRules", "meals": {}}]}
        })
        tracker = MealTracker(str(tmp_skill_dir))
        tracker.config = empty_config
        suggestions = tracker.get_meal_suggestions()
        assert suggestions["norules"]["breakfast"] == "TBD"
        assert suggestions["norules"]["lunch"] == "TBD"

    def test_kid_name_preserved(self, tmp_skill_dir):
        from features.meals.meal_tracker import MealTracker
        tracker = MealTracker(str(tmp_skill_dir))
        suggestions = tracker.get_meal_suggestions()
        assert suggestions["amyra"]["name"] == "Amyra"
        assert suggestions["reyansh"]["name"] == "Reyansh"


# ── Weekly pool resolver ─────────────────────────────────────────────────────

class TestWeeklyPool:

    def test_returns_seven_days_default(self, tmp_skill_dir):
        from features.meals.meal_tracker import MealTracker
        pool = MealTracker(str(tmp_skill_dir)).get_weekly_pool()
        assert set(pool.keys()) == {"monday", "tuesday", "wednesday",
                                     "thursday", "friday", "saturday", "sunday"}

    def test_each_day_has_each_kid_with_three_slots(self, tmp_skill_dir):
        from features.meals.meal_tracker import MealTracker
        pool = MealTracker(str(tmp_skill_dir)).get_weekly_pool()
        for day, day_pool in pool.items():
            for kid in ("amyra", "reyansh"):
                assert kid in day_pool
                assert {"breakfast", "lunch", "sides"} <= set(day_pool[kid].keys())

    def test_reyansh_lunch_pool_includes_khichdi_rotations(self, tmp_skill_dir):
        """The pool must include the khichdi rotations from fixed_dish + rotate_grains.
        It may also include explicit 'options' entries (e.g. Dalia)."""
        from features.meals.meal_tracker import MealTracker
        pool = MealTracker(str(tmp_skill_dir)).get_weekly_pool()
        lunch_pool = pool["monday"]["reyansh"]["lunch"]
        assert lunch_pool, "lunch pool empty"
        khichdi = [o for o in lunch_pool if "khichdi" in o.lower()]
        assert len(khichdi) >= 1, f"expected khichdi rotations, got {lunch_pool}"

    def test_amyra_lunch_pool_includes_eggs_unconstrained(self, tmp_skill_dir):
        """Pool is unconstrained — constraints apply at validate_plan time."""
        from features.meals.meal_tracker import MealTracker
        pool = MealTracker(str(tmp_skill_dir)).get_weekly_pool()
        assert "Egg bites" in pool["monday"]["amyra"]["lunch"]


# ── Plan validation ──────────────────────────────────────────────────────────

class TestValidatePlan:

    def _full_plan(self, lunch_for_amyra="Cheese sandwich", bf_for_amyra="Oats"):
        # Sides must match the live config catalog exactly. Tests share the
        # singleton config loaded from homebase/config.json, so use values
        # that exist in both the real config and the conftest fixture.
        return {
            day: {
                "amyra":   {"breakfast": bf_for_amyra,
                            "lunch":     lunch_for_amyra,
                            "side":      "Fruit"},
                "reyansh": {"breakfast": "Oats",
                            "lunch":     "Khichdi (rice)",
                            "side":      "Blueberries"},
            }
            for day in ["monday", "tuesday", "wednesday", "thursday",
                        "friday", "saturday", "sunday"]
        }

    def test_valid_plan_passes(self, tmp_skill_dir):
        from features.meals.meal_tracker import MealTracker
        tracker = MealTracker(str(tmp_skill_dir))
        result  = tracker.validate_plan(self._full_plan())
        assert result["ok"] is True
        assert result["corrections"] == []

    def test_off_catalog_breakfast_rejected(self, tmp_skill_dir):
        from features.meals.meal_tracker import MealTracker
        tracker = MealTracker(str(tmp_skill_dir))
        plan = self._full_plan(bf_for_amyra="Pizza")
        result = tracker.validate_plan(plan)
        assert result["ok"] is False
        assert any("breakfast" in e and "Pizza" in e for e in result["errors"])

    def test_egg_breakfast_egg_lunch_auto_corrected(self, tmp_skill_dir):
        from features.meals.meal_tracker import MealTracker
        tracker = MealTracker(str(tmp_skill_dir))
        plan = self._full_plan(bf_for_amyra="Scrambled eggs", lunch_for_amyra="Egg bites")
        result = tracker.validate_plan(plan)
        assert result["ok"] is True
        assert len(result["corrections"]) == 7  # all 7 days
        # The plan dict was mutated in place to swap lunch
        assert all(plan[day]["amyra"]["lunch"] != "Egg bites" for day in plan)


# ── Catalog learning ─────────────────────────────────────────────────────────

class TestCatalogLearning:

    def test_log_meal_known_food_does_not_create_pending(self, tmp_skill_dir):
        from features.meals.meal_tracker import MealTracker
        tracker = MealTracker(str(tmp_skill_dir))
        in_cat, _ = tracker.log_meal("amyra", "breakfast", "Oats")
        assert in_cat is True
        assert tracker.get_pending_reviews() == []

    def test_log_meal_unknown_food_creates_pending(self, tmp_skill_dir):
        from features.meals.meal_tracker import MealTracker
        tracker = MealTracker(str(tmp_skill_dir))
        in_cat, reason = tracker.log_meal("amyra", "breakfast", "Pancakes")
        assert in_cat is False
        assert "Pancakes" in (reason or "")
        pending = tracker.get_pending_reviews()
        assert len(pending) == 1
        assert pending[0]["meal"] == "Pancakes"
        assert pending[0]["occurrences"] == 1

    def test_log_meal_repeat_unknown_food_increments_count(self, tmp_skill_dir):
        from features.meals.meal_tracker import MealTracker
        tracker = MealTracker(str(tmp_skill_dir))
        tracker.log_meal("amyra", "breakfast", "Pancakes")
        tracker.log_meal("amyra", "breakfast", "pancakes")  # different case
        pending = tracker.get_pending_reviews()
        assert len(pending) == 1
        assert pending[0]["occurrences"] == 2

    def test_apply_decisions_accept_promotes_to_learned(self, tmp_skill_dir):
        from features.meals.meal_tracker import MealTracker
        tracker = MealTracker(str(tmp_skill_dir))
        tracker.log_meal("amyra", "breakfast", "Pancakes")
        result = tracker.apply_catalog_decisions([{"index": 0, "decision": "accept"}])
        assert result["ok"] is True
        # Now Pancakes should be a known catalog item
        assert tracker._is_in_catalog("amyra", "breakfast", "Pancakes") is True
        assert tracker.get_pending_reviews() == []

    def test_apply_decisions_reject_drops_without_promoting(self, tmp_skill_dir):
        from features.meals.meal_tracker import MealTracker
        tracker = MealTracker(str(tmp_skill_dir))
        tracker.log_meal("amyra", "breakfast", "Pancakes")
        result = tracker.apply_catalog_decisions([{"index": 0, "decision": "reject"}])
        assert result["ok"] is True
        assert tracker._is_in_catalog("amyra", "breakfast", "Pancakes") is False
        assert tracker.get_pending_reviews() == []

    def test_apply_decisions_out_of_range_index_rejects_batch(self, tmp_skill_dir):
        from features.meals.meal_tracker import MealTracker
        tracker = MealTracker(str(tmp_skill_dir))
        tracker.log_meal("amyra", "breakfast", "Pancakes")
        # Index 5 doesn't exist (only 1 pending)
        result = tracker.apply_catalog_decisions([
            {"index": 0, "decision": "accept"},
            {"index": 5, "decision": "accept"},
        ])
        assert result["ok"] is False
        assert "out of range" in result["error"]
        # Pending list must NOT have been mutated
        assert len(tracker.get_pending_reviews()) == 1

    def test_apply_decisions_duplicate_index_rejects_batch(self, tmp_skill_dir):
        from features.meals.meal_tracker import MealTracker
        tracker = MealTracker(str(tmp_skill_dir))
        tracker.log_meal("amyra", "breakfast", "Pancakes")
        tracker.log_meal("amyra", "breakfast", "Waffles")
        result = tracker.apply_catalog_decisions([
            {"index": 0, "decision": "accept"},
            {"index": 0, "decision": "accept"},
        ])
        assert result["ok"] is False
        assert "duplicate" in result["error"]

    def test_apply_decisions_unknown_decision_rejects_batch(self, tmp_skill_dir):
        from features.meals.meal_tracker import MealTracker
        tracker = MealTracker(str(tmp_skill_dir))
        tracker.log_meal("amyra", "breakfast", "Pancakes")
        result = tracker.apply_catalog_decisions([
            {"index": 0, "decision": "maybe"},
        ])
        assert result["ok"] is False
        assert "accept" in result["error"]

    def test_learned_catalog_persists_across_instances(self, tmp_skill_dir):
        from features.meals.meal_tracker import MealTracker
        t1 = MealTracker(str(tmp_skill_dir))
        t1.log_meal("amyra", "breakfast", "Pancakes")
        t1.apply_catalog_decisions([{"index": 0, "decision": "accept"}])

        t2 = MealTracker(str(tmp_skill_dir))
        assert t2._is_in_catalog("amyra", "breakfast", "Pancakes") is True


# ── _tracked_names tests ─────────────────────────────────────────────────────

class TestTrackedNames:

    def test_returns_configured_names(self, tmp_skill_dir):
        from features.health import health_tracker as ht
        names = ht._tracked_names()
        assert "Amyra" in names
        assert "Reyansh" in names

    def test_empty_config_returns_message(self, tmp_skill_dir):
        from features.health import health_tracker as ht
        with patch.object(ht, "_load_cfg", return_value={"children": {}}):
            names = ht._tracked_names()
            assert names == "no children configured"
