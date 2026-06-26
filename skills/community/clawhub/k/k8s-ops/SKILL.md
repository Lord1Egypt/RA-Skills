---
name: k8s-ops
description: Kubernetes operations plugin — 32 tools for cluster management, monitoring, troubleshooting, and security auditing
version: 2.1.1
metadata:
  openclaw:
    requires:
      bins:
        - kubectl
    homepage: https://github.com/CN-big-cabbage/k8s-ops-agent
---

# k8s-ops

Kubernetes operations plugin for OpenClaw. Provides 32 tools covering the full lifecycle of K8s cluster management.

## ⚠️ 安全警告

**重要：本插件具有强大的集群操作能力，使用前请仔细阅读以下安全建议：**

1. **凭据安全**：kubeconfig 文件包含集群端点、用户身份、令牌和客户端证书等敏感信息。请勿在不安全的环境中存储或共享 kubeconfig 文件。

2. **最小权限原则**：建议使用最小权限的 kubeconfig，避免使用 cluster-admin 凭据。建议先在非生产环境中测试。

3. **操作风险**：exec、rollout、scale、restart、namespace 等操作可能对生产集群造成破坏性影响。请在执行前确认操作目标。

4. **SSH 访问**：配置中的 `hosts` 字段用于 SSH 主机访问（sys-monitor 工具），请仅配置受信任的主机，避免在生产环境中使用密码认证。

## Tools

- **Pod Management**: list, inspect, exec, logs, port-forward
- **Deployments**: status, rollout, scale, restart
- **Services & Networking**: services, ingress, gateway, network policies
- **Workloads**: jobs, cronjobs, daemonsets, statefulsets, HPA
- **Storage**: PV/PVC management
- **Security**: RBAC audit, security scanning, pod security policies
- **Observability**: events, metrics, health checks, cost analysis
- **Troubleshooting**: diagnostics, topology, event analysis
- **Advanced**: CRDs, Helm releases, PDB, YAML generation, namespace management

## Requirements

- `kubectl` installed and configured with cluster access
- Valid kubeconfig (defaults to `~/.kube/config`)
- **建议**：使用最小权限的 ServiceAccount，避免使用集群管理员凭据

## Configuration

Optional plugin config:

| Field | Description | 安全建议 |
|-------|-------------|----------|
| `kubeconfigPath` | Custom path to kubeconfig file | 确保文件权限为 600，仅当前用户可读 |
| `defaultContext` | Default Kubernetes context to use | 建议使用非生产环境的 context |
| `hosts` | SSH target hosts for sys-monitor tool | 仅配置受信任的主机，建议使用 SSH 密钥认证 |

## 最佳实践

1. **环境隔离**：建议为不同环境（开发、测试、生产）使用不同的 kubeconfig
2. **审计日志**：启用 Kubernetes 审计日志，记录所有操作
3. **定期轮换**：定期轮换 kubeconfig 中的凭据和令牌
4. **权限审查**：定期审查 RBAC 权限，移除不必要的权限
