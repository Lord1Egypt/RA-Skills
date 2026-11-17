# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ | ✅ |
| 2 | SKILL.md passes specification validation (`validate-skill.sh`) | ✅ |
| 3 | ListPublicips full-field table output incl. 别名/ID/公网IP/带宽/状态/绑定资源 | ✅ `render_table` + `normalize_publicip` |
| 4 | `--json` raw output mode | ✅ |
| 5 | `--names-only` output mode | ✅ |
| 6 | `--id` / `--status` / `--public-ip` filters working (real server-side query params) | ✅ `build_command` |
| 7 | Empty-list explicit hint 「当前区域无弹性公网IP（EIP）」(exit 0) | ✅ |
| 8 | 403 explicit hint 「无权限访问弹性公网IP（EIP），请检查 IAM 权限」(exit 1) | ✅ `AuthError` |
| 9 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 10 | Missing project_id (SDK fallback) explicit hint (exit 1) | ✅ `resolve_project_id` |
| 11 | No write API call exists in code; write intents blocked by guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 12 | SDK fallback (`huaweicloudsdkeip`) when hcloud is missing | ✅ `list_publicips_via_sdk` |
| 13 | Offline unit tests with mocked hcloud, all passing | ✅ |
| 14 | Read-only REST path provenance documented | ✅ verification-method.md |
| 15 | SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
| 16 | `network/eip` provides the new Network category path | ✅ |
| 17 | `--markdown` exports a `.md` report with title 「华为云 EIP 列表」, region / generated time / record count, and the full fixed-header table | ✅ `render_markdown` |
| 18 | `-o/--output <path>` writes to an explicit path (implies Markdown mode); parent directories are created automatically | ✅ `export_markdown` |
| 19 | Default filename follows `eip_list_<region>_<timestamp>.md` (aligned with the VPC/RDS export skills) | ✅ `default_output_path` |
| 20 | Missing fields render as `-`; `bandwidth` / `vnic` nested objects are flattened into the report columns | ✅ `normalize_publicip` + `_md_cell` |
| 21 | Empty result still generates a valid `.md` with a 「无数据」 note and exits 0 | ✅ |
| 22 | File is written through a temp file + atomic rename; an interrupted write leaves no partial/corrupt `.md` | ✅ |
| 23 | stdout prints the absolute output path and the record count | ✅ |
| 24 | Export flags take precedence over `--json` / `--names-only`; without export flags the previous outputs are unchanged | ✅ |
| 25 | Markdown export unit tests added (empty / default filename / parent-dir creation / atomic write / precedence) | ✅ `tests/test_list_eip.py` |