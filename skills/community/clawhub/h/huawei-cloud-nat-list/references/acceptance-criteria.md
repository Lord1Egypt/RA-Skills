# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ | ✅ |
| 2 | ListNatGateways full-field table output incl. ID/名称/规格/状态/关联VPC(router_id)/创建时间 | ✅ `render_table` + PREFERRED_COLUMNS |
| 3 | `--json` raw output mode | ✅ |
| 4 | `--names-only` compact name list mode | ✅ |
| 5 | `--name` / `--spec` / `--status` / `--vpc` filters working (real server-side query params) | ✅ `build_command` |
| 6 | Empty-list explicit hint 「当前区域无公网NAT网关」(exit 0) | ✅ |
| 7 | 403 explicit hint 「无权限访问公网NAT网关，请检查 IAM 权限」(exit 1), including KooCLI API error envelopes on stdout with exit code 0 | ✅ `AuthError` / `_payload_error` |
| 8 | Missing AK/SK explicit hint (exit 1); invalid/expired credentials reported as 401, not 403 | ✅ `ConfigError` / `_sdk_auth_error` |
| 9 | Missing project_id (SDK fallback) explicit hint (exit 1) | ✅ `resolve_project_id` |
| 10 | No write API call exists in code; write intents blocked by guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 11 | SDK fallback (`huaweicloudsdknat`) when hcloud is missing | ✅ `list_nat_gateways_via_sdk` |
| 12 | Offline unit tests with mocked hcloud, all passing (79 tests) | ✅ |
| 13 | Read-only REST path provenance documented | ✅ verification-method.md |
| 14 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
| 15 | `network/nat` provides the new Network category path (sibling of network/eip) | ✅ |
