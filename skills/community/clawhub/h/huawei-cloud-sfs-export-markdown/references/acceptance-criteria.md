# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ + templates/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`, FAIL = 0) | ✅ |
| 3 | A local `.md` file is generated whose content includes the SFS file-system-name list | ✅ `render_markdown` + `write_markdown` |
| 4 | Empty query result still writes a valid `.md` (header + empty-table note), exit 0, no error | ✅ |
| 5 | `--region` / `--output` supported (`--output` default `sfs_share_list.md`, parent dir auto-created) | ✅ |
| 6 | Optional `--name` (client-side substring) / `--status` (client-side exact) filters | ✅ `build_command` + `filter_shares` |
| 7 | `--help` documents region / output path parameters | ✅ argparse |
| 8 | Missing AK/SK credentials produce an explicit error hint (exit 1) | ✅ `ConfigError` |
| 9 | 403 / insufficient IAM permission produces an explicit hint (exit 1) | ✅ `AuthError` |
| 10 | hcloud not installed → SDK fallback; both unavailable → explicit hint (exit 1) | ✅ `list_shares_via_sdk` |
| 11 | Read-only guard rejects mutating operations before any command runs | ✅ `guard_write_intent` / `guard_operation` |
| 12 | Only the read-only `ListShares` REST path is ever constructed | ✅ `build_command` |
| 13 | Offline unit tests with mocked hcloud, all passing | ✅ |
| 14 | Documented usage / parameters (SKILL.md Core Commands + Parameter Confirmation + references) | ✅ |
| 15 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |