# K3s 集群故障排查指南

## 常见问题

### 1. 节点 NotReady

**症状:**
```
kubectl get nodes
NAME          STATUS     ROLES           AGE   VERSION
k8s-master    NotReady   control-plane   5m    v1.28.0
```

**排查步骤:**

1. 检查 kubelet 状态
```bash
systemctl status kubelet
journalctl -u kubelet -n 50 --no-pager
```

2. 检查网络插件
```bash
kubectl get pods -n kube-system | grep flannel
kubectl describe pod <flannel-pod> -n kube-system
```

3. 检查 CNI 配置
```bash
ls -la /etc/cni/net.d/
cat /etc/cni/net.d/10-flannel.conflist
```

**常见原因:**
- Flannel 未正确部署
- CNI 配置文件缺失
- 网络接口配置错误（eth0 vs ens192）

**解决方案:**
```bash
# 重新创建 CNI 配置
cat > /etc/cni/net.d/10-flannel.conflist << 'EOF'
{
  "name": "cbr0",
  "cniVersion": "0.3.1",
  "plugins": [
    {
      "type": "flannel",
      "delegate": {
        "hairpinMode": true,
        "isDefaultGateway": true
      }
    }
  ]
}
EOF

# 重启 kubelet
systemctl restart kubelet
```

### 2. Pod Pending

**症状:**
```
kubectl get pods -n kube-system
NAME                         READY   STATUS    RESTARTS   AGE
coredns-xxxxx                0/1     Pending   0          10m
```

**排查步骤:**

```bash
# 查看 Pod 详情
kubectl describe pod coredns-xxxxx -n kube-system

# 查看调度事件
kubectl describe pod coredns-xxxxx -n kube-system | grep -A 10 "Events:"
```

**常见原因:**
- 节点有 taint 但 Pod 没有 toleration
- 资源不足
- 网络未就绪

### 3. ImagePullBackOff

**症状:**
```
kubectl get pods
NAME       READY   STATUS              RESTARTS   AGE
my-pod     0/1     ImagePullBackOff    0          5m
```

**排查步骤:**

```bash
kubectl describe pod my-pod | grep -A 5 "Events:"
```

**解决方案:**

预拉取镜像:
```bash
# 在所有节点执行
docker pull registry.aliyuncs.com/google_containers/nginx:latest
```

或使用国内镜像源:
```yaml
image: registry.aliyuncs.com/google_containers/nginx:latest
```

### 4. CrashLoopBackOff

**症状:**
```
kubectl get pods
NAME       READY   STATUS              RESTARTS     AGE
my-pod     0/1     CrashLoopBackOff    5 (10s ago)  5m
```

**排查步骤:**

```bash
# 查看容器日志
kubectl logs my-pod
kubectl logs my-pod --previous  # 查看上一个容器的日志

# 查看 Pod 详情
kubectl describe pod my-pod
```

**常见原因:**
- 应用启动失败
- 配置错误
- 依赖服务未就绪

### 5. Flannel 启动失败

**症状:**
```
kubectl get pods -n kube-system | grep flannel
kube-flannel-ds-xxxxx   0/1     CrashLoopBackOff   5 (10s ago)   10m
```

**排查步骤:**

```bash
# 查看 Flannel 日志
kubectl logs kube-flannel-ds-xxxxx -n kube-system
```

**常见错误:**

1. **找不到网络接口**
```
Could not find valid interface matching eth0: error looking up interface eth0
```

**解决方案:**
```bash
# 检测正确的接口名
ip route | grep default | awk '{print $5}'

# 更新 Flannel 配置，使用正确的接口名
# 将 --iface=eth0 改为 --iface=ens192（或其他检测到的接口）
```

2. **CNI 插件未初始化**
```
NetworkPluginNotReady message:Network plugin returns error: cni plugin not initialized
```

**解决方案:**
```bash
# 手动创建 CNI 配置文件（见问题 1）
```

## 网络接口检测

不同发行版的网络接口名可能不同:

```bash
# 方法 1: 查看默认路由接口
ip route | grep default | awk '{print $5}'

# 方法 2: 查看所有接口
ip addr show

# 方法 3: 查看有 IP 的接口
ip addr | grep "inet " | grep -v "127.0.0.1"
```

常见接口名:
- CentOS/RHEL: ens192, ens33, eth0
- Ubuntu: ens33, enp0s3, eth0
- 虚拟机：ens33, eth0

## 镜像源

### 国内可用镜像源

| 镜像 | 华为云 | 阿里云 |
|------|--------|--------|
| flannel | `swr.cn-north-4.myhuaweicloud.com/ddn-k8s/quay.io/coreos/flannel:v0.15.1` | ❌ |
| pause | `registry.aliyuncs.com/google_containers/pause:3.9` | ✅ |
| coredns | `registry.aliyuncs.com/google_containers/coredns:v1.10.1` | ✅ |
| kube-proxy | `registry.aliyuncs.com/google_containers/kube-proxy:v1.28.0` | ✅ |

### 镜像拉取失败

如果镜像拉取失败，尝试:

1. 更换镜像源
2. 检查网络连接
3. 配置 Docker 镜像加速器

```bash
# 配置阿里云镜像加速器
cat > /etc/docker/daemon.json << 'EOF'
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}
EOF

systemctl daemon-reload
systemctl restart docker
```

## 日志收集

### 收集所有诊断信息

```bash
#!/bin/bash
# save-this.sh

echo "=== 节点信息 ==="
kubectl get nodes -o wide

echo "=== 系统 Pod ==="
kubectl get pods -n kube-system -o wide

echo "=== 节点详情 ==="
for node in $(kubectl get nodes -o name); do
    echo "--- $node ---"
    kubectl describe $node
done

echo "=== Pod 详情 ==="
for pod in $(kubectl get pods -n kube-system -o name); do
    echo "--- $pod ---"
    kubectl describe $pod -n kube-system
done

echo "=== Kubelet 日志 (最近 50 行) ==="
journalctl -u kubelet -n 50 --no-pager
```

## 快速修复命令

```bash
# 重启 K3s
systemctl restart k3s  # Master
systemctl restart k3s-agent  # Worker

# 重启 kubelet
systemctl restart kubelet

# 删除 Pod 强制重建
kubectl delete pod <pod-name> -n kube-system

# 清理所有 NotReady Pod
kubectl delete pods --all -n kube-system --field-selector spec.nodeName=<node-name>

# 重新部署 Flannel
kubectl delete ds kube-flannel-ds -n kube-system
kubectl apply -f flannel-config.yml
```

## 联系支持

如果以上方法都无法解决问题，请提供:

1. `kubectl get nodes -o wide` 输出
2. `kubectl get pods -n kube-system -o wide` 输出
3. 问题 Pod 的 `kubectl describe` 输出
4. `journalctl -u kubelet -n 100` 输出
