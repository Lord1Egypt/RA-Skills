# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | Default list output standardized to exactly `id` + `name` (名称), no other fields | ✅ `render_table` / `standardize_loadbalancers` |
| 3b | Markdown document generated for a list query: standardized `id` + 名称 list (Markdown table `| ID | 名称 |`); default `elb-list.md`, `--md-out <path>`, `--no-md`; `--json` never writes it | ✅ `render_markdown` / `write_markdown_file` / `emit_markdown_doc` |
| 4 | `--json` raw output mode (every returned field, preserved) | ✅ |
| 5 | `--names-only` output mode | ✅ |
| 6 | `--id` / `--name` / `--vpc-id` / `--provisioning-status` / `--operating-status` / `--enterprise-project-id` / `--vip-address` filters working (real server-side query params) | ✅ `build_command` |
| 7 | Empty-list explicit hint 「当前区域无负载均衡器（ELB）」(exit 0) | ✅ |
| 8 | 403 explicit hint 「无权限访问弹性负载均衡（ELB），请检查 IAM 权限」(exit 1) | ✅ `AuthError` |
| 9 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 10 | Missing project_id (SDK fallback) explicit hint (exit 1) | ✅ `resolve_project_id` |
| 11 | No write API call exists in code; write intents blocked by guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 12 | `--project-id` supported (SDK fallback `/v3/{project_id}/elb/loadbalancers`) | ✅ |
| 13 | SDK fallback (`huaweicloudsdkelb`) when hcloud is missing | ✅ `list_loadbalancers_via_sdk` |
| 14 | Dependency self-heal via `scripts/ensure_env.py` | ✅ |
| 15 | Offline unit tests with mocked hcloud, all passing | ✅ |
| 16 | Read-only REST path provenance documented | ✅ verification-method.md |
| 17 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
| 18 | `network/elb` provides the new Network category path | ✅ |