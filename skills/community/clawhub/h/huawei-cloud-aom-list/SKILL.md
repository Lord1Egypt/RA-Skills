---
name: huawei-cloud-aom-list
description: |
  1. Read-only Huawei Cloud **AOM (Application Operations Management)**
     management-plane name-list query, triggerable from natural language.
  2. Lists the *names* of 12 AOM resource categories: alarm rules (告警规则),
     alarm rule templates (告警规则模板), metric/event alarm rules
     (指标/事件告警规则), event-to-alarm rules (事件告警规则), action rules
     (行动规则), mute rules (静默规则), dashboards (仪表盘), dashboard folders
     (仪表盘分组), notification templates (通知模板), Prometheus instances
     (Prometheus 实例), access codes (接入码) and service-discovery rules
     (服务发现规则).
  3. Execution order: KooCLI (`hcloud AOM <Operation>`) first, then the
     official `huaweicloudsdkaom` v2 SDK, then a token-based REST GET fallback.
     A write-intent guard rejects every mutating intent before any command runs.
  4. Output: a table by default (the name field first), `--json` for the full
     payload, or `--names-only` for names only; stdout only.
  5. Explicitly OUT OF SCOPE: raw metric data points
     (`ListMetricItems` / `ShowMetricsData` / Prometheus `query` / `query_range`),
     log items (`ListLogItems`), the AOM CMDB detail lookups
     (`ShowAppByName` / `ShowComponentByName` / `ShowEnvByName` — no list
     endpoint), and every write operation.
  6. Triggers include: "查询AOM名称列表", "AOM 资源名称", "查询AOM告警规则",
     "AOM 告警规则模板", "AOM 指标告警规则", "AOM 事件告警规则", "AOM 行动规则",
     "AOM 静默规则", "AOM 监控看板列表", "AOM 监控看板分组", "AOM 通知模板",
     "AOM Prometheus 实例", "AOM 接入码", "AOM 服务发现规则", "AOM list",
     "AOM alarm rules", "AOM prometheus instances", "AOM notification templates".
     Every trigger carries an explicit AOM qualifier so the router never confuses
     AOM with the sibling CES / EPS management-plane query skill, whose
     alarm-rule / dashboard vocabulary overlaps.
  7. Offline unit tests (mocked hcloud / SDK) cover intent routing, the
     write-intent guard, output normalization, backend fallback and all output
     modes.
tags: [huawei-cloud, aom, monitoring, readonly, list]
---

# Huawei Cloud AOM Name-List Query

## Overview

List the **management-plane resource names** of Huawei Cloud AOM (Application
Operations Management) for a Huawei Cloud account / region. The skill covers 12
read-only name-list categories and can be driven either by an explicit
`--category` or by a **natural-language** `--query` string routed to one of the
categories.

Architecture:

```text
agent → python3 scripts/list_aom.py --query "<intent>" --category <c>
      → natural-language router (query → category)
      → write-intent guard (read-only enforcement)
      → execution:  hcloud AOM <Operation>            (CLI, primary)
                  → huaweicloudsdkaom v2              (SDK fallback)
                  → REST GET with X-Auth-Token         (token fallback)
      → normalized rows → name-first table / --names-only / --json stdout
```

Key properties:

- **Read-only by design** — every category maps to a single `list` read
  operation (verified against the SDK `_http_info` `resource_path`). A
  write-intent guard rejects create / update / delete / enable / disable /
  batch-* vocabulary before anything runs.
- **CLI first, SDK fallback, REST last** — KooCLI is attempted first; when the
  operation is not available or hcloud is absent, the skill falls back to the
  official SDK, then to a token-based REST GET.
- **Name-list oriented** — each category declares the response field that
  carries the human resource name; the table shows it first and `--names-only`
  prints just those names.
- **Capability boundary (out of scope, always refused)** — raw metric / log
  data and every write operation.

> **Dependency**: Quality telemetry is collected automatically via skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

## Query Categories

All 12 categories are served by `huaweicloudsdkaom` v2. The REST path is the
SDK `_http_info` `resource_path` verbatim.

