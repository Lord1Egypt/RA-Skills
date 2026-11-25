---
name: huawei-cloud-dcs-list
description: |
  1. List Huawei Cloud DCS (Distributed Cache Service, Redis / Memcached)
     instances in a tenant region through KooCLI (hcloud DCS ListInstances —
     read-only GET /v2/{project_id}/instances), with an automatic fallback to
     the official huaweicloudsdkdcs v2 SDK when hcloud is not installed.
  2. Default output is the compact instance-name list (名称列表, also available
     via --names-only); --table renders the full-field table
     (名称/ID/引擎/版本/容量/规格/状态/连接地址/端口/可用区), --json outputs the
     raw response array, --md / --format md prints a GitHub-flavored
     Markdown table with the same fixed ten columns as
     export-markdown 口径 (缺失字段渲染 `-`, `|` 转义为 `\|`,
     换行转空格), and --csv / --format csv prints an RFC4180 CSV table with
     the same ten columns (缺失字段为空字符串, 逗号/双引号/换行由标准 csv 模块
     转义, CRLF 行尾). --md-output <path> / --csv-output [<path>] 可把表格原子
     落盘（内容与 stdout 一致）；--csv-output 省略路径或传目录时用默认文件名
     dcs_instances_<region>_<timestamp>.csv；--csv-bom 输出 UTF-8 BOM.
  3. Supports --name (server-side fuzzy query, plus --name-equal exact match),
     --instance-id / --ip / --status / --tags filtering (all real server-side
     ListInstances query parameters), region override, optional --sort-by
     name|created (client-side ascending order: case-insensitive instance name
     or created_at, missing values last, stable), and automatic limit/offset
     paging.
  4. Explicit error hints for empty instance lists (「当前区域无 DCS 实例」),
     403 / insufficient IAM permission (「无权限访问分布式缓存服务（DCS）」), missing
     or invalid AK/SK credentials, missing project_id on the SDK fallback, and
     hcloud not installed.
  5. Built-in write-intent guard: any mutating intent (create / delete /
     update / resize / restart / flush / clear / restore / backup / freeze) or
     any operation other than ListInstances is rejected before execution —
     this skill is strictly read-only.
  6. Triggers include: "list DCS instances", "DCS instance list",
     "查询 DCS 实例列表", "DCS 实例列表", "Redis 实例列表", "缓存实例列表",
     "查询缓存实例", "DCS inventory", "list cache instances", "华为云 DCS 列表",
     "DCS 实例 Markdown 表格", "导出 DCS 实例 Markdown", "DCS 实例表格输出",
     "DCS 实例 CSV", "导出 DCS CSV", "DCS CSV 输出", "导出 DCS 实例 CSV",
     "DCS csv export".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes
     (names / table / json / md / csv), filters, paging, error scenarios, SDK
     fallback, Markdown/CSV escaping + atomic file writing (incl. BOM), and
     the write-intent guard.
tags: [huawei-cloud, dcs, database, readonly, koo-cli]
---

# Huawei Cloud DCS Instance List

## Overview

Query the DCS (Distributed Cache Service, Redis / Memcached) instance list of
a tenant region through KooCLI `hcloud DCS ListInstances` (official read-only
`GET /v2/{project_id}/instances`, verified in the `huaweicloudsdkdcs` v2
client `_list_instances_http_info` metadata — `resource_path:
"/v2/{project_id}/instances"`, `method: "GET"`). The skill is aimed at DCS
inventory inspection, daily operations patrol, and as a pre-query step for
other DCS skills that need an `instance_id`.

Architecture:

```text
agent → python3 scripts/list_dcs.py → hcloud DCS ListInstances --cli-region=<region>
      → Huawei Cloud DCS OpenAPI (dcs.<region>.myhuaweicloud.com) → parsed JSON → names list / table / --json / markdown (+ optional --md-output file) / csv (+ optional --csv-output file, --csv-bom)

(hcloud binary missing) → fallback: huaweicloudsdkdcs v2 DcsClient.list_instances
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListInstances`
  (GET). A write-intent guard scans user arguments and validates the
  operation name; mutating intents (create / delete / update / resize /
  restart / flush / clear / restore / backup / freeze ...) are rejected with
  an explicit message before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when
  the hcloud binary is absent, the script falls back to the official
  `huaweicloudsdkdcs` v2 SDK (`DcsClient.list_instances`). Credentials are
  always read by the CLI profile / whitelisted SDK environment variables —
  never handled by the script.
- **Name list by default** — the default output mode is the compact
  instance-name list (「DCS 实例名称列表」); `--table` renders the full-field
  table, `--json` the raw response array, and `--md` / `--format md` a
  Markdown table.
- **Markdown output shares the export contract** — `--md` prints a fixed
  ten-column GitHub-flavored table (名称/ID/引擎/版本/容量/规格/状态/连接地址/
  端口/可用区) identical to the DCS export-markdown 口径; missing fields
  render `-`, `|` is escaped as `\|` and line breaks collapse to a space, so a
  value can never break the table. `--md-output <path>` additionally writes
  exactly that text through a temp file + atomic rename (失败非零退出、不留
  残缺文件); an empty list prints only the friendly hint — no header, no file.
- **CSV output is RFC4180** — `--csv` / `--format csv` prints the same ten
  columns (名称/ID/引擎/版本/容量/规格/状态/连接地址/端口/可用区) with
  missing fields as an empty string; commas, double quotes and line breaks
  are quoted by the standard `csv` module (QUOTE_MINIMAL, CRLF line endings),
  never hand-escaped. `--csv-output [<path>]` writes exactly the stdout bytes
  atomically (temp file + fsync + rename, parent dirs created); without a path
  (or when pointing at a directory) the default name
  `dcs_instances_<region>_<timestamp>.csv` is used. `--csv-bom` prepends the
  UTF-8 BOM (`EF BB BF`) to both stdout and the file for spreadsheet tools.
  `--csv` is a standalone mode: combining it with `--md` / `--json` /
  `--table` / `--names-only` / a different `--format` exits `1`.
  `--csv-output` / `--csv-bom` outside CSV mode also exit `1`.
- **Server-side filters & automatic paging** — `--name` / `--instance_id` /
  `--ip` / `--status` / `--tags` are real ListInstances query parameters
  (verified against `hcloud DCS ListInstances --help`); paging uses
  `--limit` (1~1000) + `--offset` and is fetched automatically until
  `instance_num` is reached.
- **Optional client-side ordering** — `--sort-by name` orders the fully
  paged (and locally filtered) result by instance name, case-insensitive
  (missing name falls back to `instance_id`); `--sort-by created` orders by
  `created_at` ascending (ISO8601, missing values last). Both are stable and
  applied to every output mode (names / table / json / md / csv); without
  `--sort-by` the API order is kept unchanged. Ordering is client-side only —
  it is never sent to the service.
- **Offline-testable** — every code path (filters, paging, error
  classification, guard, SDK fallback) is covered by unit tests that mock
  the hcloud subprocess.

Out of scope: every mutating DCS action (create / delete / resize / restart /
flush / clear data / restore backup / reset password / upgrade / IP exchange).
Those require a dedicated write-capable skill and explicit user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkdcs` to enable the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band
   (run the KooCLI configure command in your terminal, or set credential
   environment variables). Never paste AK/SK into chat; the script never
   reads, echoes, or stores secrets itself — authentication is delegated
   entirely to the hcloud profile / SDK environment.
3. **project_id (SDK fallback only)** — the DCS REST path is
   `/v2/{project_id}/instances`; when falling back to the SDK, supply the
   project id via `--project-id` or the `HUAWEICLOUD_SDK_PROJECT_ID` /
   `HUAWEI_PROJECT_ID` environment variables. The KooCLI path resolves it
   from the profile automatically.
4. **IAM permission** — read-only `dcs:instance:list`; least-privilege
   policy in [references/iam-policies.md](references/iam-policies.md).
5. **Python 3.8+** (standard library only — argparse / json / subprocess).
6. **Outbound HTTPS** access to `dcs.cn-north-4.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`).
2. **Confirm KooCLI readiness** (optional, read-only) by listing the active
   credential profile.
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — name list (default) for a compact inventory, table
   for humans, `--json` for downstream tooling, `--md` for a pasted-into-
   ticket Markdown table (optionally persisted with `--md-output`), `--csv`
   for spreadsheets/ETL (optionally persisted with `--csv-output`, BOM with
   `--csv-bom`).
5. **Handle the empty / error cases** per the Edge Cases table below (the
   script prints an explicit hint for empty region, 403, and missing AK/SK).

## Core Commands

```bash
# Compact instance-name list (default — the core ask of this skill)
python3 scripts/list_dcs.py --region cn-north-4
python3 scripts/list_dcs.py --names-only

# Full-field table (名称/ID/引擎/容量/状态/连接地址/端口 etc.)
python3 scripts/list_dcs.py --table

# Raw JSON of every returned field
python3 scripts/list_dcs.py --json

# Markdown table (fixed 10 columns, same口径 as the DCS export-markdown 能力)
python3 scripts/list_dcs.py --md
python3 scripts/list_dcs.py --format md
python3 scripts/list_dcs.py --format table          # same as --table
python3 scripts/list_dcs.py --format names          # same as --names-only

# Markdown + atomic file write (file content == stdout table)
python3 scripts/list_dcs.py --md --md-output ./dcs_instances.md

# Markdown combined with server-side filters / paging
python3 scripts/list_dcs.py --md --status RUNNING --page-size 500
python3 scripts/list_dcs.py --format md --name-equal --name cache-demo-01

# CSV table (fixed 10 columns, RFC4180, missing fields as empty strings)
python3 scripts/list_dcs.py --csv
python3 scripts/list_dcs.py --format csv

# CSV + atomic file write (content == stdout bytes); default name when no path
python3 scripts/list_dcs.py --csv --csv-output ./dcs_instances.csv
python3 scripts/list_dcs.py --csv --csv-output ./exports/     # dcs_instances_<region>_<timestamp>.csv
python3 scripts/list_dcs.py --csv --csv-output                # same default, current dir
python3 scripts/list_dcs.py --csv --csv-bom --csv-output ./dcs_instances.csv   # UTF-8 BOM

# Filter by instance name (server-side fuzzy query parameter)
python3 scripts/list_dcs.py --name cache-demo
python3 scripts/list_dcs.py --name-equal --name cache-demo-01   # exact match

# Filter by exact instance ID / connection IP / status / tags
python3 scripts/list_dcs.py --instance-id 55f47f3d-...
python3 scripts/list_dcs.py --ip 192.168.0.10
python3 scripts/list_dcs.py --status RUNNING
python3 scripts/list_dcs.py --tags env=prod

# Optional client-side ordering (ascending, stable): instance name / created_at
python3 scripts/list_dcs.py --sort-by name
python3 scripts/list_dcs.py --sort-by created --format md
python3 scripts/list_dcs.py --sort-by name --status RUNNING --json

# Automatic paging; page size is tunable (1~1000, default 100)
python3 scripts/list_dcs.py --page-size 500

# Combine filters
python3 scripts/list_dcs.py --region cn-south-1 --status RUNNING --names-only
```

Equivalent direct KooCLI command (the script wraps exactly this call, with
automatic offset paging):

```bash
hcloud DCS ListInstances --cli-region=cn-north-4 --limit=100 --offset=0
hcloud DCS ListInstances --cli-region=cn-north-4 --name=cache-demo --status=RUNNING
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--names-only` | No | Output instance names only — **this is also the default mode** | — |
| `--table` | No | Output the full-field table (名称/ID/引擎/版本/容量/规格/状态/连接地址/端口) | — |
| `--json` | No | Output the raw instance array as JSON | — |
| `--md` | No | Output a GitHub-flavored Markdown table with the fixed 10 columns of the DCS export-markdown 口径 (missing fields `-`) | — |
| `--csv` | No | Output an RFC4180 CSV table with the same fixed 10 columns (missing fields empty; commas/quotes/newlines quoted; CRLF); equivalent to `--format csv` | — |
| `--format` | No | Output format selector: `names` (default) / `table` / `json` / `md` / `csv` | `md` |
| `--md-output` | No | md mode only: atomically write the table to this `.md` path (content identical to stdout; parent dirs created; failure exits non-zero and leaves no partial file) | `./dcs_instances.md` |
| `--csv-output` | No | csv mode only: atomically write the CSV to this path (content identical to stdout bytes; parent dirs created; failure exits non-zero and leaves no partial file). Omit the path or pass a directory to use `dcs_instances_<region>_<timestamp>.csv` | `./dcs_instances.csv` |
| `--csv-bom` | No | csv mode only: prepend the UTF-8 BOM (`EF BB BF`) to stdout and the written file | — |
| `--name` | No | Filter by instance name — real server-side query parameter (fuzzy) | `cache-demo` |
| `--name-equal` | No | Exact-match switch: drops the fuzzy server param and filters locally, case-insensitive | used with `--name` |
| `--instance-id` | No | Filter by exact instance ID — real server-side query parameter | `55f47f3d-...` |
| `--ip` | No | Filter by connection IP address — real server-side query parameter | `192.168.0.10` |
| `--status` | No | Filter by instance state — real server-side query parameter (`RUNNING` / `ERROR` / ...) | `RUNNING` |
| `--tags` | No | Filter by instance tags — real server-side query parameter (`key1=value1,key2=value2`) | `env=prod` |
| `--sort-by` | No | Client-side ascending order for all output modes: `name` (case-insensitive instance name, missing name falls back to id) / `created` (ISO8601 `created_at`, missing last); stable, never sent to the service; omitted → API order | `name` |
| `--page-size` | No | Page size for ListInstances (default 100, range 1–1000; pages are fetched automatically) | `500` |
| `--project-id` | No | Project ID (needed by the SDK fallback path for `/v2/{project_id}/instances`) | `05f...` |
| `--operation` | No | hcloud DCS operation name; only `ListInstances` is allowed | `ListInstances` |

Output-mode precedence (backwards compatible): `--json` → `--names-only`
(default) → `--table` → `--md` → `--csv` → `--format` value. Without any mode
flag the script prints the instance-name list; `--json` wins over everything,
`--table` requires the full-field table, `--md` / `--format md` produce the
identical Markdown table (`--format md` and `--md` are byte-for-byte the same
output), and `--csv` / `--format csv` produce the identical CSV table
(`--format csv` and `--csv` are byte-for-byte the same output).
`--md-output` is only accepted in Markdown mode and `--csv-output` /
`--csv-bom` only in CSV mode — with any other mode the script exits `1` with
an explicit hint. `--csv` is standalone: combining it with `--md`, `--json`,
`--table`, `--names-only`, or a different `--format` value exits `1` with an
explicit combination error.

## Write-Intent Guard

- The script scans all user arguments plus the `--operation` value for
  mutating vocabulary (`create`, `delete`, `update`, `modify`, `resize`,
  `restart`, `reboot`, `flush`, `clear`, `restore`, `backup`, `freeze`,
  `unfreeze`, `release`, and DCS operation names such as `CreateInstance`,
  `BatchDeleteInstances`, `DeleteSingleInstance`, `ResizeInstance`,
  `RestartOrFlushInstances`, `UpdateInstance`, `ResetInstancePassword`).
- The local `--md-output` / `--csv-output` paths are filesystem targets, not
  DCS operations, so those values are excluded from the scan
  (`--md-output /tmp/dcs-backup.md`, `--csv-output /tmp/dcs-backup.csv` are
  allowed) — every other argument is still checked.
- Any hit raises `GuardError`, prints
  `[错误] 检测到写操作意图 ... 已被守卫拦截`, and exits with code 1 **before**
  a single hcloud command is executed.
- Only `hcloud DCS ListInstances` (GET) — or the SDK `list_instances` call
  in the fallback path — is ever constructed by `build_command()`; there is
  no code path that can issue a mutating DCS API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `DCS`.
- **Operation name** — PascalCase: `ListInstances`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete DCS call).
- **Simple parameter** — `--key=value`, e.g. `--name=cache-demo`,
  `--instance_id=<id>`, `--ip=192.168.0.10`, `--status=RUNNING`,
  `--tags=env=prod`. All of these are real server-side ListInstances query
  parameters (verified against the `huaweicloudsdkdcs` v2
  `ListInstancesRequest` model).
- **Paging** — `--limit` (integer, 1~1000; KooCLI defaults to 10 per page
  when unset) + `--offset` (integer, ≥ 0); the script fetches pages
  automatically until the response `instance_num` total is reached.
- **REST path (official SDK `_http_info`)** —
  `GET /v2/{project_id}/instances` (`huaweicloudsdkdcs` v2
  `_list_instances_http_info`); the project_id is resolved by KooCLI from
  the credential profile.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty instance list | Exit 0, prints `当前区域（<x>）无 DCS 实例` (+ active filters); in md/csv mode no header row and no file is written |
| 403 / insufficient IAM permission | Exit 1, `无权限访问分布式缓存服务（DCS），请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| Missing project_id (SDK fallback) | Exit 1, hint to pass `--project-id` or set the project-id env var |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkdcs` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| DCS API error body returned with exit code 0 (e.g. `DCS.4062` invalid parameter) | Exit 1, `DCS API 错误 <error_code>: <error_msg>` — never reported as unparseable output (a diagnostic table appended after the JSON is ignored) |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud DCS ListInstances --help` |
| `--page-size` out of range (not 1~1000) | Exit 1, explicit range error before any call |
| `--sort-by` value not `name` / `created` | Exit 1, explicit `--sort-by 取值非法` hint listing `name` / `created` (the value is exempt from the write-intent scan, so `created` is not mistaken for `create`) |
| `--md-output` given outside md mode | Exit 1, explicit hint that `--md-output` requires `--md` / `--format md` |
| `--md-output` write failure (permissions / disk) | Exit 1, `[错误] Markdown 文件写入失败…，未留下残缺文件`; no partial target file, temp file removed |
| `--csv-output` / `--csv-bom` given outside csv mode | Exit 1, explicit hint that they require `--csv` / `--format csv` |
| `--csv` combined with `--md` / `--json` / `--table` / `--names-only` / a different `--format` | Exit 1, explicit `--csv 不能与 … 组合使用` error before any call |
| `--csv-output` write failure (permissions / disk) | Exit 1, `[错误] CSV 文件写入失败…，未留下残缺文件`; no partial target file, temp file removed |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Non-`RUNNING` instances (ERROR / FROZEN / ...) | Reported with their state, not treated as failure |
| `--name` | Forwarded as the real fuzzy server-side query parameter; `--name-equal` switches to exact local matching (case-insensitive) |
| `--instance-id` / `--ip` / `--status` / `--tags` filters | Forwarded as real server-side query parameters (verified API params) |
| `--sort-by` ordering | Applied client-side after full paging + `--name-equal` filtering and before every output branch, so names/table/json/md/csv (including `--json`) share the same order; stable for equal keys; missing `name` falls back to id, missing `created_at` goes last |
| Large instance count | Automatic `limit`/`offset` paging driven by `instance_num` (max 100 pages) |
| Extra response fields | Table columns are built from the union of returned fields — new fields appear automatically |
| Field missing on an instance | Rendered as `-` in the table/md mode and as an empty field in csv mode |
| Value containing a pipe character / line breaks (md mode) | Pipe escaped as `\|`; line breaks collapse to a single space — the table can never be broken by data |
| Value containing comma / double quote / line break / Chinese (csv mode) | Passed through unmodified; `csv.writer(QUOTE_MINIMAL)` quotes per RFC4180 (double quotes doubled), CRLF row endings |
| Empty list in md/csv mode with `--md-output` / `--csv-output` | Friendly hint only; no header, no separator, and no file at the target path (an existing file is left untouched) |
| `--csv-output` without a path or pointing at a directory | Default file `dcs_instances_<region>_<timestamp>.csv` (UTC timestamp) |
| `--csv-bom` | One UTF-8 BOM (`EF BB BF`) at the start of stdout and the file; file bytes equal stdout bytes |
| `az_codes` / `tags` lists | Flattened into comma-joined cells for the table |
| Instance without a name | The name list falls back to `instance_id` |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkdcs` list_instances, same output modes |
| User asks to create/delete/resize/flush | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no
network):

```bash
python3 -m unittest discover -s tests -v
```

`templates/test-vars.json` carries the live read-only smoke cases (three
`hcloud DCS ListInstances` calls — list / name filter / status filter — all
`GET`); the smoke runner only allowlists `hcloud`/`curl`, so every script-level
output mode is covered by the offline tests above instead.

Coverage: write-intent guard (read passes / create / batch delete / resize /
restart / flush / clear / restore / backup / freeze / normalized variants /
operation whitelist / `--md-output` path exemption), command construction (real
server-side filters forwarded; paging params; no write flags ever), JSON
extraction, failure classification (missing AK/SK, 403, generic,
`[USE_ERROR]` with rc=0), offset paging (instance_num-driven / full-page
fallback / empty), SDK fallback (env credentials, alternative prefixes,
missing credentials, missing project id, pagination, filters; request
construction matches the real `ListInstancesRequest` signature), rendering
(table with engine/capacity/status/ip/port/az fields / names / fallbacks),
Markdown mode (fixed 10-column header + separator, column order, `-` for
missing fields, pipe/newline escaping, `--md` vs `--format md` equivalence,
filters/paging combination, empty list → no header and no file, `--sort-by`
name/created across all output modes + cross-page ordering + stable ties +
missing-field placement + invalid value + guard exemption, atomic
`--md-output` write + write-failure cleanup, `--md-output` rejected outside md
mode, mode precedence), CSV mode (fixed 10-column header + CRLF, empty string
for missing fields, RFC4180 comma/quote/newline/Chinese escaping, `--csv` vs
`--format csv` equivalence, filters/sort/paging combination, empty list → no
header and no file, `--csv-output` identical-to-stdout + parent-dir creation +
default file name (path omitted / directory) + write-failure cleanup,
`--csv-bom` first bytes `EF BB BF` in stdout and file, `--csv-output` /
`--csv-bom` rejected outside csv mode, `--csv` illegal combinations with
`--md`/`--json`/`--table`/`--names-only`/`--format`, `--csv-output` path
exemption in the write-intent guard), and all `main()` output modes including
default names list, empty, filter, exact-name and error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
| [references/read-only-guard.md](references/read-only-guard.md) | Read-only guard layers, exemptions and error behavior |
| [references/output-formats.md](references/output-formats.md) | Output modes, precedence, Markdown/CSV contracts and file output |
