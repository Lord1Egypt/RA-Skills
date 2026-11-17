---
name: huawei-cloud-dcs-export-markdown
description: |
  1. Query the Huawei Cloud DCS (Distributed Cache Service, Redis / Memcached)
     instance list of a tenant region through KooCLI (`hcloud DCS ListInstances`,
     the official read-only GET /v2/{project_id}/instances), with an automatic
     fallback to the official huaweicloudsdkdcs v2 SDK
     (DcsClient.list_instances) when hcloud is not installed.
  2. Export the instance list into a well-formed local Markdown table (headers
     名称 / ID / 引擎 / 版本 / 容量 / 规格 / 状态 / 连接地址 / 端口 / 可用区, missing
     fields render `-`, optional summary line) — strictly local file generation,
     nothing is ever written back to the cloud. `--output` sets the path (default
     `dcs_instances_<region>_<timestamp>.md`); the parent directory is created
     automatically and the file is written via a temp file + atomic rename.
  3. Three output modes: `--format md` (default) / `table` / `json`. Region
     aware: `--region` (default cn-north-4). Optional `--name` /
     `--name-equal` / `--instance-id` / `--ip` / `--status` / `--tags`
     server-side filters and `--page-size` (default 100); paging follows the
     reported `instance_num`.
  4. Explicit error classification: missing AK/SK credentials (「缺少 AK/SK
     凭证」), hcloud not installed (falls back to SDK, else a clear hint),
     invalid/insufficient credentials (403 / 401 → IAM hint), KooCLI usage
     errors, and generic API/network failures. Empty instance lists produce a
     friendly hint and never a corrupt Markdown file.
  5. Built-in write-intent guard: any mutating intent (create / delete / update
     / resize / restart / flush / clear / restore / backup / freeze ...) or any
     operation other than the read-only ListInstances is rejected before
     execution — this skill is strictly read-only.
  6. Triggers include: "查询 DCS 生成 md", "DCS 实例列表导出 Markdown",
     "dcs markdown", "导出 DCS 实例为 Markdown 文件", "DCS 实例报表", "缓存实例列表
     Markdown", "Redis 实例 Markdown", "DCS instance list markdown",
     "export DCS instances to markdown", "dcs 报表".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, paging,
     Markdown format correctness, filters, empty lists, error classification,
     the SDK fallback, the extra-args injection position, the skill-quality-cli
     wrapper and the write-intent guard.
tags: [huawei-cloud, dcs, database, readonly, markdown]
---

# Huawei Cloud DCS Instance List → Markdown Export

## Overview

Query the DCS (Distributed Cache Service, Redis / Memcached) instance list of a
tenant region through KooCLI `hcloud DCS ListInstances` (official read-only GET
`/v2/{project_id}/instances`, verified in the `huaweicloudsdkdcs` v2 client
`_list_instances_http_info` metadata), with a fallback to the official
`huaweicloudsdkdcs` v2 SDK, and export the result into a local **Markdown**
report. The skill is aimed at cloud cache inventory, daily operations patrol,
and Markdown-report style deliverables.

Architecture:

```text
agent → python3 scripts/list_dcs_export_markdown.py → skill-quality-cli run ─▶ hcloud DCS ListInstances --cli-region=<region> --limit=N --offset=O
      → Huawei Cloud DCS OpenAPI (regional endpoint) → parsed JSON instances → export_markdown → .md / table / json

(hcloud binary missing) → fallback: huaweicloudsdkdcs v2 DcsClient.list_instances
(missing SDK)           → run scripts/ensure_env.py  (auto pip install)
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListInstances`
  (GET). A write-intent guard scans the user arguments and validates the
  operation name; mutating intents (create / delete / update / resize /
  restart / flush / clear / restore / backup / freeze ...) are rejected with an
  explicit message before any command runs. The Markdown file is generated on
  the **local filesystem only** — no DCS write happens.
- **CLI first, SDK fallback** — KooCLI is the primary execution path (wrapped
  with `skill-quality-cli` for telemetry); when the hcloud binary is absent, the
  script falls back to the official `huaweicloudsdkdcs` v2 SDK
  (`list_instances`). Credentials are read from the hcloud profile or the SDK
  environment — never handled by the script.
