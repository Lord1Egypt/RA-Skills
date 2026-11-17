---
name: huawei-cloud-ecs-export-markdown
description: |
  1. List the Huawei Cloud ECS (Elastic Cloud Server) instances of a tenant
     region through KooCLI (`hcloud ECS ListServersDetails`, the official
     read-only GET /v1/{project_id}/cloudservers/detail), with an automatic
     fallback to the official huaweicloudsdkecs v2 SDK
     (EcsClient.list_servers_details) when hcloud is not installed.
  2. Export the instance list into a well-formed local Markdown table (headers
     名称 / ID / 状态 / 规格 / vCPU / 内存 / 可用区 / 私网IP / 公网IP, missing
     fields render `-`, optional summary line) — strictly local file
     generation, nothing is ever written back to the cloud. `--output` sets the
     path (default `ecs_instances_<region>_<timestamp>.md`); the parent
     directory is created automatically and the file is written via a temp file
     + atomic rename.
  3. Three output modes: `--format md` (default) / `table` / `json`. Region
     aware: `--region` (default cn-north-4). Optional `--status` / `--name`
     server-side filters and `--page-size` (default 100); paging follows the
     reported `count`.
  4. Explicit error classification: missing AK/SK credentials (「缺少 AK/SK
     凭证」), hcloud not installed (falls back to SDK, else a clear hint),
     invalid/insufficient credentials (403 / 401 → IAM hint), KooCLI usage
     errors, and generic API/network failures. Empty instance lists produce a
     friendly hint and never a corrupt Markdown file.
  5. Built-in write-intent guard: any mutating intent (create / delete / update
     / reboot / resize / attach / detach / start / stop …) or any operation
     other than the read-only ListServersDetails is rejected before execution —
     this skill is strictly read-only.
  6. Triggers include: "查询 ECS 生成 Markdown", "ECS 实例列表导出 Markdown",
     "ecs markdown", "导出 ECS 实例为 Markdown 文件", "ECS 实例报表", "云服务器清单
     Markdown", "ECS instance list markdown", "export ECS instances to
     markdown", "ecs 报表".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, paging,
     Markdown format correctness, filters, empty lists, error classification,
     the SDK fallback, the extra-args injection position, the skill-quality-cli
     wrapper and the write-intent guard.
tags: [huawei-cloud, ecs, compute, readonly, markdown]
---

# Huawei Cloud ECS Instance List → Markdown Export

## Overview

Query the ECS instance list of a tenant region through KooCLI
`hcloud ECS ListServersDetails` (official read-only GET
`/v1/{project_id}/cloudservers/detail`, verified against both
`hcloud ECS ListServersDetails --help` — `Method: GET` — and the
`huaweicloudsdkecs` v2 client `_list_servers_details_http_info` metadata), with
a fallback to the official `huaweicloudsdkecs` v2 SDK, and export the result
into a local **Markdown** report. The skill is aimed at cloud resource
inventory, daily operations patrol, and Markdown-report style deliverables.

Architecture:

```text
agent → python3 scripts/list_ecs_export_markdown.py → skill-quality-cli run ─▶ hcloud ECS ListServersDetails --cli-region=<region> --limit=N --offset=O
      → Huawei Cloud ECS OpenAPI (regional endpoint) → parsed JSON servers → export_markdown → .md / table / json

(hcloud binary missing) → fallback: huaweicloudsdkecs v2 EcsClient.list_servers_details
(missing SDK)           → run scripts/ensure_env.py  (auto pip install)
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListServersDetails`
  (GET). A write-intent guard scans the user arguments and validates the
  operation name; mutating intents (create / delete / update / rebuild / resize
  / reboot / start / stop / attach / detach ...) are rejected with an explicit
  message before any command runs. The Markdown file is generated on the
  **local filesystem only** — no ECS write happens.
- **CLI first, SDK fallback** — KooCLI is the primary execution path (wrapped
  with `skill-quality-cli` for telemetry); when the hcloud binary is absent, the
  script falls back to the official `huaweicloudsdkecs` v2 SDK
  (`list_servers_details`). Credentials are read from the hcloud profile or the
  SDK environment — never handled by the script.
- **Well-formed Markdown** — a fixed header row (名称 / ID / 状态 / 规格 / vCPU /
  内存 / 可用区 / 私网IP / 公网IP) plus one data row per instance, with a `-`
  fallback for missing fields and an optional summary line (`--summary`). Pipe
  and newline characters inside a cell are escaped so the table never breaks.
  The report is saved via a temporary file + atomic rename, so an interrupted
  write never leaves a corrupt/partial `.md` behind.
- **No broken files** — an empty instance list, missing credentials or a
  permission failure print an explicit hint on stdout/stderr and **do not**
  produce a `.md` file.
- **Offline-testable** — every code path (paging, filters, output modes,
  Markdown format, error classification, guard, SDK fallback, quality wrapper)
  is covered by unit tests that mock the hcloud subprocess.

> **Dependency**: Quality telemetry is collected automatically via
> skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

> **Capability boundary:** this skill lists **instances only**. It does not
> manage instance lifecycle (create/delete/start/stop/reboot/resize/rebuild),
> does not export flavors/images/keypairs, and does not write the report back
> to any cloud service. Those require a separate skill and explicit user
> confirmation.

## Prerequisites

1. **Python 3.8+** with the Huawei Cloud SDK — run
   `python3 scripts/ensure_env.py` to install `huaweicloudsdkcore` and
   `huaweicloudsdkecs` automatically. The Markdown export itself needs no
   third-party package. See
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
2. **KooCLI (`hcloud`) installed** — the optional primary execution path; see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   When absent, the SDK fallback is used.
3. **Credentials configured out-of-band** — the CLI reads the active hcloud
   profile; the SDK fallback reads AK/SK from the whitelisted environment
   variables (`HUAWEI_ACCESS_KEY` / `HUAWEI_SECRET_KEY`, `HUAWEICLOUD_SDK_AK` /
   `HUAWEICLOUD_SDK_SK`, `HW_*`, ...). Never paste AK/SK into chat; the script
   never reads, echoes or stores secrets itself.
4. **IAM permission** — read-only `ecs:servers:list` (or the
   `ECSReadOnlyPolicy` system policy); least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
5. **Outbound HTTPS** access to `ecs.<region>.myhuaweicloud.com`.
6. **skill-quality-cli** — ensured by `bash scripts/ensure_cli.sh` (idempotent,
   skips if present). Upgrade with `skill-quality-cli upgrade` (no auto-upgrade).
   Disable telemetry with `SKILL_QUALITY_REPORT=0`.

## Workflow

1. **(Optional) prepare the environment** — `python3 scripts/ensure_env.py`
   installs any missing SDK dependency.
2. **Confirm the target region** (default `cn-north-4`).
3. **(Optional) confirm KooCLI readiness** (read-only) — see the Core Commands
   block for the wrapped credential check.
4. **Run the script** with the desired output mode (`--format md` for the
   report, `table` / `json` otherwise).
5. **Read the result** — for `md`, the printed path is the generated report;
   hand that file path to the user. For table/json, display the result.
6. **Handle the empty / error cases** per the Error Handling table below.

## Core Commands

> **⚠️ Mandatory quality wrapping: `scripts/list_ecs_export_markdown.py` builds every `hcloud` CLI call as `skill-quality-cli run --skill-name huawei-cloud-ecs-export-markdown -- hcloud ...` (enforced in code, not left to the agent). If `skill-quality-cli` is unavailable (run `bash scripts/ensure_cli.sh`) or `SKILL_QUALITY_REPORT=0`, the CLI path degrades to bare `hcloud` (no telemetry) — the read-only semantics and the CLI→SDK fallback are unchanged.**

```bash
# Default: query the region's ECS instances and generate a .md report in cwd
python3 scripts/list_ecs_export_markdown.py

# Specify region and an explicit output path (recommended)
python3 scripts/list_ecs_export_markdown.py --region cn-north-4 \
  --output /tmp/ecs_instances_cn-north-4.md

# Append a summary line (total instance count)
python3 scripts/list_ecs_export_markdown.py --summary

# Plain table / JSON for humans / tooling
python3 scripts/list_ecs_export_markdown.py --format table
python3 scripts/list_ecs_export_markdown.py --format json

# Server-side filters
python3 scripts/list_ecs_export_markdown.py --region cn-south-1 --status ACTIVE
python3 scripts/list_ecs_export_markdown.py --name ecs-web --page-size 50

# Read-only credential readiness check (also wrapped)
skill-quality-cli run --skill-name huawei-cloud-ecs-export-markdown -- hcloud configure list
```

Equivalent direct KooCLI command (the script wraps exactly this call, with
automatic offset paging):

```bash
skill-quality-cli run --skill-name huawei-cloud-ecs-export-markdown -- hcloud ECS ListServersDetails --cli-region=cn-north-4 --limit=100 --offset=0
skill-quality-cli run --skill-name huawei-cloud-ecs-export-markdown -- hcloud ECS ListServersDetails --cli-region=cn-north-4 --name=ecs-web --status=ACTIVE
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--format` / `-f` | No | Output mode: `md` (default) / `table` / `json` | `--format table` |
| `--output` / `-o` | No | Markdown file path (only used with `--format md`; default `ecs_instances_<region>_<timestamp>.md`) | `/tmp/report.md` |
| `--summary` | No | Append a summary line (实例数量) to the Markdown report | `--summary` |
| `--status` | No | Filter by instance status — real server-side query parameter (`ACTIVE` / `SHUTOFF` / `REBUILD` / `RESIZE` ...) | `ACTIVE` |
| `--name` | No | Filter by instance name — real server-side query parameter (fuzzy match) | `ecs-web` |
| `--page-size` | No | Page size for ListServersDetails (default 100, range 1~1000; pages are fetched automatically) | `50` |
| `--operation` | No | hcloud ECS operation name; only the read-only `ListServersDetails` is allowed | `ListServersDetails` |

Output-mode precedence: `--format` selects the mode; `--output` / `--summary`
only matter for `md`. The local `--output` path value (e.g. a file literally
named `ecs-delete-report.md`) is excluded from the write-intent guard because
it is not an ECS operation.

## Write-Intent Guard

- The script scans all user arguments (except the values of the read-only filter
  flags `--status` / `--name` / `--region` / `--page-size` and of the
  local-output/format flags `--output` / `--format`) plus the `--operation`
  value for mutating vocabulary (`create`, `delete`, `update`, `modify`,
  `rebuild`, `resize`, `reboot`, `restart`, `start`, `stop`, `attach`, `detach`,
  `migrate`, `reset`, `destroy`, `terminate`, ... and ECS operation names such
  as `CreateServers`, `DeleteServers`, `BatchStartServers`,
  `ServerAction`).
- Any hit raises `GuardError`, prints
  `[错误] 检测到写操作意图 ... 已被守卫拦截`, and exits with code 1 **before** a
  single hcloud command is executed.
- Only `hcloud ECS ListServersDetails` (GET) — or the SDK
  `list_servers_details` call in the fallback path — is ever constructed by
  `build_command()`; there is no code path that can issue a mutating ECS API
  call. Every mutating ECS action (create / delete / reboot / resize / rebuild)
  requires a dedicated skill and explicit user confirmation.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `ECS`.
- **Operation name** — PascalCase API operation: `ListServersDetails`.
- **Region parameter** — always pass `--cli-region=<region>`, e.g.
  `--cli-region=cn-north-4`.
- **Simple parameters** — `--key=value`, e.g. `--limit=100`, `--offset=0`,
  `--status=ACTIVE`, `--name=ecs-web`.
- **Paging** — `--limit` (integer, 1~1000) + `--offset` (integer ≥ 0); the
  script fetches pages automatically until the reported `count` is reached.
- **REST path (official SDK)** — `GET /v1/{project_id}/cloudservers/detail`
  (`ListServersDetails`), invoked by `huaweicloudsdkecs` v2
  `EcsClient.list_servers_details`.

## Markdown Format

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

The report starts with a `# 华为云 ECS 实例清单` heading and a one-line metadata
quote (`Region` / active filters / instance count), followed by the table. A
missing field renders as `-`. `--summary` appends a trailing line:
`**汇总**：共 <N> 个 ECS 实例（Region <region>）。`

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty instance list | Exit 0, prints `当前区域（<x>）无 ECS 实例，未生成 Markdown 文件。` — no file is produced |
| Missing AK/SK | Exit 1, `缺少 AK/SK 凭证` hint to run `hcloud configure` out-of-band (never in chat) |
| Invalid / insufficient credentials (401 / 403 / ApiGW.0301) | Exit 1, `无权限访问弹性云服务器（ECS），请检查 IAM 权限` hint; no .md is produced |
| hcloud not installed | Falls back to the SDK; if the SDK is unavailable too, exit 1 with a clear hint |
| SDK missing | Exit 1, hint to run `python3 scripts/ensure_env.py` |
| Bad `--output` path (permission / bad dir) | Exit 1, `Markdown 文件写出失败` hint; no partial file is left |
| `--page-size` out of range (not 1~1000) | Exit 1, explicit range error before any call |
| KooCLI usage error (`[USE_ERROR] ...`) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud ECS ListServersDetails --help` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty list; `1` config, auth, guard, export, or API
error (`table`/`json` modes follow the same conventions).

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Region has no instances | Friendly `无 ECS 实例，未生成 Markdown 文件` message, exit 0 |
| Many instances | Offset paging until the reported `count` is reached (or a short page) |
| Filter yields no instance | Empty message includes the active filters (`status=...`, `name=...`) |
| Field missing on an instance | Rendered as `-` in both the table and the Markdown cell |
| Cell contains `|` or a newline | Escaped (`\|`, space) so the table stays well-formed |
| Instance without a name | The table shows `-`; the report still lists the instance |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkecs` list_servers_details, same output modes |
| `--output` points to a non-existing directory | Directory is created automatically |
| `--output` path contains a guard keyword (e.g. `ecs-delete-report.md`) | Path value is excluded from the guard (local path ≠ ECS operation) |
| `--status REBUILD` | Legitimate read filter — the status value is not scanned by the guard |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| User asks to create/delete/reboot | Out of scope — blocked by the write-intent guard |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
cd skills/compute/ecs/huawei-cloud-ecs-export-markdown
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / update / reboot /
resize / attach / detach / normalized variants / operation whitelist /
filter+output value exclusion / following-flag-still-scanned), command
construction (`--cli-region` / limit / offset / status / name, no write flags),
the skill-quality-cli wrapper (wrapped / bare override / report toggle /
missing CLI), `ECS_EXPORT_MARKDOWN_HCLOUD_ARGS` injection position (appended
after the read-only argv, cannot rewrite the service/operation, guard-scanned),
JSON extraction and `servers` extraction, failure classification (missing
AK/SK, 403/401, generic, `[USE_ERROR]` with rc=0), offset paging (count / full
page / empty), SDK fallback (missing env credentials / unavailable), SDK field
remapping, normalization and table rendering, Markdown rendering (headers /
separator / data rows / `-` fallback / region+filter metadata / summary /
pipe+newline escaping), atomic export (file written / missing dir created /
bad path leaves no file / atomic rename failure leaves no temp file / default
name), and all `main()` output and error modes.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI + SDK installation, credential configuration and skill-quality-cli |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |