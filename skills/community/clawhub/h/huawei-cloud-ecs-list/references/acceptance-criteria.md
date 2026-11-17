# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | ListServersDetails full-field table output incl. 名称/ID/状态/规格/可用区/私网IP/公网IP | ✅ `render_table` + `normalize_server` |
| 4 | `--json` raw output mode | ✅ |
| 5 | `--names-only` compact 名称+ID 清单 output mode | ✅ `server_summary_lines` |
| 6 | `--status` / `--name` filters forwarded as real server-side ECS params | ✅ `build_command` |
| 7 | Empty-list explicit hint 「当前区域无 ECS 实例」(exit 0) | ✅ |
| 8 | 403 explicit hint 「无权限访问 ECS，请检查 IAM 权限」(exit 1) | ✅ `AuthError` |
| 9 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 10 | No write API call exists in code; write intents blocked by guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 11 | SDK fallback (`huaweicloudsdkecs`) when hcloud is missing | ✅ `list_servers_via_sdk` |
| 12 | Offline unit tests with mocked hcloud, all passing (SDK-optional cases skipped when `huaweicloudsdkecs` is absent) | ✅ 66 tests |
| 13 | Read-only REST path provenance documented | ✅ verification-method.md |
| 14 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
| 15 | Stdout-only: the script writes no file in any output mode | ✅ no write path in code |
| 16 | Read-only filter values (`--status` / `--name` / `--region` / `--page-size`) are not scanned by the write-intent guard, while a following flag is still scanned | ✅ `_VALUE_STRIPPED_FLAGS` + guard regression tests |