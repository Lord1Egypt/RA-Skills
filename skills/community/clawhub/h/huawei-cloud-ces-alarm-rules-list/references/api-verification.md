# API 核对结论 — huawei-cloud-ces-alarm-rules-list

本文件记录开发时对「告警规则列表 / 策略 / 资源 / 状态」四个只读接口的**实测核对**结果，
用来消除 Issue 正文与既有记录之间的路径差异。所有结论都来自本机实测，不是按命名推断。

## 1. KooCLI 操作存在性（hcloud 7.3.12）

```bash
hcloud CES --help | grep -E "ListAlarmRules|ListAlarmRulePolicies|ListAlarmRuleResources|ListAlarms"
```

Available Operations 中确实存在：

```
ListAlarmRules
ListAlarmRulePolicies
ListAlarmRuleResources
ListAlarms
```

## 2. ListAlarmRules 的真实参数（关键差异）

```bash
hcloud CES ListAlarmRules --help
```

`Method: GET`，`Params:` 只有：

| 参数 | 位置 | 说明 |
|------|------|------|
| `--cli-region` | - | 必填区域 |
| `--project_id` | path | 必填；缺省时由 profile 的 cli-project-id / 认证信息父项目解析 |
| `--alarm_id` | query | 规则 ID（al + 22 位），单条详情用 |
| `--name` | query | 规则名称（服务端精确匹配语义） |
| `--namespace` | query | 服务命名空间（service.item） |
| `--resource_id` | query | 规则中的资源 ID（多维度按字典序逗号分隔） |
| `--enterprise_project_id` | query | 企业项目 ID（`0` / `all_granted_eps`） |
| `--product_name` | query | 云产品名（如 `SYS.ECS,instance_id`） |
| `--resource_level` | query | `product` / `dimension` |
| `--limit` | query | 每页条数，范围 [1,100]，默认 10 |
| `--offset` | query | 分页偏移，范围 [0,10000]，默认 0 |

**没有** `--alarm_level` / `--alarm_state` / `--resource_type` 这三个 query 参数。
因此本 skill 的 `--alarm-level` / `--alarm-state` / `--resource-type` 是**客户端过滤**：
先按 `--limit` + `--offset` 翻完全量，再在本地筛选。

## 3. REST 路径（SDK `_http_info` 实测）

`huaweicloudsdkces` 3.1.220，`huaweicloudsdkces/v2/ces_client.py`：

```
_list_alarm_rules_http_info            -> GET /v2/{project_id}/alarms
_list_alarm_rule_policies_http_info    -> GET /v2/{project_id}/alarms/{alarm_id}/policies
_list_alarm_rule_resources_http_info   -> GET /v2/{project_id}/alarms/{alarm_id}/resources
```

`huaweicloudsdkces/v1/ces_client.py`：

```
_list_alarms_http_info                 -> GET /V1.0/{project_id}/alarms
```

**结论：告警规则列表的真实路径是 `/v2/{project_id}/alarms`，不是 `/v2/{project_id}/alarm-rules`。**
Issue 正文与既有 `skills/monitoring/huawei-cloud-ces-eps-query` 的记录
（`GET /v2/{project_id}/alarms`）一致；`/alarm-rules` 的写法在 KooCLI 7.3.12 与
SDK 3.1.220 中都查不到，属误记。本 skill 以实测为准。

## 4. 响应字段（决定表格列的口径）

`huaweicloudsdkces.v2.ListAlarmRulesResponse`：`alarms`（list）+ `count`（int）。

`ListAlarmRespBodyAlarms`：`alarm_id`、`name`、`description`、`namespace`、
`policies`、`resources`、`type`、`enabled`、`notification_enabled`、
`alarm_notifications`、`ok_notifications`、`notification_begin_time`、
`notification_end_time`、`effective_timezone`、`enterprise_project_id`、
`alarm_template_id`、`product_name`、`resource_level`、`tags`。

