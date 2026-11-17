---
name: huawei-cloud-ces-alarm-rules-list
description: |
  1. 华为云 CES（云监控）告警规则只读盘点：主路径
     `hcloud CES ListAlarmRules --cli-region=<region>`（GET /v2/{project_id}/alarms），hcloud 缺失时
     回退官方 SDK `huaweicloudsdkces` v2。
  2. 单条规则详情（`--rule-id`）：`ListAlarmRules --alarm_id` +
     `ListAlarmRulePolicies`（阈值策略）+ `ListAlarmRuleResources`（关联资源）+
     通知对象，用于告警治理逐一核查。
  3. 三种输出：默认规则名称列表；`--table` 输出
     规则ID·名称·资源类型·监控维度·指标·阈值与比较符·告警级别·当前状态·是否启用·通知方式；
     `--json` 输出接口原始结构。
  4. 四类过滤：`--name`（服务端透传 + 客户端模糊）、`--alarm-level`（1 紧急~4 提示）、
     `--alarm-state`（ok/alarm/insufficient_data/invalid）、`--resource-type`；
     后三者在 KooCLI 7.3.12 的 ListAlarmRules 中没有对应 query 参数，翻全量后客户端过滤。
  5. `--limit` 1~100 + `--offset` 自动翻页（`--max-pages` 上限保护），区域默认 cn-north-4；
     当前告警状态由 v1 `ListAlarms` 只读补齐（v2 列表响应无 alarm_state），
     `insufficient_data` 独立标注「数据不足」，不与「正常」混同。
  6. 内置写意图守卫：create / update / delete / enable / disable / batch- / add / remove
     等意图在任何命令执行前拒绝，退出码 1；本 skill 严格只读。
  7. 触发词：「告警规则盘点」「查询CES告警规则」「告警规则列表」「告警阈值策略」
     「告警规则详情」「ces alarm rules list」「alarm rule inventory」「告警治理盘点」。
  8. 离线单元测试（mock hcloud / SDK）覆盖守卫、翻页、状态补齐、四类过滤、
     三种输出形态、单条详情、错误分类与后端回退。
tags: [huawei-cloud, ces, alarm-rules, monitoring, readonly]
---

# 华为云 CES 告警规则盘点（只读）

## Overview

盘点指定区域的 CES（Cloud Eye，云监控）告警规则，并支持查看单条规则的详情
（阈值策略 + 关联资源 + 通知对象），支撑告警治理盘点。

架构：

```text
agent → python3 scripts/ces_alarm_rules.py [--table|--json|--rule-id]
      → 写意图守卫（只读强制）
      → skill-quality-cli ─▶ hcloud CES ListAlarmRules            (CLI，主路径)
                          cli: ListAlarmRulePolicies     (单条详情：阈值策略)
                          cli: ListAlarmRuleResources    (单条详情：关联资源)
                          cli: ListAlarms                (v1，状态补齐)
      → huaweicloudsdkces v2/v1                                  (hcloud 缺失时回退)
      → 归一化 + 客户端过滤 → 名称列表 / 表格 / 原始 JSON
```

关键性质：

- **严格只读** — 只构造四个 GET 操作；写意图守卫在参数解析后、任何命令执行前拦截
  create / update / delete / enable / disable / batch- / add / remove 等意图，退出码 1。
- **CLI 优先、SDK 回退** — KooCLI 可用时走 CLI（经 `skill-quality-cli` 包裹）；
  KooCLI 缺失时回退官方 SDK。凭据始终由 CLI profile / SDK 环境变量提供，脚本不处理密钥。
- **口径以实测为准** — 规则列表路径是 `GET /v2/{project_id}/alarms`（不是
  `/alarm-rules`）；`ListAlarmRules` 没有 `alarm_level` / `alarm_state` / `resource_type`
  参数；告警状态只在 v1 `ListAlarms` 响应里。核对过程见
  [references/api-verification.md](references/api-verification.md)。
- **状态不做近似** — `insufficient_data` 独立显示为「数据不足」，绝不与「正常」合并。

> **Dependency**：质量遥测经 skill-quality-cli 自动上报（缺失时由 `scripts/ensure_cli.sh` 安装）。

> **能力边界**：本 skill 只做**规则定义与状态盘点**，不做任何变更，也不查询指标数据点
> （`ShowMetricData` / `ListMetrics`）、告警历史、模板、通知掩码、资源分组、一键告警。
> 变更操作需要单独 skill 并由用户显式确认。

## Prerequisites

1. **KooCLI（`hcloud`）** — 主执行路径，见
   [references/cli-installation-guide.md](references/cli-installation-guide.md)；
   缺失时自动回退 SDK（实测 KooCLI 7.3.12）。
2. **Python 3.8+** 与官方 SDK — `python3 scripts/ensure_env.py` 自动安装
   `huaweicloudsdkcore` 与 `huaweicloudsdkces`（实测 3.1.220）；渲染本身只用标准库。
3. **凭据带外配置** — CLI 读取 hcloud profile；SDK 回退读取白名单环境变量
   （`HUAWEICLOUD_SDK_AK` / `HUAWEI_ACCESS_KEY` …）并需要 project id
   （`CES_ALARM_PROJECT_ID` / `HUAWEICLOUD_SDK_PROJECT_ID`）。
   **绝不在对话中粘贴 AK/SK**，脚本不读取、不回显、不存储密钥。
4. **IAM 最小授权** — `ces:alarms:list`（列表）、`ces:alarms:getPolicies`、
   `ces:alarms:getResources`；策略见 [references/iam-policies.md](references/iam-policies.md)。
5. **出网 HTTPS** 访问 `ces.<region>.myhuaweicloud.com`；默认区域 `cn-north-4`。
6. **skill-quality-cli** — `bash scripts/ensure_cli.sh`（幂等）；关闭遥测
   `SKILL_QUALITY_REPORT=0`。

## Workflow

1. （可选）`python3 scripts/ensure_env.py` 补齐 SDK 依赖。
2. 决定形态：列表盘点（默认）/ `--table` / `--json` / 单条详情（`--rule-id`）。
3. 选定过滤：`--name`、`--alarm-level`、`--alarm-state`、`--resource-type`。
4. 运行脚本，指定 `--region`（默认 `cn-north-4`）与 `--limit`（1~100）。
5. 读结果：名称列表 / 表格 / 原始 JSON；空结果有明确提示。
6. 按下方 Error Handling 处理空、403、缺凭据、`[USE_ERROR]` 四类异常。

## Core Commands

> **⚠️ 强制质量包裹**：`scripts/ces_alarm_rules.py` 在代码里把每次 hcloud 调用构造为
> `skill-quality-cli run --skill-name huawei-cloud-ces-alarm-rules-list -- hcloud ...`。
> 遥测 CLI 不可用（先跑 `bash scripts/ensure_cli.sh`）或 `SKILL_QUALITY_REPORT=0` 时
> 降级为裸 `hcloud`，只读语义与 CLI→SDK 回退不变。

```bash
# 默认：规则名称列表
python3 scripts/ces_alarm_rules.py --region cn-north-4

# 全字段表格（10 列，验收口径）
python3 scripts/ces_alarm_rules.py --table

# 原始 JSON 结构
python3 scripts/ces_alarm_rules.py --json

# 过滤：名称模糊 / 级别 / 状态 / 资源类型
python3 scripts/ces_alarm_rules.py --name cpu --alarm-level 1,2 --table
python3 scripts/ces_alarm_rules.py --alarm-state 数据不足 --table
python3 scripts/ces_alarm_rules.py --resource-type SYS.ECS --table

# 单条规则详情（阈值策略 + 关联资源 + 通知对象）
python3 scripts/ces_alarm_rules.py --rule-id alxxxxxxxxxxxxxxxxxxxxxx
python3 scripts/ces_alarm_rules.py --rule-id alxxxxxxxxxxxxxxxxxxxxxx --json

# 只读凭据就绪检查（同样包裹）
skill-quality-cli run --skill-name huawei-cloud-ces-alarm-rules-list -- hcloud configure list
```

等价的直接 KooCLI 命令（脚本按需自动翻页）：

```bash
hcloud CES ListAlarmRules --cli-region=cn-north-4 --limit=100 --offset=0
hcloud CES ListAlarmRules --cli-region=cn-north-4 --alarm_id=<alarm_id> --limit=1
hcloud CES ListAlarmRulePolicies --cli-region=cn-north-4 --alarm_id=<alarm_id> --limit=100
hcloud CES ListAlarmRuleResources --cli-region=cn-north-4 --alarm_id=<alarm_id> --limit=100
hcloud CES ListAlarms --cli-region=cn-north-4 --limit=100 --order=asc     # 状态补齐（v1）
```

## Parameter Confirmation

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--region` / `-r` | 否 | 目标区域（默认 `cn-north-4`） | `cn-south-1` |
| `--rule-id` | 否 | 单条告警规则 ID（al + 22 位），输出该规则详情 | `al1111…` |
| `--name` | 否 | 规则名称：先作服务端 `name` 透传，再做客户端模糊匹配（含 alarm_id） | `cpu` |
| `--alarm-level` | 否 | 告警级别过滤（1 紧急 / 2 重要 / 3 次要 / 4 提示；可逗号分隔或重复）**客户端过滤** | `1,2` |
| `--alarm-state` | 否 | 状态过滤（`ok`/`alarm`/`insufficient_data`/`invalid` 或中文名）**客户端过滤** | `insufficient_data` |
| `--resource-type` | 否 | 资源类型/维度名子串（匹配 namespace、product_name、维度名）**客户端过滤** | `SYS.ECS` |
| `--limit` | 否 | 每页条数，范围 1~100（默认 50，自动翻页） | `100` |
| `--offset` | 否 | 起始分页偏移（默认 0） | `100` |
| `--max-pages` | 否 | 自动翻页上限（默认 100，防死循环） | `20` |
| `--table` | 否 | 输出 10 列全字段表格 | `--table` |
| `--json` | 否 | 输出接口原始 JSON 结构 | `--json` |

`--table` 与 `--json` 互斥使用（同时给出时以 `--json` 为先，脚本先判断 `--json`）。

## 客户端过滤说明（为什么不服务端过滤）

`hcloud CES ListAlarmRules --cli-region=<region> --help`（7.3.12）的 query 参数只有 `alarm_id`、`name`、
`namespace`、`resource_id`、`enterprise_project_id`、`product_name`、`resource_level`、
`limit`、`offset`，**没有** `alarm_level` / `alarm_state` / `resource_type`。
因此：

- `--name` → 先作服务端 `--name` 透传（服务端是精确匹配），再在客户端做子串匹配；
  透传后一条都没有时自动去掉该参数重取一次再做模糊过滤，避免子串查询被服务端静默过滤成空；
- `--alarm-level` → 取每条规则 `policies[].level` 与目标级别集合求交集；
- `--alarm-state` → 取 v1 `ListAlarms` 补齐的 `alarm_state` 映射比对；
- `--resource-type` → 匹配 `namespace` / `product_name` / `resources[].dimensions[].name`；
- 三者都需要**先翻全量**，`--max-pages` 是上限保护（触顶报错而非静默截断）。

## 当前状态从哪来

v2 `ListAlarmRules` 的响应**不含** `alarm_state`；状态只能从 v1 `ListAlarms`
（`GET /V1.0/{project_id}/alarms`）逐页补齐（`--start` + `--limit` + `--order=asc`）。
只在需要状态时（`--table` / `--json` / `--alarm-state`）才发起该额外只读调用：

- 调用失败且未指定 `--alarm-state` → stderr 告警，状态列显示「未知」，主结果照常输出；
- 调用失败且指定了 `--alarm-state` → 退出 1（过滤无法执行，不返回看似正常的空结果）。

## Write-Intent Guard

- 守卫扫描原始参数（剔除只读取值类旗标的取值，如 `--name` / `--rule-id` /
  `--alarm-state` 的值）并校验操作名，命中变更词汇即拒绝：
  `create` / `update` / `delete` / `modify` / `enable` / `disable` / `batch` / `add` /
  `remove`，以及 `CreateAlarmRules`、`UpdateAlarmRulePolicies`、`DeleteAlarm`、
  `BatchEnableAlarmRules`、`AddAlarmRuleResources` 等具体操作名（分隔符归一化后匹配）。
- 命中即打印 `[错误] 检测到写操作意图 … 已被守卫拦截，未执行任何命令。`，退出码 1，
  **在任何 hcloud 调用之前**。
- 只允许 `ListAlarmRules` / `ListAlarmRulePolicies` / `ListAlarmRuleResources` /
  `ListAlarms`（全部 GET），代码里没有构造写操作的通路。

## KooCLI 命令格式规范

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- Service：`CES`；Operation：PascalCase（`ListAlarmRules` 等）。
- 区域：必须 `--cli-region=<region>`。
- 简单参数：`--key=value`，如 `--limit=100`、`--offset=0`、`--alarm_id=<id>`、
  `--order=asc`（v1 `ListAlarms` 用 `--start`）。
- REST 路径（SDK `_http_info` 实测）：`/v2/{project_id}/alarms`、
  `/v2/{project_id}/alarms/{alarm_id}/policies`、
  `/v2/{project_id}/alarms/{alarm_id}/resources`、`/V1.0/{project_id}/alarms`。

## Error Handling

| 场景 | 行为 |
|------|------|
| 空列表 | 退出 0，打印 `Region <x> 无 CES 告警规则（过滤条件: …）。` |
| 单条规则不存在 | 退出 0，打印 `未找到告警规则 <id>（请核对 --rule-id 与区域）。` |
| 403 / 缺最小授权 | 退出 1，提示 `ces:alarms:list` / `ces:alarms:getPolicies` / `ces:alarms:getResources`，指向 IAM 文档；错误信封即使在 stdout + 退出码 0 也会被识别 |
| 缺 AK/SK 或凭据未配置 | 退出 1，提示带外配置（KooCLI configure 或凭证环境变量），**不索要 AK/SK** |
| hcloud 未安装 | 回退 SDK；SDK 也缺失时退出 1，提示 `python3 scripts/ensure_env.py` |
| KooCLI `[USE_ERROR]` | 退出 1，截取原文关键行 + `hcloud CES <Operation> --help` 核对建议 |
| 翻页触顶 `--max-pages` | 退出 1，明确报告未取完（不静默截断） |
| `--limit` 越界 / `--offset` 负数 / 非法级别或状态取值 | 退出 1，给出合法范围 |
| 写意图 | 退出 1，守卫消息，未执行任何命令 |

退出码：`0` 成功或空结果；`1` 守卫、配置、鉴权、参数或接口错误。

## Edge Cases

| 场景 | 处理 |
|------|------|
| 规则有多条策略（多指标/多级别） | 指标、维度、阈值、级别按策略聚合展示（`；` 分隔） |
| 分级阈值 `hierarchical_value` | 渲染为 `紧急>90/重要>80/…`，与单值阈值同样输出 |
| 规则未开启通知 | 通知方式显示「未开启通知」；`notification_enabled=false` 时同样处理 |
| 规则停用 | 是否启用列显示「停用」 |
| 状态未知 | 显示「未知」，并在 stderr 说明状态补齐失败原因 |
| 资源分组返回一维或二维维度结构 | 统一按「资源组 → 维度列表」展开 |
| 字段缺失 | 渲染为 `-` |
| 同时给 `--table` 与 `--json` | 以 `--json` 优先 |
| 用户要求创建/修改/删除告警规则 | 超出范围 — 守卫拦截；变更需要单独 skill 且用户显式确认 |

## Testing

离线单元测试（mock hcloud / SDK，无凭据无网络），在 skill 目录执行：

```bash
python3 -m unittest discover -s tests -v
```

本机还执行过一次真实只读冒烟（`--limit` / `--table` / `--alarm-state` / `--rule-id`，
全部 GET，不产生云资源），据此修正了 `period` 单位（秒）、分级阈值重复打印与详情接口
`resources` 二维结构三处口径。

覆盖：写意图守卫、命令构造、JSON/错误信封、offset 翻页与 `--max-pages`、
v1 状态补齐（含 `insufficient_data` 独立标注）、四类客户端过滤、三种输出形态、
单条详情（策略/资源/通知）、SDK 回退（含缺 AK/SK、缺 project id、凭据错误不回退）、
skill-quality-cli 包裹行为。详见
[references/verification-method.md](references/verification-method.md)。

## Reference Documents

| 文档 | 内容 |
|------|------|
| [references/api-verification.md](references/api-verification.md) | 接口、参数、路径、响应字段的实测核对结论（含 `/alarms` vs `/alarm-rules`） |
| [references/iam-policies.md](references/iam-policies.md) | 最小只读 IAM 策略（真实 action 名） |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI / SDK 安装、凭据与 skill-quality-cli |
| [references/verification-method.md](references/verification-method.md) | 接口核对、离线单测、mock 冒烟与遗留项 |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid 数据流图 |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Issue #139 验收标准对照 |