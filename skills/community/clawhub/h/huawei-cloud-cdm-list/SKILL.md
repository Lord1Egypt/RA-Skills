---
name: huawei-cloud-cdm-list
description: |
  1. Query the Huawei Cloud CDM (Cloud Data Migration) clusters of the current
     account through KooCLI (`hcloud CDM ListClusters --cli-region=<region>`;
     official read-only GET /v1.1/{project_id}/clusters), with an automatic
     fallback to the huaweicloudsdkcdm v1 SDK (CdmClient) when KooCLI is
     absent.
  2. Two read-only views: the project-wide cluster list (default,
     ListClusters) and single-cluster details incl. instance status
     (ShowClusterDetail, GET /v1.1/{project_id}/clusters/{cluster_id}) via
     --cluster-id.
  3. Four output modes: aligned key-field table (default: id / name / status /
     status_detail / status_meaning / version / instance_count / instances /
     flavor_name / az_name / public_endpoint / is_frozen / created / updated),
     `--json` (raw API records), `--markdown` (GitHub-flavored table) and
     `--csv`; `--output` writes a file via a temp file + atomic rename.
  4. Filters: `--name` (case-insensitive substring) and repeatable `--status`
     (status code 100/200/300/303/500/800/900/910/920 or Chinese meaning such
     as 正常/失败/冻结), both applied client-side — the official ListClusters
     API takes no query parameters at all (verified against
     ListClustersRequest.attribute_map being empty), so one call returns the
     whole list.
  5. Explicit error hints for empty cluster lists, 403 / missing
     `cdm:cluster:list` permission, missing AK/SK credentials, a missing KooCLI
     backend, and bad export paths.
  6. Built-in write-intent guard: any mutating intent (create / delete /
     update / restart / resize / start / stop / expand ...) or any operation
     outside the two read-only ones is rejected before execution — this skill
     is strictly read-only.
  7. Triggers include: "CDM 集群列表", "查询云数据迁移集群", "CDM 集群巡检",
     "cdm list clusters", "CDM cluster status", "迁移前集群盘点",
     "CDM 集群详情", "华为云 CDM 集群".
tags: [huawei-cloud, cdm, cloud-data-migration, readonly, koo-cli]
---

# Huawei Cloud CDM Cluster List

## Overview

Query the Huawei Cloud CDM (Cloud Data Migration, 云数据迁移) clusters of the
current account through KooCLI `hcloud CDM ListClusters
--cli-region=<region>` (official read-only GET
`/v1.1/{project_id}/clusters`, verified in the `huaweicloudsdkcdm` v1 client
`_list_clusters_http_info` metadata), plus single-cluster details via
`hcloud CDM ShowClusterDetail --cluster_id=<uuid>`. The skill is aimed at
daily ops inspection / 巡检, pre-migration cluster inventory (迁移前盘点),
and troubleshooting failed or frozen clusters.

Architecture:

```text
agent → python3 scripts/list_cdm_clusters.py → skill-quality-cli ─▶ hcloud CDM ListClusters | ShowClusterDetail --cli-region=<region>
      → Huawei Cloud CDM OpenAPI → parsed JSON → table / json / markdown / csv

(hcloud binary missing) → fallback: huaweicloudsdkcdm v1 CdmClient (BasicCredentials; project_id auto-resolved via IAM)
(missing SDK)           → run scripts/ensure_env.py  (auto pip install)
```

Key properties:

- **Read-only by design** — the only operations ever constructed are
  `ListClusters` and `ShowClusterDetail` (both GET). A write-intent guard
  scans the user arguments and validates the operation name; mutating intents
  (create / delete / update / restart / resize / start / stop / expand ...) and
  CDM write operations (CreateCluster / DeleteCluster / RestartCluster /
  StartCluster / StopCluster / ModifyCluster ...) are rejected with an explicit
  message before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path (wrapped
  with `skill-quality-cli` for telemetry); when the hcloud binary is absent, the
  script falls back to the official `huaweicloudsdkcdm` v1 SDK. Credentials are
  always read by the CLI profile / SDK environment — never handled by the
  script. `BasicCredentials` may omit the project id: the SDK queries IAM and
  resolves it for the region automatically.
- **No fake paging** — the official ListClusters API takes no query parameters
  (verified: `ListClustersRequest.attribute_map == {}`), so one call returns
  the full list; `--max-calls` is only a defensive ceiling and is never sent to
  the API. Repeated calls return the same page, so records are de-duplicated by
  cluster id and the loop stops once a call adds nothing new.
- **Client-side filtering** — `--name` and repeatable `--status` (code or
  Chinese meaning, multi-value = union) filter the returned clusters locally.
- **Offline-testable** — the guard, command construction, error classification
  (including the permission envelope returned on stdout with rc=0), client-side
  filters, SDK fallback, renderers, atomic export and a real-subprocess fake
  hcloud binary are covered by offline unit tests (no credentials, no network).

> **Dependency**: Quality telemetry is collected automatically via skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

> **Capability boundary:** this skill **lists/queries** CDM clusters and their
> details only. It does not create, delete, restart, resize or reconfigure
> clusters, does not touch CDM jobs/links (作业/连接), and never writes anything
> back to the cloud. Those require a separate skill and explicit user
> confirmation (确认).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — the primary execution path; see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   When absent, the SDK fallback is used.
2. **Python 3.8+** with the Huawei Cloud SDK — run
   `python3 scripts/ensure_env.py` to install `huaweicloudsdkcore` and
   `huaweicloudsdkcdm` automatically. Rendering itself needs only the standard
   library.
3. **Credentials configured out-of-band** — the CLI reads the active hcloud
   profile; the SDK fallback reads AK/SK from the whitelisted environment
   variables (`HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`, `CLOUD_SDK_AK` /
   `CLOUD_SDK_SK`, `HUAWEI_*` / `HW_*` / `HWC_*`, plus optional
   `HUAWEICLOUD_SDK_PROJECT_ID`). Never paste AK/SK into chat; the script
   never reads, echoes or stores secrets itself.
4. **IAM permission** — read-only `cdm:cluster:list` (ListClusters) and
   `cdm:cluster:get` (ShowClusterDetail); least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
5. **Region** — `cn-north-4` by default (CDM endpoint
   `https://cdm.<region>.myhuaweicloud.com`).
6. **Outbound HTTPS** access to the CDM OpenAPI endpoint.
- **skill-quality-cli** — ensured by bash scripts/ensure_cli.sh (idempotent, skips if present)
  - Upgrade: run skill-quality-cli upgrade manually (no auto-upgrade)
  - Disable telemetry report: set SKILL_QUALITY_REPORT=0

## Workflow

1. **(Optional) prepare the environment** — `python3 scripts/ensure_env.py`
   installs any missing SDK dependency.
2. **Pick filters** — `--name` for a name substring, repeatable `--status`
   for status codes or Chinese meanings (e.g. `--status 300 --status 303`,
   `--status 冻结`); combine freely.
3. **Run the script** with the desired `--format` and `--output`.
4. **Single-cluster details** — pass `--cluster-id <uuid>` (obtained from the
   list view) to switch to ShowClusterDetail with instance-level status/IPs.
5. **Read the result** — the table prints to stdout; file formats print the
   written path. An empty result is reported explicitly and still writes a
   valid header-only file.
6. **Handle the empty / error cases** per the Error Handling table below.

## Core Commands

> **⚠️ Mandatory quality wrapping: `scripts/list_cdm_clusters.py` builds every `hcloud` CLI call as `skill-quality-cli run --skill-name huawei-cloud-cdm-list -- hcloud ...` (enforced in code, not left to the agent). If `skill-quality-cli` is unavailable (run `bash scripts/ensure_cli.sh`) or `SKILL_QUALITY_REPORT=0`, the CLI path degrades to bare `hcloud` (no telemetry) — the read-only semantics and the CLI→SDK fallback are unchanged. When the `hcloud` binary itself is not resolvable, the wrapping is skipped and the bare command runs, so the missing binary surfaces as `FileNotFoundError` → `ConfigError` and the SDK fallback still triggers.**

```bash
# Default: project-wide CDM cluster list (ListClusters) as a table
python3 scripts/list_cdm_clusters.py --region cn-north-4

# Filter client-side by name substring / status codes or meanings
python3 scripts/list_cdm_clusters.py --name cdm-                 # 名称含 cdm-
python3 scripts/list_cdm_clusters.py --status 200                # 仅正常集群
python3 scripts/list_cdm_clusters.py --status 300 --status 303   # 失败 + 创建失败
python3 scripts/list_cdm_clusters.py --status 冻结               # 冻结集群

# Single-cluster details incl. instance status (ShowClusterDetail)
python3 scripts/list_cdm_clusters.py --cluster-id bae65496-643e-47ca-84af-948672de7eeb

# Export the cluster list to a JSON / Markdown / CSV file
python3 scripts/list_cdm_clusters.py --format json --output /tmp/cdm_clusters.json
python3 scripts/list_cdm_clusters.py --format markdown --summary --output /tmp/cdm_clusters.md
python3 scripts/list_cdm_clusters.py --format csv --output /tmp/cdm_clusters.csv

# Read-only credential readiness check (also wrapped)
skill-quality-cli run --skill-name huawei-cloud-cdm-list -- hcloud configure list
```

Equivalent direct KooCLI commands (the script wraps exactly these calls):

```bash
hcloud CDM ListClusters --cli-region=cn-north-4
hcloud CDM ShowClusterDetail --cli-region=cn-north-4 --cluster_id=bae65496-643e-47ca-84af-948672de7eeb
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--format` / `-f` | No | Output mode: `table` (default) / `json` / `markdown`(`md`) / `csv` | `--format json` |
| `--output` / `-o` | No | Export file path (json/markdown/csv; default `cdm_<view>_<region>_<timestamp>.<ext>`) | `/tmp/cdm.json` |
| `--summary` | No | Append a summary line to the Markdown report | `--summary` |
| `--cluster-id` | No | Cluster ID — switches to ShowClusterDetail (details incl. instance status) | `bae65496-...` |
| `--name` | No | Filter by cluster-name substring, case-insensitive (client-side) | `cdm-prod` |
| `--status` | No | Filter by status, repeatable (union): codes `100/200/300/303/500/800/900/910/920` or meanings `创建中/正常/失败/创建失败/重启中/冻结/已关机/...` (client-side) | `--status 200` |
| `--max-calls` | No | Defensive call ceiling for ListClusters (default 1; the official API has no paging parameters — never sent to the API; repeated results are de-duped by cluster id) | `1` |
| `--operation` | No | Explicit read-only operation (`ListClusters` / `ShowClusterDetail`) | — |

Output-mode precedence: `--format` selects the mode; `--output` only matters for
the file formats (`json` / `markdown` / `csv`); `table` writes to stdout. The
local `--output` path value (e.g. a file literally named
`cdm-delete-report.json`) and the filter values are excluded from the
write-intent guard because they are not CDM operations.

## Cluster status reference

| Code | Meaning |
| ------ | --------- |
| 100 | 创建中 |
| 200 | 正常 |
| 300 | 失败 |
| 303 | 创建失败 |
| 500 | 重启中 |
| 800 | 冻结 |
| 900 | 已关机 |
| 910 | 正在关机 |
| 920 | 正在开机 |

## Write-Intent Guard

- The script scans all user arguments (except the values of the read-only filter
  flags and of the local-output/format flags) plus the operation name for
  mutating vocabulary (`create`, `delete`, `update`, `modify`, `restart`,
  `resize`, `start`, `stop`, `expand`, and CDM operation names such as
  `CreateCluster`, `DeleteCluster`, `RestartCluster`, `StartCluster`,
  `StopCluster`, `ModifyCluster`).
- Any hit raises `GuardError`, prints
  `[错误] 检测到写操作意图 ... 已被守卫拦截`, and exits with code 1 **before** a
  single hcloud command is executed.
- Only `ListClusters` / `ShowClusterDetail` (both GET) are ever constructed by
  `build_command()`; there is no code path that can issue a mutating CDM API
  call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `CDM`.
- **Operation name** — PascalCase API operation: `ListClusters`,
  `ShowClusterDetail` (the cluster-detail API; the API-explorer title is
  查询集群详情 — there is no `ShowCluster` operation in KooCLI or the SDK).
- **Region parameter** — always pass `--cli-region=<region>`, e.g.
  `--cli-region=cn-north-4`.
- **Simple parameters** — `--key=value`, e.g. `--cluster_id=<uuid>`.
  ListClusters takes **no** query parameters (official API fact); the detail
  view takes only the `cluster_id` path parameter.
- **REST paths (official SDK `_http_info`)** —
  `GET /v1.1/{project_id}/clusters` (ListClusters),
  `GET /v1.1/{project_id}/clusters/{cluster_id}` (ShowClusterDetail).

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty cluster list / no filter match | Exit 0, prints `当前区域（<x>）无 CDM 集群` (+ active filters); a header-only export file is still written |
| 403 / missing `cdm:cluster:list` / `cdm:cluster:get` | Exit 1, `无权限访问云数据迁移服务（CDM），请检查 IAM 权限` hint; the envelope is detected even on stdout with rc=0 |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| hcloud not installed | Falls back to the SDK; if the SDK is unavailable too, exit 1 with a clear hint (运行 `python3 scripts/ensure_env.py`) |
| Bad `--output` path (permission / bad dir) | Exit 1, `导出文件写出失败` hint; no partial file is left |
| `--cluster-id` with `--operation ListClusters` | Exit 1, explicit hint that the combination requires ShowClusterDetail |
| KooCLI usage error (`[USE_ERROR] ...`, even with rc=0) | Exit 1, explicit hcloud 参数错误 hint pointing to `hcloud CDM ListClusters --help` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty list; `1` config, auth, guard, export, or API
error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Region has no clusters | Friendly message + a header-only export file, exit 0 |
| `--name` / `--status` filters | Applied client-side (CDM API has no server-side filters); status matches code OR Chinese meaning; multi-status = union |
| Large cluster count | Single full-list call (official API has no paging parameters); `--max-calls` stays a defensive ceiling and duplicates are de-duped by cluster id |
| Extra response fields | Table/CSV columns are built from the union of returned fields (camelCase normalized to snake_case); raw nested objects already represented by a derived column are dropped from table/CSV/detail |
| Field missing on a record | Rendered as `-` |
| Nested `datastore` / `instances` | `version` = datastore.version, `datastore_type` = datastore.type (raw `datastore` kept in JSON only); `instances` flattened to `name(status); ...` + `instance_count` (raw list kept in JSON) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkcdm`, same output modes; BasicCredentials resolves project_id via IAM when omitted |
| `--output` points to a non-existing directory | Directory is created automatically |
| `--output` path contains a guard keyword | Path value is excluded from the guard (local path ≠ CDM operation) |
| Detail view requested | Field/value table (or markdown two-column table) incl. per-instance status/IPs |
| User asks to create/delete/restart a CDM cluster or manage jobs/links | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation (确认) is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network),
run from the skill directory:

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / restart / stop /
normalized variants / operation whitelist / value-flag exclusion / following-flag
still scanned / extra hcloud args scanned / main argv interception), operation
resolution, command construction (ListClusters parameter-free assertion,
ShowClusterDetail cluster_id, language, REST paths), JSON extraction and
error-envelope classification (incl. the permission envelope on stdout with
rc=0), client-side name/status filters (code, meaning, union, empty),
normalization (camelCase→snake_case, derived version/instance_count/status
meaning), SDK fallback (missing hcloud / missing env credentials / missing
package), rendering (table / Markdown / CSV / JSON / detail views) and atomic
export, plus an end-to-end run through a real subprocess with a fake hcloud
binary and `--help` exit-code 0.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI + SDK installation, credential configuration and skill-quality-cli |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
