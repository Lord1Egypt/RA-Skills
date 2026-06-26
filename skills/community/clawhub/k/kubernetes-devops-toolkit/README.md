# Kubernetes DevOps Toolkit

**中文**: Kubernetes DevOps 工具包 - 完整的K8s集群管理、部署、监控和故障排查工具集

**English**: Kubernetes DevOps Toolkit - Complete K8s cluster management, deployment, monitoring and troubleshooting toolset

## 🚀 功能特性

| 功能 | 描述 |
|------|------|
| 集群管理 | 连接、配置、切换多个K8s集群 |
| 部署管理 | Deployment/Service/Ingress的创建、更新、回滚 |
| 资源监控 | Pod/Node/Namespace资源使用实时监控 |
| 日志收集 | 多Pod日志聚合和查询 |
| 故障排查 | 自动诊断常见问题并提供解决方案 |
| Helm支持 | Chart管理和Release生命周期管理 |

## 📦 安装

```bash
pip install -r requirements.txt
```

### 前置依赖

- Python 3.8+
- kubectl (推荐 v1.25+)
- Helm (可选，用于Helm操作)
- 有效的kubeconfig文件

## 🎯 快速开始

### 1. 配置集群连接

```python
from kubernetes_devops_toolkit import K8sManager

# 使用现有kubeconfig
manager = K8sManager(kubeconfig_path="~/.kube/config")

# 或连接特定集群
manager.switch_context("production-cluster")
```

### 2. 查看集群状态

```python
# 获取所有节点
nodes = manager.get_nodes()
print(f"集群节点数: {len(nodes)}")

# 查看Pod状态
pods = manager.get_pods(namespace="default")
for pod in pods:
    print(f"{pod.name}: {pod.status}")
```

### 3. 部署应用

```python
# 创建Deployment
deployment = manager.create_deployment(
    name="my-app",
    image="nginx:latest",
    replicas=3,
    namespace="default"
)
```

### 4. 监控资源

```python
# 实时监控Pod资源使用
manager.watch_pod_resources(
    namespace="default",
    interval=5
)
```

## 📚 详细用法

### 集群管理

```python
# 列出所有上下文
contexts = manager.list_contexts()

# 切换上下文
manager.switch_context("staging")

# 验证集群连接
if manager.is_connected():
    version = manager.get_cluster_version()
    print(f"K8s版本: {version}")
```

### 故障排查

```python
# 自动诊断Pod问题
diagnosis = manager.diagnose_pod(
    pod_name="my-app-123",
    namespace="default"
)
print(diagnosis.report)

# 获取事件日志
events = manager.get_events(
    namespace="default",
    field_selector="type=Warning"
)
```

### Helm操作

```python
from kubernetes_devops_toolkit import HelmManager

helm = HelmManager()

# 安装Chart
helm.install(
    release_name="my-release",
    chart="bitnami/nginx",
    namespace="default",
    values={"replicaCount": 3}
)

# 升级Release
helm.upgrade(
    release_name="my-release",
    values={"image.tag": "2.0"}
)

# 回滚
helm.rollback(release_name="my-release", revision=1)
```

## 🧪 测试

```bash
# 运行测试
pytest tests/

# 带覆盖率报告
pytest tests/ --cov=kubernetes_devops_toolkit
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和PR！
