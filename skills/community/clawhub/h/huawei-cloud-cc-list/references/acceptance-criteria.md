# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | ListCloudConnections full-field table output incl. 名称/ID/状态/带宽/网络实例数/企业项目 | ✅ `render_table` + `normalize_connection` |
| 4 | `--json` raw output mode | ✅ |
| 5 | `--names-only` output mode | ✅ |
| 6 | `--name` / `--status` / `--id` filters working (real server-side query params) | ✅ `build_command` |
| 7 | Empty-list explicit hint 「当前区域无云连接（CC）实例」(exit 0) | ✅ |
| 8 | 403 explicit hint 「无权限访问云连接（CC），请检查 IAM 权限」(exit 1) | ✅ `AuthError` |
| 9 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 10 | No write API call exists in code; write intents blocked by guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 11 | SDK fallback (`huaweicloudsdkcc`) when hcloud is missing | ✅ `list_connections_via_sdk` |
| 12 | Offline unit tests with mocked hcloud, all passing | ✅ |
| 13 | Read-only REST path provenance documented | ✅ verification-method.md |
| 14 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
| 15 | `network/cc` provides the new Network category path | ✅ |
