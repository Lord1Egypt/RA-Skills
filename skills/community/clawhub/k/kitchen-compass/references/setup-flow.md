# Kitchen Compass setup flow

## Goal
Create a portable Kitchen Compass user-data root that stays separate from the skill itself.

## Shell assumption
Run the bundled scripts from the installed `kitchen-compass` skill directory:

```bash
cd /path/to/kitchen-compass
```

## Canonical setup sequence

1. Run `python3 scripts/setup_household.py --data-root <path>` to copy the sample household seed, including a set of sample recipes under `assets/sample-household/recipes/`.
2. Fill in `household/profile.json`, `household/preferences.json`, and `household/stores.json`.
3. Add recipe markdown files under `recipes/` using `_recipe-template.md` or `assets/recipe-template.md`.
4. Validate recipes with `python3 scripts/validate_recipes.py --data-root <path>`.
5. Rebuild the catalog with `python3 scripts/build_recipe_query_index.py --data-root <path>`. The builder runs the same validation by default and exits nonzero on any failure; pass `--skip-validation` only as an escape hatch.
6. Optionally add remembered inventory with `python3 scripts/manage_inventory.py --data-root <path> ...`.
7. Query recipes or build plans.
8. Optionally opt into manual weekly deal briefs with `python3 scripts/manage_deal_sources.py --data-root <path> ...`, then curate `deals/weekly-deal-brief-input.json` and render it with `python3 scripts/render_weekly_deal_brief.py --data-root <path>`.
9. Record meal history in `history/events.jsonl` through `python3 scripts/record_meal_history.py --data-root <path> ...`.

## Practical rules

- Keep authored content in `recipes/`, `household/`, `inventory/`, optional `deals/`, and `history/`.
- Inventory only changes through explicit writes; planning/history runs do not silently subtract it.
- Weekly deal briefs are optional and manual; do not treat them as Default-mode setup or pretend retailer discovery is automatic.
- After a store works once, save the store-specific retrieval recipe in `household/stores.json` so later runs can reuse what actually worked.
- Treat `generated/` as rebuildable output.
- Do not put a real household inside the skill directory.
- Do not assume breakfast/snack/appetizer/dessert planning is part of the active v1 engine.

## Current runtime expectations

- Pass the household root with `--data-root`, or set `KITCHEN_COMPASS_DATA_ROOT`.

**Migration:** `FOOD_BRAIN_DATA_ROOT` is still honored but deprecated; set `KITCHEN_COMPASS_DATA_ROOT` instead.
- `household/preferences.json` currently drives `planning.default_preset`, `planning.default_dinners_per_week`, and `planning.prioritize_inventory` in the planner.
- `household/stores.json` can also store optional weekly deal brief setup, but deal briefs stay outside planner scoring.
- Treat other household JSON fields as stored context unless a script explicitly documents that it reads them.
- Rebuild the query catalog after recipe edits and before planning or history lookups that depend on current recipe slugs/titles.
- For exact recipe field values, enum sets, and `Composition` rules, read `recipe-schema.md`.
- For inventory storage/update rules, read `inventory-logic.md`.
- For manual history editing and runtime assumptions, read `runtime-contract.md`.

## Minimum viable user-data root

- `household/profile.json`
- `household/preferences.json`
- `household/stores.json`
- `inventory/items.json`
- at least one dinner or side recipe in `recipes/` (the shipped sample-household ships with nine across multiple proteins so presets and pairing intel have real data to chew on)
- optional `deals/weekly-deal-brief-input.json` for households that opt into manual weekly deal briefs
- optional `history/events.jsonl`

## Example commands

```bash
cd /path/to/kitchen-compass
python3 scripts/setup_household.py --data-root ~/kitchen-compass-data
python3 scripts/validate_recipes.py --data-root ~/kitchen-compass-data
python3 scripts/build_recipe_query_index.py --data-root ~/kitchen-compass-data
python3 scripts/manage_inventory.py --data-root ~/kitchen-compass-data add --label "Ground beef" --location freezer --kind protein --amount 3 --unit lb
python3 scripts/query_recipes.py --data-root ~/kitchen-compass-data --meal-type dinner --self-contained
python3 scripts/build_weekly_plan.py --data-root ~/kitchen-compass-data --preset easy
python3 scripts/manage_deal_sources.py --data-root ~/kitchen-compass-data validate
python3 scripts/render_weekly_deal_brief.py --data-root ~/kitchen-compass-data
```
