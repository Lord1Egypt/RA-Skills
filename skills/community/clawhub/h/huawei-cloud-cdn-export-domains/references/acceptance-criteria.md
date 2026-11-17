# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Query the CDN accelerated-domain list read-only via CLI (KooCLI `hcloud CDN ListDomains`) or the `huaweicloudsdkcdn` v1 SDK fallback | ✅ `list_domains` / `list_domains_via_sdk` |
| 2 | Export/download the result to a local file with `--output` (`csv` / `markdown` / `json`) | ✅ `export_report` |
| 3 | The exported table includes the **域名** (domain name) column plus 加速域名状态 / CNAME / 业务类型 / 服务区域 / HTTPS状态 / 企业项目 ID / 创建时间 / 修改时间 | ✅ `MD_HEADERS` + `render_markdown` + `render_csv` |
| 4 | `--help` documents the `--region`, `--format` and `--output`/`-o` parameters | ✅ `argparse` |
| 5 | An empty domain list outputs an empty (header-only) file and exits `0` | ✅ empty-list branch writes a header-only artifact |
| 6 | Write intents (create/delete/update/enable/disable/refresh/preheat/...) are rejected by the guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 7 | `--domain-name` / `--domain-status` / `--business-type` / `--service-area` / `--enterprise-project-id` filters forwarded as real server-side query parameters | ✅ `build_command` |
| 8 | Automatic `page_number` paging over the response `total` (full pull) | ✅ `list_domains` loop |
| 9 | Empty list / missing AK-SK / 403 / bad path each get an explicit hint; a failed write leaves no partial file | ✅ Error Handling |
| 10 | `--output` atomic write (temp file + rename, parent dir auto-created); `table` mode on stdout | ✅ `export_report` |
| 11 | New tests cover the export formats, empty result, filtering, paging, parameter parsing and the write-intent guard | ✅ `tests/test_export_cdn_domains.py` |
| 12 | SKILL.md / references/ (5 docs) / templates/ / tests/ complete and spec-compliant; no hardcoded credentials | ✅ validate-skill.sh |
| 13 | Local-only file generation: nothing is ever written back to the cloud | ✅ export is filesystem-only |
| 14 | Read-only REST path provenance documented (`GET /v1.0/cdn/domains`) | ✅ verification-method.md |