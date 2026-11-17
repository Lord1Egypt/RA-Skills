---
name: huawei-cloud-eip-list
description: |
  1. List Huawei Cloud Elastic IP (EIP) instances in a tenant region through
     KooCLI (hcloud EIP ListPublicips — read-only GET
     /v3/{project_id}/eip/publicips), with an automatic fallback to the
     official huaweicloudsdkeip v3 SDK when hcloud is not installed.
  2. Four output modes: full-field table (default, every returned field
     including 名称/别名/ID/公网IP/带宽/状态/绑定资源), --json (raw response
     array), --names-only (compact EIP alias/public-IP list), and Markdown
     export (--markdown or -o/--output <path.md>).
  3. Markdown export writes an archivable `.md` report in one query: title
     「华为云 EIP 列表」, query region / generated time / record count, and a
     full fixed-header table (公网IP、EIP ID、别名、状态、类型、绑定实例类型/ID、
     带宽名称/大小、计费方式、企业项目 ID、创建时间); missing fields render as `-`.
     Empty results still produce a `.md` marked 「无数据」 and exit 0.
  4. Supports --id / --status / --public-ip filtering (all real server-side
     ListPublicips query parameters), region override, and automatic marker
     paging.
  5. Explicit error hints for empty EIP lists (「当前区域无弹性公网IP（EIP）」),
     403 / insufficient IAM permission (「无权限访问弹性公网IP（EIP）」),
     missing or invalid AK/SK credentials, missing project_id on the SDK
     fallback, and hcloud not installed.
  6. Built-in write-intent guard: any mutating intent (create / delete / update /
     associate / disassociate / attach / detach / release / change) or any
     operation other than ListPublicips is rejected before execution — this
     skill is strictly read-only.
  7. Triggers include: "list EIPs", "eip list", "弹性公网IP列表", "查询 EIP",
     "查询弹性公网IP", "EIP 实例列表", "elastic ip inventory",
     "list public ips", "华为云 EIP", "公网IP列表", "导出 EIP Markdown",
     "EIP 列表导出 md".
  8. Offline unit tests (mocked hcloud subprocess) cover output modes, filters,
     marker paging, error scenarios, SDK fallback, Markdown export, and the
     write-intent guard.
tags: [huawei-cloud, eip, network, readonly, koo-cli]
---

# Huawei Cloud Elastic IP (EIP) Instance List

## Overview

Query the Elastic IP (EIP) instance list of a tenant through KooCLI
`hcloud EIP ListPublicips` (official read-only GET
`/v3/{project_id}/eip/publicips`, verified in the `huaweicloudsdkeip` v3
client `_list_publicips_http_info` metadata). The skill is aimed at EIP
inventory inspection, daily operations patrol, and as a pre-query step for
other skills that need an EIP `id` or a bound resource.

Architecture:

```text
agent → python3 scripts/list_eip.py → hcloud EIP ListPublicips --cli-region=<region>
      → Huawei Cloud EIP OpenAPI (vpc.<region>.myhuaweicloud.com) → parsed JSON
      → table / --json / --names-only / Markdown .md export

(hcloud binary missing) → fallback: huaweicloudsdkeip v3 EipClient.list_publicips
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListPublicips`
  (GET). A write-intent guard scans user arguments and validates the operation
  name; mutating intents (create / delete / update / associate / disassociate /
  attach / detach / release / change) are rejected with an explicit message
  before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  KooCLI binary is absent, the script falls back to the official
  `huaweicloudsdkeip` v3 SDK (`list_publicips`). Credentials are always read
  by the CLI profile / SDK environment — never handled by the script.
- **Full-field table output** — the default table renders the union of all
  fields returned by ListPublicips, with the nested `bandwidth` / `vnic`
  objects expanded into flat columns.
- **Archivable Markdown export** — `--markdown` / `-o <path>` renders the same
  query into a self-contained `.md` report (title + region/time/count + fixed
  header table), written atomically to the requested path. The default behavior
  without an export flag is unchanged.
- **Offline-testable** — every code path (marker paging, filters, error
  classification, guard, SDK fallback) is covered by unit tests that mock the
  hcloud subprocess.