| Category | Description | Name field | REST path (read) |
| -------- | ----------- | ---------- | ---------------- |
| `alarm-rules` | 告警规则列表 | `alarm_rule_name` | `GET /v2/{project_id}/alarm-rules` |
| `alarm-rule-templates` | 告警规则模板列表 | `alarm_rule_template_name` | `GET /v4/{project_id}/alarm-rules-template` |
| `metric-or-event-alarm-rules` | 指标/事件告警规则列表 | `alarm_rule_name` | `GET /v4/{project_id}/alarm-rules` |
| `event2alarm-rules` | 事件告警规则列表 | `name` | `GET /v2/{project_id}/event2alarm-rule` |
| `action-rules` | 行动规则列表 | `rule_name` | `GET /v2/{project_id}/alert/action-rules` |
| `mute-rules` | 静默规则列表 | `name` | `GET /v2/{project_id}/alert/mute-rules` |
| `dashboards` | 仪表盘列表 | `dashboard_title` | `GET /v2/{project_id}/aom/dashboards` |
| `dashboard-folders` | 仪表盘分组列表 | `folder_title` | `GET /v2/{project_id}/aom/dashboards-folder` |
| `notification-templates` | 通知模板列表 | `name` | `GET /v2/{project_id}/events/notification/templates` |
| `prom-instances` | Prometheus 实例列表 | `prom_name` | `GET /v1/{project_id}/aom/prometheus` |
| `access-codes` | 接入码列表 | `access_code` | `GET /v1/{project_id}/access-code` |
| `service-discovery-rules` | 服务发现规则列表 | `name` | `GET /v1/{project_id}/inv/servicediscoveryrules` |

> **AOM CMDB note (from Phase 2 research):** the AOM application-resource
> (CMDB) API family (`huaweicloudsdkaom` v3: applications / components /
> environments) exposes **no list endpoint** — only lookups by name or id
> (`ShowAppByName` / `ShowComponentByName` / `ShowEnvByName`). Those are
> detail queries, not name-list queries, so they are intentionally not part of
> this skill.

## Prerequisites

1. **Python 3.8+** with the Huawei Cloud SDK — run
   `python3 scripts/ensure_env.py` to install `huaweicloudsdkcore` and
   `huaweicloudsdkaom` automatically. See
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
2. **KooCLI (`hcloud`)** — optional primary execution path; see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   When absent, the SDK fallback is used.
3. **Credentials configured out-of-band** — the CLI reads the active hcloud
   profile; the SDK fallback reads AK/SK from the whitelisted environment
   variables (`HUAWEI_ACCESS_KEY` / `HUAWEI_SECRET_KEY`,
   `HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`, `HW_*`, ...). Never paste AK/SK
   into chat; the script never reads, echoes or stores secrets itself.
4. **IAM permission** — read-only AOM `list` actions (least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md)).
5. **Outbound HTTPS** access to `aom.<region>.myhuaweicloud.com`.
- **skill-quality-cli** — ensured by bash scripts/ensure_cli.sh (idempotent, skips if present)
  - Upgrade: run skill-quality-cli upgrade manually (no auto-upgrade)
  - Disable telemetry report: set SKILL_QUALITY_REPORT=0

## Workflow

> **Run `python3 scripts/ensure_env.py` FIRST.** Do this **before** any query,
> even the natural-language ones: without `huaweicloudsdkaom` installed the SDK
> fallback is unavailable, and any natural-language case that depends on it is
> skipped rather than executed. `ensure_env.py` is idempotent and only installs
> what is missing.

1. **Prepare the environment first (mandatory)** — `python3 scripts/ensure_env.py`
   installs `huaweicloudsdkcore` + `huaweicloudsdkaom` if any are missing. Run this
   as the very first step; otherwise a natural-language query whose CLI path is
   unavailable will find no SDK fallback and be skipped.
2. **Pick the query** — either the exact `--category`, or a natural-language
   `--query` that the router maps to a category.
3. **(Optional) confirm readiness** (read-only) — see the Core Commands block
   for the credential check, which is wrapped with `skill-quality-cli run`.
4. **Run the script** with `--region` (default `cn-north-4`) and, where the
   category supports it, `--name` / `--id` / `--prom-id` / `--type` filters.
5. **Read the result** — a name-first table by default, `--names-only` for names
   only, or `--json` for the full payload.
6. **Handle the empty / error cases** per the Error Handling table below.

## Core Commands

> **⚠️ Mandatory: every hcloud command in this skill MUST be wrapped with skill-quality-cli run --skill-name huawei-cloud-aom-list -- ** — bare hcloud calls are strictly forbidden.**

