# Kitchen Compass inventory logic

This document is the concrete implementation spec for Kitchen Compass inventory awareness.

It exists to lock the product behavior before and alongside the portable implementation.

Companion docs:
- `planning-logic.md`
- `runtime-contract.md`
- `user-data-layout.md`

## Product goal
Inventory is an **optional planning signal**.

It should let Kitchen Compass:
1. remember what the household explicitly says it has,
2. update that remembered state only through explicit writes,
3. subtract usage only through explicit user-confirmed updates,
4. give already-valid meals a planning bonus when the remembered inventory clearly supports them,
5. let the household toggle whether that inventory signal stays light or becomes more assertive,
6. explain that influence in plain language.

It should **not** pretend to be real-time stock tracking.
It should **not** become a hard planner gate.
It should **not** outrank preset fit, hard constraints, or week-quality logic.

## Canonical storage model

### Current-state file
Canonical machine-readable inventory state lives at:
- `inventory/items.json`

Shape:

```json
{
  "version": 1,
  "updated_at": "2026-04-18T17:15:00Z",
  "items": [
    {
      "id": "freezer-ground-beef",
      "label": "Ground beef",
      "location": "freezer",
      "kind": "protein",
      "quantity": {
        "amount": 3,
        "unit": "lb"
      },
      "match_rules": {
        "recipe_slugs": [],
        "search_terms": ["ground beef"],
        "core_proteins": ["beef"]
      },
      "planning": {
        "priority": "normal"
      },
      "notes": "80/20 family pack",
      "updated_at": "2026-04-18T17:15:00Z"
    }
  ]
}
```

### Append-only audit log
Operational writes should also append to:
- `inventory/transactions.jsonl`

This is an audit trail of explicit changes like:
- `add`
- `set`
- `confirmed-use`

The planner reads `items.json`.
The transactions log is for repairability, transparency, and debugging.

### Optional human notes
Optional freeform notes can still live at:
- `inventory/freezer.md`

That markdown file is reference context only.
The planner does not parse it.

## Item contract

### Required practical fields
- `id`
- `label`
- `location`
- `kind`
- `quantity.amount`
- `quantity.unit`

### Supported enum lanes
#### `location`
- `freezer`
- `fridge`
- `pantry`
- `other`

#### `kind`
- `protein`
- `produce`
- `prepared`
- `other`

#### `planning.priority`
- `normal`
- `prefer-soon`
- `low`

### Match rules
Each item can help the planner through any of these soft match rules:
- `recipe_slugs` — strongest, explicit recipe targeting
- `search_terms` — label/ingredient-style text matched against recipe title/slug/ingredients/planning text
- `core_proteins` — broadest lane match, for example `beef` or `chicken`

If the user does not provide match rules, the runtime can derive conservative defaults from the label:
- `search_terms` defaults to the normalized label
- `core_proteins` is auto-derived only when obvious from the label

## Update model
Inventory changes must be explicit.

### Add
Create a new remembered item.

Example:
```bash
python3 scripts/manage_inventory.py \
  --data-root ~/kitchen-compass-data \
  add \
  --label "Ground beef" \
  --location freezer \
  --kind protein \
  --amount 6 \
  --unit lb
```

### Set / update current state
Update the remembered state for an existing item.
This is the general-purpose correction path.

Example:
```bash
python3 scripts/manage_inventory.py set \
  --data-root ~/kitchen-compass-data \
  --item freezer-ground-beef \
  --amount 4 \
  --unit lb \
  --priority prefer-soon
```

### Confirmed usage subtraction
Subtract usage only when the user explicitly confirms it.

Example:
```bash
python3 scripts/manage_inventory.py use \
  --data-root ~/kitchen-compass-data \
  --item freezer-ground-beef \
  --amount 3 \
  --unit lb \
  --confirmed \
  --notes "Used for burger bowls"
```

### Non-goals
Inventory does **not** auto-update when:
- a weekly plan is generated
- a meal is marked planned
- a meal is marked made

Those events may motivate a human confirmation step, but they do not silently mutate inventory.

## Planner insertion rule
Inventory enters the planner **after** candidate validity is decided.

Locked order:
1. preset/diet gating
2. hard mix constraints
3. core scoring signals
4. week-level shaping
5. history-aware shaping
6. inventory bonus

That means inventory:
- cannot rescue an invalid candidate,
- cannot override hard constraints,
- cannot override preset fit,
- cannot fix a structurally bad week.

## Inventory scoring rule
Inventory support is a capped bonus controlled by a household boolean.

### Household boolean
Use `household/preferences.json`:
- `planning.prioritize_inventory = false` → keep inventory in the normal light/tiebreaker lane
- `planning.prioritize_inventory = true` → strengthen inventory influence for strong matches without turning it into a hard gate

Default-route households that never opt into structured inventory still get no inventory effect in practice because there is no remembered inventory state to use.

### Matching strength tiers
- explicit `recipe_slugs` match → strongest
- `search_terms` found in recipe title/slug/ingredients/planning text → medium
- `core_proteins` lane match → weakest

### Quantity role
Quantity only shapes the bonus tier.
It is not recipe-exact ingredient accounting.

Current implementation uses rough availability tiers such as:
- larger positive amount → fuller bonus
- smaller positive amount → reduced bonus
- zero or negative amount → no bonus

This is intentionally approximate and honest.
Kitchen Compass knows what the household said it has, not exact recipe-consumption math.

### Bonus cap rule
Inventory bonus stays capped low enough that it can influence close calls without dominating the planner.

## Explanation behavior
When inventory affects a selected dinner, planner output should say so plainly.

Example explanation style:
- `Inventory support: you already have 3 lb ground beef in the freezer (matches recipe text for ground beef)`

The output should expose:
- which inventory item helped
- remembered quantity
- location
- a short why/reason phrase

If no inventory helped, the planner should stay quiet about inventory.

## Runtime behavior summary
- `setup_household.py` seeds `inventory/items.json` and `inventory/transactions.jsonl`
- `manage_inventory.py` is the explicit mutation surface
- `build_weekly_plan.py` reads `inventory/items.json` directly at runtime
- inventory changes do **not** require rebuilding the recipe catalog
- recipe edits still require rebuilding the query catalog as usual

## Acceptance criteria
Inventory only counts as implemented when all of these are true:

1. **Structured storage exists**
   - a household data root contains `inventory/items.json`

2. **Explicit write paths exist**
   - the runtime supports add / set / confirmed-use operations

3. **Confirmed usage exists**
   - usage subtraction requires an explicit confirmation-style path and is logged

4. **Planner influence is real**
   - a planner run with supporting inventory can produce a higher score than the same run without that inventory

5. **Explanation is visible**
   - planner output clearly states when remembered inventory helped a selected dinner

6. **No silent subtraction**
   - planning/history scripts do not mutate inventory on their own

## Suggested smoke tests
1. Initialize a temp household root.
2. Add a small dinner recipe set and build the query catalog.
3. Run the planner with empty inventory and save the JSON output.
4. Add `Ground beef` inventory.
5. Run the planner again.
6. Verify at least one selected dinner now includes `inventory_support` and plain-language markdown output.
7. Run a confirmed usage subtraction.
8. Verify `items.json` quantity decreased and `transactions.jsonl` recorded the change.
