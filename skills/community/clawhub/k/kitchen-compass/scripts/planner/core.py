from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from planner.common import primary_structural_role, protein_family
from planner.history import build_history_context, history_summary_for_output, load_history_events
from planner.presets import PRESETS
from planner.scoring import can_add, score_recipe


def load_catalog(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing catalog: {path}. Run build_recipe_query_index.py first.")
    return json.loads(path.read_text())


def side_recipe_map(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {r["slug"]: r for r in payload["recipes"] if "side" in r["meal_type"]}


def dinner_candidates(payload: dict[str, Any], preset: dict[str, Any], include_aspirational: bool) -> list[dict[str, Any]]:
    dinners = [r for r in payload["recipes"] if "dinner" in r["meal_type"]]
    if preset.get("require_diet_mode"):
        dinners = [r for r in dinners if preset["require_diet_mode"] in r.get("diet_modes", [])]
    if not include_aspirational:
        dinners = [r for r in dinners if r.get("status") != "aspirational"]
    return dinners


def choose_side(recipe: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any] | None:
    intel = payload.get("pairing_intelligence", {}).get(recipe["slug"], {})
    side_matches = intel.get("recipe_side_matches", [])
    sides = side_recipe_map(payload)
    for match in side_matches:
        side = sides.get(match["slug"])
        if side:
            return {
                "slug": side["slug"],
                "title": side["title"],
                "path": side["path"],
                "reason": "; ".join(match.get("reasons", [])[:2]) or "pairing metadata overlap",
            }
    return None


def choose_protein_add_on(recipe: dict[str, Any], payload: dict[str, Any]) -> str | None:
    intel = payload.get("pairing_intelligence", {}).get(recipe["slug"], {})
    proteins = intel.get("protein_pairings", [])
    return proteins[0]["label"] if proteins else None


def explain_recipe(
    recipe: dict[str, Any],
    payload: dict[str, Any],
    score: int,
    reasons: list[str],
    history: dict[str, Any] | None = None,
    inventory_support: dict[str, Any] | None = None,
) -> dict[str, Any]:
    flags = recipe["composition_flags"]
    side = choose_side(recipe, payload) if flags.get("wants_side_pairing") else None
    protein_add_on = choose_protein_add_on(recipe, payload) if flags.get("needs_protein_pairing") else None

    if flags.get("needs_protein_pairing"):
        composition = {
            "kind": "needs-protein-pairing",
            "note": f"This is a base dinner, so pair it with {protein_add_on or 'a simple protein'} to make it feel complete.",
            "protein_add_on": protein_add_on,
            "side": side,
        }
    elif flags.get("mostly_self_contained"):
        composition = {
            "kind": "self-contained",
            "note": "This reads as a self-contained dinner this week; no extra side is required.",
            "protein_add_on": None,
            "side": None,
        }
    elif flags.get("wants_side_pairing"):
        composition = {
            "kind": "wants-side",
            "note": f"Treat this as a main that wants a side{(': ' + side['title']) if side else ''}.",
            "protein_add_on": None,
            "side": side,
        }
    else:
        composition = {
            "kind": "flexible",
            "note": "This can stand as dinner without mandatory extras, but a side would be optional.",
            "protein_add_on": None,
            "side": None,
        }

    last_seen = None
    if history and history.get("has_history"):
        raw = history["last_recipe_dates"].get(recipe["slug"])
        last_seen = raw.isoformat() if raw else None

    return {
        "slug": recipe["slug"],
        "title": recipe["title"],
        "path": recipe["path"],
        "score": score,
        "protein_family": protein_family(recipe),
        "primary_structural_role": primary_structural_role(recipe),
        "effort": recipe["cooking_effort"],
        "ingredient_friction": recipe["ingredient_friction"],
        "cost": recipe["cost"],
        "status": recipe["status"],
        "serving_profile": recipe["serving_profile"],
        "context": recipe.get("context_occasion", []),
        "last_seen": last_seen,
        "reasons": reasons[:8],
        "composition": composition,
        "inventory_support": inventory_support or {"total_bonus": 0, "matches": []},
    }


def summarize_plan(picks: list[dict[str, Any]]) -> dict[str, Any]:
    proteins = Counter(pick["protein_family"] for pick in picks)
    roles = Counter(pick["primary_structural_role"] for pick in picks)
    inventory_supported = [pick for pick in picks if pick.get("inventory_support", {}).get("total_bonus", 0) > 0]
    return {
        "protein_variety": dict(sorted(proteins.items())),
        "role_mix": dict(sorted(roles.items())),
        "effort_mix": dict(sorted(Counter(pick["effort"] for pick in picks).items())),
        "friction_mix": dict(sorted(Counter(pick["ingredient_friction"] for pick in picks).items())),
        "cost_mix": dict(sorted(Counter(pick["cost"] for pick in picks).items())),
        "status_mix": dict(sorted(Counter(pick["status"] for pick in picks).items())),
        "self_contained_count": sum(1 for pick in picks if pick["composition"]["kind"] == "self-contained"),
        "needs_side_count": sum(1 for pick in picks if pick["composition"]["kind"] == "wants-side"),
        "needs_protein_pairing_count": sum(1 for pick in picks if pick["composition"]["kind"] == "needs-protein-pairing"),
        "inventory_supported_count": len(inventory_supported),
        "inventory_bonus_total": sum(pick.get("inventory_support", {}).get("total_bonus", 0) for pick in inventory_supported),
    }


def build_plan(
    payload: dict[str, Any],
    preset_name: str,
    dinners_per_week: int,
    include_aspirational: bool = False,
    history_path: Path | None = None,
    ignore_history: bool = False,
    inventory_state: dict[str, Any] | None = None,
    prioritize_inventory: bool = False,
) -> dict[str, Any]:
    preset = PRESETS[preset_name]
    candidates = dinner_candidates(payload, preset, include_aspirational=include_aspirational)
    recipes_by_slug = {recipe["slug"]: recipe for recipe in payload["recipes"]}
    history = None
    if not ignore_history and history_path is not None:
        history = build_history_context(load_history_events(history_path), recipes_by_slug)

    selected: list[dict[str, Any]] = []
    picks: list[dict[str, Any]] = []

    while len(selected) < dinners_per_week:
        ranked: list[tuple[int, str, dict[str, Any], list[str], dict[str, Any] | None]] = []
        for recipe in candidates:
            if recipe in selected:
                continue
            if not can_add(recipe, selected, preset, dinners_per_week):
                continue
            score, reasons, inventory_support = score_recipe(
                recipe,
                selected,
                preset,
                history=history,
                inventory_state=inventory_state,
                prioritize_inventory=prioritize_inventory,
            )
            ranked.append((score, recipe["title"], recipe, reasons, inventory_support))

        if not ranked:
            break

        ranked.sort(key=lambda item: (-item[0], item[1]))
        score, _, recipe, reasons, inventory_support = ranked[0]
        selected.append(recipe)
        picks.append(explain_recipe(recipe, payload, score, reasons, history=history, inventory_support=inventory_support))

    return {
        "preset": preset_name,
        "preset_label": preset["label"],
        "description": preset["description"],
        "dinners_per_week": dinners_per_week,
        "picked_count": len(picks),
        "history_summary": history_summary_for_output(history) if history else None,
        "inventory_summary": {
            "mode": "prioritized" if prioritize_inventory else "light",
            "prioritize_inventory": prioritize_inventory,
            "active_item_count": len(inventory_state.get("items", [])) if inventory_state else 0,
            "available_item_count": len([item for item in inventory_state.get("items", []) if float(item.get("quantity", {}).get("amount", 0) or 0) > 0]) if inventory_state else 0,
            "supported_pick_count": sum(1 for pick in picks if pick.get("inventory_support", {}).get("total_bonus", 0) > 0),
        },
        "summary": summarize_plan(picks),
        "picks": picks,
    }
