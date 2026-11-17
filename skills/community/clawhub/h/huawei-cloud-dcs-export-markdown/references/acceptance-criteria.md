# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Query DCS instances by region and generate a `.md` report | ✅ `--format md` (default) |
| 2 | `md` (default) / `table` / `json` output modes; `--output` atomic write (temp file + rename, parent dir auto-created) | ✅ `export_markdown.py` |
| 3 | Markdown table headers 名称/ID/引擎/版本/容量/规格/状态/连接地址/端口/可用区; missing fields render `-`; `--summary` appends a summary line | ✅ `MD_HEADERS` + `render_markdown` |
| 4 | `--region` (default `cn-north-4`) + `--name` / `--name-equal` / `--instance-id` / `--ip` / `--status` / `--tags` filters; `--page-size` automatic paging | ✅ `list_instances` loop |
| 5 | Transparent SDK fallback (`huaweicloudsdkdcs` v2) when hcloud is missing | ✅ `list_instances_via_sdk` |
| 6 | Empty list / missing AK-SK / 403-401 / bad path each get an explicit hint and never produce a broken file | ✅ Error Handling |
| 7 | Write intents (create/delete/resize/restart/flush/restore/backup ...) blocked by the guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 8 | SKILL.md / references/ (5 docs) / templates/ / tests/ complete and spec-compliant | ✅ validate-skill.sh |
| 9 | Offline unit tests with mocked hcloud all passing; existing repo tests unaffected | ✅ `python3 -m unittest discover -s tests` |
| 10 | skill-quality-cli integration (ensure_cli.sh + install_cli.sh + wrapped hcloud calls) | ✅ script-side wrapper |
| 11 | Read-only REST path provenance documented (`GET /v2/{project_id}/instances`) | ✅ verification-method.md |
| 12 | No hardcoded credentials; env vars read via whitelisted `os.environ.get` only; SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
| 13 | Local-only file generation: nothing is ever written back to the cloud | ✅ Markdown export is filesystem-only |