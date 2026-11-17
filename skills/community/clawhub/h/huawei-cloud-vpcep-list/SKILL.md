---
name: huawei-cloud-vpcep-list
description: |
  1. List Huawei Cloud VPCEP (VPC 终端节点服务) resources in a tenant through
     KooCLI — three read-only views: terminal endpoints
     (`VPCEP ListEndpoints`, GET /v1/{project_id}/vpc-endpoints),
     endpoint services owned by the account
     (`VPCEP ListEndpointService`, GET /v1/{project_id}/vpc-endpoint-services),
     and public endpoint services published by O&M
     (`VPCEP ListServicePublicDetails`,
     GET /v1/{project_id}/vpc-endpoint-services/public).
     Falls back to the official `huaweicloudsdkvpcep` SDK when hcloud is absent.
  2. Three views: --view endpoint (default) / service / public; offset+limit
     paging until a short page; client-side filters --name / --fuzzy / --id /
     --vpc-id / --service-name / --status; --region override (default cn-north-4).
  3. Output modes: concise name/status/service list (default), fixed-column
     --table (ID / 名称 / 状态 / 所属服务名 / 服务ID / 服务类型 / IP / VPC ID /
     是否启用DNS / 是否启用白名单 / 创建时间 / region), raw --json, and
     --format md (fixed columns, '-' for missing fields, atomic write).
  4. Non-available resources (creating / failed / deleting / rejected) are
     split into a separate highlighted section and never mixed with available
     rows; `--status failed` can list only abnormal endpoints.
  5. Explicit Chinese hints for empty lists, invalid IDs, 403 / missing IAM
     permission, missing AK/SK credentials and KooCLI [USE_ERROR], with a
     non-zero exit code and no traceback.
  6. Built-in write-intent guard: create / update / delete / batch-add /
     batch-remove / add-whitelist / remove-whitelist / accept / reject / bind /
     unbind intents are rejected before execution (exit 1); this skill is
     strictly read-only.
  7. Triggers include: "查询 VPCEP", "终端节点列表", "VPC 终端节点", "终端节点服务",
     "公共终端节点服务", "VPCEP endpoint inventory", "list vpc endpoints",
     "list endpoint services", "list public endpoint services", "华为云 VPCEP".
tags: [huawei-cloud, vpcep, network, readonly, koo-cli]
---

# Huawei Cloud VPCEP (终端节点服务) Endpoint / Service List

## Overview

Query the VPCEP inventory of a tenant through KooCLI read-only GET APIs:
terminal endpoints (ListEndpoints), endpoint services owned by the account
(ListEndpointService), and public endpoint services published by O&M
(ListServicePublicDetails). The skill targets troubleshooting
("the endpoint is created but cannot connect", "which endpoints hang under this
VPC", "what is the public endpoint service name for OBS/DNS") and daily
inventory.

Architecture:

```text
agent → python3 scripts/list_vpcep.py --view endpoint|service|public
      → VPCEP ListEndpoints | ListEndpointService | ListServicePublicDetails
        --cli-region=<region> --limit=<n> --offset=<n> [+ real query params]
      → Huawei Cloud VPCEP OpenAPI (vpcep.<region>.myhuaweicloud.com)
      → client-side filters → concise / --table / --json / --format md

(hcloud binary missing) → fallback: huaweicloudsdkvpcep
      VpcepClient.list_endpoints / list_endpoint_service /
      list_service_public_details
```

Key properties:

- **Read-only by design** — only GET list operations are ever invoked. A
  write-intent guard scans arguments before argparse and rejects mutating
  vocabulary (create / delete / update / batch / whitelist / accept / reject /
  bind / unbind, …) with exit code 1 before a single command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  `hcloud` binary is absent the script falls back to the official
  `huaweicloudsdkvpcep` SDK. Credentials are always read by the CLI profile /
  SDK environment — never handled or echoed by the script.
- **Three views** — `--view endpoint` (default), `--view service` (services
  owned by the account), `--view public` (public services visible to all users).
- **Offset + limit paging** — every request sends `--limit` and `--offset`;
  paging stops at a short page or when `total_count` is reached (max 100 pages).
- **Non-available highlighted** — status other than `available` is rendered in a
  separate exception section with a `[!]` marker and `[异常]` status cell.
- **Offline-testable** — mock-hcloud and fake-SDK unit tests cover every view,
  paging, filters, guard, error classification and Markdown export.

Out of scope: all mutating VPCEP actions (create / update / delete an endpoint
or service, add / remove permissions or whitelist entries, accept / reject
connections, bind / unbind routetables). Those require a dedicated write-capable
skill with explicit **用户确认** (user confirmation).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdkvpcep` to enable
   the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band (run the
   KooCLI configure command in your terminal, or set credential environment
   variables). Never paste AK/SK into chat; the script never reads, echoes, or
   stores secrets itself — authentication is delegated entirely to the hcloud
   profile / SDK environment.
3. **project_id (SDK fallback only)** — VPCEP REST paths are
   `/v1/{project_id}/vpc-endpoints` and
   `/v1/{project_id}/vpc-endpoint-services`; when falling back to the SDK,
   supply the project id via `--project-id` or the
   `HUAWEICLOUD_SDK_PROJECT_ID` / `HUAWEI_PROJECT_ID` environment variables.
   KooCLI resolves it from the profile automatically.
4. **IAM permission** — read-only `vpcep:endpoints:list`,
   `vpcep:endpointServices:list` and `vpcep:endpointServices:listPublic`;
   least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
5. **Python 3.8+** (standard library only — argparse / json / subprocess).
6. **Outbound HTTPS** access to `vpcep.cn-north-4.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`) and the view:
   `endpoint` (default), `service`, or `public`.
2. **Confirm KooCLI readiness** (optional, read-only) by listing the active
   credential profile.
3. **Run the list script** with the desired view, output mode and filters.
4. **Read the result** — concise list for humans, `--table` for a fixed-column
   inventory, `--json` for downstream tooling, `--format md` for a local report.
5. **Handle non-available resources** — they appear in the separate exception
   section; use `--status failed` (or another state) to list only abnormal rows.
6. **Handle empty / error cases** per the Error Handling table below (the
   script prints explicit Chinese hints for empty region, 403, invalid ID and
   missing AK/SK).

## Core Commands

```bash
# Endpoint view (default): concise name / status / service list
python3 scripts/list_vpcep.py --region cn-north-4

# Endpoint view fixed-column table
python3 scripts/list_vpcep.py --table --region cn-north-4

# Endpoint services owned by the account
python3 scripts/list_vpcep.py --view service --table --region cn-north-4

# Public endpoint services (e.g. find the service name for OBS / DNS)
python3 scripts/list_vpcep.py --view public --name dns --fuzzy --region cn-north-4

# Endpoints under one VPC, abnormal only
python3 scripts/list_vpcep.py --vpc-id <vpc-id> --region cn-north-4
python3 scripts/list_vpcep.py --status failed --table --region cn-north-4

# Raw JSON / Markdown report
python3 scripts/list_vpcep.py --json
python3 scripts/list_vpcep.py --view public --format md --output vpcep-public.md
```

Equivalent direct KooCLI commands (the script wraps exactly these calls, with
offset+limit paging):

```bash
hcloud VPCEP ListEndpoints --cli-region=cn-north-4 --limit=100 --offset=0
hcloud VPCEP ListEndpointService --cli-region=cn-north-4 --limit=100 --offset=0
hcloud VPCEP ListServicePublicDetails --cli-region=cn-north-4 --limit=100 --offset=0
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--view` | No | `endpoint` (default) / `service` / `public` | `public` |
| `--name` | No | Filter by resource name; exact (case-insensitive) by default | `vpcep-svc-alpha` |
| `--fuzzy` | No | Make `--name` / `--service-name` a case-insensitive substring match | — |
| `--id` | No | Filter by exact resource ID | `8f...` |
| `--vpc-id` | No | Filter endpoints by VPC ID (endpoint view) | `vpc-0001` |
| `--service-name` | No | Filter by the endpoint service name | `obs` |
| `--status` | No | Filter by status (client-side exact, case-insensitive) | `failed` |
| `--table` | No | Render the fixed-column table for the selected view | — |
| `--json` | No | Output the raw response item array as JSON | — |
| `--format` | No | Export a local Markdown report (`md`) | `md` |
| `--output` | No | Markdown output path (default `vpcep-<view>-<timestamp>.md`) | `report.md` |
| `--page-size` | No | Page size (default 100; endpoints 1–500, services 1–1000) | `100` |
| `--project-id` | No | Project ID (needed by the SDK fallback path) | `05f...` |
| `--sort-key` | No | `create_at` / `update_at` (real server-side parameter) | `create_at` |
| `--sort-dir` | No | `asc` / `desc` (real server-side parameter) | `desc` |
| `--operation` | No | KooCLI operation name; only the three read-only list operations | `ListEndpoints` |

Output-mode precedence: `--json` → `--format md` → `--table` → concise list.
All user-supplied filters are applied client-side after paging, so exact
matching stays exact even though the API's name query supports fuzzy match.

## Output Modes

| Mode | Content |
| ------ | --------- |
| Default (concise) | `名称 / 状态 / 所属服务名` per row, split into AVAILABLE and 非 AVAILABLE sections |
| `--table` | Fixed columns per view; missing fields render `-`; booleans render 是/否; non-available status renders `[异常] <status>` |
| `--json` | The raw item array (every field returned by the API), indented JSON |
| `--format md` | Fixed-column Markdown report; missing fields `-`; empty result still emits the table header; written atomically via temp file + `os.replace` |

Fixed `--table` columns:

- **endpoint**: 终端节点ID / 名称 / 状态 / 所属服务名 / 服务ID / 服务类型 /
  IP / VPC ID / 是否启用DNS / 是否启用白名单 / 创建时间 / region
- **service**: 服务ID / 名称 / 状态 / 后端类型 / 创建时间 / region
- **public**: 服务ID / 名称 / 服务类型 / 创建时间

## Write-Intent Guard

- The script scans user arguments **before argparse** for mutating vocabulary
  and operation names (`CreateEndpoint`, `DeleteEndpointService`,
  `UpdateEndpoint`, `AddOrRemoveServicePermissions`, `AcceptOrRejectEndpoint`,
  `batch-add`, `batch-remove`, `add-whitelist`, `remove-whitelist`, `accept`,
  `reject`, `bind`, `unbind`, `delete`, `update`, and similar).
- Any hit prints `[错误] 检测到写操作意图 ... 已被守卫拦截` and exits **1** before a
  single hcloud command is executed.
- Read-only option values that merely contain such words are exempt from the
  scan: `--status rejected`, `--status creating`, `--status deleting`,
  `--sort-key update_at` and `--sort-key create_at` work as normal filters.
- Only the three read-only list operations (or the SDK `list_endpoints` /
  `list_endpoint_service` / `list_service_public_details` calls in the fallback
  path) are ever constructed — there is no code path that can issue a mutating
  VPCEP API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `VPCEP`.
- **Operation name** — PascalCase: `ListEndpoints`, `ListEndpointService`,
  `ListServicePublicDetails`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete VPCEP call).
- **Simple parameter** — `--key=value`, e.g. `--limit=100`, `--offset=0`,
  `--endpoint_service_name=obs`, `--id=<id>`, `--vpc_id=<vpc-id>`,
  `--status=failed`, `--sort_key=create_at`, `--sort_dir=desc`.
- **Paging** — `--limit` + `--offset`; offset increases by the page size until
  the returned batch is shorter than the page size or `total_count` is reached.
- **REST paths (official SDK `_http_info`)** —
  `GET /v1/{project_id}/vpc-endpoints`,
  `GET /v1/{project_id}/vpc-endpoint-services`,
  `GET /v1/{project_id}/vpc-endpoint-services/public`; the project_id is
  resolved by KooCLI from the credential profile.
- **Verified parameter snapshot** — endpoint view accepts `endpoint_service_name`
  (case-insensitive fuzzy), `id`, `vpc_id`, `limit` (0–500), `offset`,
  `sort_key`, `sort_dir`; service view accepts `endpoint_service_name`, `id`,
  `status` (`creating|available|failed|deleting`), `net_type`, `limit` (0–1000),
  `offset`, `sort_key`, `sort_dir`; public view accepts
  `endpoint_service_name` (case-sensitive fuzzy), `id`, `limit` (0–1000),
  `offset`, `sort_key`, `sort_dir`.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty list | Exit 0, prints `当前区域（<x>）无 VPCEP <view>` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问终端节点服务（VPCEP），请检查 IAM 权限` hint listing the three list actions |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| Invalid / unknown resource ID | Exit 1, `参数或资源 ID 无效` hint (UUID shape, region, view match) |
| Missing project_id (SDK fallback) | Exit 1, hint to pass `--project-id` or set the project-id env var |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkcore huaweicloudsdkvpcep` |
| Network / API failure | Exit 1 with a Chinese message and a short server excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit 参数错误 hint pointing to the operation `--help` output |
| API error body with KooCLI exit code 0 | Exit 1, classified by error code / message (403 / invalid ID / generic) |
| Write intent detected | Exit 1, guard message, no command executed |

Exit codes: `0` success or empty result; `1` guard, config, auth, invalid-ID or
API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Non-`available` endpoints / services | Split into a separate `[!]` exception section; `--status <state>` filters to abnormal rows |
| Endpoint has no separate `name` field | Rendered name = `endpoint_service_name` (the API's endpoint-service name) |
| `--id` / `--vpc-id` / `--service-name` / `--status` filters | Exact client-side matching after paging; `--fuzzy` switches name matching to substring |
| Page larger than the API limit | Clamped to 500 (endpoint) / 1000 (service, public) |
| Empty page before `total_count` | Paging stops (short page) |
| Extra response fields | Preserved in `--json`; fixed table/Markdown columns stay stable |
| Field missing on an item | Rendered as `-` in `--table` and Markdown |
| Nested `tags` / `error` objects | Rendered as compact JSON in the table cell |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkvpcep`, same views and output modes |
| User asks to create/delete/accept an endpoint | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess and a fake SDK (no
credentials, no network):

```bash
cd skills/network/vpcep/huawei-cloud-vpcep-list
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / update / batch /
whitelist / accept / reject / bind / unbind / normalized variants / status and
sort-key exemptions / operation whitelist), view-to-operation resolution,
command construction (per-view parameters, offset paging, no mutating flags),
JSON extraction, payload-error classification (403 with rc=0, invalid ID),
failure classification (missing AK/SK, 403, generic, `[USE_ERROR]` with rc=0),
offset paging (short page / `total_count` / empty / page-size clamp), SDK
fallback (three views / env credentials / missing credentials / missing project
id / unknown region / auth failure / invalid ID / official request-model
regression), client-side filters, fixed-column table/Markdown rendering,
atomic Markdown write, and all `main()` output modes including empty, filter,
guard and error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |