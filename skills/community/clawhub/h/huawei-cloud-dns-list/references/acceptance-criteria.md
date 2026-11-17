# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | List zones (public/private) and record sets full-field table output incl. 域名/ID/类型/状态/记录集数/邮箱/TTL | ✅ `render_table` |
| 4 | `--json` raw output mode | ✅ |
| 5 | `--names-only` output mode | ✅ |
| 6 | `--type public\|private` / `--recordsets` / `--id` / `--name` / `--record-type` filters working (real server-side query params) | ✅ `build_command` / `resolve_operation` |
| 7 | Empty-list explicit hint 「当前区域无 DNS 域名 / 记录集」(exit 0) | ✅ |
| 8 | 403 explicit hint 「无权限访问云解析服务（DNS），请检查 IAM 权限」(exit 1) | ✅ `AuthError` |
| 9 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 10 | Missing project_id (SDK fallback) explicit hint (exit 1) | ✅ `resolve_project_id` |
| 11 | No write API call exists in code; write intents blocked by guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 12 | SDK fallback (`huaweicloudsdkdns` v2) when hcloud is missing | ✅ `list_dns_via_sdk` |
| 13 | CLI / SDK / REST three-level fallback documented (KooCLI → SDK → documented REST paths) | ✅ SKILL.md / verification-method.md |
| 14 | Offline unit tests with mocked hcloud, all passing | ✅ `tests/test_list_dns.py` |
| 15 | Read-only REST path provenance documented | ✅ verification-method.md |
| 16 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
| 17 | `network/dns` provides the new DNS service category path | ✅ |
| 18 | `--output <path>` writes a UTF-8 Markdown file, valid table, prints absolute path | ✅ `render_markdown` / `write_markdown` |
| 19 | `-o` without a value uses the view default: `dns_zones.md` (zones) / `dns_recordsets.md` (`--recordsets`) | ✅ `resolve_output_path` |
| 20 | Export columns equal the default table (shared `_table_columns`); missing fields `-`, nested `tags` / `links` compact JSON, pipes / newlines escaped | ✅ `_table_columns` / `_md_escape` |
| 21 | `--type` / `--id` / `--name` / `--record-type` / `--page-size` filters affect the export and match the terminal table | ✅ |
| 22 | Empty result still writes a header-only valid file (exit 0) and keeps the empty-region hint | ✅ |
| 23 | Missing / unwritable directory: exit 1, `Markdown 文件写出失败（...）`, no partial or temporary file residue | ✅ `write_markdown` |
| 24 | `--output ./delete-report.md` is not blocked, while a real write intent is still rejected by the guard | ✅ `_strip_output_value` |
| 25 | `--json` / `--names-only` stdout semantics unchanged; export is only a table-view side effect | ✅ |
| 26 | Read-only semantics unchanged: only the three GET list operations are invoked | ✅ |
| 27 | API error envelope on stdout with exit code 0 (`errCode` / `externalMessage`, `error_code` / `error_msg`, `code` / `message`, nested `error`) is classified (`DNS.1802` / `not authorized` / `no identity-based policy` → `AuthError`) and exits 1, never reported as an empty list | ✅ `_payload_error` / `classify_hcloud_failure` |
| 28 | `extract_json` tolerates trailing diagnostics after the JSON body via `raw_decode` | ✅ `extract_json` |
| 29 | Error envelope with `--output` does not create an empty (header-only) Markdown file | ✅ regression test |
| 30 | `ListPrivateZones` always sends the required `--type=private` (script `--type private`, `--type private -o`, and direct hcloud example); `ListPublicZones` sends no `type` | ✅ `build_command` + regression tests |