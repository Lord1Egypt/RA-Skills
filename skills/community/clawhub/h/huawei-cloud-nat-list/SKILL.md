---
name: huawei-cloud-nat-list
description: |
  1. List Huawei Cloud public NAT gateways in a tenant region through
     KooCLI (hcloud NAT ListNatGateways — read-only GET
     /v2/{project_id}/nat_gateways), with an automatic fallback to the
     official huaweicloudsdknat v2 SDK when hcloud is not installed.
  2. Three output modes: full-field table (default, every returned field
     including ID/名称/规格/状态/关联VPC/状态/创建时间), --json (raw response
     array), and --names-only (compact NAT gateway name list).
  3. Supports --name / --spec / --status / --vpc (router_id) filtering (all
     real server-side ListNatGateways query parameters), region override, and
     automatic marker paging.
  4. Explicit error hints for empty NAT gateway lists (「当前区域无公网NAT网关」),
     403 / insufficient IAM permission (「无权限访问公网NAT网关」), missing or
     invalid AK/SK credentials, missing project_id on the SDK fallback, and
     hcloud not installed.
  5. Built-in write-intent guard: any mutating intent (create / delete /
     update / SNAT / DNAT rule changes / tag changes) or any operation other
     than ListNatGateways is rejected before execution — this skill is
     strictly read-only.
  6. Triggers include: "list NAT gateways", "nat gateway list", "NAT网关列表",
     "查询NAT网关", "查询公网NAT网关", "公网NAT网关列表", "NAT 实例列表",
     "华为云 NAT", "nat gateway inventory".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, filters,
     marker paging, error scenarios, SDK fallback, and the write-intent guard.
tags: [huawei-cloud, nat, network, readonly, koo-cli]
---

# Huawei Cloud Public NAT Gateway List

## Overview

Query the public NAT gateway list of a tenant through KooCLI
`hcloud NAT ListNatGateways` (official read-only GET
`/v2/{project_id}/nat_gateways`, verified in the `huaweicloudsdknat` v2
client `_list_nat_gateways_http_info` metadata and the KooCLI
[CLI 命令参考](https://support.huaweicloud.com/clir-natgateway/nat-cli.html)).
The skill is aimed at NAT gateway inventory inspection, daily operations
patrol, and as a pre-query step for other skills that need a NAT gateway
`id` or its associated VPC `router_id`.

Architecture:

```text
agent → python3 scripts/list_nat_gateways.py → hcloud NAT ListNatGateways --cli-region=<region>
      → Huawei Cloud NAT OpenAPI (nat.<region>.myhuaweicloud.com) → parsed JSON → table / --json / --names-only

(hcloud binary missing) → fallback: huaweicloudsdknat v2 NatClient.list_nat_gateways
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListNatGateways`
  (GET). A write-intent guard scans user arguments and validates the operation
  name; mutating intents (create / delete / update / SNAT / DNAT rule
  changes / tag changes) are rejected with an explicit message before any
  command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  KooCLI binary is absent, the script falls back to the official
  `huaweicloudsdknat` v2 SDK (`list_nat_gateways`). Credentials are always read
  by the CLI profile / SDK environment — never handled by the script.
- **Full-field table output** — the default table renders the union of all
  fields returned by ListNatGateways (spec 取值：`1` 小型 / `2` 中型 /
  `3` 大型 / `4` 超大型 / `5` 企业型).
- **Offline-testable** — every code path (marker paging, filters, error
  classification, guard, SDK fallback) is covered by unit tests that mock the
  hcloud subprocess.

Out of scope: private NAT gateways, every SNAT / DNAT rule action (list /
create / update / delete), and every mutating NAT gateway action (create /
update / delete a gateway, EIP binding, tag changes, prepaid conversion).
Those require a dedicated write-capable skill and explicit user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdknat` to enable
   the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band
   (run the KooCLI configure command in your terminal, or set credential
   environment variables).
   Never paste AK/SK into chat; the script never reads, echoes, or stores
   secrets itself — authentication is delegated entirely to the hcloud profile
   / SDK environment.
3. **project_id (SDK fallback only)** — the NAT REST path is
   `/v2/{project_id}/nat_gateways`; when falling back to the SDK, supply the
   project id via `--project-id` or the `HUAWEICLOUD_SDK_PROJECT_ID` /
   `HUAWEI_PROJECT_ID` environment variables. The KooCLI path resolves it from
   the profile automatically.
4. **IAM permission** — read-only `nat:natGateways:list`; least-privilege
   policy in [references/iam-policies.md](references/iam-policies.md).
5. **Python 3.8+** (standard library only — argparse / json / subprocess).
6. **Outbound HTTPS** access to `nat.cn-north-4.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`).
2. **Confirm KooCLI readiness** (optional, read-only) by listing the active
   credential profile.
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — table for humans, `--json` for downstream tooling,
   `--names-only` for a compact inventory.
5. **Handle the empty / error cases** per the Edge Cases table below (the
   script prints an explicit hint for empty region, 403, and missing AK/SK).

## Core Commands

```bash
# Full-field table (default)
python3 scripts/list_nat_gateways.py --region cn-north-4

# Raw JSON of every returned field
python3 scripts/list_nat_gateways.py --json

# Compact NAT gateway name list only
python3 scripts/list_nat_gateways.py --names-only

# Filter by gateway status (server-side query parameter)
python3 scripts/list_nat_gateways.py --status ACTIVE

# Filter by spec: 1 small / 2 medium / 3 large / 4 extra-large
python3 scripts/list_nat_gateways.py --spec 1

# Filter by exact name / associated VPC router_id
python3 scripts/list_nat_gateways.py --name my-nat
python3 scripts/list_nat_gateways.py --vpc d0a1b2c3-4d5e-6f70-8192-a3b4c5d6e7f8

# Combine filters
python3 scripts/list_nat_gateways.py --region cn-north-4 --status ACTIVE --spec 2
```

Equivalent direct KooCLI command (the script wraps exactly this call, with
marker paging):

```bash
hcloud NAT ListNatGateways --cli-region=cn-north-4 --limit=2000
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--json` | No | Output the raw gateway array as JSON | — |
| `--names-only` | No | Output NAT gateway name list only | — |
| `--name` | No | Filter by exact gateway name — real server-side ListNatGateways query parameter | `my-nat` |
| `--spec` | No | Filter by spec (`1` 小型 / `2` 中型 / `3` 大型 / `4` 超大型 / `5` 企业型) — real server-side query parameter | `1` |
| `--status` | No | Filter by gateway state (`ACTIVE` / `PENDING_CREATE` / `PENDING_UPDATE` / `PENDING_DELETE` / `INACTIVE`) — real server-side query parameter | `ACTIVE` |
| `--vpc` | No | Filter by the router_id of the associated VPC — real server-side query parameter (`router_id`) | `d0a1b2c3-4d5e-6f70-8192-a3b4c5d6e7f8` |
| `--page-size` | No | Page size for ListNatGateways (default 2000, the official API default/upper bound) | `2000` |
| `--project-id` | No | Project ID (needed by the SDK fallback path for `/v2/{project_id}/...`) | `05f...` |
| `--operation` | No | hcloud NAT operation name; only `ListNatGateways` is allowed | `ListNatGateways` |

Output-mode precedence: `--json` → `--names-only` → table (default).

## Write-Intent Guard

- The script scans the operation/command tokens (not user filter values such
  as `--name` / `--status`) for mutating vocabulary (`create`, `delete`,
  `update`, `modify`, `associate`, `disassociate`, `attach`, `detach`, `bind`,
  `unbind`, `release`, `change`, `restart`, and NAT operation names such as
  `CreateNatGateway`, `DeleteNatGateway`, `UpdateNatGateway`, `CreateSnatRule`,
  `DeleteDnatRule`, `BatchCreateDeleteNatGatewayTag`). This keeps legitimate
  queries such as `--name prod-start` working while still rejecting write
  intent.
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed.
- Only `hcloud NAT ListNatGateways` (GET) — or the SDK `list_nat_gateways`
  call in the fallback path — is ever constructed by `build_command()`; there
  is no code path that can issue a mutating NAT API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `NAT`.
- **Operation name** — PascalCase: `ListNatGateways`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete NAT call).
- **Simple parameter** — `--key=value`, e.g. `--limit=100`, `--marker=<token>`,
  `--name=my-nat`, `--router_id=d0a1b2c3-4d5e-6f70-8192-a3b4c5d6e7f8`
  (`router_id` must be the 36-character VPC router UUID).
- **Array parameter** — `spec` / `status` are declared `array<string>` by
  KooCLI, so the indexed form is required: `--spec.1=1`, `--status.1=ACTIVE`
  (a bare `--spec=1` / `--status=ACTIVE` is rejected with
  `[USE_ERROR]Invalid parameter`). All four filters are real server-side
  ListNatGateways parameters (verified against the `huaweicloudsdknat` v2
  `ListNatGatewaysRequest` model).
- **Paging** — `limit` + `marker`; NAT v2 `marker` is the starting resource
  id, so the script passes the last gateway `id` of the current page as the
  next `marker` and stops when the returned batch is shorter than `limit`
  (the response has no `next_marker` / `page_info`).
- **REST path (official SDK `_http_info`)** —
  `GET /v2/{project_id}/nat_gateways` (`huaweicloudsdknat` v2
  `_list_nat_gateways_http_info`); the project_id is resolved by KooCLI from
  the credential profile.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty NAT gateway list | Exit 0, prints `当前区域（<x>）无公网NAT网关` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问公网NAT网关，请检查 IAM 权限` hint |
| 401 / invalid or expired AK-SK | Exit 1, `凭证无效（401：AK/SK 无效或已过期）` hint (never reported as 403) |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| Missing project_id (SDK fallback) | Exit 1, hint to pass `--project-id` or set the project-id env var |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkcore huaweicloudsdknat` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud NAT ListNatGateways --help` |
| KooCLI API error envelope (`{"error_code": ..., "error_msg": ...}` or nested `error`, even with exit code 0) | Exit 1, classified as 401/403/API error; never treated as an empty gateway list |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Non-`ACTIVE` gateways | Reported with their state (`PENDING_CREATE` / `PENDING_UPDATE` / `PENDING_DELETE` / `INACTIVE` / ...), not treated as failure |
| `--name` / `--spec` / `--status` / `--vpc` filters | Forwarded as real server-side query parameters (verified API params) |
| Large gateway count | Automatic id-marker paging (last gateway `id` as marker, short page stops, max 100 pages) |
| Extra response fields | Table columns are built from the union of returned fields — new fields appear automatically |
| Field missing on a gateway | Rendered as `-` in the table |
| Nested `session_conf` | Rendered as compact JSON inside its table cell |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdknat` list_nat_gateways, same output modes |
| User asks to create/delete/update a NAT gateway or SNAT/DNAT rules | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / SNAT / DNAT /
update / normalized variants / operation whitelist), command construction
(filters forwarded server-side; marker never sent on the first page), JSON
extraction and answer-envelope detection, failure classification (missing
AK/SK, 401, 403, generic, `[USE_ERROR]` with rc=0, API error envelope with
rc=0), id-marker paging (last id / short page / exact-full-page boundary /
chained markers across pages / empty / repeated marker / unsupported
next_marker ignored), SDK fallback (success, missing credentials, missing
project id, 401 vs 403, unavailable; request construction matches the real
`ListNatGatewaysRequest` signature), rendering (table union fields / names /
fallbacks), and all main() output modes including empty, filter, and error
paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
