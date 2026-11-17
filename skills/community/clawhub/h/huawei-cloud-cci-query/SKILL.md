---
name: huawei-cloud-cci-query
version: 1.0.0
description: |
  查询华为云 CCI（Cloud Container Instances，云容器实例）实例详情的只读 Skill。
  通过 KooCLI（hcloud）执行 CCI 只读查询命令，覆盖命名空间列表、Pod 列表与详情、
  Deployment/StatefulSet/Service/Network 等资源的只读查询场景。
  适用于日常巡检、故障排查、资源管理。仅 List/Read 只读操作，不涉及 Create/Delete/Update。
triggers:
  - 查询华为云CCI
  - CCI实例查询
  - 列出CCI Pod
  - 查看CCI命名空间
  - 云容器实例查询
tags:
  - huawei-cloud
  - cci
  - query
  - kubernetes
  - readonly
tools:
  - hcloud
  - python3
---

# Huawei Cloud CCI Query（华为云云容器实例查询）

## 安全硬约束

1. AK/SK 只从环境变量动态读取，严禁写入文件/日志/评论。
2. 所有 `hcloud` 调用设 30s 超时（`timeout 30`），超时判定失败，不 hang。
3. API 返回 403（无 agency/权限）时：停止该区域查询，提示用户在 CCI 控制台完成服务授权委托，严禁绕行。
4. 仅执行只读查询（list/read/get），严禁执行 create/delete/update/patch/replace 等变更操作。
5. 凭据环境变量缺失 → 脚本退出码 3，不降级、不模拟。
6. region 参数由用户指定，脚本不做硬编码默认区域假设。

## Overview / 概述

华为云 CCI（Cloud Container Instances，云容器实例）是基于 Kubernetes 的无服务器容器服务。CCI 的 API 遵循 Kubernetes 风格，资源以 **命名空间（Namespace）+ 资源名** 组织，而非传统云服务的"实例 ID"模型。

> ⚠️ **重要说明**：CCI 服务在 KooCLI（hcloud）中 **没有** `ListInstances` / `ShowInstance` 这类命令。Issue/Spec 中提到的这两个命令名并不存在于 `hcloud CCI`。CCI 的"实例"在 Kubernetes 语义下对应 **Pod**，查询 Pod 列表用 `listCoreV1NamespacedPod`，查询 Pod 详情用 `readCoreV1NamespacedPod`。本 Skill 覆盖以下真实只读查询命令。

### 架构

```
用户 / Agent
    │  执行 scripts/cci_query.py <subcommand> [--params]
    ▼
scripts/cci_query.py
    │  动态读取 AK/SK 环境变量 → 配置 hcloud profile
    │  调用 hcloud CCI <Operation> --cli-region=<region> --cli-profile=default [--params]
    ▼
KooCLI (hcloud)
    │  HTTPS → CCI OpenAPI (Kubernetes 风格)
    ▼
华为云 CCI 服务
    │  返回 JSON (NamespaceList / Pod / PodList ...)
    ▼
脚本格式化输出（JSON / 表格）→ 用户
```

### 适用场景

| 场景 | 触发时机 | 常用命令 |
|------|----------|----------|
| 日常巡检 | 定期查看 CCI 命名空间与 Pod 运行状态 | `list-namespaces`、`list-pods` |
| 故障排查 | Pod 异常、容器重启、服务不可达 | `show-pod`、`list-pods`、`show-service` |
| 资源管理 | 清点命名空间下的 Deployment/Service/Network | `list-deployments`、`list-services`、`list-networks` |
| 资源清点 | 跨命名空间查看所有 Pod | `list-all-pods` |

## Prerequisites / 前置条件

| 条目 | 要求 | 说明 |
|------|------|------|
| KooCLI | ≥ 7.2.12 | 已验证 `hcloud CCI --help` 可列出全部操作 |
| Python | 3.8+ | 脚本运行环境 |
| AK/SK | 华为云 IAM 用户密钥 | 通过环境变量提供（动态扫描，见下） |
| IAM 权限 | `CCI:ReadOnlyAccess` | 最小只读权限 |
| CCI 服务授权 | 部分区域需在控制台完成 agency 授权 | 未授权区域返回 `CCI.01.403122` |

### 凭据环境变量

脚本动态扫描以下前缀的环境变量获取 AK/SK（不依赖固定变量名）：

- 前缀 `HUAWEI` / `HW` / `HWC`，且包含 `ACCESS_KEY` / `_AK` / `AK` → 作为 AK
- 前缀 `HUAWEI` / `HW` / `HWC`，且包含 `SECRET_KEY` / `_SK` / `SK` → 作为 SK

例如 `HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK` 即可被识别。

## Workflow / 工作流

1. **确认前置**：`hcloud --version` 可用；AK/SK 环境变量已设置且非空。
2. **配置认证**：脚本首次运行时自动 `hcloud configure set` 写入 default profile（AK/SK 从环境变量读取）。
3. **指定区域**：所有查询必须传 `--cli-region=<region>`（如 `cn-north-4`、`cn-east-3`）。
4. **执行查询**：按场景选择子命令，脚本调用对应 `hcloud CCI <Operation>`。
5. **解析输出**：脚本输出 JSON，便于 Agent 后续处理；`--pretty` 可输出格式化表格。
6. **处理空结果/403**：空 `items` 表示该区域无资源；403 提示前往 CCI 控制台完成服务授权委托。

## Core Commands / 核心命令

> 所有命令通过 `scripts/cci_query.py` 子命令封装。也可直接使用 `hcloud CCI <Operation>` 原生命令。

### 1. 命名空间查询

```bash
# 列出所有命名空间（指定区域）
python3 scripts/cci_query.py list-namespaces --region=cn-north-4

# 原生 hcloud 等价命令
hcloud CCI listNamespaces --cli-region=cn-north-4 --cli-profile=default
```

### 2. Pod 查询（CCI "实例"）

```bash
# 列出指定命名空间下的 Pod（CCI 容器实例列表）
python3 scripts/cci_query.py list-pods --region=cn-north-4 --namespace=<ns>

# 查询指定 Pod 详情（CCI 实例详情）
python3 scripts/cci_query.py show-pod --region=cn-north-4 --namespace=<ns> --name=<pod-name>

# 跨所有命名空间列出 Pod
python3 scripts/cci_query.py list-all-pods --region=cn-north-4
```

原生 hcloud 等价命令：

```bash
hcloud CCI listCoreV1NamespacedPod --cli-region=cn-north-4 --cli-profile=default --namespace=<ns>
hcloud CCI readCoreV1NamespacedPod --cli-region=cn-north-4 --cli-profile=default --namespace=<ns> --name=<pod-name>
hcloud CCI listCoreV1PodForAllNamespaces --cli-region=cn-north-4 --cli-profile=default
```

### 3. 工作负载查询

```bash
# Deployment 列表 / 详情
python3 scripts/cci_query.py list-deployments --region=cn-north-4 --namespace=<ns>
python3 scripts/cci_query.py show-deployment --region=cn-north-4 --namespace=<ns> --name=<name>

# StatefulSet 列表 / 详情
python3 scripts/cci_query.py list-statefulsets --region=cn-north-4 --namespace=<ns>
python3 scripts/cci_query.py show-statefulset --region=cn-north-4 --namespace=<ns> --name=<name>

# Job 列表 / 详情
python3 scripts/cci_query.py list-jobs --region=cn-north-4 --namespace=<ns>
python3 scripts/cci_query.py show-job --region=cn-north-4 --namespace=<ns> --name=<name>
```

### 4. 服务与网络查询

```bash
# Service 列表 / 详情
python3 scripts/cci_query.py list-services --region=cn-north-4 --namespace=<ns>
python3 scripts/cci_query.py show-service --region=cn-north-4 --namespace=<ns> --name=<name>

# Network（CCI 专属网络）列表 / 详情
python3 scripts/cci_query.py list-networks --region=cn-north-4 --namespace=<ns>
python3 scripts/cci_query.py show-network --region=cn-north-4 --namespace=<ns> --name=<name>
```

### 5. 其他资源

```bash
# ConfigMap / Secret / PVC / Event
python3 scripts/cci_query.py list-configmaps --region=cn-north-4 --namespace=<ns>
python3 scripts/cci_query.py list-secrets --region=cn-north-4 --namespace=<ns>
python3 scripts/cci_query.py list-pvcs --region=cn-north-4 --namespace=<ns>
python3 scripts/cci_query.py list-events --region=cn-north-4 --namespace=<ns>
```

### 6. 能力与特性查询

```bash
# 查看脚本支持的所有子命令
python3 scripts/cci_query.py --help

# 查看脚本能力清单
python3 scripts/cci_query.py capability-list
```

## Parameter Confirmation / 参数确认

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--region` | 是 | 区域 ID | `cn-north-4`、`cn-east-3`、`cn-south-1` |
| `--namespace` | list/show 命名空间资源时必填 | 命名空间名 | `default`、`ns-prod` |
| `--name` | show 类命令必填 | 资源名称 | `my-pod-xxx` |
| `--label-selector` | list 类可选 | 标签选择器 | `app=nginx` |
| `--field-selector` | list 类可选 | 字段选择器 | `status.phase=Running` |
| `--limit` | list 类可选 | 返回数量上限 | `100` |
| `--pretty` | 可选 | 格式化表格输出 | flag |

## KooCLI Command Format Standard

CCI 服务的 hcloud 命令遵循以下格式：

```
hcloud CCI <Operation> --cli-region=<region> --cli-profile=<profile> [--path-params] [--query-params]
```

### 命名规则

- **Service**：`CCI`（固定，全大写）
- **Operation**：Kubernetes 风格命名
  - `list*` → 列表查询（GET，返回 List 资源）
  - `read*` → 详情查询（GET，返回单个资源）
  - `get*` → 元数据/版本查询（GET，返回 API group/version）
- **路径参数**（path）：`--namespace`、`--name`
- **查询参数**（query）：`--label-selector`、`--field-selector`、`--limit`、`--continue`、`--watch`

### 只读操作白名单（本 Skill 覆盖）

| 子命令 | hcloud Operation | 说明 |
|--------|------------------|------|
| `list-namespaces` | `listNamespaces` | 列出所有命名空间 |
| `list-pods` | `listCoreV1NamespacedPod` | 列出命名空间下 Pod |
| `list-all-pods` | `listCoreV1PodForAllNamespaces` | 跨命名空间列出 Pod |
| `show-pod` | `readCoreV1NamespacedPod` | 查询 Pod 详情 |
| `list-deployments` | `listAppsV1NamespacedDeployment` / `listNamespacedDeployments` | 列出 Deployment |
| `show-deployment` | `readAppsV1NamespacedDeployment` / `readNamespacedDeployment` | 查询 Deployment 详情 |
| `list-statefulsets` | `listAppsV1NamespacedStatefulSet` | 列出 StatefulSet |
| `show-statefulset` | `readAppsV1NamespacedStatefulSet` | 查询 StatefulSet 详情 |
| `list-jobs` | `listBatchV1NamespacedJob` | 列出 Job |
| `show-job` | `readBatchV1NamespacedJob` | 查询 Job 详情 |
| `list-services` | `listCoreV1NamespacedService` / `listNamespacedServices` | 列出 Service |
| `show-service` | `readCoreV1NamespacedService` | 查询 Service 详情 |
| `list-networks` | `listNetworkingCciIoV1beta1NamespacedNetwork` / `listNamespacedNetworks` | 列出 CCI Network |
| `show-network` | `readNetworkingCciIoV1beta1NamespacedNetwork` | 查询 Network 详情 |
| `list-configmaps` | `listCoreV1NamespacedConfigMap` / `listNamespacedConfigMaps` | 列出 ConfigMap |
| `list-secrets` | `listCoreV1NamespacedSecret` / `listNamespacedSecrets` | 列出 Secret |
| `list-pvcs` | `listCoreV1NamespacedPersistentVolumeClaim` | 列出 PVC |
| `list-events` | `listCoreV1NamespacedEvent` | 列出 Event |
| `capability-list` | （脚本内置） | 列出脚本支持的全部子命令 |

### 验证命令可用性

```bash
# 列出 CCI 全部可用操作
hcloud CCI --help

# 验证某个操作存在及其参数
hcloud CCI listCoreV1NamespacedPod --help
```

## Reference Documents / 参考文档

- [CCI hcloud 命令参考](references/cci-cli-reference.md) — 全部只读查询命令的参数与输出说明
- [IAM 权限策略](references/iam-policies.md) — 最小权限 `CCI:ReadOnlyAccess`
- [hcloud CLI 安装认证指南](references/cli-installation-guide.md) — KooCLI 安装与 AK/SK 配置
- [验证方法](references/verification-method.md) — 如何确认 Skill 输出正确
- [数据流图](references/dataflow-diagram.md) — 请求/响应流程（Mermaid）
- [验收标准](references/acceptance-criteria.md) — Skill 合格条件

## 常见问题

| 问题 | 原因 | 处理 |
|------|------|------|
| `403 CCI.01.403122 user has no agency to cci` | 该区域未完成 CCI 服务授权委托 | 前往 CCI 控制台对应区域，点击「服务授权」完成 agency 授权 |
| `items: []` 或 `items: null` | 该区域/命名空间下无资源 | 正常空结果，非错误 |
| `The configuration file does not contain profile` | hcloud 未配置认证 | 脚本自动配置；或手动 `hcloud configure set --cli-access-key=... --cli-secret-key=...` |
| `Operation XXX is not supported` | 命令名错误（如误用 ListInstances） | 运行 `hcloud CCI --help` 核对真实操作名；CCI 用 Kubernetes 风格命名 |
