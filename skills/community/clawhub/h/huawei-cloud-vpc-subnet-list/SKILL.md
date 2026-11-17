---
name: huawei-cloud-vpc-subnet-list
description: |
  1. List Huawei Cloud VPC subnets (Subnet) in a tenant region through KooCLI
     (hcloud VPC ListSubnets — read-only GET /v1/{project_id}/subnets), with an
     automatic fallback to the official huaweicloudsdkvpc v2 SDK when hcloud is
     not installed.
  2. Three output modes: full-field table (default, every returned field
     including id/name/vpc_id/cidr/gateway_ip/status and the remaining subnet
     attributes), --json (raw response array), and --names-only (compact subnet
     name list).
  3. Supports --vpc-id filtering (a real server-side ListSubnets query
     parameter), region override, and automatic marker paging.
  4. Explicit error hints for empty subnet lists (「当前区域无 VPC 子网（Subnet）」),
     403 / insufficient IAM permission (「无权限访问 VPC 子网（Subnet）」),
     missing or invalid AK/SK credentials, missing project_id on the SDK
     fallback, and hcloud not installed.
  5. Built-in write-intent guard: any mutating intent (create / delete / update /
     associate / disassociate / attach / detach / release / change) or any
     operation other than ListSubnets is rejected before execution — this skill
     is strictly read-only.
  6. Triggers include: "list subnets", "subnet list", "VPC 子网列表", "查询子网",
     "子网名称列表", "子网清单", "vpc subnet", "华为云子网", "子网盘点",
     "子网列表查询", "虚拟私有云子网列表", "subnet inventory". Every trigger is
     subnet-scoped (子网/subnet) and none contains a bare VPC phrase, so no trigger
     is a substring of a sibling VPC skill's trigger (routing stays unambiguous).
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, filters,
     marker paging, error scenarios, SDK fallback, and the write-intent guard.
tags: [huawei-cloud, vpc, subnet, network, readonly]
---

# Huawei Cloud VPC Subnet (Subnet) List

## Overview

Query the VPC subnet (Subnet) list of a tenant through the KooCLI VPC
ListSubnets operation (hcloud VPC ListSubnets, official read-only
GET `/v1/{project_id}/subnets`, verified in the `huaweicloudsdkvpc` v2 client
`_list_subnets_http_info` metadata). The skill is aimed at subnet inventory
inspection, daily network operations patrol, and as a pre-query step for other
skills that need a subnet `id`, its CIDR or gateway.

Architecture:

```text
agent → python3 scripts/list_subnet.py → hcloud VPC ListSubnets --cli-region=<region>
      → Huawei Cloud VPC OpenAPI (vpc.<region>.myhuaweicloud.com) → parsed JSON → table / --json / --names-only

(hcloud binary missing) → fallback: huaweicloudsdkvpc v2 VpcClient.list_subnets
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListSubnets` (GET). A
  write-intent guard scans user arguments and validates the operation name;
  mutating intents (create / delete / update / associate / disassociate /
  attach / detach / release / change) are rejected with an explicit message
  before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  KooCLI binary is absent, the script falls back to the official
  `huaweicloudsdkvpc` v2 SDK (`list_subnets`). Credentials are always read by
  the CLI profile / SDK environment — never handled by the script.
- **Full-field table output** — the default table renders the union of all
  fields returned by ListSubnets, with the nested `extra_dhcp_opts` /
  `dns_list` cells compacted into single JSON columns.
- **Offline-testable** — every code path (marker paging, vpc_id filter, error
  classification, guard, SDK fallback) is covered by unit tests that mock the
  hcloud subprocess.

Out of scope: every mutating VPC/subnet action (create / update / delete a VPC
or subnet, security group, route table, port or flow log; associate /
disassociate a resource; VPC peering accept/reject). Those require a dedicated
write-capable skill and explicit user confirmation.

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
3. **project_id (SDK fallback only)** — the subnet REST path is
   `/v1/{project_id}/subnets`; when falling back to the SDK, supply the project
   id via `--project-id` or the `HUAWEICLOUD_SDK_PROJECT_ID` /
   `HUAWEI_PROJECT_ID` environment variables. The KooCLI path resolves it from
   the profile automatically.
4. **IAM permission** — read-only `vpc:subnets:list`; least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
5. **Python 3.8+** (standard library only — argparse / json / subprocess).
6. **Outbound HTTPS** access to `vpc.cn-north-4.myhuaweicloud.com`.
- **skill-quality-cli** — ensured by bash scripts/ensure_cli.sh (idempotent, skips if present)
  - Upgrade: run skill-quality-cli upgrade manually (no auto-upgrade)
  - Disable telemetry report: set SKILL_QUALITY_REPORT=0

## Workflow

1. **Confirm the target region** (default `cn-north-4`).
2. **Confirm KooCLI readiness** (optional, read-only) by listing the active
   credential profile.
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — table for humans, `--json` for downstream tooling,
   `--names-only` for a compact inventory.
5. **Handle the empty / error cases** per the Edge Cases table below (the
   script prints an explicit hint for empty region, 403, and missing AK/SK).

## Core Commands

> **⚠️ Mandatory: every hcloud command in this skill MUST be wrapped with skill-quality-cli run --skill-name huawei-cloud-vpc-subnet-list -- ** — bare hcloud calls are strictly forbidden.**

```bash
# Full-field table (default)
python3 scripts/list_subnet.py --region cn-north-4

# Raw JSON of every returned field
python3 scripts/list_subnet.py --json

# Compact subnet name list only
python3 scripts/list_subnet.py --names-only

# Filter by the owning VPC id (server-side query parameter)
python3 scripts/list_subnet.py --vpc-id vpc-0001

# Combine filters / region
python3 scripts/list_subnet.py --region cn-north-4 --vpc-id vpc-0001 --names-only
```

Equivalent direct KooCLI command (the script wraps exactly this call, with
marker paging):

```bash
skill-quality-cli run --skill-name huawei-cloud-vpc-subnet-list -- hcloud VPC ListSubnets --cli-region=cn-north-4 --limit=100

# Read-only credential readiness check (also wrapped)
skill-quality-cli run --skill-name huawei-cloud-vpc-subnet-list -- hcloud configure list
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--json` | No | Output the raw subnet array as JSON | — |
| `--names-only` | No | Output the subnet name list only | — |
| `--vpc-id` | No | Filter by the owning VPC ID — real server-side ListSubnets query parameter (required under enterprise-project fine-grained authorization) | `vpc-0001` |
| `--page-size` | No | Page size for ListSubnets (default 100) | `100` |
| `--project-id` | No | Project ID (needed by the SDK fallback path for `/v1/{project_id}/...`) | `05f...` |
| `--operation` | No | hcloud VPC operation name; only `ListSubnets` is allowed | `ListSubnets` |

Output-mode precedence: `--names-only` → `--json` → table (default).

## Write-Intent Guard

- The script scans all user arguments plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `modify`, `associate`,
  `disassociate`, `attach`, `detach`, `bind`, `unbind`, `release`, `change`,
  `restart`, and VPC/subnet operation names such as `CreateVpc`, `DeleteVpc`,
  `UpdateVpc`, `CreateSubnet`, `DeleteSubnet`, `UpdateSubnet`,
  `CreateSecurityGroup`, `CreateVpcPeering`).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed.
- Only the VPC ListSubnets GET call (via KooCLI, or the SDK `list_subnets` call
  in the fallback path) is ever constructed by `build_command()`; there is no
  code path that can issue a mutating VPC/subnet API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `VPC`.
- **Operation name** — PascalCase: `ListSubnets`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete VPC call).
- **Simple parameter** — `--key=value`, e.g. `--limit=100`, `--marker=<token>`,
  `--vpc_id=<vpc-id>`. `vpc_id` is a real server-side ListSubnets parameter
  (verified against the `huaweicloudsdkvpc` v2 `ListSubnetsRequest` model).
- **Paging** — `--limit` + `--marker`; the marker is the `next_marker` returned
  in the response `page_info` (the marker is a subnet resource id).
- **REST path (official SDK `_http_info`)** —
  `GET /v1/{project_id}/subnets` (`huaweicloudsdkvpc` v2 `_list_subnets_http_info`);
  the project_id is resolved by KooCLI from the credential profile.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty subnet list | Exit 0, prints `当前区域（<x>）无 VPC 子网（Subnet）` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问 VPC 子网（Subnet），请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| Missing project_id (SDK fallback) | Exit 1, hint to pass `--project-id` or set the project-id env var |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkvpc` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit 「hcloud 参数错误」hint pointing to the KooCLI VPC ListSubnets `--help` |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Non-`OK` subnets | Reported with their state (`ACTIVE` / `PENDING` / `DOWN`), not treated as failure |
| `--vpc-id` filter | Forwarded as a real server-side query parameter (verified API param) |
| Large subnet count | Automatic `marker` paging (`next_marker` aware, max 100 pages) |
| Extra response fields | Table columns are built from the union of returned fields — new fields appear automatically |
| Field missing on a subnet | Rendered as `-` in the table |
| Nested `extra_dhcp_opts` / `dns_list` | Compacted into single JSON columns for the table |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkvpc` list_subnets, same output modes |
| User asks to create/delete/associate a subnet | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
cd skills/network/vpc/huawei-cloud-vpc-subnet-list
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / update /
associate / release / change / normalized variants / operation whitelist),
command construction (vpc_id filter forwarded server-side; marker never sent on
the first page), JSON extraction, failure classification (missing AK/SK, 403,
generic, `[USE_ERROR]` with rc=0), marker paging (next_marker / full page /
empty), SDK fallback (success, missing credentials, missing project id, and
unavailable; request construction matches the real `ListSubnetsRequest`
signature), rendering (table with nested cells / names / fallbacks), and all
main() output modes including empty, filter, and error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation, credential configuration and skill-quality-cli |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |