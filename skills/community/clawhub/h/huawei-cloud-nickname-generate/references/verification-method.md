# Verification Method

## Scope

This skill is a pure local Python generator. Verification is fully offline and does not
contact Huawei Cloud, the Huawei Cloud CLI (KooCLI), any SDK, or any REST API.

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

   - The pool has all four slots (prefix / modifier / core / suffix) and every style is
     represented in every slot.
   - Every length bucket declares a range and patterns whose slots exist in the pool.
   - A default run returns exactly one nickname; the default count is `1`.
   - `--style` filtering is applied: with a covered style every part of every nickname
     carries that style and `fallbacks` is empty.
   - `--length` filtering is applied: every generated nickname's character count falls
     inside the requested bucket's `min`–`max`.
   - A `--count` batch is de-duplicated and returns exactly `count` names; the count bound
     (`1`–`20`) is enforced.
   - The same `--seed` always produces identical output; different seeds differ.
   - Aliases and case-insensitivity work; an unknown style / length / count is rejected
     (exit 2).
   - JSON output round-trips through `json.loads`.
   - No cloud/third-party imports appear in the source.
   - CLI smoke via `--help`, `--list-styles`, `--list-lengths`, every format, and
     `--output`.

3. Reproducibility spot check:

   ```bash
   python3 scripts/generate_nickname.py --seed 20240501 --count 3 --format markdown
   python3 scripts/generate_nickname.py --seed 20240501 --count 3 --format markdown   # identical
   ```

## Manual checks

- Confirm the printed nicknames are readable and that a requested style / length is
  reflected in the output.
- Confirm that a batch contains no repeated name.
- Confirm that when `--seed` is omitted, a concrete seed is shown so the run can be
  reproduced.

## Acceptance criteria

See [acceptance-criteria.md](acceptance-criteria.md).