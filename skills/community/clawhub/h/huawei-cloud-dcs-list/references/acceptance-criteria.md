# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + tests/ + references/ (5 docs) | ✅ |
| 2 | Triggerable by 「查询 DCS 实例列表」/「Redis 实例列表」/「缓存实例列表」 style prompts | ✅ description triggers |
| 3 | Default and `--names-only` output the instance-name list | ✅ default = names mode |
| 4 | Empty region prints 「当前区域（<x>）无 DCS 实例」 (exit 0, all modes) | ✅ |
| 5 | Region override (default `cn-north-4`) | ✅ `--region` |
| 6 | Automatic limit/offset paging driven by `instance_num` (page size 1–1000, default 100) | ✅ `list_instances` loop |
| 7 | `--name` filter (real server-side query param) + `--name-equal` exact match | ✅ |
| 8 | Key fields complete in table mode: 名称/ID/引擎/版本/容量/规格/状态/连接地址/端口 | ✅ `render_table` + PREFERRED_COLUMNS |
| 9 | `--json` raw structured output | ✅ |
| 10 | `--instance-id` / `--ip` / `--status` / `--tags` filters (real server-side query params) | ✅ `build_command` |
| 11 | 403 explicit hint 「无权限访问分布式缓存服务（DCS），请检查 IAM 权限」(exit 1) | ✅ `AuthError` |
| 12 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 13 | No write API call exists in code; write intents blocked by guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 14 | SDK fallback (`huaweicloudsdkdcs`) when hcloud is missing | ✅ `list_instances_via_sdk` |
| 15 | Skillspector security gate: 0 high-severity issues; env vars read via whitelisted `os.environ.get` only, never `os.environ.items()` | ✅ verified with `skillspector scan --no-llm` |
| 16 | Offline unit tests with mocked hcloud, all passing; existing repo tests unaffected | ✅ `python3 -m unittest discover -s tests` |
| 17 | Read-only REST path provenance documented (`GET /v2/{project_id}/instances`) | ✅ verification-method.md |
| 18 | No hardcoded credentials; SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
| 19 | `--md` / `--format md` prints a valid Markdown table: header of the 10 export columns in order, separator row immediately after it | ✅ `render_markdown` |
| 20 | Markdown columns match `huawei-cloud-dcs-export-markdown` verbatim (名称/ID/引擎/版本/容量/规格/状态/连接地址/端口/可用区); missing fields render `-` | ✅ `MD_HEADERS` / `normalized_row` |
| 21 | `--format md` and `--md` produce byte-identical output | ✅ unit test |
| 22 | Markdown cell escaping: pipe characters escaped with a backslash, line breaks collapsed to a single space | ✅ `_md_escape` |
| 23 | `--md-output <path>` writes the table atomically; file content equals stdout; failure exits non-zero and leaves no partial file | ✅ `write_markdown_file` |
| 24 | md mode combines with `--name` / `--name-equal` / `--instance-id` / `--ip` / `--status` / `--tags` / `--region` / `--page-size` | ✅ unit test |
| 25 | Empty list in md mode: friendly hint only, no header, no file written | ✅ unit test |
| 26 | Default / `--table` / `--json` output remains byte-identical to before the change | ✅ `test_legacy_outputs_unchanged` |
| 27 | Write-intent guard still blocks mutating intents in md mode; the local `--md-output` path never trips it | ✅ `guard_argv` |
