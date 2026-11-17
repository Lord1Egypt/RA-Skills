# Usage Guide

## Quick start

```bash
python3 scripts/generate_outfit.py --seed 20240501
```

Prints a Markdown outfit (上装 / 下装 / 鞋履 / 配饰) chosen for a random style and
season to stdout.

## Common variations

```bash
# Plain text
python3 scripts/generate_outfit.py --seed 42 --format text

# JSON (machine-readable, for piping into other tools)
python3 scripts/generate_outfit.py --seed 42 --format json

# Force a style (aliases accepted, case-insensitive)
python3 scripts/generate_outfit.py --style casual
python3 scripts/generate_outfit.py --style 通勤

# Force a season to dress for
python3 scripts/generate_outfit.py --season autumn
python3 scripts/generate_outfit.py --season 冬

# Force both filters
python3 scripts/generate_outfit.py --seed 7 --style minimal --season winter

# See what the wardrobe supports
python3 scripts/generate_outfit.py --list-styles
python3 scripts/generate_outfit.py --list-seasons

# Write to a file
python3 scripts/generate_outfit.py --seed 7 --output outfit.md
```

## Styles and seasons

The built-in wardrobe is tagged with five styles and four seasons:

- Styles: `休闲` (casual), `通勤` (commute/business), `运动` (sport), `复古` (vintage),
  `简约` (minimal).
- Seasons: `春` (spring), `夏` (summer), `秋` (autumn/fall), `冬` (winter).

`--style` / `--season` accept either the Chinese label or an ASCII alias; matching is
case-insensitive. An unknown value is rejected with exit code `2` and a message listing
the valid choices.

## Filtering behaviour

For each category the generator first looks for items that match **both** the chosen
style and season. If none exist it relaxes the season constraint, then the style one, and
records the affected category under `fallbacks` (Markdown/text print a short note, JSON
exposes the list). A category is only relaxed when the wardrobe has no strict match, so
when a strict match exists the output always respects the requested filters.

## Reproducibility

- Passing `--seed <int>` makes the output deterministic: the same seed and the same
  filters always produce the same outfit.
- Omitting `--seed` still works; the generator picks a random seed and prints it
  (`Seed: <n>` when writing to a file, `随机 seed <n>` in the body), so the run can be
  reproduced later with `--seed <n>`.

## Extending the wardrobe

`scripts/wardrobe.json` holds the item pools. Each category (`top`, `bottom`,
`footwear`, `accessory`) is an array of `{"name", "styles", "seasons"}` entries. Add
items to a category array; keep at least a couple of items per style and season so a
strict, unrelaxed match stays possible. No code change is required. A completely
different wardrobe can be supplied with `--wardrobe /path/to/wardrobe.json`, which uses
the same shape.