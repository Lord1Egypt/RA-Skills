---
name: huawei-cloud-product-list
description: |
  1. List the Huawei Cloud product (service) catalog — the 云服务类型 directory —
     through KooCLI (hcloud BSS ListServiceTypes, read-only
     GET /v2/products/service-types), with an automatic fallback to the official
      huaweicloudsdkbss v2 SDK when hcloud is not installed or the CLI metadata
      lacks the BSS service.
  2. Every catalog item carries the product name (service_type_name / 名称), its
     service type code (service_type_code / 编码) and its abbreviation
     (abbreviation / 缩写), so users can browse the对外开放 Huawei Cloud product line
     in one call.
  3. Three output modes: table (default — 名称 / 编码 / 缩写), --json (raw response
     array with every returned field), and --names-only (compact product name
     list). Output is written to stdout only (errors go to stderr).
  4. Supports --name (server-side fuzzy match on the service type name), --code
     (client-side match on the service type code), region override, page-size, and
     automatic offset paging.
  5. Explicit error hints for an empty catalog
     (「未查询到华为云产品（服务）目录数据」), 403 / insufficient IAM permission
     (「无权限访问华为云产品目录…，请检查 IAM 权限」), missing or invalid AK/SK
     credentials, and hcloud not installed.
  6. Built-in write-intent guard: any mutating intent (create / delete / update /
     modify / transfer / reclaim / adjust / freeze / send / issue / cancel ...)
     or any operation other than ListServiceTypes is rejected before execution —
     this skill is strictly read-only.
  7. Triggers include: "华为云产品列表", "产品目录", "服务目录", "云服务类型",
     "华为云有哪些产品", "list huawei cloud products", "service catalog",
     "product catalog", "list cloud services", "huawei cloud service types".
  8. Offline unit tests (mocked hcloud subprocess) cover output modes, filters,
     paging, error scenarios, SDK fallback, standardization, and the write-intent
     guard.
tags: [huawei-cloud, catalog, bss, readonly, koo-cli]
---

# Huawei Cloud Product (Service) Catalog List

## Overview

List the Huawei Cloud product (service) catalog — the 云服务类型 directory —
through KooCLI `hcloud BSS ListServiceTypes` (official read-only GET
`/v2/products/service-types`, verified in the `huaweicloudsdkbss` v2 client
`_list_service_types_http_info` metadata). Each entry exposes the product name
(`service_type_name`), its service type code (`service_type_code`) and its
abbreviation (`abbreviation`). The skill is aimed at browsing the available
Huawei Cloud product line, product/service selection pre-research, and catalog
export.

Architecture:

```text
agent → python3 scripts/list_products.py → hcloud BSS ListServiceTypes --cli-region=<region>
      → Huawei Cloud BSS OpenAPI (global endpoint) → parsed JSON
      → 名称/编码/缩写 table / --json / --names-only

(hcloud binary missing, or CLI metadata lacks BSS: `Unsupported service: BSS.`)
  → fallback: huaweicloudsdkbss v2 BssClient.list_service_types
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListServiceTypes`
  (GET). A write-intent guard scans user arguments and validates the operation
  name; mutating intents (create / delete / update / transfer / reclaim / adjust
  / freeze / send / issue / cancel ...) are rejected with an explicit message
  before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  KooCLI binary is absent, or its offline metadata does not include the BSS
  service (`[USE_ERROR]Unsupported service: BSS.`), the script falls back to the
  official `huaweicloudsdkbss` v2 SDK (`list_service_types`). BSS is a *global* service,
  so the SDK path uses `GlobalCredentials` + `with_endpoints`
  (`https://bss.myhuaweicloud.com`). Credentials are always read by the CLI
  profile / SDK environment — never handled by the script.
- **Catalog table output** — the default table renders 名称 / 编码 / 缩写 for a
  stable, easy-to-consume product inventory; `--json` preserves every returned
  field.
- **Offline-testable** — every code path (paging, filters, error classification,
  guard, SDK fallback, standardization) is covered by unit tests that mock the
  hcloud subprocess.

Out of scope: every mutating BSS operation (create / update / delete a product,
resource or coupon, order placement, account changes). Those require a dedicated
write-capable skill and explicit user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `python3 scripts/ensure_env.py` (or
   `pip install huaweicloudsdkcore huaweicloudsdkbss`) to enable the SDK fallback
   path.
2. **Active credential profile** — configure credentials out-of-band
   (run the KooCLI configure command in your terminal, or set credential
   environment variables). Never paste AK/SK into chat; the script never reads,
   echoes, or stores secrets itself — authentication is delegated entirely to
   the hcloud profile / SDK environment.
3. **IAM permission** — read-only BSS access (the catalog is a BSS domain API);
   least-privilege policy in [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess).
5. **Outbound HTTPS** access to `bss.myhuaweicloud.com`.
6. **Region** — BSS is a global service; use `cn-north-1` (the default here).

## Workflow

1. **Confirm the target region** (default `cn-north-1`; the catalog is global).
2. **Confirm KooCLI readiness** (optional, read-only) by listing the active
   credential profile.
3. **Run the catalog script** with the desired output mode and filters.
4. **Read the result** — 名称 / 编码 / 缩写 table for humans, `--json` for downstream
   tooling, `--names-only` for a compact product inventory.
5. **Handle the empty / error cases** per the Error Handling table below (the
   script prints an explicit hint for empty catalog, 403, and missing AK/SK).

## Core Commands

```bash
# Self-heal the SDK fallback dependencies (idempotent)
python3 scripts/ensure_env.py

# 名称 / 编码 / 缩写 table (default)
python3 scripts/list_products.py --region cn-north-1

# Raw JSON of every returned field
python3 scripts/list_products.py --json

# Compact product (service) name list only
python3 scripts/list_products.py --names-only

# Server-side fuzzy match on the product name
python3 scripts/list_products.py --name 弹性

# Client-side match on the service type code
python3 scripts/list_products.py --code obs

# Combine filters
python3 scripts/list_products.py --region cn-north-1 --name 存储 --names-only
```

Equivalent direct KooCLI command (the script wraps exactly this call, with
offset paging):

```bash
hcloud BSS ListServiceTypes --cli-region=cn-north-1 --limit=100 --offset=0
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-1`; BSS is global) | `cn-north-1` |
| `--json` | No | Output the raw catalog array as JSON (all fields) | — |
| `--names-only` | No | Output the product (service) name list only | — |
| `--name` | No | Fuzzy match on the product name — real server-side `service_type_name` parameter | `弹性` |
| `--code` | No | Filter by service type code — **applied client-side** (substring) | `obs` |
| `--page-size` | No | Page size for ListServiceTypes (default 100) | `100` |
| `--operation` | No | hcloud BSS operation name; only `ListServiceTypes` is allowed | `ListServiceTypes` |

Output-mode precedence: `--json` → `--names-only` → table (default).

## Write-Intent Guard

- The script scans all user arguments plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `modify`, `transfer`, `retrieve`,
  `reclaim`, `adjust`, `freeze`, `unfreeze`, `send`, `issue`, `cancel`,
  `destroy`, `release`, `remove`, and their Chinese equivalents, plus concrete BSS
  operation names such as `CreatePartnerCoupons`, `ReclaimPartnerCoupons`,
  `UpdateCouponQuotas`).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`,
  and exits with code 1 **before** a single hcloud command is executed.
- Only `hcloud BSS ListServiceTypes` (GET) — or the SDK
  `list_service_types` call in the fallback path — is ever constructed by
  `build_command()`; there is no code path that can issue a mutating BSS API
  call. Any write-capable operation would require a separate skill and explicit
  user confirmation (确认).

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `BSS`.
- **Operation name** — PascalCase: `ListServiceTypes`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-1`
  (required for every concrete BSS call; BSS is global, `cn-north-1`).
- **Simple parameter** — `--key=value`, e.g. `--limit=100`, `--offset=0`,
  `--service_type_name=弹性`.
- **REST path (official SDK `_http_info`)** — `GET /v2/products/service-types`
  (`huaweicloudsdkbss` v2 `_list_service_types_http_info`); the request carries
  no project_id — it is a global (domain) API.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty catalog | Exit 0, prints `未查询到华为云产品（服务）目录数据` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问华为云产品目录（BSS 云服务类型），请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure credentials out-of-band (never in chat) |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or run `scripts/ensure_env.py` |
| hcloud installed but its metadata lacks BSS (`Unsupported service: BSS.`, even with exit code 0) | Transparent SDK fallback; if the SDK is unavailable, the original `hcloud 参数错误` hint is kept |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud BSS ListServiceTypes --help` |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty catalog; `1` config, auth, guard, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| `--name` filter | Forwarded as the real server-side `service_type_name` fuzzy-match query parameter (prefix / suffix / middle) |
| `--code` filter | Applied client-side after the full paged list is fetched (substring, case-insensitive) |
| Large catalog | Automatic `offset` paging (total_count-aware, full-page fallback, max 100 pages) |
| Extra response fields | Dropped from the table (only 名称 / 编码 / 缩写); available via `--json` |
| Field missing on a product | Rendered as `-` in the table |
| `total_count` absent | Falls back to full-page paging detection |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkbss` `list_service_types` (GlobalCredentials + global endpoint), same output modes |
| hcloud present but metadata lacks BSS, SDK installed | Same transparent SDK fallback (detected via `Unsupported service`), same output modes |
| User asks to order / change a product | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / update / transfer /
reclaim / adjust / freeze / normalized variants / Chinese verbs / operation
whitelist), command construction (`service_type_name` forwarded server-side; no
write flags ever added), JSON extraction, failure classification (missing AK/SK,
403, generic, `[USE_ERROR]` with rc=0), offset paging (total_count / full page /
empty), SDK fallback (success / GlobalCredentials + `with_endpoints` / missing
credentials / unavailable; request construction matches the real
`ListServiceTypesRequest` signature), standardization (名称/编码/缩写 + `-`
defaults), rendering, the client-side `--code` filter, and all main() output
modes including empty, filter, and error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |