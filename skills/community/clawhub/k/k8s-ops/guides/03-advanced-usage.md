# k8s-ops 高级用法

## 多集群管理

### 切换集群上下文

```bash
# 查看所有上下文
kubectl config get-contexts

# 切换上下文
kubectl config use-context <context-name>

# 查看当前上下文
kubectl config current-context
```

### 多集群操作

```bash
# 在特定集群执行命令
kubectl --context=<context-name> get pods

# 设置默认集群
kubectl config set-context --current --namespace=<namespace>
```

## 命名空间管理

### 创建命名空间

```bash
# 创建命名空间
kubectl create namespace <namespace-name>

# 查看命名空间
kubectl get namespaces
```

### 命名空间资源隔离

```bash
# 在特定命名空间创建资源
kubectl create deployment nginx --image=nginx -n <namespace>

# 查看特定命名空间的资源
kubectl get pods -n <namespace>

# 设置默认命名空间
kubectl config set-context --current --namespace=<namespace>
```

## 高级部署策略

### 滚动更新策略

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  template:
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
```

### 蓝绿部署

```bash
# 创建蓝色部署
kubectl create deployment nginx-blue --image=nginx:1.24

# 创建绿色部署
kubectl create deployment nginx-green --image=nginx:1.25

# 切换流量
kubectl patch service nginx -p '{"spec":{"selector":{"deployment":"nginx-green"}}}'
```

### 金丝雀发布

```bash
# 创建金丝雀部署
kubectl create deployment nginx-canary --image=nginx:1.25

# 设置流量分配（10%）
kubectl patch service nginx -p '{"spec":{"trafficPolicy":{"loadBalancer":{"simple":"ROUND_ROBIN"}}}}'
```

## 资源配额管理

### 设置资源配额

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: <namespace>
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
    pods: "20"
```

### 查看资源配额

```bash
# 查看命名空间配额
kubectl get resourcequota -n <namespace>

# 查看配额使用情况
kubectl describe resourcequota <quota-name> -n <namespace>
```

## 网络策略

### 创建网络策略

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: <namespace>
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### 允许特定流量

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend
  namespace: <namespace>
spec:
  podSelector:
    matchLabels:
      app: backend
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
```

## 存储管理

### 持久卷管理

```bash
# 查看持久卷
kubectl get pv

# 查看持久卷声明
kubectl get pvc

# 创建持久卷
kubectl apply -f pv.yaml
```

### 存储类

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
reclaimPolicy: Retain
volumeBindingMode: WaitForFirstConsumer
```

## 监控和日志

### 集成 Prometheus

```bash
# 安装 Prometheus
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/main/bundle.yaml

# 查看 Prometheus 状态
kubectl get pods -n default -l app.kubernetes.io/name=prometheus
```

### 日志收集

```bash
# 查看 Pod 日志
kubectl logs <pod-name> -f

# 查看前一个容器日志
kubectl logs <pod-name> --previous

# 查看所有 Pod 日志
kubectl logs -l app=<app-name> --all-containers
```

## 安全最佳实践

### Pod 安全策略

```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'persistentVolumeClaim'
    - 'secret'
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
```

### RBAC 配置

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: <namespace>
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

## 自动化脚本

### 批量操作脚本

```bash
#!/bin/bash
# 批量重启所有 Deployment
for deploy in $(kubectl get deployments -o jsonpath='{.items[*].metadata.name}'); do
  kubectl rollout restart deployment/$deploy
done
```

### 健康检查脚本

```bash
#!/bin/bash
# 检查所有节点状态
kubectl get nodes | grep -v "Ready" && echo "WARNING: Some nodes are not ready"

# 检查所有 Pod 状态
kubectl get pods --all-namespaces | grep -v "Running" && echo "WARNING: Some pods are not running"
```

## 下一步

- 查看 [故障排查](../troubleshooting.md) 解决常见问题
- 访问 [Kubernetes 官方文档](https://kubernetes.io/docs/) 获取完整参考
- 参与 [Kubernetes 讨论](https://discuss.kubernetes.io/)
