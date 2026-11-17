---
name: huawei-cloud-cbr-vault-list
description: |
  1. List Huawei Cloud CBR (Cloud Backup and Recovery) backup vaults in a tenant
     region through KooCLI (`hcloud CBR ListVault --cli-region=<region>` — read-only), with an
     automatic fallback to the official huaweicloudsdkcbr v1 SDK
     (CbrClient.list_vault) when hcloud is not installed.
  2. Output modes: full-field aligned table (default, every returned field with
     名称/ID/状态/容量/计费模式 surfaced explicitly), --json (raw response array)
     and --names-only (compact vault name + ID inventory).
  3. Supports --region (default cn-north-4), --page-size with automatic
     limit/offset paging, and the native ListVault filters --name / --status /
     --object-type / --protect-type / --enterprise-project-id / --vault-id
     (with a client-side re-filter for the rendered rows).
  4. Explicit error hints for empty vault lists (「当前区域无 CBR 存储库」),
     403 / insufficient IAM permission (「无权限访问 CBR，请检查 IAM 权限」),
     missing or invalid AK/SK credentials, hcloud not installed, and KooCLI
     usage errors.
  5. Built-in write-intent guard: any mutating intent (create / delete / update
     / restore / copy / migrate / bind / associate / ...) or any operation other
     than the read-only ListVault is rejected before execution — this skill is
     strictly read-only.
  6. Triggers include: "list CBR vaults", "CBR vault list", "CBR 存储库列表",
     "查询CBR存储库", "查询备份存储库", "备份存储库列表", "云备份存储库",
     "存储库盘点", "备份容量盘点", "计费模式核对", "CBR inventory", "list vaults",
     "华为云CBR存储库", "华为云CBR列表".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, filters,
     paging, error scenarios, SDK fallback and the write-intent guard.
tags: [huawei-cloud, cbr, storage, readonly, koo-cli]
---

# Huawei Cloud CBR Backup Vault List

## Overview

Query the CBR (Cloud Backup and Recovery) backup vault list of a tenant region
through KooCLI `hcloud CBR ListVault --cli-region=<region>` (read-only), with a
fallback to the official `huaweicloudsdkcbr` v1 SDK (`CbrClient.list_vault`,
GET `/v3/{project_id}/vaults`). The skill is aimed at vault inventory, daily
operations patrol, capacity accounting and charging-mode verification.

Architecture:

```text
agent → python3 scripts/list_cbr_vaults.py → hcloud CBR ListVault --cli-region=<region>
      → Huawei Cloud CBR OpenAPI (regional endpoint) → parsed JSON → table / --json / --names-only

(hcloud binary missing) → fallback: huaweicloudsdkcbr v1 CbrClient.list_vault
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListVault` (GET). A
  write-intent guard scans the user arguments and validates the operation name;
  mutating intents (create / delete / update / restore / copy / migrate / bind /
  associate ...) are rejected with an explicit message before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  KooCLI binary is absent, the script falls back to the official
  `huaweicloudsdkcbr` v1 SDK (`list_vault`). Credentials are always read by the
  CLI profile / SDK environment — never handled by the script.
- **Full-field table output** — the default table renders the union of all
  fields returned by ListVault. The vault capacity, status, object type,
  protection type and charging mode nested under the response's `billing`
  object are flattened to first-class columns, so 名称 / ID / 状态 / 容量 /
  计费模式 are always directly readable.
- **Native + client-side filtering** — CBR `ListVault` accepts `name`, `status`,
  `object_type`, `protect_type`, `enterprise_project_id`, `id` (vault IDs),
  `cloud_type`, `policy_id`, `resource_ids`, `availability_zone` and
  `limit` / `offset`; the script passes the supported filters through and
  re-filters the rendered rows locally so the output always honours the
  requested filters.
- **Offline-testable** — every code path (paging, filtering, error
  classification, guard, SDK fallback) is covered by unit tests that mock the
  hcloud subprocess.

> **Scope:** this skill lists **backup vaults** only. It does not list
> individual backups, does not report vault quota/usage summaries, and does not
> run any create/delete/update/migrate/restore/copy operation — those require a
> separate skill/Issue.

Out of scope: every mutating CBR action (create / delete / update vault, bind
policy, migrate, restore / copy backup). Those require a dedicated write-capable
skill and explicit user confirmation.

**Dependency**: Quality telemetry is collected automatically via skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdkcbr` to enable the
   SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band (`hcloud
   configure` in your terminal, or credential environment variables). Never paste
   AK/SK into chat; the script never reads, echoes, or stores secrets itself —
   authentication is delegated entirely to the hcloud profile / SDK environment.
3. **IAM permission** — read-only permission for listing vaults
   (`cbr:vaults:list`, verified via `IAM GetAuthorizationSchemaV5`); least-privilege
   policy in [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess / re).
5. **Outbound HTTPS** access to `cbr.<region>.myhuaweicloud.com`.
- **skill-quality-cli** — ensured by bash scripts/ensure_cli.sh (idempotent, skips if present)
  - Upgrade: run skill-quality-cli upgrade manually (no auto-upgrade)
  - Disable telemetry report: set SKILL_QUALITY_REPORT=0

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

> **⚠️ Mandatory: every hcloud command in this skill MUST be wrapped with skill-quality-cli run --skill-name huawei-cloud-cbr-vault-list -- ** — bare hcloud calls are strictly forbidden.**

```bash
# Full-field table (default)
python3 scripts/list_cbr_vaults.py --region cn-north-4

# Raw JSON array of every returned vault
python3 scripts/list_cbr_vaults.py --json

# Compact vault name + ID inventory
python3 scripts/list_cbr_vaults.py --names-only

# Filter by name / status (server-side + client-side)
python3 scripts/list_cbr_vaults.py --name vault-prod
python3 scripts/list_cbr_vaults.py --status available

# Filter by object type / protection type
python3 scripts/list_cbr_vaults.py --object-type server --names-only
python3 scripts/list_cbr_vaults.py --protect-type backup --names-only

# Filter by enterprise project / vault ID
python3 scripts/list_cbr_vaults.py --enterprise-project-id 0 --json
python3 scripts/list_cbr_vaults.py --vault-id 8a9b0c1d-2e3f-4a5b-6c7d-8e9f0a1b2c3d

# Combine filters + custom page size
python3 scripts/list_cbr_vaults.py --region cn-south-1 --status available --names-only --page-size 50
```

Equivalent direct KooCLI call (the script wraps exactly this operation, with
paging) — illustrative, requires KooCLI installed:

```bash
skill-quality-cli run --skill-name huawei-cloud-cbr-vault-list -- hcloud CBR ListVault --cli-region=cn-north-4 --limit=100 --offset=0
skill-quality-cli run --skill-name huawei-cloud-cbr-vault-list -- hcloud CBR ListVault --cli-region=cn-north-4 --status=available --limit=100 --offset=0
```

The filter flags above map to the real KooCLI parameters, which use the
underscore form (`--object_type` / `--protect_type` /
`--enterprise_project_id`); the script emits exactly those when it builds the
command. The vault ID filter is emitted as the operation's array parameter
`--id.1=<vault_id>` (ListVault has `id.[N]`, there is no `--vault_id`).

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--json` | No | Output the raw vault array as JSON | — |
| `--names-only` | No | Output a compact name + ID inventory | — |
| `--name` | No | Filter by vault name (server-side + client-side substring) | `vault-prod` |
| `--status` | No | Filter by vault status (exact, e.g. `available`) | `available` |
| `--object-type` / `--object_type` | No | Filter by object type (exact: `server` / `disk` / `turbo` / `workspace` / `vmware` / `rds` / `file`) | `server` |
| `--protect-type` / `--protect_type` | No | Filter by protection type (exact: `backup` / `replication`) | `backup` |
| `--enterprise-project-id` / `--enterprise_project_id` | No | Filter by enterprise project ID (or `all_granted_eps`) | `0` |
| `--vault-id` / `--vault_id` | No | Filter by vault ID (exact; emitted as `--id.1=<value>`) | `8a9b0c1d-2e3f-4a5b-6c7d-8e9f0a1b2c3d` |
| `--page-size` / `--page_size` | No | Page size for ListVault (default 100) | `50` |
| `--operation` | No | hcloud CBR operation name; only `ListVault` is allowed | `ListVault` |

Output-mode precedence: `--names-only` → `--json` → table (default).

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `CBR`.
- **Operation name** — PascalCase: `ListVault` (singular; `ListVaults` is **not**
  a supported KooCLI operation and returns `[USE_ERROR]`).
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete CBR call).
- **Simple parameter** — `--key=value`, e.g. `--limit=100`, `--offset=20`.
- **Array parameter** — `--key.N=value`, e.g. `--id.1=<vault_id>`.
- **REST path (official SDK `_http_info`)** — `GET /v3/{project_id}/vaults`
  (`huaweicloudsdkcbr` v1 `_list_vault_http_info`); project_id is resolved by
  KooCLI from the credential profile.

## Write-Intent Guard

- The script scans flag names plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `modify`, `restore`, `copy`,
  `import`, `replicate`, `migrate`, `associate`, `bind`, `remove`, `add`, and CBR
  operation names such as `CreateVault`, `DeleteVault`, `UpdateVault`,
  `AddVaultResource`, `AssociateVaultPolicy`, `ChangeVaultChargeMode`).
- The values of the read-only filter flags (`--name`, `--status`,
  `--object_type`, `--protect_type`, `--enterprise_project_id`, `--vault_id`,
  `--region`, `--page-size`, `--limit`, `--offset`) are **not** scanned: they are
  query data and may legitimately contain write-looking words (e.g. a vault
  named `delete-me`). The read-only operation `ListVault` itself is never
  blocked (bare `vault` is not a keyword).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed. The guard
  runs on the raw argv *before* argparse, so a mutating flag such as
  `--delete-vault` is reported as a guard violation rather than an
  "unrecognized argument" error.
- Only `hcloud CBR ListVault --cli-region=<region>` (GET) — or the SDK
  `list_vault` call in the fallback path — is ever constructed by
  `build_command()`; there is no code path that can issue a mutating CBR API
  call. Any write request is out of scope and requires explicit user
  confirmation in a dedicated write-capable skill.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty vault list | Exit 0, prints `当前区域（<x>）无 CBR 存储库` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问 CBR，请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkcore huaweicloudsdkcbr` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| API error JSON with exit code 0 (`error_code` / `error_msg`) | Exit 1, classified as 403 / auth / generic API error |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud CBR ListVault --cli-region=<region> --help` |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| `error` / `locked` vaults | Reported with their state, not treated as failure |
| Capacity / status / charging mode | Nested under `billing` in the raw response; flattened for the table and honoured by filters |
| `--name` filter | Server-side parameter + client-side case-insensitive substring |
| `--status` / `--object_type` / `--protect_type` / `--enterprise_project_id` / `--vault_id` filter | Server-side parameter + client-side case-insensitive exact match |
| Large vault count | Automatic `offset` paging (`count` aware, full-page fallback, duplicate-ID guard, max 100 pages) |
| Extra response fields | Table columns are built from the union of returned fields — new fields appear automatically |
| Field missing on a vault | Rendered as `-` in the table |
| Nested / datetime fields | Normalized (JSON-encoded or ISO strings) before rendering |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkcbr` list_vault, same output modes |
| User asks to create/delete/update/migrate a vault | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / update / restore /
copy / import / replicate / migrate / associate / operation whitelist /
`ListVault` not blocked / filter values not blocked / `--offset` not blocked),
command construction (limit + offset + native filters, `--id.1` vault ID form,
no write flags), JSON extraction (plain / wrapped / list / invalid), vault
extraction (`vaults` / `vault_list` / bare list), failure classification
(missing AK/SK, 403, generic, `[USE_ERROR]` with rc=0, API error payload),
count-aware paging with duplicate-ID guard, SDK fallback (success and
unavailable, request construction, `Vault` attribute remapping with `billing`),
client-side filtering (name / status / object_type / protect_type /
enterprise_project_id / vault_id), rendering (table with the preferred columns /
names / summary lines / fallbacks), and all `main()` output modes including
empty, filter, and error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |