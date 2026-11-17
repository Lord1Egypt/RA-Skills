---
name: huawei-cloud-cbr-list
description: |
  1. List Huawei Cloud CBR (Cloud Backup and Recovery) backups in a tenant
     region through KooCLI (`hcloud CBR ListBackups --cli-region=<region>` — read-only), with an
     automatic fallback to the official huaweicloudsdkcbr v1 SDK
     (CbrClient.list_backups) when hcloud is not installed.
  2. Output modes: full-field aligned table (default, every returned field
     including 名称/ID/状态/所属资源/资源类型/vault_id/创建时间), --json (raw
     response array) and --names-only (compact backup name + ID inventory).
  3. Supports --region (default cn-north-4), --page-size with automatic
     limit/offset paging, and the native ListBackups filters --name / --status /
     --resource_id / --resource_name / --resource_type / --vault_id /
     --image_type (with a client-side re-filter for the rendered rows).
  4. Explicit error hints for empty backup lists (「当前区域无 CBR 备份」),
     403 / insufficient IAM permission (「无权限访问 CBR，请检查 IAM 权限」),
     missing or invalid AK/SK credentials, hcloud not installed, and KooCLI
     usage errors.
  5. Built-in write-intent guard: any mutating intent (create / delete / restore
     / copy / import / replicate / update / migrate / associate / bind / ...) or
     any operation other than the read-only ListBackups is rejected before
     execution — this skill is strictly read-only.
  6. Triggers include: "list CBR backups", "CBR backup list",
     "CBR 备份列表", "查询CBR备份", "查询备份列表", "云备份列表", "备份清单查询",
     "备份资源巡检", "备份容量盘点", "CBR inventory", "list backups",
     "华为云备份查询", "华为云CBR列表".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, filters,
     paging, error scenarios, SDK fallback and the write-intent guard.
tags: [huawei-cloud, cbr, storage, readonly, koo-cli]
---

# Huawei Cloud CBR Backup List

## Overview

Query the CBR (Cloud Backup and Recovery) backup list of a tenant region through
KooCLI `hcloud CBR ListBackups --cli-region=<region>` (read-only), with a fallback to the official
`huaweicloudsdkcbr` v1 SDK (`CbrClient.list_backups`, GET
`/v3/{project_id}/backups`). The skill is aimed at backup-resource inventory,
daily operations patrol, capacity accounting, and as a pre-query step for other
backup skills that need a backup ID.

Architecture:

```text
agent → python3 scripts/list_cbr_backups.py → hcloud CBR ListBackups --cli-region=<region>
      → Huawei Cloud CBR OpenAPI (regional endpoint) → parsed JSON → table / --json / --names-only

(hcloud binary missing) → fallback: huaweicloudsdkcbr v1 CbrClient.list_backups
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListBackups` (GET). A
  write-intent guard scans the user arguments and validates the operation name;
  mutating intents (create / delete / restore / copy / import / replicate /
  update / migrate / associate / bind ...) are rejected with an explicit message
  before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  KooCLI binary is absent, the script falls back to the official
  `huaweicloudsdkcbr` v1 SDK (`list_backups`). Credentials are always read by
  the CLI profile / SDK environment — never handled by the script.
- **Full-field table output** — the default table renders the union of all
  fields returned by ListBackups, with the owning resource (name / id / type),
  `vault_id`, `created_at` and `expired_at` surfaced explicitly.
- **Native + client-side filtering** — CBR `ListBackups` accepts `name`, `status`,
  `resource_id`, `resource_name`, `resource_type`, `vault_id`, `image_type`,
  `limit` / `offset` and more; the script passes them through and re-filters the
  rendered rows locally so the output always honours the requested filters.
- **Offline-testable** — every code path (paging, filtering, error
  classification, guard, SDK fallback) is covered by unit tests that mock the
  hcloud subprocess.

> **Scope:** this skill lists **backups**. It does not list backup vaults
> (`ListVaults`), does not report vault quota/usage, and does not run any
> restore/copy/delete operation — those require a separate skill/Issue.

Out of scope: every mutating CBR action (create / delete / restore / copy /
import / replicate / update vault / bind policy). Those require a dedicated
write-capable skill and explicit user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdkcbr` to enable the
   SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band (`hcloud
   configure` in your terminal, or credential environment variables). Never paste
   AK/SK into chat; the script never reads, echoes, or stores secrets itself —
   authentication is delegated entirely to the hcloud profile / SDK environment.
3. **IAM permission** — read-only permission for listing backups
   (`cbr:backup:list`); least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess / re).
5. **Outbound HTTPS** access to `cbr.<region>.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`); every CBR call is
   region-scoped.
2. **Confirm hcloud readiness** (optional, read-only): the credential profile is
   configured (see [references/cli-installation-guide.md](references/cli-installation-guide.md)).
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — table for humans, `--json` for downstream tooling,
   `--names-only` for a compact inventory.
5. **Handle the empty / error cases** per the Error Handling table below.

## Core Commands

```bash
# Full-field table (default)
python3 scripts/list_cbr_backups.py --region cn-north-4

# Raw JSON of every returned field
python3 scripts/list_cbr_backups.py --json

# Compact backup name + ID inventory
python3 scripts/list_cbr_backups.py --names-only

# Filter by name / status (server-side + client-side)
python3 scripts/list_cbr_backups.py --name backup-prod
python3 scripts/list_cbr_backups.py --status available

# Filter by owning resource / vault
python3 scripts/list_cbr_backups.py --resource_type OS::Nova::Server --names-only
python3 scripts/list_cbr_backups.py --resource_name ecs-prod
python3 scripts/list_cbr_backups.py --vault_id 8a9b0c1d-2e3f-4a5b-6c7d-8e9f0a1b2c3d --json

# Combine filters + custom page size
python3 scripts/list_cbr_backups.py --region cn-south-1 --status available --names-only --page-size 100
```

Equivalent direct KooCLI call (the script wraps exactly this operation, with
paging) — illustrative, requires KooCLI installed:

```text
hcloud CBR ListBackups --cli-region=cn-north-4 --limit=1000 --offset=0
```

The filter flags above map to the real KooCLI parameters, which use the
underscore form (`--resource_id` / `--resource_name` / `--resource_type` /
`--vault_id` / `--image_type`); the script emits exactly those when it builds
the command.

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--json` | No | Output the raw backup array as JSON | — |
| `--names-only` | No | Output a compact name + ID inventory | — |
| `--name` | No | Filter by backup name (server-side + client-side substring) | `backup-prod` |
| `--status` | No | Filter by status (exact, e.g. `available` / `error`) | `available` |
| `--resource-id` / `--resource_id` | No | Filter by owning resource ID (exact) | `res-1111` |
| `--resource-name` / `--resource_name` | No | Filter by owning resource name (substring) | `ecs-prod` |
| `--resource-type` / `--resource_type` | No | Filter by resource type (exact) | `OS::Nova::Server` |
| `--vault-id` / `--vault_id` | No | Filter by vault ID (exact) | `8a9b0c1d-2e3f-4a5b-6c7d-8e9f0a1b2c3d` |
| `--image-type` / `--image_type` | No | Filter by backup type (exact, e.g. `backup`) | `backup` |
| `--page-size` | No | Page size for ListBackups (default 1000) | `100` |
| `--operation` | No | hcloud CBR operation name; only `ListBackups` is allowed | `ListBackups` |

Output-mode precedence: `--names-only` → `--json` → table (default).

## Write-Intent Guard

- The script scans flag names plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `restore`, `copy`, `import`,
  `replicate`, `migrate`, `associate`, `bind`, `remove`, and CBR operation names
  such as `CreateBackup`, `DeleteBackup`, `RestoreBackup`, `CopyBackup`).
- The values of the read-only filter flags (`--name`, `--status`,
  `--resource_id`, `--resource_name`, `--resource_type`, `--vault_id`,
  `--image_type`, `--region`, `--page-size`, `--limit`, `--offset`) are **not**
  scanned: they are query data and may legitimately contain write-looking words
  (e.g. a backup named `delete-me`). The read-only operation `ListBackups`
  itself is never blocked (bare `backup` is not a keyword).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed. The guard
  runs on the raw argv *before* argparse, so a mutating flag such as
  `--delete-backup` is reported as a guard violation rather than an
  "unrecognized argument" error.
- Only `hcloud CBR ListBackups --cli-region=<region>` (GET) — or the SDK `list_backups` call in the
  fallback path — is ever constructed by `build_command()`; there is no code
  path that can issue a mutating CBR API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `CBR`.
- **Operation name** — PascalCase: `ListBackups`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete CBR call).
- **Simple parameter** — `--key=value`, e.g. `--limit=1000`, `--offset=20`.
- **REST path (official SDK `_http_info`)** — `GET /v3/{project_id}/backups`
  (`huaweicloudsdkcbr` v1 `_list_backups_http_info`); project_id is resolved by
  KooCLI from the credential profile.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty backup list | Exit 0, prints `当前区域（<x>）无 CBR 备份` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问 CBR，请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkcore huaweicloudsdkcbr` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud CBR ListBackups --cli-region=<region> --help` |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| `error` / `creating` backups | Reported with their state, not treated as failure |
| `--name` / `--resource_name` filter | Server-side parameter + client-side case-insensitive substring |
| `--status` / `--resource_id` / `--resource_type` / `--vault_id` / `--image_type` filter | Server-side parameter + client-side case-insensitive exact match |
| Large backup count | Automatic `offset` paging (`count` aware, full-page fallback, max 100 pages) |
| Extra response fields | Table columns are built from the union of returned fields — new fields appear automatically |
| Field missing on a backup | Rendered as `-` in the table |
| Nested / datetime fields | Normalized (ISO strings) before rendering |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkcbr` list_backups, same output modes |
| User asks to create/delete/restore/copy a backup | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / restore / copy /
import / replicate / update / migrate / associate / operation whitelist /
`ListBackups` not blocked / filter values not blocked / `--offset` not blocked),
command construction (limit + offset + native filters, no write flags), JSON
extraction (plain / wrapped / list / invalid), backup extraction (`backups` /
`backup_list` / bare list), failure classification (missing AK/SK, 403, generic,
`[USE_ERROR]` with rc=0), count-aware paging, SDK fallback (success and
unavailable, request construction, `BackupResp` attribute remapping),
client-side filtering (name / status / resource_id / resource_name /
resource_type / vault_id), rendering (table with the preferred columns / names /
summary lines / fallbacks), and all `main()` output modes including empty,
filter, and error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |