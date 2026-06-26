#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from contract import ACTIVE_ENGINE_MEAL_TYPES, ENUM_CHOICES
from paths import KitchenCompassPaths, resolve_data_root


def load_catalog(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing catalog: {path}. Run build_recipe_query_index.py first.")
    return json.loads(path.read_text())


def filter_recipes(recipes: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    filtered = []
    for recipe in recipes:
        if args.meal_type and args.meal_type not in recipe["meal_type"]:
            continue
        if args.cooking_effort and recipe["cooking_effort"] != args.cooking_effort:
            continue
        if args.ingredient_friction and recipe["ingredient_friction"] != args.ingredient_friction:
            continue
        if args.cost and recipe["cost"] != args.cost:
            continue
        if args.serving_profile and recipe["serving_profile"] != args.serving_profile:
            continue
        if args.status and recipe["status"] != args.status:
            continue
        if args.structural_role and args.structural_role not in recipe["structural_role"]:
            continue
        if args.diet_mode and args.diet_mode not in recipe["diet_modes"]:
            continue
        if args.context and args.context not in recipe["context_occasion"]:
            continue
        if args.core and args.core.lower() not in recipe["core_protein"].lower():
            continue
        if args.pairs_protein:
            protein = args.pairs_protein.lower()
            typed = recipe.get("pair_with_typed", [])
            if not any(item["kind"] == "protein" and protein in item["label"].lower() for item in typed):
                continue
        if args.needs_protein and not recipe["composition_flags"]["needs_protein_pairing"]:
            continue
        if args.wants_side and not recipe["composition_flags"]["wants_side_pairing"]:
            continue
        if args.self_contained and not recipe["composition_flags"]["mostly_self_contained"]:
            continue
        if args.text and args.text.lower() not in recipe["search_blob"]:
            continue
        filtered.append(recipe)
    return filtered


def sort_recipes(recipes: list[dict[str, Any]], sort_key: str) -> list[dict[str, Any]]:
    order_map = {
        "cooking_effort": {"easy": 0, "moderate": 1, "involved": 2},
        "ingredient_friction": {"low": 0, "medium": 1, "high": 2},
        "cost": {"cheap": 0, "medium": 1, "expensive": 2},
        "status": {"trusted": 0, "testing": 1, "aspirational": 2},
        "serving_profile": {"small-table": 0, "family-table": 1, "crowd-friendly": 2},
    }
    if sort_key in order_map:
        mapper = order_map[sort_key]
        return sorted(recipes, key=lambda recipe: (mapper.get(recipe[sort_key], 99), recipe["title"]))
    return sorted(recipes, key=lambda recipe: recipe.get(sort_key, recipe["title"]))


def render_recipe(recipe: dict[str, Any], verbose: bool) -> str:
    head = f"- {recipe['title']} [{recipe['slug']}]"
    meta = (
        f"  meal={','.join(recipe['meal_type'])} | effort={recipe['cooking_effort']} | friction={recipe['ingredient_friction']} | "
        f"cost={recipe['cost']} | serves={recipe['serving_profile']} | status={recipe['status']} | core={recipe['core_protein']}"
    )
    comp = (
        f"  composition: needs_protein={recipe['composition_flags']['needs_protein_pairing']} | "
        f"wants_side={recipe['composition_flags']['wants_side_pairing']} | self_contained={recipe['composition_flags']['mostly_self_contained']}"
    )
    if not verbose:
        return head + "\n" + meta + "\n" + comp
    details = [
        f"  role={','.join(recipe['structural_role']) or '-'} | diet={','.join(recipe['diet_modes']) or '-'} | context={','.join(recipe['context_occasion']) or '-'}",
        f"  pair_with={', '.join(recipe['pair_with']) if recipe['pair_with'] else '-'}",
        f"  path={recipe['path']}",
    ]
    return "\n".join([head, meta, comp, *details])


def resolve_recipe(recipes: list[dict[str, Any]], slug_or_title: str) -> dict[str, Any]:
    query = slug_or_title.lower()
    recipe = next((item for item in recipes if item["slug"] == query or item["title"].lower() == query), None)
    if not recipe:
        for item in recipes:
            if query in item["slug"] or query in item["title"].lower():
                recipe = item
                break
    if not recipe:
        raise SystemExit(f"No recipe found for pairing lookup: {slug_or_title}")
    return recipe


def show_pairs(payload: dict[str, Any], slug_or_title: str, limit: int) -> str:
    recipes = payload["recipes"]
    recipe = resolve_recipe(recipes, slug_or_title)
    intel = payload["pairing_intelligence"].get(recipe["slug"], {})
    flags = intel.get("composition_flags", {})

    lines = [f"Pairing intelligence for {recipe['title']} ({recipe['slug']}):"]
    if flags:
        lines.append(
            f"- composition: needs_protein={flags['needs_protein_pairing']}, wants_side={flags['wants_side_pairing']}, self_contained={flags['mostly_self_contained']}"
        )

    protein_pairs = intel.get("protein_pairings", [])[:limit]
    side_pairs = intel.get("side_pairings", [])[:limit]
    support_pairs = intel.get("support_pairings", [])[:limit]
    recipe_sides = intel.get("recipe_side_matches", [])[:limit]
    recipe_dinners = intel.get("recipe_dinner_matches", [])[:limit]

    if protein_pairs:
        lines.append("- protein add-ons from metadata:")
        for item in protein_pairs:
            lines.append(f"  - {item['label']} — {item['why']}")
    if side_pairs:
        lines.append("- side ideas from metadata:")
        for item in side_pairs:
            lines.append(f"  - {item['label']} — {item['why']}")
    if support_pairs:
        lines.append("- support pairings from metadata:")
        for item in support_pairs:
            lines.append(f"  - {item['label']} — {item['why']}")
    if recipe_sides:
        lines.append("- matching side recipes:")
        for item in recipe_sides:
            reason = "; ".join(item.get("reasons", [])[:2]) or "metadata overlap"
            lines.append(f"  - {item['title']} [{item['slug']}] score={item['score']} — {reason}")
    if recipe_dinners:
        lines.append("- matching dinner recipes:")
        for item in recipe_dinners:
            reason = "; ".join(item.get("reasons", [])[:2]) or "metadata overlap"
            lines.append(f"  - {item['title']} [{item['slug']}] score={item['score']} — {reason}")

    if len(lines) == 1:
        lines.append("- None found.")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Query the portable Kitchen Compass dinner + side catalog.")
    parser.add_argument("--data-root", help="Household data root. Defaults to ./kitchen-compass-data, except when run from the installed skill root it defaults to ../kitchen-compass-data so household data stays outside the skill.")
    parser.add_argument("--meal-type", choices=list(ACTIVE_ENGINE_MEAL_TYPES))
    parser.add_argument("--cooking-effort", choices=list(ENUM_CHOICES["cooking_effort"]))
    parser.add_argument("--ingredient-friction", choices=list(ENUM_CHOICES["ingredient_friction"]))
    parser.add_argument("--cost", choices=list(ENUM_CHOICES["cost"]))
    parser.add_argument("--serving-profile", choices=list(ENUM_CHOICES["serving_profile"]))
    parser.add_argument("--status", choices=list(ENUM_CHOICES["status"]))
    parser.add_argument("--structural-role", choices=list(ENUM_CHOICES["structural_role"]))
    parser.add_argument("--diet-mode")
    parser.add_argument("--context")
    parser.add_argument("--core", help="Substring match against core protein / main ingredient")
    parser.add_argument("--pairs-protein", help="Filter to recipes whose Pair With metadata explicitly mentions a protein term like chicken, pork, or beef")
    parser.add_argument("--needs-protein", action="store_true", help="Only show recipes that still need protein pairing")
    parser.add_argument("--wants-side", action="store_true", help="Only show dinners that naturally want a side")
    parser.add_argument("--self-contained", action="store_true", help="Only show dinners that are mostly self-contained")
    parser.add_argument("--text", help="Free-text search against title + snapshot + planning notes")
    parser.add_argument("--sort", default="title", choices=["title", "cooking_effort", "ingredient_friction", "cost", "status", "serving_profile", "core_protein"])
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--verbose", action="store_true", help="Render richer recipe output and print the resolved data root to stderr.")
    parser.add_argument("--pairs-with", help="Show pairing intelligence for a recipe slug or title")
    parser.add_argument("--show-view", choices=[
        "weeknight_easy_low_friction_dinners",
        "cheap_family_table_dinners",
        "filler_meals",
        "base_recipes_needing_pairing",
        "low_carb_dinners",
        "crowd_friendly_sides",
        "recipes_needing_protein_pairing",
        "dinners_that_want_a_side",
        "self_contained_dinners",
    ])
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    paths = KitchenCompassPaths.from_root(resolve_data_root(args.data_root, verbose=args.verbose))
    payload = load_catalog(paths.generated_query_dir / "recipe-catalog.json")

    if args.pairs_with:
        print(show_pairs(payload, args.pairs_with, args.limit))
        return

    recipes = payload["recipes"]
    if args.show_view:
        slugs = payload["common_queries"].get(args.show_view, [])
        recipes = [recipe for recipe in recipes if recipe["slug"] in slugs]

    recipes = sort_recipes(filter_recipes(recipes, args), args.sort)[: args.limit]
    if not recipes:
        print("No matching recipes.")
        return

    for recipe in recipes:
        print(render_recipe(recipe, args.verbose))


if __name__ == "__main__":
    main()
