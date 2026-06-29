---
name: kubernetes-event-analyzer
description: |
  华为云 CCE 集群 Kubernetes 事件查询与分析技能，覆盖 Warning 事件查询、重复事件模式识别、Pod/Node/Workload 异常检测、LTS 日志流事件历史查询，并自动移交至对应诊断技能。
  触发场景：(1) 查询集群或命名空间的 Kubernetes 事件；(2) 查找 Warning 事件；(3) 识别事件模式如 ImagePullBackOff、Eviction、NodeNotReady、FailedScheduling；(4) 关联事件与特定工作负载或时间窗口；(5) 事件趋势与频率汇总。
  关键词：Kubernetes events, Kubernetes 事件, CCE events, CCE 事件, event analysis, 事件分析, FailedScheduling, FailedMount, event query, 事件查询, cluster events, 集群事件, Warning 事件, 事件模式
tags: [cce, kubernetes, 事件, 可观测性, 分析]
version: 1.0.0
---

# Kubernetes 事件分析器

## 概述

在华为云 CCE 集群中查询和分析 Kubernetes 事件，发现 Warning 事件、异常和故障模式。通过 K8s API 或 LTS 日志流查询事件，客户端过滤和分组，汇总模式并移交至诊断技能。

**架构**: MCP 工具 → CCE K8s API / LTS 日志流 → 事件 → 客户端过滤与分组 → 模式汇总 → 诊断移交

**标准流程**:
```
1. 从用户查询中识别 region、cluster_id 和可选 namespace
2. 使用 huawei_get_cce_events (K8s API) 或 huawei_query_k8s_events_from_lts (LTS) 获取事件
3. 客户端过滤（type、reason、involved_object、时间窗口）
4. 按 reason、namespace 或模式分组聚合
5. 汇总有高频原因、重复模式和受影响资源
6. 若发现特定故障，移交至对应诊断技能
```

**关联技能**（移交目标）:
- Pod 故障 -> `pod-failure-diagnoser`
- 工作负载发布问题 -> `workload-failure-diagnoser`
- 节点问题 -> `node-failure-diagnoser`
- 服务/网络问题 -> `network-failure-diagnoser`
- 需要执行操作 -> `auto-remediation-runner`

## 安全约束

### 只读技能

> **本技能严格只读。** 仅查询 Kubernetes 事件和列出相关资源，不执行任何修改操作。

- **禁止写操作**: 不修改、删除或创建任何 Kubernetes 资源
- **脱敏处理**: 不暴露节点名称、Pod 名称或工作负载名称等可识别生产系统的信息，汇总中使用脱敏或虚构示例
- **移交修复**: 若事件分析发现明确修复路径，提供证据并移交至诊断或修复技能，不在此技能中执行恢复操作
- **时间有界查询**: 保持事件查询时间有界，优先使用近1-24小时窗口以避免结果过大
- **重定向操作请求**: 若用户要求基于事件结果执行操作，汇总证据后重定向至 `auto-remediation-runner`

## 工具

| 工具 | 用途 | 必需参数 | 可选参数 |
|------|------|---------|---------|
| `huawei_get_cce_events` | 通过 K8s API Server 查询 CCE Kubernetes 事件 | `region`, `cluster_id` | `namespace`, `limit` |
| `huawei_query_k8s_events_from_lts` | 通过 LTS 日志流查询 K8s 事件（需 Event→LTS LogConfig） | `region`, `cluster_id`, `start_time`, `end_time` | `keywords` |

## 场景路由

| 用户意图 | 参考文档 |
|---------|---------|
| 全流程事件查询（5步） | [references/workflow.md](references/workflow.md) |
| 事件模式识别表 | [references/workflow.md](references/workflow.md) |
| 时间窗口分析指引 | [references/workflow.md](references/workflow.md) |
| 风险约束与护栏 | [references/risk-rules.md](references/risk-rules.md) |
| 输出结构（查询与分析） | [references/output-schema.md](references/output-schema.md) |

## 核心命令

### 步骤1：通过 K8s API 查询事件 (huawei_get_cce_events)

从集群 API Server 获取原始 Kubernetes 事件。除 `namespace` 和 `limit` 外的所有过滤均在获取后客户端执行。

```bash
# 查询集群所有事件
python3 scripts/huawei-cloud.py huawei_get_cce_events \
  region=cn-north-4 \
  cluster_id=<cluster-id>

# 查询特定命名空间的事件
python3 scripts/huawei-cloud.py huawei_get_cce_events \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  namespace=default

# 限制事件数量
python3 scripts/huawei-cloud.py huawei_get_cce_events \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  limit=100
```

**API 支持的过滤**: `namespace`, `limit` (默认 500)

**需客户端过滤**: `event_type`, `reason`, `involved_object_kind`, `involved_object_name`, `hours`, `start_time`, `end_time`

### 步骤2：通过 LTS 查询事件 (huawei_query_k8s_events_from_lts)

查询通过 Event→LTS LogConfig 收集到 LTS 的 K8s 事件。需已启用事件收集并指向 LTS 输出的 LogConfig。

```bash
# 在时间窗口内查询 LTS 事件
python3 scripts/huawei-cloud.py huawei_query_k8s_events_from_lts \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  start_time="2026-05-30 06:00:00" \
  end_time="2026-05-30 08:00:00"

# 关键词过滤查询
python3 scripts/huawei-cloud.py huawei_query_k8s_events_from_lts \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  start_time="2026-05-30 00:00:00" \
  end_time="2026-05-30 23:59:59" \
  keywords=FailedScheduling
```

**LTS 时间格式**: `YYYY-MM-DD HH:MM:SS`

**降级方案**: 若未找到启用了事件收集的 Event→LTS LogConfig，将返回错误，改用 `huawei_get_cce_events`。

### 步骤3：客户端过滤

获取事件后，根据用户需求应用过滤：

- `type == "Warning"` — 仅 Warning 事件
- `reason` — 特定模式（FailedScheduling、ImagePullBackOff、FailedMount 等）
- `involved_object.kind` + `involved_object.name` — 特定资源
- `namespace` — 命名空间分析
- `first_timestamp` / `last_timestamp` — 时间窗口分析

### 步骤4：分组聚合

- 按 `reason` 分组查找高频事件模式
- 按 `namespace` 分组查找高噪声命名空间
- 标记 `count > 1` 的事件为重复模式
- 计算 `warning_count` 与 `normal_count` 作为快速健康信号

### 步骤5：汇总与移交

汇总结果含计数、时间戳和受影响对象。若事件指向特定故障，带证据移交至对应诊断技能。

## 事件模式速查表

| 模式 | 可能原因 | 移交目标 |
|------|---------|---------|
| `ImagePullBackOff` 重复 | 镜像错误或拉取密钥缺失 | `pod-failure-diagnoser` |
| `FailedScheduling` + `insufficient` | 资源压力或节点未就绪 | `workload-failure-diagnoser` |
| `FailedMount` | 卷挂载或 PVC 问题 | `storage-failure-diagnoser` |
| `Evicted` Pod | 预算中断或节点压力 | `pod-failure-diagnoser` |
| `NodeNotReady` | 节点代理或网络问题 | `node-failure-diagnoser` |
| `Unhealthy` + Readiness 探针 | 应用问题或启动失败 | `pod-failure-diagnoser` |
| `FailedCreatePodSandBox` | CNI 或网络问题 | `network-failure-diagnoser` |
| `OOMKilled` | 内存限制超出 | `pod-failure-diagnoser` |

## 输出格式

### 来自 huawei_get_cce_events (K8s API)

| 字段 | 描述 |
|------|------|
| `region` | 华为云区域 |
| `cluster_id` | CCE 集群 ID |
| `namespace` | Kubernetes 命名空间过滤（若使用） |
| `total_fetched` | API 返回的事件数量 |
| `events` | 原始事件列表（客户端过滤） |
| `warning_count` | Warning 事件数量（计算值） |
| `top_reasons` | 高频事件原因及计数（计算值） |
| `repeated_patterns` | count > 1 的事件按原因分组 |
| `namespace_breakdown` | 各命名空间事件计数 |
| `next_steps` | 建议的后续查询或诊断技能 |

### 来自 huawei_query_k8s_events_from_lts (LTS)

| 字段 | 描述 |
|------|------|
| `region` | 华为云区域 |
| `cluster_id` | CCE 集群 ID |
| `log_group_id` | LTS 日志组 ID |
| `log_stream_id` | LTS 日志流 ID |
| `keywords` | 过滤关键词 |
| `event_count` | 返回的事件数量 |
| `events` | 解析后的规范化事件列表 |
| `time_range` | 查询起止时间 |
| `log_config` | LogConfig 信息（名称、是否启用事件等） |

## 最佳实践

1. **优先用 K8s API** — 使用 `huawei_get_cce_events` 快速查询；仅在需精确时间范围时降级至 LTS
2. **先过滤 Warning** — Warning 事件是主要信号；分析前先过滤 `type == "Warning"`
3. **按原因分组** — 按事件原因分组比逐条分析更快揭示系统性问题
4. **时间有界查询** — 优先使用近1-24小时窗口避免结果过大
5. **移交而非修复** — 本技能只读；始终带证据移交至诊断技能
6. **脱敏名称** — 汇要中使用通用标签；不暴露生产 Pod/节点/工作负载名称

## 参考文档

| 文档 | 说明 |
|------|------|
| [workflow.md](references/workflow.md) | 全流程事件查询、模式识别、时间窗口分析、聚合指引 |
| [risk-rules.md](references/risk-rules.md) | 只读约束、数据脱敏规则、移交策略、护栏 |
| [output-schema.md](references/output-schema.md) | 事件查询汇总、分析汇总和逐条事件详情结构 |