```bash
# Prepare the environment FIRST (idempotent; installs huaweicloudsdkaom if missing)
python3 scripts/ensure_env.py

# Natural-language query (Prometheus instances)
python3 scripts/list_aom.py --query "查询 Prometheus 实例列表" --region cn-north-4

# AOM-qualified natural-language query (disambiguated from the CES sibling skill)
python3 scripts/list_aom.py --query "查询AOM告警规则" --region cn-north-4 --names-only

# Explicit category (alarm rules), names only
python3 scripts/list_aom.py --category alarm-rules --region cn-north-4 --names-only

# Dashboards as JSON
python3 scripts/list_aom.py --category dashboards --region cn-north-4 --json

# List every supported category
python3 scripts/list_aom.py --list-categories

# Read-only credential readiness check (wrapped)
skill-quality-cli run --skill-name huawei-cloud-aom-list -- hcloud configure list
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `--query` / `-q` | One of `--query`/`--category` | Natural-language intent, routed to a category | `"查询AOM告警规则"` |
| `--category` | One of `--query`/`--category` | Exact query category | `alarm-rules` |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--json` | No | Emit full JSON instead of a table | `--json` |
| `--names-only` | No | Print only the resource names (one per line) | `--names-only` |
| `--name` | No | Server-side name filter | `prod-alarm` |
| `--id` / `-i` | No | Resource id (per category; e.g. alarm template / service discovery rule) | `<id>` |
| `--type` | No | Type filter (e.g. alarm template type) | `<type>` |
| `--prom-id` | No | Prometheus instance id filter | `<prom_id>` |
| `--prom-type` | No | Prometheus instance type filter | `<prom_type>` |
| `--enterprise-project-id` | No | Enterprise project id filter | `<eps_id>` |
| `--limit` / `--offset` | No | Paging — only `alarm-rules` and `metric-or-event-alarm-rules` accept `--limit`; `ListPromInstance` / `ListNotificationTemplates` do **not** accept `--limit` (the script drops unsupported params) | `--limit 50` |
| `--project-id` | No | Project id (needed by the REST fallback) | `<project_id>` |
| `--operation` | No | Explicit operation name (read-only whitelist enforced) | `ListAlarmRule` |
| `--list-categories` | No | Print every supported category | `--list-categories` |

## Natural-Language Routing

`--query` is lower-cased and matched (most specific phrase first) against the
category phrases. Examples:

| Query (excerpt) | Routed category |
| --------------- | --------------- |
| 查询AOM告警规则 / AOM 告警规则模板 / alarm template | `alarm-rule-templates` / `alarm-rules` |
| AOM 指标告警规则 / metric alarm rule | `metric-or-event-alarm-rules` |
| AOM 事件告警规则 / event to alarm | `event2alarm-rules` |
| AOM 告警规则 / AOM alarm rule | `alarm-rules` |
| AOM 行动规则 / action rule | `action-rules` |
| AOM 静默规则 / mute rule | `mute-rules` |
| AOM 监控看板分组 / 仪表盘分组 / dashboard folder | `dashboard-folders` |
| AOM 监控看板列表 / 仪表盘 / dashboard | `dashboards` |
| AOM 通知模板 / notification template | `notification-templates` |
| AOM Prometheus 实例 / prometheus instance | `prom-instances` |
| AOM 接入码 / access code | `access-codes` |
| AOM 服务发现规则 / service discovery rule | `service-discovery-rules` |

An unrecognized query is rejected and the full category list is printed.

> **Trigger disambiguation vs the sibling CES / EPS query skill:** this skill's
> external triggers always carry an explicit **AOM** qualifier (e.g. 查询AOM告警规则
> / AOM 监控看板列表) so an Agent router never confuses AOM with the CES
> (Cloud Eye) sibling, whose alarm-rule / dashboard vocabulary overlaps. Inside
> `--query`, the bare phrases (告警规则, 仪表盘, 看板, dashboard) still route
> correctly because routing only runs **after** this skill has been selected.

## Write-Intent Guard

- The guard scans the raw arguments for a curated mutating vocabulary (AOM
  write operation names such as `CreateAlarmRule`, `DeleteDashboard`,
  `CreatePromInstance`, plus generic verbs create / delete / update / enable /
  disable / import / upgrade, and the Chinese 创建 / 删除 / 修改 / 更新 / 启用 /
  停用 / 绑定 / 解绑 / 升级 / 导入 / 批量*).
- Only the read-only categories and operations are constructible. `--operation`
  is validated against each category's read operation.
- Any hit raises `GuardError`, prints
  `[错误] 检测到写操作意图 ... 已被守卫拦截`, and exits `1` **before** any
  command is executed.
- Values of read-only flags (notably the `--query` text) are not scanned for
  ordinary flag values, so a read query such as "查询服务发现规则" is never
  mistaken for a write.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — exact KooCLI service name: `AOM`.
- **Operation name** — PascalCase, e.g. `ListAlarmRule`, `ListPromInstance`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`.
- **Header parameters** — named with the API header casing, not snake_case, e.g.
  `--Enterprise-Project-Id=<eps>` (the AOM `enterprise_project_id` is a header).
- Some AOM operations may not be exposed by every KooCLI version; the script
  transparently falls back to the official SDK (`huaweicloudsdkaom` v2) in that
  case. The REST path in the category table is the SDK `_http_info`
  `resource_path` verbatim.

Concrete raw KooCLI commands (attempted first by the script; wrap with
`skill-quality-cli run` in production):

| Command | Purpose |
| ------- | ------- |
| `hcloud AOM ListAlarmRule --cli-region=cn-north-4 --limit=1` | 告警规则名称列表（`ListAlarmRule` 支持 `--limit`） |
| `hcloud AOM ListPromInstance --cli-region=cn-north-4 --Enterprise-Project-Id=<eps_id>` | Prometheus 实例名称列表（`ListPromInstance` 必填 `Enterprise-Project-Id` 且为 **header 形式**，**不接受** `--limit`） |
| `hcloud AOM ListNotificationTemplates --cli-region=cn-north-4 --Enterprise-Project-Id=<eps_id>` | 通知模板名称列表（`ListNotificationTemplates` 的 `Enterprise-Project-Id` 同为 header，**不接受** `--limit`） |

> **企业项目参数是 header，必须用 `--Enterprise-Project-Id`：** AOM 列表接口的
> `enterprise_project_id` 在 API 中定义为请求头 `Enterprise-Project-Id`（SDK
> `attribute_map` 亦如此），KooCLI 仅接受 header 形式。传 snake_case 的
> `--enterprise_project_id` 会被 KooCLI 拒绝（`[USE_ERROR]Invalid parameter`），
> 导致 CLI 主路径与 SDK-403 降级重试路径双双失效。脚本通过类别的
> `cli_param_names` 映射，在构建 `hcloud` 命令时把内部参数名
> `enterprise_project_id` 输出为 `--Enterprise-Project-Id`；凡声明该参数的类别
> （`alarm-rule-templates` / `metric-or-event-alarm-rules` / `dashboards` /
> `dashboard-folders` / `notification-templates` / `prom-instances`）一律如此。
>
> `--Enterprise-Project-Id` is optional only where the API documents it as
> optional; for `ListPromInstance` KooCLI requires it. So that the CLI path is
> always viable, the script **defaults `enterprise_project_id` to `0`** (the
> default enterprise project) for the `prom-instances` category when the caller
> omits `--enterprise-project-id`; an explicit value always wins. This keeps the
> Prometheus instance list on the CLI path (`ListPromInstance`) instead of
> silently degrading to the SDK, whose `aom:metric:list` action may be absent
> from the active credential. Additionally, when the SDK path fails with a
> permission-scoped `403` (`aom:metric:list` / `AOM.0403`), the script retries
> the read-only CLI path (with the header form) before hard-failing.

## Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| Empty result | Exit 0, prints `...：无数据。` |
| Unknown `--query` intent | Exit 1, `无法识别查询意图` + the category list |
| Missing AK/SK (SDK path) / hcloud not configured | Exit 1, `缺少 AK/SK 凭证` hint (never paste AK/SK in chat) |
| IAM 401/403 | Exit 1, `无权限访问 AOM，请检查 IAM 权限` hint |
| hcloud operation unsupported | Transparent fallback to the SDK |
| SDK `403` on a permission-scoped read action (`aom:metric:list` / `AOM.0403`) | Retry the read-only CLI path; only raise `AuthError` if that also fails |
| No backend available (no CLI, no SDK, no token) | Exit 1, `无可用执行后端` with the per-backend reasons |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty; `1` config, auth, guard or API error.

## Capability Boundary (Out of Scope)

This skill **never** queries raw metric / log data and **never** performs
writes:

- ❌ `ListMetricItems` / `ShowMetricsData` / Prometheus `query` / `query_range`
  — raw metric data points.
- ❌ `ListLogItems` — log data.
- ❌ AOM CMDB detail lookups (`ShowAppByName` / `ShowComponentByName` /
  `ShowEnvByName`) — no list endpoint.
- ❌ Any write: create / update / delete / enable / disable / batch-* on alarm
  rules, templates, dashboards, notification templates, Prometheus instances.

## Testing

Offline unit tests with a mocked hcloud subprocess and a mocked SDK (no
credentials, no network):

```bash
cd skills/monitoring/huawei-cloud-aom-list
python3 -m unittest discover -s tests -v
```

Coverage: natural-language routing, the write-intent guard (read passes / write
verbs and operation names blocked / `--query` value not scanned), category
registry integrity (12 categories), CLI command construction, hcloud output
parsing and failure classification, SDK request building + response
normalization via a fake loader, backend fallback (CLI→SDK→REST), rendering
(name-first table / names-only / empty) and all `main()` output modes.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy for AOM |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI + SDK installation, credential configuration and skill-quality-cli |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |