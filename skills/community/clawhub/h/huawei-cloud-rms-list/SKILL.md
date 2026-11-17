---
name: huawei-cloud-rms-list
description: |
  1. Query the Huawei Cloud RMS unified resource inventory of a tenant through
     KooCLI (`hcloud RMS ListAllResources --cli-region=<region>`; official
     read-only GET /v1/resource-manager/domains/{domain_id}/all-resources), with
     an automatic fallback to the huaweicloudsdkrms v1 SDK when KooCLI is
     absent.
  2. Four read-only views: account-wide resource list (default, ListAllResources),
     provider+type-scoped resource list (ListResources), the RMS provider /
     resource-type catalog (ListProviders) and the RMS region catalog
     (ListRegions).
  3. Four output modes: aligned full-field table (default), `--json`, `--markdown`
     (GitHub-flavored table) and `--csv`; `--output` writes a file via a temp
     file + atomic rename.
  4. Filters: `--provider` / `--type` / `--region-id` / `--ep-id` / `--id` /
     `--name` / `--tags` / `--domain-id` (all real RMS query parameters) plus
     automatic `marker` paging (and `offset` paging for ListProviders).
  5. Explicit error hints for empty inventories, 403 / missing
     `rms:resources:list` permission (RMS.00010006), missing AK/SK credentials,
     a missing KooCLI backend, and bad export paths.
  6. Built-in write-intent guard: any mutating intent (create / delete / update /
     enable / disable / run-query ...) or any operation outside the four
     read-only ones is rejected before execution — this skill is strictly
     read-only.
  7. Triggers include: "RMS 资源清单", "查询资源管理服务资源", "统一资源视图",
     "rms list resources", "list all resources", "资源清单导出", "资源盘点",
     "RMS resources list", "华为云资源清单".
tags: [huawei-cloud, rms, resource-inventory, readonly, koo-cli]
---

# Huawei Cloud RMS Resource Inventory

## Overview

Query the Huawei Cloud RMS (Resource Management Service) unified resource view of
a tenant through KooCLI `hcloud RMS ListAllResources --cli-region=<region>`
(official read-only GET `/v1/resource-manager/domains/{domain_id}/all-resources`,
verified in the `huaweicloudsdkrms` v1 client `_list_all_resources_http_info`
metadata). The skill is aimed at account-wide resource inventory / 资源盘点, asset
archival, compliance pre-checks, and as a pre-query step for other skills that
need a `resource_id`.

Architecture:

```text
agent → python3 scripts/list_rms_resources.py → skill-quality-cli ─▶ hcloud RMS <Operation> --cli-region=<region> [filters] [--marker]
      → Huawei Cloud RMS OpenAPI (resource-manager) → parsed JSON → table / json / markdown / csv

(hcloud binary missing) → fallback: huaweicloudsdkrms v1 RmsClient (ListAllResources / ListResources / ListProviders / ListRegions)
(missing SDK)           → run scripts/ensure_env.py  (auto pip install)
```

Key properties:

- **Read-only by design** — the only operations ever constructed are
  `ListAllResources`, `ListResources`, `ListProviders` and `ListRegions` (all
  GET). A write-intent guard scans the user arguments and validates the
  operation name; mutating intents (create / delete / update / enable / disable /
  run-query ...) are rejected with an explicit message before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path (wrapped
  with `skill-quality-cli` for telemetry); when the hcloud binary is absent, the
  script falls back to the official `huaweicloudsdkrms` v1 SDK. Credentials are
  always read by the CLI profile / SDK environment — never handled by the
  script.
- **Paging-aware** — resource views follow `page_info.next_marker` until the
  last page; ListProviders advances `offset` until `total_count` is reached.
- **Offline-testable** — the guard, command construction, paging, error
  classification (including the `RMS.00010006` permission envelope returned on
  stdout with rc=0), SDK fallback, renderers and atomic export are covered by
  offline unit tests that mock the hcloud subprocess.

> **Dependency**: Quality telemetry is collected automatically via skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

> **Capability boundary:** this skill **lists/queries** the RMS resource
> inventory and the provider/region catalogs only. It does not create, delete or
> modify resources, does not manage RMS config aggregators / trackers / policy
> assignments, and never writes anything back to the cloud. Those require a
> separate skill and explicit user confirmation (确认).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — the primary execution path; see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   When absent, the SDK fallback is used.
2. **Python 3.8+** with the Huawei Cloud SDK — run
   `python3 scripts/ensure_env.py` to install `huaweicloudsdkcore` and
   `huaweicloudsdkrms` automatically. Rendering itself needs only the standard
   library.
3. **Credentials configured out-of-band** — the CLI reads the active hcloud
   profile; the SDK fallback reads AK/SK from the whitelisted environment
   variables (`HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`, `HUAWEI_ACCESS_KEY` /
   `HUAWEI_SECRET_KEY`, `HW_*`, ...). Never paste AK/SK into chat; the script
   never reads, echoes or stores secrets itself.
4. **IAM permission** — read-only `rms:resources:list` (plus `rms::listTags` /
   `rms::listResourcesByTag` when listing tag-based views); least-privilege policy
   in [references/iam-policies.md](references/iam-policies.md).
5. **Region** — `cn-north-4` by default (the RMS SDK catalog advertises the
   global endpoint `https://rms.myhuaweicloud.com`).
6. **Outbound HTTPS** access to the RMS OpenAPI endpoint.
- **skill-quality-cli** — ensured by bash scripts/ensure_cli.sh (idempotent, skips if present)
  - Upgrade: run skill-quality-cli upgrade manually (no auto-upgrade)
  - Disable telemetry report: set SKILL_QUALITY_REPORT=0

## Workflow

1. **(Optional) prepare the environment** — `python3 scripts/ensure_env.py`
   installs any missing SDK dependency.
2. **Choose the view** — default account-wide inventory (ListAllResources);
   `--list-providers` / `--list-regions` for the catalogs; `--provider P --type T`
   for a provider+type-scoped list (ListResources).
3. **Pick filters** — `--region-id`, `--ep-id`, `--id`, `--name`, `--tags`,
   `--domain-id` (real server-side RMS query parameters).
4. **Run the script** with the desired `--format` and `--output`.
5. **Read the result** — the table prints to stdout; file formats print the
   written path. An empty result is reported explicitly and still writes a valid
   header-only file.
6. **Handle the empty / error cases** per the Error Handling table below.

## Core Commands

> **⚠️ Mandatory quality wrapping: `scripts/list_rms_resources.py` builds every `hcloud` CLI call as `skill-quality-cli run --skill-name huawei-cloud-rms-list -- hcloud ...` (enforced in code, not left to the agent). If `skill-quality-cli` is unavailable (run `bash scripts/ensure_cli.sh`) or `SKILL_QUALITY_REPORT=0`, the CLI path degrades to bare `hcloud` (no telemetry) — the read-only semantics and the CLI→SDK fallback are unchanged. When the `hcloud` binary itself is not resolvable, the wrapping is skipped and the bare command runs, so the missing binary surfaces as `FileNotFoundError` → `ConfigError` and the SDK fallback still triggers.**

```bash
# Default: account-wide RMS resource inventory (ListAllResources) as a table
python3 scripts/list_rms_resources.py --region cn-north-4

# Export the inventory to a JSON / Markdown / CSV file
python3 scripts/list_rms_resources.py --format json --output /tmp/rms_resources.json
python3 scripts/list_rms_resources.py --format markdown --summary --output /tmp/rms_resources.md
python3 scripts/list_rms_resources.py --format csv --output /tmp/rms_resources.csv

# Filter by region, resource type, enterprise project, name or tags
python3 scripts/list_rms_resources.py --region-id cn-north-4 --type ecs.cloudservers
python3 scripts/list_rms_resources.py --ep-id 0 --name web-01
python3 scripts/list_rms_resources.py --tags env=prod --tags owner=ops

# Provider+type-scoped resource list (ListResources)
python3 scripts/list_rms_resources.py --provider ecs --type cloudservers

# RMS provider / resource-type catalog and region catalog
python3 scripts/list_rms_resources.py --list-providers --format table
python3 scripts/list_rms_resources.py --list-regions --format json

# Read-only credential readiness check (also wrapped)
skill-quality-cli run --skill-name huawei-cloud-rms-list -- hcloud configure list
```

Equivalent direct KooCLI commands (the script wraps exactly these calls, with
automatic paging):

```bash
hcloud RMS ListAllResources --cli-region=cn-north-4 --limit=100
hcloud RMS ListResources --cli-region=cn-north-4 --provider=ecs --type=cloudservers --limit=100
hcloud RMS ListProviders --cli-region=cn-north-4 --limit=100 --offset=1
hcloud RMS ListRegions --cli-region=cn-north-4
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--format` / `-f` | No | Output mode: `table` (default) / `json` / `markdown`(`md`) / `csv` | `--format json` |
| `--output` / `-o` | No | Export file path (json/markdown/csv; default `rms_<view>_<region>_<timestamp>.<ext>`) | `/tmp/rms.json` |
| `--summary` | No | Append a summary line to the Markdown report | `--summary` |
| `--domain-id` | No | Account domain id (RMS required path parameter; resolved by KooCLI/SDK when omitted) | `01a0...996d6` |
| `--list-providers` | No | List the RMS provider / resource-type catalog (ListProviders) | — |
| `--list-regions` | No | List the RMS region catalog (ListRegions) | — |
| `--provider` | No | Cloud service name; with `--type` selects ListResources | `ecs` |
| `--type` | No | Resource type; in full mode it is `provider.type` | `ecs.cloudservers` |
| `--region-id` | No | Filter by region ID — real server-side query parameter | `cn-north-4` |
| `--ep-id` | No | Filter by enterprise project ID — real server-side query parameter | `0` |
| `--id` | No | Filter by resource ID — real ListAllResources query parameter | `r-0001` |
| `--name` | No | Filter by resource name — real ListAllResources query parameter | `web-01` |
| `--tags` | No | Filter by tag(s), repeatable — real ListAllResources query parameter | `env=prod` |
| `--limit` | No | Page size (default 100; pages are fetched automatically) | `200` |
| `--offset` | No | Paging offset (ListProviders; default 1, min 1) | `1` |
| `--track` | No | Whether resources are collected by default (ListProviders) | `Tracked` |
| `--max-pages` | No | Maximum auto-pages (default 100, prevents infinite loops) | `50` |

Output-mode precedence: `--format` selects the mode; `--output` only matters for
the file formats (`json` / `markdown` / `csv`); `table` writes to stdout. The
local `--output` path value (e.g. a file literally named
`rms-delete-report.json`) and the filter values are excluded from the
write-intent guard because they are not RMS operations.

## Write-Intent Guard

- The script scans all user arguments (except the values of the read-only filter
  flags and of the local-output/format flags) plus the operation name for
  mutating vocabulary (`create`, `delete`, `update`, `modify`, `enable`,
  `disable`, `run-query`, and RMS operation names such as
  `CreateConfigurationAggregator`, `DeletePolicyAssignment`,
  `UpdateTrackerConfig`).
- Any hit raises `GuardError`, prints
  `[错误] 检测到写操作意图 ... 已被守卫拦截`, and exits with code 1 **before** a
  single hcloud command is executed.
- Only `ListAllResources` / `ListResources` / `ListProviders` / `ListRegions`
  (all GET) are ever constructed by `build_command()`; there is no code path
  that can issue a mutating RMS API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `RMS`.
- **Operation name** — PascalCase API operation: `ListAllResources`,
  `ListResources`, `ListProviders`, `ListRegions`.
- **Region parameter** — always pass `--cli-region=<region>`, e.g.
  `--cli-region=cn-north-4`.
- **Simple parameters** — `--key=value`, e.g. `--limit=100`, `--marker=<token>`,
  `--region_id=cn-north-4`, `--type=ecs.cloudservers`, `--provider=ecs`.
  All filters are real server-side parameters (verified against the
  `huaweicloudsdkrms` v1 request models and `hcloud RMS <Operation> --help`).
- **Indexed parameter** — `--tags.N=value`, e.g. `--tags.1=env=prod`.
- **Paging** — resources use `--limit` + `--marker` (`page_info.next_marker`);
  ListProviders uses `--limit` + `--offset` (`total_count`).
- **REST paths (official SDK `_http_info`)** —
  `GET /v1/resource-manager/domains/{domain_id}/all-resources` (ListAllResources),
  `GET /v1/resource-manager/domains/{domain_id}/provider/{provider}/type/{type}/resources` (ListResources),
  `GET /v1/resource-manager/domains/{domain_id}/providers` (ListProviders),
  `GET /v1/resource-manager/domains/{domain_id}/regions` (ListRegions).

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty inventory | Exit 0, prints `当前区域（<x>）无 <operation> 结果` (+ active filters); a header-only export file is still written |
| 403 / missing `rms:resources:list` (`RMS.00010006`) | Exit 1, `无权限访问资源管理服务（RMS），请检查 IAM 权限` hint; the envelope is detected even on stdout with rc=0 |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| hcloud not installed | Falls back to the SDK; if the SDK is unavailable too, exit 1 with a clear hint |
| Bad `--output` path (permission / bad dir) | Exit 1, `导出文件写出失败` hint; no partial file is left |
| `--provider` without `--type` | Exit 1, explicit hint that ListResources needs both |
| KooCLI usage error (`[USE_ERROR] ...`, even with rc=0) | Exit 1, explicit hcloud 参数错误 hint pointing to `hcloud RMS <Operation> --help` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, export, or API
error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Region has no resources | Friendly message + a header-only export file, exit 0 |
| `--provider` / `--type` / `--region-id` / `--tags` filters | Forwarded as real server-side query parameters |
| Large resource count | Automatic `marker` paging (`page_info.next_marker` aware, max 100 pages) |
| Extra response fields | Table/CSV columns are built from the union of returned fields |
| Field missing on a record | Rendered as `-` |
| Nested `tags` / `resource_types` | Flattened into `k=v,...` / `name,...` strings |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkrms`, same output modes |
| `--output` points to a non-existing directory | Directory is created automatically |
| `--output` path contains a guard keyword | Path value is excluded from the guard (local path ≠ RMS operation) |
| Provider/region catalog returned | Rendered with `provider` / `region_id` columns and `display_name` |
| User asks to create/delete an RMS resource or aggregator | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation (确认) is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network),
run from the skill directory:

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / update / enable /
normalized variants / operation whitelist / value-flag exclusion / following-flag
still scanned), operation resolution, command construction (filters, domain id,
language, provider scope), JSON extraction and error-envelope classification
(including the `RMS.00010006` permission envelope on stdout with rc=0), marker
paging, provider offset paging, SDK fallback (missing hcloud / missing env
credentials), rendering (table / Markdown / CSV / JSON) and atomic export.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI + SDK installation, credential configuration and skill-quality-cli |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
