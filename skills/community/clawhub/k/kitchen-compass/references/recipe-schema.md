# Kitchen Compass recipe schema

This is the human-readable recipe contract for authored markdown files.
The portable scripts share the same machine-used labels, enums, and composition values through `scripts/contract.py`; keep this reference aligned with that file.

## Canonical section order

Every recipe file should use this exact order:

1. `## Snapshot`
2. `## Ingredients`
3. `## Instructions`
4. `## House Tweaks / Change Log`
5. `## Planning Notes`
6. `## Notes`

## Snapshot syntax

Use this authored pattern for every field:

```md
- **Field Label:** value
```

Exact label spelling matters.

## Snapshot labels and machine keys

- `Source` -> `source`
- `Status` -> `status`
- `Meal Type` -> `meal_type`
- `Structural Role` -> `structural_role`
- `Core Protein / Main Ingredient` -> `core_protein`
- `Serves` -> `serves`
- `Time` -> `time`
- `Cooking Effort` -> `cooking_effort`
- `Ingredient Friction` -> `ingredient_friction`
- `Cost` -> `cost`
- `Serving Profile` -> `serving_profile`
- `Diet Modes` -> `diet_modes`
- `Context / Occasion` -> `context_occasion`
- `Flexibility` -> `flexibility`
- `Pair With` -> `pair_with`
- `Tags` -> `tags`

## Required for dinner + side engine participation

These fields need usable values:

- `source`
- `status`
- `meal_type`
- `structural_role`
- `core_protein`
- `serves`
- `time`
- `cooking_effort`
- `ingredient_friction`
- `cost`
- `serving_profile`
- `flexibility`

## Enum sets

### `status`
- `trusted`
- `testing`
- `aspirational`

### `meal_type`
- `dinner`
- `side`
- `breakfast-brunch`
- `snack`
- `appetizer-party`
- `dessert`
- `component`

### `structural_role`
- `full-meal`
- `base`
- `component`
- `pairing`
- `filler-meal`

### `cooking_effort`
- `easy`
- `moderate`
- `involved`

### `ingredient_friction`
- `low`
- `medium`
- `high`

### `cost`
- `cheap`
- `medium`
- `expensive`

### `serving_profile`
- `small-table`
- `family-table`
- `crowd-friendly`

### `flexibility`
- `rigid`
- `some-flex`
- `forgiving`

## List fields

These fields are comma-separated lists in authored markdown:

- `meal_type`
- `structural_role`
- `diet_modes`
- `context_occasion`
- `pair_with`
- `tags`

## `Pair With` semantics

Prefer typed entries when the category is clear:

- `protein: ...`
- `side: ...`
- `support: ...`
- `general: ...`

Untyped legacy entries still work, but the engine treats them as fallback.
For compatibility, the shared parser also normalizes legacy `condiment:` entries to `support` if they appear.

## Planning Notes contract

Keep `## Planning Notes` in every recipe.

Recommended labeled bullets:

- `Serving assumptions`
- `Scaling notes`
- `Composition`
- `Pairing notes`
- `Deal / sale notes`
- `Visual reference`

### `Composition`
Use exactly one of:

- `self-contained`
- `wants-side`
- `needs-protein-pairing`
- `flexible`

## House-version rule

Ingredients and instructions should reflect the current operating version of the recipe. Do not bury the real version only in notes.

## Scope boundary

The active engine is only guaranteed for dinner + side planning. Broader meal types can exist in the same schema, but the planner/query surface is dinner-side first.

## Related runtime contract

For history event shape, planner defaults, rebuild expectations, and the authored-vs-generated boundary, read `runtime-contract.md`.
