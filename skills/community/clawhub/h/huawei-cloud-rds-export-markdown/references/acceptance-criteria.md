# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ + templates/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`, FAIL = 0) | ✅ |
| 3 | A local `.md` file is generated whose content includes the RDS instance-name list | ✅ `render_markdown` + `write_markdown` |
| 4 | Empty query result still writes a valid `.md` (header + empty-table note), exit 0, no error | ✅ |
| 5 | `--region` / `--project_id` / `--output` supported | ✅ |
| 6 | Optional `--name` / `--status` filters (status applied client-side) | ✅ `build_command` + `filter_by_status` |
| 7 | Missing AK/SK credentials produce an explicit error hint (exit 1) | ✅ `ConfigError` |
| 8 | 403 / insufficient IAM permission produces an explicit hint (exit 1) | ✅ `AuthError` |
| 9 | hcloud not installed → SDK fallback; both unavailable → explicit hint (exit 1) | ✅ `list_instances_via_sdk` |
| 10 | Read-only guard rejects mutating operations before any command runs | ✅ `guard_write_intent` / `guard_operation` |
| 11 | Only the read-only `ListInstances` REST path is ever constructed | ✅ `build_command` |
| 12 | Offline unit tests with mocked hcloud, all passing | ✅ |
| 13 | Documented usage / parameters (SKILL.md Core Commands + Parameter Confirmation + references) | ✅ |
| 14 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |