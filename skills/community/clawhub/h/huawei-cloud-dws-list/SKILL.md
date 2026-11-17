---
name: huawei-cloud-dws-list
description: |
  1. List Huawei Cloud DWS (Data Warehouse Service / GaussDB(DWS)) clusters in a
     tenant region through KooCLI (hcloud DWS ListClusters — read-only
     GET /v1.0/{project_id}/clusters), with an automatic fallback to the official
     huaweicloudsdkdws v2 SDK when hcloud is not installed.
  2. Three output modes: full-field table (default, every returned field including
     名称/ID/状态/版本/规格/节点数/可用区/连接信息), --json (raw response array),
     and --names-only (compact cluster-name list).
  3. Supports --name / --status / --cluster-id filtering, --limit / --offset
     pagination, region override, and the real --enterprise-project-id API
     parameter. --name / --status / --cluster-id / --limit / --offset are applied
     client-side (the real ListClusters API exposes only enterprise_project_id).
  4. Explicit error hints for empty cluster lists (「当前区域无 DWS 集群」), 403 /
     insufficient IAM permission (「无权限访问 DWS，请检查 IAM 权限」), missing or
     invalid AK/SK credentials, and hcloud not installed.
  5. Built-in write-intent guard: any mutating intent (create / delete / update /
     resize / restart / stop / restore / upgrade / reboot) or any operation other
     than ListClusters is rejected before execution — this skill is strictly
     read-only.
  6. Triggers include: "list DWS clusters", "DWS cluster list", "DWS 集群列表",
     "查询DWS集群", "数据仓库集群列表", "GaussDB(DWS) 列表", "DWS inventory",
     "list data warehouse clusters", "华为云DWS集群".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, filters,
     pagination, error scenarios, SDK fallback, and the write-intent guard.
tags: [huawei-cloud, dws, data-warehouse, readonly, koo-cli]
---

# Huawei Cloud DWS Cluster List

## Overview

Query the DWS (Data Warehouse Service) cluster list of a tenant region through
KooCLI `hcloud DWS ListClusters` (official read-only
`GET /v1.0/{project_id}/clusters`, verified in the `huaweicloudsdkdws` v2 client
`_list_clusters_http_info` metadata — `resource_path: "/v1.0/{project_id}/clusters"`).
The skill is aimed at DWS inventory inspection, daily operations patrol, and as a
pre-query step for other DWS skills that need a `cluster_id`.

Architecture:

```text
agent → python3 scripts/list_dws.py → hcloud DWS ListClusters --cli-region=<region>
      → Huawei Cloud DWS OpenAPI (regional endpoint) → parsed JSON → table / --json / --names-only

(hcloud binary missing) → fallback: huaweicloudsdkdws v2 DwsClient.list_clusters
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListClusters` (GET). A
  write-intent guard scans user arguments and validates the operation name;
  mutating intents (create / delete / update / resize / restart / stop / restore
  / upgrade / reboot ...) are rejected with an explicit message before any
  command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  hcloud binary is absent, the script falls back to the official
  `huaweicloudsdkdws` v2 SDK (`list_clusters`). Credentials are always read by
  the CLI profile / SDK environment — never handled by the script.
- **Full-field table output** — the default table renders the union of all
  fields returned by ListClusters, with `endpoints` / `public_endpoints` /
  `public_ip` flattened into readable `endpoint` / `public_endpoint` /
  `publicIp` columns.
- **Client-side filters & paging** — the real ListClusters API has no name / id /
  status / limit / offset parameters (only `enterprise_project_id`); the script
  fetches the full list in a single call and applies those filters locally.
- **Offline-testable** — every code path (filters, paging, error classification,
  guard, SDK fallback) is covered by unit tests that mock the hcloud subprocess.

Out of scope: every mutating DWS action (create / delete / resize / restart /
stop / restore snapshot / reset password / upgrade / reboot). Those require a
dedicated write-capable skill and explicit user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkdws` to enable the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band
   (`hcloud configure` in your terminal, or credential environment variables).
   Never paste AK/SK into chat; the script never reads, echoes, or stores
   secrets itself — authentication is delegated entirely to the hcloud profile
   / SDK environment.
3. **IAM permission** — read-only DWS list permission; least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess).
5. **Outbound HTTPS** access to `*.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`); every DWS call is
   region-scoped.
2. **Confirm hcloud readiness** (optional, read-only): `hcloud configure list`.
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — table for humans, `--json` for downstream tooling,
   `--names-only` for a compact inventory.
5. **Handle the empty / error cases** per the Edge Cases table below (the
   script prints an explicit hint for empty region, 403, and missing AK/SK).

## Core Commands

```bash
# Full-field table (default)
python3 scripts/list_dws.py --region cn-north-4

# Raw JSON of every returned field
python3 scripts/list_dws.py --json

# Compact cluster-name list only
python3 scripts/list_dws.py --names-only

# Filter by cluster status (client-side exact, case-insensitive)
python3 scripts/list_dws.py --status AVAILABLE

# Filter by name (client-side substring) / exact ID
python3 scripts/list_dws.py --name dws-demo
python3 scripts/list_dws.py --cluster-id 6f8f7b0a-...

# Client-side pagination and the real enterprise-project API parameter
python3 scripts/list_dws.py --limit 20 --offset 0 --enterprise-project-id 0

# Combine filters
python3 scripts/list_dws.py --region cn-south-1 --status AVAILABLE \
  --limit 10 --names-only
```

Equivalent direct KooCLI command (the script wraps exactly this call):

```bash
hcloud DWS ListClusters --cli-region=cn-north-4
hcloud DWS ListClusters --cli-region=cn-north-4 --enterprise_project_id=0
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--json` | No | Output the raw cluster array as JSON | — |
| `--names-only` | No | Output cluster names only | — |
| `--name` | No | Filter by cluster name — **applied client-side** (case-insensitive substring; the ListClusters API has no name parameter) | `dws-demo` |
| `--status` | No | Filter by cluster state — **applied client-side** (case-insensitive exact; API has no status parameter) | `AVAILABLE`, `CREATING`, `FAILED` |
| `--cluster-id` | No | Filter by exact cluster ID — **applied client-side** | `6f8f7b0a-...` |
| `--limit` | No | Client-side pagination: max clusters returned (`0` = unlimited, default `0`) | `20` |
| `--offset` | No | Client-side pagination: skip the first N clusters (default `0`) | `20` |
| `--enterprise-project-id` | No | Enterprise project ID — **real ListClusters API parameter**, forwarded to hcloud/SDK | `0` (default project), `all_granted_eps` |
| `--operation` | No | hcloud DWS operation name; only `ListClusters` is allowed | `ListClusters` |

Output-mode precedence: `--names-only` → `--json` → table (default).
Filtering is applied before pagination: `filter (name/status/id) → slice
(offset/limit)`.

## Write-Intent Guard

- The script scans all user arguments plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `resize`, `restart`, `stop`,
  `restore`, `upgrade`, `reboot`, `scale`, `terminate`, `destroy`, and DWS
  operation names such as `CreateCluster`, `DeleteCluster`, `ResizeCluster`).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`,
  and exits with code 1 **before** a single hcloud command is executed.
- Only `hcloud DWS ListClusters` (GET) — or the SDK `list_clusters` call in the
  fallback path — is ever constructed by `build_command()`; there is no code
  path that can issue a mutating DWS API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `DWS`.
- **Operation name** — PascalCase: `ListClusters`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete DWS call).
- **Simple parameter** — `--key=value`, e.g. `--enterprise_project_id=0`.
  There is **no `--name` / `--status` / `--id` / `--limit` / `--offset`
  parameter** on the real DWS ListClusters API; those filters are applied
  client-side by the script, never forwarded to the CLI/API.
- **REST path (official SDK `_http_info`)** —
  `GET /v1.0/{project_id}/clusters` (`huaweicloudsdkdws` v2
  `_list_clusters_http_info`); project_id is resolved by KooCLI from the
  credential profile.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty cluster list | Exit 0, prints `当前区域（<x>）无 DWS 集群` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问 DWS，请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkdws` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud DWS ListClusters --help` |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| `CREATING` / `FAILED` clusters | Reported with their state, not treated as failure |
| `--status` / `--name` / `--cluster-id` filters | Applied client-side after the full list is fetched (the server API has only `enterprise_project_id`) |
| `--limit` / `--offset` | Client-side slice applied after filtering (the server API has no paging) |
| Large cluster count | Single ListClusters call returns the whole list; local slicing keeps memory/output bounded by `--limit` |
| Extra response fields | Table columns are built from the union of returned fields — new fields appear automatically |
| Field missing on a cluster | Rendered as `-` in the table |
| Nested `endpoints` / `public_endpoints` / `public_ip` | Flattened into `endpoint` / `public_endpoint` / `publicIp` for the table |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkdws` list_clusters, same output modes |
| User asks to create/delete/resize | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / resize / restart /
stop / restore / upgrade / reboot / normalize variants / operation whitelist),
command construction (including "no unsupported filter ever sent to the
server"), JSON extraction, failure classification (missing AK/SK, 403, generic,
`[USE_ERROR]` with rc=0), client-side filters (name substring / status exact /
id exact / no-match / missing field), client-side pagination (limit / offset /
combined / overflow), SDK fallback (success and unavailable; request
construction matches the real `ListClustersRequest` signature),
rendering (table with version/node_type/endpoint/publicIp fields / names /
fallbacks), and all main() output modes including empty, filter, paging and
error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |