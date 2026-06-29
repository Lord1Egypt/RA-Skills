---
name: alarm-correlation-engine
description: 华为云 AOM 告警关联分析技能，支持查询 active/history 告警、当前活跃告警、告警去重归并、严重级别分组、突发/常态告警识别，以及告警规则查询、创建、修改、删除、动作规则和静默规则核对。
---

# 华为云 AOM 告警关联分析

华为云 AOM 告警关联分析技能，用于把 CCE 相关告警从原始事件流整理成可行动的告警线索。核心原则是同时考虑 active 和 history，避免漏掉已经恢复但影响诊断的资源类告警。

## ⛔ 安全约束

### 告警规则变更二次确认机制

> **本技能允许查询、创建、修改和删除 AOM 告警规则，并支持删除 AOM 通知动作规则；其中创建、修改和删除类操作必须携带 `confirm=true` 才会真正执行，否则仅返回预览和确认提示。**

#### 需二次确认的操作列表

| 工具 | 操作类型 | 风险等级 | 说明 |
|------|---------|---------|------|
| `huawei_create_aom_alarm_rule` | 创建 | 🟡 中 | 创建新的 AOM 告警规则，可能引入新的告警通知 |
| `huawei_update_aom_alarm_rule` | 修改 | 🟠 高 | 修改 AOM 告警规则阈值、开关、通知动作、描述等配置 |
| `huawei_delete_aom_alarm_rule` | 删除 | 🔴 高 | 删除 AOM 告警规则，可能导致后续告警无法触发 |
| `huawei_disable_aom_alarm_rule` | 停用 | 🔴 高 | 停用 AOM 告警规则，可能导致相关告警不再触发 |
| `huawei_enable_aom_alarm_rule` | 启用 | 🟠 高 | 启用 AOM 告警规则，可能恢复并触发告警通知 |
| `huawei_delete_aom_action_rule` | 删除 | 🔴 高 | 删除 AOM 通知动作规则，可能导致告警无法发送通知 |

#### 工作流程

**第一步：预览操作** - 不带 `confirm` 参数调用
```bash
# 示例：预览创建告警规则
python3 huawei-cloud.py huawei_create_aom_alarm_rule \
  region=cn-north-4 \
  rule_name=my-rule \
  metric_name=cpuUsage \
  namespace=PAAS.NODE \
  comparison_operator='>' \
  threshold=80 \
  period=60 \
  evaluation_periods=3 \
  statistic=average \
  alarm_level=2

```

返回：操作预览、目标规则、规则字段和确认示例，不执行真实创建。

**第二步：确认执行** - 携带 `confirm=true` 参数再次调用
```bash
# 示例：确认创建告警规则
python3 huawei-cloud.py huawei_create_aom_alarm_rule \
  region=cn-north-4 \
  rule_name=my-rule \
  metric_name=cpuUsage \
  namespace=PAAS.NODE \
  comparison_operator='>' \
  threshold=80 \
  period=60 \
  evaluation_periods=3 \
  statistic=average \
  alarm_level=2 \
  confirm=true
```

#### 禁止动作

| 动作 | 说明 |
|------|------|
| 创建/更新动作规则 | 不创建、更新通知动作规则 |
| 修改静默规则 | 不创建、更新、删除静默规则 |
| 执行恢复动作 | 不扩缩容、不重启、不 drain、不删除工作负载或节点 |
| 修改集群资源 | 不变更 CCE、ECS、ELB、EIP、VPC、安全组等资源 |

如果分析结果需要扩缩容、重启、drain、漏洞状态变更或其它恢复动作，必须只输出建议，并转交 `auto-remediation-runner` 进行预览、确认和执行后验证。

### 认证信息安全

✅ **本技能严格遵守以下安全规则：**

1. **禁止持久化存储认证信息** - 从不将 AK/SK、Token、证书等敏感认证信息保存到磁盘文件
2. **禁止长期内存缓存** - AK/SK 仅在当前 API 请求调用过程中存在于内存，调用结束后自动释放
3. **仅项目 ID 内存缓存** - 仅将非敏感的项目 ID 缓存在进程内存中（不写入磁盘）
4. **禁止日志泄露** - 不在任何日志、响应输出或错误信息中包含 AK/SK 等敏感信息
5. **输出脱敏** - 对外输出只展示告警、资源和规则信息，不展示认证凭证

AK/SK 仅支持以下两种方式使用：
- 通过环境变量 `HUAWEI_AK` / `HUAWEI_SK` 传入（推荐）
- 通过每次调用参数传入（仅本次调用有效）

---

## 前置条件

### 环境变量配置

**方式一：环境变量（推荐）**
```bash
export HUAWEI_AK="your-access-key-id"
export HUAWEI_SK="your-secret-access-key"
```

**方式二：每次调用参数传入**
在每次 API 调用时传入 `ak` 和 `sk` 参数（不推荐用于生产环境）。

### Python 依赖

```bash
pip install huaweicloudsdkcore huaweicloudsdkaom huaweicloudsdkiam
```

### IAM 权限策略

确保 IAM 用户具有以下最小权限：

| 权限 | 说明 |
|------|------|
| `aom:event:list` | 查询 AOM 告警事件 |
| `aom:alarmRule:list` | 查询 AOM 告警规则 |
| `aom:alarmRule:create` | 创建 AOM 告警规则 |
| `aom:alarmRule:update` | 修改 AOM 告警规则 |
| `aom:alarmRule:delete` | 删除 AOM 告警规则 |
| `aom:actionRule:list` | 查询 AOM 动作规则 |
| `aom:muteRule:list` | 查询 AOM 静默规则 |
| `cce:cluster:list` | 通过集群 ID 获取集群名称和辅助过滤信息 |

---

## 工具分类

### 告警查询与归并

| 工具 | 功能 | 集群过滤 | 参数 |
|------|------|---------|------|
| `huawei_list_aom_alarms` | 查询 active + history 告警并合并去重 | 支持 `cluster_id` | `region` |
| `huawei_list_aom_current_alarms` | 查询当前活跃告警 | 支持 `cluster_id` | `region` |
| `huawei_analyze_aom_alarms` | 对 active + history 告警做去重、分级和突发/常态识别 | 支持 `cluster_id` | `region` |

**参数说明：**
- `region` (required): 华为云区域，例如 `cn-north-4`
- `cluster_id` (optional): CCE 集群 ID；传入后只返回该集群相关告警
- `ak` (optional): Access Key ID，优先使用 `HUAWEI_AK`
- `sk` (optional): Secret Access Key，优先使用 `HUAWEI_SK`
- `project_id` (optional): 华为云项目 ID，不传时按 region 自动获取

**使用示例：**
```bash
# 查询区域内 active + history 告警
python3 huawei-cloud.py huawei_list_aom_alarms \
  region=cn-north-4

# 查询指定集群 active + history 告警
python3 huawei-cloud.py huawei_list_aom_alarms \
  region=cn-north-4 \
  cluster_id=xxx

# 查询指定集群当前活跃告警
python3 huawei-cloud.py huawei_list_aom_current_alarms \
  region=cn-north-4 \
  cluster_id=xxx

# 分析指定集群告警，输出突发、关注、常态分组
python3 huawei-cloud.py huawei_analyze_aom_alarms \
  region=cn-north-4 \
  cluster_id=xxx
```

---

### 告警规则管理

**事件告警创建约束：**
- 使用 `huawei_create_aom_event_alarm_rule` 创建事件告警时，`event_name` 必须优先参考 `references/cce-event-list.md` 中的事件列表与命名格式（推荐 `中文事件描述##事件名称`）。
- 创建事件告警时，默认启用告警降噪（`route_group_enable=true`）。

**指标告警创建约束：**
- 使用 `huawei_create_aom_alarm_rule` 创建指标告警时，PromQL/指标口径与阈值应优先参考 `references/cce-prometheus-metric-alarms.md`。

| 工具 | 功能 | 风险等级 | 需确认 | 参数 |
|------|------|---------|-------|------|
| `huawei_list_aom_alarm_rules` | 查询 AOM 告警规则 | 🟢 低 | 否 | `region` |
| `huawei_create_aom_alarm_rule` | 创建 AOM 告警规则 | 🟡 中 | **是** | `region`, `rule_name`, `metric_name`, `namespace`, `comparison_operator`, `threshold`, `period`, `evaluation_periods`, `statistic`, `alarm_level` |
| `huawei_update_aom_alarm_rule` | 修改 AOM 告警规则 | 🟠 高 | **是** | `region`, `rule_name` |
| `huawei_delete_aom_alarm_rule` | 删除 AOM 告警规则 | 🔴 高 | **是** | `region`, `rule_name` |
| `huawei_disable_aom_alarm_rule` | 停用 AOM 告警规则 | 🔴 高 | **是** | `region`, `rule_id` |
| `huawei_enable_aom_alarm_rule` | 启用 AOM 告警规则 | 🟠 高 | **是** | `region`, `rule_id` |
| `huawei_list_aom_action_rules` | 查询 AOM 告警动作规则 | 🟢 低 | 否 | `region`, `enterprise_project_id` |
| `huawei_delete_aom_action_rule` | 删除 AOM 告警动作规则（通知规则） | 🔴 高 | **是** | `region`, `rule_name` |
| `huawei_list_aom_mute_rules` | 查询 AOM 静默规则 | 🟢 低 | 否 | `region` |

**参数说明：**
- `region` (required): 华为云区域
- `metric_name` (required for create): 指标名称
- `namespace` (required for create): 指标命名空间
- `comparison_operator` (required for create): 阈值比较符，例如 `>`、`<`、`>=`、`<=`
- `threshold` (required for create): 告警阈值
- `period` (required for create): 统计周期，单位秒
- `evaluation_periods` (required for create): 连续触发周期数
- `statistic` (required for create): 统计方式，例如 `average`、`max`、`min`
- `alarm_level` (required for create): 告警级别
- `rule_name` (required for update): 告警规则名称，AOM 更新接口通过规则名称定位规则
- `rule_name` (required for delete): 告警规则名称
- `rule_id` (required for disable): 需要停用的告警规则 ID
- `rule_id` (required for enable): 需要启用的告警规则 ID
- `rule_name` (required for delete action rule): AOM 通知动作规则名称
- `enterprise_project_id` (optional for list action rules): 企业项目范围，默认 `all_granted_eps`
- `fields` (optional): 创建规则时的额外 JSON 字段，例如 `{"unit":"%","is_turn_on":true}`
- `updates` (optional): JSON 格式的批量更新字段，例如 `{"threshold":"80","is_turn_on":true}`
- `confirm` (optional): 创建、修改或删除时必须显式设置为 `true` 才会执行
- `ak` (optional): Access Key ID
- `sk` (optional): Secret Access Key
- `project_id` (optional): 华为云项目 ID

**使用示例：**
```bash
# 查询告警规则
python3 huawei-cloud.py huawei_list_aom_alarm_rules \
  region=cn-north-4

# 预览创建告警规则，不执行
python3 huawei-cloud.py huawei_create_aom_alarm_rule \
  region=cn-north-4 \
  rule_name=my-rule \
  metric_name=cpuUsage \
  namespace=PAAS.NODE \
  comparison_operator='>' \
  threshold=80 \
  period=60 \
  evaluation_periods=3 \
  statistic=average \
  alarm_level=2

# 确认创建告警规则
python3 huawei-cloud.py huawei_create_aom_alarm_rule \
  region=cn-north-4 \
  rule_name=my-rule \
  metric_name=cpuUsage \
  namespace=PAAS.NODE \
  comparison_operator='>' \
  threshold=80 \
  period=60 \
  evaluation_periods=3 \
  statistic=average \
  alarm_level=2 \
  confirm=true

# 预览修改告警规则，不执行
python3 huawei-cloud.py huawei_update_aom_alarm_rule \
  region=cn-north-4 \
  rule_name=my-rule \
  threshold=80

# 确认修改告警规则
python3 huawei-cloud.py huawei_update_aom_alarm_rule \
  region=cn-north-4 \
  rule_name=my-rule \
  threshold=80 \
  confirm=true

# 预览删除告警规则，不执行
python3 huawei-cloud.py huawei_delete_aom_alarm_rule \
  region=cn-north-4 \
  rule_name=xxx

# 确认删除告警规则
python3 huawei-cloud.py huawei_delete_aom_alarm_rule \
  region=cn-north-4 \
  rule_name=xxx \
  confirm=true

# 预览停用告警规则，不执行
python3 huawei-cloud.py huawei_disable_aom_alarm_rule \
  region=cn-north-4 \
  rule_id=xxx

# 确认停用告警规则
python3 huawei-cloud.py huawei_disable_aom_alarm_rule \
  region=cn-north-4 \
  rule_id=xxx \
  confirm=true

# 预览启用告警规则，不执行
python3 huawei-cloud.py huawei_enable_aom_alarm_rule \
  region=cn-north-4 \
  rule_id=xxx

# 确认启用告警规则
python3 huawei-cloud.py huawei_enable_aom_alarm_rule \
  region=cn-north-4 \
  rule_id=xxx \
  confirm=true


# 查询动作规则
python3 huawei-cloud.py huawei_list_aom_action_rules \
  region=cn-north-4

# 预览删除动作规则，不执行
python3 huawei-cloud.py huawei_delete_aom_action_rule \
  region=cn-north-4 \
  rule_name=xxx

# 确认删除动作规则
python3 huawei-cloud.py huawei_delete_aom_action_rule \
  region=cn-north-4 \
  rule_name=xxx \
  confirm=true

# 查询静默规则
python3 huawei-cloud.py huawei_list_aom_mute_rules \
  region=cn-north-4
```

### 集群告警巡检

| 工具 | 功能 | 集群过滤 | 参数 |
|------|------|---------|------|
| `huawei_aom_alarm_inspection` | 对指定 CCE 集群做 AOM 告警巡检并输出风险项 | `cluster_id` 必填 | `region`, `cluster_id` |

**参数说明：**
- `region` (required): 华为云区域
- `cluster_id` (required): CCE 集群 ID
- `ak` (optional): Access Key ID
- `sk` (optional): Secret Access Key
- `project_id` (optional): 华为云项目 ID

**使用示例：**
```bash
# 巡检指定集群 AOM 告警
python3 huawei-cloud.py huawei_aom_alarm_inspection \
  region=cn-north-4 \
  cluster_id=xxx
```

---

## 推荐工作流

### 场景一：查询指定集群告警

1. 明确 `region` 和 `cluster_id`
2. 调用 `huawei_list_aom_alarms` 查询 active + history 合并结果
3. 按告警类型、资源对象、状态和严重级别归并
4. 输出当前触发中告警、已恢复但仍需关注的历史告警、Top 资源对象

### 场景二：告警风暴或重复告警降噪

1. 调用 `huawei_analyze_aom_alarms`
2. 将原始告警归并为唯一告警组
3. 区分突发告警、关注告警和常态告警
4. 输出噪音削减比例、Top 关注项和推荐诊断 skill

### 场景三：查询、创建、修改或删除告警规则

1. 调用 `huawei_list_aom_alarm_rules` 查询告警规则
2. 需要创建时先调用 `huawei_create_aom_alarm_rule` 获取预览
3. 需要修改时先调用 `huawei_update_aom_alarm_rule` 获取预览
4. 需要删除时先调用 `huawei_delete_aom_alarm_rule` 获取预览
5. 需要停用时先调用 `huawei_disable_aom_alarm_rule` 获取预览
6. 用户明确确认后再次调用并携带 `confirm=true`
7. 创建、修改、删除或停用后再次调用 `huawei_list_aom_alarm_rules` 验证规则状态

### 场景四：确认告警是否被动作规则或静默影响

1. 调用 `huawei_list_aom_action_rules` 查询通知动作规则
2. 如需删除失效动作规则，先调用 `huawei_delete_aom_action_rule` 预览，再由用户确认后携带 `confirm=true` 执行
3. 调用 `huawei_list_aom_mute_rules` 查询静默规则
4. 判断是否存在动作规则异常或静默导致的通知缺失

### 场景五：集群巡检入口

1. 调用 `huawei_aom_alarm_inspection`
2. 汇总指定集群告警总数、触发中数量、已恢复数量和严重级别分布
3. 输出资源告警列表和需要进一步诊断的对象
4. 如涉及 Pod、Node、Network 问题，转交对应诊断 skill

---

## 输出要求

### 告警摘要

输出必须包含：

| 字段 | 说明 |
|------|------|
| `region` | 查询区域 |
| `cluster_id` | 如用户指定集群，则输出集群 ID |
| `total_count` | 告警总数 |
| `firing_count` | 当前触发中告警数量 |
| `resolved_count` | 已恢复告警数量 |
| `severity_stats` | 严重级别分布 |
| `type_stats` | 按告警类型归并统计 |

### 资源线索

对 CCE 告警，优先输出以下资源维度：

| 字段 | 说明 |
|------|------|
| `cluster_name` | 集群名称 |
| `namespace` | 命名空间 |
| `pod_name` | Pod 名称 |
| `resource_kind` | 资源类型 |
| `event_name` | 告警名称 |
| `message` | 告警消息 |

### 推荐诊断 skill

| 告警特征 | 推荐 skill |
|----------|------------|
| `CrashLoopBackOff`、`BackOffStart`、`FailedStart`、`ImagePullBackOff` | `pod-failure-diagnoser` |
| `FailedScheduling`、`Insufficient cpu`、`Insufficient memory` | `pod-failure-diagnoser` 或 `node-failure-diagnoser` |
| `NodeNotReady`、节点资源压力、NPD 事件 | `node-failure-diagnoser` |
| `Ingress 502/504`、Service 不通、ELB 异常 | `network-failure-diagnoser` |
| 多类告警同时出现且影响业务 | `root-cause-analyzer` |
| 需要扩缩容、重启、drain 等恢复动作 | `auto-remediation-runner` |

---

## References

- 告警归并步骤读 `references/workflow.md`
- 只读边界和误报处理读 `references/risk-rules.md`
- 输出结构按 `references/output-schema.md`
- Prometheus 指标告警规则参考 `references/cce-prometheus-metric-alarms.md`
