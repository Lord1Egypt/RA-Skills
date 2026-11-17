---
name: huawei-cloud-sfs-list
description: |
  1. List Huawei Cloud SFS (Scalable File Service) file systems in a tenant
     region through KooCLI (`hcloud SFSTurbo ListShares` — read-only), with an
     automatic fallback to the official huaweicloudsdksfsturbo v1 SDK
     (SFSTurboClient.list_shares) when hcloud is not installed.
  2. Output modes: full-field aligned table (default, every returned field
     including 名称/ID/状态/协议/容量/可用区/类型/企业项目), --json (raw response
     array), --names-only (compact file-system name + ID inventory) and
     --count-only (just the number of matching file systems).
  3. Supports --region (default cn-north-4), --page-size with automatic
     limit/offset paging, and client-side --name / --id / --status /
     --share-proto / --az filtering (the SFS ListShares request itself only
     accepts limit/offset).
  4. Explicit error hints for empty file-system lists (「当前区域无 SFS 文件
     系统」), 403 / insufficient IAM permission (「无权限访问 SFS，请检查 IAM
     权限」), missing or invalid AK/SK credentials, hcloud not installed, and
     KooCLI usage errors.
  5. Built-in write-intent guard: any mutating intent (create / delete / expand
     / shrink / resize / mount / unmount / attach / detach / restore / reboot
     ...) or any operation other than the read-only ListShares is rejected
     before execution — this skill is strictly read-only.
  6. Triggers include: "list SFS file systems", "SFS file system list",
     "SFS 文件系统列表", "查询SFS文件系统", "查询文件系统列表", "SFS Turbo 列表",
     "文件存储列表", "SFS inventory", "list file systems", "华为云SFS列表".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, filters,
     paging, error scenarios, SDK fallback and the write-intent guard.
tags: [huawei-cloud, sfs, storage, readonly, koo-cli]
---

# Huawei Cloud SFS File System List

## Overview

Query the SFS (Scalable File Service) file-system list of a tenant region
through KooCLI `hcloud SFSTurbo ListShares` (read-only), with a fallback to the
official `huaweicloudsdksfsturbo` v1 SDK (`SFSTurboClient.list_shares`, GET
`/v1/{project_id}/sfs-turbo/shares/detail`). The skill is aimed at storage
resource inventory, daily operations patrol, and as a pre-query step for other
SFS skills that need a file-system ID.

Architecture:

```text
agent → python3 scripts/list_sfs.py → hcloud SFSTurbo ListShares --cli-region=<region>
      → Huawei Cloud SFS OpenAPI (regional endpoint) → parsed JSON → table / --json / --names-only

(hcloud binary missing) → fallback: huaweicloudsdksfsturbo v1 SFSTurboClient.list_shares
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListShares` (GET). A
  write-intent guard scans the user arguments and validates the operation name;
  mutating intents (create / delete / expand / shrink / resize / mount /
  unmount / attach / detach / restore / reboot ...) are rejected with an
  explicit message before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  hcloud binary is absent, the script falls back to the official
  `huaweicloudsdksfsturbo` v1 SDK (`list_shares`). Credentials are always read
  by the CLI profile / SDK environment — never handled by the script.
- **Full-field table output** — the default table renders the union of all
  fields returned by ListShares, with `availability_zone` surfaced explicitly
  and nested `metadata` JSON-encoded.
- **Client-side filtering** — SFS `ListShares` accepts only `limit` / `offset`,
  so `--name` / `--id` / `--status` / `--share-proto` / `--az` are applied
  locally after the paged query completes.
- **Offline-testable** — every code path (paging, filtering, error
  classification, guard, SDK fallback) is covered by unit tests that mock the
  hcloud subprocess.

> **Scope:** this skill lists **file systems**. It does not list objects inside
> a file system, does not report quota/usage, and does not list the SFS 3.0
> 「通用文件系统」 (`ListFileSystems`) product — those require a separate
> skill/Issue.

Out of scope: every mutating SFS action (create / delete / expand / shrink /
rename / ACL / permission rules / backend binding). Those require a dedicated
write-capable skill and explicit user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdksfsturbo` to
   enable the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band
   (`hcloud configure` in your terminal, or credential environment variables).
   Never paste AK/SK into chat; the script never reads, echoes, or stores
   secrets itself — authentication is delegated entirely to the hcloud profile
   / SDK environment.
3. **IAM permission** — read-only permission for listing SFS file systems;
   least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess / re).
5. **Outbound HTTPS** access to `sfs-turbo.<region>.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`); every SFS call is
   region-scoped.
2. **Confirm hcloud readiness** (optional, read-only): `hcloud configure list`.
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — table for humans, `--json` for downstream tooling,
   `--names-only` for a compact inventory.
5. **Handle the empty / error cases** per the Error Handling table below.

## Core Commands

```bash
# Full-field table (default)
python3 scripts/list_sfs.py --region cn-north-4

# Raw JSON of every returned field
python3 scripts/list_sfs.py --json

# Compact file-system name + ID inventory
python3 scripts/list_sfs.py --names-only

# Just the number of matching file systems
python3 scripts/list_sfs.py --count-only

# Filter by name / id (client-side, case-insensitive substring)
python3 scripts/list_sfs.py --name sfs-prod
python3 scripts/list_sfs.py --id 8be2f1a3

# Filter by status / protocol (client-side, exact)
python3 scripts/list_sfs.py --status available
python3 scripts/list_sfs.py --share-proto NFS

# Filter by availability zone (client-side, case-insensitive substring)
python3 scripts/list_sfs.py --az cn-north-4a

# Combine filters + custom page size
python3 scripts/list_sfs.py --region cn-south-1 --share-proto NFS --az cn-south-1a --names-only --page-size 100
```

Equivalent direct KooCLI command (the script wraps exactly this call, with
paging):

```bash
hcloud SFSTurbo ListShares --cli-region=cn-north-4 --limit=200 --offset=0
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--json` | No | Output the raw file-system array as JSON | — |
| `--names-only` | No | Output a compact name + ID inventory | — |
| `--count-only` | No | Output only the number of matching file systems | — |
| `--name` | No | Filter by file-system name (client-side substring) | `sfs-prod` |
| `--id` | No | Filter by file-system ID (client-side substring) | `8be2f1a3` |
| `--status` | No | Filter by status (client-side exact) | `available` |
| `--share-proto` | No | Filter by protocol (client-side exact) | `NFS`, `CIFS` |
| `--az` | No | Filter by availability zone (client-side substring) | `cn-north-4a` |
| `--page-size` | No | Page size for ListShares (default `200`, max `200`; values outside `[1, 200]` are clamped) | `100` |
| `--operation` | No | hcloud SFSTurbo operation name; only `ListShares` is allowed | `ListShares` |

Output-mode precedence: `--count-only` → `--names-only` → `--json` → table (default).

## Write-Intent Guard

- The script scans flag names plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `expand`, `shrink`, `resize`,
  `mount`, `unmount`, `attach`, `detach`, `restore`, `reboot`, and SFS
  operation names such as `CreateShare`, `DeleteShare`, `ExpandShare`).
- The values of the read-only filter flags (`--name`, `--id`, `--status`,
  `--share-proto`, `--az`, `--region`, `--page-size`, `--limit`, `--offset`)
  are **not** scanned: they are query data and may legitimately contain
  write-looking words (e.g. a file system named `delete-test`).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed. The guard
  runs on the raw argv *before* argparse, so a mutating flag such as
  `--create-share` is reported as a guard violation rather than an
  "unrecognized argument" error.
- Only `hcloud SFSTurbo ListShares` (GET) — or the SDK `list_shares` call in the
  fallback path — is ever constructed by `build_command()`; there is no code
  path that can issue a mutating SFS API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `SFSTurbo`
  (KooCLI's file-storage service; `SFS` is not a registered KooCLI service).
- **Operation name** — PascalCase: `ListShares`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete SFS call).
- **Simple parameter** — `--key=value`, e.g. `--limit=200`, `--offset=20`.
- **REST path (official SDK `_http_info`)** —
  `GET /v1/{project_id}/sfs-turbo/shares/detail`
  (`huaweicloudsdksfsturbo` v1 `_list_shares_http_info`); project_id is
  resolved by KooCLI from the credential profile.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty file-system list | Exit 0, prints `当前区域（<x>）无 SFS 文件系统` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问 SFS，请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkcore huaweicloudsdksfsturbo` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud SFSTurbo ListShares --help` |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| `creating` / `error` file systems | Reported with their state, not treated as failure |
| `--name` / `--id` / `--az` filter | Applied client-side (case-insensitive substring) after the full paged query — the SFS request itself has no such parameters |
| Large file-system count | Automatic `offset` paging (`count` aware, full-page fallback, max 100 pages) |
| `--page-size` above the API cap | Clamped to `200` (SFS Turbo `ListShares` rejects `limit > 200`); below `1` clamped to `1` |
| Extra response fields | Table columns are built from the union of returned fields — new fields appear automatically |
| Field missing on a file system | Rendered as `-` in the table |
| Nested `metadata` | JSON-encoded in the table cell |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdksfsturbo` list_shares, same output modes |
| User asks to create/delete/expand/mount | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / expand / shrink /
resize / mount / unmount / attach / detach / restore / reboot / operation
whitelist / filter values not blocked / `--offset` not blocked), command
construction (limit + offset, no write flags), JSON extraction (plain / wrapped
/ list / invalid), file-system extraction (`shares` / `file_systems` / bare
list), failure classification (missing AK/SK, 403, generic, `[USE_ERROR]` with
rc=0), paging (count-aware multi-page), SDK fallback (success and unavailable,
request construction, `ShareInfo` attribute remapping), client-side filtering
(name / id / status / protocol / az / descriptions), rendering (table with the
preferred columns / names / summary lines / fallbacks), and all `main()` output
modes (table / json / names / count-only) including empty, filter, and error
paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |