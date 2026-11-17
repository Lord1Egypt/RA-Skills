---
name: huawei-cloud-dns-list
description: |
  1. List Huawei Cloud DNS (云解析服务) zones and record sets in a tenant
     through KooCLI (hcloud DNS ListPublicZones / ListPrivateZones /
     ListRecordSets — read-only GET /v2/zones and /v2/recordsets), with an
     automatic fallback to the official `huaweicloudsdkdns` v2 SDK when hcloud
     is not installed.
  2. Three output modes: full-field table (default, every returned field
     including 域名/ID/类型/状态/记录集数/邮箱/TTL), --json (raw response
     array), and --names-only (compact domain-name list).
  3. Markdown export: --output / -o [FILE] writes the current table view to a
     UTF-8 Markdown file (zone view default dns_zones.md, --recordsets view
     default dns_recordsets.md), atomically (temp file + rename) and prints the
     absolute path; an empty result still writes a header-only file.
  4. Supports --type public|private, --recordsets, --id / --name /
     --record-type filtering (all real server-side ListZones / ListRecordSets
     query parameters), region override, and automatic marker paging.
  5. Explicit error hints for empty lists (「当前区域无 DNS 域名」),
     403 / insufficient IAM permission (「无权限访问云解析服务（DNS）」),
     API error bodies returned on stdout with exit code 0 (`DNS.1802` /
     `not authorized` / `no identity-based policy` envelopes are never
     reported as an empty list), missing or invalid AK/SK credentials,
     missing project_id on the SDK fallback, hcloud not installed, and
     Markdown write failure.
  6. Built-in write-intent guard: any mutating intent (create / delete / update /
     associate / transfer / enable / disable / import / export / batch) or any
     operation other than the three list operations is rejected before
     execution — this skill is strictly read-only. The --output value is caller
     data and is excluded from the guard scan.
  7. Triggers include: "list DNS zones", "DNS 域名列表", "查询 DNS", "云解析",
     "公网域名列表", "私网域名列表", "DNS 记录集", "dns zone inventory",
     "list public zones", "list record sets", "华为云 DNS", "导出 DNS 清单",
     "DNS Markdown 导出", "export DNS to markdown".
  8. Offline unit tests (mocked hcloud subprocess) cover output modes, filters,
     marker paging, error scenarios, SDK fallback, Markdown export (default file
     names / atomic write / escaping / empty result), and the write-intent guard.
tags: [huawei-cloud, dns, network, readonly, koo-cli]
---

# Huawei Cloud DNS (云解析服务) Zone / Record-Set List

## Overview

Query the DNS (云解析服务) zone and record-set inventory of a tenant through
KooCLI hcloud DNS ListPublicZones / ListPrivateZones / ListRecordSets
(official read-only GET `/v2/zones` and `/v2/recordsets`, verified in the
`huaweicloudsdkdns` v2 client `_list_public_zones_http_info` /
`_list_private_zones_http_info` / `_list_record_sets_http_info` metadata). The
skill is aimed at DNS inventory inspection, daily operations patrol, and as a
pre-query step for other skills that need a zone `id` or a domain name.

Architecture:

```text
agent → python3 scripts/list_dns.py → hcloud DNS ListPublicZones --cli-region=<region>
      → Huawei Cloud DNS OpenAPI (dns.<region>.myhuaweicloud.com) → parsed JSON → table / --json / --names-only
      → (--output) atomic UTF-8 Markdown file (dns_zones.md / dns_recordsets.md)

(hcloud binary missing) → fallback: huaweicloudsdkdns v2 DnsClient.list_public_zones / list_private_zones / list_record_sets
```

Key properties:

- **Read-only by design** — the only APIs ever invoked are the list operations
  (`ListPublicZones` / `ListPrivateZones` / `ListRecordSets`, all GET). A
  write-intent guard scans user arguments and validates the operation name;
  mutating intents (create / delete / update / associate / transfer / enable /
  disable / import / export / batch) are rejected with an explicit message
  before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  KooCLI binary is absent, the script falls back to the official
  `huaweicloudsdkdns` v2 SDK. Credentials are always read by the CLI profile /
  SDK environment — never handled by the script.
- **Full-field table output** — the default table renders the union of all
  fields returned by the list API (public/private zones carry
  `name` / `zone_type` / `status` / `record_num` / `email` / `ttl`; record sets
  carry `name` / `type` / `ttl` / `records` / `zone_name`).
- **Markdown export (additional, opt-in)** — `--output` / `-o [FILE]` renders
  the same columns as the default table into a UTF-8 Markdown table and writes
  it atomically (temp file + `os.replace`). The stdout modes are unchanged; the
  export is skipped for `--json` / `--names-only`. Default file names are
  `dns_zones.md` (zone view) and `dns_recordsets.md` (`--recordsets` view); an
  empty result still produces a header-only file.
- **Global resource note** — public zones are a global resource; call them in
  `cn-north-4` (default). Private zones and record sets are regional.
- **Offline-testable** — every code path (marker paging, filters, error
  classification, guard, SDK fallback) is covered by unit tests that mock the
  hcloud subprocess.

Out of scope: every mutating DNS action (create / update / delete a zone or
record set, transfer, enable/disable, batch import/export). Those require a
dedicated write-capable skill and explicit **用户确认** (user confirmation).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkdns` to enable the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band
   (run the KooCLI configure command in your terminal, or set credential
   environment variables).
   Never paste AK/SK into chat; the script never reads, echoes, or stores
   secrets itself — authentication is delegated entirely to the hcloud profile
   / SDK environment.
3. **project_id (SDK fallback only)** — the DNS REST paths are `/v2/zones` and
   `/v2/recordsets`; when falling back to the SDK, supply the project id via
   `--project-id` or the `HUAWEICLOUD_SDK_PROJECT_ID` / `HUAWEI_PROJECT_ID`
   environment variables. The KooCLI path resolves it from the profile
   automatically.
4. **IAM permission** — read-only `dns:zone:list` (and `dns:recordset:list` for
   `--recordsets`); least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
5. **Python 3.8+** (standard library only — argparse / json / subprocess).
6. **Outbound HTTPS** access to `dns.cn-north-4.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`; public zones are a
   global resource served from `cn-north-4`).
2. **Confirm KooCLI readiness** (optional, read-only) by listing the active
   credential profile.
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — table for humans, `--json` for downstream tooling,
   `--names-only` for a compact inventory; add `--output [FILE]` to also save
   the table view as a Markdown file for patrol records / delivery.
5. **Handle the empty / error cases** per the Edge Cases table below (the
   script prints an explicit hint for empty region, 403, and missing AK/SK).

## Core Commands

```bash
# Full-field table of public zones (default)
python3 scripts/list_dns.py --region cn-north-4

# Private zones
python3 scripts/list_dns.py --type private

# Record sets (public by default; combine with --type private for internal)
python3 scripts/list_dns.py --recordsets --record-type A

# Raw JSON of every returned field
python3 scripts/list_dns.py --json

# Compact domain-name list only
python3 scripts/list_dns.py --names-only

# Filter by exact zone id / domain name (server-side query parameters)
python3 scripts/list_dns.py --id zone-0001
python3 scripts/list_dns.py --name example.com

# Combine filters
python3 scripts/list_dns.py --type private --name internal.local --names-only

# Export the table view to Markdown (prints the absolute path)
python3 scripts/list_dns.py --output ./dns-zones.md

# -o without a value uses the view default: dns_zones.md / dns_recordsets.md
python3 scripts/list_dns.py -o
python3 scripts/list_dns.py --recordsets -o

# Export with filters (same result set as the terminal table)
python3 scripts/list_dns.py --type private --name internal.local -o priv.md
```

Equivalent direct KooCLI commands (the script wraps exactly these calls, with
marker paging):

```bash
hcloud DNS ListPublicZones --cli-region=cn-north-4 --limit=100
hcloud DNS ListPrivateZones --cli-region=cn-north-4 --type=private --limit=100
hcloud DNS ListRecordSets --cli-region=cn-north-4 --zone_type=public --limit=100
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--type` | No | Zone type: `public` (default) / `private` | `private` |
| `--recordsets` | No | Query record sets (`ListRecordSets`) instead of zones | — |
| `--json` | No | Output the raw instance array as JSON | — |
| `--names-only` | No | Output the domain-name list only | — |
| `--id` | No | Filter by exact zone ID (or record-set ID) — real server-side query parameter | `zone-0001` |
| `--name` | No | Filter by domain name — real server-side (fuzzy) query parameter | `example.com` |
| `--record-type` | No | Record-set type filter (only with `--recordsets`) | `A` |
| `--page-size` | No | Page size for the list API (default 100, range 0–500) | `100` |
| `--project-id` | No | Project ID (needed by the SDK fallback path) | `05f...` |
| `--operation` | No | hcloud DNS operation name; only `ListPublicZones` / `ListPrivateZones` / `ListRecordSets` are allowed | `ListPublicZones` |
| `--output` / `-o` | No | Export the current table view to a UTF-8 Markdown file (value optional); prints the absolute path | `./dns-zones.md` |

Output-mode precedence: `--json` → `--names-only` → table (default). The
Markdown export is an additional side effect of the table view only: it is
ignored when `--json` or `--names-only` is given, and never changes stdout.
`-o` without a value uses the view default (`dns_zones.md` for zones,
`dns_recordsets.md` for `--recordsets`); an explicit path always wins.

## Write-Intent Guard

- The script scans all user arguments plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `modify`, `associate`,
  `disassociate`, `attach`, `detach`, `bind`, `unbind`, `release`, `remove`,
  `destroy`, `change`, `transfer`, `restore`, `enable`, `disable`, `import`,
  `export`, and DNS operation names such as `CreatePublicZone`,
  `DeletePrivateZone`, `UpdateRecordSet`, `BatchCreateRecordSets`).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed.
- The `--output` / `-o` **value** is caller data, not an operation intent, so it
  is removed before the scan: `--output ./delete-report.md` is allowed while a
  real write intent (e.g. `--operation DeletePublicZone`) is still blocked.
- Only the three read-only list operations — or the SDK `list_public_zones` /
  `list_private_zones` / `list_record_sets` calls in the fallback path — are
  ever constructed by `build_command()`; there is no code path that can issue a
  mutating DNS API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `DNS`.
- **Operation name** — PascalCase: `ListPublicZones`, `ListPrivateZones`,
  `ListRecordSets`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete DNS call).
- **Simple parameter** — `--key=value`, e.g. `--limit=100`, `--marker=<token>`,
  `--id=zone-0001`, `--name=example.com`, `--zone_type=public`, `--type=A`.
  `--id` / `--name` are real server-side parameters for `ListPublicZones` /
  `ListPrivateZones`; `--zone_type` / `--type` are real server-side parameters
  for `ListRecordSets` (verified against the `huaweicloudsdkdns` v2 request
  models).
- **Required `--type=private` on `ListPrivateZones`** — `hcloud DNS
  ListPrivateZones --help` marks `--type` as **required** (range: `private`),
  so the script always appends `--type=private` for the private-zone
  operation. `ListPublicZones` has no such required parameter and keeps the
  service default (`public`).
- **Paging** — `--limit` + `--marker`; the marker is the **id of the last
  resource of the previous page** (DNS responses report `metadata.total_count`
  but no next_marker). `limit` and `marker` must be used together.
- **REST paths (official SDK `_http_info`)** —
  `GET /v2/zones` (`ListPublicZones` / `ListPrivateZones`) and
  `GET /v2/recordsets` (`ListRecordSets`); the project_id is resolved by KooCLI
  from the credential profile.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty list | Exit 0, prints `当前区域（<x>）无 DNS 域名 / 记录集` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问云解析服务（DNS），请检查 IAM 权限` hint |
| API error body on stdout with exit code 0 (`errCode` / `externalMessage`, `error_code` / `error_msg`, `code` / `message`, nested `error`; e.g. `DNS.1802` / `not authorized` / `no identity-based policy`) | Detected as an error envelope and surfaced through failure classification — exit 1 with the auth hint, never an empty list and never a header-only Markdown file |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| Missing project_id (SDK fallback) | Exit 1, hint to pass `--project-id` or set the project-id env var |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkdns` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit 参数错误 hint pointing to the DNS ListPublicZones `--help` output |
| Write intent detected | Exit 1, `GuardError` message, no command executed |
| Markdown write failure (missing/unwritable directory, I/O error) | Exit 1, `Markdown 文件写出失败（...）`, no partial / temporary file left behind |

Exit codes: `0` success / empty region (a header-only Markdown file is still
written when `--output` is given); `1` config, auth, guard, API, or Markdown
write error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Non-`ACTIVE` zones / record sets | Reported with their state, not treated as failure |
| `--id` / `--name` / `--record-type` filters | Forwarded as real server-side query parameters (verified API params) |
| Large zone / record-set count | Automatic `marker` paging (last-resource-id aware, `total_count` aware, max 100 pages) |
| Extra response fields | Table columns are built from the union of returned fields — new fields appear automatically |
| Field missing on an item | Rendered as `-` in the table and in the Markdown export |
| Nested `tags` / `links` | Rendered as compact JSON in the corresponding cell |
| `--output` without a value | Default file name by view: `dns_zones.md` (zones) / `dns_recordsets.md` (`--recordsets`) in the current directory |
| Empty result with `--output` | Exit 0, header-only valid Markdown file written, empty-region hint still printed |
| `--output` path containing `delete` / `create` words | Allowed — the path is caller data and excluded from the write-intent scan |
| Markdown cell containing a pipe character or line breaks | Pipe and newline escaped so the table stays valid |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars); trailing diagnostics after a JSON body are tolerated via `raw_decode` |
| API error envelope with exit code 0 | Classified as `AuthError` / `ApiError` (never treated as an empty result); `--output` does not create a header-only file |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkdns` v2, same output modes |
| Public zones requested in a non-`cn-north-4` region | Works via the global endpoint, but `cn-north-4` is the documented region |
| User asks to create/delete/transfer a zone | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
cd skills/network/dns/huawei-cloud-dns-list
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / update /
associate / transfer / enable / disable / normalized variants / operation
whitelist), operation resolution (`--type` / `--recordsets`), command
construction (filters forwarded server-side; marker never sent on the first
page; required `--type=private` forced on `ListPrivateZones` and never added to
`ListPublicZones`), JSON extraction (trailing diagnostics tolerated via `raw_decode`),
failure classification (missing AK/SK, 403, `DNS.1802` / `not authorized` /
`no identity-based policy`, generic, `[USE_ERROR]` with rc=0), API error
envelopes returned with rc=0 (never an empty list; `--output` stays empty),
marker paging (last-id / `total_count` / empty),
SDK fallback (public zones / private zones / record sets / missing credentials /
missing project id / unavailable; request construction matches the real
`huaweicloudsdkdns` v2 request signatures), rendering (table with
zone/record-set fields / names / fallbacks), Markdown export (shared
`_table_columns` parity with the table, default file names per view,
header-only empty result, pipe / newline escaping, atomic write, missing /
unwritable directory, guard exemption for the output value), private-zone
regressions (`--type private` and `--type private -o` both send
`--type=private`), and all main() output modes including empty, filter, and
error paths.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |