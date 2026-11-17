---
name: huawei-cloud-vpc-export-markdown
description: |
  1. Query the Huawei Cloud Virtual Private Cloud (VPC) list of a tenant region
     through KooCLI (`hcloud VPC ListVpcs`, the official read-only GET
     /v1/{project_id}/vpcs), with an automatic fallback to the official
     huaweicloudsdkvpc v2 SDK (VpcClient.list_vpcs) when hcloud is not installed.
  2. Export the VPC list into a well-formed local Markdown table whose first
     column is the required **VPC 名称** (VPC name), followed by VPC ID / 区域 /
     网段 / 状态 / 企业项目 ID / 描述 / 创建时间 — strictly local file generation,
     nothing is ever written back to the cloud. `--output`/`-o` sets the path
     (default `vpc_list_<region>_<timestamp>.md`); the parent directory is created
     automatically and the file is written via a temp file + atomic rename.
  3. Three output modes: `--format md` (default) / `table` / `json`. Region aware:
     `--region` (default cn-north-4). Optional `--id` / `--enterprise-project-id`
     server-side filters and `--page-size` (default 100); paging follows the
     reported `page_info.next_marker`.
  4. Explicit error classification: missing AK/SK credentials (「缺少 AK/SK
     凭证」), hcloud not installed (falls back to the SDK, else a clear hint),
     invalid/insufficient credentials (403 / 401 → IAM hint), KooCLI usage errors,
     and generic API/network failures. An empty VPC list still outputs an empty
     (header-only) Markdown table and exits 0 — never a corrupt file.
  5. Built-in write-intent guard: any mutating intent (create / delete / update /
     associate / disassociate / attach / detach / release / change ...) or any
     operation other than the read-only ListVpcs is rejected before execution —
     this skill is strictly read-only.
  6. Triggers include: "导出 VPC 名称清单为 Markdown", "VPC 列表导出 Markdown",
     "vpc markdown", "VPC 导出 Markdown", "虚拟私有云 Markdown 报表",
     "VPC 名称留档", "vpc 报表", "export VPC to markdown" — Markdown/export
     specialised only (plain VPC list / query intents are owned by the separate
     VPC list skill, not by this Markdown export skill).
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, marker
     paging, Markdown format correctness, empty results, filters, error
     classification, the SDK fallback, the skill-quality-cli wrapper and the
     write-intent guard.
tags: [huawei-cloud, vpc, network, readonly, markdown]
---

# Huawei Cloud VPC List → Markdown Export

## Overview

Query the Virtual Private Cloud (VPC) list of a tenant region through KooCLI
`hcloud VPC ListVpcs` (official read-only GET `/v1/{project_id}/vpcs`, verified
in the `huaweicloudsdkvpc` v2 client `_list_vpcs_http_info` metadata), with a
fallback to the official `huaweicloudsdkvpc` v2 SDK, and export the result into
a local **Markdown** report. The skill is aimed at VPC inventory inspection,
daily operations patrol, and Markdown-report style deliverables.

Architecture:

```text
agent → python3 scripts/export_vpc_markdown.py → skill-quality-cli run ─▶ hcloud VPC ListVpcs --cli-region=<region> --limit=N --marker=M
      → Huawei Cloud VPC OpenAPI (vpc.<region>.myhuaweicloud.com) → parsed JSON vpcs → render_markdown → .md / table / json

(hcloud binary missing) → fallback: huaweicloudsdkvpc v2 VpcClient.list_vpcs
(missing SDK)           → run scripts/ensure_env.py  (auto pip install)
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListVpcs` (GET). A
  write-intent guard scans the user arguments and validates the operation name;
  mutating intents (create / delete / update / associate / disassociate /
  attach / detach / release / change ...) are rejected with an explicit message
  before any command runs. The Markdown file is generated on the **local
  filesystem only** — no VPC write happens.
- **CLI first, SDK fallback** — KooCLI is the primary execution path (wrapped
  with `skill-quality-cli` for telemetry); when the hcloud binary is absent, the
  script falls back to the official `huaweicloudsdkvpc` v2 SDK (`list_vpcs`).
  Credentials are read from the hcloud profile or the SDK environment — never
  handled by the script.
- **Well-formed, name-first Markdown** — a fixed header row whose **first column
  is VPC 名称** (VPC ID / 区域 / 网段 / 状态 / 企业项目 ID / 描述 / 创建时间), one
  data row per VPC, a **`-`** fallback for missing fields, and an **optional
  summary line** (`--summary`). The report is saved via a temporary file +
  atomic rename, so an interrupted write never leaves a corrupt/partial `.md`.
- **Empty region is not an error** — an empty VPC list still produces a valid
  header-only (empty) Markdown table and exits `0`.
- **Offline-testable** — every code path (marker paging, filters, output modes,
  Markdown format, empty result, error classification, guard, SDK fallback,
  quality wrapper) is covered by unit tests that mock the hcloud subprocess.

> **Dependency**: Quality telemetry is collected automatically via skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

> **Capability boundary:** this skill lists **VPCs only**. It does not manage VPC
> lifecycle (create/delete/update), subnets, route tables, security groups or
> peering, and it does not write the report back to any cloud service. Those
> require a separate skill and explicit user confirmation.

## Prerequisites

1. **Python 3.8+** with the Huawei Cloud SDK — run
   `python3 scripts/ensure_env.py` to install `huaweicloudsdkcore` and
   `huaweicloudsdkvpc` automatically. The Markdown export itself needs no
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
4. **project_id (SDK fallback only)** — the VPC REST path is
   `/v1/{project_id}/vpcs`; supply the project id via `--project-id` or the
   `HUAWEICLOUD_SDK_PROJECT_ID` / `HUAWEI_PROJECT_ID` environment variables. The
   KooCLI path resolves it from the profile automatically.
5. **IAM permission** — read-only `vpc:vpcs:list`; least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
6. **Outbound HTTPS** access to `vpc.cn-north-4.myhuaweicloud.com`.
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

> **⚠️ Mandatory quality wrapping: `scripts/export_vpc_markdown.py` builds every `hcloud` CLI call as `skill-quality-cli run --skill-name huawei-cloud-vpc-export-markdown -- hcloud ...` (enforced in code, not left to the agent). If `skill-quality-cli` is unavailable (run `bash scripts/ensure_cli.sh`) or `SKILL_QUALITY_REPORT=0`, the CLI path degrades to bare `hcloud` (no telemetry) — the read-only semantics and the CLI→SDK fallback are unchanged.**

```bash
# Default: query the region's VPCs and generate a .md report in cwd
python3 scripts/export_vpc_markdown.py

# Specify region and an explicit output path (recommended)
python3 scripts/export_vpc_markdown.py --region cn-north-4 \
  --output /tmp/vpc_list_cn-north-4.md

# Append a summary line (total VPC count)
python3 scripts/export_vpc_markdown.py --summary

# Plain table / JSON for humans / tooling
python3 scripts/export_vpc_markdown.py --format table
python3 scripts/export_vpc_markdown.py --format json

# Server-side filters
python3 scripts/export_vpc_markdown.py --region cn-south-1 --id vpc-0001
python3 scripts/export_vpc_markdown.py --enterprise-project-id 0 --page-size 50

# Read-only credential readiness check (also wrapped)
skill-quality-cli run --skill-name huawei-cloud-vpc-export-markdown -- hcloud configure list
```

Equivalent direct KooCLI command (the script wraps exactly this call, with
automatic marker paging):

```bash
skill-quality-cli run --skill-name huawei-cloud-vpc-export-markdown -- hcloud VPC ListVpcs --cli-region=cn-north-4 --limit=100
skill-quality-cli run --skill-name huawei-cloud-vpc-export-markdown -- hcloud VPC ListVpcs --cli-region=cn-north-4 --id=vpc-0001 --enterprise_project_id=0
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--format` / `-f` | No | Output mode: `md` (default) / `table` / `json` | `--format table` |
| `--output` / `-o` | No | Markdown file path (only used with `--format md`; default `vpc_list_<region>_<timestamp>.md`) | `/tmp/report.md` |
| `--summary` | No | Append a summary line (VPC 数量) to the Markdown report | `--summary` |
| `--id` | No | Filter by exact VPC ID — real server-side query parameter | `vpc-0001` |
| `--enterprise-project-id` | No | Filter by enterprise project ID — real server-side query parameter (`0` = default project) | `0` |
| `--page-size` | No | Page size for ListVpcs (default 100, range 1–2000; pages are fetched automatically) | `500` |
| `--project-id` | No | Project ID (needed by the SDK fallback path for `/v1/{project_id}/vpcs`) | `05f...` |
| `--operation` | No | hcloud VPC operation name; only the read-only `ListVpcs` is allowed | `ListVpcs` |

Output-mode precedence: `--format` selects the mode; `--output` / `--summary`
only matter for `md`. The local `--output` path value (e.g. a file literally
named `vpc-delete-report.md`) is excluded from the write-intent guard because it
is not a VPC operation.

## Write-Intent Guard

- The script scans all user arguments (except the values of the read-only filter
  flags `--id` / `--enterprise-project-id` / `--region` / `--page-size` /
  `--project-id` and of the local-output/format flags `--output` / `-o` /
  `--format` / `-f`) plus the `--operation` value for mutating vocabulary
  (`create`, `delete`, `update`, `modify`, `associate`, `disassociate`,
  `attach`, `detach`, `bind`, `unbind`, `release`, `remove`, `change`, ... and
  VPC operation names such as `CreateVpc`, `DeleteVpc`, `UpdateVpc`,
  `CreateSubnet`, `DeleteSubnet`, `CreateSecurityGroup`, `CreateVpcPeering`).
- Any hit raises `GuardError`, prints
  `[错误] 检测到写操作意图 ... 已被守卫拦截`, and exits with code 1 **before** a
  single hcloud command is executed.
- Only `hcloud VPC ListVpcs` (GET) — or the SDK `list_vpcs` call in the fallback
  path — is ever constructed by `build_command()`; there is no code path that
  can issue a mutating VPC API call. Every mutating VPC action requires a
  dedicated skill and explicit user confirmation.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `VPC`.
- **Operation name** — PascalCase API operation: `ListVpcs`.
- **Region parameter** — always pass `--cli-region=<region>`, e.g.
  `--cli-region=cn-north-4`.
- **Simple parameters** — `--key=value`, e.g. `--limit=100`, `--marker=<token>`,
  `--id=<vpc-id>`, `--enterprise_project_id=0`. Both filters are real
  server-side ListVpcs parameters (verified against the `huaweicloudsdkvpc` v2
  `ListVpcsRequest` model).
- **Paging** — `--limit` + `--marker`; the marker is the `next_marker` returned
  in the response `page_info` (the marker is a VPC resource id).
- **REST path (official SDK `_http_info`)** —
  `GET /v1/{project_id}/vpcs` (`huaweicloudsdkvpc` v2 `_list_vpcs_http_info`);
  the project_id is resolved by KooCLI from the credential profile.

## Markdown Format

| Column (header) | Source key | Notes |
| ---------- | ---------- | --------- |
| VPC 名称 | `name` | **Required column** — the VPC name |
| VPC ID | `id` | VPC ID |
| 区域 | `--region` | Region label of the query |
| 网段 | `cidr` | VPC CIDR range |
| 状态 | `status` | `OK` / `CREATING` / ... |
| 企业项目 ID | `enterprise_project_id` | Enterprise project id (`0` = default) |
| 描述 | `description` | VPC description |
| 创建时间 | `created_at` | Creation timestamp |

A missing field renders as `-`. `--summary` appends a trailing line:
`**汇总**：共 <N> 个 VPC（Region <region>）。` An empty VPC list still renders a
valid header-only (empty) table.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty VPC list | Exit 0, prints `当前区域（<x>）无虚拟私有云（VPC）...已生成空表（仅表头）`; the `.md` contains a header-only (empty) table |
| Missing AK/SK | Exit 1, `缺少 AK/SK 凭证` hint to run `hcloud configure` out-of-band (never in chat); no file is produced |
| Invalid / insufficient credentials (401 / 403 / ApiGW.0301) | Exit 1, `无权限访问虚拟私有云（VPC），请检查 IAM 权限` hint; no file is produced |
| hcloud not installed | Falls back to the SDK; if the SDK is unavailable too, exit 1 with a clear hint |
| Missing project_id (SDK fallback) | Exit 1, hint to pass `--project-id` or set the project-id env var |
| Bad `--output` path (permission / bad dir) | Exit 1, `Markdown 文件写出失败` hint; no partial file is left |
| `--page-size` out of range (not 1~2000) | Exit 1, explicit range error before any call |
| KooCLI usage error (`[USE_ERROR] ...`) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud VPC ListVpcs --help` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, export, or API
error (`table`/`json` modes follow the same conventions).

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Region has no VPCs | Friendly message + a header-only (empty) Markdown table, exit 0 |
| Many VPCs | Automatic `marker` paging (`next_marker` aware, max 100 pages) |
| Filter yields no VPC | Empty message includes the active filters (`id=...`, `enterprise_project_id=...`) |
| Field missing on a VPC | Rendered as `-` in both the table and the Markdown cell |
| Non-`OK` VPCs | Reported with their state (`CREATING`), not treated as failure |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkvpc` list_vpcs, same output modes |
| `--output` points to a non-existing directory | Directory is created automatically |
| `--output` path contains a guard keyword (e.g. `vpc-delete-report.md`) | Path value is excluded from the guard (local path ≠ VPC operation) |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| User asks to create/delete/associate a VPC | Out of scope — blocked by the write-intent guard |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network),
executed from the skill directory through the bundled runner (the same
executor-friendly entrypoint declared in templates/test-vars.json):

```bash
python3 scripts/run_unit_tests.py
```

Coverage: write-intent guard (read passes / create / delete / update /
associate / release / normalized variants / operation whitelist / filter+output
value exclusion / following-flag-still-scanned), command construction, the
skill-quality-cli wrapper (wrapped / bare override / report toggle), JSON
extraction and `vpcs` extraction, failure classification (missing AK/SK, 403,
generic, `[USE_ERROR]` with rc=0), marker paging (`next_marker` / full page /
empty), SDK fallback (missing env credentials / missing project id),
normalization and table rendering, Markdown rendering (headers / `-` fallback /
header-only empty table / summary / pipe escaping), atomic export (file written /
empty table file written / missing dir created / bad path leaves no file /
default name), and all `main()` output modes.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI + SDK installation, credential configuration and skill-quality-cli |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |