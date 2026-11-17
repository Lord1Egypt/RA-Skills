---
name: huawei-cloud-functiongraph-list
description: |
  1. List Huawei Cloud FunctionGraph (函数工作流) functions of the current
     account / project / region through KooCLI (`hcloud functiongraph
     ListFunctions` — read-only GET `/v2/{project_id}/fgs/functions`, verified
     in the `huaweicloudsdkfunctiongraph` v2 `_list_functions_http_info`
     metadata), with an automatic fallback to the official SDK when hcloud is
     not installed.
  2. Output is **sorted by function name** by default and rendered as a table
     showing 函数名称 (func_name) / 内存 (memory_size, MB) / 超时时间 (timeout,
     s) / 入口 (handler) / 运行时 (runtime) / URN / 分组 (package) etc. Three
     output modes: full-field table (default), `--json` (raw response array),
     and `--names-only` (compact function-name list).
  3. Supports `--name` filtering (func_name, server-side fuzzy search),
     `--package-name` (分组), page-size, automatic marker paging, and a region
     override via `--region` (`--cli-region` under the hood).
  4. Explicit error hints for empty function lists (「当前区域无函数」), 403 /
     insufficient IAM permission (「无权限访问 FunctionGraph」), missing or
     invalid AK/SK credentials, and hcloud not installed.
  5. Built-in write-intent guard: any mutating intent (create / delete / update
     / publish / invoke / import / export / trigger ...) or any operation other
     than ListFunctions is rejected before execution — this skill is strictly
     read-only.
  6. Triggers include: "list functions", "functiongraph list", "查询函数列表",
     "函数工作流函数列表", "FunctionGraph 函数", "函数列表", "functions list",
     "function inventory", "华为云函数工作流", "list functions".
  7. Offline unit tests (mocked hcloud subprocess) cover output modes, filters,
     paging, error scenarios, SDK fallback, sorting, and the write-intent guard.
tags: [huawei-cloud, functiongraph, compute, readonly, koo-cli]
---

# Huawei Cloud FunctionGraph Function List

## Overview

List the FunctionGraph (函数工作流) functions of a Huawei Cloud account /
project / region through KooCLI `hcloud functiongraph ListFunctions` (official
read-only GET `/v2/{project_id}/fgs/functions`, verified in the
`huaweicloudsdkfunctiongraph` v2 `_list_functions_http_info` metadata). The
skill is aimed at function inventory inspection, daily operations patrol, and as
a pre-query step for other FunctionGraph skills that need a function `urn`
(`func_urn`).

Architecture:

```text
agent → python3 scripts/list_functiongraph.py --region <region>
      → hcloud functiongraph ListFunctions --cli-region=<region> --maxitems=<n>
      → Huawei Cloud FunctionGraph OpenAPI (project-scoped endpoint)
      → parsed JSON → sort by func_name → table / --json / --names-only

(hcloud binary missing) → fallback: huaweicloudsdkfunctiongraph v2
                          FunctionGraphClient.list_functions
```

Key properties:

- **Read-only by design** — the only API ever invoked is `ListFunctions` (GET).
  A write-intent guard scans user arguments and validates the operation name;
  mutating intents (create / delete / update / publish / invoke / import /
  export / trigger ...) are rejected with an explicit message before any command
  runs.
- **Sorted by function name** — the result list is sorted by `func_name`
  (case-insensitive, stable) so the table and `--names-only` output are easy to
  scan.
- **CLI first, SDK fallback** — KooCLI is the primary execution path; when the
  KooCLI binary is absent, the script falls back to the official
  `huaweicloudsdkfunctiongraph` v2 SDK (`list_functions`). Credentials are
  always read by the CLI profile / SDK environment — never handled by the
  script.
- **Key columns first** — the default table puts 函数名称 / URN / 内存 / 超时 /
  入口 / 运行时 / 分组 first, then any remaining returned fields.
- **Offline-testable** — every code path (filters, error classification, guard,
  SDK fallback, sorting, paging) is covered by unit tests that mock the hcloud
  subprocess.

Out of scope: every mutating FunctionGraph action (create / delete / update a
function, publish a version, invoke, import / export, trigger management,
dependency management). Those require a dedicated write-capable skill and
explicit user confirmation.

> **Dependency**: Quality telemetry is collected automatically via skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdkfunctiongraph` to
   enable the SDK fallback path.
2. **Active credential profile** — configure credentials out-of-band (run the
   KooCLI configure command in your terminal, or set credential environment
   variables). Never paste AK/SK into chat; the script never reads, echoes, or
   stores secrets itself — authentication is delegated entirely to the hcloud
   profile / SDK environment.
3. **IAM permission** — read-only `functiongraph:function:list`; least-privilege
   policy in [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess).
5. **Outbound HTTPS** access to the region FunctionGraph endpoint
   (`functiongraph.<region>.myhuaweicloud.com`).

- **skill-quality-cli** — ensured by bash scripts/ensure_cli.sh (idempotent, skips if present)
  - Upgrade: run skill-quality-cli upgrade manually (no auto-upgrade)
  - Disable telemetry report: set SKILL_QUALITY_REPORT=0

## Workflow

1. **Confirm the target region** (default `cn-north-4`); the function list is
   project-scoped and region-scoped.
2. **Confirm KooCLI readiness** (optional, read-only) by listing the active
   credential profile.
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — table for humans, `--json` for downstream tooling,
   `--names-only` for a compact inventory; results are sorted by function name.
5. **Handle the empty / error cases** per the Edge Cases table below (the
   script prints an explicit hint for empty region, 403, and missing AK/SK).

## Core Commands

> **⚠️ Mandatory: every hcloud command in this skill MUST be wrapped with skill-quality-cli run --skill-name huawei-cloud-functiongraph-list -- ** — bare hcloud calls are strictly forbidden.**

```bash
# Full-field table (default), sorted by function name
skill-quality-cli run --skill-name huawei-cloud-functiongraph-list -- python3 scripts/list_functiongraph.py --region cn-north-4

# Raw JSON of every returned field
skill-quality-cli run --skill-name huawei-cloud-functiongraph-list -- python3 scripts/list_functiongraph.py --json

# Compact function-name list only
skill-quality-cli run --skill-name huawei-cloud-functiongraph-list -- python3 scripts/list_functiongraph.py --names-only

# Filter by function name (server-side func_name fuzzy search)
skill-quality-cli run --skill-name huawei-cloud-functiongraph-list -- python3 scripts/list_functiongraph.py --name demo

# Filter by package (group name)
skill-quality-cli run --skill-name huawei-cloud-functiongraph-list -- python3 scripts/list_functiongraph.py --package-name default

# Combine filters
skill-quality-cli run --skill-name huawei-cloud-functiongraph-list -- python3 scripts/list_functiongraph.py --region cn-north-4 --name demo --names-only

# Equivalent direct KooCLI command (the script wraps exactly this call)
skill-quality-cli run --skill-name huawei-cloud-functiongraph-list -- hcloud functiongraph ListFunctions --cli-region=cn-north-4 --maxitems=400
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`); passed to hcloud as `--cli-region` | `cn-south-1` |
| `--json` | No | Output the raw function array as JSON | — |
| `--names-only` | No | Output function names only | — |
| `--name` | No | Filter by function name (`func_name`, server-side fuzzy search) | `demo` |
| `--package-name` | No | Filter by the group/package name (`package_name`, server-side) | `default` |
| `--page-size` | No | Number of records per page, max 400 (KooCLI `--maxitems`, default 400) | `100` |
| `--operation` | No | hcloud FunctionGraph operation name; only `ListFunctions` is allowed | `ListFunctions` |

Output-mode precedence: `--names-only` → `--json` → table (default).

> `--project_id` is a required path parameter of `ListFunctions`, but KooCLI
> fills it automatically from the credential profile / `cli-project-id` config,
> so the script never emits it.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — the KooCLI FunctionGraph metadata service name (template
  dir `functiongraph`): `functiongraph`.
- **Operation name** — PascalCase: `ListFunctions`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete FunctionGraph call).
- **REST path (official SDK `_http_info`)** —
  `GET /v2/{project_id}/fgs/functions` (`huaweicloudsdkfunctiongraph` v2
  `_list_functions_http_info`); the project_id is resolved by KooCLI from the
  credential profile.
- **Query parameters** — `--func_name` (fuzzy name), `--package_name` (group),
  `--marker` (pagination cursor from `next_marker`), `--maxitems` (page size,
  max 400, default 400). There is no server-side sort parameter, so the script
  sorts by `func_name` client-side.

## Write-Intent Guard

- The script scans all user arguments plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `modify`, `publish`, `invoke`,
  `import`, `export`, `remove`, `destroy`, and FunctionGraph operation names
  such as `CreateFunction`, `DeleteFunction`, `UpdateFunctionConfig`,
  `PublishFunctionVersion`, `AsyncInvokeFunction`, `CreateFunctionTrigger`).
- Any hit raises `GuardError`, prints
  `[错误] 检测到写操作意图 ... 已被守卫拦截`, and exits with code 1 **before** a
  single hcloud command is executed.
- Only `hcloud functiongraph ListFunctions` (GET) — or the SDK `list_functions`
  call in the fallback path — is ever constructed by `build_command()`; there is
  no code path that can issue a mutating FunctionGraph API call.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty function list | Exit 0, prints `当前区域（<x>）无函数` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问 FunctionGraph，请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| hcloud not installed | Exit 1 after SDK fallback also unavailable, hint to install KooCLI or `pip install huaweicloudsdkcore huaweicloudsdkfunctiongraph` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `hcloud functiongraph ListFunctions --help` |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Pagination | `next_marker` from each page is forwarded as `--marker` until `count` is reached or no more records return |
| `--name` / `--package-name` filters | Forwarded server-side (real `func_name` / `package_name` query parameters) |
| Extra response fields | Table columns are built from the union of flattened fields — new fields appear automatically |
| Field missing on a function | Rendered as `-` in the table |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to `huaweicloudsdkfunctiongraph` `list_functions`, same output modes and sorting |
| User asks to create/delete/invoke a function | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
cd skills/compute/functiongraph/huawei-cloud-functiongraph-list
skill-quality-cli run --skill-name huawei-cloud-functiongraph-list -- python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / publish / invoke /
import / export / trigger / normalized variants / operation whitelist), command
construction (no `--project_id` emitted), JSON extraction, failure
classification (missing AK/SK, 403, generic, `[USE_ERROR]` with rc=0),
client-side name sorting, marker paging, SDK fallback (missing-deps path, real
call), table/names/json rendering, and all `main()` output modes.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
