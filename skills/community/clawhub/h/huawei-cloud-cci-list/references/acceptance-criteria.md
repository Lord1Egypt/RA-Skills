# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ + templates/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | List CCI namespaces (`ListCoreV1Namespace`) with 名称/状态/创建时间 | ✅ `normalize_item` + `render_table` |
| 4 | List CCI pods / instances (`ListCoreV1Pod*`) with 名称/命名空间/状态/Pod IP/镜像 | ✅ |
| 5 | List CCI workloads (`ListAppsV1Deployment*`) with 名称/命名空间/副本/就绪副本 | ✅ |
| 6 | `--json` raw Kubernetes-object output mode | ✅ |
| 7 | `--names-only` compact inventory mode | ✅ |
| 8 | `--region` and `--namespace` scoping; `--name` client-side filter; server-side `--label-selector` / `--field-selector` | ✅ |
| 9 | Empty-list explicit hint 「当前区域无 CCI 资源（resource=…）」(exit 0) | ✅ |
| 10 | 403 explicit hint 「无权限访问云容器实例（CCI），请检查 IAM 权限」(exit 1) | ✅ `AuthError` |
| 11 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 12 | hcloud not installed explicit hint (exit 1) | ✅ `ConfigError` |
| 13 | No mutating API call exists in code; write intents blocked by guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 14 | Automatic continue-token paging | ✅ `collect` + `next_continue_token` |
| 15 | Offline unit tests with mocked hcloud, all passing | ✅ `tests/test_list_cci.py` |
| 16 | Read-only REST path provenance documented | ✅ verification-method.md |
| 17 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
| 18 | `compute/cci` provides the Compute/CCI category path | ✅ |