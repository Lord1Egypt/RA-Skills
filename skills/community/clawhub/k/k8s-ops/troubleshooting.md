# k8s-ops 故障排查

## 安装问题

### kubectl 未安装

**症状**: `kubectl: command not found`

**解决**:
```bash
# macOS
brew install kubectl

# Linux (curl)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# 验证安装
kubectl version --client
```

### kubeconfig 配置错误

**症状**: `The connection to the server localhost:8080 was refused`

**解决**:
```bash
# 检查 kubeconfig
kubectl config view

# 设置正确的 kubeconfig
export KUBECONFIG=/path/to/your/kubeconfig

# 或使用默认路径
mkdir -p ~/.kube
cp /path/to/your/kubeconfig ~/.kube/config
```

## 连接问题

### 集群连接失败

**症状**: `Unable to connect to the server`

**解决**:
```bash
# 检查集群状态
kubectl cluster-info

# 检查网络连接
ping <cluster-ip>

# 检查防火墙规则
# 确保 6443 端口开放
```

### 认证失败

**症状**: `Unauthorized` 或 `Forbidden`

**解决**:
```bash
# 检查当前上下文
kubectl config current-context

# 切换到正确的上下文
kubectl config use-context <context-name>

# 检查 RBAC 权限
kubectl auth can-i --list
```

## 权限问题

### RBAC 权限不足

**症状**: `Error from server (Forbidden)`

**解决**:
```bash
# 检查当前用户权限
kubectl auth can-i --list

# 创建 ClusterRoleBinding
kubectl create clusterrolebinding admin-binding \
  --clusterrole=cluster-admin \
  --user=<your-user>

# 或创建 RoleBinding（命名空间级别）
kubectl create rolebinding admin-binding \
  --clusterrole=admin \
  --user=<your-user> \
  --namespace=<namespace>
```

## 资源问题

### Pod 启动失败

**症状**: Pod 状态为 `CrashLoopBackOff` 或 `Error`

**解决**:
```bash
# 查看 Pod 详情
kubectl describe pod <pod-name>

# 查看 Pod 日志
kubectl logs <pod-name>

# 查看前一个容器的日志（如果崩溃）
kubectl logs <pod-name> --previous

# 检查资源限制
kubectl top pod
```

### 资源不足

**症状**: `Insufficient cpu` 或 `Insufficient memory`

**解决**:
```bash
# 查看节点资源使用情况
kubectl top nodes

# 查看 Pod 资源请求
kubectl describe pod <pod-name> | grep -A5 "Limits"

# 调整资源请求
kubectl patch deployment <deployment-name> -p \
  '{"spec":{"template":{"spec":{"containers":[{"name":"<container-name>","resources":{"requests":{"memory":"256Mi","cpu":"250m"}}}]}}}}'
```

## 网络问题

### Service 无法访问

**症状**: 无法通过 Service 访问 Pod

**解决**:
```bash
# 检查 Service 状态
kubectl get svc

# 检查 Endpoints
kubectl get endpoints <service-name>

# 检查 Pod 标签是否匹配
kubectl get pods --show-labels

# 测试 Service 连通性
kubectl run -it --rm debug --image=busybox --restart=Never -- wget -qO- http://<service-name>:<port>
```

### Ingress 配置问题

**症状**: Ingress 无法路由流量

**解决**:
```bash
# 检查 Ingress 状态
kubectl get ingress

# 查看 Ingress 详情
kubectl describe ingress <ingress-name>

# 检查 Ingress Controller 日志
kubectl logs -n <ingress-namespace> <ingress-pod>
```

## 存储问题

### PVC 绑定失败

**症状**: PVC 状态为 `Pending`

**解决**:
```bash
# 查看 PVC 状态
kubectl get pvc

# 查看 PVC 详情
kubectl describe pvc <pvc-name>

# 检查 PV 是否可用
kubectl get pv

# 检查 StorageClass
kubectl get storageclass
```

## 调试技巧

### 获取集群信息

```bash
# 集群信息
kubectl cluster-info

# 节点信息
kubectl get nodes -o wide

# 所有资源
kubectl get all --all-namespaces
```

### 查看事件

```bash
# 查看所有事件
kubectl get events --all-namespaces

# 按时间排序
kubectl get events --sort-by='.lastTimestamp'
```

### 资源使用情况

```bash
# 节点资源使用
kubectl top nodes

# Pod 资源使用
kubectl top pods

# 按命名空间查看
kubectl top pods -n <namespace>
```

## 获取帮助

如果以上方法都无法解决问题：

1. 查看 [Kubernetes 官方文档](https://kubernetes.io/docs/)
2. 搜索 [Kubernetes Issues](https://github.com/kubernetes/kubernetes/issues)
3. 参与 [Kubernetes 讨论](https://discuss.kubernetes.io/)
