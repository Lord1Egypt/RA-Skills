# K8sSkill 故障排查手册

## 快速诊断流程

### 1. Pod问题诊断流程

```
用户: "Pod为什么崩溃"
    ↓
K8sSkill执行分析
    ↓
检查Pod Phase
    ├── Pending → 检查调度问题
    ├── Running → 检查容器状态
    ├── Failed → 检查终止原因
    └── Succeeded → Job完成（正常）
    ↓
输出诊断报告
```

### 2. 服务连通性诊断流程

```
用户: "服务访问不了"
    ↓
K8sSkill执行分析
    ↓
检查Service
    ├── Endpoints为空 → 检查Pod标签/状态
    ├── Endpoints正常 → 检查网络策略
    └── 外部访问 → 检查Ingress/NodePort
    ↓
输出诊断报告
```

## 常见问题排查

### Pod相关

#### 问题1: Pod一直处于Pending状态

**症状：**
```
NAME         READY   STATUS    RESTARTS   AGE
my-pod       0/1     Pending   0          10m
```

**排查步骤：**

1. **查看Pod事件**
```bash
kubectl describe pod my-pod
```

2. **检查调度失败原因**
```
Events:
  Type     Reason            Age   From               Message
  ----     ------            ----  ----               -------
  Warning  FailedScheduling  10m   default-scheduler  0/3 nodes are available: 3 Insufficient memory
```

**常见原因及解决：**

| 原因 | 错误信息 | 解决方案 |
|------|---------|---------|
| 资源不足 | Insufficient cpu/memory | 减少请求资源或扩容节点 |
| 亲和性冲突 | node affinity | 调整亲和性规则 |
| 污点阻止 | Taint | 添加容忍或移除污点 |
| PVC未绑定 | unbound immediate PersistentVolumeClaim | 检查存储类或手动创建PV |

#### 问题2: CrashLoopBackOff

**症状：**
```
NAME         READY   STATUS             RESTARTS   AGE
my-pod       0/1     CrashLoopBackOff   5          10m
```

**排查步骤：**

1. **查看容器日志**
```bash
kubectl logs my-pod --previous
```

2. **检查终止原因**
```bash
kubectl get pod my-pod -o yaml | grep -A 10 lastState
```

**常见原因：**

| 终止原因 | 含义 | 解决方案 |
|---------|------|---------|
| OOMKilled | 内存溢出 | 增加内存限制 |
| Error | 应用错误 | 查看日志修复代码 |
| Completed | 正常退出 | 检查重启策略 |

#### 问题3: ImagePullBackOff

**症状：**
```
NAME         READY   STATUS             RESTARTS   AGE
my-pod       0/1     ImagePullBackOff   0          5m
```

**排查步骤：**

1. **检查镜像是否存在**
```bash
docker pull your-image:tag
```

2. **检查镜像仓库认证**
```bash
kubectl get secret regcred
```

3. **检查网络连通性**
```bash
kubectl run test --image=busybox --rm -it -- ping registry.example.com
```

### Deployment相关

#### 问题1: 滚动更新停滞

**症状：**
```
NAME       READY   UP-TO-DATE   AVAILABLE   AGE
my-deploy  3/5     2            3           1h
```

**排查步骤：**

1. **查看Deployment状态**
```bash
kubectl rollout status deployment/my-deploy
```

2. **检查新Pod状态**
```bash
kubectl get pods -l app=my-app
kubectl describe pod new-pod-xxx
```

3. **查看ReplicaSet**
```bash
kubectl get rs -l app=my-app
```

**常见原因：**
- 新Pod启动失败（CrashLoopBackOff）
- 健康检查失败
- 资源配额不足
- 进度超时（默认10分钟）

#### 问题2: 可用副本不足

**症状：**
```
NAME       READY   UP-TO-DATE   AVAILABLE   AGE
my-deploy  2/5     5            2           1h
```

**排查步骤：**

1. **检查Pod状态**
```bash
kubectl get pods -l app=my-app
```

2. **检查资源配额**
```bash
kubectl describe resourcequota
```

3. **检查节点资源**
```bash
kubectl top nodes
kubectl describe nodes
```

### Service相关

#### 问题1: Service端点为空

**症状：**
```
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
my-service   ClusterIP   10.96.123.45    <none>        80/TCP    1h

# Endpoints为空
kubectl get endpoints my-service
NAME         ENDPOINTS   AGE
my-service   <none>      1h
```

**排查步骤：**

1. **检查Service选择器**
```bash
kubectl get svc my-service -o yaml | grep selector -A 3
```

2. **检查Pod标签**
```bash
kubectl get pods --show-labels
```

3. **验证选择器匹配**
```bash
kubectl get pods -l app=my-app,version=v1
```

**解决方案：**

| 问题 | 检查命令 | 修复方法 |
|------|---------|---------|
| 标签不匹配 | get pods --show-labels | 修改Pod标签或Service选择器 |
| Pod未就绪 | get pods | 检查Pod健康状态 |
| 选择器语法错误 | get svc -o yaml | 修正选择器配置 |

#### 问题2: 无法从外部访问Service

**排查步骤：**

1. **检查Service类型**
```bash
kubectl get svc my-service
```

2. **ClusterIP类型测试**
```bash
kubectl run test --image=busybox --rm -it -- wget -O- http://my-service
```

3. **NodePort类型检查**
```bash
kubectl get svc my-service
# 检查节点IP:NodePort
```

4. **LoadBalancer类型检查**
```bash
kubectl get svc my-service
# 检查EXTERNAL-IP
```

## K8sSkill诊断命令速查

### 自然语言 → Kubectl命令映射

| 自然语言 | K8sSkill执行 | 对应Kubectl命令 |
|---------|-------------|----------------|
| "检查Pod状态" | PodAnalyzer | `kubectl get pods` |
| "查看Pod日志" | 日志获取 | `kubectl logs pod-name` |
| "检查Deployment" | DeploymentAnalyzer | `kubectl get deploy` |
| "查看Service端点" | ServiceAnalyzer | `kubectl get endpoints` |
| "检查所有资源" | 全量分析 | `kubectl get all` |
| "查看事件" | EventAnalyzer | `kubectl get events` |

### 快速修复命令

```bash
# Pod问题
kubectl logs pod-name --previous          # 查看崩溃前日志
kubectl describe pod pod-name             # 查看Pod详情
kubectl delete pod pod-name --force       # 强制删除卡住的Pod

# Deployment问题  
kubectl rollout status deploy/name        # 查看滚动更新状态
kubectl rollout undo deploy/name          # 回滚Deployment
kubectl set resources deploy/name --limits=memory=512Mi  # 调整资源

# Service问题
kubectl get endpoints service-name        # 检查端点
kubectl get pods -l app=label             # 检查标签匹配
kubectl port-forward svc/name 8080:80     # 本地端口转发测试
```

## 高级诊断技巧

### 1. 使用临时容器调试

```bash
kubectl debug pod-name -it --image=busybox --target=container-name
```

### 2. 网络连通性测试

```bash
# 创建测试Pod
kubectl run test --image=nicolaka/netshoot --rm -it -- bash

# 测试Service连通性
curl http://service-name.namespace.svc.cluster.local

# 测试DNS解析
nslookup kubernetes.default
```

### 3. 资源使用分析

```bash
# 查看资源使用
kubectl top pods
kubectl top nodes

# 查看资源配额
kubectl describe resourcequota

# 查看LimitRange
kubectl describe limitrange
```

## 参考资源

- [Kubernetes故障排查官方指南](https://kubernetes.io/docs/tasks/debug/)
- [Kubernetes最佳实践](https://kubernetes.io/docs/concepts/configuration/overview/)
- [Kubernetes Troubleshooting](https://kubernetes.io/docs/tasks/debug-application-cluster/)
