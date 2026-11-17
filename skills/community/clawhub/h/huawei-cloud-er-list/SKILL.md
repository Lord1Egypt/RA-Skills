---
name: huawei-cloud-er-list
description: |
  1. Read-only inventory of Huawei Cloud Enterprise Router (ER) resources
     through KooCLI: enterprise routers (hcloud ER ListEnterpriseRouters —
     GET /v3/{project_id}/enterprise-router/instances), VPC attachments
     (hcloud ER ListVpcAttachments — GET
     /v3/{project_id}/enterprise-router/{er_id}/vpc-attachments), route tables
     (hcloud ER ListRouteTables — GET
     /v3/{project_id}/enterprise-router/{er_id}/route-tables) and single-ER
     detail (hcloud ER ShowEnterpriseRouter — GET
     /v3/{project_id}/enterprise-router/instances/{er_id}), with an automatic
     fallback to the official huaweicloudsdker v3 SDK when hcloud is missing.
  2. `--resource {er,attachment,route-table,detail}` selects the view
     (default `er`); attachment / route-table / detail require `--er-id`.
  3. Output modes: compact list (default), fixed-column table (`--table`:
     ER 8 columns / VPC attachment 6 columns / route table 6 columns) and
     `--json` (raw response fields).
  4. Non-`available` enterprise routers / attachments are rendered in a
     separate, explicitly flagged `[!]` / `[异常]` section instead of being
     mixed with healthy resources.
  5. Filters: local `--name` (exact) and `--fuzzy` (case-insensitive), plus
     server-side `--er-id` / `--state` / `--owned-by-self` /
     `--enterprise-project-id` / `--vpc-id` / `--sort-key` / `--sort-dir`;
     region defaults to `cn-north-4`; `--page-size`/`--limit` is 1–2000 with
     automatic `page_info.next_marker` paging.
  6. Built-in write-intent guard: Create / Delete / Update / Associate /
     Disassociate / Enable / Disable / Accept / Reject and any non-whitelisted
     operation are rejected before execution (exit 1) — this skill is strictly
     read-only.
  7. Explicit hints for empty lists, 403 / insufficient IAM permission, missing
     or invalid AK/SK, missing project_id on the SDK fallback, invalid `--er-id`
     (not found), network failures and hcloud not installed.
  8. Triggers include: "list enterprise routers", "er list", "企业路由器列表",
     "查询企业路由器", "ER 实例列表", "VPC 连接列表", "ER VPC 连接", "ER 路由表",
     "企业路由器详情", "er inventory", "list vpc attachments", "list route tables",
     "华为云 ER", "企业路由器下钻".
  9. Offline unit tests (mocked hcloud subprocess + fake SDK) cover output
     modes, filters, paging, error scenarios, SDK fallback, abnormal-state
     separation and the write-intent guard.
tags: [huawei-cloud, er, network, readonly, koo-cli]
---

# Huawei Cloud Enterprise Router (ER) List

## Overview

Query Huawei Cloud Enterprise Router (ER) resources of a tenant through four
read-only KooCLI operations:

- **Enterprise routers** — `hcloud ER ListEnterpriseRouters --cli-region=<region>`
  (official read-only `GET /v3/{project_id}/enterprise-router/instances`, verified
  in the `huaweicloudsdker` v3 client `resource_path` metadata).
- **VPC attachments** — `hcloud ER ListVpcAttachments --cli-region=<region> --er_id=<id>`
  (`GET /v3/{project_id}/enterprise-router/{er_id}/vpc-attachments`).
- **Route tables** — `hcloud ER ListRouteTables --cli-region=<region> --er_id=<id>`
  (`GET /v3/{project_id}/enterprise-router/{er_id}/route-tables`).
- **ER detail** — `hcloud ER ShowEnterpriseRouter --cli-region=<region> --er_id=<id>`
  (`GET /v3/{project_id}/enterprise-router/instances/{er_id}`).

The skill is aimed at ER inventory inspection, daily operations patrol, network
topology checks, and as a pre-query step for other skills that need an ER `id`,
its `state`, its VPC attachments or route tables.

Architecture:

```text
agent → python3 scripts/list_er.py --resource er|attachment|route-table|detail
      → hcloud ER ListEnterpriseRouters / ListVpcAttachments /
        ListRouteTables / ShowEnterpriseRouter --cli-region=<region>
      → Huawei Cloud ER OpenAPI (er.<region>.myhuaweicloud.com) → parsed JSON
      → compact list / --table / --json

(hcloud binary missing) → fallback: huaweicloudsdker v3 ErClient
      list_enterprise_routers / list_vpc_attachments /
      list_route_tables / show_enterprise_router
```

Key properties:

- **Read-only by design** — the only APIs ever invoked are the four GET
  operations above. A write-intent guard scans user arguments and validates the
  operation name per `--resource`; mutating intents are rejected with an
  explicit message before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  KooCLI binary is absent the script falls back to the official
  `huaweicloudsdker` v3 SDK. Credentials are always read by the CLI profile /
  SDK environment — never handled by the script.
- **Abnormal resources are separated** — non-`available` enterprise routers and
  VPC attachments are collected into a dedicated section, prefixed with `[!]`
  in table mode and `[异常]` in compact mode, so a failed / pending resource is
  never silently mixed with healthy rows.
- **Offline-testable** — every code path (paging, filters, error classification,
  SDK fallback, rendering, guard) is covered by unit tests that mock the hcloud
  subprocess and the SDK.

Out of scope: every mutating ER action (create / update / delete an ER, VPC
attachment, route table or static route; associate / disassociate a route table;
accept / reject an attachment; enable / disable a flow log or propagation; tag
changes). Those require a dedicated write-capable skill and explicit user
confirmation.

**Dependency**: Quality telemetry is collected automatically via skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdker` to enable the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band
   (run the KooCLI configure command in your terminal, or set credential
   environment variables).
   Never paste AK/SK into chat; the script never reads, echoes, or stores
   secrets itself — authentication is delegated entirely to the hcloud profile
   / SDK environment.
3. **project_id (SDK fallback only)** — the ER REST paths are
   `/v3/{project_id}/enterprise-router/...`; when falling back to the SDK,
   supply the project id via `--project-id` or the
   `HUAWEICLOUD_SDK_PROJECT_ID` / `HUAWEI_PROJECT_ID` environment variables.
   The KooCLI path resolves it from the profile automatically.
4. **IAM permission** — read-only `er:instances:list`, `er:instances:get`,
   `er:instances:listVpcAttachments` and `er:routeTables:list`; least-privilege
   policy in [references/iam-policies.md](references/iam-policies.md).
5. **Python 3.8+** (standard library only — argparse / json / subprocess).
6. **Outbound HTTPS** access to `er.cn-north-4.myhuaweicloud.com`.
- **skill-quality-cli** — ensured by bash scripts/ensure_cli.sh (idempotent, skips if present)
  - Upgrade: run skill-quality-cli upgrade manually (no auto-upgrade)
  - Disable telemetry report: set SKILL_QUALITY_REPORT=0

## Workflow

1. **Confirm the target region** (default `cn-north-4`).
2. **Confirm the resource type** — `--resource er` (default) / `attachment` /
   `route-table` / `detail`.
3. **For attachment / route-table / detail, confirm the ER id** (`--er-id`).
   Get it from the `--resource er` inventory when unknown.
4. **Run the list script** with the desired output mode and filters.
5. **Read the result** — compact list for humans, `--table` for fixed columns,
   `--json` for downstream tooling. Check the `[!]` / `[异常]` section first.
6. **Handle the empty / error cases** per the Edge Cases table below (the script
   prints an explicit hint for empty lists, 403, missing AK/SK, invalid
   `--er-id`, network failure and hcloud missing).

## Core Commands

> **⚠️ Mandatory: every hcloud command in this skill MUST be wrapped with `skill-quality-cli run --skill-name huawei-cloud-er-list -- ` — bare hcloud calls are strictly forbidden.**

```bash
# Enterprise router inventory (compact list, default)
python3 scripts/list_er.py --region cn-north-4

# Fixed 8-column table (名称 / ID / 状态 / ASN / 企业项目ID / 可用区 / 描述 / 创建时间)
python3 scripts/list_er.py --region cn-north-4 --table

# Raw JSON of every returned field
python3 scripts/list_er.py --region cn-north-4 --json

# Local name filters (exact / case-insensitive fuzzy)
python3 scripts/list_er.py --name er-demo-01
python3 scripts/list_er.py --fuzzy demo

# Server-side filters
python3 scripts/list_er.py --state failed
python3 scripts/list_er.py --er-id er-0001
python3 scripts/list_er.py --owned-by-self true --enterprise-project-id 0
python3 scripts/list_er.py --sort-key name --sort-dir asc --page-size 50

# Drill down: VPC attachments of one ER (6-column table)
python3 scripts/list_er.py --resource attachment --er-id er-0001 --table

# Drill down: route tables of one ER (6-column table)
python3 scripts/list_er.py --resource route-table --er-id er-0001 --table

# Drill down: single ER detail
python3 scripts/list_er.py --resource detail --er-id er-0001
python3 scripts/list_er.py --resource detail --er-id er-0001 --json

# Filter attachments by VPC id / state
python3 scripts/list_er.py --resource attachment --er-id er-0001 \
  --vpc-id vpc-0001 --state available
```

Equivalent direct KooCLI commands (the script wraps exactly these calls, with
marker paging):

```bash
skill-quality-cli run --skill-name huawei-cloud-er-list -- hcloud ER ListEnterpriseRouters --cli-region=cn-north-4 --limit=100
skill-quality-cli run --skill-name huawei-cloud-er-list -- hcloud ER ListVpcAttachments --cli-region=cn-north-4 --er_id=er-0001 --limit=100
skill-quality-cli run --skill-name huawei-cloud-er-list -- hcloud ER ListRouteTables --cli-region=cn-north-4 --er_id=er-0001 --limit=100
skill-quality-cli run --skill-name huawei-cloud-er-list -- hcloud ER ShowEnterpriseRouter --cli-region=cn-north-4 --er_id=er-0001

# Read-only credential readiness check (also wrapped)
skill-quality-cli run --skill-name huawei-cloud-er-list -- hcloud configure list
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--resource` | No | View: `er` (default) / `attachment` / `route-table` / `detail` | `attachment` |
| `--table` | No | Fixed-column table output | — |
| `--json` | No | Raw response array / detail object as JSON | — |
| `--name` | No | Exact name filter (local) | `er-demo-01` |
| `--fuzzy` | No | Case-insensitive substring name filter (local) | `demo` |
| `--er-id` | Conditional | ER ID; required for `attachment` / `route-table` / `detail`, and a server-side `id` filter for `er` | `er-0001` |
| `--state` | No | Server-side state filter (`available` / `pending` / `modifying` / `deleting` / `deleted` / `failed`, attachments also `pending_acceptance` / `rejected` / `initiating_request`) | `failed` |
| `--owned-by-self` | No | `true` = current tenant only; `false` = include shared resources (`er` only) | `true` |
| `--enterprise-project-id` | No | Enterprise project ID filter (`er` only; `0` = default project) | `0` |
| `--vpc-id` | No | VPC ID filter (`attachment` only) | `vpc-0001` |
| `--sort-key` | No | Sort field: `id` / `name` / `state` | `name` |
| `--sort-dir` | No | Sort direction: `asc` / `desc` | `asc` |
| `--default-association-table` | No | Only default association route tables (`route-table` only; `true` / `false`) | `true` |
| `--default-propagation-table` | No | Only default propagation route tables (`route-table` only; `true` / `false`) | `true` |
| `--page-size` / `--limit` | No | Page size (default 100, range 1–2000) | `50` |
| `--project-id` | No | Project ID (needed by the SDK fallback path) | `05f...` |
| `--operation` | No | hcloud ER operation name; defaults to the operation for `--resource`; only the four read-only operations are allowed | `ListVpcAttachments` |

Output-mode precedence: `--json` → `--table` → compact list (default).
`--name` / `--fuzzy` are applied locally after the API response is fetched;
all other filters are real server-side query parameters.

## Output Formats

| View | Compact (default) | `--table` columns |
| ---------- | ---------- | --------- |
| `er` | `名称 (ID) [状态] ASN=… 企业项目=…` | 名称 / ID / 状态 / ASN / 企业项目ID / 可用区 / 描述 / 创建时间 (**8**) |
| `attachment` | `名称 (ID) [状态] VPC=… 子网=…` | 名称 / ID / 状态 / VPC ID / 子网 ID / 创建时间 (**6**) |
| `route-table` | `名称 (ID) [状态] 默认关联=… 默认传播=…` | 名称 / ID / 状态 / 默认关联 / 默认传播 / 创建时间 (**6**) |
| `detail` | labelled key/value detail block | the ER 8-column table (single row) |

For `er` and `attachment`, records whose `state` is **not** `available` are
rendered in a second, clearly flagged section (`[!] … 单独列出，请重点关注` in
table mode; `[异常]`-prefixed lines in compact mode) instead of being mixed with
healthy resources. A missing field renders as `-`; list values are joined with
`,`.

## Write-Intent Guard

- The script scans the raw arguments plus the `--operation` value for mutating
  vocabulary: `create` / `delete` / `update` / `modify` / `associate` /
  `disassociate` / `bind` / `unbind` / `release` / `remove` / `destroy` /
  `change` / `restart` / `enable` / `disable`, and the specific ER operation
  names (`CreateEnterpriseRouter`, `DeleteEnterpriseRouter`,
  `UpdateEnterpriseRouter`, `CreateVpcAttachment`, `DeleteVpcAttachment`,
  `UpdateVpcAttachment`, `AssociateRouteTable`, `DisassociateRouteTable`,
  `AcceptAttachment`, `RejectAttachment`, `EnablePropagation`,
  `DisablePropagation`, `CreateFlowLog`, `DeleteFlowLog`, …).
- An allowed `--resource` value (`er` / `attachment` / `route-table` /
  `detail`) and the local `--name` / `--fuzzy` search values are excluded from
  the scan, so a legit read request is never blocked by a read-only noun.
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`,
  and exits with code 1 **before** a single hcloud command is executed.
- The operation whitelist is per resource: `er` → `ListEnterpriseRouters`,
  `attachment` → `ListVpcAttachments`, `route-table` → `ListRouteTables`,
  `detail` → `ShowEnterpriseRouter`; a mismatched `--operation` is rejected.
  There is no code path that can issue a mutating ER API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `ER`.
- **Operation name** — PascalCase: `ListEnterpriseRouters`,
  `ListVpcAttachments`, `ListRouteTables`, `ShowEnterpriseRouter`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete ER call).
- **Path parameter** — `--er_id=<id>` for `ShowEnterpriseRouter`,
  `ListVpcAttachments` and `ListRouteTables`.
- **Array parameter** — `state`, `id`, `vpc_id`, `enterprise_project_id`,
  `sort_key`, `sort_dir` are declared as `array<string>`; KooCLI requires the
  indexed form `--state.1=available`, `--id.1=er-0001`,
  `--vpc_id.1=vpc-0001`, `--enterprise_project_id.1=0`,
  `--sort_key.1=name`, `--sort_dir.1=asc`. A bare `--state=<v>` is rejected
  with `[USE_ERROR]Invalid parameter`.
- **Boolean parameter** — `--owned_by_self=true|false`,
  `--is_default_association_table=true|false`,
  `--is_default_propagation_table=true|false`.
- **Paging** — `--limit` + `--marker` (1–2000); the marker is the response
  `page_info.next_marker` (a resource id).
- **REST paths (official SDK `resource_path`)** —
  `GET /v3/{project_id}/enterprise-router/instances`,
  `GET /v3/{project_id}/enterprise-router/instances/{er_id}`,
  `GET /v3/{project_id}/enterprise-router/{er_id}/vpc-attachments`,
  `GET /v3/{project_id}/enterprise-router/{er_id}/route-tables`; the project_id
  is resolved by KooCLI from the credential profile.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty ER list | Exit 0, prints `当前区域（<x>）无企业路由器（ER）` (+ active filters) |
| Empty attachment list | Exit 0, prints `企业路由器 <er-id> 无 VPC 连接（VPC Attachment）` |
| Empty route table list | Exit 0, prints `企业路由器 <er-id> 无路由表（Route Table）` |
| 403 / insufficient IAM permission | Exit 1, `无权限访问企业路由器（ER），请检查 IAM 权限` hint (also when KooCLI returns a JSON error body with exit code 0) |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| Missing project_id (SDK fallback) | Exit 1, hint to pass `--project-id` or set the project-id env var |
| Invalid / unknown `--er-id` | Exit 1, `未找到指定的企业路由器（ER 不存在，或 --er-id 有误）`; never a traceback |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdker` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud ER <Operation> --help` |
| `--page-size` out of range | Exit 1, explicit 1–2000 range hint |
| `attachment` / `route-table` / `detail` without `--er-id` | Exit 1, explicit `--er-id` required hint |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty list; `1` config, auth, guard, not-found or API
error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Non-`available` ERs / attachments | Rendered in a separate `[!]` / `[异常]` section, not treated as failure and never mixed with healthy rows |
| `--state failed` / other abnormal states | Forwarded as a server-side filter; only matching resources are returned |
| `--name` / `--fuzzy` | Applied locally after paging, so they never hide a server-side paging quirk |
| Large resource count | Automatic `marker` paging (`page_info.next_marker` aware, max 100 pages) |
| Extra response fields | `--json` preserves every field; fixed tables keep their contract |
| Field missing on a resource | Rendered as `-` |
| List value (`availability_zone_ids`) | Joined with `,` in the table |
| Nested object (`tags`) | Compacted into a single JSON cell |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdker`, same output modes |
| User asks to create/delete/update an ER | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess and fake SDK objects (no
credentials, no network):

```bash
cd skills/network/er/huawei-cloud-er-list
python3 -m unittest discover -s tests -v
```

Static checks:

```bash
bash -n scripts/ensure_cli.sh
bash -n scripts/install_cli.sh
python3 -m py_compile scripts/list_er.py
python3 -m json.tool templates/test-vars.json >/dev/null
```

Coverage: write-intent guard (read passes / create / delete / update /
associate / disassociate / enable / disable / normalized variants / per-resource
operation whitelist / allowed `--resource` values / local filter values),
command construction (array forms, boolean forms, marker paging), JSON
extraction, JSON error bodies returned with exit code 0 (403 and 404), failure
classification, marker paging, SDK fallback dispatch and request/response
wiring (enterprise routers / VPC attachments / route tables / detail), local
name filters, abnormal-state section rendering, and all `main()` output modes
(compact / table / json / detail / empty / error).

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy (action names verified via `GetAuthorizationSchemaV5`) |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation, credential configuration and skill-quality-cli |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified, plus API/parameter provenance |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |