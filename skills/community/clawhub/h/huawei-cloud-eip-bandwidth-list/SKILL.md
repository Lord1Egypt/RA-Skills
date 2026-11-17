---
name: huawei-cloud-eip-bandwidth-list
description: |
  1. Query Huawei Cloud EIP bandwidth resources in a tenant region through
     KooCLI `hcloud EIP ListBandwidths` (read-only GET
     /v3/{project_id}/eip/bandwidths), with an automatic fallback to the
     official `huaweicloudsdkeip` v3 SDK (`list_bandwidths`) when hcloud is not
     installed.
  2. Inspect a single bandwidth by `--bandwidth-id`, switching to
     `hcloud EIP ShowBandwidth` (read-only GET
     /v3/{project_id}/eip/bandwidths/{bandwidth_id}) and additionally listing
     each public IP (`publicip_address` / `publicip_type` / `ip_version`) and
     the `bandwidth_rules` / `rule_quota` fields.
  3. List output carries 带宽名称 / 带宽 ID / 大小(Mbit/s) / share_type
     (PER 独占, WHOLE 共享) / charge_mode (bandwidth 按带宽, traffic 按流量) /
     关联公网 IP 数 / 状态 / 企业项目 ID / 创建时间.
  4. Server-side filters `--share-type {PER,WHOLE}` and
     `--enterprise-project-id`; `--limit` defaults to 10 (the Huawei Cloud
     list lower bound) and marker paging automatically aggregates all pages.
  5. Three output modes: default fixed-header terminal table, `--json` (raw
     list array / detail object), and `--format md -o <file>` (archivable
     Markdown report; an empty list still writes the header plus 「无数据」).
  6. Explicit error hints for empty results (distinguishing 「整体无带宽」 from
     「按 share_type 过滤后为空」), 403 / insufficient IAM permission
     (`eip:bandwidths:list` / `eip:bandwidths:get`), missing AK/SK, hcloud not
     installed, missing project_id on the SDK fallback, and a 404 when the
     requested bandwidth does not exist.
  7. Built-in write guard: only `ListBandwidths` / `ShowBandwidth` (both GET)
     are allowed; any mutating intent (create / update / delete a bandwidth,
     change charge mode, bind / unbind a public IP) is rejected before
     execution. This skill is strictly read-only.
  8. Triggers include: "EIP 带宽列表", "带宽列表", "共享带宽盘点", "独占带宽查询",
     "EIP 带宽巡检", "查询带宽", "带宽明细", "EIP bandwidth list",
     "list bandwidths", "show bandwidth", "shared bandwidth inventory",
     "带宽计费模式核查", "导出带宽 Markdown".
tags: [huawei-cloud, eip, bandwidth, readonly, koo-cli]
---

# Huawei Cloud EIP Bandwidth List

## Overview

Inventory the Elastic IP **bandwidth resources** of a tenant region (shared /
dedicated bandwidths, distinguished by `share_type`) through the read-only
KooCLI operations:

```text
agent → python3 scripts/list_bandwidths.py
      → hcloud EIP ListBandwidths  --cli-region=<region> [--share_type=] [--enterprise_project_id=] [--limit=] [--marker=]
      → hcloud EIP ShowBandwidth   --cli-region=<region> --bandwidth_id=<id>
      → Huawei Cloud EIP OpenAPI (vpc.<region>.myhuaweicloud.com) → parsed JSON
      → table / --json / --format md -o <file>

(hcloud binary missing) → fallback: huaweicloudsdkeip v3 EipClient.list_bandwidths / show_bandwidth
```

Key properties:

- **Read-only by design** — only `ListBandwidths` and `ShowBandwidth` (both
  GET) are ever constructed. A write-intent guard scans user arguments and the
  operation name; create / update / delete / change charge mode / bind / unbind
  intents are rejected before any command runs.
- **Bandwidth-resource dimension** — one row per bandwidth, with the number of
  attached public IPs derived from `publicip_info`; this is different from a
  public-IP-dimension list.
- **Filter + paging** — `--share-type` and `--enterprise-project-id` are real
  server-side query parameters; `--limit` defaults to 10 and marker paging
  collects every page automatically.
- **Three output modes** — fixed-header table (default), raw `--json`, and an
  archivable Markdown report via `--format md -o <path>`.
- **Offline-testable** — every code path (guard, filters, marker paging,
  rendering, Markdown export, error classification, SDK fallback) is covered by
  unit tests that mock the hcloud subprocess.

Out of scope: every mutating bandwidth action (create / update / delete a
bandwidth, change the charge mode, bind / unbind a public IP) and the
public-IP-dimension inventory handled elsewhere in the repository.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkeip` for the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band (KooCLI
   configure in your terminal, or credential environment variables). Never
   paste AK/SK into chat; the script never reads, echoes, or stores secrets
   itself.
3. **project_id (SDK fallback only)** — the bandwidth REST paths are
   `/v3/{project_id}/eip/bandwidths[/*]`; the SDK fallback needs the project id
   via `--project-id` or `HUAWEICLOUD_SDK_PROJECT_ID` / `HUAWEI_PROJECT_ID`.
   The KooCLI path resolves it from the profile automatically.
4. **IAM permission** — `eip:bandwidths:list` and `eip:bandwidths:get`; least
   privilege policy in [references/iam-policies.md](references/iam-policies.md).
5. **Python 3.8+** (standard library only for the CLI path).
6. **Outbound HTTPS** access to `vpc.<region>.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`).
2. **Optionally confirm KooCLI readiness** (read-only) by listing the active
   credential profile.
3. **Run the list script** with the desired filters and output mode.
4. **Optional detail** — pass `--bandwidth-id <id>` to query one bandwidth and
   see its public IPs and bandwidth rules.
5. **Read the result** — fixed table for humans, `--json` for downstream
   tooling, `--format md -o <path.md>` for an archivable report.
6. **Handle empty / error cases** per the tables below (empty region,
   filtered-empty, 403, missing AK/SK, hcloud missing). Empty queries still
   produce a valid Markdown file marked 「无数据」 with exit 0.

## Core Commands

```bash
# List (default table)
python3 scripts/list_bandwidths.py --region cn-north-4

# Raw JSON array of bandwidth records
python3 scripts/list_bandwidths.py --region cn-north-4 --json

# Filter by share type (server-side): PER 独占 / WHOLE 共享
python3 scripts/list_bandwidths.py --share-type WHOLE

# Filter by enterprise project (server-side)
python3 scripts/list_bandwidths.py --enterprise-project-id 0

# Combine filters and change the page size (default 10)
python3 scripts/list_bandwidths.py --share-type PER --enterprise-project-id 0 --limit 50

# Single-bandwidth detail (switches to ShowBandwidth)
# Use an ID returned by the list command above; IDs are region/account specific.
python3 scripts/list_bandwidths.py --bandwidth-id <bandwidth-id>

# Detail as raw JSON
python3 scripts/list_bandwidths.py --bandwidth-id <bandwidth-id> --json

# Markdown export (default filename eip_bandwidth_list_<region>_<timestamp>.md)
python3 scripts/list_bandwidths.py --format md -o /data/reports/bandwidths.md

# Markdown export of a filtered empty result (header + 「无数据」)
python3 scripts/list_bandwidths.py --share-type WHOLE --format md -o bandwidth_whole.md

# Markdown detail export
python3 scripts/list_bandwidths.py --bandwidth-id <bandwidth-id> --format md -o bandwidth_detail.md
```

Equivalent direct KooCLI commands (the script wraps exactly these, adding
`--marker` paging to the list call):

```bash
hcloud EIP ListBandwidths --cli-region=cn-north-4 --limit=10
hcloud EIP ListBandwidths --cli-region=cn-north-4 --limit=10 --share_type=WHOLE --enterprise_project_id=0
hcloud EIP ShowBandwidth --cli-region=cn-north-4 --bandwidth_id=<bandwidth-id>
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| --------- | -------- | ----------- | ------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--bandwidth-id` | No | Query one bandwidth (switches to `ShowBandwidth`) | `<bandwidth-id>` from list output |
| `--share-type` | No | Server-side filter: `PER` (dedicated) / `WHOLE` (shared) | `WHOLE` |
| `--enterprise-project-id` | No | Server-side enterprise-project filter (`0` = default, `all_granted_eps` = all) | `0` |
| `--limit` | No | List page size (default 10) | `50` |
| `--json` | No | Output the raw list array / detail object | — |
| `--format` | No | Output form: `table` (default) / `json` / `md` | `md` |
| `-o` / `--output` | No | Markdown output path; implies `--format md`; parent dirs created | `/data/bw.md` |
| `--project-id` | No | Project ID (needed by the SDK fallback) | `05f...` |
| `--operation` | No | hcloud EIP operation name; only `ListBandwidths` / `ShowBandwidth` allowed | `ListBandwidths` |

Output-mode precedence: `-o/--output` → `--format md` → `--json` → table.
`--bandwidth-id` selects the detail path regardless of the output mode.

## Output Formats

- **Table (default)** — fixed headers: 带宽名称 / 带宽 ID / 大小(Mbit/s) /
  共享类型 / 计费方式 / 关联公网 IP 数 / 状态 / 企业项目 ID / 创建时间.
  Missing values render as `-`.
- **Detail** — the summary row above, then a public-IP table
  (公网 IP / 公网 IP ID / 类型 / IP 版本) and the bandwidth rules
  (`rule_quota`, `enable_bandwidth_rules`, `bandwidth_rules`). An empty public
  IP list renders the header plus 「无数据」.
- **`--json`** — the raw `bandwidths` array (list) or the raw `bandwidth`
  object (detail), re-readable with `json.load`.
- **`--format md -o <file>`** — title 「华为云 EIP 带宽列表」 (or
  「华为云 EIP 带宽明细」), region / generated time / record count, active
  filters, and the fixed-header table. An empty list still writes the header
  and a 「无数据」 note, exit 0. Files are staged through a temp file and
  atomically renamed; parent directories are created.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `EIP`.
- **Operation names** — PascalCase: `ListBandwidths` / `ShowBandwidth` (both
  `Method: GET`).
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete EIP call).
- **Scalar parameters** — `--key=value`:
  `--limit`, `--marker`, `--share_type`, `--enterprise_project_id`,
  `--bandwidth_id` (verified live against the KooCLI parameter list).
- **Paging** — `--limit` + `--marker`; the marker of the next page is the last
  bandwidth `id` of the current full page (the observed response has no
  `page_info`, so page completion is detected by `len(page) == limit`).
- **REST paths** — `GET /v3/{project_id}/eip/bandwidths` and
  `GET /v3/{project_id}/eip/bandwidths/{bandwidth_id}`; project_id is resolved
  by KooCLI from the credential profile.

## Error Handling

| Scenario | Behavior |
| -------- | -------- |
| Empty list (no bandwidth at all) | Exit 0, `当前 region（<x>）无带宽（Bandwidth）数据。` |
| Empty list after `--share-type=WHOLE` | Exit 0, `当前 region（<x>）无 share_type=WHOLE 的带宽（共享带宽）数据。` |
| Empty list after `--share-type=PER` | Exit 0, `当前 region（<x>）无 share_type=PER 的带宽（独占带宽）数据。` |
| Empty list after enterprise-project filter | Exit 0, the message also names the enterprise project |
| 403 / insufficient IAM permission | Exit 1, hint names `eip:bandwidths:list` (list) or `eip:bandwidths:get` (detail) |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| Missing project_id (SDK fallback) | Exit 1, hint to pass `--project-id` or set the project-id env var |
| hcloud not installed | Exit 1 after the SDK fallback is also unavailable, hint to install KooCLI or the SDK |
| Bandwidth not found (`ShowBandwidth` 404 / `VPC.0305` / `NoEipBandWidthExist`) | Exit 1, explicit hint that the bandwidth does not exist and to run `ListBandwidths` first to verify `--bandwidth-id` (the sample IDs in docs are illustrative only) |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud EIP <operation> --help` |
| API error body with exit code 0 (`{"code": "VPC.0305", "message": ...}`) | The parsed body is classified before rendering: not-found → bandwidth-does-not-exist hint (`ListBandwidths` first), auth codes → IAM hint, other codes → explicit API-error hint; exit 1 |
| Write intent detected | Exit 1, `GuardError` message, no command executed |
| Markdown path unusable / write failed | Exit 1, `ExportError` with the path and OS reason; no partial file left behind |

Exit codes: `0` success / empty result (including an empty Markdown export);
`1` config, auth, guard, API, or local export error.

## Edge Cases

| Scenario | Handling |
| -------- | -------- |
| Non-`NORMAL` bandwidths | Reported with their `status`, not treated as a failure |
| `--share-type` / `--enterprise-project-id` | Forwarded as real server-side query parameters |
| Large bandwidth count | Automatic marker paging (full page → next; explicit `next_marker` honored; max 100 pages) |
| Exactly one full page then an empty page | Second call returns 0 records and stops, no duplicate rows |
| Field missing on a bandwidth | Rendered as `-` in table and Markdown |
| `publicip_info` empty | 关联公网 IP 数 = 0; detail renders the public-IP header plus 「无数据」 |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkeip` list/show, same output modes |
| User asks to create/delete/modify a bandwidth or change its charge mode | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit confirmation is required |
| Markdown output path contains write-looking words | The local output path is not scanned by the write guard (only cloud-operation intents are) |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 scripts/run_tests.py
```

Coverage (78 tests): write-intent guard (read passes / create / delete / update /
change / bind / unbind / release / normalized variants / operation allowlist),
command construction (filters and marker), JSON extraction, failure
classification (missing AK-SK, 403 list vs detail, 404 detail, `[USE_ERROR]`
with rc=0), API error bodies returned with exit code 0 (`VPC.0305` not-found,
`APIGW.0301` auth, generic codes, success payload not misclassified), marker
paging (full page / partial page / empty page / explicit
`next_marker`), SDK fallback (hcloud missing → SDK, SDK unavailable, request
construction and pagination with a mocked SDK module), rendering (list table /
detail text / Markdown list / Markdown detail / `-` fallback / empty
「无数据」), Markdown export (parent creation / atomic write / detail), and all
`main()` output and error paths.

## Reference Documents

| Document | Content |
| -------- | ------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | Live parameter verification and test coverage |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria mapping |