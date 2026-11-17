# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Query the region's VPC list read-only via CLI (KooCLI `hcloud VPC ListVpcs`) or the `huaweicloudsdkvpc` v2 SDK fallback | ✅ `list_vpcs` / `list_vpcs_via_sdk` |
| 2 | Export the result to a `.md` file whose table includes a **VPC 名称** column (plus 区域 / VPC ID / 网段 / 状态 / 企业项目 ID / 描述 / 创建时间) | ✅ `MD_HEADERS` + `render_markdown` |
| 3 | `--help` documents the `--region` and `--output`/`-o` parameters | ✅ `argparse` |
| 4 | An empty VPC list outputs an empty (header-only) table and exits `0` | ✅ empty-list branch writes the header-only `.md` |
| 5 | Write intents (create/delete/update/associate/release/...) are rejected by the guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 6 | `md` (default) / `table` / `json` output modes; `--output` atomic write (temp file + rename, parent dir auto-created) | ✅ `export_markdown` |
| 7 | `--region` (default `cn-north-4`) + `--id` / `--enterprise-project-id` filters; `--page-size` automatic marker paging | ✅ `list_vpcs` loop |
| 8 | Empty list / missing AK-SK / 403 / bad path each get an explicit hint; a failed write leaves no partial file | ✅ Error Handling |
| 9 | New tests cover the Markdown output, empty result, parameter parsing and the write-intent guard | ✅ `tests/test_export_vpc_markdown.py` |
| 10 | SKILL.md / references/ (5 docs) / templates/ / tests/ complete and spec-compliant; no hardcoded credentials | ✅ validate-skill.sh |
| 11 | Local-only file generation: nothing is ever written back to the cloud | ✅ Markdown export is filesystem-only |
| 12 | Read-only REST path provenance documented (`GET /v1/{project_id}/vpcs`) | ✅ verification-method.md |