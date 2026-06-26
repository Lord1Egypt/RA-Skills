# kubeasz 部署故障排查指南

本文档涵盖 kubeasz 部署和运维过程中最常见的 18 类问题及其解决方案。

---

## 一、部署阶段常见问题 (6类)

### 问题1: 镜像拉取失败

**问题描述**  
部署时提示镜像拉取超时或失败，如 `ImagePullBackOff`, `ErrImagePull`。

**诊断步骤**
```bash
# 检查镜像拉取状态
kubectl describe pod <pod-name> -n kube-system

# 查看具体错误
kubectl logs <pod-name> -n kube-system

# 检查本地镜像
docker images | grep <image-name>
crictl images | grep <image-name>
```

**常见原因**
1. 网络不通导致无法访问镜像仓库
2. 镜像仓库限速或不可用
3. 镜像不存在或tag错误
4. 认证信息不正确

**解决方案**

**方案A: 离线安装(推荐)**

在可访问外网的机器上提前下载：
```bash
# 下载默认镜像
./ezdown -D

# 下载额外镜像
./ezdown -X calico
./ezdown -X flannel
./ezdown -X prometheus

# 打包传输到离线环境
cd /etc/kubeasz
tar -czf kubeasz-images.tar.gz down/
scp kubeasz-images.tar.gz <离线环境节点>:/etc/kubeasz/
```

**方案B: 使用镜像加速**

配置 Docker 镜像加速器：
```bash
# 编辑 /etc/docker/daemon.json
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://hub1.nat.tf",
    "https://docker.1panel.live"
  ]
}

# 重启 Docker
systemctl restart docker
```

配置 containerd 镜像加速：
```bash
# 编辑 /etc/containerd/config.toml
[plugins."io.containerd.grpc.v1.cri".registry.mirrors]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
    endpoint = ["https://docker.1ms.run"]

# 重启 containerd
systemctl restart containerd
```

**方案C: 手动拉取并重命名**
```bash
# 使用加速地址拉取
docker pull docker.1ms.run/library/nginx:alpine

# 重新标记
docker tag docker.1ms.run/library/nginx:alpine nginx:alpine
```

---

### 问题2: Ansible 连接失败

**问题描述**  
执行 `ansible-playbook` 时提示节点连接失败。

**诊断步骤**
```bash
# 测试SSH连接
ssh <node-ip>

# 测试ansible连接
ansible -i clusters/<cluster>/hosts all -m ping

# 查看详细错误
ansible-playbook -i clusters/<cluster>/hosts playbooks/01.prepare.yml -vvv
```

**常见原因**
1. SSH免密未配置
2. hosts文件配置错误
3. 防火墙阻挡SSH端口
4. 节点间网络不通

**解决方案**

配置SSH免密登录：
```bash
# 生成密钥对
ssh-keygen -t rsa -b 2048 -N '' -f ~/.ssh/id_rsa

# 批量分发公钥
for ip in <所有节点IP>; do
  ssh-copy-id -i ~/.ssh/id_rsa.pub $ip
done

# 验证
for ip in <所有节点IP>; do
  ssh $ip "hostname"
done
```

---

### 问题3: 证书相关错误

**问题描述**  
部署时提示证书过期或无效。

**诊断步骤**
```bash
# 查看证书有效期
openssl x509 -in /etc/kubernetes/pki/ca.crt -text -noout | grep Not

# 检查证书链
openssl verify -CAfile /etc/kubernetes/pki/ca.crt /etc/kubernetes/pki/apiserver.crt

# 查看kubeadm配置
kubeadm config view
```

**常见原因**
1. 系统时间不正确
2. 证书生成时时间设置错误
3. CA证书不匹配

**解决方案**

重新生成证书：
```bash
# 使用ezctl重新生成
./ezctl kca-renew <cluster-name>

# 或手动更新
kubeadm certs renew all
```

---

### 问题4: 端口冲突

**问题描述**  
部署时提示端口已被占用。

**诊断步骤**
```bash
# 查看端口占用
netstat -tlnp | grep -E "6443|2379|2380|10250"
ss -tlnp | grep -E "6443|2379|2380|10250"

# 查看进程
lsof -i:6443
```

**常见冲突端口**
- 6443: kube-apiserver
- 2379, 2380: etcd
- 10250: kubelet
- 10251: kube-scheduler
- 10252: kube-controller-manager

**解决方案**
```bash
# 停止冲突服务
systemctl stop <conflicting-service>

# 修改kubeasz配置使用其他端口
# 编辑 clusters/<cluster>/hosts
SECURE_PORT="16443"  # 改用非标准端口
```

---

### 问题5: etcd 集群启动失败

**问题描述**  
etcd节点无法正常启动或加入集群。

**诊断步骤**
```bash
# 查看etcd日志
journalctl -u etcd -f

# 检查etcd服务状态
systemctl status etcd

# 查看etcd配置
cat /etc/systemd/system/etcd.service

# 检查etcd数据目录
ls -la /var/lib/etcd/
```

**常见原因**
1. 节点时间不同步
2. etcd数据目录权限问题
3. 节点间网络不通
4. etcd成员配置错误

**解决方案**

时间同步：
```bash
# 安装chrony
yum install -y chrony  # CentOS/RHEL
apt install -y chrony  # Ubuntu/Debian

# 配置时间服务器
cat >> /etc/chrony.conf <<EOF
server ntp.aliyun.com iburst
server time1.cloud.tencent.com iburst
EOF

# 启动服务
systemctl start chronyd
systemctl enable chronyd

# 验证
chronyc sources
timedatectl
```

修复权限：
```bash
chown -R etcd:etcd /var/lib/etcd
chmod 755 /var/lib/etcd
```

---

### 问题6: 网络插件安装失败

**问题描述**  
Calico/Flannel/Cilium等CNI插件Pod无法启动。

**诊断步骤**
```bash
# 查看网络插件Pod状态
kubectl get pods -n kube-system | grep -E "calico|flannel|cilium"

# 查看Pod详情
kubectl describe pod <cni-pod-name> -n kube-system

# 查看日志
kubectl logs <cni-pod-name> -n kube-system

# 检查kubelet日志
journalctl -u kubelet | grep -i cni
```

**常见原因**
1. 镜像拉取失败
2. Pod CIDR配置冲突
3. kubelet配置问题
4. 内核模块未加载

**解决方案**

检查CIDR配置：
```bash
# 确保不与物理网络冲突
# 编辑 clusters/<cluster>/hosts
kube_pods_subnet="10.244.0.0/16"
kube_service_subnet="10.96.0.0/12"

# 重新部署网络插件
./ezctl setup <cluster> 06
```

加载内核模块：
```bash
# 加载必要的内核模块
modprobe br_netfilter
modprobe overlay

# 设置sysctl参数
cat > /etc/sysctl.d/99-kubernetes.conf <<EOF
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward = 1
EOF

sysctl --system
```

---

## 二、运维阶段常见问题 (6类)

### 问题7: 节点NotReady

**问题描述**  
kubectl get nodes显示节点状态为NotReady。

**诊断步骤**
```bash
# 查看节点详情
kubectl describe node <node-name>

# 查看kubelet日志
journalctl -u kubelet -f

# 检查容器运行时
systemctl status containerd
crictl ps

# 检查网络插件
kubectl get pods -n kube-system -o wide | grep <node-name>
```

**常见原因**
1. 网络插件异常
2. kubelet服务异常
3. 容器运行时异常
4. 磁盘空间不足

**解决方案**

重启kubelet：
```bash
systemctl restart kubelet
systemctl status kubelet
```

重启容器运行时：
```bash
systemctl restart containerd
systemctl status containerd
```

检查磁盘空间：
```bash
df -h
# 清理无用镜像和容器
docker system prune -af  # Docker
crictl rmi --prune      # containerd
```

---

### 问题8: Pod镜像拉取超时

**问题描述**  
Pod状态为ImagePullBackOff或ErrImagePull。

**诊断步骤**
```bash
# 查看Pod详情
kubectl describe pod <pod-name>

# 查看事件
kubectl get events --field-selector involvedObject.name=<pod-name>

# 检查镜像是否存在
docker pull <image-name>
crictl pull <image-name>
```

**解决方案**  
参考问题1的镜像拉取解决方案。

---

### 问题9: Pod无法调度

**问题描述**  
Pod状态为Pending，无法分配到节点。

**诊断步骤**
```bash
# 查看Pod详情
kubectl describe pod <pod-name>

# 查看节点资源
kubectl describe nodes
kubectl top nodes

# 查看资源请求
kubectl get pod <pod-name> -o yaml | grep -A 5 requests
```

**常见原因**
1. 资源不足(CPU/Memory)
2. 节点选择器不匹配
3. taints/tolerations不匹配
4. 持久卷未绑定

**解决方案**

增加节点或调整资源请求：
```yaml
# 调整Pod资源请求
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "200m"
    memory: "256Mi"
```

处理taints：
```bash
# 查看节点taints
kubectl describe node <node-name> | grep Taints

# 添加toleration到Pod
tolerations:
- key: "key"
  operator: "Equal"
  value: "value"
  effect: "NoSchedule"

# 或删除节点taint
kubectl taint nodes <node-name> key:NoSchedule-
```

---

### 问题10: Service无法访问

**问题描述**  
Service创建成功但无法访问。

**诊断步骤**
```bash
# 查看Service
kubectl get svc <service-name>
kubectl describe svc <service-name>

# 查看Endpoints
kubectl get endpoints <service-name>

# 检查Pod label
kubectl get pods --show-labels

# 测试ClusterIP
kubectl run test --image=busybox --rm -it -- wget -qO- <cluster-ip>:<port>
```

**常见原因**
1. Pod未就绪
2. selector配置错误
3. 端口配置错误
4. 网络策略阻挡

**解决方案**

检查Pod状态：
```bash
# 确保Pod正常运行
kubectl get pods -l <label-key>=<label-value>

# 检查Pod是否ready
kubectl get pods -o wide

# 查看Pod labels
kubectl get pods --show-labels
```

验证selector：
```yaml
# Service selector必须与Pod labels匹配
spec:
  selector:
    app: nginx  # 必须与Pod labels中的app匹配
  ports:
  - port: 80
    targetPort: 80  # 必须与容器端口匹配
```

---

### 问题11: DNS解析失败

**问题描述**  
Pod内无法解析Service域名。

**诊断步骤**
```bash
# 检查CoreDNS Pod
kubectl get pods -n kube-system -l k8s-app=kube-dns

# 查看CoreDNS日志
kubectl logs -n kube-system <coredns-pod-name>

# 测试DNS解析
kubectl exec <pod-name> -- nslookup kubernetes.default
kubectl exec <pod-name> -- nslookup <service-name>.<namespace>.svc.cluster.local

# 查看Pod DNS配置
kubectl exec <pod-name> -- cat /etc/resolv.conf
```

**常见原因**
1. CoreDNS Pod异常
2. kubelet DNS配置错误
3. Pod dnsPolicy配置问题
4. 网络策略阻挡DNS请求

**解决方案**

重启CoreDNS：
```bash
kubectl rollout restart deployment coredns -n kube-system
```

检查kubelet配置：
```bash
# 确保kubelet配置了正确的DNS
ps aux | grep kubelet | grep cluster-dns

# 检查配置
cat /var/lib/kubelet/config.yaml | grep -A 5 clusterDNS
```

---

### 问题12: PV/PVC无法绑定

**问题描述**  
PVC状态为Pending，无法找到匹配的PV。

**诊断步骤**
```bash
# 查看PVC状态
kubectl get pvc
kubectl describe pvc <pvc-name>

# 查看PV状态
kubectl get pv

# 检查StorageClass
kubectl get storageclass
kubectl describe storageclass <sc-name>
```

**常见原因**
1. 无可用PV
2. StorageClass配置错误
3. accessModes不匹配
4. 存储大小不匹配

**解决方案**

创建匹配的PV：
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-example
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: standard
  hostPath:
    path: /mnt/data
```

配置动态存储：
```bash
# 安装local-path-provisioner
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.24/deploy/local-path-storage.yaml

# 或使用kubeasz安装
./ezdown -X local-path-provisioner
./ezctl setup <cluster> 07
```

---

## 三、集群运维问题 (3类)

### 问题13: 集群升级失败

**问题描述**  
执行./ezctl upgrade后集群异常。

**诊断步骤**
```bash
# 查看节点状态
kubectl get nodes

# 查看Pod状态
kubectl get pods -A

# 查看kubelet日志
journalctl -u kubelet -f

# 检查组件版本
kubectl version
```

**解决方案**

备份恢复：
```bash
# 恢复到升级前的备份
./ezctl restore <cluster-name>
```

重新部署：
```bash
# 完全清理重新部署
./ezctl destroy <cluster-name>
./ezctl setup <cluster-name> all
```

---

### 问题14: 集群备份恢复失败

**问题描述**  
执行./ezctl restore后数据丢失或服务异常。

**诊断步骤**
```bash
# 查看etcd状态
ETCDCTL_API=3 etcdctl member list
ETCDCTL_API=3 etcdctl endpoint status

# 检查备份文件
ls -lh /etc/kubeasz/clusters/<cluster>/backup/
```

**注意事项**
1. 确保备份文件完整
2. restore前先停止集群
3. 恢复后需重启所有组件

**解决方案**

正确恢复流程：
```bash
# 1. 停止集群
./ezctl stop <cluster-name>

# 2. 执行恢复
./ezctl restore <cluster-name>

# 3. 启动集群
./ezctl start <cluster-name>

# 4. 验证集群状态
kubectl get nodes
kubectl get pods -A
```

---

### 问题15: 添加节点失败

**问题描述**  
执行add-node/add-master后节点无法加入集群。

**诊断步骤**
```bash
# 查看节点日志
journalctl -u kubelet -f

# 检查证书
openssl x509 -in /etc/kubernetes/pki/ca.crt -text -noout

# 检查网络连通性
ping <master-ip>
telnet <master-ip> 6443
```

**常见原因**
1. 证书不匹配
2. 网络不通
3. token过期

**解决方案**

检查证书和token：
```bash
# 确保使用正确的CA证书
# kubeasz会自动处理，检查配置即可

# 检查bootstrap token
kubeadm token list

# 创建新token
kubeadm token create --print-join-command
```

---

## 四、系统层面问题 (3类)

### 问题16: 系统资源不足

**问题描述**  
集群运行缓慢或服务频繁重启。

**诊断步骤**
```bash
# 查看系统资源
free -h
df -h
top

# 查看容器资源使用
kubectl top nodes
kubectl top pods -A

# 查看系统负载
uptime
```

**解决方案**

清理资源：
```bash
# 清理无用镜像
docker system prune -af

# 清理无用Pod
kubectl delete pods --field-selector status.phase=Failed -A

# 清理日志
journalctl --vacuum-time=7d
```

增加资源限制：
```yaml
# 为Pod设置资源限制
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

---

### 问题17: 时间不同步

**问题描述**  
证书验证失败或etcd异常。

**诊断步骤**
```bash
# 查看时间
date
timedatectl status

# 查看时间差
for node in <所有节点>; do
  ssh $node date
done
```

**解决方案**

配置时间同步：
```bash
# 安装chrony
yum install -y chrony  # CentOS/RHEL
apt install -y chrony  # Ubuntu/Debian

# 配置时间服务器
cat >> /etc/chrony.conf <<EOF
server ntp.aliyun.com iburst
server time1.cloud.tencent.com iburst
server ntp.tencent.com iburst
EOF

# 启动服务
systemctl start chronyd
systemctl enable chronyd

# 验证
chronyc sources
chronyc tracking
```

---

### 问题18: 防火墙阻挡通信

**问题描述**  
节点间无法通信或服务无法访问。

**诊断步骤**
```bash
# 查看防火墙状态
firewall-cmd --state
iptables -L -n

# 测试端口连通性
telnet <node-ip> 6443
nc -zv <node-ip> 2379
```

**解决方案**

开放必要端口：
```bash
# K8s Master节点
firewall-cmd --permanent --add-port=6443/tcp
firewall-cmd --permanent --add-port=2379-2380/tcp
firewall-cmd --permanent --add-port=10250-10252/tcp

# K8s Worker节点
firewall-cmd --permanent --add-port=10250/tcp
firewall-cmd --permanent --add-port=30000-32767/tcp

# 应用规则
firewall-cmd --reload

# 或关闭防火墙(测试环境)
systemctl stop firewalld
systemctl disable firewalld
```

---

## 五、故障排查工具和命令速查

### 快速诊断脚本

```bash
#!/bin/bash
# cluster-health-check.sh - 集群健康检查脚本

echo "=== 节点状态 ==="
kubectl get nodes -o wide

echo -e "\n=== 组件状态 ==="
kubectl get cs

echo -e "\n=== 系统Pod ==="
kubectl get pods -n kube-system

echo -e "\n=== 资源使用 ==="
kubectl top nodes

echo -e "\n=== 最近事件 ==="
kubectl get events --sort-by='.lastTimestamp' | tail -20

echo -e "\n=== 检查完成 ==="
```

### 常用诊断命令

| 场景 | 命令 |
|------|------|
| 节点状态 | `kubectl get nodes -o wide` |
| 组件健康 | `kubectl get cs` |
| Pod状态 | `kubectl get pods -A -o wide` |
| 查看详情 | `kubectl describe <resource> <name>` |
| 查看日志 | `kubectl logs <pod-name>` |
| 进入容器 | `kubectl exec -it <pod-name> -- /bin/sh` |
| 资源使用 | `kubectl top nodes/pods` |
| 事件查看 | `kubectl get events` |
| DNS测试 | `nslookup kubernetes.default` |
| 网络测试 | `kubectl run test --image=busybox --rm -it -- ping <ip>` |

---

## 六、获取帮助

### 日志收集

部署失败时收集关键日志：
```bash
# kubelet日志
journalctl -u kubelet > kubelet.log

# containerd日志
journalctl -u containerd > containerd.log

# etcd日志
journalctl -u etcd > etcd.log

# Pod日志
kubectl logs <pod-name> -n kube-system > pod.log

# 事件日志
kubectl get events > events.log
```

### 参考资源

- **kubeasz官方文档**: https://github.com/easzlab/kubeasz/tree/master/docs
- **Kubernetes官方文档**: https://kubernetes.io/docs
- **社区支持**: 微信群"k8s&kubeasz实践"(搜索微信号 badtobone)
- **问题反馈**: https://github.com/easzlab/kubeasz/issues

### 提问技巧

提问时提供以下信息能更快获得帮助：
1. 集群环境(AllinOne/生产环境)
2. 操作系统版本
3. kubeasz版本
4. 具体错误信息和日志
5. 已尝试的解决方案

---

**最后更新**: 2026-04-08  
**维护者**: kubeasz-deploy skill team