- **Well-formed Markdown** — a fixed header row (名称 / ID / 引擎 / 版本 / 容量 /
  规格 / 状态 / 连接地址 / 端口 / 可用区) plus one data row per instance, with a
  **`-`** fallback for missing fields and an **optional summary line**
  (`--summary`). The report is saved via a temporary file + atomic rename, so an
  interrupted write never leaves a corrupt/partial `.md` behind.
- **No broken files** — an empty instance list, missing credentials or a
  permission failure print an explicit hint on stdout/stderr and **do not**
  produce a `.md` file.
- **Offline-testable** — every code path (paging, filters, output modes,
  Markdown format, error classification, guard, SDK fallback, quality wrapper)
  is covered by unit tests that mock the hcloud subprocess.

> **Dependency**: Quality telemetry is collected automatically via skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

> **Capability boundary:** this skill lists **instances only**. It does not
> manage instance lifecycle (create/delete/resize/restart/flush/restore),
> does not export flavors, and does not write the report back to any cloud
> service. Those require a separate skill and explicit user confirmation.

## Prerequisites

1. **Python 3.8+** with the Huawei Cloud SDK — run
   `python3 scripts/ensure_env.py` to install `huaweicloudsdkcore` and
   `huaweicloudsdkdcs` automatically. The Markdown export itself needs no
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
4. **project_id (SDK fallback only)** — the DCS REST path is
   `/v2/{project_id}/instances`; supply the project id via `--project-id` or the
   `HUAWEICLOUD_SDK_PROJECT_ID` / `HUAWEI_PROJECT_ID` environment variables. The
   KooCLI path resolves it from the profile automatically.
5. **IAM permission** — read-only `dcs:instance:list`; least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
6. **Outbound HTTPS** access to `dcs.<region>.myhuaweicloud.com`.
- **skill-quality-cli** — ensured by bash scripts/ensure_cli.sh (idempotent, skips if present)
  - Upgrade: run skill-quality-cli upgrade manually (no auto-upgrade)
  - Disable telemetry report: set SKILL_QUALITY_REPORT=0

## Workflow

1. **(Optional) prepare the environment** — `python3 scripts/ensure_env.py`
   installs any missing SDK dependency.
2. **Confirm the target region** (default `cn-north-4`).
3. **(Optional) confirm KooCLI readiness** (read-only) — see the Core Commands
   block for the wrapped credential check.
4. **Run the script** with the desired output mode (`--format md` for the
   report, `table` / `json` otherwise).
5. **Read the result** — for `md`, the printed path is the generated report; hand
   that file path to the user. For table/json, display the result.
6. **Handle the empty / error cases** per the Error Handling table below.

## Core Commands

> **⚠️ Mandatory quality wrapping: `scripts/list_dcs_export_markdown.py` builds every `hcloud` CLI call as `skill-quality-cli run --skill-name huawei-cloud-dcs-export-markdown -- hcloud ...` (enforced in code, not left to the agent). If `skill-quality-cli` is unavailable (run `bash scripts/ensure_cli.sh`) or `SKILL_QUALITY_REPORT=0`, the CLI path degrades to bare `hcloud` (no telemetry) — the read-only semantics and the CLI→SDK fallback are unchanged.**

```bash
# Default: query the region's DCS instances and generate a .md report in cwd
python3 scripts/list_dcs_export_markdown.py

# Specify region and an explicit output path (recommended)
python3 scripts/list_dcs_export_markdown.py --region cn-north-4 \
  --output /tmp/dcs_instances_cn-north-4.md

# Append a summary line (total instance count)
python3 scripts/list_dcs_export_markdown.py --summary

# Plain table / JSON for humans / tooling
python3 scripts/list_dcs_export_markdown.py --format table
python3 scripts/list_dcs_export_markdown.py --format json

# Server-side filters
python3 scripts/list_dcs_export_markdown.py --region cn-south-1 --status RUNNING
python3 scripts/list_dcs_export_markdown.py --name cache --page-size 50
python3 scripts/list_dcs_export_markdown.py --name cache-demo-01 --name-equal
python3 scripts/list_dcs_export_markdown.py --instance-id 55f47f3d-...
python3 scripts/list_dcs_export_markdown.py --ip 192.168.0.10 --tags env=prod

# Read-only credential readiness check (also wrapped)
skill-quality-cli run --skill-name huawei-cloud-dcs-export-markdown -- hcloud configure list
```

Equivalent direct KooCLI command (the script wraps exactly this call, with
automatic offset paging):

```bash
skill-quality-cli run --skill-name huawei-cloud-dcs-export-markdown -- hcloud DCS ListInstances --cli-region=cn-north-4 --limit=100 --offset=0
skill-quality-cli run --skill-name huawei-cloud-dcs-export-markdown -- hcloud DCS ListInstances --cli-region=cn-north-4 --name=cache --status=RUNNING
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--format` / `-f` | No | Output mode: `md` (default) / `table` / `json` | `--format table` |
| `--output` / `-o` | No | Markdown file path (only used with `--format md`; default `dcs_instances_<region>_<timestamp>.md`) | `/tmp/report.md` |
| `--summary` | No | Append a summary line (实例数量) to the Markdown report | `--summary` |
| `--name` | No | Filter by instance name — real server-side query parameter (fuzzy) | `cache` |
| `--name-equal` | No | Exact-match switch: filters locally, case-insensitive | used with `--name` |
| `--instance-id` | No | Filter by exact instance ID — real server-side query parameter | `55f47f3d-...` |
| `--ip` | No | Filter by connection IP address — real server-side query parameter | `192.168.0.10` |
| `--status` | No | Filter by instance state — real server-side query parameter (`RUNNING` / `ERROR` / ...) | `RUNNING` |
| `--tags` | No | Filter by instance tags — real server-side query parameter (`key1=value1,key2=value2`) | `env=prod` |
| `--page-size` | No | Page size for ListInstances (default 100, range 1–1000; pages are fetched automatically) | `500` |
| `--project-id` | No | Project ID (needed by the SDK fallback path for `/v2/{project_id}/instances`) | `05f...` |
| `--operation` | No | hcloud DCS operation name; only the read-only `ListInstances` is allowed | `ListInstances` |

Output-mode precedence: `--format` selects the mode; `--output` / `--summary`
only matter for `md`. The local `--output` path value (e.g. a file literally
named `cache-delete-report.md`) is excluded from the write-intent guard because
it is not a DCS operation.

## Write-Intent Guard

- The script scans all user arguments (except the values of the read-only filter
  flags `--status` / `--name` / `--instance-id` / `--ip` / `--tags` / `--region`
  / `--page-size` / `--project-id` and of the local-output/format flags
  `--output` / `--format`) plus the `--operation` value for mutating vocabulary
  (`create`, `delete`, `update`, `modify`, `resize`, `restart`, `flush`, `clear`,
  `restore`, `backup`, `freeze`, ... and DCS operation names such as
  `CreateInstance`, `BatchDeleteInstances`, `ResizeInstance`,
  `RestartOrFlushInstances`, `ResetInstancePassword`).
- Any hit raises `GuardError`, prints
  `[错误] 检测到写操作意图 ... 已被守卫拦截`, and exits with code 1 **before** a
  single hcloud command is executed.
- Only `hcloud DCS ListInstances` (GET) — or the SDK `list_instances` call in the
  fallback path — is ever constructed by `build_command()`; there is no code
  path that can issue a mutating DCS API call. Every mutating DCS action
  (create / delete / resize / restart / flush / restore) requires a dedicated
  skill and explicit user confirmation.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `DCS`.
- **Operation name** — PascalCase API operation: `ListInstances`.
- **Region parameter** — always pass `--cli-region=<region>`, e.g.
  `--cli-region=cn-north-4`.
- **Simple parameters** — `--key=value`, e.g. `--limit=100`, `--offset=0`,
  `--name=cache`, `--instance_id=<id>`, `--ip=192.168.0.10`,
  `--status=RUNNING`, `--tags=env=prod`.
- **Paging** — `--limit` (integer, 1~1000) + `--offset` (integer, ≥ 0); the
  script fetches pages automatically until `instance_num` is reached.
- **REST path (official SDK)** — `GET /v2/{project_id}/instances`
  (`ListInstances`), invoked by `huaweicloudsdkdcs` v2
  `DcsClient.list_instances`.

## Markdown Format

| Column (header) | Source key | Notes |
| ---------- | ---------- | --------- |
| 名称 | `name` | Instance name |
| ID | `instance_id` | Instance ID (falls back to `id`) |
| 引擎 | `engine` | `Redis` / `Memcached` |
| 版本 | `engine_version` | Engine version |
| 容量 | `capacity` | Capacity (GB) |
| 规格 | `spec_code` | Flavor spec code |
| 状态 | `status` | `RUNNING` / `ERROR` / ... |
| 连接地址 | `ip` | Connection IP (falls back to domain name); `-` when absent |
| 端口 | `port` | Connection port |
| 可用区 | `az_codes` | Availability zones, comma-joined |

A missing field renders as `-`. `--summary` appends a trailing line:
`**汇总**：共 <N> 个 DCS 实例（Region <region>）。`

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty instance list | Exit 0, prints `当前区域（<x>）无 DCS 实例，未生成 Markdown 文件。` — no file is produced |
| Missing AK/SK | Exit 1, `缺少 AK/SK 凭证` hint to run `hcloud configure` out-of-band (never in chat) |
| Invalid / insufficient credentials (401 / 403 / ApiGW.0301) | Exit 1, `无权限访问分布式缓存服务（DCS），请检查 IAM 权限` hint; no .md is produced |
| hcloud not installed | Falls back to the SDK; if the SDK is unavailable too, exit 1 with a clear hint |
| Missing project_id (SDK fallback) | Exit 1, hint to pass `--project-id` or set the project-id env var |
| Bad `--output` path (permission / bad dir) | Exit 1, `Markdown 文件写出失败` hint; no partial file is left |
| `--page-size` out of range (not 1~1000) | Exit 1, explicit range error before any call |
| KooCLI usage error (`[USE_ERROR] ...`) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud DCS ListInstances --help` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty list; `1` config, auth, guard, export, or API
error (`table`/`json` modes follow the same conventions).

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Region has no instances | Friendly `无 DCS 实例，未生成 Markdown 文件` message, exit 0 |
| Many instances | Offset paging until the reported `instance_num` is reached (or a short page) |
| Filter yields no instance | Empty message includes the active filters (`status=...`, `name=...`) |
| `--name` | Forwarded as the real fuzzy server-side query parameter; `--name-equal` switches to exact local matching (case-insensitive) |
| Field missing on an instance | Rendered as `-` in both the table and the Markdown cell |
| `az_codes` / `tags` lists | Flattened into comma-joined cells |
| Instance without a name | The table shows `-`; the report still lists the instance |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkdcs` list_instances, same output modes |
| `--output` points to a non-existing directory | Directory is created automatically |
| `--output` path contains a guard keyword (e.g. `cache-delete-report.md`) | Path value is excluded from the guard (local path ≠ DCS operation) |
| `--status RUNNING` | Legitimate read filter — the status value is not scanned by the guard |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| User asks to create/delete/flush | Out of scope — blocked by the write-intent guard |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
cd skills/database/dcs/huawei-cloud-dcs-export-markdown
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / resize / restart /
flush / restore / backup / freeze / normalized variants / operation whitelist /
filter+output value exclusion / following-flag-still-scanned), command
construction, the skill-quality-cli wrapper (wrapped / bare override / report
toggle), JSON extraction and `instances` extraction, failure classification
(missing AK/SK, 403/401, generic, `[USE_ERROR]` with rc=0), offset paging
(instance_num / full page / empty), SDK fallback (missing env credentials /
missing project id), normalization and table rendering, Markdown rendering
(headers / `-` fallback / summary / pipe escaping), atomic export (file written /
missing dir created / bad path leaves no file / default name), and all `main()`
output modes.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI + SDK installation, credential configuration and skill-quality-cli |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |