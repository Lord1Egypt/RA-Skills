---
name: huawei-cloud-elb-list
description: |
  1. List Huawei Cloud Elastic Load Balance (ELB) load balancers in a tenant
     region through KooCLI (hcloud ELB ListLoadbalancers — read-only GET
     /v3/{project_id}/elb/loadbalancers), with an automatic fallback to the
     official huaweicloudsdkelb v3 SDK when hcloud is not installed.
  2. Output modes: standardized table (default, exactly two columns — ID and
     名称, no other fields), --json (raw response array with every returned
     field), and --names-only (compact load balancer name list).
  3. Every list query (default table or --names-only) also generates a Markdown
     document whose content is the standardized ID + 名称 list (Markdown table
     `| ID | 名称 |`). It is written to `elb-list.md` by default; use
     `--md-out <path>` to change the path (missing parent directories are
     created automatically) or `--no-md` to disable. `--json` never writes the
     document.
  4. Supports --id / --name / --vpc-id / --provisioning-status /
     --operating-status / --enterprise-project-id / --vip-address filtering (all
     real server-side ListLoadbalancers query parameters), region override,
     --project-id, and automatic marker paging.
  5. Explicit error hints for empty ELB lists (「当前区域无负载均衡器（ELB）」),
     403 / insufficient IAM permission (「无权限访问弹性负载均衡（ELB）」),
     missing or invalid AK/SK credentials, missing project_id on the SDK
     fallback, and hcloud not installed.
  6. Built-in write-intent guard: any mutating intent (create / delete / update /
     modify / clone / restore / enable / disable / associate / detach / change)
     or any operation other than ListLoadbalancers is rejected before execution
     — this skill is strictly read-only.
  7. Triggers include: "list ELB", "elb list", "负载均衡器列表", "查询 ELB",
     "查询负载均衡器", "ELB 实例列表", "elastic load balancer inventory",
     "list loadbalancers", "华为云 ELB", "负载均衡器名称列表".
  8. Offline unit tests (mocked hcloud subprocess) cover output modes, filters,
     marker paging, error scenarios, SDK fallback, the standardized output, the
     Markdown generation, and the write-intent guard.
tags: [huawei-cloud, elb, network, readonly, koo-cli]
---

# Huawei Cloud Elastic Load Balance (ELB) Load Balancer List

## Overview

Query the Elastic Load Balance (ELB) load balancer list of a tenant through
KooCLI `hcloud ELB ListLoadbalancers` (official read-only GET
`/v3/{project_id}/elb/loadbalancers`, verified in the `huaweicloudsdkelb` v3
client `_list_load_balancers_http_info` metadata). The skill is aimed at ELB
inventory inspection, daily operations patrol, and as a pre-query step for other
skills that need an ELB `id` / `vip_address` or a bound EIP.

Architecture:

```text
agent → python3 scripts/list_elb.py → hcloud ELB ListLoadbalancers --cli-region=<region>
      → Huawei Cloud ELB OpenAPI (elb.<region>.myhuaweicloud.com) → parsed JSON
      → standardized id+name table / --json / --names-only
      → Markdown document (standardized id + 名称, default elb-list.md)

(hcloud binary missing) → fallback: huaweicloudsdkelb v3 ElbClient.list_load_balancers
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListLoadbalancers`
  (GET). A write-intent guard scans user arguments and validates the operation
  name; mutating intents (create / delete / update / modify / clone / restore /
  enable / disable / associate / detach / change) are rejected with an explicit
  message before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  KooCLI binary is absent, the script falls back to the official
  `huaweicloudsdkelb` v3 SDK (`list_load_balancers`). Credentials are always
  read by the CLI profile / SDK environment — never handled by the script.
- **Standardized table output** — the default table renders exactly two columns,
  `id` and `name` (名称); every other field returned by ListLoadbalancers is
  dropped for a stable, easy-to-consume inventory. The raw full-field response is
  still available through `--json`.
- **Markdown document** — each list query also writes a Markdown document whose
  content is the standardized `id` + 名称 list (Markdown table `| ID | 名称 |`),
  to `elb-list.md` by default (`--md-out <path>` / `--no-md` to control).
- **Offline-testable** — every code path (marker paging, filters, error
  classification, guard, SDK fallback, standardization, Markdown generation) is
  covered by unit tests that mock the hcloud subprocess.

Out of scope: every mutating ELB action (create / update / delete a load
balancer, create / update / delete a listener, pool, member, health monitor, L7
policy or certificate, clone, restore, change charge mode). Those require a
dedicated write-capable skill and explicit user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `python3 scripts/ensure_env.py` (or
   `pip install huaweicloudsdkcore huaweicloudsdkelb`) to enable the SDK
   fallback path.
2. **Active credential profile** — configure credentials out-of-band
   (run the KooCLI configure command in your terminal, or set credential
   environment variables).
   Never paste AK/SK into chat; the script never reads, echoes, or stores
   secrets itself — authentication is delegated entirely to the hcloud profile
   / SDK environment.
3. **project_id (SDK fallback only)** — the ELB REST path is
   `/v3/{project_id}/elb/loadbalancers`; when falling back to the SDK, supply
   the project id via `--project-id` or the `HUAWEICLOUD_SDK_PROJECT_ID` /
   `HUAWEI_PROJECT_ID` environment variables. The KooCLI path resolves it from
   the profile automatically.
4. **IAM permission** — read-only `elb:loadbalancers:list`; least-privilege
   policy in [references/iam-policies.md](references/iam-policies.md).
5. **Python 3.8+** (standard library only — argparse / json / subprocess).
6. **Outbound HTTPS** access to `elb.cn-north-4.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`).
2. **Confirm KooCLI readiness** (optional, read-only) by listing the active
   credential profile.
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — standardized `id` + `name` table for humans, `--json` for
   downstream tooling, `--names-only` for a compact inventory.
5. **Collect the Markdown document** — the list query writes the standardized
   `id` + 名称 list to `elb-list.md` (or `--md-out <path>`); pass `--no-md` to skip.
6. **Handle the empty / error cases** per the Edge Cases table below (the
   script prints an explicit hint for empty region, 403, and missing AK/SK).

## Core Commands

```bash
# Self-heal the SDK fallback dependencies (idempotent)
python3 scripts/ensure_env.py

# Standardized id + 名称 table (default) + Markdown document (elb-list.md)
python3 scripts/list_elb.py --region cn-north-4

# Markdown document to a custom path (still prints the standardized table)
python3 scripts/list_elb.py --region cn-north-4 --md-out inventory/elb-list.md

# Standardized table only, no Markdown document
python3 scripts/list_elb.py --region cn-north-4 --no-md

# Raw JSON of every returned field (no Markdown document)
python3 scripts/list_elb.py --json

# Compact load balancer name list only (also writes the Markdown document)
python3 scripts/list_elb.py --names-only

# Filter by provisioning status (server-side query parameter)
python3 scripts/list_elb.py --provisioning-status ACTIVE

# Filter by exact load balancer id / name / VIP
python3 scripts/list_elb.py --id lb-0001
python3 scripts/list_elb.py --name lb-demo
python3 scripts/list_elb.py --vip-address 192.168.0.10

# Combine filters
python3 scripts/list_elb.py --region cn-north-4 --provisioning-status ACTIVE --names-only
```

Equivalent direct KooCLI command (the script wraps exactly this call, with
marker paging):

```bash
hcloud ELB ListLoadbalancers --cli-region=cn-north-4 --limit=100
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--json` | No | Output the raw load balancer array as JSON (all fields; no Markdown) | — |
| `--names-only` | No | Output the load balancer name list only (also writes Markdown) | — |
| `--md-out` | No | Path of the standardized `id` + 名称 Markdown document (default `elb-list.md`) | `inventory/elb-list.md` |
| `--no-md` | No | Do not generate the Markdown document | — |
| `--id` | No | Filter by exact load balancer ID — real server-side query parameter | `lb-0001` |
| `--name` | No | Filter by load balancer name — real server-side query parameter | `lb-demo` |
| `--vpc-id` | No | Filter by the VPC the ELB belongs to — real server-side query parameter | `vpc-0001` |
| `--provisioning-status` | No | Filter by config state (`ACTIVE`/`PENDING_DELETE`) — real server-side query parameter | `ACTIVE` |
| `--operating-status` | No | Filter by operation state (`ONLINE`/`FROZEN`) — real server-side query parameter | `ONLINE` |
| `--enterprise-project-id` | No | Filter by enterprise project ID — real server-side query parameter | `0` |
| `--vip-address` | No | Filter by IPv4 private VIP address — real server-side query parameter | `192.168.0.10` |
| `--page-size` | No | Page size for ListLoadbalancers (default 100, range 0–2000) | `100` |
| `--project-id` | No | Project ID (needed by the SDK fallback path for `/v3/{project_id}/...`) | `05f...` |
| `--operation` | No | hcloud ELB operation name; only `ListLoadbalancers` is allowed | `ListLoadbalancers` |

Output-mode precedence: `--json` → `--names-only` → standardized table (default).
Markdown document generation applies to the default table and `--names-only` modes
(never to `--json`); `--no-md` disables it.

## Write-Intent Guard

- The script scans all user arguments plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `modify`, `clone`, `restore`,
  `enable`, `disable`, `associate`, `disassociate`, `detach`, `bind`, `unbind`,
  `release`, `remove`, `destroy`, `change`, `restart`, and ELB operation names
  such as `CreateLoadBalancer`, `DeleteLoadBalancer`, `UpdateLoadBalancer`,
  `CreateListener`, `DeletePool`, `CloneLoadbalancer`, `RestoreLoadbalancer`).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`,
  and exits with code 1 **before** a single hcloud command is executed.
- Only `hcloud ELB ListLoadbalancers` (GET) — or the SDK `list_load_balancers`
  call in the fallback path — is ever constructed by `build_command()`; there is
  no code path that can issue a mutating ELB API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...] [--key.1=value ...]
```

- **Service name** — exact KooCLI title-case service name: `ELB`.
- **Operation name** — PascalCase: `ListLoadbalancers`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (scalar; required for every concrete ELB call).
- **Scalar parameter** — `--key=value`, e.g. `--limit=100`, `--marker=<token>`.
- **Array parameter** — `--key.1=value`. The ListLoadbalancers filters `id`,
  `name`, `vpc_id`, `provisioning_status`, `operating_status`,
  `enterprise_project_id`, `vip_address` are **array-typed** in the OpenAPI
  model, so KooCLI requires the indexed form, e.g. `--id.1=lb-0001`,
  `--name.1=lb-demo`, `--vpc_id.1=vpc-0001`,
  `--provisioning_status.1=ACTIVE`, `--operating_status.1=ONLINE`,
  `--enterprise_project_id.1=0`, `--vip_address.1=192.168.0.10`. A bare
  `--id=lb-0001` is rejected with `[USE_ERROR]Invalid parameter`. For repeated
  values use `--key.1=v1 --key.2=v2` (the script sends one value per filter).
  All filters are real server-side ListLoadbalancers parameters (verified against
  the `huaweicloudsdkelb` v3 `ListLoadBalancersRequest` model).
- **Paging** — `--limit` + `--marker`; the marker is the `next_marker` returned
  in the response `page_info`. `limit` and `marker` must be used together.
- **REST path (official SDK `_http_info`)** —
  `GET /v3/{project_id}/elb/loadbalancers` (`huaweicloudsdkelb` v3
  `_list_load_balancers_http_info`); the project_id is resolved by KooCLI from
  the credential profile.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty load balancer list | Exit 0, prints `当前区域（<x>）无负载均衡器（ELB）` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问弹性负载均衡（ELB），请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| Missing project_id (SDK fallback) | Exit 1, hint to pass `--project-id` or set the project-id env var |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or run `scripts/ensure_env.py` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud ELB ListLoadbalancers --help` |
| Missing parent directory of `--md-out` | Created automatically (e.g. `inventory/elb-list.md` → `inventory/` is made first) |
| Markdown document cannot be written (`--md-out` path unwritable) | Exit 1, `[错误] 无法写入 Markdown 文档 <path>：<reason>` |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, API, or Markdown-write error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Non-`ACTIVE` load balancers | Reported with their state, not treated as failure |
| `--id` / `--name` / `--vpc-id` / `--provisioning-status` / `--operating-status` / `--enterprise-project-id` / `--vip-address` filters | Forwarded as real server-side query parameters using the KooCLI array form (`--key.1=value`, verified API params) |
| Large load balancer count | Automatic `marker` paging (`next_marker` aware, max 100 pages) |
| Extra response fields | Dropped from the standardized table (only `id` + `name`); available via `--json` |
| Field missing on a load balancer | `name` falls back to `id`; either missing renders as `-` |
| Nested arrays (`eips` / `publicips` / `availability_zone_list` / `tags`) | Not shown in the standardized table; present only in `--json` output |
| Markdown document path | Default `elb-list.md` in the current directory; `--md-out <path>` writes elsewhere and its missing parent directories are created automatically; `--no-md` disables; `--json` never writes it |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkelb` list_load_balancers, same output modes |
| User asks to create/delete/clone a load balancer | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / update / clone /
restore / change / normalized variants / operation whitelist), command
construction (filters forwarded server-side; marker never sent on the first
page), JSON extraction, failure classification (missing AK/SK, 403, generic,
`[USE_ERROR]` with rc=0), marker paging (next_marker / full page / empty), SDK
fallback (success, missing credentials, missing project id, and unavailable;
request construction matches the real `ListLoadBalancersRequest` signature),
standardization (`id` + `name` only, `name`→`id` fallback, `-` defaults),
rendering (standardized table / names / fallbacks), Markdown generation
(`| ID | 名称 |` table, empty document, `|` escaping, `--md-out` / `--no-md`,
`--json` never writes), and all main() output modes including empty, filter, and
error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |