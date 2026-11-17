# Acceptance Criteria

| # | Criterion | Status |
| - | ---------- | ------ |
| 1 | Skill structure complete: SKILL.md + scripts/ + templates/ + references/ (5 docs) | ✅ |
| 2 | Triggerable by 「查询 GaussDB 实例列表」/「GaussDB 实例列表」/「GaussDB inventory」 style prompts | ✅ description triggers |
| 3 | Default output is an aligned table with 名称/ID/状态/引擎版本/规格/存储/可用区(区域)/创建时间 etc. | ✅ `render_table` |
| 4 | Empty region prints 「当前区域（<x>）无 GaussDB 实例」 (exit 0) | ✅ |
| 5 | Region override (default `cn-north-4`) | ✅ `--region` |
| 6 | Automatic limit/offset paging driven by `total_count` (page size 1–100, default 100) | ✅ `list_instances` loop |
| 7 | `--name` server-side fuzzy filter (leading `*` added when missing) | ✅ `build_command` / `fuzzy_name` |
| 8 | `--status` local exact filter (API has no status parameter) | ✅ `filter_by_status` |
| 9 | `--json` raw instance array output | ✅ |
| 10 | `--id` / `--datastore-type` / `--type` / `--vpc-id` / `--subnet-id` real server-side filters | ✅ `build_command` |
| 11 | Uses `ListGaussMySqlInstances` (not the non-existent `ListInstances`) | ✅ `ALLOWED_OPERATION` |
| 12 | 403 explicit hint 「无权限访问 GaussDB（云数据库 GaussDB），请检查 IAM 权限」(exit 1) | ✅ `AuthError` |
| 13 | Missing AK/SK explicit hint (exit 1) | ✅ `ConfigError` |
| 14 | No write API call exists in code; write intents blocked by guard before execution | ✅ `guard_write_intent` / `guard_operation` |
| 15 | SDK fallback (`huaweicloudsdkgaussdb`) when hcloud is missing | ✅ `list_instances_via_sdk` |
| 16 | Credentials read via whitelisted `os.environ.get` only, never `os.environ` enumeration | ✅ |
| 17 | Read-only smoke cases provided in `templates/test-vars.json` (list / name filter / paging) | ✅ |
| 18 | Read-only REST path provenance documented (`GET /v3/{project_id}/instances`) | ✅ verification-method.md |
| 19 | No hardcoded credentials; SKILL.md ≤ 500 lines, files ≤ 30, size ≤ 40 MB, extension allowlist | ✅ |
| 20 | Does not duplicate the GaussDB(for openGauss) variant covered by another skill | ✅ scope note |
| 21 | Backward compatible: without export flags the output is unchanged (aligned table; `--json` raw array) | ✅ `main` / `render_table` |
| 22 | `--format md` / `-o` / `--output FILE` writes a valid Markdown table (Chinese header + separator + data rows), content matching the query result | ✅ `render_markdown` |
| 23 | Markdown columns cover 名称/实例ID/状态/引擎/引擎版本/内核版本/规格/CPU内存/存储类型/存储/私网IP/公网IP/端口/类型/区域/VPC/子网/创建时间 | ✅ `MD_COLUMNS` |
| 24 | Default file name `gaussdb_instances_<region>_<timestamp>.md`; custom path supported; parent directories created | ✅ `default_output_path` / `write_markdown` |
| 25 | Empty result exports only the table header + separator plus an explicit 「无 GaussDB 实例」 note (exit 0) | ✅ `render_markdown` |
| 26 | Write failure prints `[错误] Markdown 文件写出失败 (...)` and exits non-zero, leaving no partial/temp file | ✅ `write_markdown` (temp file + `os.replace`) |
| 27 | Markdown cells escape `\|` and collapse newlines | ✅ `_md_cell` |
| 28 | `--format md` / `--output` is mutually exclusive with `--json` / `--table` (explicit parameter error, exit 2); `--output` implies `--format md` | ✅ `main` (`parser.error`) |
| 29 | Unit tests cover export success, empty result, write failure, escaping, default name and parameter mutual exclusion | ✅ `tests/test_list_gaussdb.py` |
| 30 | SKILL.md and this acceptance-criteria document describe the Markdown export | ✅ |