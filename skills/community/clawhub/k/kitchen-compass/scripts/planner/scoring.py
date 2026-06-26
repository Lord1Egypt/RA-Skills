from __future__ import annotations

from typing import Any

from inventory import recipe_inventory_support

from planner.common import primary_structural_role, protein_family
from planner.presets import EFFORT_ORDER, FRICTION_ORDER, RECENT_WINDOW_DAYS, SOON_REPEAT_DAYS


def score_recipe(
    recipe: dict[str, Any],
    selected: list[dict[str, Any]],
    preset: dict[str, Any],
    history: dict[str, Any] | None = None,
    inventory_state: dict[str, Any] | None = None,
    prioritize_inventory: bool = False,
) -> tuple[int, list[str], dict[str, Any] | None]:
    weights = preset["weights"]
    score = weights["base"]
    reasons: list[str] = []
    penalties: list[str] = []

    def apply(delta: int, if_reason: str | None = None, if_penalty: str | None = None) -> None:
        nonlocal score
        score += delta
        if delta > 0 and if_reason:
            reasons.append(if_reason)
        elif delta < 0 and if_penalty:
            penalties.append(if_penalty)

    effort = recipe["cooking_effort"]
    friction = recipe["ingredient_friction"]
    cost = recipe["cost"]
    status = recipe["status"]
    serving = recipe["serving_profile"]
    flags = recipe["composition_flags"]
    contexts = set(recipe.get("context_occasion", []))

    apply(weights.get("easy", 0) if effort == "easy" else 0, "easy to cook")
    apply(weights.get("moderate", 0) if effort == "moderate" else 0, "moderate effort but still reasonable")
    apply(weights.get("involved", 0) if effort == "involved" else 0, if_penalty="involved cooking project")

    apply(weights.get("low_friction", 0) if friction == "low" else 0, "low ingredient friction")
    apply(weights.get("medium_friction", 0) if friction == "medium" else 0, "ingredient list is manageable")
    apply(weights.get("high_friction", 0) if friction == "high" else 0, if_penalty="high ingredient friction")

    apply(weights.get("cheap", 0) if cost == "cheap" else 0, "cheap dinner")
    apply(weights.get("medium_cost", 0) if cost == "medium" else 0, "normal medium-cost dinner")
    apply(weights.get("expensive", 0) if cost == "expensive" else 0, if_penalty="expensive for a routine week")

    apply(weights.get("trusted", 0) if status == "trusted" else 0, "trusted house recipe")
    apply(weights.get("testing", 0) if status == "testing" else 0, "testing recipe but still plausible")
    apply(weights.get("aspirational", 0) if status == "aspirational" else 0, if_penalty="aspirational / less proven")

    apply(weights.get("family_table", 0) if serving == "family-table" else 0, "good family-table fit")
    apply(weights.get("crowd_friendly", 0) if serving == "crowd-friendly" else 0, "scales well")
    apply(weights.get("small_table", 0) if serving == "small-table" else 0, if_penalty="smaller-scale dinner")

    apply(weights.get("self_contained", 0) if flags.get("mostly_self_contained") else 0, "self-contained dinner")
    apply(weights.get("wants_side", 0) if flags.get("wants_side_pairing") else 0, if_penalty="needs side support")
    apply(weights.get("needs_protein", 0) if flags.get("needs_protein_pairing") else 0, if_penalty="needs protein pairing to feel complete")

    apply(weights.get("sale_trigger", 0) if "sale-trigger" in contexts else 0, "nice sale-trigger option")
    apply(weights.get("hosting", 0) if "hosting" in contexts else 0, "hosting-friendly")
    apply(weights.get("comfort_food", 0) if "comfort-food" in contexts else 0, "comfort-food lane")

    protein = protein_family(recipe)
    selected_proteins = [protein_family(item) for item in selected]
    repeats = selected_proteins.count(protein)
    if repeats >= 1:
        apply(weights.get("repeat_protein_penalty", 0), if_penalty=f"repeats {protein}")
        if repeats >= 2:
            apply(weights.get("repeat_protein_after_first", 0), if_penalty=f"would make {protein} dominate the week")

    side_dependent_count = sum(1 for item in selected if item["composition_flags"].get("wants_side_pairing"))
    if flags.get("wants_side_pairing") and side_dependent_count >= 1:
        apply(weights.get("second_side_dependent_penalty", 0), if_penalty="would stack another side-dependent dinner")
    if flags.get("wants_side_pairing") and side_dependent_count >= 2:
        apply(weights.get("third_side_dependent_penalty", 0), if_penalty="too many dinners needing side support")

    medium_friction_count = sum(1 for item in selected if FRICTION_ORDER[item["ingredient_friction"]] >= FRICTION_ORDER["medium"])
    if FRICTION_ORDER[friction] >= FRICTION_ORDER["medium"] and medium_friction_count >= 1:
        apply(weights.get("second_medium_friction_penalty", 0), if_penalty="would make the week more shop-annoying")

    moderate_plus_count = sum(1 for item in selected if EFFORT_ORDER[item["cooking_effort"]] >= EFFORT_ORDER["moderate"])
    if EFFORT_ORDER[effort] >= EFFORT_ORDER["moderate"] and moderate_plus_count >= 1:
        apply(weights.get("second_moderate_penalty", 0), if_penalty="would stack another non-easy dinner")

    testing_count = sum(1 for item in selected if item["status"] == "testing")
    if status == "testing" and testing_count >= 1:
        apply(weights.get("second_testing_penalty", 0), if_penalty="already have a testing meal in the week")

    if history and history.get("has_history"):
        last_seen = history["last_recipe_dates"].get(recipe["slug"])
        if last_seen:
            gap_days = (history["anchor_date"] - last_seen).days
            if gap_days <= SOON_REPEAT_DAYS:
                apply(weights.get("history_exact_repeat_soon", 0), if_penalty=f"made or planned too recently ({gap_days}d ago)")
            elif gap_days <= RECENT_WINDOW_DAYS:
                apply(weights.get("history_exact_repeat_recent", 0), if_penalty=f"still fairly recent ({gap_days}d ago)")
        else:
            apply(weights.get("history_long_gap_bonus", 0), if_reason="has not shown up recently")

        protein_count = history["recent_protein_counts"].get(protein, 0)
        if protein_count >= 2.2:
            apply(weights.get("history_recent_protein_dominant", 0), if_penalty=f"recent history already leans {protein}")
        elif protein_count >= 0.7:
            apply(weights.get("history_recent_protein_present", 0), if_penalty=f"recent history already includes {protein}")

        role = primary_structural_role(recipe)
        role_count = history["recent_role_counts"].get(role, 0)
        if role_count >= 2.2:
            apply(weights.get("history_recent_role_dominant", 0), if_penalty=f"recent history already leans {role}")
        elif role_count >= 0.7:
            apply(weights.get("history_recent_role_present", 0), if_penalty=f"recent history already includes {role}")

    inventory_support = None
    if inventory_state:
        inventory_support = recipe_inventory_support(recipe, inventory_state, prioritize_inventory=prioritize_inventory)
        if inventory_support["total_bonus"] > 0:
            apply(
                inventory_support["total_bonus"],
                if_reason=inventory_support["matches"][0]["explanation"],
            )

    return score, reasons + penalties, inventory_support


def can_add(recipe: dict[str, Any], selected: list[dict[str, Any]], preset: dict[str, Any], target: int) -> bool:
    mix = preset.get("target_mix", {})
    simulated = selected + [recipe]

    involved_count = sum(1 for item in simulated if item["cooking_effort"] == "involved")
    moderate_plus_count = sum(1 for item in simulated if EFFORT_ORDER[item["cooking_effort"]] >= EFFORT_ORDER["moderate"])
    if involved_count > mix.get("effort_max_counts", {}).get("involved", target):
        return False
    if moderate_plus_count > mix.get("effort_max_counts", {}).get("moderate_plus", target):
        return False

    high_friction_count = sum(1 for item in simulated if item["ingredient_friction"] == "high")
    medium_plus_friction_count = sum(1 for item in simulated if FRICTION_ORDER[item["ingredient_friction"]] >= FRICTION_ORDER["medium"])
    if high_friction_count > mix.get("friction_max_counts", {}).get("high", target):
        return False
    if medium_plus_friction_count > mix.get("friction_max_counts", {}).get("medium_plus", target):
        return False

    expensive_count = sum(1 for item in simulated if item["cost"] == "expensive")
    if expensive_count > mix.get("cost_max_counts", {}).get("expensive", target):
        return False

    aspirational_count = sum(1 for item in simulated if item["status"] == "aspirational")
    testing_count = sum(1 for item in simulated if item["status"] == "testing")
    wants_side_count = sum(1 for item in simulated if item["composition_flags"].get("wants_side_pairing"))

    if aspirational_count > mix.get("aspirational_max", target):
        return False
    if testing_count > mix.get("testing_max", target):
        return False
    if wants_side_count > mix.get("wants_side_max", target):
        return False
    return True
