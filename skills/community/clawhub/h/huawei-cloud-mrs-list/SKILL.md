---
name: huawei-cloud-mrs-list
description: |
  1. List Huawei Cloud MapReduce Service (MRS) clusters in a tenant region through KooCLI
     (hcloud MRS ListClusters — read-only GET /v1.1/{project_id}/cluster_infos).
  2. Three output modes: full-field table (default, every returned field), --json (raw
     response array), and --names-only (compact cluster-name list).
  3. Supports --cluster-state filtering (running / terminated / failed / abnormal ...),
     --cluster-name filtering, region override, and automatic currentPage paging.
  4. Explicit error hints for empty cluster lists, 403 / insufficient IAM permission,
     missing or invalid AK/SK credentials, and hcloud not installed.
  5. Built-in write-intent guard: any mutating intent (create / delete / update / scale /
     restart / terminate) or any operation other than ListClusters is rejected before
     execution — this skill is strictly read-only.
  6. Triggers include: "list MRS clusters", "MRS cluster list", "MRS 集群列表",
     "查询MRS集群", "MRS inventory", "list MapReduce Service clusters", "华为云MRS列表".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, filters, paging,
     error scenarios, and the write-intent guard.
tags: [huawei-cloud, mrs, bigdata, readonly, koo-cli]
---

# Huawei Cloud MRS Cluster List

## Overview

Query the MRS cluster list of a tenant region through KooCLI `hcloud MRS ListClusters`
(official read-only GET `/v1.1/{project_id}/cluster_infos`, verified in the
`huaweicloudsdkmrs` v1 client `_list_clusters_http_info` metadata). The skill is aimed at
MRS inventory inspection, daily operations patrol, and as a pre-query step for other MRS
skills that need a `cluster_id`.

Architecture:

```text
agent → python3 scripts/list_mrs.py → hcloud MRS ListClusters --cli-region=<region>
      → Huawei Cloud MRS OpenAPI (regional endpoint) → parsed JSON → table / --json / --names-only
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListClusters` (GET). A
  write-intent guard scans user arguments and validates the operation name; mutating
  intents (create / delete / update / scale / restart / terminate / submit job ...) are
  rejected with an explicit message before any command runs.
- **Full-field table output** — the default table renders the union of all fields
  returned by ListClusters (clusterId, clusterName, clusterState, billingType, version,
  node counts, enterprise project, tags, ...), not a trimmed subset.
- **Offline-testable** — every code path (paging, filters, error classification, guard)
  is covered by unit tests that mock the hcloud subprocess.

Out of scope: every mutating MRS action (create / delete / scale-out / scale-in /
restart / patch / submit or stop jobs). Those require a dedicated write-capable skill
and explicit user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
2. **Active credential profile** — configure credentials out-of-band
   (`hcloud configure` in your terminal, or credential environment variables). Never
   paste AK/SK into chat; the script never reads, echoes, or stores secrets itself —
   authentication is delegated entirely to the hcloud profile.
3. **IAM permission** — read-only `mrs:cluster:list`; least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess).
5. **Outbound HTTPS** access to `*.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`); every MRS call is region-scoped.
2. **Confirm hcloud readiness** (optional, read-only): `hcloud configure list`.
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — table for humans, `--json` for downstream tooling,
   `--names-only` for a compact inventory.
5. **Handle the empty / error cases** per the Edge Cases table below (the script prints
   an explicit hint for empty region, 403, and missing AK/SK).

## Core Commands

```bash
# Full-field table (default)
python3 scripts/list_mrs.py --region cn-north-4

# Raw JSON of every returned field
python3 scripts/list_mrs.py --json

# Compact cluster-name list only
python3 scripts/list_mrs.py --names-only

# Filter by cluster state
python3 scripts/list_mrs.py --cluster-state running

# Combine filters
python3 scripts/list_mrs.py --region cn-south-1 --cluster-state running --names-only
```

Equivalent direct KooCLI command (the script wraps exactly this call, with paging):

```bash
hcloud MRS ListClusters --cli-region=cn-north-4 --pageSize=10 --currentPage=1
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--json` | No | Output the raw cluster array as JSON | — |
| `--names-only` | No | Output cluster names only | — |
| `--cluster-state` | No | Filter by cluster state | `running`, `terminated`, `failed`, `abnormal` |
| `--cluster-name` | No | Filter by cluster name | `mrs-demo-01` |
| `--page-size` | No | Page size for ListClusters (default 10) | `10` |
| `--operation` | No | hcloud MRS operation name; only `ListClusters` is allowed | `ListClusters` |

Output-mode precedence: `--names-only` → `--json` → table (default).

## Write-Intent Guard

- The script scans all user arguments plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `scale`, `restart`, `terminate`, and MRS
  operation names such as `CreateCluster`, `DeleteCluster`, `ScaleOut`).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed.
- Only `hcloud MRS ListClusters` (GET) is ever constructed by `build_command()` — there
  is no code path that can issue a mutating MRS API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `MRS`.
- **Operation name** — PascalCase: `ListClusters`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete MRS call).
- **Simple parameter** — `--key=value`, e.g. `--clusterState=running`,
  `--pageSize=10`, `--currentPage=2`, `--clusterName=mrs-01`.
- **REST path (official SDK `_http_info`)** —
  `GET /v1.1/{project_id}/cluster_infos` (`huaweicloudsdkmrs` v1
  `_list_clusters_http_info`); project_id is resolved by KooCLI from the credential
  profile.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty cluster list | Exit 0, prints `Region <x> 下暂无 MRS 集群` (+ active filter) |
| 403 / insufficient IAM permission | Exit 1, explicit hint to check credentials and grant `mrs:cluster:list` |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| hcloud not installed | Exit 1, hint to install KooCLI (references/cli-installation-guide.md) |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| `terminated` clusters | Still returned by ListClusters; reported with their state, not treated as failure |
| Large cluster count | Automatic `currentPage` paging (total-count aware, full-page fallback, max 100 pages) |
| Extra response fields | Table columns are built from the union of returned fields — new fields appear automatically |
| Field missing on a cluster | Rendered as `-` in the table |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| User asks to create/delete/scale | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / scale / restart /
normalize variants / operation whitelist), command construction, JSON extraction,
failure classification (missing AK/SK, 403, generic), paging (total / full-page /
isFinished), output rendering (table full fields / names / fallbacks), and all main()
output modes including empty, filter, and error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
