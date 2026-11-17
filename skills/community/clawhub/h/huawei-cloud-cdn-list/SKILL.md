---
name: huawei-cloud-cdn-list
description: |
  1. List Huawei Cloud CDN (Content Delivery Network) accelerated domains in a
     tenant through KooCLI (hcloud CDN ListDomains — read-only GET
     /v1.0/cdn/domains), with an automatic fallback to the official
     huaweicloudsdkcdn v1 SDK when hcloud is not installed.
  2. Three output modes: full-field table (default, every returned field
     including 域名/加速域名状态/CNAME/业务类型), --json (raw response array),
     and --names-only (compact accelerated-domain name list).
  3. Supports --domain-name / --domain-status / --business-type /
     --service-area / --enterprise-project-id filtering (all real server-side
     ListDomains query parameters), region override, and automatic
     page_number paging over the response `total` count.
  4. Explicit error hints for empty domain lists (「当前区域无 CDN 加速域名」),
     403 / insufficient IAM permission (「无权限访问内容分发网络（CDN）」),
     missing or invalid AK/SK credentials, and hcloud not installed.
  5. Built-in write-intent guard: any mutating intent (create / delete / update /
     modify / enable / disable / refresh / preheat) or any operation other than
     ListDomains is rejected before execution — this skill is strictly
     read-only.
  6. Triggers include: "list CDN domains", "cdn list", "加速域名列表",
     "查询 CDN", "查询加速域名", "CDN 域名列表", "CDN 域名盘点",
     "list cdn domains", "accelerated domain inventory", "华为云 CDN".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, filters,
     page_number paging, error scenarios, SDK fallback, and the write-intent
     guard.
tags: [huawei-cloud, cdn, network, readonly, koo-cli]
---

# Huawei Cloud CDN (Content Delivery Network) Accelerated Domain List

## Overview

Query the CDN accelerated-domain list of a tenant through KooCLI
`hcloud CDN ListDomains --cli-region=<region>` (official read-only GET
`/v1.0/cdn/domains`, verified
in the `huaweicloudsdkcdn` v1 client `_list_domains_http_info` metadata). The
skill is aimed at CDN inventory inspection, daily operations patrol, and as a
pre-query step for other CDN workflows that need a domain name or CNAME.

Architecture:

```text
agent → python3 scripts/list_cdn.py → hcloud CDN ListDomains --cli-region=<region>
      → Huawei Cloud CDN OpenAPI → parsed JSON → table / --json / --names-only

(hcloud binary missing) → fallback: huaweicloudsdkcdn v1 CdnClient.list_domains
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListDomains` (GET). A
  write-intent guard scans user arguments and validates the operation name;
  mutating intents (create / delete / update / modify / enable / disable /
  refresh / preheat ...) are rejected with an explicit message before any
  command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  KooCLI binary is absent, the script falls back to the official
  `huaweicloudsdkcdn` v1 SDK (`list_domains`). Credentials are always read by
  the CLI profile / SDK environment — never handled by the script.
- **Full-field table output** — the default table renders the union of all
  fields returned by ListDomains, with `tags` flattened for readability and the
  key columns (域名/加速域名状态/CNAME/业务类型) first.
- **Offline-testable** — every code path (paging, filters, error
  classification, guard, SDK fallback) is covered by unit tests that mock the
  hcloud subprocess.

Out of scope: every mutating CDN action (create / delete / enable / disable /
update a domain, origin or config changes, refresh / preheat tasks,
certificate management). Those require a dedicated write-capable skill and
explicit user confirmation (确认).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcdn` to enable the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band
   (run the KooCLI configure command in your terminal, or set credential
   environment variables).
   Never paste AK/SK into chat; the script never reads, echoes, or stores
   secrets itself — authentication is delegated entirely to the hcloud profile
   / SDK environment.
3. **IAM permission** — read-only `cdn:domain:list`; least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess).
5. **Outbound HTTPS** access to `cdn.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`); CDN accelerated domains
   are queried through the CDN endpoint, and the credential project is
   region-scoped.
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
python3 scripts/list_cdn.py --region cn-north-4

# Raw JSON of every returned field
python3 scripts/list_cdn.py --json

# Compact accelerated-domain name list only
python3 scripts/list_cdn.py --names-only

# Filter by accelerated-domain status (server-side query parameter)
python3 scripts/list_cdn.py --domain-status online

# Filter by accelerated domain name / business type
python3 scripts/list_cdn.py --domain-name www.example.com
python3 scripts/list_cdn.py --business-type web

# Combine filters
python3 scripts/list_cdn.py --region cn-north-4 --domain-status online --names-only
```

Equivalent direct KooCLI command (the script wraps exactly this call, with
page_number paging):

```bash
hcloud CDN ListDomains --cli-region=cn-north-4 --page_size=100 --page_number=1
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--json` | No | Output the raw domain array as JSON | — |
| `--names-only` | No | Output accelerated-domain names only | — |
| `--domain-name` | No | Filter by accelerated domain name — real server-side query parameter (fuzzy match) | `www.example.com` |
| `--domain-status` | No | Filter by accelerated-domain status — real server-side query parameter | `online` |
| `--business-type` | No | Filter by business type — real server-side query parameter | `web` |
| `--service-area` | No | Filter by service area — real server-side query parameter | `mainland_china` |
| `--enterprise-project-id` | No | Filter by enterprise project ID — real server-side query parameter | `0` |
| `--page-size` | No | Page size for ListDomains (default 100) | `100` |
| `--operation` | No | hcloud CDN operation name; only `ListDomains` is allowed | `ListDomains` |

Output-mode precedence: `--names-only` → `--json` → table (default).

## Write-Intent Guard

- The script scans all user arguments plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `modify`, `enable`, `disable`,
  `refresh`, `preheat`, and CDN operation names such as `CreateDomain`,
  `DeleteDomain`, `UpdateDomain`, `EnableDomain`, `DisableDomain`).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed.
- Only `hcloud CDN ListDomains --cli-region=<region>` (GET) — or the SDK
  `list_domains` call in the
  fallback path — is ever constructed by `build_command()`; there is no code
  path that can issue a mutating CDN API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `CDN`.
- **Operation name** — PascalCase: `ListDomains`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete CDN call).
- **Simple parameter** — `--key=value`, e.g. `--page_size=100`,
  `--page_number=1`, `--domain_name=www.example.com`, `--domain_status=online`,
  `--business_type=web`. All filters are real server-side ListDomains
  parameters (verified against the `huaweicloudsdkcdn` v1 `ListDomainsRequest`
  model).
- **Paging** — `--page_size` + `--page_number`; the loop advances `page_number`
  until the collected count reaches the response `total`.
- **REST path (official SDK `_http_info`)** —
  `GET /v1.0/cdn/domains` (`huaweicloudsdkcdn` v1
  `_list_domains_http_info`).

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty domain list | Exit 0, prints `当前区域（<x>）无 CDN 加速域名` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问内容分发网络（CDN），请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkcdn` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud CDN ListDomains --cli-region=<region> --help` |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Non-`online` domains | Reported with their state (`offline` / `configuring` ...), not treated as failure |
| `--domain-name` / `--domain-status` / `--business-type` filters | Forwarded as real server-side query parameters (verified API params) |
| Large domain count | Automatic `page_number` paging (`total` aware, max 100 pages) |
| Extra response fields | Table columns are built from the union of returned fields — new fields appear automatically |
| Field missing on a domain | Rendered as `-` in the table |
| Nested `tags` | Flattened into `key=value,...` for the table |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkcdn` list_domains, same output modes |
| User asks to create/delete/enable a domain | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / update / enable /
disable / normalized variants / operation whitelist), command construction
(filters forwarded server-side; page_number paging), JSON extraction, failure
classification (missing AK/SK, 403, generic, `[USE_ERROR]` with rc=0), total
paging (page_number / full page / empty), SDK fallback (success / unavailable /
pagination), rendering (table with 域名/状态/CNAME/业务类型 / names /
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