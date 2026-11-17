---
name: huawei-cloud-voucher-list
description: |
  1. List Huawei Cloud BSS (费用中心) vouchers / coupons of a tenant account
     through KooCLI (hcloud BSS ListSubCustomerCoupons — read-only
     GET /v2/promotions/benefits/coupons), with an automatic fallback to the
     official huaweicloudsdkbss v2 SDK when hcloud is not installed.
  2. Three output modes: full-field table (default, every returned field
     including 券ID/券码/状态/类型/面额/余额/有效期/促销计划), --json (raw
     response array), and --names-only (compact voucher / plan-name list).
  3. Supports --status / --name / --coupon-id filtering, region override, and
     automatic offset paging. --coupon-id and --status are real coupon-list
     query parameters (status accepts 1-5 or textual aliases such as
     available / used / expired / reclaimed); --name is applied client-side
     because the API has no name parameter.
  4. Explicit error hints for an empty voucher list (「当前区域无 BSS 代金券」),
     403 / insufficient IAM permission (「无权限访问 BSS 代金券，请检查 IAM
     权限」), missing or invalid AK/SK credentials, and hcloud not installed.
  5. Built-in write-intent guard: any mutating intent (create / delete /
     update / reclaim / transfer / retrieve / adjust / send / freeze / cancel)
     or any operation other than the read-only coupon list is rejected before
     execution — this skill is strictly read-only.
  6. Triggers include: "代金券盘点", "代金券列表", "查询代金券", "优惠券列表",
     "费用管理", "list BSS coupons", "list vouchers", "coupon inventory",
     "voucher list", "华为云代金券", "billing voucher query".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, filters,
     paging, error scenarios, SDK fallback, and the write-intent guard.
tags: [huawei-cloud, bss, billing, readonly, koo-cli]
---

# Huawei Cloud BSS Voucher (Coupon) List

## Overview

Query the voucher / coupon list of a Huawei Cloud account through KooCLI
`hcloud BSS ListSubCustomerCoupons` (official read-only GET
`/v2/promotions/benefits/coupons`, verified in the `huaweicloudsdkbss` v2
client `_list_sub_customer_coupons_http_info` metadata). The skill is aimed at
voucher inventory (代金券盘点), cost management (费用管理), and as a pre-query
step for other BSS skills that need a `coupon_id`.

Architecture:

```text
agent → python3 scripts/list_voucher.py → hcloud BSS ListSubCustomerCoupons --cli-region=<region>
      → Huawei Cloud BSS OpenAPI (global endpoint) → parsed JSON → table / --json / --names-only

(hcloud binary missing) → fallback: huaweicloudsdkbss v2 BssClient.list_sub_customer_coupons
```

Key properties:

- **Read-only by design** — the only API ever invoked is the coupon list
  (GET). A write-intent guard scans user arguments and validates the operation
  name; mutating intents (create / delete / reclaim / transfer / adjust / ...)
  are rejected with an explicit message before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  KooCLI binary is absent, the script falls back to the official
  `huaweicloudsdkbss` v2 SDK (`list_sub_customer_coupons`). BSS is a *global*
  service, so the SDK path uses `GlobalCredentials` + `with_endpoints`
  (`https://bss.myhuaweicloud.com`). Credentials are always read by the CLI
  profile / SDK environment — never handled by the script.
- **Full-field table output** — the default table renders the union of all
  fields returned by the coupon list, with the numeric `status` / `coupon_type`
  enumerations rendered as human-readable labels.
- **Offline-testable** — every code path (paging, filters, error
  classification, guard, SDK fallback) is covered by unit tests that mock the
  hcloud subprocess.

Out of scope: every mutating BSS operation (create / reclaim / transfer /
retrieve / adjust coupon quotas, claim / send / freeze / cancel coupons).
Those require a dedicated write-capable skill and explicit user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdkbss` to enable the
   SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band
   (hcloud configure in your terminal, or credential environment variables).
   Never paste AK/SK into chat; the script never reads, echoes, or stores
   secrets itself — authentication is delegated entirely to the hcloud profile
   / SDK environment.
3. **IAM permission** — read-only `bss:coupon:list`; least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess).
5. **Outbound HTTPS** access to `bss.myhuaweicloud.com`.
6. **Region** — BSS is a global service; use `cn-north-1` (the default here).

## Workflow

1. **Confirm the target region** (default `cn-north-1`); the coupon list is
   region-scoped to the global BSS endpoint.
2. **Confirm hcloud readiness** (optional, read-only): hcloud configure list.
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — table for humans, `--json` for downstream tooling,
   `--names-only` for a compact inventory.
5. **Handle the empty / error cases** per the Error Handling table below (the
   script prints an explicit hint for empty region, 403, and missing AK/SK).

## Core Commands

```bash
# Full-field table (default)
python3 scripts/list_voucher.py --region cn-north-1

# Raw JSON of every returned field
python3 scripts/list_voucher.py --json

# Compact voucher (plan-name) list only
python3 scripts/list_voucher.py --names-only

# Filter by voucher status (numeric 1-5 or textual alias; forwarded
# server-side when recognised)
python3 scripts/list_voucher.py --status available
python3 scripts/list_voucher.py --status 2

# Filter by exact voucher ID (server-side query parameter)
python3 scripts/list_voucher.py --coupon-id CP0001

# Filter by plan name / coupon code (client-side: full list fetched, then
# filtered locally — the API has no name parameter)
python3 scripts/list_voucher.py --name spring

# Combine filters
python3 scripts/list_voucher.py --region cn-north-1 --status used --names-only
```

Equivalent direct KooCLI command (the script wraps exactly this call, with
paging):

```bash
hcloud BSS ListSubCustomerCoupons --cli-region=cn-north-1 --offset=0 --limit=100
```

> The coupon-list operation is `ListSubCustomerCoupons` (the underlying
> `GET /v2/promotions/benefits/coupons`). `ListCoupons` is accepted as a
> read-only alias for the limited voucher-list feature. When hcloud is
> available, confirm the exact parameter list with
> `hcloud BSS ListSubCustomerCoupons --help`.

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-1`; BSS is global) | `cn-north-1` |
| `--json` | No | Output the raw voucher array as JSON | — |
| `--names-only` | No | Output voucher (plan) names only | — |
| `--status` | No | Filter by voucher status: `1` unactivated, `2` available, `3` used, `4` expired, `5` reclaimed — numeric codes or aliases (`available` / `used` / `expired` / `reclaimed` …) are forwarded server-side; unrecognised values fall back to a client-side label filter | `available`, `2` |
| `--name` | No | Filter by promotion plan name / coupon code — **applied client-side** (the API has no name parameter; full list fetched, then filtered locally, case-insensitive substring) | `spring` |
| `--coupon-id` | No | Filter by exact voucher ID (server-side query parameter) | `CP0001` |
| `--page-size` | No | Page size for the coupon list (BSS maximum 100; default 100) | `100` |
| `--operation` | No | hcloud BSS operation name; only the read-only coupon list is allowed (`ListSubCustomerCoupons` / alias `ListCoupons`) | `ListSubCustomerCoupons` |

Output-mode precedence: `--names-only` → `--json` → table (default).

## Write-Intent Guard

- The script scans all user arguments plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `modify`, `reclaim`, `transfer`,
  `retrieve`, `adjust`, `send`, `freeze`, `cancel`, plus the concrete BSS
  operation names `CreatePartnerCoupons`, `ReclaimPartnerCoupons`,
  `UpdateCouponQuotas`, `TransferEnterpriseMultiAccountCoupon`, …).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed.
- Read-only status labels are **not** blocked: specific operation names are
  matched instead of generic verbs for `reclaim*`, so `--status reclaimed`
  (已回收) passes the guard.
- Only the read-only coupon list (GET) — or the SDK
  `list_sub_customer_coupons` call in the fallback path — is ever constructed
  by `build_command()`; there is no code path that can issue a mutating BSS
  API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `BSS`.
- **Operation name** — PascalCase: `ListSubCustomerCoupons`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-1`
  (required for every concrete BSS call; BSS is global, `cn-north-1`).
- **Simple parameter** — `--key=value`, e.g. `--limit=100`, `--offset=20`,
  `--coupon_id=CP0001`, `--status=2`.
- **REST path (official SDK `_http_info`)** —
  `GET /v2/promotions/benefits/coupons` (`huaweicloudsdkbss` v2
  `_list_sub_customer_coupons_http_info`); the request carries no project_id —
  it is a global (domain) API.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty voucher list | Exit 0, prints `当前区域（<x>）无 BSS 代金券` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问 BSS 代金券，请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure credentials out-of-band (never in chat) |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkcore huaweicloudsdkbss` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit hcloud 参数错误 hint pointing to `hcloud BSS ListSubCustomerCoupons --help` |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| `--status` numeric / alias | Forwarded server-side as the numeric BSS status code (1-5); displayed with a human-readable label |
| `--status` unrecognised text | Applied client-side on the rendered status label (case-insensitive) |
| `--name` filter | Applied client-side after the full paged list is fetched (the API has no name parameter) |
| Large voucher count | Automatic `offset` paging (count-aware, full-page fallback, max 100 pages, page size capped at 100) |
| Extra response fields | Table columns are built from the union of returned fields — new fields appear automatically |
| Field missing on a voucher | Rendered as `-` in the table |
| Nested `use_limits` | Flattened into a `useLimits` JSON column for the table |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkbss` `list_sub_customer_coupons` (GlobalCredentials + global endpoint), same output modes |
| User asks to create/reclaim/transfer coupons | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / reclaim / update / transfer
/ freeze / normalize variants / operation whitelist + `ListCoupons` alias /
read-only status label not blocked), `--status` parsing (numeric / aliases /
unknown), command construction (including "no name parameter is ever sent to
the server"), JSON extraction, failure classification (missing AK/SK, 403,
generic, `[USE_ERROR]` with rc=0), server-side status forwarding, client-side
name / status filtering, paging (count / full-page / empty), SDK fallback
(success / unavailable; GlobalCredentials + `with_endpoints`; request
construction matches the real `ListSubCustomerCouponsRequest` signature —
`name=` must raise TypeError), rendering (table with status/type/plan/amount
fields / names / fallbacks), and all main() output modes including empty,
filter, and error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
