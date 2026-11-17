# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | ListInstances full-field table output incl. 名称/ID/状态/引擎/规格/私网IP/可用区 | ✅ `render_table` + `normalize_instance` |
| 4 | `--json` raw output mode | ✅ |
| 5 | `--names-only` output mode | ✅ |
| 6 | `--status` / `--name` / `--datastore-type` / `--instance-id` filters working: `--name` / `--datastore-type` / `--instance-id` forwarded as real API params; `--status` applied client-side (API has no status param) | ✅ `build_command` + `filter_by_status` |
| 7 | Empty-list explicit hint 「当前区域无 RDS 实例」(exit 0) | ✅ |
| 8 | 403 explicit hint 「无权限访问 RDS，请检查 IAM 权限」(exit 1) | ✅ `AuthError` |
| 9 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 10 | No write API call exists in code; write intents blocked by guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 11 | SDK fallback (`huaweicloudsdkrds`) when hcloud is missing | ✅ `list_instances_via_sdk` |
| 12 | Offline unit tests with mocked hcloud, all passing | ✅ |
| 13 | Read-only REST path provenance documented | ✅ verification-method.md |
| 14 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
| 15 | Default terminal output unchanged when no export flags are passed (table / `--json` / `--names-only` / empty result) | ✅ backward-compatible tests |
| 16 | `--format {table,md}` (default `table`) and `--output <path>` (implies md); md file has title + Chinese headers + separator + one row per instance | ✅ `render_markdown` + `MD_COLUMNS` |
| 17 | `--output` accepts relative/absolute paths and auto-creates parent directories | ✅ `write_markdown` |
| 18 | Empty result with md export: table header + explicit 「无实例」note, exit 0 | ✅ |
| 19 | Write failure: explicit stderr error + non-zero exit, atomic write (no half file) | ✅ tempfile + `os.replace` |
| 20 | Markdown cells escape `|` and collapse newlines | ✅ `_md_cell` |
| 21 | `--format md` / `--output` are mutually exclusive with `--json` / `--names-only` (exit 2) | ✅ `parser.error` |
| 22 | New unit tests cover export success / empty / write failure / parameter combinations / backward compatibility; all tests pass | ✅ |
