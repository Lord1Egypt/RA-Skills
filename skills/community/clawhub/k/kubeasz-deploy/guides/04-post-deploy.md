# 部署后验证与使用指南

本指南帮助你验证 Kubernetes 集群部署成功，学习基础操作，并配置常用附加组件。

---

## 一、集群健康检查

### 1.1 节点状态检查

**检查节点状态**：

```bash
# 查看所有节点状态
kubectl get nodes

# 查看详细信息
kubectl get nodes -o wide

# 查看特定节点详情
kubectl describe node <node-name>
```

**期望结果**：

```
NAME        STATUS   ROLES           AGE   VERSION   INTERNAL-IP    OS-IMAGE
master-01   Ready    control-plane   10m   v1.28.2   192.168.1.1    Ubuntu 22.04
master-02   Ready    control-plane   10m   v1.28.2   192.168.1.2    Ubuntu 22.04
worker-01   Ready    <none>          9m    v1.28.2   192.168.1.4    Ubuntu 22.04
```

**成功指标**：
- STATUS 为 `Ready`
- ROLES 正确标识节点角色（control-plane、<none>）
- VERSION 显示正确的 Kubernetes 版本

---

### 1.2 组件状态检查

**检查控制平面组件**：

```bash
# 查看组件健康状态
kubectl get cs

# 或使用完整命令
kubectl get componentstatuses
```

**期望结果**：

```
NAME                 STATUS    MESSAGE                         ERROR
controller-manager   Healthy   ok                              
scheduler            Healthy   ok                              
etcd-0               Healthy   {"health":"true","reason":""}  
etcd-1               Healthy   {"health":"true","reason":""}  
etcd-2               Healthy   {"health":"true","reason":""}  
```

**成功指标**：
- scheduler、controller-manager 状态为 `Healthy`
- 所有 etcd 成员状态为 `Healthy`

---

### 1.3 系统 Pod 检查

**检查系统命名空间 Pod**：

```bash
# 查看所有系统 Pod
kubectl get pods -n kube-system

# 查看详细信息
kubectl get pods -n kube-system -o wide
```

**期望结果**：

```
NAMESPACE     NAME                                       READY   STATUS    AGE
kube-system   calico-kube-controllers-xxx                1/1     Running   8m
kube-system   calico-node-xxx                            1/1     Running   8m
kube-system   coredns-xxx                                1/1     Running   7m
kube-system   kube-apiserver-master-01                   1/1     Running   9m
kube-system   kube-controller-manager-master-01         1/1     Running   9m
kube-system   kube-proxy-xxx                             1/1     Running   8m
kube-system   kube-scheduler-master-01                   1/1     Running   9m
kube-system   metrics-server-xxx                        1/1     Running   7m
```

**成功指标**：
- 所有 Pod 状态为 `Running`
- READY 列显示 `1/1` 或 `n/n`
- 无 `ImagePullBackOff`、`CrashLoopBackOff` 等错误状态

---

### 1.4 网络插件检查

**检查 Calico 网络（如使用 Calico）**：

```bash
# 查看 Calico Pod
kubectl get pods -n kube-system -l k8s-app=calico-node

# 查看 Calico 网络状态
kubectl exec -n kube-system calico-node-xxx -- calicoctl node status

# 查看 Calico IP池
kubectl exec -n kube-system calico-node-xxx -- calicoctl get ipPool -o yaml
```

**检查 Flannel 网络（如使用 Flannel）**：

```bash
# 查看 Flannel Pod
kubectl get pods -n kube-system -l app=flannel

# 查看网络配置
kubectl logs -n kube-system kube-flannel-xxx
```

**成功指标**：
- 网络插件 Pod 状态为 `Running`
- 网络配置正确（Pod CIDR、IP池）
- 节点间网络互通

---

### 1.5 etcd 集群健康检查

**检查 etcd 集群**：

```bash
# 在任一 etcd 节点执行
export NODE_IPS="192.168.1.1 192.168.1.2 192.168.1.3"

for ip in ${NODE_IPS}; do
  etcdctl \
  --endpoints=https://${ip}:2379  \
  --cacert=/etc/kubernetes/ssl/ca.pem \
  --cert=/etc/kubernetes/ssl/etcd.pem \
  --key=/etc/kubernetes/ssl/etcd-key.pem \
  endpoint health; done

# 查看 etcd 集群成员
etcdctl \
  --endpoints=https://192.168.1.1:2379 \
  --cacert=/etc/kubernetes/ssl/ca.pem \
  --cert=/etc/kubernetes/ssl/etcd.pem \
  --key=/etc/kubernetes/ssl/etcd-key.pem \
  member list
```

**期望结果**：

```
https://192.168.1.1:2379 is healthy: successfully committed proposal: took = 2.210885ms
https://192.168.1.2:2379 is healthy: successfully committed proposal: took = 2.784043ms
https://192.168.1.3:2379 is healthy: successfully committed proposal: took = 3.275705ms
```

**成功指标**：
- 所有 etcd 节点返回 `healthy`
- etcd 集群成员数量正确
- 时间同步正常（偏差 < 50ms）

---

## 二、功能验证测试

### 2.1 Pod 网络测试

**创建测试 Pod**：

```bash
# 创建两个测试 Pod
kubectl run test-pod-1 --image=busybox --restart=Never -- sleep 3600
kubectl run test-pod-2 --image=busybox --restart=Never -- sleep 3600

# 等待 Pod 启动
kubectl wait --for=condition=Ready pod/test-pod-1 --timeout=60s
kubectl wait --for=condition=Ready pod/test-pod-2 --timeout=60s

# 查看 Pod IP
kubectl get pods -o wide
```

**测试 Pod 间网络互通**：

```bash
# 从 test-pod-1 ping test-pod-2
kubectl exec test-pod-1 -- ping -c 3 <test-pod-2-IP>

# 测试跨节点 Pod 网络（如果在不同节点）
kubectl exec test-pod-1 -- ping -c 3 <其他节点Pod-IP>
```

**期望结果**：
- Pod 间网络互通（ping 成功）
- 跨节点 Pod 网络互通

**清理测试资源**：

```bash
kubectl delete pod test-pod-1 test-pod-2
```

---

### 2.2 Service 测试

**创建测试 Service**：

```bash
# 创建 Deployment
kubectl create deployment nginx-test --image=nginx:alpine

# 等待 Deployment 就绪
kubectl wait --for=condition=available deployment/nginx-test --timeout=60s

# 创建 Service
kubectl expose deployment nginx-test --port=80 --target-port=80 --name=nginx-svc

# 查看 Service
kubectl get svc nginx-svc
kubectl get endpoints nginx-svc
```

**测试 Service 访问**：

```bash
# 获取 Service ClusterIP
kubectl get svc nginx-svc -o jsonpath='{.spec.clusterIP}'

# 从 Pod 测试 Service 访问
kubectl run test-svc --image=curlimages/curl --restart=Never -- curl -s http://<ClusterIP>/

# 或使用 DNS 名称
kubectl run test-svc-dns --image=curlimages/curl --restart=Never -- curl -s http://nginx-svc/
```

**期望结果**：
- Service 分配了 ClusterIP
- Service 有正确的 Endpoints（Pod IP）
- 从 Pod 可以访问 Service

**清理测试资源**：

```bash
kubectl delete deployment nginx-test
kubectl delete svc nginx-svc
kubectl delete pod test-svc test-svc-dns --ignore-not-found=true
```

---

### 2.3 DNS 解析测试

**测试集群内部 DNS**：

```bash
# 创建测试 Pod
kubectl run test-dns --image=busybox --restart=Never -- sleep 3600

# 测试 DNS 解析
kubectl exec test-dns -- nslookup kubernetes.default

# 测试 Service DNS 解析
kubectl exec test-dns -- nslookup kube-dns.kube-system

# 测试外部域名解析
kubectl exec test-dns -- nslookup www.baidu.com
```

**期望结果**：

```
Server:    10.68.0.2
Address 1: 10.68.0.2 kube-dns.kube-system.svc.cluster.local

Name:      kubernetes.default
Address 1: 10.68.0.1 kubernetes.default.svc.cluster.local
```

**成功指标**：
- 集群内部域名解析正常（kubernetes.default）
- Service DNS 解析正常（kube-dns.kube-system）
- 外部域名解析正常（测试外网访问）

**清理测试资源**：

```bash
kubectl delete pod test-dns
```

---

### 2.4 存储测试（可选）

**测试 PVC 创建**：

```bash
# 创建测试 PVC
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
EOF

# 查看 PVC 状态
kubectl get pvc test-pvc
```

**期望结果**：
- PVC 状态为 `Bound`（如果有默认 StorageClass）
- 或 PVC 状态为 `Pending`（需手动创建 PV）

**清理测试资源**：

```bash
kubectl delete pvc test-pvc
```

---

### 2.5 应用部署测试

**完整应用部署测试**：

```bash
# 创建 Deployment
kubectl create deployment demo-app --image=nginx:alpine --replicas=3

# 扩容 Deployment
kubectl scale deployment demo-app --replicas=5

# 创建 Service
kubectl expose deployment demo-app --port=80 --target-port=80 --type=NodePort --name=demo-svc

# 查看状态
kubectl get deployment demo-app
kubectl get pods -l app=demo-app
kubectl get svc demo-svc
```

**测试 NodePort 访问**：

```bash
# 获取 NodePort
kubectl get svc demo-svc -o jsonpath='{.spec.ports[0].nodePort}'

# 在节点上测试访问
curl http://<Node-IP>:<NodePort>/
```

**成功指标**：
- Deployment 所有副本就绪
- Service Endpoints 包含所有 Pod IP
- NodePort 可以访问应用

**清理测试资源**：

```bash
kubectl delete deployment demo-app
kubectl delete svc demo-svc
```

---

## 三、常见验证失败排查

### 3.1 节点 NotReady

**现象**：

```bash
kubectl get nodes
NAME        STATUS       ROLES           AGE   VERSION
master-01   NotReady     control-plane   10m   v1.28.2
```

**排查步骤**：

```bash
# 查看节点详情
kubectl describe node master-01

# 查看 kubelet 日志
journalctl -u kubelet -n 50 --no-pager

# 查看容器运行时状态
systemctl status containerd
# 或
systemctl status docker

# 查看网络插件 Pod
kubectl get pods -n kube-system -l k8s-app=calico-node
```

**常见原因与解决**：

| 原因 | 解决方案 |
|:-----|:---------|
| 网络插件未启动 | 检查 CNI Pod 状态，重新部署网络插件 |
| 容器运行时异常 | 重启 containerd/docker 服务 |
| kubelet 服务异常 | 重启 kubelet，检查配置 |
| 证书错误 | 检查 kubelet 证书，重新生成 |
| 节点资源不足 | 释放资源或扩容节点 |

---

### 3.2 Pod 启动失败

**现象 1：镜像拉取失败**

```bash
kubectl get pods
NAME        READY   STATUS             AGE
demo-app-0  0/1     ImagePullBackOff   5m
```

**排查步骤**：

```bash
# 查看 Pod 详情
kubectl describe pod demo-app-0

# 查看镜像拉取错误
kubectl describe pod demo-app-0 | grep -A 10 "Events"

# 检查镜像是否存在
docker images | grep <image-name>
# 或
crictl images | grep <image-name>
```

**解决方案**：
- 参考 [03-production-deploy.md](03-production-deploy.md) "镜像拉取解决方案"
- 使用离线安装：`./ezdown -D`
- 手动拉取镜像并重命名

---

**现象 2：Pod 一直 Pending**

```bash
kubectl get pods
NAME        READY   STATUS    AGE
demo-app-0  0/1     Pending   5m
```

**排查步骤**：

```bash
# 查看 Pod 详情
kubectl describe pod demo-app-0

# 查看事件
kubectl get events --sort-by='.lastTimestamp'

# 检查节点资源
kubectl describe nodes | grep -A 5 "Allocated resources"

# 检查节点污点
kubectl describe nodes | grep Taints
```

**常见原因与解决**：

| 原因 | 解决方案 |
|:-----|:---------|
| 资源不足（CPU/内存） | 扩容节点或减少 Pod 资源请求 |
| 节点污点（Taint） | 添加 Toleration 或移除污点 |
| PVC 未绑定 | 创建 PV 或 StorageClass |
| 节点选择器不匹配 | 修改 Pod nodeSelector |

---

### 3.3 DNS 解析失败

**现象**：

```bash
kubectl exec test-dns -- nslookup kubernetes
Server:    10.68.0.2
Address 1: 10.68.0.2
nslookup: can't resolve 'kubernetes'
```

**排查步骤**：

```bash
# 查看 CoreDNS Pod
kubectl get pods -n kube-system -l k8s-app=kube-dns

# 查看 CoreDNS 日志
kubectl logs -n kube-system <coredns-pod>

# 查看 CoreDNS 配置
kubectl get configmap coredns -n kube-system -o yaml

# 测试 Pod 网络（DNS 需要网络正常）
kubectl exec test-dns -- ping -c 3 10.68.0.2
```

**常见原因与解决**：

| 原因 | 解决方案 |
|:-----|:---------|
| CoreDNS Pod 异常 | 重启 CoreDNS Pod，检查日志 |
| Pod 网络不通 | 检查网络插件，确保 Pod 网络互通 |
| DNS ConfigMap 错误 | 检查 CoreDNS 配置，重新部署 |
| Service 网段配置错误 | 检查 SERVICE_CIDR 配置 |

---

### 3.4 网络不通

**现象**：

```bash
kubectl exec test-pod-1 -- ping <test-pod-2-IP>
PING <IP>: 56 data bytes
--- <IP> ping statistics ---
3 packets transmitted, 0 packets received, 100% packet loss
```

**排查步骤**：

```bash
# 查看网络插件 Pod
kubectl get pods -n kube-system -l k8s-app=calico-node

# 查看网络插件日志
kubectl logs -n kube-system <calico-node-pod>

# 查看 Pod 网络配置
kubectl exec test-pod-1 -- ip addr

# 检查 iptables/ipvs 规则
iptables -t nat -L -n -v
# 或
ipvsadm -Ln
```

**常见原因与解决**：

| 原因 | 解决方案 |
|:-----|:---------|
| 网络插件未启动 | 检查 CNI Pod 状态，重启网络插件 |
| Pod CIDR 配置错误 | 检查 CLUSTER_CIDR 配置 |
| 节点防火墙阻止 | 开放必要端口或禁用防火墙 |
| iptables/ipvs 配置错误 | 检查 kube-proxy 配置 |

---

## 四、基础使用指南

### 4.1 kubectl 常用操作

**查看资源**：

```bash
# 查看所有资源
kubectl get all

# 查看特定类型资源
kubectl get nodes
kubectl get pods -n <namespace>
kubectl get services
kubectl get deployments
kubectl get configmaps
kubectl get secrets

# 查看详细信息
kubectl describe <resource-type> <resource-name>

# 查看资源定义
kubectl get <resource-type> <resource-name> -o yaml
```

**创建资源**：

```bash
# 从文件创建
kubectl apply -f <file.yaml>

# 从命令行创建
kubectl create deployment <name> --image=<image>
kubectl expose deployment <name> --port=<port>
kubectl run <pod-name> --image=<image>

# 创建命名空间
kubectl create namespace <namespace>
```

**更新资源**：

```bash
# 修改资源定义
kubectl edit <resource-type> <resource-name>

# 更新 Deployment
kubectl set image deployment/<name> <container>=<new-image>
kubectl scale deployment/<name> --replicas=<number>

# 更新配置
kubectl apply -f <file.yaml>
```

**删除资源**：

```bash
# 删除单个资源
kubectl delete <resource-type> <resource-name>

# 从文件删除
kubectl delete -f <file.yaml>

# 删除所有资源（谨慎使用）
kubectl delete all --all -n <namespace>
```

**查看日志和调试**：

```bash
# 查看 Pod 日志
kubectl logs <pod-name>
kubectl logs -f <pod-name>  # 实时日志
kubectl logs <pod-name> -c <container-name>  # 多容器 Pod

# 进入 Pod
kubectl exec -it <pod-name> -- /bin/sh
kubectl exec -it <pod-name> -- /bin/bash

# 端口转发
kubectl port-forward <pod-name> <local-port>:<pod-port>
kubectl port-forward svc/<service-name> <local-port>:<service-port>
```

---

### 4.2 配置管理

**ConfigMap 管理**：

```bash
# 从文件创建 ConfigMap
kubectl create configmap <name> --from-file=<file>

# 从字面值创建
kubectl create configmap <name> --from-literal=<key>=<value>

# 查看 ConfigMap
kubectl get configmap <name> -o yaml

# 更新 ConfigMap
kubectl edit configmap <name>
```

**Secret 管理**：

```bash
# 创建 Secret（通用）
kubectl create secret generic <name> --from-literal=<key>=<value>

# 创建 Secret（TLS）
kubectl create secret tls <name> --cert=<cert-file> --key=<key-file>

# 创建 Secret（docker-registry）
kubectl create secret docker-registry <name> \
  --docker-server=<server> \
  --docker-username=<user> \
  --docker-password=<password>

# 查看 Secret
kubectl get secret <name> -o yaml
```

---

### 4.3 集群管理

**节点管理**：

```bash
# 查看节点资源使用
kubectl top nodes

# 查看节点详情
kubectl describe node <node-name>

# 标记节点不可调度（维护）
kubectl cordon <node-name>

# 标记节点可调度
kubectl uncordon <node-name>

# 驱逐节点 Pod
kubectl drain <node-name> --delete-emptydir-data --ignore-daemonsets

# 删除节点
kubectl delete node <node-name>
```

**资源配额管理**：

```bash
# 查看资源使用
kubectl top pods -n <namespace>
kubectl top pods --all-namespaces

# 查看资源配额
kubectl get quota -n <namespace>

# 创建资源配额
kubectl apply -f - <<EOF
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: <namespace>
spec:
  hard:
    pods: "10"
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
EOF
```

**命名空间管理**：

```bash
# 创建命名空间
kubectl create namespace <namespace>

# 查看命名空间
kubectl get namespaces

# 切换默认命名空间
kubectl config set-context --current --namespace=<namespace>

# 删除命名空间（会删除其中所有资源）
kubectl delete namespace <namespace>
```

---

## 五、后续配置建议

### 5.1 Ingress 控制器

**推荐方案**：
- **Nginx Ingress**：最成熟、功能丰富
- **Traefik**：云原生、动态配置

**安装 Nginx Ingress**：

```bash
# 安装 Nginx Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml

# 验证安装
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx
```

**创建 Ingress 示例**：

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: demo-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: demo.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: demo-svc
            port:
              number: 80
```

---

### 5.2 监控系统

**推荐方案**：
- **Prometheus + Grafana**：开源监控标准方案
- **kube-prometheus-stack**：一站式监控栈

**安装 Prometheus（使用 kubeasz）**：

```bash
# 下载 Prometheus 镜像
./ezdown -X prometheus

# 安装 Prometheus（参考 kubeasz docs/guide/prometheus.md）
dk ezctl setup default extra-prometheus
```

**验证监控**：

```bash
# 查看 Prometheus Pod
kubectl get pods -n monitoring

# 查看 Grafana Service
kubectl get svc -n monitoring grafana

# 访问 Grafana（端口转发）
kubectl port-forward -n monitoring svc/grafana 3000:80
# 浏览器访问：http://localhost:3000
```

---

### 5.3 持久化存储

**推荐方案**：
- **Local PV**：单节点存储，适合开发测试
- **NFS Provisioner**：简单共享存储
- **Ceph RBD**：分布式存储，生产环境

**安装 NFS Provisioner**：

```bash
# 创建 NFS Provisioner（参考 kubeasz docs/setup/08-cluster-storage.md）
kubectl apply -f /etc/kubeasz/clusters/default/yml/storage/nfs-client/

# 创建 StorageClass
kubectl apply -f - <<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-client
provisioner: nfs-client
parameters:
  archiveOnDelete: "true"
EOF

# 设置默认 StorageClass
kubectl patch storageclass nfs-client -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```

**测试存储**：

```bash
# 创建 PVC
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-pvc
spec:
  storageClassName: nfs-client
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
EOF

# 查看 PVC（应为 Bound）
kubectl get pvc test-pvc
```

---

### 5.4 Dashboard

**安装 Kubernetes Dashboard**：

```bash
# 使用 kubeasz 安装（推荐）
./ezdown -X dashboard
dk ezctl setup default 07

# 或手动安装
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```

**创建访问用户**：

```bash
# 创建 ServiceAccount
kubectl create serviceaccount dashboard-admin -n kubernetes-dashboard

# 创建 ClusterRoleBinding
kubectl create clusterrolebinding dashboard-admin \
  --clusterrole=cluster-admin \
  --serviceaccount=kubernetes-dashboard:dashboard-admin

# 获取访问 Token
kubectl create token dashboard-admin -n kubernetes-dashboard
```

**访问 Dashboard**：

```bash
# 端口转发访问
kubectl port-forward -n kubernetes-dashboard svc/kubernetes-dashboard-kong-proxy 10443:443

# 浏览器访问（使用 Token 登录）
https://localhost:10443/
```

---

### 5.5 Harbor 私有仓库

**安装 Harbor（可选）**：

```bash
# 参考 kubeasz docs/guide/harbor.md
# Harbor 提供私有镜像仓库，适合生产环境
```

---

### 5.6 日志系统

**推荐方案**：
- **ELK Stack**：Elasticsearch + Logstash + Kibana
- **EFK Stack**：Elasticsearch + Fluentd + Kibana
- **Loki**：云原生日志系统，轻量级

**安装 EFK（参考 kubeasz docs）**：

```bash
# 安装 Elasticsearch + Fluentd + Kibana
# 参考 docs/deprecated/efk.md（注意：文档已归档）
```

---

## 六、成功标准总结

### 6.1 集群健康标准

**基础检查清单**：

- ✅ 所有节点状态为 `Ready`
- ✅ etcd 集群所有成员 `healthy`
- ✅ scheduler、controller-manager 状态 `Healthy`
- ✅ 系统所有 Pod 状态为 `Running`
- ✅ 网络插件 Pod 运行正常
- ✅ DNS Pod（CoreDNS）运行正常

### 6.2 功能验证标准

**网络功能**：

- ✅ Pod 间网络互通
- ✅ 跨节点 Pod 网络互通
- ✅ Service ClusterIP 可以访问
- ✅ Service DNS 解析正常

**存储功能**（可选）：

- ✅ PVC 可以正常绑定
- ✅ Pod 可以挂载 PVC
- ✅ 数据持久化正常

**应用部署**：

- ✅ Deployment 可以创建和扩容
- ✅ Service 可以正常访问
- ✅ NodePort 可以从外部访问

### 6.3 生产就绪标准

**附加检查**：

- ✅ 监控系统已部署（Prometheus）
- ✅ 日志系统已部署（可选）
- ✅ Ingress 控制器已部署
- ✅ 持久化存储已配置
- ✅ Dashboard 已安装（可选）
- ✅ 资源配额已配置
- ✅ 网络策略已配置（可选）

---

## 七、快速诊断脚本

### 7.1 集群健康检查脚本

创建快速诊断脚本：

```bash
#!/bin/bash
# cluster-health-check.sh

echo "=== 集群健康检查 ==="
echo

echo "1. 节点状态"
kubectl get nodes
echo

echo "2. 组件状态"
kubectl get cs
echo

echo "3. 系统 Pod"
kubectl get pods -n kube-system
echo

echo "4. 网络 Pod"
kubectl get pods -n kube-system -l k8s-app=calico-node
echo

echo "5. DNS Pod"
kubectl get pods -n kube-system -l k8s-app=kube-dns
echo

echo "6. 集群信息"
kubectl cluster-info
echo

echo "=== 检查完成 ==="
```

**执行检查**：

```bash
chmod +x cluster-health-check.sh
./cluster-health-check.sh
```

---

### 7.2 功能测试脚本

```bash
#!/bin/bash
# function-test.sh

echo "=== 功能测试 ==="
echo

echo "1. 创建测试 Pod"
kubectl run test-pod --image=busybox --restart=Never -- sleep 60
kubectl wait --for=condition=Ready pod/test-pod --timeout=30s
echo

echo "2. 测试 DNS"
kubectl exec test-pod -- nslookup kubernetes.default
echo

echo "3. 测试网络"
kubectl exec test-pod -- ping -c 2 kubernetes.default
echo

echo "4. 清理测试 Pod"
kubectl delete pod test-pod --ignore-not-found=true
echo

echo "=== 测试完成 ==="
```

---

## 八、常用命令速查

### 8.1 查看命令

| 命令 | 说明 |
|:-----|:-----|
| `kubectl get nodes` | 查看节点状态 |
| `kubectl get pods -A` | 查看所有 Pod |
| `kubectl get cs` | 查看组件状态 |
| `kubectl cluster-info` | 查看集群信息 |
| `kubectl top nodes` | 查看节点资源使用 |
| `kubectl top pods -A` | 查看所有 Pod 资源使用 |
| `kubectl get events` | 查看集群事件 |
| `kubectl describe <resource>` | 查看资源详情 |

### 8.2 操作命令

| 命令 | 说明 |
|:-----|:-----|
| `kubectl apply -f <file>` | 创建/更新资源 |
| `kubectl delete -f <file>` | 删除资源 |
| `kubectl logs <pod>` | 查看 Pod 日志 |
| `kubectl exec -it <pod> -- sh` | 进入 Pod |
| `kubectl port-forward <pod> <port>` | 端口转发 |
| `kubectl cordon <node>` | 标记节点不可调度 |
| `kubectl drain <node>` | 驱逐节点 Pod |

### 8.3 故障排查命令

| 命令 | 说明 |
|:-----|:-----|
| `kubectl describe pod <pod>` | 查看 Pod 详情和事件 |
| `kubectl logs <pod> --previous` | 查看上一个容器日志 |
| `kubectl get events --sort-by='.lastTimestamp'` | 查看最近事件 |
| `journalctl -u kubelet` | 查看 kubelet 日志 |
| `journalctl -u containerd` | 查看容器运行时日志 |

---

## 九、参考信息

### 9.1 相关文档

- [前置条件检查](01-prerequisites.md)
- [AllinOne 快速部署](02-allinone-quickstart.md)
- [生产环境部署](03-production-deploy.md)
- [故障排查指南](../troubleshooting.md)
- [kubeasz 官方文档](https://github.com/easzlab/kubeasz)
- [Kubernetes 官方文档](https://kubernetes.io/docs/)

### 9.2 kubeasz 运维文档

- [节点管理](https://github.com/easzlab/kubeasz/blob/master/docs/op/op-node.md)
- [Master 管理](https://github.com/easzlab/kubeasz/blob/master/docs/op/op-master.md)
- [etcd 管理](https://github.com/easzlab/kubeasz/blob/master/docs/op/op-etcd.md)
- [集群升级](https://github.com/easzlab/kubeasz/blob/master/docs/op/upgrade.md)
- [集群备份恢复](https://github.com/easzlab/kubeasz/blob/master/docs/op/cluster_restore.md)

---

**部署成功标志**：
- ✅ 集群健康检查全部通过
- ✅ 功能验证测试成功
- ✅ 应用可以正常部署和访问

**下一步**：
- 配置监控、日志、存储、Ingress 等附加组件
- 学习 Kubernetes 应用部署最佳实践
- 参考 [troubleshooting.md](../troubleshooting.md) 解决常见问题

---

**文档版本**：v1.0.0  
**更新日期**：2026-04-08  
**参考文档**：kubeasz docs/guide/, docs/op/