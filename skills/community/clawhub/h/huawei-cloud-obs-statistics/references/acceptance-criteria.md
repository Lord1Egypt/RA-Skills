# Acceptance Criteria

## Functional Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| AC-01 | Bucket count is reported | `summary.bucket_count` equals the number of buckets in scope |
| AC-02 | Object count is reported | `summary.object_count` equals the number of objects scanned (prefix-limited when `--prefix`) |
| AC-03 | Total capacity is reported | `summary.total_size_bytes` is the sum of object `Size` (documented as an estimate, not a billing figure) |
| AC-04 | Storage-class distribution is reported | `storage_class_distribution` maps each storage class to its object count (with `storage_class_size_bytes`) |
| AC-05 | Region distribution is reported | `region_distribution` maps each region to its bucket count |
| AC-06 | Table output (default) | `python3 scripts/collect_obs_stats.py --bucket <bucket>` prints a readable table |
| AC-07 | JSON output | `--json` / `--output json` prints the full structured object |
| AC-08 | Markdown output | `--output md` prints a Markdown report |
| AC-09 | Empty scope returns zeroed report | A bucket with no objects yields zeros and exit 0 |
| AC-10 | Truncation is signalled | Reaching `--max-objects` sets `truncated=true` and a warning |
| AC-11 | SDK fallback works | `--executor sdk` yields the same report shape as the CLI path |
| AC-12 | Read-only guarantee | No create/update/delete operation is ever invoked |

## Security Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| AC-S1 | No AK/SK hardcoded in skill files | grep for literal `access_key=` / `secret_key=` values returns nothing |
| AC-S2 | No in-session credential-entry command | SKILL.md and references never include `hcloud configure set` with credential flags |
| AC-S3 | Least-privilege IAM policy | `references/iam-policies.md` grants only `obs:bucket:ListBucket` and `obs:object:List` |
| AC-S4 | Write-intent guard | Mutating intents are rejected before any command runs |

## Quality Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| AC-Q1 | SKILL.md follows the Huawei Cloud Skill Specification | `bash validate-skill.sh -s <skill-path>` passes with zero Critical failures |
| AC-Q2 | Script runs without syntax errors | `python3 scripts/collect_obs_stats.py --help` exits 0 |
| AC-Q3 | Offline tests pass | `python3 -m unittest discover -s tests` reports OK |
| AC-Q4 | SKILL.md ≤ 500 lines, total files ≤ 30 | `wc -l SKILL.md`; `find . -type f` |