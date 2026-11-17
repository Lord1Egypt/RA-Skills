# Verification Method

## Scope

This skill is a pure local Python generator. Verification is fully offline and
does not contact Huawei Cloud, the Huawei Cloud CLI (KooCLI), any SDK, or any REST
API.

## Automated checks

1. Structural / specification validation:

   ```bash
   bash scripts/validate-skill.sh -s <skill-dir>
   ```

2. Unit tests bundled with the skill:

   ```bash
   python3 -m unittest discover -s tests -v
   ```

   Covered assertions:

   - The wardrobe has all four categories (上装 / 下装 / 鞋履 / 配饰) and every style /
     season is represented in each category.
   - A default outfit has exactly one item per category.
   - `--style` / `--season` filters are applied: with a fully covered pair (e.g.
     `休闲` + `秋`, `简约` + `冬`) every picked item is a strict match and `fallbacks`
     is empty.
   - The same `--seed` always produces identical output; different seeds differ.
   - Aliases and case-insensitivity work; an unknown style / season is rejected (exit 2).
   - JSON output round-trips through `json.loads`.
   - CLI smoke via `--help`, `--list-styles`, and end-to-end runs in each format.

3. Reproducibility spot check:

   ```bash
   python3 scripts/generate_outfit.py --seed 20240501 --format markdown
   python3 scripts/generate_outfit.py --seed 20240501 --format markdown   # identical
   ```

## Manual checks

- Confirm the printed outfit is readable and contains one item per category.
- Confirm that a forced `--style` / `--season` is reflected in the output and that no
  fallback note appears when a strict match exists.
- Confirm that when `--seed` is omitted, a concrete seed is shown so the run can be
  reproduced.

## Acceptance criteria

See [acceptance-criteria.md](acceptance-criteria.md).