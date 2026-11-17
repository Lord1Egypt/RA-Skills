# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | Three views: `--view endpoint` (default) / `service` / `public` | ✅ `VIEWS` / `VIEW_TO_OPERATION` |
| 4 | Terminal endpoint list renders name / status / service name and fixed table fields (ID / 名称 / 状态 / 所属服务名 / 服务ID / 服务类型 / IP / VPC ID / 是否启用DNS / 是否启用白名单 / 创建时间 / region) | ✅ `ENDPOINT_COLUMNS` |
| 5 | Endpoint-service table: 服务ID / 名称 / 状态 / 后端类型 / 创建时间 / region; public table: 服务ID / 名称 / 服务类型 / 创建时间 | ✅ `SERVICE_COLUMNS` / `PUBLIC_COLUMNS` |
| 6 | Offset + limit paging until a short page or `total_count` | ✅ `list_vpcep` |
| 7 | SDK fallback (`huaweicloudsdkvpcep`) when hcloud is missing | ✅ `list_vpcep_via_sdk` |
| 8 | Client-side filters `--name` (exact by default) / `--fuzzy` / `--id` / `--vpc-id` / `--service-name` / `--status` | ✅ `filter_items` |
| 9 | `--json` raw response output | ✅ |
| 10 | `--format md` fixed columns, missing fields `-`, empty list header, atomic write | ✅ `render_markdown` / `write_markdown_atomic` |
| 11 | Non-available status (creating / failed / deleting / rejected) highlighted in a separate section; `--status failed` can list only abnormal endpoints | ✅ `is_non_available` / `_print_grouped` / `_print_table_grouped` |
| 12 | Empty list explicit hint, exit 0 | ✅ |
| 13 | 403 / insufficient IAM permission explicit Chinese hint, exit 1 | ✅ `AuthError` |
| 14 | Missing / invalid AK-SK explicit Chinese hint, exit 1 | ✅ `ConfigError` |
| 15 | Invalid resource ID explicit Chinese hint, exit 1, no traceback | ✅ `InvalidRequestError` |
| 16 | `[USE_ERROR]` and API error body with KooCLI exit 0 both classified, exit 1 | ✅ `classify_hcloud_failure` / `classify_payload_error` |
| 17 | Write intents (create / update / delete / batch / whitelist / accept / reject / bind / unbind) blocked before execution, exit 1 | ✅ `guard_argv` / `guard_write_intent` / `guard_operation` |
| 18 | Offline unit tests with mocked hcloud and fake SDK, all passing | ✅ `tests/test_list_vpcep.py` (92 tests) |
| 19 | Official SDK request-model / import regression tests | ✅ `TestSdkFallback.test_official_sdk_imports_resolve` |
| 20 | Read-only REST path and parameter provenance documented, no forbidden operation spellings | ✅ `verification-method.md` / SKILL.md |
| 21 | `bash -n` / `py_compile` / `json.tool` syntax checks pass | ✅ |
| 22 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, allowed extensions | ✅ |
| 23 | Existing repository tests have no regression | ✅ |
| 24 | Live three-view smoke with real credentials | ⏳ QA (dev account lacked VPCEP list permission; classified as IAM 403 and verified with mock) |
