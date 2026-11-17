---
name: huawei-cloud-ces-eps-query
description: |
  1. Read-only Huawei Cloud **management-plane** queries for CES (Cloud Eye)
     and EPS (Enterprise Project Service), triggerable from natural language.
  2. CES (7 query categories): alarm rules (告警规则), alarm histories
     (告警历史), alarm templates (告警模板), dashboards (仪表盘),
     notification masks (通知掩码), resource groups (资源分组),
     one-click alarms (一键告警).
  3. EPS (5 query categories): enterprise project list (企业项目列表),
     enterprise project detail (企业项目详情), enterprise project quotas
     (企业项目配额), resources bound to an enterprise project (绑定资源),
     migration records (迁移记录).
  4. Execution order: KooCLI (`hcloud CES|EPS <Operation>`) first, then the
     official `huaweicloudsdkces` v2 / `huaweicloudsdkeps` v1 SDK, then a
     token-based REST GET fallback. A write-intent guard rejects every
     mutating intent before any command runs.
  5. Explicitly OUT OF SCOPE: raw metric data points (`ShowMetricData` /
     `ListMetrics` / `BatchListMetricData`), service-level metric values
     (RDS / DCS / DMS / EVS / ELB ...), and every write operation
     (create / update / delete / enable / disable / migrate / batch-*).
  6. Triggers include: "查询告警规则", "告警历史", "告警模板", "仪表盘",
     "通知掩码", "资源分组", "一键告警", "企业项目列表", "企业项目详情",
     "企业项目配额", "企业项目绑定资源", "迁移记录", "CES query",
     "EPS query", "cloud eye", "enterprise project", "alarm rule list".
  7. Offline unit tests (mocked hcloud / SDK) cover intent routing, the
     write-intent guard, output normalization, backend fallback and all CLI
     output modes.
tags: [huawei-cloud, ces, eps, monitoring, readonly]
---

# Huawei Cloud CES / EPS Management-Plane Query

## Overview

Query the **management-plane metadata** of Huawei Cloud CES (Cloud Eye) and
EPS (Enterprise Project Service) for a Huawei Cloud account. The skill covers
12 read-only query categories and can be driven either by an explicit
`--category` or by a **natural-language** `--query` string that is routed to
one of the categories.

Architecture:

```text
agent → python3 scripts/ces_eps_query.py --query "<intent>" --category <c>
      → natural-language router (query → category)
      → write-intent guard (read-only enforcement)
      → execution:  skill-quality-cli run ─▶ hcloud CES|EPS <Operation>   (CLI, primary)
                  → huaweicloudsdkces v2 / huaweicloudsdkeps v1 (SDK fallback)
                  → REST GET with X-Auth-Token            (token fallback)
      → normalized rows → table / JSON stdout
```

Key properties:

- **Read-only by design** — every category maps to a single read operation
  (verified against the SDK `_http_info` `resource_path`). A write-intent guard
  rejects create / update / delete / enable / disable / migrate / batch-*
  vocabulary before anything runs. The only `POST` paths used
  (`notification-masks/batch-query`, `resources/filter`) are read **batch
  query** operations, never mutations.
- **CLI first, SDK fallback, REST last** — KooCLI is attempted first; when the
  operation is not available or hcloud is absent, the skill falls back to the
  official SDK, then to a token-based REST GET.
- **Natural-language triggerable** — `--query "查询企业项目绑定资源"` routes to
  `eps-resources`; unknown intents are rejected with the list of categories.
- **Capability boundary (out of scope, always refused)** — raw metric data
  points (`ShowMetricData` / `ListMetrics` / `BatchListMetricData`),
  service-level metric values (RDS / DCS / DMS / EVS / ELB ...), and every
  write operation.

> **Dependency**: Quality telemetry is collected automatically via skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

## Query Categories

### CES — 7 categories (`huaweicloudsdkces` v2)

| Category | Description | SDK method | REST path (read) |
| ---------- | ----------- | ---------- | ---------------- |
| `alarm-rules` | 告警规则列表 | `list_alarm_rules` | `GET /v2/{project_id}/alarms` |
| `alarm-histories` | 告警历史列表 | `list_alarm_histories` | `GET /v2/{project_id}/alarm-histories` |
| `alarm-templates` | 告警模板列表 | `list_alarm_templates` | `GET /v2/{project_id}/alarm-templates` |
| `dashboards` | 仪表盘列表 | `list_dashboard_infos` | `GET /v2/{project_id}/dashboards` |
| `notification-masks` | 通知掩码列表 | `list_notification_masks` | `POST /v2/{project_id}/notification-masks/batch-query` (read) |
| `resource-groups` | 资源分组列表 | `list_resource_groups` | `GET /v2/{project_id}/resource-groups` |
| `one-click-alarms` | 一键告警列表 | `list_one_click_alarms` | `GET /v2/{project_id}/one-click-alarms` |

### EPS — 5 categories (`huaweicloudsdkeps` v1)

| Category | Description | SDK method | REST path (read) |
| ---------- | ----------- | ---------- | ---------------- |
| `eps-projects` | 企业项目列表 | `list_enterprise_project` | `GET /v1.0/enterprise-projects` |
| `eps-project-detail` | 企业项目详情 (needs `--id`) | `show_enterprise_project` | `GET /v1.0/enterprise-projects/{enterprise_project_id}` |
| `eps-quotas` | 企业项目配额 | `show_enterprise_project_quota` | `GET /v1.0/enterprise-projects/quotas` |
| `eps-resources` | 企业项目绑定资源 (needs `--id`) | `show_resource_bind_enterprise_project` | `POST /v1.0/enterprise-projects/{enterprise_project_id}/resources/filter` (read) |
| `eps-migration-records` | 企业项目迁移记录 | `list_migration_record` | `GET /v1.0/enterprise-projects/migrate-record/list` |

## Prerequisites

1. **Python 3.8+** with the Huawei Cloud SDK — run
   `python3 scripts/ensure_env.py` to install `huaweicloudsdkcore`,
   `huaweicloudsdkces` and `huaweicloudsdkeps` automatically. See
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
2. **KooCLI (`hcloud`)** — optional primary execution path; see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   When absent, the SDK fallback is used.
3. **Credentials configured out-of-band** — the CLI reads the active hcloud
   profile; the SDK fallback reads AK/SK from the whitelisted environment
   variables (`HUAWEI_ACCESS_KEY` / `HUAWEI_SECRET_KEY`,
   `HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`, `HW_*`, ...). Never paste AK/SK
   into chat; the script never reads, echoes or stores secrets itself.
4. **IAM permission** — read-only CES / EPS actions (least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md)).
5. **Outbound HTTPS** access to `ces.<region>.myhuaweicloud.com` and
   `eps.<region>.myhuaweicloud.com`.
- **skill-quality-cli** — ensured by bash scripts/ensure_cli.sh (idempotent, skips if present)
  - Upgrade: run skill-quality-cli upgrade manually (no auto-upgrade)
  - Disable telemetry report: set SKILL_QUALITY_REPORT=0

## Workflow

1. **(Optional) prepare the environment** — `python3 scripts/ensure_env.py`
   installs any missing SDK dependency.
2. **Pick the query** — either the exact `--category`, or a natural-language
   `--query` that the router maps to a category.
3. **(Optional) confirm readiness** (read-only) — see the Core Commands block
   for the credential check, which is wrapped with `skill-quality-cli run`.
4. **Run the script** with `--region` (default `cn-north-4`) and, where the
   category needs it, `--id` (enterprise project id / alarm id / group id).
5. **Read the result** — a table by default, or `--json` for the full payload.
6. **Handle the empty / error cases** per the Error Handling table below.

## Core Commands

> **⚠️ Mandatory quality wrapping: `scripts/ces_eps_query.py` builds every `hcloud` CLI call as `skill-quality-cli run --skill-name huawei-cloud-ces-eps-query -- hcloud ...` (enforced in code, not left to the agent). If `skill-quality-cli` is unavailable (run `bash scripts/ensure_cli.sh`) or `SKILL_QUALITY_REPORT=0`, the CLI path degrades to bare `hcloud` (no telemetry) — the read-only semantics and the CLI→SDK→REST fallback are unchanged.**

```bash
# Natural-language query example (CES alarm rules)
python3 scripts/ces_eps_query.py --query "查询告警规则" --region cn-north-4

# Explicit category (CES), JSON output
python3 scripts/ces_eps_query.py --category alarm-rules --region cn-north-4 --json

# EPS enterprise project list
python3 scripts/ces_eps_query.py --category eps-projects --region cn-north-4

# EPS enterprise project detail (needs an enterprise project id)
python3 scripts/ces_eps_query.py --category eps-project-detail --id <enterprise_project_id>

# EPS resources bound to an enterprise project
python3 scripts/ces_eps_query.py --query "查询企业项目绑定资源" --id <enterprise_project_id>

# List every supported category
python3 scripts/ces_eps_query.py --list-categories
```

Equivalent direct KooCLI command (attempted first by the script):

```bash
skill-quality-cli run --skill-name huawei-cloud-ces-eps-query -- hcloud CES ListAlarmRules --cli-region=cn-north-4 --limit=50
skill-quality-cli run --skill-name huawei-cloud-ces-eps-query -- hcloud EPS ListEnterpriseProject --cli-region=cn-north-4 --limit=50

# Read-only credential readiness check (also wrapped)
skill-quality-cli run --skill-name huawei-cloud-ces-eps-query -- hcloud configure list
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--query` / `-q` | One of `--query`/`--category` | Natural-language intent, routed to a category | `"查询企业项目配额"` |
| `--category` | One of `--query`/`--category` | Exact query category | `alarm-rules` |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--id` / `-i` | For `eps-project-detail` / `eps-resources` / `*-detail` | Resource id (enterprise project / alarm / group / template), interpreted per category | `<enterprise_project_id>` |
| `--name` | No | Server-side name filter | `prod-alarm` |
| `--resource-id` | No | Server-side resource id filter (CES) | `<resource_id>` |
| `--limit` | No | Page size (default 50) | `100` |
| `--offset` | No | Page offset (default 0) | `50` |
| `--json` | No | Emit full JSON instead of a table | `--json` |
| `--operation` | No | Explicit operation name (read-only whitelist enforced) | `ListAlarmRules` |
| `--list-categories` | No | Print every supported category | `--list-categories` |

## Natural-Language Routing

`--query` is lower-cased and matched (most specific phrase first) against the
category phrases. Examples:

| Query (excerpt) | Routed category |
| --------------- | --------------- |
| 告警规则 / alarm rule | `alarm-rules` |
| 告警历史 / alarm history | `alarm-histories` |
| 告警模板 / alarm template | `alarm-templates` |
| 仪表盘 / dashboard | `dashboards` |
| 通知掩码 / notification mask | `notification-masks` |
| 资源分组 / resource group | `resource-groups` |
| 一键告警 / one-click alarm | `one-click-alarms` |
| 企业项目详情 / enterprise project detail | `eps-project-detail` |
| 企业项目配额 / quota | `eps-quotas` |
| 绑定资源 / bound resource | `eps-resources` |
| 迁移记录 / migration record | `eps-migration-records` |
| 企业项目 / enterprise project | `eps-projects` |

An unrecognized query is rejected and the full category list is printed.

## Write-Intent Guard

- The guard scans the raw arguments for a curated mutating vocabulary (CES/EPS
  write operation names such as `CreateAlarm`, `DeleteAlarmRule`,
  `MigrateResource`, plus generic verbs create / delete / update / enable /
  disable / associate, and the Chinese 创建 / 删除 / 修改 / 更新 / 启用 / 停用 /
  绑定 / 解绑 / 迁移资源 / 批量*).
- Only the read-only categories and operations are constructible. `--operation`
  is validated against each category's read operation.
- Any hit raises `GuardError`, prints
  `[错误] 检测到写操作意图 ... 已被守卫拦截`, and exits `1` **before** any
  command is executed.
- Values of read-only flags (notably the `--query` text) are not scanned for
  generic verbs, so a read query such as "查询迁移记录" is never mistaken for a
  migration write.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI title-case service name: `CES` or `EPS`.
- **Operation name** — PascalCase, e.g. `ListAlarmRules`,
  `ListEnterpriseProject`, `ShowEnterpriseProject`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`.
- **Simple parameter** — `--key=value`, e.g. `--limit=50`, `--group_id=<id>`.
- Some CES/EPS management operations may not be exposed by every KooCLI
  version; the script transparently falls back to the official SDK
  (`huaweicloudsdkces` v2 / `huaweicloudsdkeps` v1) in that case. The REST path
  in the category table is the SDK `_http_info` `resource_path` verbatim.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty result | Exit 0, prints `...：无数据。` |
| Unknown `--query` intent | Exit 1, `无法识别查询意图` + the category list |
| Missing `--id` for a category that needs one | Exit 1, `缺少必填参数 --id` |
| Missing AK/SK (SDK path) / hcloud not configured | Exit 1, `缺少 AK/SK 凭证` hint (never paste AK/SK in chat) |
| IAM 401/403 | Exit 1, `无权限访问 CES/EPS，请检查 IAM 权限` hint |
| hcloud operation unsupported | Transparent fallback to the SDK |
| No backend available (no CLI, no SDK, no token) | Exit 1, `无可用执行后端` with the per-backend reasons |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty; `1` config, auth, guard or API error.

## Capability Boundary (Out of Scope)

This skill **never** queries raw metric data points or service-level metric
values, and **never** performs writes:

- ❌ `ShowMetricData` / `ListMetrics` / `BatchListMetricData` — raw metric data
  points. Use a dedicated metric-data skill.
- ❌ Service-level metric values (RDS / DCS / DMS / EVS / ELB ...).
- ❌ Any write: create / update / delete / enable / disable / migrate /
  batch-* on alarms, templates, dashboards, masks, groups, enterprise projects.

## Testing

Offline unit tests with a mocked hcloud subprocess and a mocked SDK (no
credentials, no network):

```bash
cd skills/monitoring/huawei-cloud-ces-eps-query
python3 -m unittest discover -s tests -v
```

Coverage: natural-language routing, the write-intent guard (read passes /
write verbs and operation names blocked / `--query` value not scanned),
category registry integrity (12 categories = CES 7 + EPS 5), CLI command
construction, the skill-quality-cli wrapper (wrapped / bare fallback / report
toggle / binary override), hcloud output parsing and failure classification, SDK
request building + response normalization via a fake loader, backend fallback
(CLI→SDK→REST), rendering and all `main()` output modes; plus offline tests for
the helper scripts `ensure_env.py` and `yaml-check-frontmatter.py`.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy for CES / EPS |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI + SDK installation, credential configuration and skill-quality-cli |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |