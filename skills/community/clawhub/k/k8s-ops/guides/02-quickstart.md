# k8s-ops 快速开始

## 基本用法

### 查看集群信息

```bash
# 查看集群信息
kubectl cluster-info

# 查看节点
kubectl get nodes

# 查看所有命名空间
kubectl get namespaces
```

### Pod 管理

```bash
# 列出所有 Pod
kubectl get pods

# 查看 Pod 详情
kubectl describe pod <pod-name>

# 查看 Pod 日志
kubectl logs <pod-name>

# 进入 Pod
kubectl exec -it <pod-name> -- /bin/bash

# 端口转发
kubectl port-forward <pod-name> 8080:80
```

### Deployment 管理

```bash
# 查看 Deployment
kubectl get deployments

# 扩缩容
kubectl scale deployment <deployment-name> --replicas=3

# 滚动更新
kubectl set image deployment/<deployment-name> <container-name>=<new-image>

# 查看更新状态
kubectl rollout status deployment/<deployment-name>

# 回滚
kubectl rollout undo deployment/<deployment-name>
```

### Service 管理

```bash
# 查看 Service
kubectl get services

# 查看 Service 详情
kubectl describe service <service-name>

# 查看 Endpoints
kubectl get endpoints <service-name>
```

## 使用 k8s-ops 工具

### 集群健康检查

```bash
# 检查集群整体健康状态
kubectl get componentstatuses

# 检查节点状态
kubectl get nodes -o wide

# 检查系统组件
kubectl get pods -n kube-system
```

### 资源监控

```bash
# 查看节点资源使用
kubectl top nodes

# 查看 Pod 资源使用
kubectl top pods

# 按命名空间查看
kubectl top pods -n <namespace>
```

### 安全审计

```bash
# 检查 RBAC 权限
kubectl auth can-i --list

# 查看集群角色
kubectl get clusterroles

# 查看角色绑定
kubectl get clusterrolebindings
```

## 常见场景

### 部署应用

```bash
# 创建 Deployment
kubectl create deployment nginx --image=nginx

# 暴露服务
kubectl expose deployment nginx --port=80 --type=LoadBalancer

# 查看状态
kubectl get pods,svc
```

### 调试应用

```bash
# 查看 Pod 事件
kubectl describe pod <pod-name>

# 查看容器日志
kubectl logs <pod-name> -c <container-name>

# 进入容器调试
kubectl exec -it <pod-name> -- /bin/sh
```

### 扩缩容

```bash
# 手动扩缩容
kubectl scale deployment <deployment-name> --replicas=5

# 自动扩缩容
kubectl autoscale deployment <deployment-name> --min=3 --max=10 --cpu-percent=80
```

## 下一步

- 学习 [高级用法](03-advanced-usage.md) 了解更多功能
- 查看 [故障排查](../troubleshooting.md) 解决常见问题
- 访问 [Kubernetes 官方文档](https://kubernetes.io/docs/) 获取完整参考
