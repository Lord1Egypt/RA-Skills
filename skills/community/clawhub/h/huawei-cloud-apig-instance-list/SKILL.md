---
name: huawei-cloud-apig-instance-list
description: |
  1. List Huawei Cloud APIG dedicated instances in a tenant region through
     KooCLI (hcloud APIG ListInstancesV2 — read-only GET
     /v2/{project_id}/apigw/instances), with an automatic fallback to the
     official huaweicloudsdkapig v2 SDK when hcloud is not installed.
  2. Drill down into one instance's API inventory with --instance-id
     (hcloud APIG ListApisV2 — read-only GET
     /v2/{project_id}/apigw/instances/{instance_id}/apis); an unknown instance
     id is reported explicitly with a non-zero exit code.
  3. Three output modes: compact list (default — instance name / id / status),
     --table (实例ID/名称/状态/规格/版本/可用区/EIP/VPC/创建时间), and --json
     (raw response records).
  4. Client-side filters --name (--fuzzy for substring match), --instance-id
     and --status; --region override (default cn-north-4); --limit 1-100 with
     automatic offset/limit paging.
  5. Explicit error hints for empty instance lists, 403 / insufficient IAM
     permission, missing or invalid AK/SK credentials, [USE_ERROR] parameter
     errors, and a non-existent instance id.
  6. Built-in write-intent guard: any mutating intent (create / delete /
     update / publish / offline / bind-eip / unbind-eip / ...) is rejected
     before execution — this skill is strictly read-only.
  7. Triggers include: "list APIG instances", "APIG 实例列表", "查询APIG实例",
     "APIG 专享版实例", "apig instance inventory", "查询实例API列表",
     "APIG API 列表", "apig gateway list".
tags: [huawei-cloud, apig, network, readonly, koo-cli]
---

# Huawei Cloud APIG Dedicated Instance List

## Overview

Query the APIG (API Gateway) dedicated instance inventory of a tenant through
KooCLI `hcloud APIG ListInstancesV2 --cli-region=<region>` (official read-only GET
`/v2/{project_id}/apigw/instances`), and optionally drill down into one
instance's API inventory through `hcloud APIG ListApisV2 --cli-region=<region>` (official read-only
GET `/v2/{project_id}/apigw/instances/{instance_id}/apis`). Both endpoints and
parameter names were verified against the official `huaweicloudsdkapig` v2
client metadata (`_list_instances_v2_http_info`,
`_list_apis_v2_http_info`) and the KooCLI `--help` output at build time.

Architecture:

```text
agent → python3 scripts/list_apig_instances.py → hcloud APIG ListInstancesV2 --cli-region=<region>
      → Huawei Cloud APIG OpenAPI (apig.<region>.myhuaweicloud.com)
      → parsed JSON → compact list / --table / --json
      (--instance-id) → hcloud APIG ListApisV2 --instance_id=<id> → API list of that instance

(hcloud binary missing) → fallback: huaweicloudsdkapig v2 ApigClient
                          .list_instances_v2 / .list_apis_v2
```

Key properties:

- **Read-only by design** — the only APIs ever invoked are `ListInstancesV2`
  and `ListApisV2` (both GET). `build_command()` cannot construct anything
  else, and a write-intent guard rejects mutating intents before any command
  runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  `hcloud` binary is absent the script falls back to the official
  `huaweicloudsdkapig` v2 SDK. Credentials are always resolved by the CLI
  profile / SDK environment — never handled by the script.
- **Instance → API drill-down** — `--instance-id` first verifies the instance
  exists (a ListInstancesV2 call filtered by `instance_id`), then lists that
  instance's APIs; an unknown id yields an explicit `实例不存在` error (exit 1).
- **Offline-testable** — paging, filters, output modes, error classification,
  the guard and the SDK fallback are all covered by unit tests that mock the
  KooCLI subprocess (no credentials, no network).

Out of scope: every mutating APIG action (create / delete / update instances,
publish / offline APIs, bind / unbind EIP), other APIG objects (groups,
environments, apps, plugins, ACLs, throttling policies, signatures), and
non-APIG services. Those require dedicated write-capable skills with explicit
user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdkapig` to enable
   the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band (run the
   KooCLI configure command in your terminal, or set credential environment
   variables). Never paste AK/SK into chat; the script never reads, echoes or
   stores secrets — authentication is delegated entirely to the hcloud profile
   / SDK environment.
3. **project_id (SDK fallback only)** — both REST paths carry
   `{project_id}`; when falling back to the SDK, supply it via `--project-id`
   or the `HUAWEICLOUD_SDK_PROJECT_ID` / `HUAWEI_PROJECT_ID` environment
   variables. The KooCLI path resolves it from the profile automatically.
4. **IAM permission** — read-only `apig:instances:list` (instances) and
   `apig:apis:list` (APIs); least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
5. **Python 3.8+** (standard library only — argparse / json / subprocess).
6. **Outbound HTTPS** access to `apig.cn-north-4.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`).
2. **(Optional, read-only) confirm KooCLI readiness** by listing the active
   credential profile.
3. **Run the list script** with the desired output mode and filters; add
   `--instance-id` to drill down into one instance's API list.
4. **Read the result** — compact list for humans, `--table` for a
   fixed-column overview, `--json` for downstream tooling.
5. **Handle the empty / error cases** per the Error Handling table (the script
   prints explicit hints for an empty region, 403, missing AK/SK, parameter
   errors and a non-existent instance).

## Core Commands

```bash
# Compact list (default): 名称 / 实例ID / 状态
python3 scripts/list_apig_instances.py --region cn-north-4

# Fixed-column table: 实例ID/名称/状态/规格/版本/可用区/EIP/VPC/创建时间
python3 scripts/list_apig_instances.py --table

# Raw response records as JSON
python3 scripts/list_apig_instances.py --json

# Client-side filters: exact name, fuzzy name, status
python3 scripts/list_apig_instances.py --name apig-prod-01
python3 scripts/list_apig_instances.py --name apig --fuzzy
python3 scripts/list_apig_instances.py --status Running

# Drill down: list the APIs of one instance (validates the id first)
python3 scripts/list_apig_instances.py --instance-id c16795b9553d422a8cb1977a2279113f
python3 scripts/list_apig_instances.py --instance-id c16795b9553d422a8cb1977a2279113f --table
python3 scripts/list_apig_instances.py --instance-id c16795b9553d422a8cb1977a2279113f --limit 5 --json

# Cap the record count (1-100, automatic offset/limit paging)
python3 scripts/list_apig_instances.py --limit 20
```

Equivalent direct KooCLI commands (the script wraps exactly these calls, with
offset/limit paging):

```bash
hcloud APIG ListInstancesV2 --cli-region=cn-north-4 --limit=50 --offset=0
hcloud APIG ListInstancesV2 --cli-region=cn-north-4 --instance_id=c16795b9553d422a8cb1977a2279113f --limit=1 --offset=0
hcloud APIG ListApisV2 --cli-region=cn-north-4 --instance_id=c16795b9553d422a8cb1977a2279113f --limit=50 --offset=0
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--json` | No | Output the raw response records as JSON | — |
| `--table` | No | Output the fixed-column table instead of the compact list | — |
| `--name` | No | Filter by instance name (API name in drill-down mode); exact match unless `--fuzzy` | `apig-prod-01` |
| `--fuzzy` | No | Make `--name` a substring (fuzzy) match | — |
| `--instance-id` | No | Drill down: verify the instance, then list its APIs | `c16795b9553d422a8cb1977a2279113f` |
| `--status` | No | Filter by status string (`Running`, `CreateSuccess`, ... for instances) — client-side | `Running` |
| `--limit` | No | Maximum number of records returned (1-100, default 100); larger result sets are fetched with offset/limit paging | `20` |
| `--project-id` | No | Project ID (only needed by the SDK fallback for `/v2/{project_id}/apigw/...`) | `05f...` |

Output-mode precedence: `--json` → `--table` → compact list (default).

`--name` / `--status` are applied **client-side** (the APIG service-side
`instance_name` / `status` parameters match less predictably and `--fuzzy`
needs substring matching); only `--instance-id` is forwarded to the API, as the
existence check. In drill-down mode `--name` filters API names and `--status`
filters API status values.

## Output Format

| Mode | Instances | Drill-down (APIs) |
| ---- | --------- | ----------------- |
| default | `- <名称>  <实例ID>  <状态>` per instance | `- <名称>  <方法> <路径>  <API_ID>  <状态>` per API |
| `--table` | 实例ID / 名称 / 状态 / 规格 / 版本 / 可用区 / EIP / VPC / 创建时间 | API_ID / 名称 / 类型 / 版本 / 请求方法 / 协议 / 路径 / 认证方式 / 状态 / 分组 / 注册时间 |
| `--json` | `{"region","count","instances":[...]}` | `{"region","instance_id","instance","count","apis":[...]}` |

- `ListInstancesV2` returns `id` / `instance_name` / `status` / `spec` /
  `eip_address` / `create_time` (epoch **milliseconds**) and a few extras
  (`type`, `instance_status`, `loadbalancer*`, `project_id`,
  `enterprise_project_id`, `charging_mode`). The service does **not** return
  version / availability zone / VPC for a basic instance, so those table cells
  show `-`; `--json` always carries the complete raw record.
- `create_time` is rendered as `YYYY-MM-DD HH:MM:SS UTC` in the table and kept
  raw in `--json`.
- `--table` keeps the documented column set (readable in a terminal);
  `--json` is the lossless view.

## Write-Intent Guard

- The guard scans the command tokens (not user filter values such as
  `--name` / `--status` / `--instance-id`) for mutating vocabulary:
  `create`, `delete`, `update`, `modify`, `publish`, `offline`, `unpublish`,
  `bind`, `unbind`, `add`, `remove`, `attach`, `detach`, `associate`,
  `disassociate`, `enable`, `disable`, `import`, `export`, `reset`,
  `restart`, `change`, `freeze`, `migrate`, `upgrade`, `authorize`, `cancel`,
  plus APIG operation names (`CreateInstanceV2`, `DeleteApiV2`,
  `PublishApiV2`, `BindEip`, `UnbindEip`, ...). Normalized separators
  (`--delete-api`, `delete_api_v2`, `deleteApi`) all hit the same keyword.
- The guard runs **before argparse**, so a mutating flag such as `--publish`
  is rejected with exit code 1 (guard message) instead of argparse's
  "unrecognized arguments" exit code 2.
- `build_instance_command()` / `build_apis_command()` can only emit
  `ListInstancesV2` / `ListApisV2`; there is no code path that issues a
  mutating APIG call.
- A legitimate query whose resource name contains a mutating verb (for example
  an API named `create-api`) still works: filter values are excluded from the
  guard scan.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `APIG`.
- **Operation names** — PascalCase and versioned: `ListInstancesV2` (there is
  **no** bare `ListInstances` operation in KooCLI 7.3.12 — the version-less
  name answers `[USE_ERROR]Operation ListInstances is not supported`),
  `ListApisV2`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete APIG call).
- **Simple parameter** — `--key=value`, e.g. `--limit=50`, `--offset=0`,
  `--instance_id=<32-hex id>`.
- **Paging** — `offset` + `limit` (limit ≤ 500 server-side; this skill uses a
  50-record page step and caps the returned records at `--limit` 1-100). The
  response carries `total` / `size` plus the `instances` (or `apis`) array.
- **REST paths (official SDK `_http_info`)** —
  `GET /v2/{project_id}/apigw/instances` (`ListInstancesV2`) and
  `GET /v2/{project_id}/apigw/instances/{instance_id}/apis` (`ListApisV2`);
  `project_id` is resolved by KooCLI from the credential profile,
  `instance_id` is a required path parameter of the API list call.

## Error Handling

| Scenario | Behavior |
| --------- | --------- |
| Empty APIG instance list | Exit 0, prints `当前区域（<x>）无 APIG 专享版实例` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问 APIG 实例，请检查 IAM 权限` hint (mentions `apig:instances:list` / `apig:apis:list`) |
| 401 / invalid or expired AK-SK (`APIGW.0301`) | Exit 1, `凭证无效（401：AK/SK 无效或已过期）` hint (never reported as 403) |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| Missing project_id (SDK fallback) | Exit 1, hint to pass `--project-id` or set the project-id env var |
| hcloud not installed | SDK fallback; only when that is unavailable too → exit 1 with install hints |
| `--instance-id` not found in the region | Exit 1, `实例不存在：region <x> 下未找到实例 <id>` (hint to list instances first) |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit KooCLI parameter-error hint pointing to the `ListInstancesV2` operation help |
| KooCLI API error envelope (`{"error_code": ..., "error_msg": ...}`, even with exit code 0) | Exit 1, classified as 401/403/API error; never treated as an empty list |
| Write intent detected | Exit 1, guard message, no command executed |
| `--limit` outside 1-100 | Exit 2, argparse range error |

Exit codes: `0` success / empty region; `1` config, auth, guard, not-found or
API error; `2` invalid CLI argument.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Non-`Running` instances | Reported with their state (`CreateSuccess` / `Initing` / `Deleting` / ...), not treated as failure |
| `--name` / `--status` filters | Applied client-side (documented above), so `--fuzzy` works and no server parameter spelling is assumed |
| Large inventories | offset/limit paging with a 50-record page step, hard stop at 100 pages; returned records capped by `--limit` |
| Field missing on an instance | Rendered as `-` in the table; `--json` keeps the record as returned |
| Nested field (`loadbalancerIdList`) | Rendered as compact JSON inside its `--json` record; the table keeps the documented columns |
| Instance with no APIs | Exit 0, `实例 <id>（<region>）下无 API` hint |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkapig` v2, same output modes |
| User asks to create/delete/publish an instance or API | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / update /
publish / offline / bind-eip / unbind-eip / normalized variants / operation
whitelist / filter values exempt), command construction (region, limit, offset,
instance_id; ListApisV2 requires an instance id; only read operations can be
built), JSON extraction and error-envelope detection, failure classification
(missing AK/SK / 401 / 403 / generic / `[USE_ERROR]` with rc=0 / API envelope
with rc=0), offset/limit paging (page step, second-page offset, limit stop,
total bound, empty page), SDK fallback (CLI missing → SDK called once, missing
credentials, SDK unavailable, request field construction), client-side filters
(exact / fuzzy / status), rendering (table columns, missing field, timestamps,
compact lines), and all `main()` modes incl. empty-list hints, drill-down,
invalid instance id, write intent, and `--limit` boundaries.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified (incl. live smoke evidence) |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
