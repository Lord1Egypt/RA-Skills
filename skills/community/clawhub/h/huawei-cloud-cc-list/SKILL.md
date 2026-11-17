---
name: huawei-cloud-cc-list
description: |
  1. List Huawei Cloud Cloud Connect (CC) instances in a tenant region through
     KooCLI (hcloud CC ListCloudConnections — read-only GET
     /v3/{domain_id}/ccaas/cloud-connections), with an automatic fallback to the
     official huaweicloudsdkcc v3 SDK when hcloud is not installed.
  2. Three output modes: full-field table (default, every returned field including
     名称/ID/状态/带宽/网络实例数/企业项目), --json (raw response array), and
     --names-only (compact instance-name list).
  3. Supports --name / --status / --id filtering (all real server-side
     ListCloudConnections query parameters), region override, and automatic
     marker paging.
  4. Explicit error hints for empty instance lists (「当前区域无云连接（CC）实例」),
     403 / insufficient IAM permission (「无权限访问云连接（CC）」), missing or
     invalid AK/SK credentials, and hcloud not installed.
  5. Built-in write-intent guard: any mutating intent (create / delete / update /
     associate / disassociate / attach / detach / restart) or any operation other
     than ListCloudConnections is rejected before execution — this skill is
     strictly read-only.
  6. Triggers include: "list CC instances", "cloud connect list", "云连接列表",
     "查询云连接", "CC 实例列表", "cloud connection inventory", "list cloud
     connections", "华为云云连接".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, filters,
     marker paging, error scenarios, SDK fallback, and the write-intent guard.
tags: [huawei-cloud, cc, network, readonly, koo-cli]
---

# Huawei Cloud Cloud Connect (CC) Instance List

## Overview

Query the Cloud Connect (CC) instance list of a tenant through KooCLI
`hcloud CC ListCloudConnections` (official read-only GET
`/v3/{domain_id}/ccaas/cloud-connections`, verified in the `huaweicloudsdkcc` v3
client `_list_cloud_connections_http_info` metadata). The skill is aimed at CC
inventory inspection, daily operations patrol, and as a pre-query step for other
CC skills that need a `cloud_connection_id`.

Architecture:

```text
agent → python3 scripts/list_cc.py → hcloud CC ListCloudConnections --cli-region=<region>
      → Huawei Cloud CC OpenAPI (global endpoint) → parsed JSON → table / --json / --names-only

(hcloud binary missing) → fallback: huaweicloudsdkcc v3 CcClient.list_cloud_connections
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListCloudConnections`
  (GET). A write-intent guard scans user arguments and validates the operation
  name; mutating intents (create / delete / update / associate / disassociate /
  attach / detach / restart ...) are rejected with an explicit message before any
  command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  KooCLI binary is absent, the script falls back to the official
  `huaweicloudsdkcc` v3 SDK (`list_cloud_connections`). Credentials are always
  read by the CLI profile / SDK environment — never handled by the script.
- **Full-field table output** — the default table renders the union of all
  fields returned by ListCloudConnections, with `tags` flattened for
  readability.
- **Offline-testable** — every code path (marker paging, filters, error
  classification, guard, SDK fallback) is covered by unit tests that mock the
  hcloud subprocess.

Out of scope: every mutating CC action (create / update / delete a cloud
connection, bandwidth-package association, network-instance attach/detach,
inter-region bandwidth, central-network management). Those require a dedicated
write-capable skill and explicit user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcc` to enable the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band
   (run the KooCLI configure command in your terminal, or set credential
   environment variables).
   Never paste AK/SK into chat; the script never reads, echoes, or stores
   secrets itself — authentication is delegated entirely to the hcloud profile
   / SDK environment.
3. **IAM permission** — read-only `cc:cloudConnections:list`; least-privilege
   policy in [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess).
5. **Outbound HTTPS** access to `cc.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`); CC instances are
   queried through the CC global endpoint but the credential project is
   region-scoped.
2. **Confirm KooCLI readiness** (optional, read-only) by listing the active
   credential profile.
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — table for humans, `--json` for downstream tooling,
   `--names-only` for a compact inventory.
5. **Handle the empty / error cases** per the Edge Cases table below (the
   script prints an explicit hint for empty region, 403, and missing AK/SK).

## Core Commands

```bash
# Full-field table (default)
python3 scripts/list_cc.py --region cn-north-4

# Raw JSON of every returned field
python3 scripts/list_cc.py --json

# Compact instance-name list only
python3 scripts/list_cc.py --names-only

# Filter by instance status (server-side query parameter)
python3 scripts/list_cc.py --status ACTIVE

# Filter by name / id
python3 scripts/list_cc.py --name cc-demo

# Combine filters
python3 scripts/list_cc.py --region cn-north-4 --status ACTIVE --names-only
```

Equivalent direct KooCLI command (the script wraps exactly this call, with
marker paging):

```bash
hcloud CC ListCloudConnections --cli-region=cn-north-4 --limit=100
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--json` | No | Output the raw instance array as JSON | — |
| `--names-only` | No | Output instance names only | — |
| `--status` | No | Filter by instance state — real server-side ListCloudConnections query parameter (case-insensitive on the service side) | `ACTIVE` |
| `--name` | No | Filter by instance name — real server-side query parameter | `cc-demo-01` |
| `--id` | No | Filter by exact instance ID — real server-side query parameter | `cc-0001` |
| `--page-size` | No | Page size for ListCloudConnections (default 100, range 1–2000) | `100` |
| `--operation` | No | hcloud CC operation name; only `ListCloudConnections` is allowed | `ListCloudConnections` |

Output-mode precedence: `--names-only` → `--json` → table (default).

## Write-Intent Guard

- The script scans all user arguments plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `modify`, `associate`,
  `disassociate`, `attach`, `detach`, `restart`, `stop`, and CC operation names
  such as `CreateCloudConnection`, `DeleteCloudConnection`,
  `UpdateCloudConnection`).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed.
- Only `hcloud CC ListCloudConnections` (GET) — or the SDK
  `list_cloud_connections` call in the fallback path — is ever constructed by
  `build_command()`; there is no code path that can issue a mutating CC API
  call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `CC`.
- **Operation name** — PascalCase: `ListCloudConnections`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete CC call).
- **Simple parameter** — `--key=value`, e.g. `--limit=100`, `--marker=<token>`,
  `--name=cc-01`, `--status=ACTIVE`, `--id=cc-0001`. All three filters are real
  server-side ListCloudConnections parameters (verified against the
  `huaweicloudsdkcc` v3 `ListCloudConnectionsRequest` model).
- **Paging** — `--limit` + `--marker`; the marker is the `next_marker` returned
  in the response `page_info`. `limit` and `marker` must be used together.
- **REST path (official SDK `_http_info`)** —
  `GET /v3/{domain_id}/ccaas/cloud-connections` (`huaweicloudsdkcc` v3
  `_list_cloud_connections_http_info`); the domain_id is resolved by KooCLI
  from the credential profile.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty instance list | Exit 0, prints `当前区域（<x>）无云连接（CC）实例` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问云连接（CC），请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkcc` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud CC ListCloudConnections --help` |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Non-`ACTIVE` instances | Reported with their state, not treated as failure |
| `--status` / `--name` / `--id` filters | Forwarded as real server-side query parameters (verified API params) |
| Large instance count | Automatic `marker` paging (`next_marker` aware, max 100 pages) |
| Extra response fields | Table columns are built from the union of returned fields — new fields appear automatically |
| Field missing on an instance | Rendered as `-` in the table |
| Nested `tags` | Flattened into `key=value,...` for the table |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkcc` list_cloud_connections, same output modes |
| User asks to create/delete/update a connection | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / update /
associate / restart / normalized variants / operation whitelist), command
construction (filters forwarded server-side; marker never sent on the first
page), JSON extraction, failure classification (missing AK/SK, 403, generic,
`[USE_ERROR]` with rc=0), marker paging (next_marker / full page / empty), SDK
fallback (success and unavailable; request construction matches the real
`ListCloudConnectionsRequest` signature), rendering (table with
bandwidth/network fields / names / fallbacks), and all main() output modes
including empty, filter, and error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
