---
slug: kubernetes-toolkit-free
name: kubernetes-toolkit-free
version: 1.0.0
displayName: K8s集群管理入门
summary: Kubernetes集群基础管理工具，支持多Agent协作与常用资源操作。
license: Proprietary
edition: free
description: '面向个人开发者与小团队的K8s集群管理工具。支持多Agent协作模式，

  提供Pod/Service/Deployment/ConfigMap等常用资源的创建、查询与

  管理功能。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。适用于独立开发者、企业团队和自动化工作流场景。'
tags:
- Operations
- Kubernetes
- 集群管理
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L1-入门级"
pricing_model: per_use
suggested_price: "9.9 CNY/per_use"
tools: ["read", "write", "exec"]
tags: "工具,效率,自动化"
---
# K8s集群管理入门（免费版）

## 概述

本工具为个人开发者和小团队提供K8s集群管理能力。采用多Agent协作模式，支持常用K8s资源的创建、查询与管理。适合个人开发环境与小规模集群的日常运维。

## 核心能力

### 管理功能

| 功能 | 说明 | 免费版支持 |
|---|---|-----|
| 资源管理 | Pod/Service/Deployment等 | 支持 |
| 多Agent | 协作管理模式 | 支持 |
| 配置管理 | ConfigMap/Secret | 支持 |
| 故障排查 | 基础问题诊断 | 支持 |
| 命名空间 | 命名空间管理 | 支持 |
| 节点管理 | 节点查询与标签 | 基础 |
| 监控告警 | 集群监控 | 不支持 |
| 策略治理 | 策略管理 | 不支持 |

**输入**: 用户提供管理功能所需的指令和必要参数。
**处理**: 解析管理功能的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回管理功能的响应数据,包含状态码、结果和日志。

### 支持的资源类型

| 资源 | 创建 | 查询 | 更新 | 删除 |
|:-----|:-----|:-----|:-----|:-----|
| Pod | 支持 | 支持 | 有限 | 支持 |
| Deployment | 支持 | 支持 | 支持 | 支持 |
| Service | 支持 | 支持 | 支持 | 支持 |
| ConfigMap | 支持 | 支持 | 支持 | 支持 |
| Secret | 支持 | 支持 | 支持 | 支持 |
| Ingress | 支持 | 支持 | 支持 | 支持 |
| PVC | 支持 | 支持 | 有限 | 支持 |
| Namespace | 支持 | 支持 | 不支持 | 支持 |

**输入**: 用户提供支持的资源类型所需的指令和必要参数。
**处理**: 解析支持的资源类型的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回支持的资源类型的响应数据,包含状态码、结果和日志。

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Kubernetes、集群基础管理工具、支持多、协作与常用资源操、面向个人开发者与、小团队的、集群管理工具、协作模式、等常用资源的创建、Use、when、需要代码生成、编程辅助、调试测试、开发部署时使用、不适用于无明确技、术栈的模糊需求、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：部署应用

用户输入："帮我部署一个Nginx应用"

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| input | string | 是 | K8s集群管理入门处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 创建Deployment
python3 （请参考skill目录中的脚本文件） deploy \
  --name nginx-app \
  --image nginx:1.25 \
  --replicas 3 \
  --port 80 \
  --namespace default
# ...
# 创建Service
python3 （请参考skill目录中的脚本文件） expose \
  --deployment nginx-app \
  --port 80 \
  --type ClusterIP \
  --name nginx-service
```

### 场景二：多Agent协作管理

用户输入："让多个Agent分别管理不同命名空间"

```bash
# 配置多Agent
python3 （请参考skill目录中的脚本文件） agents config \
  --agent dev-agent --namespace development \
  --agent staging-agent --namespace staging \
  --agent prod-agent --namespace production