`PolicyResp`：`metric_name`、`period`、`filter`、`comparison_operator`、`value`、
`hierarchical_value{critical,major,minor,info}`、`unit`、`count`、
`suppress_duration`、`level`、`namespace`、`dimension_name`。

`ResourcesInListResp`：`resource_group_id`、`resource_group_name`、
`dimensions[{name,value}]`。

`NotificationResp`：`type`、`notification_list`。

**`alarm_state` 不在 v2 列表响应里**；它只出现在
`huaweicloudsdkces.v1.MetricAlarmsResp`（`ListAlarms`，`GET /V1.0/{project_id}/alarms`）。
因此 `--table` 的「当前状态」列与 `--alarm-state` 过滤依赖这一次额外的只读 v1 调用：
按 `--start`（上一条 alarm_id）+ `--limit` + `--order=asc` 翻页，建立
`alarm_id → alarm_state` 映射。该调用失败时：

- 未指定 `--alarm-state` → stderr 告警，状态列标注「未知」，主查询结果照常输出；
- 指定了 `--alarm-state` → 报错退出 1（过滤无法执行，不能给出看似正常的空结果）。

`ListAlarmRuleResourcesResponse.resources` 是**二维**结构
（`list[list[DimensionResp]]`，即按资源分组的维度数组），实现里按「资源组 → 维度列表」
展开，兼容一维/二维两种返回形态。

## 4.1 真实响应补充（cn-north-4 实测）

```bash
hcloud CES ListAlarmRules --cli-region=cn-north-4 --limit=1
hcloud CES ListAlarmRulePolicies --cli-region=cn-north-4 --alarm_id=<id> --limit=100
hcloud CES ListAlarmRuleResources --cli-region=cn-north-4 --alarm_id=<id> --limit=100
```

实测到四件影响输出口径的事实：

1. **`period` 单位是秒**（如 `300` = 5 分钟），不是分钟。表格/详情文案按「周期 %d 秒」输出。
2. **分级阈值规则会同时返回 `value` 与 `hierarchical_value`**（例如 `value: 80` +
   `hierarchical_value: {major: 80}`）。渲染时优先展示分级阈值，避免同一阈值打印两遍。
3. **`ListAlarmRuleResources` 的 `resources` 是二维结构**
   （`[[{"name": "rds_cluster_id", "value": "..."}]]`），内层一组即一组维度；
   而 `ListAlarmRules` 列表里的 `resources` 是
   `[{"dimensions": [{"name": "..."}]}]`（且列表视图常只给 `name`、不给 `value`）。
   实现按「资源组 → 维度列表」归一化，两种形态都能渲染。
4. **`alarm_notifications[].type` 实测取值是 `notification`**（不是 `SMN`），且
   `notification_list` 里是 `urn:smn:...` 主题。渲染直接使用接口返回值，不做枚举假设。

## 5. 分页语义

- `ListAlarmRules`：响应带 `count`（本次查询命中的总条数，实测 `--limit=1` 时 `count=1`），按 `offset += limit` 翻页；本 skill 在
  取满 `count`、遇到短页（`len(batch) < limit`）或空页时停止，`--max-pages` 兜底防死循环。
- `ListAlarms`（v1）：响应带 `meta_data{count,total,marker}`，按 `start=<last alarm_id>` 翻页；
  边界语义（是否含该 id）各区域不一致，实现按「本页无新增 alarm_id 即停止」兜底。

## 6. 级别的中文口径

`level`：1 紧急 / 2 重要 / 3 次要 / 4 提示（同时接受中文名作为 `--alarm-level` 入参）。

## 7. 状态的中文口径

`alarm_state`：`ok` 正常 / `alarm` 告警 / `insufficient_data` 数据不足 / `invalid` 无效。
`insufficient_data` **独立标注「数据不足」**，不得与「正常」混同（这是告警治理盘点的关键区分）。