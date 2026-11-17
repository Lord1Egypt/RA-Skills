---
name: huawei-cloud-cse-engine-list
description: |
  1. Read-only inventory of Huawei Cloud CSE microservice engines in a tenant
     region through KooCLI: `hcloud CSE ListEngines`
     (GET /v2/{project_id}/enginemgr/engines). Returns name / ID / type /
     version / status / flavor / instance counts / creation time / region.
  2. Automatic fallback to the official Python SDK `huaweicloudsdkcse`
     (`CseClient.list_engines`, the v1 SDK module that wraps the same v2 REST
     API) when the hcloud binary is not installed.
  3. Filtering: `--type` server-side (ALL / CSE / Nacos / MicroGateway),
     `--name` client-side exact match, `--fuzzy` client-side substring match,
     `--region` override (default cn-north-4), optional `--project-id`.
  4. Three output modes: concise inventory (default), `--table` full-field
     table, and `--json` normalized items.
  5. `total`-driven paging: every page is fetched until the reported total is
     reached (with a full-page fallback when `total` is absent).
  6. Empty list prints 「未找到微服务引擎」and exits 0.
  7. Explicit error hints for 403 / insufficient IAM permission
     (`cse:engine:list`), missing or invalid AK/SK, KooCLI `[USE_ERROR]`
     parameter errors, and network failures — never a traceback.
  8. Built-in write-intent guard: any mutating intent (create / delete /
     update / upgrade / modify / remove / start / stop / resize ...) is
     rejected before execution — strictly read-only.
  9. Offline unit tests (mocked hcloud + fake SDK) cover filtering, paging,
     output modes, error classification, SDK fallback and the guard.
  10. Triggers include: "CSE 微服务引擎列表", "查询CSE引擎", "微服务引擎盘点",
      "CSE引擎版本核查", "Nacos引擎列表", "网关引擎列表", "ListEngines",
      "CSE engine inventory", "list CSE engines", "华为云CSE引擎".
tags: [huawei-cloud, cse, devtools, readonly, koo-cli]
---

# Huawei Cloud CSE Microservice Engine List

## Overview

Query the read-only list of Huawei Cloud CSE microservice engines in a tenant
region through KooCLI, and fall back to the official SDK when hcloud is absent.

| Item | Value |
| ---- | ----- |
| KooCLI service / operation | `CSE` / `ListEngines` |
| REST path | `GET /v2/{project_id}/enginemgr/engines` |
| Method | GET (read-only) |
| Scope | region |
| SDK fallback | `huaweicloudsdkcse.v1` → `CseClient.list_engines` |

Service code, operation name, parameters and REST path are verified against the
live KooCLI metadata (`hcloud CSE ListEngines --help`, KooCLI 7.3.12) and the
official SDK `_list_engines_http_info` resource path — see
[references/verification-method.md](references/verification-method.md).

Architecture:

```text
agent → python3 scripts/list_cse_engines.py --region <region> [--type ...] [--name ...]
      → hcloud CSE ListEngines → CSE OpenAPI (regional endpoint)
      → parsed JSON → concise / --table / --json

(hcloud binary missing) → fallback: huaweicloudsdkcse CseClient.list_engines
```

Typical uses:

- **Engine inventory** — how many CSE / Nacos / MicroGateway engines exist in a
  region, their IDs, flavors and instance capacity.
- **Version and status audit** — current version vs latest version, engine
  status, and creation time.
- **Mixed-engine detection** — confirm whether a tenant runs both CSE
  (ServiceComb) engines and Nacos / gateway engines.

Key properties:

- **Read-only by design** — only `ListEngines` is ever constructed; the
  write-intent guard rejects mutating intents before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary path; when the hcloud
  binary is absent the official SDK is used with the same output modes.
- **Full pagination** — `total`-driven paging (full-page fallback, max 100
  pages).
- **Secret-safe** — credentials come only from the active KooCLI profile or
  standard environment variables; the script never reads, echoes or stores
  secrets.

Out of scope: creating, deleting, upgrading, resizing, rebooting or otherwise
mutating engines; engine detail / job inspection. Those require a dedicated
write-capable skill and explicit user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdkcse` for the
   fallback path.
2. **Active credential profile** — configure credentials out-of-band
   (`hcloud configure` in your own terminal, or credential environment
   variables). Never paste AK/SK into chat; the script never reads, echoes or
   stores secrets.
3. **IAM permission** — `cse:engine:list` (read-only); least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess).
5. **Outbound HTTPS** access to `cse.<region>.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`).
2. **Choose the engine type** with `--type` (default `ALL`).
3. **Optionally filter by name** with `--name` (exact) or `--name ... --fuzzy`
   (substring); the filter is applied client-side after all pages are fetched.
4. **Run the list script** with the desired output mode.
5. **Read the result** — concise for humans, `--table` for a full audit,
   `--json` for tooling.
6. **Handle empty / error cases** per the Error Handling table below.

## Core Commands

```bash
# 1) All engines in the default region (cn-north-4), concise inventory
python3 scripts/list_cse_engines.py --region cn-north-4

# 2) Only Nacos engines, full-field table
python3 scripts/list_cse_engines.py --type Nacos --table

# 3) Only microservice-gateway engines, JSON output
python3 scripts/list_cse_engines.py --type MicroGateway --json

# 4) Exact name lookup (client-side, case-insensitive)
python3 scripts/list_cse_engines.py --name cse-prod

# 5) Fuzzy name lookup (client-side substring)
python3 scripts/list_cse_engines.py --name prod --fuzzy

# 6) Explicit sub-project + larger page size
python3 scripts/list_cse_engines.py --project-id <project-id> --page-size 50
```

Equivalent direct KooCLI command (the script wraps exactly this, with paging):

```bash
hcloud CSE ListEngines --cli-region=cn-north-4 --limit=100 --offset=0 --type=ALL
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| --------- | -------- | ----------- | ------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--type` | No | Engine type, server-side: `ALL` \| `CSE` \| `Nacos` \| `MicroGateway` (case-insensitive, default `ALL`) | `Nacos` |
| `--name` | No | Engine name filter, client-side, case-insensitive **exact** match | `cse-prod` |
| `--fuzzy` | No | Turn `--name` into a case-insensitive substring match | — |
| `--project-id` | No | Sub-project ID; when omitted KooCLI uses the profile's default project | `41bd...e3c8` |
| `--table` | No | Output the full-field table | — |
| `--json` | No | Output normalized items as JSON | — |
| `--page-size` | No | Page size (default 100) | `50` |
| `--operation` | No | hcloud operation name; must equal `ListEngines` | `ListEngines` |

Output-mode precedence: `--json` → `--table` → concise (default).

`--type` is forwarded to the API on every page; `--name` / `--fuzzy` are applied
locally after the full list is fetched (the API has no name parameter).

## Output Modes

| Mode | Trigger | Content |
| ---- | ------- | ------- |
| Concise (default) | none | One line per engine: name, id, type, version, status, instances (`used/total`), region |
| Table | `--table` | Union of all returned fields, with preferred columns first: name / id / type / version / status / flavor / instance counts / create_time / region / enterprise project / addresses; missing fields render `-`; epoch times render as UTC |
| JSON | `--json` | Normalized items (camelCase and snake_case both mapped to canonical keys) as a JSON array |

## Write-Intent Guard

- The script scans flag names plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `upgrade`, `modify`, `remove`,
  `start`, `stop`, `restart`, `reboot`, `resize`, `scale`, `bind`, `unbind`,
  `batch...`, and CSE operation names such as `CreateEngine`, `DeleteEngine`).
- The values of read-only selector/filter flags (`--region`, `--type`,
  `--name`, `--project-id`, `--page-size`) are **not** scanned: they are read
  data and may legitimately contain write-looking words (e.g. an engine named
  `update-prod`).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`,
  and exits with code 1 **before** a single hcloud command is executed. The
  guard runs on the raw argv *before* argparse, so a mutating flag such as
  `--create-engine` is reported as a guard violation.
- Only `ListEngines` is ever constructed by `build_command()`; there is no code
  path that can issue a mutating call.

## KooCLI Command Format Standard

```text
hcloud CSE ListEngines --cli-region=<region> --limit=<n> --offset=<n> --type=<ALL|CSE|Nacos|MicroGateway> [--project_id=<id>]
```

- **Service name** — exact KooCLI title-case name: `CSE`.
- **Operation name** — PascalCase: `ListEngines`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete call).
- **Parameters** — `--limit` (string), `--offset` (integer), `--type`
  (`ALL`/`CSE`/`Nacos`/`MicroGateway`), optional `--project_id`. There is no
  name query parameter, so `--name` is applied client-side.

## Error Handling

| Scenario | Behavior |
| -------- | -------- |
| Empty list | Exit 0, prints `未找到微服务引擎（region=<r>，type=<t>...）` |
| 403 / insufficient IAM permission | Exit 1, `无权限访问 CSE 微服务引擎，请检查 IAM 权限（cse:engine:list）` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| hcloud not installed | Exit 1 after the SDK fallback is also unavailable, hint to install KooCLI or the SDK |
| Network / API failure | Exit 1, `网络异常` hint with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `CSE ListEngines --help` |
| API error body with exit code 0 (`error_code` / `error_message`) | Exit 1, classified as auth / credential / generic instead of being parsed as data |
| Write intent detected | Exit 1, `GuardError` message, no command executed |
| Unexpected exception | Exit 1, one-line `[错误] 未预期的失败：...` — no traceback |

Exit codes: `0` success / empty list; `1` config, auth, guard, or API error;
`2` argparse usage error (invalid `--type`, unknown flag).

## Edge Cases

| Scenario | Handling |
| -------- | -------- |
| `--type` omitted | Defaults to `ALL` |
| `--fuzzy` without `--name` | Ignored (no name filter applied) |
| `--name` matches nothing | Exit 0 with the 未找到微服务引擎 message including the filter |
| Large collection | `total`-driven paging with `offset`/`limit`; full-page fallback when `total` is absent; max 100 pages |
| Response is a bare array | Defensive support: treated like `{"data": [...]}` |
| camelCase / snake_case fields | Both mapped during normalization (`totalInstance` / `total_instance`) |
| Field missing on an engine | Rendered as `-` in the table / concise line |
| `createTime` epoch milliseconds | Rendered as `YYYY-MM-DD HH:MM:SS UTC` in table output |
| `region` absent in the item | Filled from `--region` |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkcse`, same output modes |
| User asks to create/delete/upgrade | Out of scope — blocked by the write-intent guard |

## Testing

Offline unit tests with a mocked hcloud subprocess and a fake SDK (no
credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / update / upgrade /
modify / restart / resize / selector values not scanned / operation whitelist),
command construction (region, limit, offset, type, project id), JSON extraction
(object / bare array / noise / invalid), envelope extraction (`{total,data}` /
bare array / unknown), normalization (camelCase / snake_case / missing fields),
time formatting, name filters (exact / fuzzy / case-insensitive), paging
(total-driven / full-page fallback / short page / max-page guard), failure
classification (missing AK/SK / 403 / `[USE_ERROR]` with rc=0 / network /
generic / error body with rc=0), SDK fallback (success / missing credentials /
auth error / hcloud absent), rendering, and all main() output modes
(concise / table / json / empty / guard rejection).

## Reference Documents

| Document | Content |
| -------- | ------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy (`cse:engine:list`) |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation, credential configuration and SDK fallback |
| [references/verification-method.md](references/verification-method.md) | How the skill, its commands and tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |