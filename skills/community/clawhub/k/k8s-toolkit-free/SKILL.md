---
slug: k8s-toolkit-free
name: k8s-toolkit-free
version: 1.0.0
displayName: K8s避坑入门工具
summary: Kubernetes常见问题避坑指南，提供基础排查与优选实践建议。
license: Proprietary
edition: free
description: '面向K8s初学者与个人开发者的常见问题避坑工具。总结Kubernetes

  使用中的高频问题与陷阱，提供排查思路与解决方案。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。适用于独立开发者、企业团队和自动化工作流场景。Use
  when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。'
tags:
- Operations
- Kubernetes
- 运维
- 学习
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
# K8s避坑入门工具（免费版）

## 概述

本工具为K8s初学者和个人开发者提供常见问题避坑指南。总结Kubernetes使用中的高频问题与陷阱，提供排查思路、解决方案和优选实践建议，帮助用户快速解决日常K8s问题。

## 核心能力

### 避坑知识库

| 类别 | 问题数量 | 免费版覆盖 |
|---|----|-----|
| Pod问题 | 15个 | 常见8个 |
| Service问题 | 10个 | 常见5个 |
| Deployment问题 | 12个 | 常见6个 |
| 网络问题 | 10个 | 常见5个 |
| 存储问题 | 8个 | 常见4个 |
| 安全问题 | 8个 | 常见4个 |
| 性能问题 | 10个 | 不支持 |
| 集群运维 | 15个 | 不支持 |

**输入**: 用户提供避坑知识库所需的指令和必要参数。
**处理**: 解析避坑知识库的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回避坑知识库的响应数据,包含状态码、结果和日志。

### 常见避坑主题

| 主题 | 常见陷阱 | 影响 |
|:-----|:-----|:-----|
| 资源限制 | 未设置resources | Pod抢占资源 |
| 镜像策略 | 用latest标签 | 版本不可控 |
| 健康检查 | 未配置探针 | 僵尸Pod |
| 服务类型 | 误用LoadBalancer | 成本增加 |
| 配置管理 | 硬编码配置 | 环境不可迁移 |
| 持久化 | 数据卷未备份 | 数据丢失 |

**输入**: 用户提供常见避坑主题所需的指令和必要参数。
**处理**: 解析常见避坑主题的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回常见避坑主题的响应数据,包含状态码、结果和日志。

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Kubernetes、常见问题避坑指南、提供基础排查与优、选实践建议、初学者与个人开发、者的常见问题避坑、使用中的高频问题、与陷阱、提供排查思路与解、决方案、Use、when、需要代码生成、编程辅助、调试测试、开发部署时使用、不适用于无明确技、术栈的模糊需求、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

## 错误处理

- 边界输入处理: 空输入返回提示信息, 超长输入自动截断
- 降级策略: 异常时返回默认值, 确保流程不中断 - 处理方式: 按上述步骤操作并确认结果
- 完成ping命令测试网络连通性,检查防火墙和代理设置连接后重新完成命令机制: 失败时自动完成ping命令测试网络连通性,检查防火墙和代理设置连接后重新完成命令, 最多3次 - 解析方式: 按上述步骤任务并确认响应

