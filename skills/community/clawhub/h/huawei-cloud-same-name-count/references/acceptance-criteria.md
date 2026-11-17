# Acceptance Criteria

| # | Criterion | How it is checked |
|---|-----------|-------------------|
| 1 | Skill directory follows the Huawei Cloud Skill layout (`SKILL.md` + `scripts/` + `tests/` + `references/`) | `validate-skill.sh`; directory tree |
| 2 | A single run returns the same-name count for a given name | `python3 scripts/query.py --name 张伟`; `test_total_for_known_name` |
| 3 | Optional `--gender` / `--province` filter the result and drive the dimension breakdown | `test_gender_filter_is_applied`; `test_province_filter_is_applied`; `test_combined_filter` |
| 4 | A name absent from the dataset yields an explicit no-result message (not silent) | `test_absent_name_reports_no_result`; `test_cli_no_match_exits_zero_with_message` |
| 5 | A filter that excludes every record also yields an explicit message with the available dimensions | `test_filter_excludes_all_reports_no_result`; `test_cli_filter_excludes_all_message` |
| 6 | `--format json` emits parseable JSON carrying `matched` / `message` | `test_json_render_round_trips`; `test_json_no_match_carries_message` |
| 7 | Unknown gender / province and a missing name are rejected (exit 2) | `test_cli_unknown_gender_fails`; `test_cli_missing_name_fails` |
| 8 | Results are reproducible (fixed dataset) | `test_total_for_known_name`; reproducibility spot check |
| 9 | No Huawei Cloud API / resource / credential is required | No `hcloud`/SDK/curl in the skill; runs offline |

## Out of scope (not acceptance criteria)

- Real, authoritative population-register data (the dataset is a demo fixture)
- Live third-party / public-security name-query interfaces
- Cross-database aggregation or full-national coverage
- UI / chart rendering of the breakdown
- Personal-data or privacy controls beyond the bundled sample figures