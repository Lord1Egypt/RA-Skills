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

   - A default plan has 7 days with exactly 3 slots per day; each cell has a non-empty
     topic, a non-empty practice item, and an integer duration.
   - Dates increment one day at a time from `--start-date` and carry the correct weekday.
   - No topic repeats until the whole pool has been used (`test_topic_no_repeat_until_pool_exhausted`).
   - Within a day, slot intervals never overlap, even at the maximum slot count and the
     maximum session length (`test_slots_do_not_overlap_within_a_day`).
   - Durations stay inside `[session_minutes - 10, session_minutes + 10]` and `[15, 110]`.
   - The same `--seed` always produces identical Markdown / text / JSON output, and two
     different seeds produce different output.
   - `--topics` works both as a comma-separated list of names and as a JSON pool file.
   - The Markdown renderer emits the expected table header and one row per cell.
   - CLI smoke: `--help`, default Markdown run, text and JSON runs, `--output` file
     writing, and a non-zero exit code for invalid arguments.

3. Reproducibility spot check:

   ```bash
   python3 scripts/generate_study_plan.py --seed 20240501 --start-date 2026-10-24
   python3 scripts/generate_study_plan.py --seed 20240501 --start-date 2026-10-24   # identical
   ```

## Manual checks

- Confirm the printed table is readable and contains one row per day per slot.
- Confirm that when `--seed` is omitted, a concrete seed is printed so the run can be
  reproduced.

## Acceptance criteria

See [acceptance-criteria.md](acceptance-criteria.md).