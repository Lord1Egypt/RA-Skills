# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | ListBareMetalServers full-field table output incl. 名称/ID/状态/规格/可用区/IP | ✅ `render_table` + `normalize_server` |
| 4 | `--json` raw output mode | ✅ |
| 5 | `--names-only` output mode | ✅ |
| 6 | `--name` / `--status` forwarded as real server-side API params; `--server-id` applied client-side (API has no server-id param) | ✅ `build_command` + `filter_by_server_id` |
| 7 | Empty-list explicit hint 「当前区域无裸金属服务器」(exit 0) | ✅ |
| 8 | 403 explicit hint 「无权限访问 BMS，请检查 IAM 权限」(exit 1) | ✅ `AuthError` |
| 9 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 10 | No write API call exists in code; write intents blocked by guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 11 | SDK fallback (`huaweicloudsdkbms`) when hcloud is missing | ✅ `list_servers_via_sdk` |
| 12 | Automatic page-number offset paging (count/total_count aware, max pages cap) | ✅ `list_servers` |
| 13 | Offline unit tests with mocked hcloud, all passing | ✅ |
| 14 | Read-only REST path provenance documented | ✅ verification-method.md |
| 15 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
