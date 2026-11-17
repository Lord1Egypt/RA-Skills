# Acceptance Criteria

| # | Criterion | Status |
| - | --------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ + templates/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | ListSubnets full-field table output incl. 名称/ID/CIDR/网关/VPC ID/状态 及其余字段 | ✅ `render_table` + `normalize_subnet` |
| 4 | `--json` raw output mode | ✅ |
| 5 | `--names-only` output mode | ✅ |
| 6 | `--vpc-id` filter working (real server-side query parameter) | ✅ `build_command` |
| 7 | Empty-list explicit hint 「当前区域无 VPC 子网（Subnet）」(exit 0) | ✅ |
| 8 | 403 explicit hint 「无权限访问 VPC 子网（Subnet），请检查 IAM 权限」(exit 1) | ✅ `AuthError` |
| 9 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 10 | Missing project_id (SDK fallback) explicit hint (exit 1) | ✅ `resolve_project_id` |
| 11 | No write API call exists in code; write intents blocked by guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 12 | SDK fallback (`huaweicloudsdkvpc`) when hcloud is missing | ✅ `list_subnets_via_sdk` |
| 13 | Offline unit tests with mocked hcloud, all passing | ✅ |
| 14 | Read-only REST path provenance documented | ✅ verification-method.md |
| 15 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
| 16 | `network/vpc` provides the new VPC category path | ✅ |