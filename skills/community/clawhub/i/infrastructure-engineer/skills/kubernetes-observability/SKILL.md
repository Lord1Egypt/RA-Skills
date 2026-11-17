---
name: kubernetes-observability
description: K8s 可观测性：日志聚合、指标采集、分布式追踪、告警规则
source:
  type: derived
  repo: skills-repo/infrastructure-engineer
  path: skills/kubernetes-observability/SKILL.md
  url: https://skills.sh/dynatrace/dynatrace-for-ai/dt-obs-kubernetes
  version: 1.0.0
  updated: 2026-07-31
metadata:
  author: hope
  category: 云基础设施
  platform: Kubernetes
  difficulty: 进阶
  version: 1.0.0
  created: 2026-07-31
tags:
  - kubernetes
  - observability
  - monitoring
  - logging
  - tracing
---

# Kubernetes Observability — K8s 可观测性

> 为 Kubernetes 集群搭建完整的可观测性体系，覆盖日志聚合、指标采集、分布式追踪和智能告警，确保集群运行状态透明可控。

## 能力

- **日志聚合**：配置 Fluentd/Fluent Bit 收集容器日志，Loki/Elasticsearch 存储和查询
- **指标采集**：Prometheus + Grafana 采集集群和应用的 CPU、内存、网络、磁盘指标
- **分布式追踪**：Jaeger/Tempo 追踪微服务调用链，定位延迟瓶颈
- **告警规则**：基于 PromQL 编写告警规则，配置 Alertmanager 通知渠道
- **仪表盘**：设计 Grafana 仪表盘，覆盖集群健康、资源利用、应用性能

## 使用方式

在 Claude Code 中使用 `/kubernetes-observability` 调用。

```
/kubernetes-observability 为这个 K8s 集群配置 Prometheus 监控
/kubernetes-observability 设计一套 Pod 资源告警规则
/kubernetes-observability 排查为什么这个 Service 的延迟突然升高
```

## 工作流

1. **评估现状** — 检查集群当前的可观测性覆盖情况，识别盲区
2. **部署采集器** — 安装和配置 Prometheus、Grafana、Loki、Jaeger 等组件
3. **定义指标** — 确定关键指标（RED/USE 方法），配置采集规则
4. **设置告警** — 编写告警规则，配置分级通知（警告→紧急→关键）
5. **仪表盘** — 设计运维仪表盘，确保关键指标一目了然

## 适用场景

- 新集群上线前的可观测性基础设施搭建
- 现有集群的监控盲区排查和补全
- 微服务架构下的分布式追踪配置
- 独立开发者运维个人 K8s 集群

## 限制

- 需要 K8s 集群的管理员权限才能部署监控组件
- 大规模集群的指标采集可能有性能开销
- 不包含 APM（应用性能监控）的代码级 instrumentation
- 告警规则需要根据实际业务调整阈值

## 相关参考（Playbook）

K8s 可观测性四支柱与黄金信号审查框架 → [references/kubernetes-observability.md](../../references/kubernetes-observability.md)。