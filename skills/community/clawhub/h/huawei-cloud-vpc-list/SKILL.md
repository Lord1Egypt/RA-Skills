---
name: huawei-cloud-vpc-list
description: |
  1. List Huawei Cloud Virtual Private Cloud (VPC) resources in a tenant
     region through KooCLI: virtual private clouds (hcloud VPC ListVpcs —
     read-only GET /v1/{project_id}/vpcs) and VPC peering connections
     (hcloud VPC ListVpcPeerings — read-only GET
     /v2.0/{project_id}/vpc/peerings), with an automatic fallback to the
     official huaweicloudsdkvpc v2 SDK when hcloud is not installed.
  2. `--resource {vpc,peering}` selects the query object (default `vpc`);
     the peering table has exactly four columns — name / local VPC / peer VPC /
     status — mapped from request_vpc_info.vpc_id / accept_vpc_info.vpc_id.
  3. Output modes: full-field table (default, every returned field including
     id/name/cidr/status and the remaining VPC attributes; peering uses the
     fixed four columns), --json (raw response array), --names-only (compact
     name list), and --format md (local Markdown report whose first column is
     VPC 名称; `--resource vpc` only).
  4. `--format md` writes a fixed 8-column Markdown table (VPC 名称 / VPC ID /
     区域 / 网段 / 状态 / 企业项目 ID / 描述 / 创建时间; missing field `-`;
     empty list = header-only table) to `--output`/`-o` (default
     `vpc_list_<region>_<timestamp>.md`), creates the parent directory, and
     writes via a temp file + atomic rename. Optional `--summary` appends the
     VPC count. Contract matches the dedicated VPC Markdown export skill
     (same fixed 8-column table; rendering kept independently).
  5. Supports --id / --enterprise-project-id filtering (both real server-side
     ListVpcs query parameters; the CLI path emits the v3 array form
     `--id.1=<vpc-id>`, which KooCLI requires), region override, and automatic
     marker paging for both VPC and peering queries.
  6. Explicit error hints for empty VPC / peering lists, 403 / insufficient IAM
     permission, missing or invalid AK/SK credentials, missing project_id on
     the SDK fallback, and hcloud not installed.
  7. Built-in write-intent guard: any mutating intent (create / delete / update /
     associate / disassociate / attach / detach / release / change, including
     CreateVpcPeering / AcceptVpcPeering / DeleteVpcPeering) or any operation
     other than the whitelisted ListVpcs / ListVpcPeerings is rejected before
     execution — this skill is strictly read-only. The local `--output` /
     `--format` values are excluded from the guard (a report path like
     `vpc-delete-report.md` is not a VPC operation).
  8. Triggers include: "list VPCs", "vpc list", "虚拟私有云列表", "查询 VPC",
     "查询虚拟私有云", "VPC 名称列表", "VPC 实例列表", "vpc inventory",
     "list vpcs", "华为云 VPC", "私有云列表", "对等连接", "对等连接列表",
     "VPC 对等连接", "peering list", "list vpc peerings". Dedicated
     Markdown-report intents are also served by the sibling export skill (see
     the division of labour below).
  9. Offline unit tests (mocked hcloud subprocess) cover output modes, Markdown
     rendering/export, filters, marker paging, error scenarios, SDK fallback,
     peering four-column mapping, and the write-intent guard.
tags: [huawei-cloud, vpc, network, readonly, koo-cli]
---

# Huawei Cloud Virtual Private Cloud (VPC) List

## Overview

Query the Virtual Private Cloud (VPC) resources of a tenant through two
read-only KooCLI operations:

- **VPC list** — hcloud VPC ListVpcs (official read-only GET
  `/v1/{project_id}/vpcs`, verified in the `huaweicloudsdkvpc` v2 client
  `_list_vpcs_http_info` metadata).
- **VPC peering list** — hcloud VPC ListVpcPeerings (official read-only GET
  `/v2.0/{project_id}/vpc/peerings`, verified in the `huaweicloudsdkvpc` v2
  client `_list_vpc_peerings_http_info` metadata).

The skill is aimed at VPC inventory inspection, daily operations patrol,
network topology checks, and as a pre-query step for other skills that need a
VPC `id`, its CIDR/status, or the peering links between VPCs.

Architecture:

```text
agent → python3 scripts/list_vpc.py --resource vpc|peering
      → hcloud VPC ListVpcs | ListVpcPeerings --cli-region=<region>
      → Huawei Cloud VPC OpenAPI (vpc.<region>.myhuaweicloud.com) → parsed JSON
      → table / --json / --names-only / --format md (.md file on local disk)

(hcloud binary missing) → fallback: huaweicloudsdkvpc v2
      VpcClient.list_vpcs | VpcClient.list_vpc_peerings
```

Key properties:

- **Read-only by design** — the only APIs ever invoked are `ListVpcs` and
  `ListVpcPeerings` (both GET). A write-intent guard scans user arguments and
  validates the operation name; mutating intents (create / delete / update /
  associate / disassociate / attach / detach / release / change, including
  peering create/accept/reject/delete) are rejected with an explicit message
  before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  KooCLI binary is absent, the script falls back to the official
  `huaweicloudsdkvpc` v2 SDK (`list_vpcs` / `list_vpc_peerings`). Credentials
  are always read by the CLI profile / SDK environment — never handled by the
  script.
- **Two resource views** — `--resource vpc` (default) keeps the full-field
  table; `--resource peering` renders exactly name / local VPC / peer VPC /
  status.
- **Full-field VPC table output** — the default VPC table renders the union of
  all fields returned by ListVpcs, with the nested `routes` array compacted
  into a single JSON column.
- **Name-first Markdown report** — `--format md` (VPC only) writes a fixed
  8-column Markdown table (`VPC 名称` first), with a `-` fallback for missing
  fields and a header-only table for an empty list. The report is generated on
  the local filesystem only, via a temp file + atomic rename; nothing is
  written back to the cloud.
- **Offline-testable** — every code path (marker paging, filters, output modes,
  Markdown rendering/export, error classification, guard, SDK fallback,
  peering mapping) is covered by unit tests that mock the hcloud subprocess.

Out of scope: every mutating VPC action (create / update / delete a VPC, subnet,
security group, route table, port or flow log; associate / disassociate a
resource; VPC peering create/accept/reject/delete). Those require a dedicated
write-capable skill and explicit user confirmation.

**Division of labour with the dedicated VPC Markdown export skill**: this skill
is the general VPC list / query entry point, and now also offers a convenience
`--format md` export. The dedicated VPC Markdown export skill remains the
Markdown-export specialist (same 8-column contract, rendering logic kept
independently, each skill installs on its own; see
`references/verification-method.md` for the cross-reference note). For
"导出 VPC 名称清单为 Markdown / VPC Markdown 报表" intents either skill works;
prefer the export skill when the task is purely Markdown deliverable, and this
skill when the task also needs table/json/name-list querying.

**Dependency**: Quality telemetry is collected automatically via skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkvpc` to enable the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band
   (run the KooCLI configure command in your terminal, or set credential
   environment variables).
   Never paste AK/SK into chat; the script never reads, echoes, or stores
   secrets itself — authentication is delegated entirely to the hcloud profile
   / SDK environment.
3. **project_id (SDK fallback only)** — the REST paths are
   `/v1/{project_id}/vpcs` and `/v2.0/{project_id}/vpc/peerings`; when falling
   back to the SDK, supply the project id via `--project-id` or the
   `HUAWEICLOUD_SDK_PROJECT_ID` / `HUAWEI_PROJECT_ID` environment variables.
   The KooCLI path resolves it from the profile automatically.
4. **IAM permission** — read-only `vpc:vpcs:list` (VPC list) and
   `vpc:peerings:list` (peering list); least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
5. **Python 3.8+** (standard library only — argparse / json / subprocess).
6. **Outbound HTTPS** access to `vpc.cn-north-4.myhuaweicloud.com`.
- **skill-quality-cli** — ensured by bash scripts/ensure_cli.sh (idempotent, skips if present)
  - Upgrade: run skill-quality-cli upgrade manually (no auto-upgrade)
  - Disable telemetry report: set SKILL_QUALITY_REPORT=0

## Workflow

1. **Confirm the target region** (default `cn-north-4`).
2. **Confirm the resource type** — `--resource vpc` (default) or
   `--resource peering`.
3. **Confirm KooCLI readiness** (optional, read-only) by listing the active
   credential profile.
4. **Run the list script** with the desired output mode and filters.
5. **Read the result** — table for humans (four fixed peering columns), `--json`
   for downstream tooling, `--names-only` for a compact inventory, `--format md`
   for a local Markdown report (the printed path is the generated `.md`).
6. **Handle the empty / error cases** per the Edge Cases table below (the
   script prints an explicit hint for empty VPC / peering lists, 403, and
   missing AK/SK; `--format md` always leaves a valid header-only file for an
   empty list).

## Core Commands

> **⚠️ Mandatory: every hcloud command in this skill MUST be wrapped with skill-quality-cli run --skill-name huawei-cloud-vpc-list -- ** — bare hcloud calls are strictly forbidden.**

```bash
# Full-field table (default)
python3 scripts/list_vpc.py --region cn-north-4

# Raw JSON of every returned field
python3 scripts/list_vpc.py --json

# Compact VPC name list only
python3 scripts/list_vpc.py --names-only

# Explicit format selection (table / json / names / md)
python3 scripts/list_vpc.py --format table
python3 scripts/list_vpc.py --format json
python3 scripts/list_vpc.py --format names

# Markdown report (default path vpc_list_<region>_<timestamp>.md in cwd)
python3 scripts/list_vpc.py --format md

# Markdown report to an explicit path (parent dir auto-created)
python3 scripts/list_vpc.py --format md --output /tmp/vpc_list_cn-north-4.md

# Markdown report with a trailing summary line (VPC count)
python3 scripts/list_vpc.py --format md --summary

# Filter by exact VPC id / enterprise project id (server-side query parameters)
python3 scripts/list_vpc.py --id vpc-0001
python3 scripts/list_vpc.py --enterprise-project-id 0

# Combine filters
python3 scripts/list_vpc.py --region cn-north-4 --enterprise-project-id 0 --names-only
python3 scripts/list_vpc.py --format md --output ./vpc.md --enterprise-project-id 0

# VPC peering connections: name / local VPC / peer VPC / status
python3 scripts/list_vpc.py --resource peering --region cn-north-4

# Peering raw JSON (request_vpc_info / accept_vpc_info preserved)
python3 scripts/list_vpc.py --resource peering --json

# Peering name list only
python3 scripts/list_vpc.py --resource peering --names-only
```

Equivalent direct KooCLI commands (the script wraps exactly these calls, with
marker paging):

```bash
skill-quality-cli run --skill-name huawei-cloud-vpc-list -- hcloud VPC ListVpcs --cli-region=cn-north-4 --limit=100
skill-quality-cli run --skill-name huawei-cloud-vpc-list -- hcloud VPC ListVpcPeerings --cli-region=cn-north-4 --limit=100

# Read-only credential readiness check (also wrapped)
skill-quality-cli run --skill-name huawei-cloud-vpc-list -- hcloud configure list
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--resource` | No | Query object: `vpc` (default, ListVpcs) or `peering` (ListVpcPeerings) | `peering` |
| `--json` | No | Output the raw response array as JSON | — |
| `--names-only` | No | Output the name list only | — |
| `--format` / `-f` | No | Output mode: `table` (default) / `json` / `names` / `md` (`md` requires `--resource vpc`) | `--format md` |
| `--output` / `-o` | No | Markdown file path (only used with `--format md`; default `vpc_list_<region>_<timestamp>.md`) | `/tmp/report.md` |
| `--summary` | No | Append a summary line (VPC 数量) to the Markdown report | `--summary` |
| `--id` | No | Filter by exact VPC ID — real server-side ListVpcs query parameter (forwarded to KooCLI as the v3 array form `--id.1=<vpc-id>`; `vpc` only) | `vpc-0001` |
| `--enterprise-project-id` | No | Filter by enterprise project ID — real server-side query parameter (`0` = default project; `vpc` only) | `0` |
| `--page-size` | No | Page size for ListVpcs / ListVpcPeerings (default 100, range 0–2000) | `100` |
| `--project-id` | No | Project ID (needed by the SDK fallback path for `/v1/{project_id}/...` or `/v2.0/{project_id}/...`) | `05f...` |
| `--operation` | No | hcloud VPC operation name; defaults to the operation for `--resource`; only `ListVpcs` / `ListVpcPeerings` are allowed | `ListVpcPeerings` |

Output-mode precedence: `--names-only` → `--json` → `--format` → table (default).
`--output` / `--summary` only matter for `--format md`; `--format md` writes a
file and prints its path instead of printing the table. Markdown export is
available for `--resource vpc`; peering uses the table / json / names modes.

## Write-Intent Guard

- The script scans all user arguments (except the values of the local
  output/format flags `--output` / `-o` / `--format` / `-f`, which are pure
  file-path / format data) plus the `--operation` value for mutating vocabulary
  (`create`, `delete`, `update`, `modify`, `associate`, `disassociate`,
  `attach`, `detach`, `bind`, `unbind`, `release`, `change`, `restart`, and VPC
  operation names such as `CreateVpc`, `DeleteVpc`, `UpdateVpc`,
  `CreateSubnet`, `DeleteSubnet`, `CreateSecurityGroup`, `CreateVpcPeering`,
  `AcceptVpcPeering`, `RejectVpcPeering`, `DeleteVpcPeering`).
  A following flag is still scanned, so a mutating flag cannot hide behind a
  stripped value. Filter values (`--id` etc.) remain scanned.
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed.
- The operation whitelist is per resource: `vpc` allows only `ListVpcs`,
  `peering` allows only `ListVpcPeerings`; a mismatched `--operation` is
  rejected. Only `build_command()` (ListVpcs) and `build_peering_command()`
  (ListVpcPeerings) can construct an hcloud call — there is no code path that
  can issue a mutating VPC API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `VPC`.
- **Operation name** — PascalCase: `ListVpcs` or `ListVpcPeerings`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete VPC call).
- **Simple parameter** — `--key=value`, e.g. `--limit=100`, `--marker=<token>`,
  `--enterprise_project_id=0`.
- **Array parameter** — v3 ListVpcs declares `id` / `cidr` / `description` /
  `name` as `array<string>`, so the filter must be emitted as
  `--id.1=<vpc-id>` (a bare `--id=<vpc-id>` fails with
  `[USE_ERROR]Invalid parameter: id`). Both filters are real server-side
  ListVpcs parameters (verified against `hcloud VPC ListVpcs --help` and the
  `huaweicloudsdkvpc` v2 `ListVpcsRequest` model).
- **Paging** — `--limit` + `--marker`; the marker is the `next_marker` returned
  in the response `page_info` (the marker is a resource id).
- **REST paths (official SDK `_http_info`)** —
  `GET /v1/{project_id}/vpcs` (`_list_vpcs_http_info`) and
  `GET /v2.0/{project_id}/vpc/peerings` (`_list_vpc_peerings_http_info`);
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

A missing field renders as `-`; pipe / newline characters are escaped. An
empty VPC list still renders a valid header-only (empty) table and exits 0.
`--summary` appends a trailing line:
`**汇总**：共 <N> 个 VPC（Region <region>）。`

The file is written with a temp file + atomic rename, so an interrupted write
never leaves a corrupt/partial `.md`. The parent directory of `--output` is
created automatically. The 8-column contract is held identical to
the dedicated VPC Markdown export skill (rendering is copied, not imported,
so the two skills each install independently; a unit test locks the contract).

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty VPC list | Exit 0, prints `当前区域（<x>）无虚拟私有云（VPC）` (+ active filters) |
| Empty peering list | Exit 0, prints `当前区域（<x>）无对等连接（VPC Peering）` |
| 403 / insufficient IAM permission | Exit 1, `无权限访问虚拟私有云（VPC），请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| Missing project_id (SDK fallback) | Exit 1, hint to pass `--project-id` or set the project-id env var |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkvpc` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit 「hcloud 参数错误」hint pointing to the KooCLI operation `--help` |
| Bad `--output` path (permission / bad dir) | Exit 1, `Markdown 文件写出失败` hint; no partial file is left |
| Empty VPC list with `--format md` | Exit 0, `当前区域（<x>）无虚拟私有云（VPC）...已生成空表（仅表头）`; the `.md` contains a header-only table |
| `--id` / `--enterprise-project-id` with `--resource peering` | Exit 1, explicit hint that these filters are VPC-only |
| `--format md` with `--resource peering` | Exit 1, explicit hint that Markdown export is VPC-only |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Non-`OK` VPCs / peerings | Reported with their state (`CREATING`, `PENDING_ACCEPTANCE`), not treated as failure |
| `--id` / `--enterprise-project-id` filters | Forwarded as real server-side ListVpcs query parameters; `--id` uses the v3 array form `--id.1=<vpc-id>` (bare `--id` is rejected by KooCLI; `vpc` only) |
| Large VPC / peering count | Automatic `marker` paging (`next_marker` aware, max 100 pages) |
| Extra VPC response fields | VPC table columns are built from the union of returned fields — new fields appear automatically |
| Field missing on a VPC | Rendered as `-` in the table |
| Nested `routes` array | Compacted into a single JSON column for the table |
| Peering side missing (`request_vpc_info` / `accept_vpc_info`) | Local / peer VPC cell rendered as `-` |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkvpc` list_vpcs / list_vpc_peerings, same output modes |
| `--format md` and the list is empty (or filtered to empty) | Header-only `.md` written, exit 0; the empty message lists active filters |
| `--output` points to a non-existing directory | Directory is created automatically |
| `--output` path contains a guard keyword (e.g. `vpc-delete-report.md`) | Path value is excluded from the guard (local path ≠ VPC operation) |
| `--format md` combined with legacy `--json` / `--names-only` | Legacy flag wins (`--names-only` → `--json` → `--format`) |
| User asks to create/delete/accept a VPC or peering | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
cd skills/network/vpc/huawei-cloud-vpc-list
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / update /
associate / release / change / normalized variants / per-resource operation
whitelist / output-value exclusion / following-flag-still-scanned), command
construction (filters forwarded server-side; marker never sent on the first
page), JSON extraction, failure classification (missing AK/SK, 403, generic,
`[USE_ERROR]` with rc=0), marker paging (next_marker / full page / empty), SDK
fallback (success, missing credentials, missing project id, and unavailable;
request construction matches the real `ListVpcsRequest` / `ListVpcPeeringsRequest`
signature), peering four-column mapping (request_vpc_info / accept_vpc_info /
missing side), rendering (table with routes / names / fallbacks), Markdown
rendering (fixed headers / name first / `-` fallback / header-only empty table /
summary / pipe escaping / contract equality with the dedicated export skill),
atomic export (file written / empty table file / missing dir created / bad path
leaves no partial file / default name), and all main() output modes including
`--format md`, empty, filter, peering, and error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation, credential configuration and skill-quality-cli |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |