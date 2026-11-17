# Acceptance Criteria

| # | Criterion | Status |
| - | --------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ + templates/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | Outputs the Huawei Cloud product / service catalog with the product name (名称), plus code (编码) and abbreviation (缩写) | ✅ `standardize_products` / `render_table` |
| 4 | Default table output (名称 / 编码 / 缩写) | ✅ `render_table` |
| 5 | `--json` raw output mode (every returned field, preserved) | ✅ |
| 6 | `--names-only` output mode | ✅ |
| 7 | Data source & execution method explicit and reproducible (CLI → SDK → API) | ✅ BSS `ListServiceTypes` (`GET /v2/products/service-types`); verification-method.md |
| 8 | `--name` filter forwarded server-side (`service_type_name` fuzzy match) | ✅ `build_command` |
| 9 | `--code` filter applied client-side (service type code) | ✅ `filter_by_code` |
| 10 | Empty catalog explicit hint 「未查询到华为云产品（服务）目录数据」(exit 0) | ✅ |
| 11 | 403 explicit hint 「无权限访问华为云产品目录…，请检查 IAM 权限」(exit 1) | ✅ `AuthError` |
| 12 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 13 | hcloud not installed explicit hint (exit 1) after SDK fallback also unavailable | ✅ `ConfigError` |
| 14 | No write API call exists in code; write intents blocked by guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 15 | Output only written to stdout (errors to stderr) | ✅ |
| 16 | SDK fallback (`huaweicloudsdkbss`) when hcloud is missing | ✅ `list_products_via_sdk` |
| 17 | Dependency self-heal via `scripts/ensure_env.py` | ✅ |
| 18 | Offline unit tests with mocked hcloud, all passing | ✅ |
| 19 | Read-only REST path provenance documented | ✅ verification-method.md |
| 20 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |