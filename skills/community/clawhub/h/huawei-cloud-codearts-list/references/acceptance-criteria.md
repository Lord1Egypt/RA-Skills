# Acceptance Criteria

| # | Criterion | Status |
| - | --------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | Read-only list of all four CodeArts resources via `--resource` (projects / repos / pipelines / deploy-tasks) | ✅ `RESOURCES` routing |
| 4 | Full-field table output incl. 名称/ID/状态/项目/可见性 | ✅ `render_table` |
| 5 | `--json` raw output mode | ✅ |
| 6 | `--names-only` compact name + ID inventory | ✅ `item_summary_lines` |
| 7 | Project-scoped resources take `--project-id`; unique project auto-resolved | ✅ `resolve_project_id` |
| 8 | `--name` filter (server-side where available, client-side otherwise) | ✅ `build_command` / `filter_by_name` |
| 9 | `--status` client-side filter | ✅ `filter_by_status` |
| 10 | Automatic paging (offset/limit and page/size), no missed items | ✅ `_collect` / `_has_more` |
| 11 | Empty-list explicit hint 「无 CodeArts 资源」(exit 0) | ✅ |
| 12 | 403 explicit hint 「请检查 IAM 权限」(exit 1) | ✅ `AuthError` |
| 13 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 14 | No write API call exists in code; write intents blocked by guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 15 | SDK fallback to the matching official CodeArts SDK when hcloud is missing | ✅ `list_resource_via_sdk` |
| 16 | Offline unit tests with mocked hcloud, all passing | ✅ 78 tests |
| 17 | Service codes / operation names / REST paths verified against live KooCLI + SDK metadata | ✅ verification-method.md |
| 18 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
