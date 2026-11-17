# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | Coupon-list full-field table output incl. 券ID/券码/状态/类型/面额/余额/有效期/促销计划 | ✅ `render_table` + `normalize_coupon` |
| 4 | `--json` raw output mode | ✅ |
| 5 | `--names-only` output mode | ✅ |
| 6 | `--status` / `--name` / `--coupon-id` filters working: `--coupon-id` / `--status` forwarded as real API params (status numeric 1-5 or alias); `--name` applied client-side (API has no name param) | ✅ `build_command` + `parse_status` + `filter_by_name` |
| 7 | Automatic offset paging (count-aware, page size ≤ 100) | ✅ `list_coupons` |
| 8 | Empty-list explicit hint 「当前区域无 BSS 代金券」(exit 0) | ✅ |
| 9 | 403 explicit hint 「无权限访问 BSS 代金券，请检查 IAM 权限」(exit 1) | ✅ `AuthError` |
| 10 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 11 | hcloud not installed explicit hint after SDK fallback (exit 1) | ✅ `ConfigError` |
| 12 | No write API call exists in code; write intents blocked by guard before execution (exit 1) | ✅ `guard_write_intent` / `guard_operation` |
| 13 | SDK fallback (`huaweicloudsdkbss` v2, GlobalCredentials + global endpoint) when hcloud is missing | ✅ `list_coupons_via_sdk` |
| 14 | Offline unit tests with mocked hcloud, all passing (69 tests) | ✅ |
| 15 | Read-only REST path provenance documented | ✅ verification-method.md |
| 16 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
