import copy

from build_weekly_plan import PRESETS, can_add, score_recipe


def _recipe(**overrides):
    base = {
        "slug": "example",
        "title": "Example",
        "cooking_effort": "easy",
        "ingredient_friction": "low",
        "cost": "cheap",
        "status": "trusted",
        "serving_profile": "family-table",
        "composition_flags": {
            "mostly_self_contained": True,
            "wants_side_pairing": False,
            "needs_protein_pairing": False,
        },
        "context_occasion": [],
        "core_protein": "chicken",
        "meal_type": ["dinner"],
        "structural_role": ["full-meal"],
        "diet_modes": [],
        "pair_with_typed": [],
        "search_blob": "example recipe chicken",
        "ingredients_blob": "chicken",
    }
    base.update(overrides)
    return base


def test_trusted_scores_higher_than_testing():
    preset = PRESETS["balanced"]
    trusted = _recipe(status="trusted")
    testing = _recipe(status="testing")
    s_trusted, _, _ = score_recipe(trusted, [], preset)
    s_testing, _, _ = score_recipe(testing, [], preset)
    assert s_trusted > s_testing


def test_can_add_rejects_fourth_involved():
    preset = PRESETS["balanced"]
    involved_recipes = [_recipe(slug=f"i{n}", cooking_effort="involved") for n in range(3)]
    candidate = _recipe(slug="i4", cooking_effort="involved")
    # Balanced preset allows 0 involved; even the first one is rejected.
    assert not can_add(candidate, [], preset, target=4)
    assert not can_add(candidate, involved_recipes, preset, target=4)


def test_can_add_respects_aspirational_cap():
    preset = PRESETS["balanced"]
    candidate = _recipe(slug="a1", status="aspirational")
    assert not can_add(candidate, [], preset, target=3)


def test_inventory_bonus_nonzero_when_match():
    preset = PRESETS["balanced"]
    recipe = _recipe(search_blob="chicken thighs weeknight", core_protein="chicken")
    inventory_state = {
        "items": [
            {
                "id": "freezer-chicken-thighs",
                "label": "Chicken thighs",
                "location": "freezer",
                "kind": "protein",
                "quantity": {"amount": 3.0, "unit": "lb"},
                "match_rules": {
                    "recipe_slugs": [],
                    "search_terms": ["chicken thighs"],
                    "core_proteins": ["chicken"],
                },
                "planning": {"priority": "normal"},
                "notes": "",
            }
        ]
    }
    baseline, _, baseline_support = score_recipe(copy.deepcopy(recipe), [], preset)
    boosted, _, boost_support = score_recipe(copy.deepcopy(recipe), [], preset, inventory_state=inventory_state)
    assert boosted >= baseline
    assert boost_support is not None and boost_support.get("matches")


def test_inventory_bonus_zero_when_no_match():
    preset = PRESETS["balanced"]
    recipe = _recipe(search_blob="tofu stir fry", core_protein="tofu")
    inventory_state = {
        "items": [
            {
                "id": "freezer-beef",
                "label": "Ground beef",
                "location": "freezer",
                "kind": "protein",
                "quantity": {"amount": 2.0, "unit": "lb"},
                "match_rules": {
                    "recipe_slugs": [],
                    "search_terms": ["ground beef"],
                    "core_proteins": ["beef"],
                },
                "planning": {"priority": "normal"},
                "notes": "",
            }
        ]
    }
    baseline, _, _ = score_recipe(copy.deepcopy(recipe), [], preset)
    scored, _, support = score_recipe(copy.deepcopy(recipe), [], preset, inventory_state=inventory_state)
    assert scored == baseline
    assert not support or not support.get("matches")
