# Acceptance Criteria

| # | Criterion | Status |
| - | --------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | ListVpcs full-field table output incl. 名称/ID/cidr/status 及其余字段 | ✅ `render_table` + `normalize_vpc` |
| 4 | `--json` raw output mode (VPC and peering) | ✅ |
| 5 | `--names-only` output mode | ✅ |
| 6 | `--id` / `--enterprise-project-id` filters working (real server-side query params, `vpc` only; `--id` emitted as v3 array form `--id.1=<vpc-id>`) | ✅ `build_command` |
| 7 | Empty VPC list explicit hint 「当前区域无虚拟私有云（VPC）」(exit 0) | ✅ |
| 8 | 403 explicit hint 「无权限访问虚拟私有云（VPC），请检查 IAM 权限」(exit 1) | ✅ `AuthError` |
| 9 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 10 | Missing project_id (SDK fallback) explicit hint (exit 1) | ✅ `resolve_project_id` |
| 11 | No write API call exists in code; write intents blocked by guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 12 | SDK fallback (`huaweicloudsdkvpc`) when hcloud is missing (VPC and peering) | ✅ `list_vpcs_via_sdk` / `list_peerings_via_sdk` |
| 13 | Offline unit tests with mocked hcloud, all passing | ✅ all passing |
| 14 | Read-only REST path provenance documented | ✅ verification-method.md |
| 15 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
| 16 | `network/vpc` provides the new VPC category path | ✅ |
| 17 | `--resource peering` outputs 名称/本地 VPC/对端 VPC/状态 four columns from ListVpcPeerings | ✅ `normalize_peering` / `render_peering_table` |
| 18 | Empty peering list explicit hint 「当前区域无对等连接（VPC Peering）」(exit 0) | ✅ |
| 19 | Default `vpc` behavior, output and exit codes unchanged | ✅ regression tests |
| 20 | Peering write operations (create/accept/reject/delete) blocked by the guard | ✅ per-resource operation whitelist |
| 21 | `--format {table,json,names,md}` (default `table`), legacy `--json` / `--names-only` kept | ✅ `main` |
| 22 | `--format md` writes a valid 8-column Markdown table, VPC 名称 first (`vpc` only) | ✅ `render_markdown` / `normalized_row` |
| 23 | Empty / filtered-empty list still writes a header-only `.md` and exits 0 | ✅ |
| 24 | Default name `vpc_list_<region>_<timestamp>.md`, parent dir auto-created, temp file + atomic rename | ✅ `default_output_path` / `export_markdown` |
| 25 | `--output` / `--format` values excluded from the write-intent guard; write intents still blocked | ✅ `guard_text_from_argv` |
| 26 | Markdown contract identical to huawei-cloud-vpc-export-markdown (locked by test) | ✅ `test_contract_matches_export_markdown` |