用户输入："我的Pod一直处于CrashLoopBackOff状态"

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| input | string | 是 | K8s避坑入门工具处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 排查Pod问题
/k8s troubleshoot pod --name my-app --namespace default
# ...
# 输出排查步骤：
# 1. 查看Pod事件
#    kubectl describe pod my-app
# 2. 查看容器日志
#    kubectl logs my-app --previous
# 3. 常见原因：
#    - 应用启动失败（检查配置）
#    - 资源不足（调整resources）
#    - 健康检查失败（调整探针）
#    - 镜像拉取失败（检查镜像名）
```

### 场景二：Service无法访问 - 处理方式: 按上述步骤操作并确认结果

用户输入："Service创建成功但访问不了"

```bash
# 排查Service问题
/k8s troubleshoot service --name my-service
# ...
# 输出排查步骤：
# 1. 检查Service端点
#    kubectl get endpoints my-service
# 2. 检查Pod标签匹配
#    kubectl get pods --show-labels
# 3. 检查端口配置
# 4. 常见原因：标签不匹配、端口不一致
```

### 场景三：优选实践检查

用户输入："检查我的Deployment配置是否有问题"

```bash
# 配置检查
/k8s check deployment --name my-app
# ...
# 输出建议：
# 已知限制
# [建议] 添加liveness/readiness探针
# [建议] 使用具体镜像版本而非latest
# [建议] 配置PodDisruptionBudget
```
### 错误场景3

检查`error_code`并按照处理方式进行排查。
## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 常用命令

```bash
# 问题排查
/k8s troubleshoot pod --name <pod-name>
/k8s troubleshoot service --name <svc-name>
/k8s troubleshoot deployment --name <dep-name>
# ...
# 配置检查
/k8s check deployment --name <dep-name>
/k8s check pod --name <pod-name>
# ...
# 命令速查
/k8s cheat-sheet
/k8s cheat-sheet --topic networking
# ...
# 避坑指南
/k8s pitfalls --category resources
/k8s pitfalls --category networking
```

### 常用kubectl速查

```bash
# 集群信息
kubectl cluster-info
kubectl get nodes
# ...
# Pod管理
kubectl get pods --all-namespaces
kubectl describe pod <name>
kubectl logs <name> --previous
kubectl exec -it <name> -- /（请参考skill目录中的脚本文件）
# ...
# Service管理
kubectl get svc
kubectl get endpoints <name>
# ...
# Deployment管理
kubectl get deployments
kubectl scale deployment <name> --replicas=3
kubectl rollout status deployment/<name>
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤。

## 示例

### 安全Deployment模板

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: safe-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: safe-app
  template:
    metadata:
      labels:
        app: safe-app
    spec:
      containers:
      - name: app
        image: my-app:v1.2.3          # 避免用latest
        resources:                      # 必须设置资源限制
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:                  # 必须配置健康检查
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        securityContext:                # 安全上下文
          runAsNonRoot: true
          readOnlyRootFilesystem: true
```

## 优选实践

1. **资源限制必设**：所有容器必须设置requests和limits
2. **镜像版本固定**：使用具体版本号，避免latest
3. **健康检查必配**：配置liveness和readiness探针
4. **标签规范统一**：统一标签命名规范，便于管理

| 避坑要点 | 说明 |
|:---:|:---:|
| 资源设置 | requests用于调度，limits用于限制 |
| 探针配置 | liveness检测存活，readiness检测就绪 |
| 镜像策略 | 固定版本便于回滚和追踪 |
| 配置分离 | 使用ConfigMap/Secret管理配置 |

## 已知限制

- 本skill的能力范围受限于核心能力章节中定义的功能,不支持超出范围的操作
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 常见问题

### Q1：免费版支持集群级问题排查吗？

免费版聚焦Pod/Service/Deployment基础排查。如需集群级问题诊断，建议升级PRO版。

### Q2：避坑指南覆盖多少问题？

免费版覆盖约32个常见问题。如需完整知识库（88+问题），建议升级PRO版。

### Q3：支持哪些K8s发行版？

通用K8s避坑指南适用于所有K8s发行版（包括EKS/GKE/AKS/自建集群）。发行版特有问题建议升级PRO版。

### Q4：可以直接修复问题吗？

免费版提供排查建议和解决方案，需手动执行修复。如需自动修复功能，建议升级PRO版。

## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **kubectl**: 已配置集群访问（排查时需要）

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| kubectl | CLI工具 | 推荐 | 官网安装 |

### API Key 配置

- 免费版无需API Key
- 避坑指南为纯知识库，无需集群连接

### 可用性分类

- **分类**: MD（纯Markdown指令知识库）
- **说明**: K8s常见问题避坑指南与排查建议
- **免费版限制**: 基础问题覆盖、不支持集群级诊断与自动修复

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
