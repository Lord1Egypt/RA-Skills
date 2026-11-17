---
name: huawei-cloud-ecs-export-excel
description: |
  1. List the Huawei Cloud ECS (Elastic Cloud Server) instances of a tenant
     region through KooCLI (`hcloud ECS ListServersDetails`, the official
     read-only GET /v1/{project_id}/cloudservers/detail), with an automatic
     fallback to the official huaweicloudsdkecs v2 SDK
     (EcsClient.list_servers_details) when hcloud is not installed.
  2. Export the instance list into a well-formed local `.xlsx` workbook via
     openpyxl (headers 名称 / ID / 状态 / 规格 / vCPU / 内存 / 可用区 / 私网IP /
     公网IP, optional summary row) — strictly local file generation, nothing is
     ever written back to the cloud. `--output` sets the file path (default
     `ecs_instances_<region>_<timestamp>.xlsx`).
  3. Three output modes: `--format xlsx` (default) / `table` / `json`. Region
     aware: `--region` (default cn-north-4). Optional `--status` / `--name`
     server-side filters and `--page-size` (default 100); paging follows the
     reported `count`.
  4. Explicit error classification: missing AK/SK credentials (「缺少 AK/SK
     凭证」), hcloud not installed (falls back to SDK, else a clear hint),
     invalid/insufficient credentials (403 / 401 → IAM hint), KooCLI usage
     errors, and generic API/network failures. Empty instance lists produce a
     friendly hint and never a corrupt .xlsx.
  5. Built-in write-intent guard: any mutating intent (create / delete / update
     / rebuild / resize / reboot / start / stop / attach / detach …) or any
     operation other than the read-only ListServersDetails is rejected before
     execution — this skill is strictly read-only.
  6. Triggers include: "查询 ECS 生成 Excel", "ECS 实例列表导出 Excel", "ecs excel",
     "导出 ECS 实例为 Excel", "ECS 实例报表", "云服务器清单 Excel", "ECS instance list excel",
     "export ECS instances to excel", "ecs 报表".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, paging,
     xlsx format correctness, empty lists, error classification, SDK fallback,
     the extra-args injection position, and the write-intent guard.
tags: [huawei-cloud, ecs, compute, readonly, excel]
---

# Huawei Cloud ECS Instance List → Excel Export

## Overview

Query the ECS instance list of a tenant region through KooCLI
`hcloud ECS ListServersDetails` (official read-only GET
`/v1/{project_id}/cloudservers/detail`, verified in the `huaweicloudsdkecs` v2
client `_list_servers_details_http_info` metadata), with a fallback to the
official `huaweicloudsdkecs` v2 SDK, and export the result into a local
**.xlsx** workbook (openpyxl). The skill is aimed at cloud resource inventory,
daily operations patrol, and Excel-report style deliverables.

Architecture:

```text
agent → python3 scripts/list_ecs_export_excel.py → hcloud ECS ListServersDetails --cli-region=<region> --limit=N --offset=O
      → Huawei Cloud ECS OpenAPI (regional endpoint) → parsed JSON servers → export_xlsx (openpyxl) → .xlsx / table / json

(hcloud binary missing) → fallback: huaweicloudsdkecs v2 EcsClient.list_servers_details
(missing openpyxl)      → run scripts/ensure_env.py  (auto pip install)
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListServersDetails`
  (GET). A write-intent guard scans the user arguments and validates the
  operation name; mutating intents (create / delete / update / rebuild /
  resize / reboot / start / stop / attach / detach ...) are rejected with an
  explicit message before any command runs. The Excel file is generated on the
  **local filesystem only** — no ECS write happens.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  hcloud binary is absent, the script falls back to the official
  `huaweicloudsdkecs` v2 SDK (`list_servers_details`). Credentials are read from
  the hcloud profile or the SDK environment — never handled by the script.
- **Well-formed .xlsx** — a fixed header row (名称 / ID / 状态 / 规格 / vCPU /
  内存 / 可用区 / 私网IP / 公网IP) plus one data row per instance, with an
  **optional summary row** (`--summary`) showing the total instance count. The
  workbook is saved via a temporary file + atomic rename, so an interrupted
  write never leaves a corrupt/partial .xlsx behind.
- **No broken files** — an empty instance list, missing credentials or a
  permission failure print an explicit hint on stdout/stderr and **do not**
  produce a .xlsx file.
- **Offline-testable** — every code path (paging, filters, output modes, xlsx
  format, error classification, guard, SDK fallback) is covered by unit tests
  that mock the hcloud subprocess.

> **Capability boundary:** this skill lists **instances only**. It does not
> manage instance lifecycle (create/delete/start/stop/reboot/resize/rebuild),
> does not export flavors/images/keypairs, and does not write the report back
> to any cloud service. Those require a separate skill/Issue.

## Prerequisites

1. **Python 3.8+** with `openpyxl` — run
   `python3 scripts/ensure_env.py` to install it automatically (also installs
   `huaweicloudsdkcore` / `huaweicloudsdkecs` for the SDK fallback). See
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
2. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdkecs` to enable the
   SDK fallback path.
3. **KooCLI credentials configured out-of-band** — the script never reads,
   echoes, or stores AK/SK itself; authentication is delegated to the active
   KooCLI profile. Never paste AK/SK into chat.
4. **IAM permission** — read-only `ecs:servers:list` (or the
   `ECSReadOnlyPolicy` system policy); least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
5. **Outbound HTTPS** access to `ecs.<region>.myhuaweicloud.com`.

## Workflow

1. **(Optional) prepare the environment** — `python3 scripts/ensure_env.py`
   installs any missing dependency (openpyxl / SDK).
2. **Confirm the target region** (default `cn-north-4`).
3. **Confirm KooCLI readiness** (optional, read-only):
   `hcloud ECS ListServersDetails --cli-region=cn-north-4 --limit=1`.
4. **Run the script** with the desired output mode (`--format xlsx` for the
   worksheet, `table` / `json` otherwise).
5. **Read the result** — for `xlsx`, the printed path is the generated report;
   hand that file/路径 to the user. For table/json, display the result.
6. **Handle the empty / error cases** per the Error Handling table below.

## Core Commands

```bash
# Default: query the region's ECS instances and generate an .xlsx report in cwd
python3 scripts/list_ecs_export_excel.py

# Specify region and an explicit output path (recommended)
python3 scripts/list_ecs_export_excel.py --region cn-north-4 \
  --output /tmp/ecs_instances_cn-north-4.xlsx

# Append a summary row (total instance count)
python3 scripts/list_ecs_export_excel.py --summary

# Plain table / JSON for humans / tooling
python3 scripts/list_ecs_export_excel.py --format table
python3 scripts/list_ecs_export_excel.py --format json

# Server-side filters
python3 scripts/list_ecs_export_excel.py --region cn-south-1 --status ACTIVE
python3 scripts/list_ecs_export_excel.py --name ecs-web --page-size 50
```

Equivalent direct KooCLI command (the script wraps exactly this call):

```bash
hcloud ECS ListServersDetails --cli-region=cn-north-4 --limit=100 --offset=0
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--format` / `-f` | No | Output mode: `xlsx` (default) / `table` / `json` | `--format table` |
| `--output` / `-o` | No | .xlsx file path (only used with `--format xlsx`; default `ecs_instances_<region>_<timestamp>.xlsx`) | `/tmp/report.xlsx` |
| `--summary` | No | Append a summary row (实例数量 / N) to the xlsx worksheet | `--summary` |
| `--status` | No | Filter by instance status (`ACTIVE` / `SHUTOFF` / `REBUILD` ...), a real server-side ListServersDetails parameter | `ACTIVE` |
| `--name` | No | Filter by instance name (server-side, fuzzy match) | `ecs-web` |
| `--page-size` | No | Paging size (default 100); paging follows the reported `count` | `50` |
| `--operation` | No | hcloud ECS operation name; only the read-only `ListServersDetails` is allowed | `ListServersDetails` |

Output-mode precedence: `--format` selects the mode; `--output` / `--summary`
only matter for `xlsx`. The local `--output` path value (e.g. a folder literally
named `downloads`) is excluded from the write-intent guard because it is not an
ECS operation.

## Write-Intent Guard

- The script scans all user arguments (except the values of the read-only
  filter flags `--status` / `--name` / `--region` / `--page-size` and of the
  local-output flag `--output`) plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `modify`, `rebuild`, `resize`,
  `reboot`, `restart`, `start`, `stop`, `attach`, `detach`, ... and ECS
  operation names such as `CreateServers`, `DeleteServers`, `BatchStartServers`).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`,
  and exits with code 1 **before** a single hcloud command is executed.
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

## Excel Format

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

`--summary` appends a bolded footer row: `实例数量 | <N> | Region <region>`.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty instance list | Exit 0, prints `当前区域（Region <x>）无 ECS 实例，未生成 Excel 文件。` — no file is produced |
| Missing AK/SK | Exit 1, `缺少 AK/SK 凭证` hint to run `hcloud configure` out-of-band (never in chat) |
| Invalid / insufficient credentials (401 / 403 / ApiGW.0301) | Exit 1, `无权限访问 ECS，请检查 IAM 权限` hint; no xlsx is produced |
| hcloud not installed | Falls back to the SDK; if the SDK is unavailable too, exit 1 with a clear hint |
| openpyxl missing | Exit 1, `缺少依赖 openpyxl` hint to run `python3 scripts/ensure_env.py` |
| Bad `--output` path (permission / bad dir) | Exit 1, `Excel 文件写出失败` hint; no partial file is left |
| KooCLI usage error (`[USE_ERROR] ...`) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud ECS ListServersDetails --help` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty list; `1` config, auth, guard, export, or API
error (`table`/`json` modes follow the same conventions).

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Region has no instances | Friendly `无 ECS 实例，未生成 Excel 文件` message, exit 0 |
| Many instances | Offset paging until the reported `count` is reached (or a short page) |
| Filter yields no instance | Empty message includes the active filters (`status=...`, `name=...`) |
| Field missing on an instance | Rendered as `-` in both the table and the xlsx cell |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkecs` list_servers_details, same output modes |
| `--output` points to a non-existing directory | Directory is created automatically |
| `--output` path contains a guard keyword (e.g. `downloads/`) | Path value is excluded from the guard (local path ≠ ECS operation) |
| `--status REBUILD` | Legitimate read filter — the status value is not scanned by the guard |
| User asks to create/delete/reboot | Out of scope — blocked by the write-intent guard |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
cd skills/compute/ecs/huawei-cloud-ecs-export-excel
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / mutating verbs /
normalized variants / operation whitelist / filter+output value exclusion /
following-flag-still-scanned), command construction (`--cli-region` / limit /
offset / status / name, no write flags), `ECS_EXPORT_EXCEL_HCLOUD_ARGS`
injection position (appended after the read-only argv, cannot rewrite the
service/operation, guard-scanned), JSON extraction and `servers` extraction,
failure classification (missing AK/SK, 403/401, generic, `[USE_ERROR]` with
rc=0), offset paging (count / full page / empty), SDK fallback (missing env
credentials / success / unavailable) and SDK field remapping, normalization and
table rendering, xlsx export (header / data rows / summary row / cell fallbacks
/ openpyxl missing / bad path / default name), and all `main()` output modes.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation, credential configuration and openpyxl setup |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |