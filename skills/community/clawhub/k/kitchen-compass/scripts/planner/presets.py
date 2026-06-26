from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from paths import KitchenCompassPaths

EFFORT_ORDER = {"easy": 0, "moderate": 1, "involved": 2}
FRICTION_ORDER = {"low": 0, "medium": 1, "high": 2}
PROTEIN_SPLIT_CHARS = [",", "/"]
SOON_REPEAT_DAYS = 14
RECENT_WINDOW_DAYS = 28

PRESETS: dict[str, dict[str, Any]] = {
    "balanced": {
        "label": "Balanced week",
        "description": "Default practical week: mostly trusted, low-friction dinners with one slot for something slightly more interesting.",
        "target_mix": {
            "effort_max_counts": {"involved": 0, "moderate_plus": 1},
            "friction_max_counts": {"high": 0, "medium_plus": 2},
            "cost_max_counts": {"expensive": 0},
            "aspirational_max": 0,
            "testing_max": 1,
            "wants_side_max": 2,
        },
        "weights": {
            "base": 40,
            "easy": 8, "moderate": 2, "involved": -18,
            "low_friction": 9, "medium_friction": 2, "high_friction": -18,
            "cheap": 8, "medium_cost": 3, "expensive": -20,
            "trusted": 7, "testing": 1, "aspirational": -20,
            "family_table": 4, "crowd_friendly": 2, "small_table": -1,
            "self_contained": 7, "wants_side": -2, "needs_protein": -4,
            "sale_trigger": 1, "hosting": 0, "comfort_food": 1,
            "repeat_protein_penalty": -12, "repeat_protein_after_first": -8,
            "second_side_dependent_penalty": -4, "third_side_dependent_penalty": -8,
            "second_medium_friction_penalty": -4, "second_moderate_penalty": -4,
            "second_testing_penalty": -6,
            "history_exact_repeat_soon": -18, "history_exact_repeat_recent": -10,
            "history_recent_protein_dominant": -10, "history_recent_protein_present": -4,
            "history_recent_role_dominant": -6, "history_recent_role_present": -2,
            "history_long_gap_bonus": 5,
        },
    },
    "easy": {
        "label": "Easy week",
        "description": "Bias hard toward low-effort, low-friction, proven weeknight dinners.",
        "target_mix": {
            "effort_max_counts": {"involved": 0, "moderate_plus": 0},
            "friction_max_counts": {"high": 0, "medium_plus": 1},
            "cost_max_counts": {"expensive": 0},
            "aspirational_max": 0,
            "testing_max": 1,
            "wants_side_max": 2,
        },
        "weights": {
            "base": 40,
            "easy": 12, "moderate": -8, "involved": -30,
            "low_friction": 14, "medium_friction": -6, "high_friction": -30,
            "cheap": 9, "medium_cost": 2, "expensive": -20,
            "trusted": 8, "testing": 0, "aspirational": -25,
            "family_table": 4, "crowd_friendly": 1, "small_table": -1,
            "self_contained": 8, "wants_side": -3, "needs_protein": -5,
            "sale_trigger": 1, "hosting": -2, "comfort_food": 1,
            "repeat_protein_penalty": -12, "repeat_protein_after_first": -8,
            "second_side_dependent_penalty": -5, "third_side_dependent_penalty": -10,
            "second_medium_friction_penalty": -8, "second_moderate_penalty": -10,
            "second_testing_penalty": -8,
            "history_exact_repeat_soon": -20, "history_exact_repeat_recent": -12,
            "history_recent_protein_dominant": -10, "history_recent_protein_present": -4,
            "history_recent_role_dominant": -6, "history_recent_role_present": -2,
            "history_long_gap_bonus": 4,
        },
    },
    "cheap": {
        "label": "Cheap week",
        "description": "Prioritize cheap dinners and keep friction low enough that the savings still feel real.",
        "target_mix": {
            "effort_max_counts": {"involved": 0, "moderate_plus": 1},
            "friction_max_counts": {"high": 0, "medium_plus": 2},
            "cost_max_counts": {"expensive": 0},
            "aspirational_max": 0,
            "testing_max": 1,
            "wants_side_max": 2,
        },
        "weights": {
            "base": 40,
            "easy": 8, "moderate": 1, "involved": -18,
            "low_friction": 10, "medium_friction": 1, "high_friction": -20,
            "cheap": 16, "medium_cost": 0, "expensive": -30,
            "trusted": 6, "testing": 0, "aspirational": -20,
            "family_table": 4, "crowd_friendly": 1, "small_table": -1,
            "self_contained": 5, "wants_side": -2, "needs_protein": -6,
            "sale_trigger": 3, "hosting": -2, "comfort_food": 1,
            "repeat_protein_penalty": -10, "repeat_protein_after_first": -7,
            "second_side_dependent_penalty": -3, "third_side_dependent_penalty": -6,
            "second_medium_friction_penalty": -5, "second_moderate_penalty": -4,
            "second_testing_penalty": -6,
            "history_exact_repeat_soon": -18, "history_exact_repeat_recent": -10,
            "history_recent_protein_dominant": -8, "history_recent_protein_present": -3,
            "history_recent_role_dominant": -5, "history_recent_role_present": -2,
            "history_long_gap_bonus": 4,
        },
    },
    "low-carb": {
        "label": "Low-carb week",
        "description": "Stay inside the low-carb lane while still balancing variety and avoiding an annoying week.",
        "require_diet_mode": "low-carb",
        "target_mix": {
            "effort_max_counts": {"involved": 0, "moderate_plus": 1},
            "friction_max_counts": {"high": 0, "medium_plus": 2},
            "cost_max_counts": {"expensive": 0},
            "aspirational_max": 1,
            "testing_max": 1,
            "wants_side_max": 2,
        },
        "weights": {
            "base": 40,
            "easy": 8, "moderate": 2, "involved": -18,
            "low_friction": 8, "medium_friction": 1, "high_friction": -18,
            "cheap": 8, "medium_cost": 3, "expensive": -20,
            "trusted": 6, "testing": 1, "aspirational": -10,
            "family_table": 3, "crowd_friendly": 1, "small_table": -1,
            "self_contained": 7, "wants_side": -1, "needs_protein": -8,
            "sale_trigger": 1, "hosting": -1, "comfort_food": 1,
            "repeat_protein_penalty": -12, "repeat_protein_after_first": -8,
            "second_side_dependent_penalty": -2, "third_side_dependent_penalty": -4,
            "second_medium_friction_penalty": -4, "second_moderate_penalty": -4,
            "second_testing_penalty": -5,
            "history_exact_repeat_soon": -20, "history_exact_repeat_recent": -12,
            "history_recent_protein_dominant": -10, "history_recent_protein_present": -4,
            "history_recent_role_dominant": -4, "history_recent_role_present": -1,
            "history_long_gap_bonus": 4,
        },
    },
    "hosting-friendly": {
        "label": "Hosting-friendly week",
        "description": "Allow one bigger or more special dinner, but still avoid stacking multiple high-friction projects.",
        "target_mix": {
            "effort_max_counts": {"involved": 1, "moderate_plus": 2},
            "friction_max_counts": {"high": 1, "medium_plus": 2},
            "cost_max_counts": {"expensive": 1},
            "aspirational_max": 1,
            "testing_max": 2,
            "wants_side_max": 3,
        },
        "weights": {
            "base": 40,
            "easy": 4, "moderate": 4, "involved": -6,
            "low_friction": 5, "medium_friction": 3, "high_friction": -8,
            "cheap": 3, "medium_cost": 4, "expensive": -8,
            "trusted": 5, "testing": 2, "aspirational": -4,
            "family_table": 4, "crowd_friendly": 7, "small_table": -3,
            "self_contained": 4, "wants_side": -1, "needs_protein": -6,
            "sale_trigger": 1, "hosting": 8, "comfort_food": 2,
            "repeat_protein_penalty": -10, "repeat_protein_after_first": -6,
            "second_side_dependent_penalty": -2, "third_side_dependent_penalty": -4,
            "second_medium_friction_penalty": -3, "second_moderate_penalty": -2,
            "second_testing_penalty": -3,
            "history_exact_repeat_soon": -14, "history_exact_repeat_recent": -8,
            "history_recent_protein_dominant": -8, "history_recent_protein_present": -3,
            "history_recent_role_dominant": -4, "history_recent_role_present": -1,
            "history_long_gap_bonus": 5,
        },
    },
}


def load_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def load_household_preferences(paths: KitchenCompassPaths) -> dict[str, Any]:
    return load_json_if_exists(paths.household_dir / "preferences.json")


def planner_defaults(paths: KitchenCompassPaths) -> tuple[str, int, bool]:
    planning = load_household_preferences(paths).get("planning", {})
    preset = planning.get("default_preset", "balanced")
    dinners_per_week = planning.get("default_dinners_per_week", 3)
    prioritize_inventory = planning.get("prioritize_inventory")
    legacy_prioritize_inventory = planning.get("prioritize_freezer_inventory")
    if preset not in PRESETS:
        preset = "balanced"
    if not isinstance(dinners_per_week, int) or dinners_per_week < 1:
        dinners_per_week = 3
    if not isinstance(prioritize_inventory, bool):
        prioritize_inventory = legacy_prioritize_inventory if isinstance(legacy_prioritize_inventory, bool) else False
    return preset, dinners_per_week, prioritize_inventory
