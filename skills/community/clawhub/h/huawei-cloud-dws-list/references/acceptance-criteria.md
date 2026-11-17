# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | ListClusters full-field table output incl. 名称/ID/状态/版本/规格/节点数/可用区/连接信息 | ✅ `render_table` + `normalize_cluster` |
| 4 | `--json` raw output mode | ✅ |
| 5 | `--names-only` output mode | ✅ |
| 6 | `--name` / `--status` / `--cluster-id` filters working: applied client-side (API has only `enterprise_project_id`) | ✅ `filter_clusters` |
| 7 | `--limit` / `--offset` pagination working (client-side slice) | ✅ `paginate` |
| 8 | Empty-list explicit hint 「当前区域无 DWS 集群」(exit 0) | ✅ |
| 9 | 403 explicit hint 「无权限访问 DWS，请检查 IAM 权限」(exit 1) | ✅ `AuthError` |
| 10 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 11 | No write API call exists in code; write intents blocked by guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 12 | SDK fallback (`huaweicloudsdkdws`) when hcloud is missing | ✅ `list_clusters_via_sdk` |
| 13 | Offline unit tests with mocked hcloud, all passing | ✅ |
| 14 | Read-only REST path provenance documented | ✅ verification-method.md |
| 15 | No hardcoded credentials; SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |