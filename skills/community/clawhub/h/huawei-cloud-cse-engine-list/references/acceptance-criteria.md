# Acceptance Criteria

| # | Criterion | Status |
| - | --------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | Read-only CSE engine list via `hcloud CSE ListEngines` (GET `/v2/{project_id}/enginemgr/engines`) | ✅ `build_command` |
| 4 | Engine fields: name / ID / type / version / status / flavor / instance counts / creation time / region | ✅ `normalize_engine` |
| 5 | Concise (default), `--table` full-field and `--json` output modes | ✅ `main` |
| 6 | `--type` ALL/CSE/Nacos/MicroGateway forwarded server-side | ✅ `build_command` |
| 7 | `--name` client-side exact filter; `--fuzzy` substring filter | ✅ `filter_by_name` |
| 8 | `--region` override (default cn-north-4) and optional `--project-id` | ✅ |
| 9 | `total`-driven paging to fetch the full list (full-page fallback) | ✅ `_collect` / `_has_more` |
| 10 | Empty-list explicit hint 「未找到微服务引擎」(exit 0) | ✅ |
| 11 | 403 explicit hint 「请检查 IAM 权限」(exit 1) | ✅ `AuthError` |
| 12 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 13 | `[USE_ERROR]` parameter error hint (exit 1, even rc=0) | ✅ `classify_hcloud_failure` |
| 14 | Network error hint, no traceback (exit 1) | ✅ `ApiError` |
| 15 | No write API call exists in code; write intents blocked before execution (exit 1) | ✅ `guard_write_intent` / `guard_operation` |
| 16 | SDK fallback to official `huaweicloudsdkcse` when hcloud is missing | ✅ `list_engines_via_sdk` |
| 17 | Offline unit tests with mocked hcloud + fake SDK, all passing | ✅ 61 tests |
| 18 | Service / operation / parameters / REST path verified against live KooCLI + SDK metadata | ✅ verification-method.md |
| 19 | Script never writes files and only calls ListEngines | ✅ |
| 20 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |