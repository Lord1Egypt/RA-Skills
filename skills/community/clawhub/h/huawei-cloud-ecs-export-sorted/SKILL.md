---
name: huawei-cloud-ecs-export-sorted
description: |
  1. List the Huawei Cloud ECS (Elastic Cloud Server) instances of a tenant
     region through KooCLI (`hcloud ECS ListServersDetails`, the official
     read-only GET /v1/{project_id}/cloudservers/detail), with an automatic
     fallback to the official huaweicloudsdkecs v2 SDK
     (EcsClient.list_servers_details) when hcloud is not installed.
  2. Sort the fetched instances **locally** by a chosen field — name / id /
     status / flavor / vCPU / 内存 / availability_zone / created / privateIps /
     publicIps (Chinese aliases accepted) — in ascending (`--order asc`) or
     descending (`--order desc`) order. Numeric and timestamp fields compare
     natively; records with a missing/unparseable value are always placed last.
  3. Export the (optionally sorted) list into a local `.xlsx` workbook (openpyxl),
     a UTF-8-BOM `.csv`, or structured `.json`; `--format table` prints an aligned
     full-field table. `--output` sets the file path. Strictly local file
     generation — nothing is ever written back to the cloud.
  4. Region aware: `--region` (default cn-north-4); optional server-side
     `--status` / `--name` filters and `--page-size` (default 100); paging follows
     the reported `count`.
  5. Explicit error classification (missing AK/SK, invalid credentials / IAM 403,
     KooCLI usage error, unknown sort field, export failure, network) and a
     built-in write-intent guard that rejects any mutating ECS intent
     (create / delete / update / reboot / resize / start / stop / attach /
     detach …) before a single command runs — this skill is strictly read-only.
  6. Triggers include: "ECS 列表导出并排序", "ECS 实例排序导出", "按创建时间排序导出 ECS",
     "ecs sorted export", "export ECS instances sorted", "ECS 实例报表排序",
     "sort ecs instances csv", "云服务器清单排序导出".
tags: [huawei-cloud, ecs, compute, readonly, export]
---

# Huawei Cloud ECS Instance List → Sorted Export (xlsx / csv / json)

## Overview

Query the ECS instance list of a tenant region through KooCLI
`hcloud ECS ListServersDetails` (official read-only GET
`/v1/{project_id}/cloudservers/detail`), with a fallback to the official
`huaweicloudsdkecs` v2 SDK, sort the result **locally** by a chosen field
(ascending / descending), and export it into a local `.xlsx` / `.csv` / `.json`
report. The skill is aimed at cloud resource inventory, daily operations patrol,
and Excel/CSV-report style deliverables.

Sorting runs entirely on the locally fetched result set: `ListServersDetails`
has **no server-side ordering parameter**, so the sort is applied in memory after
paging completes. This keeps the query read-only and the ordering deterministic.

**Dependency**: Quality telemetry is collected automatically via skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

Architecture:

```text
agent → python3 scripts/list_ecs_export_sorted.py
      → hcloud ECS ListServersDetails --cli-region=<region> --limit=N --offset=O
      → Huawei Cloud ECS OpenAPI (regional endpoint)
      → parsed JSON servers → normalize → local sort (--sort-by / --order)
      → export_report (xlsx via openpyxl / csv) → .xlsx / .csv / .json / table

(hcloud binary missing) → fallback: huaweicloudsdkecs v2 EcsClient.list_servers_details
(missing openpyxl)      → run scripts/ensure_env.py  (auto pip install)
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListServersDetails`
  (GET). A write-intent guard scans the user arguments and validates the
  operation name; mutating intents are rejected with an explicit message before
  any command runs. Report files are generated on the **local filesystem only**.
- **Local sorting** — `--sort-by` maps a friendly field name to a normalized
  record key; `--order asc|desc` picks the direction. Numeric (`vcpus`, `ram`)
  and timestamp (`created`) fields compare natively, the rest case-insensitively
  as text. Records whose sort key is missing/unparseable are always placed last.
  With no `--sort-by`, the original query order is preserved.
- **Three export formats** — `xlsx` (default, openpyxl), `csv` (UTF-8 BOM, Excel
  friendly), `json` (normalized records for tooling); `table` for humans.
- **CLI first, SDK fallback** — KooCLI is the primary path; when the hcloud
  binary is absent the script falls back to the official `huaweicloudsdkecs` v2
  SDK (`list_servers_details`). Credentials are read from the hcloud profile or
  the SDK environment — never handled by the script.
- **No broken files** — empty lists, missing credentials or a permission failure
  print an explicit hint and **do not** produce a report file.
- **Offline-testable** — every code path (sorting, formats, paging, filters,
  error classification, guard, SDK fallback) is covered by unit tests that mock
  the hcloud subprocess.

> **Capability boundary:** this skill lists and exports **instances only**. It
> does not manage instance lifecycle (create/delete/start/stop/reboot/resize/
> rebuild), does not export flavors/images/keypairs, and does not write anything
> back to any cloud service. Those require a separate skill/Issue.

## Prerequisites

1. **Python 3.8+** with `openpyxl` — run `python3 scripts/ensure_env.py` to
   install it automatically (also installs `huaweicloudsdkcore` /
   `huaweicloudsdkecs` for the SDK fallback). See
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
2. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdkecs` for the SDK
   fallback path.
3. **KooCLI credentials configured out-of-band** — the script never reads,
   echoes, or stores AK/SK itself; authentication is delegated to the active
   KooCLI profile. Never paste AK/SK into chat.
4. **IAM permission** — read-only `ecs:servers:list` (or the `ECSReadOnlyPolicy`
   system policy); least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
5. **Outbound HTTPS** access to `ecs.<region>.myhuaweicloud.com`.
- **skill-quality-cli** — ensured by bash scripts/ensure_cli.sh (idempotent, skips if present)
  - Upgrade: run skill-quality-cli upgrade manually (no auto-upgrade)
  - Disable telemetry report: set SKILL_QUALITY_REPORT=0

## Workflow

1. **(Optional) prepare the environment** — `python3 scripts/ensure_env.py`
   installs any missing dependency (openpyxl / SDK).
2. **Confirm the target region** (default `cn-north-4`).
3. **Confirm KooCLI readiness** (optional, read-only):
   `hcloud ECS ListServersDetails --cli-region=cn-north-4 --limit=1`.
4. **Choose the sort field and direction** (`--sort-by` / `--order`); omit
   `--sort-by` to keep the original query order.
5. **Run the script** with the desired output mode (`--format xlsx` for the
   worksheet, `csv` / `json` / `table` otherwise).
6. **Read the result** — for `xlsx` / `csv`, the printed path is the generated
   report; for `table` / `json`, display the result.
7. **Handle the empty / error cases** per the Error Handling table below.

## Core Commands

> **⚠️ Mandatory: every hcloud command in this skill MUST be wrapped with skill-quality-cli run --skill-name huawei-cloud-ecs-export-sorted -- ** — bare hcloud calls are strictly forbidden.**

```bash
# Default: query the region's ECS instances and generate an .xlsx report in cwd
python3 scripts/list_ecs_export_sorted.py

# Sort by a field (ascending / descending) and export an explicit xlsx path
python3 scripts/list_ecs_export_sorted.py --region cn-north-4 \
  --sort-by created --order desc --output /tmp/ecs_sorted_cn-north-4.xlsx

# Export a CSV (UTF-8 BOM) sorted by instance name
python3 scripts/list_ecs_export_sorted.py --format csv \
  --sort-by name --order asc --output /tmp/ecs_sorted.csv

# Structured JSON sorted by vCPU (descending)
python3 scripts/list_ecs_export_sorted.py --format json \
  --sort-by vcpus --order desc

# Aligned full-field table (no file written)
python3 scripts/list_ecs_export_sorted.py --format table --sort-by status

# Server-side filters + paging size
python3 scripts/list_ecs_export_sorted.py --region cn-south-1 --status ACTIVE \
  --name ecs-web --page-size 50 --sort-by name

# Equivalent direct KooCLI query (the script wraps exactly this read-only call)
skill-quality-cli run --skill-name huawei-cloud-ecs-export-sorted -- hcloud ECS ListServersDetails --cli-region=cn-north-4 --limit=100 --offset=0
```

Supported `--sort-by` fields (Chinese aliases accepted):

| `--sort-by` | Normalized key | Comparison |
| ----------- | -------------- | ---------- |
| `name` / `名称` / `实例名` | `name` | text (case-insensitive) |
| `id` | `id` | text |
| `status` / `状态` | `status` | text |
| `flavor` / `规格` | `flavor` | text |
| `vcpus` / `vcpu` / `vCPU` | `vcpus` | numeric |
| `ram` / `memory` / `内存` | `ram` | numeric |
| `availability_zone` / `az` / `可用区` | `availability_zone` | text |
| `created` / `created_at` / `创建时间` | `created` | timestamp |
| `privateIps` / `私网IP` | `privateIps` | text |
| `publicIps` / `公网IP` | `publicIps` | text |

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--format` / `-f` | No | Output mode: `xlsx` (default) / `csv` / `json` / `table` | `--format csv` |
| `--sort-by` / `-s` | No | Local sort field (see table above); omit to keep query order | `--sort-by created` |
| `--order` | No | Sort direction: `asc` (default) / `desc` | `--order desc` |
| `--output` / `-o` | No | Report path (xlsx/csv; default `ecs_instances_<region>_<timestamp>.<ext>`) | `/tmp/report.csv` |
| `--summary` | No | Append a summary row (实例数量 / N) to the xlsx/csv report | `--summary` |
| `--status` | No | Filter by instance status (`ACTIVE` / `SHUTOFF` / `REBUILD` ...), a real server-side ListServersDetails parameter | `ACTIVE` |
| `--name` | No | Filter by instance name (server-side, fuzzy match) | `ecs-web` |
| `--page-size` | No | Paging size (default 100); paging follows the reported `count` | `50` |
| `--operation` | No | hcloud ECS operation name; only the read-only `ListServersDetails` is allowed | `ListServersDetails` |

Output-mode precedence: `--format` selects the mode; `--output` / `--summary`
only matter for `xlsx` / `csv`. Sorting is a no-op when `--sort-by` is omitted;
`--order` is only meaningful together with `--sort-by`. The local `--output` /
`--sort-by` / `--order` values are excluded from the write-intent guard because
they are not ECS operations.

## Write-Intent Guard

- The script scans all user arguments (except the values of the read-only /
  local-output flags `--region` / `--status` / `--name` / `--page-size` /
  `--sort-by` / `--order` / `--output`) plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `modify`, `rebuild`, `resize`,
  `reboot`, `restart`, `start`, `stop`, `attach`, `detach`, ... and ECS
  operation names such as `CreateServers`, `DeleteServers`, `BatchStartServers`).
- Any hit raises `GuardError`, prints
  `[错误] 检测到写操作意图 ... 已被守卫拦截`, and exits with code 1 **before** a
  single hcloud command is executed. No user confirmation is requested because
  the operation is refused outright.
- Only `hcloud ECS ListServersDetails` (read-only) — or the SDK
  `list_servers_details` call in the fallback path — is ever constructed by
  `build_command()`; there is no code path that can issue a mutating ECS API
  call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `ECS`.
- **Operation name** — PascalCase API operation: `ListServersDetails`.
- **Region** — always pass `--cli-region=<region>` (e.g. `--cli-region=cn-north-4`).
- **Simple parameters** — `--key=value`, e.g. `--limit=100`, `--offset=0`,
  `--status=ACTIVE`, `--name=ecs-web`.
- **REST path (official SDK)** — `GET /v1/{project_id}/cloudservers/detail`
  (`ListServersDetails`), invoked by `huaweicloudsdkecs` v2
  `EcsClient.list_servers_details`.
- **Sorting** — not a KooCLI/OpenAPI parameter; performed locally by the script.

## Report Format

xlsx / csv columns (fixed order):

| Column (header) | Source key | Notes |
| ---------- | ---------- | --------- |
| 名称 | `name` | Instance name |
| ID | `id` | Instance ID |
| 状态 | `status` | `ACTIVE` / `SHUTOFF` / `REBUILD` ... |
| 规格 | `flavor` | Flavor name (flattened from `flavor.name`) |
| vCPU | `vcpus` | Flavor vCPU count (flattened from `flavor.vcpus`) |
| 内存 | `ram` | Flavor memory (MB, flattened from `flavor.ram`) |
| 可用区 | `availability_zone` | From `OS-EXT-AZ:availability_zone` |
| 私网IP | `privateIps` | Fixed IPs from `addresses`, comma-joined; `-` when absent |
| 公网IP | `publicIps` | Floating IPs / `accessIPv4`, comma-joined; `-` when absent |
| 创建时间 | `created` | Instance creation timestamp (wire `created`) |

`--summary` appends a footer row: `实例数量 | <N> | Region <region>`.
`--format json` emits the normalized records (same keys as the source column).

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty instance list | Exit 0, prints `当前区域（Region <x>）无 ECS 实例，未生成报表文件。` — no file is produced |
| Missing AK/SK | Exit 1, `缺少 AK/SK 凭证` hint to run `KooCLI configure` out-of-band (never in chat) |
| Invalid / insufficient credentials (401 / 403 / ApiGW.0301) | Exit 1, `无权限访问 ECS，请检查 IAM 权限` hint; no report file is produced |
| Unknown `--sort-by` field | Exit 1, `未知的排序字段` hint listing the accepted fields (fails before querying) |
| hcloud not installed | Falls back to the SDK; if the SDK is unavailable too, exit 1 with a clear hint |
| openpyxl missing | Exit 1, `缺少依赖 openpyxl` hint to run `python3 scripts/ensure_env.py` |
| Bad `--output` path (permission / bad dir) | Exit 1, `文件写出失败` hint; no partial file is left |
| KooCLI usage error (`[USE_ERROR] ...`) | Exit 1, explicit `KooCLI 参数错误` hint pointing to `KooCLI ECS ListServersDetails --help` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty list; `1` config, auth, guard, sort, export, or
API error (`json` / `table` modes follow the same conventions).

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Region has no instances | Friendly `无 ECS 实例，未生成报表文件` message, exit 0 |
| Many instances | Offset paging until the reported `count` is reached (or a short page) |
| `--sort-by` omitted | Original query order preserved (stable, no reordering) |
| Missing / unparseable sort value | Always placed last regardless of `--order`; ties keep original order |
| Timestamp sort | ISO-8601 `created` parsed as a timestamp; unparseable values fall back to text and sort last |
| Field missing on an instance | Rendered as `-` in the table, xlsx and csv |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkecs` list_servers_details, same output modes |
| `--output` points to a non-existing directory | Directory is created automatically |
| `--output` path contains a guard keyword (e.g. `downloads/`) | Path value is excluded from the guard (local path ≠ ECS operation) |
| `--status REBUILD` | Legitimate read filter — the status value is not scanned by the guard |
| User asks to create/delete/reboot | Out of scope — blocked by the write-intent guard |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
cd skills/compute/ecs/huawei-cloud-ecs-export-sorted
python3 -m unittest discover -s tests -v
```

Functional smoke (live read-only path; needs KooCLI credentials + network):

```bash
bash scripts/test-cli-commands.sh
```

Coverage: write-intent guard (read passes / create / delete / mutating verbs /
normalized variants / operation whitelist / filter+sort+output value exclusion /
following-flag-still-scanned), command construction, `ECS_EXPORT_SORTED_HCLOUD_ARGS`
injection position, JSON extraction and `servers` extraction, failure
classification (missing AK/SK, 403/401, generic, `[USE_ERROR]` with rc=0), offset
paging, SDK fallback, normalization (flavor / AZ / IPs / created), rendering,
**local sorting** (aliases, unknown field, text / numeric / timestamp asc & desc,
invalid-values-last, stable ties, invalid order), xlsx export (header / rows /
summary / missing dir / bad path / missing openpyxl / default name), csv export
(header / rows / summary / UTF-8 BOM), and all `main()` output modes.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation, credential configuration, skill-quality-cli and openpyxl setup |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |