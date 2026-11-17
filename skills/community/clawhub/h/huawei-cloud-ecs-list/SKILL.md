---
name: huawei-cloud-ecs-list
description: |
  1. List Huawei Cloud ECS (Elastic Cloud Server) instances in a tenant region
     through KooCLI (hcloud ECS ListServersDetails — read-only GET
     /v1/{project_id}/cloudservers/detail), with an automatic fallback to the
     official huaweicloudsdkecs v2 SDK when hcloud is not installed.
  2. Output modes: full-field table (default, every returned field including
     名称/ID/状态/规格(vCPU/内存)/可用区/私网IP/公网IP), --json (raw response
     array), and --names-only (compact instance-name + ID inventory). All output
     goes to stdout only — the script never writes a file.
  3. Supports --status / --name server-side filtering (both are real
     ListServersDetails query parameters), region override, and automatic offset
     paging.
  4. Explicit error hints for empty instance lists (「当前区域无 ECS 实例」), 403 /
     insufficient IAM permission (「无权限访问 ECS，请检查 IAM 权限」), missing or
     invalid AK/SK credentials, and hcloud not installed.
  5. Built-in write-intent guard: any mutating intent (create / delete / update /
     rebuild / resize / reboot / start / stop / attach / detach) or any operation
     other than ListServersDetails is rejected before execution — this skill is
     strictly read-only.
  6. Triggers include: "list ECS instances", "ECS instance list", "ECS 实例列表",
     "查询ECS实例", "云服务器列表", "ECS inventory", "list cloud servers",
     "华为云ECS列表".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, filters,
     paging, error scenarios, SDK fallback, and the write-intent guard.
tags: [huawei-cloud, ecs, compute, readonly, koo-cli]
---

# Huawei Cloud ECS Instance List

## Overview

Query the ECS instance list of a tenant region through KooCLI
`hcloud ECS ListServersDetails` (official read-only GET
`/v1/{project_id}/cloudservers/detail`, verified in the `huaweicloudsdkecs`
v2 client `_list_servers_details_http_info` metadata). The skill is aimed at
cloud resource inventory, daily operations patrol, and as a pre-query step for
other ECS skills that need a `server_id`.

Architecture:

```text
agent → python3 scripts/list_ecs.py → hcloud ECS ListServersDetails --cli-region=<region>
      → Huawei Cloud ECS OpenAPI (regional endpoint) → parsed JSON → table / --json / --names-only
                                                       → stdout only (no file is written)

(hcloud binary missing) → fallback: huaweicloudsdkecs v2 EcsClient.list_servers_details
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListServersDetails`
  (GET). A write-intent guard scans the user arguments and validates the
  operation name; mutating intents (create / delete / update / rebuild /
  resize / reboot / start / stop / attach / detach ...) are rejected with an
  explicit message before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  hcloud binary is absent, the script falls back to the official
  `huaweicloudsdkecs` v2 SDK (`list_servers_details`). Credentials are always
  read by the CLI profile / SDK environment — never handled by the script.
- **Full-field table output** — the default table renders the union of all
  fields returned by ListServersDetails, with `flavor` flattened into
  name/vcpus/ram, `addresses` split into private/public IPs, and the
  `OS-EXT-AZ:availability_zone` attribute surfaced as `availability_zone`.
- **Stdout only** — the script prints to stdout in every mode; it never creates
  or writes a file.
- **Offline-testable** — every code path (paging, filters, error
  classification, guard, SDK fallback) is covered by unit tests that mock the
  hcloud subprocess.

Out of scope: every mutating ECS action (create / delete / start / stop /
restart / resize flavor / rebuild / attach-detach volume / change image /
change password). Those require a dedicated write-capable skill and explicit
user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkecs` to enable the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band
   (`hcloud configure` in your terminal, or credential environment variables).
   Never paste AK/SK into chat; the script never reads, echoes, or stores
   secrets itself — authentication is delegated entirely to the hcloud profile
   / SDK environment.
3. **IAM permission** — read-only `ecs:servers:list`; least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess).
5. **Outbound HTTPS** access to `*.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`); every ECS call is
   region-scoped.
2. **Confirm hcloud readiness** (optional, read-only): `hcloud configure list`.
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — table for humans, `--json` for downstream tooling,
   `--names-only` for a compact inventory. Output is printed to stdout only; the
   script writes no file.
5. **Handle the empty / error cases** per the Error Handling table below (the
   script prints an explicit hint for empty region, 403, and missing AK/SK).

## Core Commands

```bash
# Full-field table (default)
python3 scripts/list_ecs.py --region cn-north-4

# Raw JSON of every returned field
python3 scripts/list_ecs.py --json

# Compact instance-name + ID inventory
python3 scripts/list_ecs.py --names-only

# Filter by instance status (server-side ECS query parameter)
python3 scripts/list_ecs.py --status ACTIVE

# Filter by instance name (server-side ECS query parameter, fuzzy)
python3 scripts/list_ecs.py --name ecs-web

# Combine filters
python3 scripts/list_ecs.py --region cn-south-1 --status ACTIVE --names-only
```

Equivalent direct KooCLI call (the script wraps exactly this operation, with
paging) — illustrative, requires KooCLI installed:

```text
hcloud ECS ListServersDetails --cli-region=cn-north-4 --limit=100 --offset=0
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--json` | No | Output the raw server array as JSON | — |
| `--names-only` | No | Output instance-name + ID inventory | — |
| `--status` | No | Filter by instance state — **server-side** ECS ListServersDetails parameter | `ACTIVE`, `BUILD`, `ERROR`, `SHUTOFF`, `REBUILD`, `RESIZE` |
| `--name` | No | Filter by instance name (server-side, fuzzy match) | `ecs-web` |
| `--page-size` | No | Page size for ListServersDetails (default 100) | `100` |
| `--operation` | No | hcloud ECS operation name; only `ListServersDetails` is allowed | `ListServersDetails` |

Output-mode precedence: `--names-only` → `--json` → table (default). In every
mode the rendered result is printed to stdout; the script never writes a file.

## Write-Intent Guard

- The script scans flag names plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `rebuild`, `resize`, `reboot`,
  `start`, `stop`, `attach`, `detach`, `server-action`, and ECS operation names
  such as `CreateServers`, `DeleteServers`, `BatchStartServers`).
- The values of read-only filter flags (`--status`, `--name`, `--region`,
  `--page-size`) are **not** scanned: they are query data and may legitimately
  contain write-looking words (e.g. the ECS status value `REBUILD`, or an
  instance named `restart-me`).
- A flag following such a filter flag is still scanned — `--status
  --create-server` cannot hide a mutating flag.
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed. The guard
  runs on the raw argv *before* argparse, so a mutating flag such as
  `--create-server` is reported as a guard violation rather than an
  "unrecognized argument" error.
- Only `hcloud ECS ListServersDetails` (GET) — or the SDK `list_servers_details`
  call in the fallback path — is ever constructed by `build_command()`; there
  is no code path that can issue a mutating ECS API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `ECS`.
- **Operation name** — PascalCase: `ListServersDetails`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete ECS call).
- **Simple parameter** — `--key=value`, e.g. `--limit=100`, `--offset=20`,
  `--status=ACTIVE`, `--name=ecs-web`.
- **REST path (official SDK `_http_info`)** —
  `GET /v1/{project_id}/cloudservers/detail` (`huaweicloudsdkecs` v2
  `_list_servers_details_http_info`); project_id is resolved by KooCLI from the
  credential profile.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty instance list | Exit 0, prints `当前区域（<x>）无 ECS 实例` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问 ECS，请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkecs` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud ECS ListServersDetails --help` |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| `SHUTOFF` / `ERROR` instances | Reported with their state, not treated as failure |
| `--status` filter | Forwarded to the ECS server as a real query parameter (the value is database-side); a database that accepts `REBUILD`/`RESIZE` etc. is not blocked by the guard |
| Large instance count | Automatic `offset` paging (`count` aware, full-page fallback, max 100 pages) |
| Extra response fields | Table columns are built from the union of returned fields — new fields appear automatically |
| Field missing on an instance | Rendered as `-` in the table |
| Nested `flavor` / `addresses` / `image` | Flattened into name/vcpus/ram / privateIps+publicIps / image_id for the table |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkecs` list_servers_details, same output modes |
| User asks to create/delete/start/stop/rebuild | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / rebuild / resize /
reboot / start / stop / attach / operation whitelist / filter values not
blocked / a flag after a filter flag still scanned), command construction
(status and name are real server-side params), JSON extraction, failure
classification (missing AK/SK, 403, generic, `[USE_ERROR]` with rc=0),
server-side status/name forwarding, paging (count / full-page / empty), SDK
fallback (success and unavailable; request construction matches the real
`ListServersDetailsRequest` signature), SDK field remapping
(`access_i_pv4` → `accessIPv4`, `os_ext_a_zavailability_zone` →
`OS-EXT-AZ:availability_zone`), rendering (table with flavor/IP/AZ fields /
names / summary lines / fallbacks), active-filter descriptions, and all main()
output modes including empty, filter, and error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
