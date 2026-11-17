---
name: huawei-cloud-dds-list
description: |
  1. List Huawei Cloud DDS (Document Database Service, 文档数据库服务) instances
     in a tenant region through KooCLI — `hcloud DDS ListInstances`
     (read-only GET /v3/{project_id}/instances) — with automatic fallbacks to
     the official huaweicloudsdkdds v3 SDK (`DdsClient.list_instances`) when
     hcloud is not installed, and then to a locally signed REST call when the
     SDK is missing too.
  2. Default output is the compact instance-name list (名称列表, also available
     via --names-only); --table renders the fixed eight-column table
     (实例ID/名称/状态/引擎版本/规格/节点数/创建时间/模式, missing values shown
     as "-", 模式 shown as 集群/副本集/单节点; 规格取自 groups[].nodes[].spec_code,
     节点数取自 groups[].nodes), and --json outputs the raw instance array.
  3. Supports region (default cn-north-4) / project override, --limit (1~100) /
     --offset paging with automatic page fetching until `total_count`, and the
     real server-side filters --name (--fuzzy switches to *-prefix fuzzy
     matching) / --instance-id / --mode Sharding|ReplicaSet|Single /
     --datastore-type / --vpc-id / --subnet-id; --status is a client-side
     filter (the ListInstances API has no server-side status parameter —
     verified).
  4. Explicit error hints for empty instance lists (「当前区域（x）无 DDS 实例」),
     403 / insufficient IAM permission, missing or invalid AK/SK credentials,
     missing project_id on the SDK fallback, missing hcloud, and KooCLI
     [USE_ERROR] usage failures (all non-zero exit).
  5. Built-in write-intent guard: any mutating intent (create / delete /
     restart / resize / backup / restore / upgrade / node add-remove ...) or
     any operation other than the read-only ListInstances is rejected before
     execution — this skill is strictly read-only, every request is a GET.
  6. Triggers include: "list DDS instances", "DDS instance list",
     "查询 DDS 实例列表", "DDS 实例列表", "DDS实例", "文档数据库实例列表",
     "查询DDS实例列表", "MongoDB 实例列表", "DDS inventory",
     "华为云 DDS 列表", "文档数据库".
  7. Offline unit tests (mocked hcloud subprocess + fake SDK clients) cover the
     output modes, filters, paging, error scenarios, SDK fallback and the
     write-intent guard.
tags: [huawei-cloud, dds, document-database, mongodb, readonly]
---

# Huawei Cloud DDS Instance List

## Overview

Query the DDS (Document Database Service, 文档数据库服务) instance list of a
tenant region through KooCLI:

| KooCLI command | REST path |
|----------------|-----------|
| `hcloud DDS ListInstances` | `GET /v3/{project_id}/instances` |

The path, method (`Method: GET`) and the full parameter list were verified
against the KooCLI `DDS ListInstances` help output on KooCLI 7.2.12, and the response
shape (`{"instances": [...], "total_count": N}`) against a live read-only
call. Each instance follows the official `QueryInstanceResponse` model:
creation/update time are `created` / `updated`, the instance type is `mode`,
and the flavor lives at `groups[].nodes[].spec_code` (see
[references/verification-method.md](references/verification-method.md) §3.1).
The IAM action `dds:instance:listAll` was verified against the official
IAM authorization schema. The skill is aimed at database inventory inspection,
daily operations patrol, and as a pre-query step for other DDS skills that
need an `instance_id`.

Architecture:

```text
agent → python3 scripts/list_dds.py → hcloud DDS ListInstances --cli-region=<region>
      → Huawei Cloud DDS OpenAPI (dds.<region>.myhuaweicloud.com) → parsed JSON
      → names list / table / --json

(hcloud binary missing) → fallback 2: huaweicloudsdkdds v3 DdsClient.list_instances
(SDK also missing)      → fallback 3: REST GET /v3/{project_id}/instances (local AK/SK signing)
```

Key properties:

- **Read-only by design** — every request is `GET
  /v3/{project_id}/instances`. A write-intent guard scans user arguments and
  validates the operation name; mutating intents are rejected with an explicit
  message before any command runs.
- **CLI → SDK → REST** — KooCLI is the primary execution path (it also
  resolves `project_id` from the profile); when the hcloud binary is absent
  the script falls back to the official huaweicloudsdkdds SDK, and when the SDK
  is missing as well it issues the same read-only
  `GET /v3/{project_id}/instances` directly with local AK/SK signature V4.
  Credentials are always read from the CLI profile or a whitelisted set of
  AK/SK / security-token environment variable names — never handled by the
  script.
- **Name list by default** — the default output mode is the compact
  instance-name list (「DDS 实例名称列表」); `--table` renders the fixed
  eight-column table and `--json` the raw response array.
- **Fixed table columns** — 实例ID/名称/状态/引擎版本/规格/节点数/创建时间/模式;
  missing values render `-`. 规格 comes from `groups[].nodes[].spec_code`
  (distinct codes de-duplicated) and 节点数 is the number of
  `groups[].nodes[]` entries — there is no top-level flavor field.
- **Server-side filters & automatic paging** — `--name` / `--fuzzy` /
  `--instance-id` / `--mode` / `--datastore-type` / `--vpc-id` /
  `--subnet-id` / `--tags` are real server-side query parameters; paging uses `--limit`
  (1~100) + `--offset` and is fetched automatically until `total_count` is
  reached. `--status` is a client-side filter (no such server parameter).
- **Offline-testable** — every code path (filters, paging, error
  classification, guard, SDK fallback, REST fallback + signing, rendering) is
  covered by unit tests that mock the hcloud subprocess, the SDK clients and
  the REST HTTP fetcher.

Out of scope: every mutating DDS action (create / delete / restart / resize /
backup / restore / upgrade / add-sharding-node / add-readonly-node / backup
management) and tag-based instance listing (`ListInstancesByTags`). Write
actions require a dedicated write-capable skill with explicit user
confirmation.

**Dependency**: Quality telemetry is collected automatically via
skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `python3 scripts/ensure_env.py` (or
   `pip install huaweicloudsdkcore huaweicloudsdkdds`) to enable the SDK
   fallback path. If both are missing, the REST fallback needs no extra
   package (standard library only).
2. **Active credential profile configured offline/out-of-band** — run the
   KooCLI configure command in your own terminal, or export
   `HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK` before starting the agent (add
   `HUAWEICLOUD_SDK_SECURITY_TOKEN` for temporary credentials).
   Never paste AK/SK into chat; the script never reads, echoes or stores
   secrets itself — authentication is delegated to the hcloud profile / SDK
   environment.
3. **project_id** — the KooCLI path resolves it from the credential profile
   automatically; pass `--project-id` to override. The SDK and REST fallbacks
   require it (`--project-id` or `HUAWEICLOUD_SDK_PROJECT_ID` /
   `HUAWEI_PROJECT_ID`), because the REST path is `/v3/{project_id}/instances`.
4. **IAM permission** — read-only `dds:instance:list` (alias
   `dds:instance:listAll`); least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
5. **Python 3.8+** (standard library only — argparse / json / subprocess /
   urllib / hmac).
6. **Outbound HTTPS** access to `dds.cn-north-4.myhuaweicloud.com`.
7. **Runtime dependency helper** — `python3 scripts/ensure_env.py`
   (`--check` = 只检查不安装, `--upgrade` = 强制升级).
- **skill-quality-cli** — ensured by `bash scripts/ensure_cli.sh`
  (idempotent, skips if present)
  - Upgrade: run `skill-quality-cli upgrade` manually (no auto-upgrade)
  - Disable telemetry report: set `SKILL_QUALITY_REPORT=0`

## Workflow

1. **Confirm the target region** (default `cn-north-4`).
2. **Confirm KooCLI readiness** (optional, read-only) by listing the active
   credential profile.
3. **Run the list script** with the desired output mode and filters.
4. **Read the result** — name list (default) for a compact inventory, table
   (状态/引擎版本/规格/节点数/模式 etc.) for humans, `--json` for downstream tooling.
5. **Handle the empty / error cases** per the Error Handling table below (the
   script prints an explicit hint for an empty region, 401/403, missing AK/SK,
   missing project_id, missing hcloud+SDK, and KooCLI `[USE_ERROR]`).

## Core Commands

> **⚠️ Mandatory: every hcloud command in this skill MUST be wrapped with
> `skill-quality-cli run --skill-name huawei-cloud-dds-list -- ` — bare hcloud
> calls are strictly forbidden.**

```bash
# Compact instance-name list (default)
python3 scripts/list_dds.py --region cn-north-4
python3 scripts/list_dds.py --names-only

# Fixed eight-column table (实例ID/名称/状态/引擎版本/规格/节点数/创建时间/模式)
python3 scripts/list_dds.py --table

# Raw JSON of every returned field
python3 scripts/list_dds.py --json

# Filters (server-side query parameters)
python3 scripts/list_dds.py --name dds-demo            # exact name match
python3 scripts/list_dds.py --name dds --fuzzy          # *-prefix fuzzy match
python3 scripts/list_dds.py --instance-id <your-instance-id>
python3 scripts/list_dds.py --mode Sharding             # 集群
python3 scripts/list_dds.py --mode ReplicaSet           # 副本集
python3 scripts/list_dds.py --mode Single               # 单节点
python3 scripts/list_dds.py --datastore-type DDS-Community
python3 scripts/list_dds.py --tags env=prod
python3 scripts/list_dds.py --vpc-id vpc-0001 --subnet-id subnet-0001

# Client-side status filter (the API has no server-side status param)
python3 scripts/list_dds.py --status normal

# Paging: page size 1~100 (default 100); pages are fetched automatically
python3 scripts/list_dds.py --limit 10 --offset 20
python3 scripts/list_dds.py --limit 10 --single-page    # exactly one page

# Explicit project override (otherwise resolved from the profile)
python3 scripts/list_dds.py --project-id <your-project-id>
```

Equivalent direct KooCLI commands (the script wraps exactly these calls, with
automatic offset paging):

```bash
skill-quality-cli run --skill-name huawei-cloud-dds-list -- hcloud DDS ListInstances --cli-region=cn-north-4 --limit=100 --offset=0
skill-quality-cli run --skill-name huawei-cloud-dds-list -- hcloud DDS ListInstances --cli-region=cn-north-4 --name=dds-demo
skill-quality-cli run --skill-name huawei-cloud-dds-list -- hcloud DDS ListInstances --cli-region=cn-north-4 --cli-mode=AKSK --mode=Sharding
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--names-only` | No | Output instance names only — **this is also the default mode** | — |
| `--table` | No | Output the fixed eight-column table (实例ID/名称/状态/引擎版本/规格/节点数/创建时间/模式) | — |
| `--json` | No | Output the raw instance array as JSON | — |
| `--name` | No | Filter by instance name — real server-side query parameter (exact unless prefixed with `*`) | `dds-demo` |
| `--fuzzy` | No | Fuzzy name match: forwards `*<name>` (server-side `*` prefix semantics) | used with `--name` |
| `--instance-id` | No | Filter by exact instance ID — real server-side query parameter | `<your-instance-id>` |
| `--mode` | No | Filter by instance type — real server-side query parameter (`Sharding`=集群 / `ReplicaSet`=副本集 / `Single`=单节点); the script also forwards `--cli-mode` to disambiguate the KooCLI system parameter | `ReplicaSet` |
| `--datastore-type` | No | Filter by DB type — real server-side query parameter (`DDS-Community` / `DDS-Enhanced`) | `DDS-Community` |
| `--vpc-id` | No | Filter by VPC ID — real server-side query parameter | `vpc-0001` |
| `--subnet-id` | No | Filter by subnet ID — real server-side query parameter | `subnet-0001` |
| `--tags` | No | Filter by instance tags — real server-side query parameter (`key1=value1,key2=value2`) | `env=prod` |
| `--status` | No | Filter by instance state — **client-side** (the API has no server-side status param): `normal` / `abnormal` / `creating` / `frozen` / ... | `normal` |
| `--limit` | No | Page size (default 100, server range 1–100; pages are fetched automatically) | `10` |
| `--offset` | No | Start offset (server parameter, default 0) | `20` |
| `--max-pages` | No | Maximum pages fetched automatically (default 50, loop guard) | `5` |
| `--single-page` | No | Fetch exactly one page (no further offsets) | — |
| `--project-id` | No | Project ID override (needed by the SDK / REST fallback paths) | `<your-project-id>` |

Output-mode precedence: `--json` → `--table` → default names list
(`--names-only` is an explicit synonym of the default).

## Write-Intent Guard

- The script scans all user arguments for mutating vocabulary (`create`,
  `delete`, `drop`, `update`, `modify`, `resize`, `scale`, `restart`,
  `reboot`, `restore`, `backup`, `freeze`, `unfreeze`, `release`,
  `terminate`, `destroy`, `upgrade`, `rollback`, `migrate`, `reset`,
  `attach`, `configure`, `kill`, and DDS operation names such as
  `CreateInstance`, `DeleteInstance`, `RestartInstance`, `ResizeInstance`,
  `BatchDeleteBackup`, `CreateManualBackup`).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`,
  and exits with code 1 **before** a single hcloud command is executed.
- Only **operation/option positions** are scanned. Values of read-only filter
  options (`--name`, `--instance-id`, `--vpc-id`, `--subnet-id`, `--tags`,
  `--status`, `--mode`, `--datastore-type`, `--project-id`, `--region`,
  `--limit`, `--offset`, `--max-pages`) are data, not commands, and are
  exempt: `--name create-me`, `--instance-id create-instance-01`,
  `--name checkpoint-demo` and `--name dds-copy-01` all pass. Matching itself
  is token-based (separator- and camelCase-split, whole words), so
  `CreateInstance`, `create_instance`, `--create-instance` and `StopInstance`
  are still rejected.
- Only `hcloud DDS ListInstances` (GET), the SDK `list_instances` call or the
  signed REST `GET /v3/{project_id}/instances` in the fallback paths is ever
  issued; there is no code path that can issue a mutating DDS API call.
- Status values that are legitimate DDS states (`creating`, `deleting`,
  `resizing`, `frozen`, ...) are not write intents and are **not** blocked.

## KooCLI Command Format Standard

```text
hcloud DDS ListInstances --cli-region=<region> [--key=value ...]
```

- **Service name** — `DDS` (a real KooCLI service, verified).
- **Operation name** — `ListInstances` (PascalCase).
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`.
- **Simple parameter** — `--key=value`, e.g. `--name=dds-demo`,
  `--id=<instance-id>`, `--mode=Sharding`, `--datastore_type=DDS-Community`,
  `--vpc_id=<id>`, `--subnet_id=<id>`, `--tags=env=prod`, `--limit=<1..100>`,
  `--offset=<n>`, `--project_id=<id>`. All are real server-side ListInstances parameters
  (verified against the KooCLI `DDS ListInstances` help output).
- **Name matching** — leading `*` = fuzzy, otherwise exact (`--fuzzy` adds it).
- **`mode` collision** — KooCLI has a system parameter `--mode` (authentication
  mode). When the API `mode` filter is used the script emits both
  `--cli-mode=<auth mode>` and `--mode=<value>`; KooCLI then treats `--cli-mode`
  as the system parameter and `--mode` as the API parameter. The auth mode
  defaults to `AKSK` and can be overridden with the `DDS_LIST_CLI_MODE`
  environment variable (set it to the active profile's mode, e.g. `SSO`).
- **No status parameter** — `--status` of this script is client-side.
- **Paging** — `--limit` (1~100; the server returns up to 100 per page when
  unset) + `--offset`; the script fetches pages automatically until the
  response `total_count` is reached.
- **REST path** — `GET /v3/{project_id}/instances`; KooCLI resolves the
  project_id from the credential profile, while the SDK / REST fallbacks need
  `--project-id` or the project-id environment variable.
- **REST signing** — the REST fallback uses AK/SK Signature V4
  (`SDK-HMAC-SHA256`, host + `X-Sdk-Date` + optional `X-Security-Token`).

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty instance list | Exit 0, prints `当前区域（<x>）无 DDS 实例` (+ active filters) |
| 403 / insufficient IAM permission | Exit 1, `无权限访问文档数据库服务（DDS），请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure credentials out-of-band (never in chat) |
| Missing project_id (SDK / REST fallback) | Exit 1, hint to pass `--project-id` or set the project-id env var |
| hcloud not installed | SDK fallback, then REST fallback; exit 1 only when all three tiers are unavailable, with install hints |
| KooCLI `[USE_ERROR] ...` (even with exit code 0) | Exit 1, explicit `hcloud 参数错误` hint pointing to `--help` |
| 401 / invalid AK-SK | Exit 1, explicit invalid/expired credential hint (never retries another identity) |
| Network / API failure | Exit 1 with the hcloud stderr / REST response excerpt |
| `--limit` / `--offset` / `--max-pages` out of range | Exit 1, explicit range error before any call |
| Invalid `--mode` / `--datastore-type` value | Exit 1, explicit value error before any call |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty region; `1` config, auth, guard, or API error.

## Edge Cases

| Scenario | Handling |
| ---------- | --------- |
| Non-`normal` instances (abnormal / creating / frozen / ...) | Reported with their state; `--status normal` hides them |
| Large instance count | Automatic `limit`/`offset` paging driven by `total_count` (max 100 per page, max 50 pages) |
| Multiple node groups with the same spec code | 规格 column lists each distinct `groups[].nodes[].spec_code` once, comma-joined (e.g. shard + mongos) |
| Node count | 节点数 = number of `groups[].nodes[]` entries (all groups summed); instances without `groups` render `-` |
| Field missing on an instance (e.g. no `groups`) | Rendered as `-` in the table |
| Empty instance list with `--table` | Table renders header + rule only (no crash) |
| CJK headers / values | Columns are padded by display width (`unicodedata.east_asian_width`), so the table stays aligned |
| Instance without a name | The name list falls back to `id` |
| Exact vs fuzzy name | `--name demo` is exact (server-side), `--name demo --fuzzy` sends `*demo` |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to the official DDS SDK list call, same output modes |
| hcloud and SDK both absent | REST fallback (`GET /v3/{project_id}/instances`, local AK/SK signing), same output modes and paging |
| User asks to create/delete/restart/resize/backup an instance | Out of scope — blocked by the write-intent guard; a write-capable skill with explicit user confirmation is required |

## Testing

Offline unit tests with a mocked hcloud subprocess, fake SDK clients and a
mocked REST fetcher (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / restart /
resize / backup / restore / upgrade / migrate / normalized variants /
operation positions still blocked / verb-named read-only filter values
(`--name create-me`, `--instance-id create-instance-01`) pass / operation
whitelist / status values not blocked), command construction
(service/operation names, real server-side filters forwarded, fuzzy `*`
prefix, paging params, no write flags ever), JSON extraction, failure
classification (missing AK/SK, 403, generic, `[USE_ERROR]` with rc=0),
offset paging (`total_count`-driven / short-page stop / empty / max-pages
guard), client-side status filter, SDK fallback (env credentials, missing
credentials, missing project id, pagination, request signature, auth error
mapping), REST fallback (URL + canonical query, deterministic AK/SK
signature, security token, pagination, filter forwarding, missing
credentials/project_id, error-body mapping, automatic SDK→REST hand-off),
rendering (fixed 8-column table over the official response shape (`created` +
`groups[].nodes[].spec_code` + node count), 模式映射 集群/副本集/单节点, missing
values as `-`, legacy `created_at`/`flavor[]` fallback, empty-input table, CJK
display-width alignment, name fallback to id) and all `main()`
output and error paths. SDK-specific tests run when the official SDK is
installed and skip otherwise.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy (`dds:instance:list`, alias `dds:instance:listAll`) |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI / skill-quality-cli installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its API provenance were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