Out of scope: every mutating EIP action (create / update / delete an EIP,
associate / disassociate an EIP, bind / unbind a bandwidth, change bandwidth).
Those require a dedicated write-capable skill and explicit user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkeip` to enable the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band
   (run the KooCLI configure command in your terminal, or set credential
   environment variables).
   Never paste AK/SK into chat; the script never reads, echoes, or stores
   secrets itself — authentication is delegated entirely to the hcloud profile
   / SDK environment.
3. **project_id (SDK fallback only)** — the EIP REST path is
   `/v3/{project_id}/eip/publicips`; when falling back to the SDK, supply the
   project id via `--project-id` or the `HUAWEICLOUD_SDK_PROJECT_ID` /
   `HUAWEI_PROJECT_ID` environment variables. The KooCLI path resolves it from
   the profile automatically.
4. **IAM permission** — read-only `vpc:publicIps:list`; least-privilege
   policy in [references/iam-policies.md](references/iam-policies.md).
5. **Python 3.8+** (standard library only — argparse / json / subprocess).
6. **Outbound HTTPS** access to `vpc.cn-north-4.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`).
2. **Confirm KooCLI readiness** (optional, read-only) by listing the active
   credential profile.
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — table for humans, `--json` for downstream tooling,
   `--names-only` for a compact inventory, `--markdown` / `-o <path.md>` for an
   archivable report file.
5. **Handle the empty / error cases** per the Edge Cases table below (the
   script prints an explicit hint for empty region, 403, and missing AK/SK).
   Empty queries still produce a Markdown file marked 「无数据」 with exit 0.

## Core Commands

```bash
# Full-field table (default)
python3 scripts/list_eip.py --region cn-north-4

# Raw JSON of every returned field
python3 scripts/list_eip.py --json

# Compact EIP alias / public-IP list only
python3 scripts/list_eip.py --names-only

# Filter by EIP status (server-side query parameter)
python3 scripts/list_eip.py --status ACTIVE

# Filter by exact EIP id / public IP
python3 scripts/list_eip.py --id eip-0001
python3 scripts/list_eip.py --public-ip 1.2.3.4

# Combine filters
python3 scripts/list_eip.py --region cn-north-4 --status ACTIVE --names-only

# Export an archivable Markdown report (default filename eip_list_<region>_<timestamp>.md)
python3 scripts/list_eip.py --region cn-north-4 --markdown

# Export to an explicit path (implies Markdown mode; parent dirs are created)
python3 scripts/list_eip.py --region cn-north-4 -o /data/reports/eip_list.md

# Export + filters (filters are recorded in the report)
python3 scripts/list_eip.py --status ACTIVE --markdown -o eip_active.md
```

Equivalent direct KooCLI command (the script wraps exactly this call, with
marker paging):

```bash
hcloud EIP ListPublicips --cli-region=cn-north-4 --limit=100
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--json` | No | Output the raw instance array as JSON | — |
| `--names-only` | No | Output EIP alias / public-IP list only | — |
| `--markdown` | No | Export a Markdown `.md` report (default filename `eip_list_<region>_<timestamp>.md` in the current directory) | — |
| `-o` / `--output` | No | Explicit Markdown output path; implies Markdown mode; parent directories are created automatically | `/data/reports/eip_list.md` |
| `--id` | No | Filter by exact EIP ID — real server-side ListPublicips query parameter | `eip-0001` |
| `--status` | No | Filter by EIP state — real server-side query parameter (`ACTIVE`/`DOWN`/`ERROR`/`FREEZED`) | `ACTIVE` |
| `--public-ip` | No | Filter by public IP address — real server-side query parameter | `1.2.3.4` |
| `--page-size` | No | Page size for ListPublicips (default 100, range 0–2000) | `100` |
| `--project-id` | No | Project ID (needed by the SDK fallback path for `/v3/{project_id}/...`) | `05f...` |
| `--operation` | No | hcloud EIP operation name; only `ListPublicips` is allowed | `ListPublicips` |

Output-mode precedence: Markdown export (`-o` / `--output` or `--markdown`) →
`--names-only` → `--json` → table (default). Supplying an export flag overrides
`--json` / `--names-only`; without one, behavior is unchanged.

## Markdown Export

`--markdown` / `-o <path>` renders exactly one ListPublicips query into a
self-contained report file (no extra API calls):

```text
# 华为云 EIP 列表

> 查询区域：cn-north-4 | 生成时间：2026-11-10T10:00:00Z | 记录数：2
> 过滤条件：status=ACTIVE            # only when a filter is active

| 公网IP | EIP ID | 别名 | 状态 | 类型 | 绑定实例类型 | 绑定实例 ID | 带宽名称 | 带宽大小 | 计费方式 | 企业项目 ID | 创建时间 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.2.3.4 | eip-0001 | eip-demo-01 | ACTIVE | EIP | PORT | port-0001 | bw-demo | 5 | traffic | 0 | 2024-01-01T00:00:00 |
```

- **Fixed full header** — all twelve columns are always present, even when a
  field is absent on an EIP; missing values render as `-`.
- **Default path** — `<cwd>/eip_list_<region>_<timestamp>.md`; `-o/--output`
  takes an absolute or relative path and implies Markdown mode. Missing parent
  directories are created.
- **Atomic write** — content is written to a temp file in the destination
  directory and atomically renamed, so an interrupted run never leaves a
  partial/corrupt `.md`.
- **Empty result** — a valid document is still produced, with the table header
  and an explicit 「无数据」 note; exit code stays `0`.
- **stdout** — prints the absolute path of the written file and the record
  count.

## Write-Intent Guard

- The script scans all user arguments plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `modify`, `associate`,
  `disassociate`, `attach`, `detach`, `bind`, `unbind`, `release`, `change`,
  `restart`, and EIP operation names such as `CreatePublicip`,
  `DeletePublicip`, `UpdatePublicip`, `AssociatePublicips`,
  `DisassociatePublicips`).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed.
- Only `hcloud EIP ListPublicips` (GET) — or the SDK `list_publicips` call in
  the fallback path — is ever constructed by `build_command()`; there is no
  code path that can issue a mutating EIP API call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `EIP`.
- **Operation name** — PascalCase: `ListPublicips`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete EIP call).
- **Simple parameter** — `--key=value`, e.g. `--limit=100`, `--marker=<token>`.
- **Array parameter** — `--key.1=value`, e.g. `--id.1=eip-0001`,
  `--status.1=ACTIVE`, `--public_ip_address.1=1.2.3.4`. All three filters are
  `array<string>` server-side ListPublicips parameters (verified against the
  KooCLI `ListPublicips --help` param list and the `huaweicloudsdkeip` v3
  `ListPublicipsRequest` model); KooCLI 7.x rejects the scalar form with
  `[USE_ERROR]Invalid parameter`.
- **Paging** — `--limit` + `--marker`; the marker is the `next_marker` returned
  in the response `page_info`. `limit` and `marker` must be used together.
- **REST path (official SDK `_http_info`)** —
  `GET /v3/{project_id}/eip/publicips` (`huaweicloudsdkeip` v3
  `_list_publicips_http_info`); the project_id is resolved by KooCLI from the
  credential profile.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty EIP list | Exit 0, prints `当前区域（<x>）无弹性公网IP（EIP）` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问弹性公网IP（EIP），请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| Missing project_id (SDK fallback) | Exit 1, hint to pass `--project-id` or set the project-id env var |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkeip` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud EIP ListPublicips --help` |
| Write intent detected | Exit 1, `GuardError` message, no command executed |
| Markdown export path unusable / write failed | Exit 1, `ExportError` message with the path and OS reason; no partial file left behind |

Exit codes: `0` success / empty region (including an empty Markdown export);
`1` config, auth, guard, API, or local export error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Non-`ACTIVE` EIPs | Reported with their state, not treated as failure |
| `--id` / `--status` / `--public-ip` filters | Forwarded as real server-side query parameters (verified API params) |
| Large EIP count | Automatic `marker` paging (`next_marker` aware, max 100 pages) |
| Extra response fields | Table columns are built from the union of returned fields — new fields appear automatically |
| Field missing on an EIP | Rendered as `-` in the table |
| Nested `bandwidth` / `vnic` | Expanded into flat `bandwidth_*` / `vnic_*` columns for the table |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkeip` list_publicips, same output modes |
| User asks to create/delete/associate an EIP | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |
| Empty Markdown export | Still writes a valid `.md` with header + 「无数据」 note, exit 0 |
| `-o` path with missing parent dirs | Created automatically (`os.makedirs`) |
| Our own report path contains write-looking words | The local output path is not scanned by the write-intent guard (only cloud-operation intents are) |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / update /
associate / release / change / normalized variants / operation whitelist),
command construction (filters forwarded server-side; marker never sent on the
first page), JSON extraction, failure classification (missing AK/SK, 403,
generic, `[USE_ERROR]` with rc=0), marker paging (next_marker / full page /
empty), SDK fallback (success, missing credentials, missing project id, and
unavailable; request construction matches the real `ListPublicipsRequest`
signature), rendering (table with bandwidth/association/vnic fields / names /
fallbacks), all main() output modes including empty, filter, and error paths,
and Markdown export (full header / `-` fallback / default filename / explicit
path / parent-dir creation / atomic temp cleanup / empty-result 「无数据」 /
export precedence over `--json` and `--names-only`, exit 0).

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |