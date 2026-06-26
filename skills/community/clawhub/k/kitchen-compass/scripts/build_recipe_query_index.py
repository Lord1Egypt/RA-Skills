#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from contract import (
    ACTIVE_ENGINE_MEAL_TYPES,
    COMPOSITION_NORMALIZATION_ALIASES,
    LIST_FIELDS,
    PAIR_WITH_KIND_ALIASES,
    extract_block,
    parse_planning_notes_block,
    parse_snapshot_block,
    slugify,
    snapshot_fields_with_defaults,
    split_list,
)
from paths import KitchenCompassPaths, resolve_data_root, write_atomic
from validation import validate_recipe_paths

PROTEIN_KEYWORDS = {
    "chicken", "sausage", "beef", "pork", "steak", "shrimp", "fish", "salmon", "cod",
    "meatballs", "tenderloin", "chops", "ribeye", "turkey",
}
SIDE_KEYWORDS = {
    "rice", "pilaf", "potato", "potatoes", "salad", "vegetable", "vegetables", "bread", "fries",
    "cauliflower", "panzanella", "grilled cheese", "soup", "croutons", "buns", "chips", "pita",
    "mezze", "side", "applesauce",
}
SUPPORT_KEYWORDS = {"sauce", "tzatziki", "bbq", "lime-tahini", "bang bang", "provolone", "pepperoncini"}
MATCH_STOPWORDS = {"simple", "other", "classic", "favorite", "house", "warm-weather", "summer", "dinner", "dinners", "mains", "main", "food", "spread", "spreads"}
PAIR_WITH_PREFIX_PATTERN = "|".join(sorted((re.escape(prefix) for prefix in PAIR_WITH_KIND_ALIASES), key=len, reverse=True))


def parse_snapshot(text: str) -> dict[str, Any]:
    if "## Snapshot" not in text or "## Ingredients" not in text:
        raise ValueError("Recipe missing Snapshot/Ingredients boundary")
    raw_fields, _ = parse_snapshot_block(extract_block(text, "## Snapshot", "## Ingredients"))
    return snapshot_fields_with_defaults(raw_fields)


def parse_planning_notes(text: str) -> dict[str, str]:
    notes, _ = parse_planning_notes_block(extract_block(text, "## Planning Notes", "## Notes"))
    return {slugify(label): value for label, value in notes.items()}


def normalize_text(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def meaningful_tokens(text: str) -> set[str]:
    return {
        token for token in normalize_text(text).split()
        if len(token) > 2 and token not in MATCH_STOPWORDS
    }


def pair_kind(label: str) -> str:
    text = label.lower()
    if any(keyword in text for keyword in PROTEIN_KEYWORDS):
        return "protein"
    if any(keyword in text for keyword in SUPPORT_KEYWORDS):
        return "support"
    if any(keyword in text for keyword in SIDE_KEYWORDS):
        return "side"
    return "general"


def parse_pair_with_entry(entry: str) -> dict[str, str]:
    match = re.match(rf"^({PAIR_WITH_PREFIX_PATTERN})\s*:\s*(.+)$", entry, re.IGNORECASE)
    if match:
        return {
            "label": match.group(2).strip(),
            "kind": PAIR_WITH_KIND_ALIASES[match.group(1).lower()],
            "source": "explicit",
        }
    return {
        "label": entry,
        "kind": pair_kind(entry),
        "source": "heuristic",
    }


def parse_composition_mode(notes: dict[str, str]) -> str | None:
    raw = notes.get("composition", "")
    for part in split_list(raw):
        normalized = COMPOSITION_NORMALIZATION_ALIASES.get(slugify(part))
        if normalized:
            return normalized
    return None


def derive_heuristic_composition(recipe: dict[str, Any]) -> tuple[str, dict[str, bool]]:
    roles = set(recipe.get("structural_role", []))
    notes = recipe.get("planning_notes", {})
    pairing_notes = notes.get("pairing-notes", "").lower()
    typed_pairs = recipe.get("pair_with_typed", [])

    needs_protein = "base" in roles or "no meaningful protein" in pairing_notes
    wants_side = (
        "filler-meal" in roles
        or "needs a side" in pairing_notes
        or "paired with sides" in pairing_notes
        or "paired with a side" in pairing_notes
        or "paired with sides unless" in pairing_notes
        or "especially strong with" in pairing_notes
        or any(item["kind"] == "side" for item in typed_pairs)
    )
    self_contained = (
        "works as a full dinner" in pairing_notes
        or "full dinner on its own" in pairing_notes
        or "does not need extra sides" in pairing_notes
        or "can function as a complete" in pairing_notes
        or "can stand alone" in pairing_notes
        or "already works as a full dinner" in pairing_notes
        or "already lands as a full meal" in pairing_notes
        or "works as a standalone meal" in pairing_notes
    )

    if needs_protein:
        self_contained = False
    if self_contained and "needs a side" not in pairing_notes:
        wants_side = False

    if needs_protein:
        mode = "needs-protein-pairing"
    elif self_contained:
        mode = "self-contained"
    elif wants_side:
        mode = "wants-side"
    else:
        mode = "flexible"

    return mode, {
        "needs_protein_pairing": needs_protein,
        "wants_side_pairing": wants_side,
        "mostly_self_contained": self_contained,
    }


def build_composition_flags(recipe: dict[str, Any]) -> dict[str, Any]:
    explicit_mode = parse_composition_mode(recipe.get("planning_notes", {}))
    typed_pairs = recipe.get("pair_with_typed", [])
    has_side_pairings = any(item["kind"] == "side" for item in typed_pairs)

    if explicit_mode == "self-contained":
        return {
            "mode": "self-contained",
            "source": "explicit",
            "needs_protein_pairing": False,
            "wants_side_pairing": False,
            "mostly_self_contained": True,
        }

    if explicit_mode == "wants-side":
        return {
            "mode": "wants-side",
            "source": "explicit",
            "needs_protein_pairing": False,
            "wants_side_pairing": True,
            "mostly_self_contained": False,
        }

    if explicit_mode == "needs-protein-pairing":
        return {
            "mode": "needs-protein-pairing",
            "source": "explicit",
            "needs_protein_pairing": True,
            "wants_side_pairing": has_side_pairings,
            "mostly_self_contained": False,
        }

    if explicit_mode == "flexible":
        return {
            "mode": "flexible",
            "source": "explicit",
            "needs_protein_pairing": False,
            "wants_side_pairing": False,
            "mostly_self_contained": False,
        }

    mode, flags = derive_heuristic_composition(recipe)
    return {
        "mode": mode,
        "source": "heuristic",
        **flags,
    }


def parse_ingredients_blob(text: str) -> str:
    return normalize_text(extract_block(text, "## Ingredients", "## Instructions"))


def build_search_blob(recipe: dict[str, Any]) -> str:
    values: list[str] = [recipe["title"], recipe["slug"], recipe.get("core_protein", ""), recipe.get("ingredients_blob", "")]
    for key in LIST_FIELDS:
        values.extend(recipe.get(key, []))
    values.extend(item["label"] for item in recipe.get("pair_with_typed", []))
    values.extend(recipe.get("planning_notes", {}).values())
    return " ".join(values).lower()


def build_pairing_blob(recipe: dict[str, Any]) -> str:
    values: list[str] = [recipe["title"], recipe["slug"], recipe.get("core_protein", "")]
    for key in ["meal_type", "structural_role", "diet_modes", "context_occasion", "tags"]:
        values.extend(recipe.get(key, []))
    values.extend(item["label"] for item in recipe.get("pair_with_typed", []))
    values.extend(recipe.get("planning_notes", {}).values())
    return " ".join(values).lower()


def load_recipe(path: Path, paths: KitchenCompassPaths) -> dict[str, Any]:
    text = path.read_text()
    title = text.splitlines()[0].lstrip("# ").strip()
    snapshot = parse_snapshot(text)
    recipe = {
        "slug": path.stem,
        "title": title,
        "path": str(path.relative_to(paths.data_root)),
        **snapshot,
        "planning_notes": parse_planning_notes(text),
        "ingredients_blob": parse_ingredients_blob(text),
    }
    recipe["pair_with_typed"] = [parse_pair_with_entry(label) for label in recipe.get("pair_with", [])]
    recipe["search_blob"] = build_search_blob(recipe)
    recipe["pairing_blob"] = build_pairing_blob(recipe)
    recipe["composition_flags"] = build_composition_flags(recipe)
    return recipe


def meal_scope(recipe: dict[str, Any]) -> bool:
    meal_types = set(recipe["meal_type"])
    return any(meal_type in meal_types for meal_type in ACTIVE_ENGINE_MEAL_TYPES)


def matches(recipe: dict[str, Any], **filters: str) -> bool:
    for key, expected in filters.items():
        value = recipe.get(key)
        if isinstance(value, list):
            if expected not in value:
                return False
        else:
            if value != expected:
                return False
    return True


def score_side_for_dinner(dinner: dict[str, Any], side: dict[str, Any]) -> tuple[int, list[str]]:
    if dinner["slug"] == side["slug"] or "side" not in side["meal_type"] or "dinner" not in dinner["meal_type"]:
        return -1, []

    score = 0
    reasons: list[str] = []
    dinner_pairs = {item["label"] for item in dinner["pair_with_typed"] if item["kind"] == "side"}
    side_pairs = {item["label"] for item in side["pair_with_typed"]}
    dinner_blob = dinner["pairing_blob"]
    side_blob = side["pairing_blob"]
    side_tokens = meaningful_tokens(side["title"])
    dinner_tokens = meaningful_tokens(dinner["title"])

    for label in dinner_pairs:
        label_tokens = meaningful_tokens(label)
        if normalize_text(label) == normalize_text(side["title"]):
            score += 12
            reasons.append(f"dinner explicitly asks for {label}")
        elif label_tokens and len(label_tokens & side_tokens) >= 2:
            score += 8
            reasons.append(f"dinner side note overlaps with {label}")

    for label in side_pairs:
        label_tokens = meaningful_tokens(label)
        if normalize_text(label) == normalize_text(dinner["title"]):
            score += 10
            reasons.append(f"side explicitly mentions {label}")
        elif label_tokens and len(label_tokens & dinner_tokens) >= 2:
            score += 6
            reasons.append(f"side dinner note overlaps with {label}")
        elif label_tokens and len(label_tokens & meaningful_tokens(dinner_blob)) >= 2:
            score += 4
            reasons.append(f"side metadata aligns with {label}")

    if side.get("core_protein") in {"potatoes", "rice", "bread"} and dinner["composition_flags"]["wants_side_pairing"]:
        score += 2
        reasons.append("hearty side fits a dinner that wants support")

    if side.get("core_protein") == "cauliflower" and "low-carb" in dinner.get("diet_modes", []):
        score += 4
        reasons.append("low-carb side matches low-carb dinner")

    if "comfort-food" in dinner.get("context_occasion", []) and side.get("core_protein") == "bread":
        score += 2
        reasons.append("comfort-food dinner likes a bready side")

    if any(token in dinner_blob for token in ["mediterranean", "kofta", "soutzoukakia", "mezze", "pilaf"]) and any(
        token in side_blob for token in ["mediterranean", "pilaf", "pita", "feta", "mezze", "salad"]
    ):
        score += 3
        reasons.append("Mediterranean serving style lines up")

    return score, reasons


def build_pairing_intelligence(recipes: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    intel: dict[str, dict[str, Any]] = {}
    dinners = [recipe for recipe in recipes if "dinner" in recipe["meal_type"]]
    sides = [recipe for recipe in recipes if "side" in recipe["meal_type"]]

    for recipe in recipes:
        generic_pairs = []
        for item in recipe["pair_with_typed"]:
            why = {
                "protein": "direct metadata pairing for completing the meal",
                "side": "direct metadata pairing for rounding out the plate",
                "support": "direct metadata pairing for serving/support",
                "general": "direct metadata pairing note",
            }[item["kind"]]
            generic_pairs.append({**item, "why": why})

        side_matches = []
        dinner_matches = []
        if "dinner" in recipe["meal_type"]:
            for side in sides:
                score, reasons = score_side_for_dinner(recipe, side)
                if score > 0:
                    side_matches.append({
                        "slug": side["slug"],
                        "title": side["title"],
                        "score": score,
                        "path": side["path"],
                        "reasons": reasons,
                    })
            side_matches.sort(key=lambda item: (-item["score"], item["title"]))

        if "side" in recipe["meal_type"]:
            for dinner in dinners:
                score, reasons = score_side_for_dinner(dinner, recipe)
                if score > 0:
                    dinner_matches.append({
                        "slug": dinner["slug"],
                        "title": dinner["title"],
                        "score": score,
                        "path": dinner["path"],
                        "reasons": reasons,
                    })
            dinner_matches.sort(key=lambda item: (-item["score"], item["title"]))

        intel[recipe["slug"]] = {
            "composition_flags": recipe["composition_flags"],
            "generic_pair_with": generic_pairs,
            "protein_pairings": [item for item in generic_pairs if item["kind"] == "protein"],
            "side_pairings": [item for item in generic_pairs if item["kind"] == "side"],
            "support_pairings": [item for item in generic_pairs if item["kind"] in {"support", "general"}],
            "recipe_side_matches": side_matches[:5],
            "recipe_dinner_matches": dinner_matches[:5],
        }
    return intel


def common_query_views(recipes: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    return {
        "weeknight_easy_low_friction_dinners": [
            recipe for recipe in recipes
            if matches(recipe, cooking_effort="easy")
            and matches(recipe, ingredient_friction="low")
            and "dinner" in recipe["meal_type"]
            and recipe["status"] in {"trusted", "testing"}
        ],
        "cheap_family_table_dinners": [
            recipe for recipe in recipes
            if matches(recipe, cost="cheap")
            and matches(recipe, serving_profile="family-table")
            and "dinner" in recipe["meal_type"]
        ],
        "filler_meals": [recipe for recipe in recipes if "filler-meal" in recipe["structural_role"]],
        "base_recipes_needing_pairing": [recipe for recipe in recipes if "base" in recipe["structural_role"]],
        "low_carb_dinners": [recipe for recipe in recipes if "dinner" in recipe["meal_type"] and "low-carb" in recipe["diet_modes"]],
        "crowd_friendly_sides": [
            recipe for recipe in recipes
            if "side" in recipe["meal_type"]
            and (
                recipe["serving_profile"] == "crowd-friendly"
                or "hosting" in recipe["context_occasion"]
                or "appetizer-party" in recipe["meal_type"]
            )
        ],
        "recipes_needing_protein_pairing": [recipe for recipe in recipes if recipe["composition_flags"]["needs_protein_pairing"]],
        "dinners_that_want_a_side": [recipe for recipe in recipes if "dinner" in recipe["meal_type"] and recipe["composition_flags"]["wants_side_pairing"]],
        "self_contained_dinners": [recipe for recipe in recipes if "dinner" in recipe["meal_type"] and recipe["composition_flags"]["mostly_self_contained"]],
    }


def summarize_catalog(recipes: list[dict[str, Any]]) -> dict[str, Any]:
    summary = {
        "total_recipes": len(recipes),
        "by_meal_type": Counter(),
        "by_status": Counter(),
        "by_core_protein": Counter(),
        "by_composition_mode": Counter(),
        "by_composition_source": Counter(),
    }
    for recipe in recipes:
        for meal_type in recipe["meal_type"]:
            summary["by_meal_type"][meal_type] += 1
        summary["by_status"][recipe["status"]] += 1
        summary["by_core_protein"][recipe["core_protein"]] += 1
        summary["by_composition_mode"][recipe["composition_flags"]["mode"]] += 1
        summary["by_composition_source"][recipe["composition_flags"]["source"]] += 1

    for key, value in list(summary.items()):
        if isinstance(value, Counter):
            summary[key] = dict(sorted(value.items()))
    return summary


def write_json(path: Path, payload: Any) -> None:
    write_atomic(path, json.dumps(payload, indent=2, sort_keys=False) + "\n")


def load_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def load_household_config(paths: KitchenCompassPaths) -> dict[str, Any]:
    return {
        "profile": load_json_if_exists(paths.household_dir / "profile.json"),
        "preferences": load_json_if_exists(paths.household_dir / "preferences.json"),
        "stores": load_json_if_exists(paths.household_dir / "stores.json"),
    }


def render_recipe_lines(recipes: list[dict[str, Any]]) -> list[str]:
    lines = []
    for recipe in recipes:
        lines.append(
            f"- **{recipe['title']}** — {recipe['cooking_effort']} effort, {recipe['ingredient_friction']} friction, {recipe['cost']} cost, {recipe['serving_profile']}, status: {recipe['status']} (`{recipe['path']}`)"
        )
    return lines or ["- None yet."]


def render_common_queries(views: dict[str, list[dict[str, Any]]]) -> str:
    labels = [
        ("weeknight_easy_low_friction_dinners", "Easy low-friction dinners"),
        ("cheap_family_table_dinners", "Cheap family-table dinners"),
        ("filler_meals", "Strong filler meals"),
        ("base_recipes_needing_pairing", "Base dinners that need protein pairing"),
        ("low_carb_dinners", "Low-carb dinners"),
        ("crowd_friendly_sides", "Crowd- and hosting-friendly sides"),
        ("recipes_needing_protein_pairing", "Recipes needing protein pairing"),
        ("dinners_that_want_a_side", "Dinners that naturally want a side"),
        ("self_contained_dinners", "Mostly self-contained dinners"),
    ]
    lines = ["# Kitchen Compass Query Layer — Common Planning Views", ""]
    for key, title in labels:
        lines.append(f"## {title}")
        lines.extend(render_recipe_lines(views.get(key, [])))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_sides_by_protein(recipes: list[dict[str, Any]]) -> str:
    sides = [recipe for recipe in recipes if "side" in recipe["meal_type"]]
    proteins = ["chicken", "pork", "beef", "shrimp", "fish"]
    lines = ["# Kitchen Compass Query Layer — Sides By Main-Protein Affinity", ""]
    for protein in proteins:
        lines.append(f"## {protein.title()}")
        matches_found = []
        for recipe in sides:
            labels = [item["label"] for item in recipe.get("pair_with_typed", []) if item["kind"] == "protein"]
            if any(protein in label.lower() for label in labels):
                matches_found.append((recipe, labels))
        if not matches_found:
            lines.append("- None tagged yet.")
        else:
            for recipe, labels in matches_found:
                lines.append(f"- **{recipe['title']}** — Pair With: {', '.join(labels)}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_pairings(recipes: list[dict[str, Any]], pairing_intel: dict[str, dict[str, Any]]) -> str:
    lines = ["# Kitchen Compass Query Layer — Pairing Intelligence", "", "## Dinners"]

    for recipe in [item for item in recipes if "dinner" in item["meal_type"]]:
        intel = pairing_intel[recipe["slug"]]
        flags = intel["composition_flags"]
        lines.append(f"### {recipe['title']}")
        lines.append(
            f"- Composition: mode = {flags['mode']} ({flags['source']}), needs protein = {flags['needs_protein_pairing']}, wants side = {flags['wants_side_pairing']}, mostly self-contained = {flags['mostly_self_contained']}"
        )
        if intel["protein_pairings"]:
            lines.append("- Protein add-ons from metadata:")
            for item in intel["protein_pairings"]:
                lines.append(f"  - {item['label']} — {item['why']}")
        if intel["side_pairings"]:
            lines.append("- Side ideas from metadata:")
            for item in intel["side_pairings"]:
                lines.append(f"  - {item['label']} — {item['why']}")
        if intel["recipe_side_matches"]:
            lines.append("- Matching side recipes:")
            for item in intel["recipe_side_matches"][:3]:
                reason = "; ".join(item["reasons"][:2]) if item["reasons"] else "metadata overlap"
                lines.append(f"  - {item['title']} (score {item['score']}) — {reason}")
        lines.append("")

    lines.append("## Sides")
    for recipe in [item for item in recipes if "side" in item["meal_type"]]:
        intel = pairing_intel[recipe["slug"]]
        lines.append(f"### {recipe['title']}")
        if intel["recipe_dinner_matches"]:
            for item in intel["recipe_dinner_matches"][:3]:
                reason = "; ".join(item["reasons"][:2]) if item["reasons"] else "metadata overlap"
                lines.append(f"- {item['title']} (score {item['score']}) — {reason}")
        else:
            lines.append("- No strong dinner matches yet.")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the portable Kitchen Compass dinner + side query catalog.")
    parser.add_argument("--data-root", help="Household data root. Defaults to ./kitchen-compass-data, except when run from the installed skill root it defaults to ../kitchen-compass-data so household data stays outside the skill.")
    parser.add_argument("--skip-validation", action="store_true", help="Skip the pre-build validation pass. Power-user escape hatch; normal usage should leave this off.")
    parser.add_argument("--verbose", action="store_true", help="Print the resolved data root to stderr.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = KitchenCompassPaths.from_root(resolve_data_root(args.data_root, verbose=args.verbose))
    if not paths.recipes_dir.exists():
        raise SystemExit(f"Missing recipes directory: {paths.recipes_dir}")

    recipe_paths = sorted(path for path in paths.recipes_dir.glob("*.md") if not path.name.startswith("_"))
    if not args.skip_validation:
        failures = validate_recipe_paths(recipe_paths)
        if failures:
            for recipe_path, errors in failures:
                print(f"- {recipe_path.relative_to(paths.data_root)}")
                for error in errors:
                    print(f"  - {error}")
            raise SystemExit(
                f"[ERROR] {len(failures)} recipe file(s) failed validation. "
                f"Run `python3 scripts/validate_recipes.py --data-root {paths.data_root}` "
                "and fix errors before rebuilding (or pass --skip-validation)."
            )

    recipes = [load_recipe(path, paths) for path in recipe_paths]
    recipes = [recipe for recipe in recipes if meal_scope(recipe)]
    pairing_intel = build_pairing_intelligence(recipes)
    common_views = common_query_views(recipes)

    payload = {
        "generated_at": None,
        "scope": "Dinner + side recipes only",
        "household_config": load_household_config(paths),
        "summary": summarize_catalog(recipes),
        "recipes": recipes,
        "pairing_intelligence": pairing_intel,
        "common_queries": {key: [item["slug"] for item in value] for key, value in common_views.items()},
    }

    paths.ensure_runtime_dirs()
    write_json(paths.generated_query_dir / "recipe-catalog.json", payload)
    write_json(paths.generated_query_dir / "common-queries.json", {key: value for key, value in common_views.items()})
    write_atomic(paths.query_planning_dir / "common-queries.md", render_common_queries(common_views))
    write_atomic(paths.query_planning_dir / "pairing-suggestions.md", render_pairings(recipes, pairing_intel))
    write_atomic(paths.query_planning_dir / "sides-by-main-protein.md", render_sides_by_protein(recipes))
    print(f"Built query index for {len(recipes)} dinner/side recipes.")
    print(f"Wrote: {paths.generated_query_dir / 'recipe-catalog.json'}")


if __name__ == "__main__":
    main()