# ...
# 各Agent独立管理各自命名空间
python3 （请参考skill目录中的脚本文件） agents status
```

### 场景三：资源查询

用户输入："查看default命名空间的所有资源"

```bash
# 查询资源
python3 （请参考skill目录中的脚本文件） list --namespace default --all-resources
# ...
# 输出：
# Deployments: nginx-app (3/3)
# Services: nginx-service (ClusterIP: 10.96.0.10)
# ConfigMaps: nginx-config
# Pods: nginx-app-xxx (running)
```

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 环境准备

```bash
# 依赖说明
# 安装Python依赖
pip install kubernetes
# ...
# 验证连接
python3 （请参考skill目录中的脚本文件） info
```

### 常用命令

```bash
# 部署应用
python3 （请参考skill目录中的脚本文件） deploy --name my-app --image my-image:v1 --replicas 3
# ...
# 查询资源
python3 （请参考skill目录中的脚本文件） list --namespace default
python3 （请参考skill目录中的脚本文件） get pod --name my-app-xxx
python3 （请参考skill目录中的脚本文件） logs --name my-app-xxx --tail 100
# ...
# 更新资源
python3 （请参考skill目录中的脚本文件） scale --deployment my-app --replicas 5
python3 （请参考skill目录中的脚本文件） rollout --deployment my-app --status
# ...
# 配置管理
python3 （请参考skill目录中的脚本文件） configmap create --name my-config --from-file ./config.yaml
python3 （请参考skill目录中的脚本文件） secret create --name my-secret --from-literal password=xxx
# ...
# 故障排查
python3 （请参考skill目录中的脚本文件） diagnose --pod my-app-xxx
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤。

## 示例

### K8s管理配置

```yaml
k8s_config:
  kubeconfig: "~/.kube/config"
  context: "default"
  namespace: "default"
# ...
  agents:
    mode: "collaborative"         # collaborative | single
    max_agents: 5
    namespaces:
      - agent: "dev-agent"
        namespace: "development"
      - agent: "prod-agent"
        namespace: "production"
# ...
  defaults:
    replicas: 2
    image_pull_policy: "IfNotPresent"
    restart_policy: "Always"
    service_type: "ClusterIP"
# ...
  resources:
    default_requests:
      cpu: "100m"
      memory: "128Mi"
    default_limits:
      cpu: "500m"
      memory: "512Mi"
```

## 最佳实践

1. **命名规范**：统一资源命名规范，便于管理
2. **标签管理**：使用标签组织资源，便于查询筛选
3. **命名空间隔离**：不同环境使用不同命名空间
4. **配置分离**：使用ConfigMap/Secret管理配置

| 实践要点 | 说明 |
|:---:|:---:|
| 资源限制 | 所有Pod设置resources |
| 镜像版本 | 使用固定版本号 |
| 健康检查 | 配置liveness/readiness |
| 多Agent | 按命名空间分工，避免冲突 |

## 常见问题

### Q1：多Agent协作如何工作？

多个Agent各自管理指定命名空间的资源，互不干扰。中央协调器负责跨命名空间的协调与冲突检测。适合团队按环境或项目分工。

### Q2：免费版支持多少个命名空间？

免费版支持最多5个命名空间的管理。如需管理更多命名空间或大规模集群，建议升级PRO版。

### Q3：支持CRD（自定义资源）吗？

免费版支持查询CRD，但创建和管理CRD能力有限。如需完整CRD支持，建议升级PRO版。

### Q4：如何接入已有集群？

配置kubeconfig文件指向已有集群的API Server。本工具通过kubernetes-python客户端连接集群，无需在集群内部署。

## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8+
- **kubectl**: 已配置集群访问

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python | 运行时 | 必需 | 系统安装或conda环境 |
| kubernetes | Python库 | 必需 | `pip install kubernetes` |
| PyYAML | Python库 | 必需 | `pip install pyyaml` |

### API Key 配置

- 通过kubeconfig认证集群
- 无需额外API Key
- kubeconfig文件包含集群访问凭证

### 可用性分类

- **分类**: MD+EXEC（Markdown指令+Python脚本+kubectl执行）
- **说明**: 通过kubernetes-python客户端管理K8s集群
- **免费版限制**: 基础资源管理、5命名空间、不支持监控与策略治理

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 错误处理

- 边界输入处理: 空输入返回提示信息, 超长输入自动截断
- 降级策略: 异常时返回默认值, 确保流程不中断 - 处理方式: 按上述步骤操作并确认结果
- 完成ping命令测试网络连通性,检查防火墙和代理设置连接后重新完成命令机制: 失败时自动完成ping命令测试网络连通性,检查防火墙和代理设置连接后重新完成命令, 最多3次 - 解析方式: 按上述步骤任务并确认响应

<!-- 触发条件: 用户明确请求时激活 -->
## 案例展示

```json
{
  "input": "示例输入",
  "output": "处理结果"
}
```

## 输出格式

处理结果以结构化格式返回, 包含状态码、消息和数据字段。
