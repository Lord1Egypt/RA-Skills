---
name: huawei-cloud-gaussdb-list
description: |
  1. List Huawei Cloud GaussDB (云数据库 GaussDB for MySQL) instances in a
     tenant region through KooCLI
     (`hcloud GaussDB ListGaussMySqlInstances`, the official read-only
     GET /v3/{project_id}/instances), with an automatic fallback to the
     official `huaweicloudsdkgaussdb` v3 SDK
     (`GaussDBClient.list_gauss_my_sql_instances`) when KooCLI is not installed.
  2. Default output is an aligned Chinese-header table
     (名称/实例ID/状态/引擎/引擎版本/规格/CPU内存/存储类型/存储/私网IP/公网IP/
     端口/类型/区域/VPC/子网/创建时间); `--json` prints the raw instance array;
     `--format md` / `-o FILE` exports the same fields as a Markdown table file
     (default `gaussdb_instances_<region>_<timestamp>.md`).
  3. Supports `--region` override (default cn-north-4), `--name` server-side
     fuzzy filtering (a leading `*` is added when missing), `--status`
     client-side exact filtering (the real API has no status parameter), and
     automatic `limit`/`offset` paging until the reported total is reached.
  4. Ambiguous / empty results are explained explicitly: 「当前区域（<x>）无
     GaussDB 实例」, 403 / insufficient IAM permission, missing AK/SK
     credentials, and network / API failures.
  5. Built-in write-intent guard: any mutating intent (create / delete /
     update / resize / restart / stop / backup / restore / bind / unbind ...)
     or any operation other than `ListGaussMySqlInstances` is rejected before a
     single command runs — this skill is strictly read-only.
  6. Triggers include: "查询 GaussDB 实例列表", "GaussDB 实例列表",
     "GaussDB inventory", "list GaussDB instances", "华为云 GaussDB 实例",
     "GaussDB MySQL 实例清单", "查询云数据库 GaussDB 实例", "GaussDB list".
tags: [huawei-cloud, gaussdb, database, readonly, koo-cli]
---

# Huawei Cloud GaussDB Instance List

## Overview

Query the GaussDB (云数据库 GaussDB for MySQL, the TaurusDB-compatible service)
instance list of a tenant region through KooCLI
`hcloud GaussDB ListGaussMySqlInstances` (official read-only
`GET /v3/{project_id}/instances`, verified in the `huaweicloudsdkgaussdb` v3
client `_list_gauss_my_sql_instances_http_info` metadata). The skill is aimed
at GaussDB inventory inspection, daily operations patrol, and as a pre-query
step for other GaussDB skills that need an `instance_id`.

Architecture:

```text
agent → python3 scripts/list_gaussdb.py
      → hcloud GaussDB ListGaussMySqlInstances --cli-region=<region> --limit=N --offset=O
      → Huawei Cloud GaussDB OpenAPI (gaussdb.<region>.myhuaweicloud.com)
      → parsed JSON instances → local status filter → table / --json / Markdown file

(hcloud binary missing) → fallback: huaweicloudsdkgaussdb v3 GaussDBClient.list_gauss_my_sql_instances
```

Key properties:

- **Read-only by design** — the only API ever invoked is
  `ListGaussMySqlInstances` (GET). A write-intent guard scans user arguments and
  validates the operation name; mutating intents (create / delete / update /
  resize / restart / stop / backup / restore / bind / unbind ...) are rejected
  with an explicit message before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  KooCLI binary is absent, the script falls back to the official
  `huaweicloudsdkgaussdb` v3 SDK. Credentials are always read by the CLI
  profile / whitelisted SDK environment variables — never handled by the script.
- **Table by default, JSON / Markdown on demand** — the default output is an
  aligned table with the common GaussDB fields; `--json` prints the raw instance
  array for downstream tooling; `--format md` / `-o FILE` writes the same fields
  as a Markdown table file (atomic write, pipe/newline escaping, default name
  `gaussdb_instances_<region>_<timestamp>.md`).
- **Server-side fuzzy name filter & automatic paging** — `--name` is the real
  `ListGaussMySqlInstances` query parameter; the API only performs fuzzy
  matching when the value starts with `*`, so the script adds the leading `*`
  automatically. Paging uses `--limit` (1~100) + `--offset` and is fetched
  automatically until `total_count` is reached.
- **Read-only smoke cases included** — `templates/test-vars.json` lists the
  three read-only `hcloud GaussDB ListGaussMySqlInstances` smoke cases
  (instance list / name filter / paging) used for verification.

Out of scope: every mutating GaussDB action (create / delete / specification
change / restart / backup / restore / password reset / database or user
management). The GaussDB(for openGauss) variant is covered by a separate skill
and is intentionally not duplicated here.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdkgaussdb` to enable
   the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band (run the
   KooCLI configure command in your terminal, or set credential environment
   variables). Never paste AK/SK into chat; the script never reads, echoes, or
   stores secrets itself — authentication is delegated entirely to the hcloud
   profile / SDK environment.
3. **project_id (SDK fallback only)** — the GaussDB REST path is
   `/v3/{project_id}/instances`; when falling back to the SDK, supply the
   project id via `--project-id` or the `HUAWEICLOUD_SDK_PROJECT_ID` /
   `HUAWEI_PROJECT_ID` environment variables. The KooCLI path resolves it from
   the profile automatically.
4. **IAM permission** — read-only `gaussdb:instance:list`; least-privilege
   policy in [references/iam-policies.md](references/iam-policies.md).
5. **Python 3.8+** (standard library only — argparse / json / subprocess).
6. **Outbound HTTPS** access to `gaussdb.cn-north-4.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`).
2. **Confirm KooCLI readiness** (optional, read-only) by listing the active
   credential profile.
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — table for humans, `--json` for downstream tooling.
5. **Handle the empty / error cases** per the Error Handling table below (the
   script prints an explicit hint for empty region, 403, and missing AK/SK).

## Core Commands

> In production, wrap every `hcloud` invocation with
> `skill-quality-cli run --skill-name huawei-cloud-gaussdb-list -- ` — bare
> hcloud calls are reserved for the read-only smoke runner.

```bash
# Default: full-field table of the region's GaussDB instances
python3 scripts/list_gaussdb.py --region cn-north-4

# Raw JSON array of every returned field
python3 scripts/list_gaussdb.py --json

# Server-side fuzzy name filter (leading * added automatically → *gauss-demo)
python3 scripts/list_gaussdb.py --name gauss-demo

# Client-side status filter (the API has no status parameter)
python3 scripts/list_gaussdb.py --status ACTIVE

# Combine filters, region override and a larger page size
python3 scripts/list_gaussdb.py --region cn-south-1 --name gauss --status ACTIVE --page-size 100

# Automatic paging; page size is tunable (1~100, default 100)
python3 scripts/list_gaussdb.py --page-size 50

# Export the instance list to a Markdown table file
python3 scripts/list_gaussdb.py --format md --output reports/gaussdb_instances.md
# --output alone implies --format md (default file name in the current dir)
python3 scripts/list_gaussdb.py --output gaussdb_instances.md

# Default Markdown file name: gaussdb_instances_<region>_<timestamp>.md
python3 scripts/list_gaussdb.py --format md --region cn-south-1
```

Equivalent direct KooCLI command (the script wraps exactly this call, with
automatic offset paging):

```bash
hcloud GaussDB ListGaussMySqlInstances --cli-region=cn-north-4 --limit=100 --offset=0
hcloud GaussDB ListGaussMySqlInstances --cli-region=cn-north-4 --name=*gauss-demo --limit=100 --offset=0
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--table` | No | Output the aligned table — **this is also the default mode** | — |
| `--json` | No | Output the raw instance array as JSON | — |
| `--name` | No | Filter by instance name — real server-side query parameter (fuzzy; a leading `*` is added when missing) | `gauss-demo` |
| `--status` | No | Filter by instance state — **applied locally** (the API has no status parameter; exact, case-insensitive) | `ACTIVE` |
| `--id` | No | Filter by exact instance ID — real server-side query parameter | `xxxx` |
| `--datastore-type` | No | Filter by database type — real server-side query parameter (currently only `gaussdb-mysql`) | `gaussdb-mysql` |
| `--type` | No | Filter by instance type — real server-side query parameter (currently only `Cluster`) | `Cluster` |
| `--vpc-id` | No | Filter by VPC ID — real server-side query parameter | `vpc-0001` |
| `--subnet-id` | No | Filter by subnet ID — real server-side query parameter | `subnet-0001` |
| `--page-size` | No | Page size for ListGaussMySqlInstances (default 100, range 1–100; pages are fetched automatically) | `50` |
| `--project-id` | No | Project ID (needed by the SDK fallback path for `/v3/{project_id}/instances`) | `05f...` |
| `--operation` | No | hcloud GaussDB operation name; only `ListGaussMySqlInstances` is allowed | `ListGaussMySqlInstances` |
| `--format` | No | Output format: `table` (default, aligned terminal table) or `md` (Markdown file) | `md` |
| `-o` / `--output` | No | Markdown output file path (implies `--format md`); default `gaussdb_instances_<region>_<timestamp>.md` in the current directory | `reports/gaussdb_instances.md` |

Output-mode precedence: `--json` wins over the default table mode. Without any
mode flag the script prints the aligned table. `--format md` / `--output` is
mutually exclusive with `--json` and `--table` (explicit parameter error, exit
code 2); `--output` is equivalent to `--format md`.

## Write-Intent Guard

- The script validates the `--operation` value (only the read-only
  `ListGaussMySqlInstances` is accepted) and scans the remaining arguments for
  mutating vocabulary (`create`, `delete`, `update`, `modify`, `resize`,
  `restart`, `stop`, `start`, `shutdown`, `restore`, `backup`, `bind`, `unbind`,
  `expandvolume`, `upgrade`, `downgrade`, `switchover`, `failover`, `reset
  password`, and GaussDB operation names such as `CreateGaussMySqlInstance`,
  `DeleteGaussMySqlInstance`, `ChangeGaussMySqlInstanceSpecification`,
  `RestartGaussMySqlInstance`).
- Values of read-only flags (region, filters, `--project-id`, `--page-size`,
  `--operation`) are excluded from the scan so a filter value such as
  `--status CREATING` or a region id is never mistaken for a GaussDB operation.
- Any hit raises `GuardError`, prints
  `[错误] 检测到写操作意图 ... 已被守卫拦截`, and exits with code 1 **before** a
  single hcloud command is executed.
- `build_command()` can only construct `ListGaussMySqlInstances` (GET); there is
  no code path that issues a mutating GaussDB API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `GaussDB`.
- **Operation name** — PascalCase: `ListGaussMySqlInstances`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete GaussDB call).
- **Project parameter** — `--project_id=<value>` (path parameter; emitted only
  when `--project-id` is supplied, otherwise KooCLI resolves it from the
  profile).
- **Simple parameter** — `--key=value`, e.g. `--limit=100`, `--offset=20`,
  `--name=*gauss-demo`, `--id=xxxx`, `--datastore_type=gaussdb-mysql`,
  `--type=Cluster`, `--vpc_id=...`, `--subnet_id=...`. All of these are real
  `ListGaussMySqlInstances` query parameters (verified against
  `hcloud GaussDB ListGaussMySqlInstances --help`). There is **no `--status`
  parameter**; status filtering is done by the script locally.
- **Paging** — `--limit` (integer, 1~100) + `--offset` (integer, ≥ 0); the
  script fetches pages automatically until `total_count` is reached.
- **REST path (official SDK `_http_info`)** —
  `GET /v3/{project_id}/instances`
  (`huaweicloudsdkgaussdb` v3 `_list_gauss_my_sql_instances_http_info`);
  project_id is resolved by KooCLI / the SDK from the credential profile.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty instance list | Exit 0, prints `当前区域（<x>）无 GaussDB 实例` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问 GaussDB（云数据库 GaussDB），请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| Missing project_id (SDK fallback) | Exit 1, hint to pass `--project-id` or set the project-id env var |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkgaussdb` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| GaussDB API error body returned with exit code 0 | Exit 1, `GaussDB API 错误 <error_code>: <error_msg>` — never reported as unparseable output |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud GaussDB ListGaussMySqlInstances --help` |
| `--page-size` out of range (not 1~100) | Exit 1, explicit range error before any call |
| Write intent detected | Exit 1, `GuardError` message, no command executed |
| Markdown export with empty result | Exit 0, file contains the table header + separator and an explicit 「无 GaussDB 实例」 note |
| Markdown file write failure (unwritable path / disk error) | Exit 1, `[错误] Markdown 文件写出失败 (...)`, no partial file left behind |
| `--format md` / `--output` combined with `--json` or `--table` | Exit 2, explicit parameter error `不能同时使用` |

Exit codes: `0` success / empty region; `1` config, auth, guard, API, or
Markdown write error; `2` argument error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Non-`ACTIVE` instances (FAILED / BUILDING / FROZEN / ...) | Reported with their state, not treated as failure |
| `--name` | Forwarded as the real fuzzy server-side query parameter; a leading `*` is added when missing |
| `--status` | Exact, case-insensitive local filter applied after paging |
| `--id` / `--datastore-type` / `--type` / `--vpc-id` / `--subnet-id` | Forwarded as real server-side query parameters (verified API params) |
| Large instance count | Automatic `limit`/`offset` paging driven by `total_count` (max 100 pages) |
| Nested fields (`datastore`, `volume`, `flavor_info`) | Flattened into dedicated table columns |
| Field missing on an instance | Rendered as `-` in the table |
| `private_ips` / `public_ips` lists | Flattened into comma-joined cells |
| Instance without a name | Table renders `-` for name but keeps the instance ID |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkgaussdb` list_gauss_my_sql_instances, same output modes |
| Markdown cell containing `|` or newlines | Escaped as `\|` / collapsed to spaces so the table stays valid |
| Missing `--output` directory | Parent directories are created automatically |
| Existing file at the output path | Overwritten atomically (temp file + rename; never a partial file) |
| User asks to create/delete/resize/restart | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Verification is performed on a real, read-only environment. The acceptance
cases live in `templates/test-vars.json` (three
`hcloud GaussDB ListGaussMySqlInstances` calls — instance list / fuzzy name
filter / paging — all `GET`), and the structure checks are listed in
[references/acceptance-criteria.md](references/acceptance-criteria.md).

```bash
# Read-only smoke (with a working hcloud profile)
python3 scripts/list_gaussdb.py --region cn-north-4
python3 scripts/list_gaussdb.py --json | python3 -m json.tool >/dev/null
python3 scripts/list_gaussdb.py --name gauss --status ACTIVE

# Markdown export (unit-testable offline; no cloud call for render/write paths)
python3 scripts/list_gaussdb.py --format md --output /tmp/gaussdb_instances.md
```

Expected: a table (or raw JSON array, or a Markdown file); an explicit
`当前区域（cn-north-4）无 GaussDB 实例` message on an empty region; an explicit
IAM hint on 403. Detailed method and provenance:
[references/verification-method.md](references/verification-method.md).

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill was verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |