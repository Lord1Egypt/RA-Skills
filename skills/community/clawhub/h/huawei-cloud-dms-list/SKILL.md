---
name: huawei-cloud-dms-list
description: |
  1. List Huawei Cloud DMS (Distributed Message Service) instances in a tenant
     region through KooCLI — Kafka via `hcloud Kafka ListInstances` and RabbitMQ
     via `hcloud RabbitMQ ListInstancesDetails` (both read-only
     GET /v2/{project_id}/instances) — with an automatic fallback to the
     official huaweicloudsdkkafka / huaweicloudsdkrabbitmq v2 SDKs when hcloud
     is not installed.
  2. Default output is the compact instance-name list (名称列表, also available
     via --names-only); --table renders the full-field table
     (实例ID/名称/引擎/版本/规格/状态/节点数/存储空间/创建时间/VPC/子网/连接地址,
     missing values shown as "-"), and --json outputs the raw instance array.
  3. Supports --engine kafka|rabbitmq|all (default all, both engines), region /
     project override, --limit / --offset paging with automatic page fetching,
     and the real server-side filters --name / --name-equal / --instance-id /
     --status / --enterprise-project-id.
  4. Explicit error hints for empty instance lists (「当前区域（x）无 DMS 实例」),
     403 / insufficient IAM permission, missing or invalid AK/SK credentials,
     missing project_id on the SDK fallback, missing hcloud, and KooCLI
     [USE_ERROR] usage failures (all non-zero exit).
  5. Built-in write-intent guard: any mutating intent (create / delete / resize /
     restart / flush / clear / restore / backup / freeze / migrate) or any
     operation other than the two read-only list operations is rejected before
     execution — this skill is strictly read-only, every request is a GET.
  6. Triggers include: "list DMS instances", "DMS instance list", "查询 DMS 实例
     列表", "DMS 实例列表", "Kafka 实例列表", "RabbitMQ 实例列表", "消息实例列表",
     "DMS inventory", "list kafka instances", "华为云 DMS 列表".
  7. Offline unit tests (mocked hcloud subprocess + fake SDK clients) cover the
     output modes, filters, paging, error scenarios, SDK fallback and the
     write-intent guard.
tags: [huawei-cloud, dms, kafka, rabbitmq, readonly]
---

# Huawei Cloud DMS Instance List

## Overview

Query the DMS (Distributed Message Service) instance list of a tenant region
through KooCLI. DMS has **no `DMS` KooCLI service name**: Kafka and RabbitMQ are
two distinct KooCLI services, so one inventory query is two read-only calls:

| Engine | KooCLI command | REST path |
|--------|----------------|-----------|
| Kafka | `hcloud Kafka ListInstances --engine=kafka` | `GET /v2/{project_id}/instances` |
| RabbitMQ | `hcloud RabbitMQ ListInstancesDetails --engine=rabbitmq` | `GET /v2/{project_id}/instances` |

Both paths and parameters were verified against `hcloud ... --help` on
KooCLI 7.3.12 and against the official SDK `_http_info` metadata
(`huaweicloudsdkkafka` v2 `KafkaClient.list_instances`,
`huaweicloudsdkrabbitmq` v2 `RabbitMQClient.list_instances_details`). The skill
is aimed at message-service inventory inspection, daily operations patrol, and
as a pre-query step for other DMS skills that need an `instance_id`.

Architecture:

```text
agent → python3 scripts/list_dms.py → hcloud Kafka    ListInstances        --engine=kafka
                                    → hcloud RabbitMQ ListInstancesDetails --engine=rabbitmq
      → Huawei Cloud DMS OpenAPI (dms.<region>.myhuaweicloud.com) → parsed JSON
      → names list / table / --json

(hcloud binary missing) → fallback: huaweicloudsdkkafka v2 KafkaClient.list_instances
                                    huaweicloudsdkrabbitmq v2 RabbitMQClient.list_instances_details
```

Key properties:

- **Read-only by design** — every request is `GET
  /v2/{project_id}/instances`. A write-intent guard scans user arguments and
  validates the operation name; mutating intents are rejected with an explicit
  message before any command runs.
- **CLI first, SDK fallback** — KooCLI is the primary execution path (it also
  resolves `project_id` from the profile); when the hcloud binary is absent the
  script falls back to the official Kafka / RabbitMQ SDKs. Credentials are
  always read from the CLI profile or a whitelisted set of AK/SK environment
  variable names — never handled by the script.
- **Name list by default** — the default output mode is the compact
  instance-name list (「DMS 实例名称列表」); `--table` renders the full-field
  table and `--json` the raw response array.
- **Server-side filters & automatic paging** — `--name` / `--exact_match_name`
  / `--instance_id` / `--status` / `--enterprise_project_id` are real
  server-side query parameters; paging uses `--limit` (1~50) + `--offset` and is
  fetched automatically until `instance_num` is reached.
- **Offline-testable** — every code path (filters, paging, error
  classification, guard, SDK fallback, rendering) is covered by unit tests that
  mock the hcloud subprocess and the SDK clients.

Out of scope: every mutating DMS action (create / delete / resize / restart /
flush / clear data / backup / restore / migrate, topic-queue-vhost-user
sub-resources) and cross-region aggregation. Write actions require a dedicated
write-capable skill with explicit user confirmation.

**Dependency**: Quality telemetry is collected automatically via
skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install huaweicloudsdkcore huaweicloudsdkkafka
   huaweicloudsdkrabbitmq` to enable the SDK fallback path.
2. **Active credential profile configured offline/out-of-band** — run the
   KooCLI configure command in your own terminal, or export
   `HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK` before starting the agent.
   Never paste AK/SK into chat; the script never reads, echoes or stores secrets
   itself — authentication is delegated to the hcloud profile / SDK
   environment.
3. **project_id** — the KooCLI path resolves it from the credential profile
   automatically; pass `--project-id` to override. The SDK fallback requires it
   (`--project-id` or `HUAWEICLOUD_SDK_PROJECT_ID` / `HUAWEI_PROJECT_ID`),
   because the REST path is `/v2/{project_id}/instances`.
4. **IAM permission** — read-only `dms:instance:list`; least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
5. **Python 3.8+** (standard library only — argparse / json / subprocess).
6. **Outbound HTTPS** access to `dms.cn-north-4.myhuaweicloud.com`.
- **skill-quality-cli** — ensured by `bash scripts/ensure_cli.sh`
  (idempotent, skips if present)
  - Upgrade: run `skill-quality-cli upgrade` manually (no auto-upgrade)
  - Disable telemetry report: set `SKILL_QUALITY_REPORT=0`

## Workflow

1. **Confirm the target region** (default `cn-north-4`) and engine
   (`all` = Kafka + RabbitMQ, or a single engine).
2. **Confirm KooCLI readiness** (optional, read-only) by listing the active
   credential profile.
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — name list (default) for a compact inventory, table for
   humans, `--json` for downstream tooling.
5. **Handle the empty / error cases** per the Error Handling table below (the
   script prints an explicit hint for an empty region, 403, missing AK/SK,
   missing hcloud, and KooCLI `[USE_ERROR]`).

## Core Commands

> **⚠️ Mandatory: every hcloud command in this skill MUST be wrapped with
> `skill-quality-cli run --skill-name huawei-cloud-dms-list -- ` — bare hcloud
> calls are strictly forbidden.**

```bash
# Compact instance-name list for both engines (default)
python3 scripts/list_dms.py --region cn-north-4
python3 scripts/list_dms.py --names-only

# Only one engine
python3 scripts/list_dms.py --engine kafka
python3 scripts/list_dms.py --engine rabbitmq

# Full-field table (实例ID/名称/引擎/版本/规格/状态/节点数/存储空间/创建时间/VPC/子网/连接地址)
python3 scripts/list_dms.py --table

# Raw JSON of every returned field
python3 scripts/list_dms.py --json

# Filters (all real server-side query parameters)
python3 scripts/list_dms.py --name dms-demo
python3 scripts/list_dms.py --name dms-demo --name-equal      # exact_match_name=true
python3 scripts/list_dms.py --instance-id 6c7f2f0e-...
python3 scripts/list_dms.py --status RUNNING
python3 scripts/list_dms.py --enterprise-project-id 0

# Paging: page size 1~50 (default 50); pages are fetched automatically
python3 scripts/list_dms.py --limit 10 --offset 20
python3 scripts/list_dms.py --limit 10 --single-page           # exactly one page

# Explicit project override (otherwise resolved from the profile)
python3 scripts/list_dms.py --project-id 05f6... --engine kafka
```

Equivalent direct KooCLI commands (the script wraps exactly these calls, with
automatic offset paging):

```bash
skill-quality-cli run --skill-name huawei-cloud-dms-list -- hcloud Kafka ListInstances --cli-region=cn-north-4 --engine=kafka --limit=50 --offset=0
skill-quality-cli run --skill-name huawei-cloud-dms-list -- hcloud RabbitMQ ListInstancesDetails --cli-region=cn-north-4 --engine=rabbitmq --limit=50 --offset=0
skill-quality-cli run --skill-name huawei-cloud-dms-list -- hcloud Kafka ListInstances --cli-region=cn-north-4 --engine=kafka --name=dms-demo --status=RUNNING
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--engine` | No | Message engine: `kafka` / `rabbitmq` / `all` (default `all`) | `kafka` |
| `--names-only` | No | Output instance names only — **this is also the default mode** | — |
| `--table` | No | Output the full-field table | — |
| `--json` | No | Output the raw instance array as JSON | — |
| `--name` | No | Filter by instance name — real server-side query parameter (fuzzy) | `dms-demo` |
| `--name-equal` | No | Exact name match: forwards `exact_match_name=true` with `--name` | used with `--name` |
| `--instance-id` | No | Filter by exact instance ID — real server-side query parameter | `6c7f2f0e-...` |
| `--status` | No | Filter by instance state — real server-side query parameter (`RUNNING` / `ERROR` / `CREATING` / ...) | `RUNNING` |
| `--enterprise-project-id` | No | Filter by enterprise project ID — real server-side query parameter | `0` |
| `--limit` | No | Page size (default 50, server range 1–50; pages are fetched automatically) | `10` |
| `--offset` | No | Start offset (server parameter, default 0) | `20` |
| `--max-pages` | No | Maximum pages fetched automatically (default 50, loop guard) | `5` |
| `--single-page` | No | Fetch exactly one page (no further offsets) | — |
| `--project-id` | No | Project ID override (needed by the SDK fallback path) | `05f6...` |
| `--operation` | No | hcloud operation name; only `ListInstances` / `ListInstancesDetails` are allowed | `ListInstances` |

Output-mode precedence: `--json` → `--table` → default names list
(`--names-only` is an explicit synonym of the default).

## Write-Intent Guard

- The script scans all user arguments plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `drop`, `update`, `modify`, `resize`, `scale`,
  `restart`, `reboot`, `flush`, `clear`, `purge`, `restore`, `backup`, `freeze`,
  `unfreeze`, `release`, `terminate`, `destroy`, `upgrade`, `rollback`,
  `migrate`, and DMS operation names such as `CreateInstance`,
  `DeleteInstance`, `ResizeInstance`, `RestartInstance`, `ResetPassword`).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`,
  and exits with code 1 **before** a single hcloud command is executed.
- Only `hcloud Kafka ListInstances` / `hcloud RabbitMQ ListInstancesDetails`
  (GET) — or the SDK `list_instances` / `list_instances_details` calls in the
  fallback path — are ever constructed by `build_command()`; there is no code
  path that can issue a mutating DMS API call.
- Status values that are legitimate DMS states (`CREATING`, `DELETING`,
  `EXTENDING`, …) are not write intents and are **not** blocked.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — there is **no `DMS` service** in KooCLI
  (`hcloud DMS ListInstances` → `[USE_ERROR]Unsupported service: DMS`). Use the
  engine services: `Kafka` and `RabbitMQ`.
- **Operation name** — PascalCase: `ListInstances` (Kafka) /
  `ListInstancesDetails` (RabbitMQ).
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete DMS call).
- **Engine parameter** — `--engine=kafka` / `--engine=rabbitmq` (required; the
  operation rejects a missing or mismatched engine).
- **Simple parameter** — `--key=value`, e.g. `--name=dms-demo`,
  `--instance_id=<id>`, `--status=RUNNING`, `--exact_match_name=true`,
  `--enterprise_project_id=0`, `--project_id=<id>`. All of these are real
  server-side ListInstances query parameters (verified against the SDK
  `ListInstancesRequest` / `ListInstancesDetailsRequest` models).
- **Paging** — `--limit` (1~50; KooCLI defaults to 10 per page when unset) +
  `--offset` (≥ 0); the script fetches pages automatically until the response
  `instance_num` total is reached.
- **REST path (official SDK `_http_info`)** —
  `GET /v2/{project_id}/instances` for both engines; the project_id is resolved
  by KooCLI from the credential profile.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty instance list | Exit 0, prints `当前区域（<x>）无 DMS 实例` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问分布式消息服务（DMS），请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure credentials out-of-band (never in chat) |
| Missing project_id (SDK fallback) | Exit 1, hint to pass `--project-id` or set the project-id env var |
| hcloud not installed | SDK fallback; exit 1 only when the SDK is also unavailable, with install hints |
| KooCLI `[USE_ERROR] ...` (even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `--help` |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| `--limit` / `--offset` / `--max-pages` out of range | Exit 1, explicit range error before any call |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Account with only Kafka or only RabbitMQ instances | `--engine all` merges both lists; use one engine to narrow |
| Kafka + RabbitMQ instances with the same name | Both are listed (names are per engine); `--instance-id` disambiguates |
| Non-`RUNNING` instances (ERROR / FROZEN / CREATING / ...) | Reported with their state, not treated as failure |
| Large instance count | Automatic `limit`/`offset` paging driven by `instance_num` (max 50 pages) |
| Field missing on an instance (e.g. no `subnet_name`) | Rendered as `-` in the table; VPC/subnet fall back to the `*_id` field |
| Kafka `node_num` vs RabbitMQ `broker_num` | The 节点数 column reads `node_num` then `broker_num` |
| Instance without a name | The name list falls back to `instance_id` |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to the official Kafka / RabbitMQ SDK list calls, same output modes |
| User asks to create/delete/resize/flush a topic or instance | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess and fake SDK clients (no
credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / resize / restart /
flush / clear / restore / backup / freeze / migrate / normalized variants /
operation whitelist / status values not blocked), command construction (Kafka vs
RabbitMQ service names, real server-side filters forwarded, paging params, no
write flags ever), JSON extraction, failure classification (missing AK/SK, 403,
generic, `[USE_ERROR]` with rc=0), offset paging (`instance_num`-driven /
short-page stop / empty / max-pages guard), SDK fallback (env credentials,
missing credentials, missing project id, pagination, filters, real request
signature, client endpoint resolution), rendering (12-column table, missing
values as `-`, VPC/subnet fallback, `broker_num` fallback) and all `main()`
output and error paths. SDK-specific tests run when the official SDKs are
installed and skip otherwise.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy (`dms:instance:list`) |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI / skill-quality-cli installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its API provenance were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |