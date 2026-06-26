# Kitchen Compass runtime contract

This is the human-readable runtime contract for the portable skill.
Shared machine-used constants live in `scripts/contract.py`; keep runtime docs aligned with the shipped scripts.

## Active v1 scope

The active engine is only guaranteed for `dinner` + `side` recipes.

Recipes for other meal types can exist in the same markdown schema, but the planner/query flow is dinner-side first.

## Authored sources of truth

Treat these as authored operational data:
- `recipes/*.md`
- `household/*.json`
- `inventory/items.json`
- `inventory/transactions.jsonl`
- optional human notes like `inventory/freezer.md`
- optional `deals/weekly-deal-brief-input.json`
- optional `deals/store-briefs/*.json`
- `history/events.jsonl`

Treat these as generated and rebuildable:
- `generated/query/recipe-catalog.json`
- `generated/query/common-queries.json`
- `generated/deals/weekly-deal-brief-latest.json`
- `generated/deals/weekly-deal-brief-latest.md`
- `generated/deals/weekly-deal-scan-latest.json`
- `generated/deals/weekly-deal-scan-latest.md`
- `generated/deals/combined-weekly-deal-sheet-latest.json`
- `generated/deals/combined-weekly-deal-sheet-latest.md`
- human-facing planning/query views under `generated/`

## Runtime expectations

- Create a new household root with `scripts/setup_household.py`.
- Pass the root with `--data-root`, or set `KITCHEN_COMPASS_DATA_ROOT`. The legacy `FOOD_BRAIN_DATA_ROOT` env var is still honored but deprecated.
- Recipe slugs come from markdown filename stems.
- Run `scripts/validate_recipes.py --data-root <path>` after recipe edits and before rebuilding the query catalog.
- Rebuild the query catalog after recipe edits before querying, planning, or recording history by title/slug.
- The planner reads `history/events.jsonl` automatically when present.
- The planner also reads `inventory/items.json` automatically when present.
- Weekly deal brief input/output is optional and manual; the planner does **not** read it as a scoring signal.
- Use `--history-file` to override the default history path.
- Use `--ignore-history` to disable history-aware scoring for a specific planner run.
- Inventory changes happen only through explicit edits; the planner and history recorder do not silently subtract stock.
- `household/preferences.json` currently drives:
  - `planning.default_preset`
  - `planning.default_dinners_per_week`
  - `planning.prioritize_inventory`
- `household/stores.json` can also store optional weekly deal brief setup, but that remains a manual decision-support feature outside planner scoring.

## History event contract

### Canonical path
- `history/events.jsonl`

### Format
- append-only JSON Lines
- one JSON object per line
- dates in ISO format: `YYYY-MM-DD`
- do not wrap the file in a JSON array

### Required keys
- `date`
- `event_type`
- `meal_slot`
- `recipe_slug`
- `source`

### Optional keys
- `notes`

### Allowed / expected values

#### `event_type`
- `planned`
- `made`

#### `meal_slot`
- current engine defaults to `dinner`
- keep the field explicit even though the current planner is dinner-centric

#### `recipe_slug`
- should match the recipe slug in the query catalog and the markdown filename stem

### Example event

```json
{"date":"2026-04-17","event_type":"made","meal_slot":"dinner","recipe_slug":"burger-bowls","source":"manual"}
```

## Related planning reference

For planner behavior, preset intent, hard constraints vs soft preferences, history-aware scoring, composition effects, and the current inventory bonus model, read `planning-logic.md` and `inventory-logic.md`.
For optional weekly deal brief setup and rendered output shape, read `weekly-deal-brief.md`.

## Inventory contract

### Canonical paths
- `inventory/items.json`
- `inventory/transactions.jsonl`

### Runtime notes
- `items.json` is the current remembered inventory state.
- `transactions.jsonl` is an append-only audit log of explicit inventory writes.
- Use `scripts/manage_inventory.py` for normal add / set / confirmed-use operations.
- The planner reads `items.json` directly, so inventory-only updates do not require rebuilding the recipe catalog.
- Inventory remains approximate household memory, not real-time stock tracking.

## Weekly deal brief contract

### Canonical authored path
- `deals/weekly-deal-brief-input.json`

### Canonical generated paths
- `generated/deals/weekly-deal-brief-latest.json`
- `generated/deals/weekly-deal-brief-latest.md`
- `generated/deals/weekly-deal-scan-latest.json`
- `generated/deals/weekly-deal-scan-latest.md`
- `generated/deals/combined-weekly-deal-sheet-latest.json`
- `generated/deals/combined-weekly-deal-sheet-latest.md`

### Runtime notes
- Use `scripts/manage_deal_sources.py` to manage and validate `household/stores.json` weekly deal source setup and the preferred weekly scan schedule.
- `household/stores.json` may also store a per-store `retrieval_recipe` that remembers how a successful weekly retrieval worked last time.
- `household/stores.json` may also store `weekly_deal_brief.scan_schedule` to remember the household's preferred scan time.
- Use `scripts/prepare_weekly_deal_scan.py` to create per-store weekly brief stubs and a current scan packet for the selected stores.
- Use `scripts/render_weekly_deal_brief.py` to normalize and render a single-store weekly deal brief.
- Use `scripts/render_combined_weekly_deal_sheet.py` to combine all selected store briefs into one grouped weekly deal sheet.
- The combined sheet groups by display category (`meat`, `starch`, `dairy`, `fruit-veg`, `beverages`, `misc`) and keeps the display layer simple.
- Discount percentage is only rendered when it is explicitly provided or honestly computable from sale vs regular price, but combined output may simply show sale and normal price text directly.
- The planner does not read the rendered weekly deal brief or combined weekly deal sheet.

## Manual editing rules

- Append one event per line.
- Keep dates parseable and recipe slugs current.
- Prefer the recorder script for normal writes; edit manually only when you need to repair or backfill history.
