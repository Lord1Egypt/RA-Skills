"""
test_get_kids_meals.py — the "what are the kids eating <day>" tool.

Regression coverage for the bug this tool exists to prevent: the agent
free-handing which weekday key of weekly_meal_plan.json applies to a given
date and blending entries from the wrong days. get_kids_meals must resolve
the date to a weekday key in code and hand the model an already-correct
answer.
"""
from __future__ import annotations

import sys
import types
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))


with patch("core.config_loader._load_config") as _mc:
    from conftest import MINIMAL_CONFIG
    from core.config_loader import Config
    _mc.return_value = Config(MINIMAL_CONFIG)
    import tools  # noqa: E402


class TestGetKidsMeals:
    def test_returns_formatted_meals_for_requested_date(self):
        plan_for_day = {
            "ana":   {"breakfast": "Scrambled eggs", "lunch": "Cheese sandwich", "side": "Fruit"},
            "ben": {"breakfast": "Soft scrambled eggs", "lunch": "Khichdi (rice)", "side": "Strawberries (chopped)"},
        }
        with patch("features.meals.weekly_meal_planner.get_meals_for_date",
                   return_value=plan_for_day) as mocked:
            out = tools.get_kids_meals("2026-07-20")

        assert "Monday, July 20" in out
        assert "Scrambled eggs" in out
        assert "Khichdi (rice)" in out
        # Must not leak a different day's items
        assert "Oats" not in out
        assert "Dalia" not in out
        mocked.assert_called_once_with("2026-07-20")

    def test_defaults_to_today_when_date_omitted(self):
        with patch("features.meals.weekly_meal_planner.get_meals_for_date",
                   return_value=None) as mocked:
            tools.get_kids_meals()
        # Called with *some* YYYY-MM-DD string derived from datetime.now()
        called_date = mocked.call_args[0][0]
        assert len(called_date) == 10 and called_date.count("-") == 2

    def test_no_locked_plan_returns_friendly_message_not_a_guess(self):
        with patch("features.meals.weekly_meal_planner.get_meals_for_date",
                   return_value=None):
            out = tools.get_kids_meals("2026-07-20")
        assert "No locked meal plan" in out

    def test_invalid_date_string_returns_error(self):
        out = tools.get_kids_meals("Friday")
        assert out.startswith("❌")
        assert "YYYY-MM-DD" in out

    def test_dispatch_wires_the_tool(self):
        """The tool must be reachable via execute_tool, or the agent can't call it."""
        with patch("features.meals.weekly_meal_planner.get_meals_for_date",
                   return_value=None):
            out = tools.execute_tool("get_kids_meals", {"date": "2026-07-20"})
        assert "No locked meal plan" in out
