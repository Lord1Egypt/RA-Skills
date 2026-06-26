# Kitchen Compass user-data layout

## Principle
Ship the engine in the skill. Keep real household data outside the skill.

## Canonical layout

```text
kitchen-compass-data/
  household/
    profile.json
    preferences.json
    stores.json
  inbox/
    raw-recipes/
  recipes/
    _recipe-template.md
    *.md
  inventory/
    items.json
    transactions.jsonl
    freezer.md
  deals/
    weekly-deal-brief-input.json
    store-briefs/
      <store-id>.json
  history/
    events.jsonl
  generated/
    query/
      recipe-catalog.json
      common-queries.json
      planning-views/
    planner/
      weekly-plans.json
      planning-views/
    deals/
      weekly-deal-brief-latest.json
      weekly-deal-brief-latest.md
      weekly-deal-scan-latest.json
      weekly-deal-scan-latest.md
      combined-weekly-deal-sheet-latest.json
      combined-weekly-deal-sheet-latest.md
```

## Canonical authored vs generated material

Authored operational data lives in:
- `household/`
- `recipes/`
- `inventory/`
- `deals/`
- `history/events.jsonl`

Rebuildable machine output lives in:
- `generated/`

## What belongs where

### `household/`
Store household-level context only:
- `profile.json` — household shape and descriptive context
- `preferences.json` — planner defaults; the v1 planner currently reads `planning.default_preset`, `planning.default_dinners_per_week`, and `planning.prioritize_inventory`
- `stores.json` — store notes/preferences for agent or user reference; this can also hold optional `weekly_deal_brief` manual setup, a small preferred scan schedule, and remembered per-store retrieval recipes, but store-specific automation is not part of the v1 runtime contract

Do not put recipe-specific serving math here.

### `inbox/raw-recipes/`
Use for messy intake material to normalize later.

### `recipes/`
Store authored recipe markdown files. This is the main source of truth for meal content.

### `inventory/`
Store remembered household inventory here.

Current portable runtime expectations:
- `items.json` — canonical machine-readable current inventory state
- `transactions.jsonl` — append-only audit log of explicit add / set / confirmed-use writes
- `freezer.md` — optional human notes only; the planner does not parse this markdown file

### `deals/`
Store optional manual weekly deal inputs here.

Current portable runtime expectations:
- `weekly-deal-brief-input.json` — legacy single-store current-week input
- `store-briefs/<store-id>.json` — current per-store weekly deal brief inputs used for the combined multi-store sheet

### `history/`
Store append-only meal history. `events.jsonl` is authored operational data, not generated output. Follow `runtime-contract.md` for event shape.

### `generated/`
Store rebuildable machine and view outputs only, including rendered weekly deal scan packets, single-store briefs, and combined weekly deal sheet artifacts.

## Path guidance

- Pass the user-data root with `--data-root` when running scripts.
- If you omit `--data-root` from the installed skill directory, the implicit default resolves to sibling `../kitchen-compass-data` so the household stays outside the skill.
- Do not hardcode workspace-specific paths inside portable scripts or usage guidance.
- Keep paths inside generated output relative to the data root when practical.

## Future-user contract

A future user should be able to:
1. create a fresh `kitchen-compass-data/` directory,
2. run the setup script,
3. add recipes and household config,
4. run the planner/query scripts,
5. keep their own data without touching the skill package.
