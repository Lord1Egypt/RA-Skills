---
name: cce-cluster-upgrade-planner
description: |
  华为云 CCE 集群版本升级评估技能，覆盖升级路径验证、76项升级前检查清单、插件兼容性评估、版本特有破坏性变更、废弃API迁移、升级窗口估算与执行预览。
  触发场景：(1) 计划升级CCE集群K8s版本；(2) 评估升级路径兼容性；(3) 升级前差异检查；(4) 估算升级窗口时间；(5) 生成升级执行方案预览；(6) 插件升级兼容性评估。
  关键词：CCE 集群升级、升级评估、版本兼容、升级窗口、升级前检查、Kubernetes升级、插件升级、差异检查、升级方案、升级路径、废弃API、回退策略
tags: [cce, kubernetes, 升级, 兼容性, 评估]
version: 1.0.0
---

# 华为云 CCE 集群升级评估

## 概述

使用 hcloud CLI (KooCLI) 评估和规划 CCE 集群 Kubernetes 版本升级。覆盖升级路径验证、76项升级前检查、插件兼容性、版本特有破坏性变更、废弃API迁移、升级窗口估算与执行预览（需二次确认才执行）。

**架构**: hcloud CLI → CCE OpenAPI → 集群信息 / 升级路径 / 升级工作流 / 插件信息 / 节点池信息

**标准流程**:
```
1. 采集集群现状（版本、节点、插件、节点池）
2. 查询升级路径（ListClusterUpgradePaths）
3. 升级前检查（ShowClusterUpgradeInfo 或 CreateUpgradeWorkFlow）
4. 评估插件兼容性（逐个插件版本兼容矩阵）
5. 估算升级窗口（节点数/插件数/批次策略）
6. 生成升级方案（具体 hcloud CLI 命令预览）
7. 回退策略与升级后验证
```

## ⛔ 安全约束

### 危险操作二次确认机制

> **本技能严格执行升级执行预览的二次确认机制。**

所有升级执行预览命令需要用户明确确认后才执行。

**第一步：预览** — 展示升级命令、目标版本、受影响组件、风险警告

**第二步：确认执行** — 用户明确确认后才执行

#### 需二次确认的操作

| 操作 | 风险等级 | 说明 |
|------|---------|------|
| UpgradeCluster | 🔴 极高 | 升级Kubernetes控制面，启动后不可逆 |
| UpgradeNodePool | 🟠 高 | 升级节点池K8s版本，节点临时不可调度 |
| CreateUpgradeWorkFlow | 🟠 高 | 创建升级工作流（含升级前检查→集群升级→升级后检查） |

### 认证信息安全

- **禁止暴露 AK/SK 值** — 不在对话、命令或输出中包含
- **禁止要求用户直接输入 AK/SK** — 不在对话中请求
- **仅用** `hcloud configure list` 检查凭证状态（仅检查是否存在，不读取值）
- **优先** 使用配置模式或环境变量，而非显式 AK/SK 参数

## 前置条件

> **前置检查: hcloud (KooCLI) >= 7.2.2 必需**
> 运行 `hcloud version` 验证版本，`hcloud configure list` 检查配置是否存在。

```bash
hcloud version
hcloud configure list
```

## 命令格式

CCE 升级遵循标准 hcloud 格式：

```bash
hcloud CCE <Operation> --param=value --cli-region=<region> --cli-output=json
```

### 升级特有参数规则

1. **cluster_id 必需**: 所有升级操作需要 `--cluster_id`
2. **目标版本必需**: 升级操作需要 `--spec.clusterUpgradeAction.targetVersion=v1.XX`
3. **插件升级用数组格式**: `--spec.clusterUpgradeAction.addons.1.addonTemplateName=<name> --spec.clusterUpgradeAction.addons.1.version=<ver>`
4. **节点池优先级用键值格式**: `--spec.clusterUpgradeAction.nodePoolOrder.key1=value1`
5. **节点选择器用嵌套格式**: `--spec.clusterUpgradeAction.nodeOrder.key1.1.nodeSelector.key=<label-key> --spec.clusterUpgradeAction.nodeOrder.key1.1.nodeSelector.operator=In --spec.clusterUpgradeAction.nodeOrder.key1.1.nodeSelector.value.1=<val>`
6. **升级策略**: `--spec.clusterUpgradeAction.strategy.type=inPlaceRollingUpdate`（仅支持原地升级）
7. **批次大小**: `--spec.clusterUpgradeAction.strategy.inPlaceRollingUpdate.userDefinedStep=<1-40>`（默认20，推荐）
8. **批次范围**: `--spec.clusterUpgradeAction.strategy.inPlaceRollingUpdate.scope=Cluster` 或 `NodePool`

> **⚠️ 关键**: 构造任何升级命令前，务必运行 `hcloud CCE <Operation> --help` 验证参数名。

## 场景路由

| 用户意图 | 参考文档 |
|---------|---------|
| 全流程升级评估（7步工作流） | [references/upgrade-workflow.md](references/upgrade-workflow.md) |
| 升级前检查清单（76项） | [references/pre-upgrade-checklist.md](references/pre-upgrade-checklist.md) |
| 插件兼容矩阵与升级顺序 | [references/addon-compatibility.md](references/addon-compatibility.md) |
| K8s版本升级路径规则 | [references/k8s-version-matrix.md](references/k8s-version-matrix.md) |
| 升级窗口时间估算 | [references/upgrade-window-estimation.md](references/upgrade-window-estimation.md) |
| 版本特有破坏性变更 | [references/pre-upgrade-checklist.md](references/pre-upgrade-checklist.md) |
| 废弃API迁移 | [references/pre-upgrade-checklist.md](references/pre-upgrade-checklist.md) |
| 风险约束与回退 | [references/risk-rules.md](references/risk-rules.md) |
| 输出结构 | [references/output-schema.md](references/output-schema.md) |

## 核心命令

### 步骤1：采集集群现状

```bash
hcloud CCE ShowCluster --cluster_id=<cluster-id> --detail=true --cli-region=<region> --cli-output=json
hcloud CCE ListAddonInstances --cluster_id=<cluster-id> --cli-region=<region> --cli-output=json
hcloud CCE ListNodePools --cluster_id=<cluster-id> --cli-region=<region> --cli-output=json
hcloud CCE ListNodes --cluster_id=<cluster-id> --cli-region=<region> --cli-output=json
```

### 步骤2：查询升级路径

```bash
hcloud CCE ListClusterUpgradePaths --cli-region=<region> --cli-output=json
```

### 步骤3：升级前检查

```bash
hcloud CCE ShowClusterUpgradeInfo --cluster_id=<cluster-id> --cli-region=<region> --cli-output=json
hcloud CCE CreateUpgradeWorkFlow \
  --cluster_id=<cluster-id> \
  --apiVersion=v3 --kind=WorkFlowTask \
  --spec.targetVersion=<target-version> \
  --spec.clusterVersion=<current-version> \
  --cli-region=<region> --cli-output=json
```

### 步骤4：插件兼容性检查

```bash
hcloud CCE ListAddonInstances --cluster_id=<cluster-id> --cli-region=<region> --cli-output=json
hcloud CCE ListAddonTemplates --cluster_id=<cluster-id> --addon_template_name=<addon-name> --cli-region=<region> --cli-output=json
```

### 步骤5：升级执行预览

```bash
hcloud CCE UpgradeCluster \
  --cluster_id=<cluster-id> \
  --metadata.apiVersion=v3 --metadata.kind=UpgradeTask \
  --spec.clusterUpgradeAction.targetVersion=<target-version> \
  --spec.clusterUpgradeAction.strategy.type=inPlaceRollingUpdate \
  --spec.clusterUpgradeAction.strategy.inPlaceRollingUpdate.userDefinedStep=20 \
  --spec.clusterUpgradeAction.strategy.inPlaceRollingUpdate.scope=Cluster \
  --cli-region=<region> --cli-output=json
```

### 步骤6：监控升级进度

```bash
hcloud CCE ShowUpgradeWorkFlow --cluster_id=<cluster-id> --upgrade_workflow_id=<workflow-id> --cli-region=<region> --cli-output=json
hcloud CCE ListUpgradeClusterTasks --cluster_id=<cluster-id> --cli-region=<region> --cli-output=json
hcloud CCE PauseUpgradeClusterTask --cluster_id=<cluster-id> --cli-region=<region> --cli-output=json
hcloud CCE ContinueUpgradeClusterTask --cluster_id=<cluster-id> --cli-region=<region> --cli-output=json
hcloud CCE RetryUpgradeClusterTask --cluster_id=<cluster-id> --cli-region=<region> --cli-output=json
```

### 步骤7：取消升级工作流

```bash
hcloud CCE UpgradeWorkFlowUpdate \
  --cluster_id=<cluster-id> --upgrade_workflow_id=<workflow-id> \
  --status.phase=Cancel --cli-region=<region> --cli-output=json
```

## 升级窗口估算公式

详见 [references/upgrade-window-estimation.md](references/upgrade-window-estimation.md)

**快速估算**:
```
T_total = T控制面 + T节点批次 + T插件 + T验证 + T缓冲

T控制面 = 10-30分钟
T节点批次 = N节点 / 批次大小 * (5-15分钟/节点)
T插件 = 插件数 * (5-15分钟/插件)
T验证 = 30分钟
T缓冲 = 20% * (T控制面 + T节点批次 + T插件 + T验证)
```

**示例**: 10节点5插件集群 v1.23→v1.25：
- 控制面: 15分钟
- 节点批次: 1+4+5节点, ~100分钟
- 插件: 50分钟
- 验证: 30分钟
- 缓冲: 40分钟
- **总计: ~235分钟 (3小时55分钟)**

## 升级方式

| 方式 | 优点 | 限制 | 推荐场景 |
|------|------|------|---------|
| **原地升级** | 控制面升级时业务Pod不中断；节点分批升级；插件自动升级 | 节点升级时临时不可调度；v1.27+需Docker→Containerd切换 | 大多数场景（默认） |
| **迁移** | 全新环境；无兼容性风险累积；跳过中间版本升级 | 全量工作负载重新部署；需要双倍资源；更长的停机时间 | 大跨版本升级（如v1.15→v1.28）；不兼容运行时 |

## 关键约束

- **禁止跨版本跳跃升级**: 必须按升级路径逐版本走（如v1.21→v1.23→v1.25→v1.27→v1.28）
- **补丁版本先行**: 升级到最新补丁版本后再升大版本
- **先升控制面再升节点**: 控制面先升级，然后节点池
- **集群升级后再升插件**: 集群达到目标版本后再升级插件
- **v1.28+控制节点IP变更**: 升级到v1.28+会创建新控制节点，IP地址变更
- **自动伸缩暂停**: 控制面升级期间自动伸缩暂停；控制面完成后恢复扩容，缩容需等全部升级完成

## 最佳实践

1. **先做升级前检查** — 用 CreateUpgradeWorkFlow 或 ShowClusterUpgradeInfo 验证就绪状态
2. **先升补丁版本** — 确保当前补丁版本为最新后再升大版本
3. **业务低流量时段** — 在低流量时段安排升级
4. **每个节点池≥2节点** — 升级期间保持冗余
5. **监控升级进度** — 每个阶段后检查 ShowUpgradeWorkFlow 状态
6. **每阶段后验证** — 控制面和节点升级后运行业务验证
7. **准备回退方案** — 使用备份数据和 PauseUpgradeClusterTask 处理问题

## 参考文档

| 文档 | 说明 |
|------|------|
| [upgrade-workflow.md](references/upgrade-workflow.md) | 7步升级全流程详情 |
| [pre-upgrade-checklist.md](references/pre-upgrade-checklist.md) | 76项升级前检查清单与版本特有破坏性变更 |
| [addon-compatibility.md](references/addon-compatibility.md) | 插件兼容矩阵、DaemonSet插件、升级顺序 |
| [k8s-version-matrix.md](references/k8s-version-matrix.md) | 官方CCE升级路径表与补丁版本规则 |
| [upgrade-window-estimation.md](references/upgrade-window-estimation.md) | 升级窗口估算公式、批次策略、示例 |
| [risk-rules.md](references/risk-rules.md) | 风险约束、回退策略、护栏 |
| [output-schema.md](references/output-schema.md) | 评估报告和执行预览JSON结构