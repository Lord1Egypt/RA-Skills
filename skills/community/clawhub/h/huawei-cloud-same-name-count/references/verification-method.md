# Verification Method

## Scope

This skill is a pure local Python query tool. Verification is fully offline and
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

   - The dataset loads and contains records, both genders, and the expected provinces.
   - A known name (`张伟`) returns the exact total (`6901`) and a by-province
     breakdown whose parts sum to the total.
   - `--gender` and `--province` filters actually constrain the result (`刘洋` splits
     2210 男 / 2108 女; `张伟` + 广东 → 1688).
   - An absent name returns `matched=false` with an explicit message.
   - A name that exists but whose filter excludes all rows (`张伟` + 女) returns
     `matched=false` with an explicit message and the dimensions the name does have.
   - Gender / province aliases (and case-insensitivity) resolve to canonical values.
   - Unknown gender / province and an empty name are rejected (exit 2).
   - Markdown / text / JSON renderings; JSON round-trips through `json.loads`.
   - CLI smoke: default run, JSON run, no-result run (exit 0), invalid filter (exit 2),
     missing name (exit 2), `--list-provinces`, `--list-genders`, `--help`.

3. Reproducibility spot check:

   ```bash
   python3 scripts/query.py --name 张伟 --format markdown
   python3 scripts/query.py --name 张伟 --format markdown   # identical
   ```

## Manual checks

- Confirm the printed total equals the sum of the by-province breakdown.
- Confirm a forced `--gender` / `--province` is reflected in the output.
- Confirm a no-match query prints an explicit message instead of an empty or silent
  output.

## Acceptance criteria

See [acceptance-criteria.md](acceptance-criteria.md).