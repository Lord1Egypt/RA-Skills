# kubernetes-devops-toolkit

## 描述

**中文**: Kubernetes DevOps 工具包 - 完整的K8s集群管理、部署、监控和故障排查工具集

**English**: Kubernetes DevOps Toolkit - Complete K8s cluster management, deployment, monitoring and troubleshooting toolset

## 功能

- **集群管理**: 连接、配置、切换多个K8s集群
- **部署管理**: Deployment/Service/Ingress的创建、更新、回滚
- **资源监控**: Pod/Node/Namespace资源使用实时监控
- **日志收集**: 多Pod日志聚合和查询
- **故障排查**: 自动诊断常见问题并提供解决方案
- **Helm支持**: Chart管理和Release生命周期管理

## 使用场景

- 开发和生产环境的K8s集群运维
- CI/CD流水线中的K8s部署
- 故障排查和性能优化
- 多集群统一管理

## 依赖

- Python 3.8+
- kubernetes-client
- helm (可选)
- kubectl (可选)
