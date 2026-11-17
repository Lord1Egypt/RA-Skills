---
name: huawei-cloud-rds-list
description: |
  1. List Huawei Cloud RDS (cloud database) instances in a tenant region through
     KooCLI (hcloud RDS ListInstances — read-only GET /v3/{project_id}/instances),
     with an automatic fallback to the official huaweicloudsdkrds v3 SDK when
     hcloud is not installed.
  2. Four output modes: full-field table (default, every returned field including
     名称/ID/状态/引擎/规格/私网IP/可用区), --json (raw response array),
     --names-only (compact instance-name list), and optional Markdown export
     (--format md / --output <path>, Chinese-column table written to a local .md
     file for inventory/patrol/handover reports).
  3. Supports --status / --name / --datastore-type / --instance-id filtering,
     region override, and automatic offset paging. --name / --datastore-type /
     --instance-id are real ListInstances query parameters; --status is applied
     client-side (full list fetched first, then filtered locally) because the
     real RDS ListInstances API has no status parameter.
  4. Explicit error hints for empty instance lists (「当前区域无 RDS 实例」), 403 /
     insufficient IAM permission (「无权限访问 RDS，请检查 IAM 权限」), missing or
     invalid AK/SK credentials, and hcloud not installed.
  5. Built-in write-intent guard: any mutating intent (create / delete / update /
     resize / restart / stop / restore) or any operation other than ListInstances
     is rejected before execution — this skill is strictly read-only.
  6. Triggers include: "list RDS instances", "RDS instance list", "RDS 实例列表",
     "查询RDS实例", "云数据库列表", "RDS inventory", "list cloud database instances",
     "华为云RDS列表".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, filters,
     paging, error scenarios, SDK fallback, Markdown export, and the
     write-intent guard.
tags: [huawei-cloud, rds, database, readonly, koo-cli]
---

# Huawei Cloud RDS Instance List

## Overview

Query the RDS instance list of a tenant region through KooCLI
`hcloud RDS ListInstances` (official read-only GET `/v3/{project_id}/instances`,
verified in the `huaweicloudsdkrds` v3 client `_list_instances_http_info`
metadata). The skill is aimed at RDS inventory inspection, daily operations
patrol, and as a pre-query step for other RDS skills that need an `instance_id`.

Architecture:

```text
agent → python3 scripts/list_rds.py → hcloud RDS ListInstances --cli-region=<region>
      → Huawei Cloud RDS OpenAPI (regional endpoint) → parsed JSON
      → table / --json / --names-only / Markdown file (--format md / --output)

(hcloud binary missing) → fallback: huaweicloudsdkrds v3 RdsClient.list_instances
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListInstances` (GET). A
  write-intent guard scans user arguments and validates the operation name;
  mutating intents (create / delete / update / resize / restart / stop /
  restore ...) are rejected with an explicit message before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  hcloud binary is absent, the script falls back to the official
  `huaweicloudsdkrds` v3 SDK (`list_instances`). Credentials are always read by
  the CLI profile / SDK environment — never handled by the script.
- **Full-field table output** — the default table renders the union of all
  fields returned by ListInstances, with `datastore` flattened into
  engine/engineVersion and `private_ips` joined for readability.
- **Optional Markdown export** — `--format md` (or `--output <path>`, which
  implies md) writes a valid Markdown table (Chinese headers + separator +
  rows) to a local file, atomically (temp file + `os.replace`). Omitting the
  export flags keeps the existing terminal output byte-for-byte unchanged.
- **Offline-testable** — every code path (paging, filters, error
  classification, guard, SDK fallback, Markdown render/write) is covered by
  unit tests that mock the hcloud subprocess.

Out of scope: every mutating RDS action (create / delete / resize / restart /
stop / restore backup / change password / read-replica management). Those
require a dedicated write-capable skill and explicit user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkrds` to enable the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band
   (`hcloud configure` in your terminal, or credential environment variables).
   Never paste AK/SK into chat; the script never reads, echoes, or stores
   secrets itself — authentication is delegated entirely to the hcloud profile
   / SDK environment.
3. **IAM permission** — read-only `rds:instance:list`; least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess).
5. **Outbound HTTPS** access to `*.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`); every RDS call is
   region-scoped.
2. **Confirm hcloud readiness** (optional, read-only): `hcloud configure list`.
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — table for humans, `--json` for downstream tooling,
   `--names-only` for a compact inventory, `--format md` / `--output` for a
   Markdown report file (inventory / patrol / handover).
5. **Handle the empty / error cases** per the Edge Cases table below (the
   script prints an explicit hint for empty region, 403, missing AK/SK, and
   Markdown write failures).

## Core Commands

```bash
# Full-field table (default)
python3 scripts/list_rds.py --region cn-north-4

# Raw JSON of every returned field
python3 scripts/list_rds.py --json

# Compact instance-name list only
python3 scripts/list_rds.py --names-only

# Filter by instance status (client-side: full list fetched, then filtered
# locally — the RDS ListInstances API has no status query parameter)
python3 scripts/list_rds.py --status ACTIVE

# Filter by engine / name
python3 scripts/list_rds.py --datastore-type MySQL --name rds-demo

# Combine filters
python3 scripts/list_rds.py --region cn-south-1 --status ACTIVE --names-only

# Export to Markdown (explicit file path; parent directories auto-created)
python3 scripts/list_rds.py --format md --output reports/rds-cn-north-4.md

# --output alone implies --format md; omitting it uses
# rds_instances_<region>_<timestamp>.md in the current directory
python3 scripts/list_rds.py --output reports/rds.md
python3 scripts/list_rds.py --format md

# Markdown + filters (empty result still writes header + 「无实例」note, exit 0)
python3 scripts/list_rds.py --format md --status ACTIVE --output reports/active.md
```

Markdown file layout: a title (`# 华为云 RDS 实例列表 — <region>`), a metadata
line, then a Chinese-header table (`实例 ID / 名称 / 状态 / 引擎 / 版本 / 规格 /
私有 IP / 可用区 / 区域 / 创建时间`) with a `---` separator and one row per
instance. `|` in a cell is escaped as `\|` and newlines are collapsed to spaces.
Writes are atomic (temp file + `os.replace`), so a failed write never leaves a
half-written file.

Equivalent direct KooCLI command (the script wraps exactly this call, with
paging):

```bash
hcloud RDS ListInstances --cli-region=cn-north-4 --limit=100 --offset=0
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--json` | No | Output the raw instance array as JSON | — |
| `--names-only` | No | Output instance names only | — |
| `--status` | No | Filter by instance state — **applied client-side** (RDS ListInstances has no status API parameter; full list fetched, then filtered locally, case-insensitive) | `ACTIVE`, `FAILED`, `BUILDING` |
| `--name` | No | Filter by instance name | `rds-demo-01` |
| `--datastore-type` | No | Filter by engine | `MySQL`, `PostgreSQL`, `SQLServer` |
| `--instance-id` | No | Filter by exact instance ID | `rds-0001` |
| `--page-size` | No | Page size for ListInstances (default 100) | `100` |
| `--operation` | No | hcloud RDS operation name; only `ListInstances` is allowed | `ListInstances` |
| `--format` | No | Output format: `table` (default, terminal table) or `md` (Markdown file) | `md` |
| `--output` / `-o` | No | Markdown file path; **implies `--format md`**. Relative/absolute paths accepted, parent directories auto-created. Default file name `rds_instances_<region>_<timestamp>.md` in the current directory | `reports/rds.md` |

Output-mode precedence: `--names-only` → `--json` → `--format md` → table
(default). `--format md` / `--output` are **mutually exclusive** with `--json` /
`--names-only` (exit code 2 with an explicit message).

## Write-Intent Guard

- The script scans all user arguments plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `resize`, `restart`, `stop`,
  `restore`, and RDS operation names such as `CreateInstance`,
  `DeleteInstance`, `ResizeFlavor`).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed.
- Only `hcloud RDS ListInstances` (GET) — or the SDK `list_instances` call in
  the fallback path — is ever constructed by `build_command()`; there is no
  code path that can issue a mutating RDS API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `RDS`.
- **Operation name** — PascalCase: `ListInstances`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete RDS call).
- **Simple parameter** — `--key=value`, e.g. `--limit=100`,
  `--offset=20`, `--name=rds-01`, `--datastore_type=MySQL`, `--id=rds-01`.
  There is **no `--status` parameter** on the real RDS ListInstances API
  (verified via `hcloud RDS ListInstances --help`); status filtering is done
  client-side by the script, never forwarded to the CLI/API.
- **REST path (official SDK `_http_info`)** —
  `GET /v3/{project_id}/instances` (`huaweicloudsdkrds` v3
  `_list_instances_http_info`); project_id is resolved by KooCLI from the
  credential profile.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty instance list | Exit 0, prints `当前区域（<x>）无 RDS 实例` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问 RDS，请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkrds` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud RDS ListInstances --help` |
| Write intent detected | Exit 1, `GuardError` message, no command executed |
| Markdown write failure (uncreatable directory / I/O error) | Exit 1, `[错误] Markdown 文件写出失败（...）` on stderr; no partial file left behind |
| `--format md` / `--output` combined with `--json` / `--names-only` | Exit 2, explicit "不能同时使用" message, no query executed |

Exit codes: `0` success / empty region / empty Markdown export; `1` config,
auth, guard, API, or Markdown write error; `2` mutually exclusive arguments.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| `BUILDING` / `FAILED` instances | Reported with their state, not treated as failure |
| `--status` filter | Applied client-side after the full paged list is fetched (case-insensitive); the server API has no status parameter |
| Large instance count | Automatic `offset` paging (total_count aware, full-page fallback, max 100 pages) |
| Extra response fields | Table columns are built from the union of returned fields — new fields appear automatically |
| Field missing on an instance | Rendered as `-` in the table |
| Nested `datastore` / `nodes` / `private_ips` | Flattened into engine / engineVersion / availability_zone / privateIps for the table |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkrds` list_instances, same output modes |
| Empty result with `--format md` | Still writes title + header + separator + explicit `_当前区域（<x>）无 RDS 实例。_` note, exit 0 |
| Markdown cell contains `|` / newline | Pipe escaped as `\|`, newlines collapsed to spaces (table stays valid) |
| `--output` points at a nested / relative path | Parent directories created automatically; atomic temp-file write |
| `--output` path contains mutating words | Local path values are excluded from the write-intent scan (no false positive) |
| User asks to create/delete/resize | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / resize / restart
/ stop / restore / normalize variants / operation whitelist), command
construction (including "status never sent to the server"), JSON extraction,
failure classification (missing AK/SK, 403, generic, `[USE_ERROR]` with rc=0),
client-side status filtering (exact / case-insensitive / no-match / missing
field), paging (total / full-page / empty), SDK fallback (success and
unavailable; request construction matches the real `ListInstancesRequest`
signature — `status=` must raise TypeError), rendering (table with
engine/flavor/private IP fields / names / fallbacks), Markdown export
(render columns/escaping/empty note, explicit and default file names,
relative paths + parent-dir creation, atomic write, write-failure cleanup,
mutual exclusivity), and all main() output modes including empty, filter, and
error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
