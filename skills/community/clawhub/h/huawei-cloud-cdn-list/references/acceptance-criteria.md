# Acceptance Criteria

| # | Criterion | Status |
| - | --------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ + templates/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | ListDomains full-field table output incl. 域名/状态/CNAME/业务类型 | ✅ `render_table` + `normalize_domain` |
| 4 | `--json` raw output mode | ✅ |
| 5 | `--names-only` output mode | ✅ |
| 6 | `--domain-name` / `--domain-status` / `--business-type` filters working (real server-side query params) | ✅ `build_command` |
| 7 | Empty-list explicit hint 「当前区域无 CDN 加速域名」(exit 0) | ✅ |
| 8 | 403 explicit hint 「无权限访问内容分发网络（CDN），请检查 IAM 权限」(exit 1) | ✅ `AuthError` |
| 9 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 10 | No write API call exists in code; write intents blocked by guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 11 | SDK fallback (`huaweicloudsdkcdn` v1) when hcloud is missing | ✅ `list_domains_via_sdk` |
| 12 | Offline unit tests with mocked hcloud, all passing | ✅ |
| 13 | Read-only REST path provenance documented | ✅ verification-method.md |
| 14 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
| 15 | `network/cdn` provides the new CDN category path | ✅ |