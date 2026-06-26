# AllinOne 快速部署指南

本文档帮助你快速部署单节点 Kubernetes 集群，适合学习、测试和开发环境。AllinOne 模式将所有组件（etcd、master、worker）部署在同一台机器上。

---

## 一、适用场景

### 推荐使用场景

- **Kubernetes 学习与实验**：快速体验 K8s 功能，学习集群操作
- **应用开发测试**：搭建本地开发环境，测试应用部署
- **功能验证**：验证应用在 K8s 环境中的运行情况
- **CI/CD 测试环境**：作为持续集成的测试集群

### 资源要求

**最低配置（测试）：**
- CPU: 2核
- 内存: 4GB
- 硬盘: 30GB+

**推荐配置：**
- CPU: 4核
- 内存: 8GB
- 硬盘: 50GB+

### 系统要求

- 操作系统：Ubuntu 22.04/20.04、CentOS 7/8、Debian 10/11 等
- **重要**：必须是干净的系统，不能使用曾经装过 kubeadm 或其他 K8s 发行版的环境

### 前置条件检查

参考 [01-prerequisites.md](01-prerequisites.md) 完成以下检查：
- [ ] 系统版本符合要求
- [ ] 资源配置满足最低要求
- [ ] 网络连通性正常
- [ ] 必要端口未被占用

---

## 二、部署方法

### 方法一：一键自动部署（推荐）

适用于快速体验，使用默认配置自动完成所有部署步骤。

#### 步骤 1：下载安装脚本

```bash
# 设置版本号（建议使用最新稳定版本）
export release=3.6.7

# 下载 ezdown 工具
wget https://github.com/easzlab/kubeasz/releases/download/${release}/ezdown
chmod +x ./ezdown
```

**验证下载：**
```bash
ls -lh ezdown
# 应显示文件存在且有执行权限
```

#### 步骤 2：下载所需文件

下载 kubeasz 代码、二进制文件和容器镜像：

```bash
# 国内环境（推荐）
./ezdown -D

# 海外环境
# ./ezdown -D -m standard
```

**说明：**
- `-D`：下载所有必需文件（代码、二进制、镜像）
- 下载内容存储在 `/etc/kubeasz/` 目录
- 下载时间取决于网络速度，约 10-30 分钟

**可选：下载额外组件**
```bash
# 下载 Dashboard（Web 管理界面）
./ezdown -X dashboard

# 下载 Prometheus（监控套件）
./ezdown -X prometheus

# 查看更多选项
./ezdown
```

#### 步骤 3：启动 kubeasz 容器

```bash
./ezdown -S
```

**验证容器运行：**
```bash
docker ps | grep kubeasz
# 应看到 kubeasz 容器运行中
```

#### 步骤 4：一键部署集群

```bash
docker exec -it kubeasz ezctl start-aio
```

**执行过程：**
- 自动创建 `default` 集群配置
- 按序执行所有部署步骤
- 整个过程约 10-20 分钟

**查看详细日志：**
```bash
# 实时查看部署日志
docker exec -it kubeasz tail -f /etc/kubeasz/ansible.log
```

---

### 方法二：手动配置部署

适用于需要自定义配置的场景。

#### 步骤 1-3：同方法一

完成文件下载和容器启动（同上）。

#### 步骤 4：创建集群配置

```bash
# 创建新集群配置（示例：k8s-01）
docker exec -it kubeasz ezctl new k8s-01
```

**输出示例：**
```
2021-01-19 10:48:23 DEBUG generate custom cluster files in /etc/kubeasz/clusters/k8s-01
2021-01-19 10:48:23 DEBUG set version of common plugins
2021-01-19 10:48:23 DEBUG cluster k8s-01: files successfully created.
2021-01-19 10:48:23 INFO next steps 1: to config '/etc/kubeasz/clusters/k8s-01/hosts'
2021-01-19 10:48:23 INFO next steps 2: to config '/etc/kubeasz/clusters/k8s-01/config.yml'
```

#### 步骤 5：修改集群配置

**配置节点信息（hosts）：**
```bash
# 编辑 hosts 文件
vi /etc/kubeasz/clusters/k8s-01/hosts
```

**AllinOne 模式示例：**
```ini
# etcd 集群
[etcd]
192.168.1.100

# master 节点
[kube_master]
192.168.1.100

# worker 节点
[kube_node]
192.168.1.100
```

**配置集群参数（config.yml）：**
```bash
vi /etc/kubeasz/clusters/k8s-01/config.yml
```

可自定义参数示例：
```yaml
# 集群名称
CLUSTER_NAME: "k8s-01"

# K8s 版本
K8S_VER: "v1.28.0"

# 容器运行时（containerd 或 docker）
CONTAINER_RUNTIME: "containerd"

# 网络插件（calico, flannel, cilium 等）
NETWORK_PLUGIN: "calico"

# 集群网段
CLUSTER_CIDR: "172.16.0.0/16"
SERVICE_CIDR: "172.20.0.0/16"
```

#### 步骤 6：执行部署

**一键部署：**
```bash
# 设置命令别名
source ~/.bashrc

# 执行部署
docker exec -it kubeasz ezctl setup k8s-01 all
```

**或分步部署（便于排查问题）：**
```bash
# 步骤 01：系统环境初始化
docker exec -it kubeasz ezctl setup k8s-01 01

# 步骤 02：安装 etcd
docker exec -it kubeasz ezctl setup k8s-01 02

# 步骤 03：安装容器运行时
docker exec -it kubeasz ezctl setup k8s-01 03

# 步骤 04：安装 master 节点
docker exec -it kubeasz ezctl setup k8s-01 04

# 步骤 05：安装 worker 节点
docker exec -it kubeasz ezctl setup k8s-01 05

# 步骤 06：安装网络插件
docker exec -it kubeasz ezctl setup k8s-01 06

# 步骤 07：安装集群附加组件
docker exec -it kubeasz ezctl setup k8s-01 07
```

**查看所有步骤：**
```bash
docker exec -it kubeasz ezctl help setup
```

---

## 三、部署监控

### 查看部署进度

**实时日志：**
```bash
# 查看 ansible 执行日志
docker exec -it kubeasz tail -f /etc/kubeasz/ansible.log
```

**查看集群状态：**
```bash
# 加载 kubectl 配置
source ~/.bashrc

# 查看节点状态
kubectl get node -o wide

# 查看所有 Pod
kubectl get pod -A

# 查看组件状态
kubectl get cs
```

### 部署阶段说明

| 阶段 | 步骤编号 | 主要任务 | 预计时间 |
|:--|:--|:--|:--|
| 环境准备 | 01 | 系统初始化、依赖安装 | 2-3 分钟 |
| etcd 安装 | 02 | 安装 etcd 集群 | 2-3 分钟 |
| 容器运行时 | 03 | 安装 containerd/docker | 3-5 分钟 |
| Master 安装 | 04 | 安装 kube-apiserver 等 | 5-8 分钟 |
| Node 安装 | 05 | 安装 kubelet/kube-proxy | 2-3 分钟 |
| 网络插件 | 06 | 安装 CNI 网络插件 | 2-3 分钟 |
| 附加组件 | 07 | 安装 coredns/metrics 等 | 2-3 分钟 |

---

## 四、成功指标

### 节点状态验证

```bash
# 查看节点状态
kubectl get node

# 期望输出
NAME           STATUS   ROLES           AGE   VERSION
192.168.1.100  Ready    control-plane   10m   v1.28.0
```

**成功指标：**
- STATUS 为 `Ready`
- ROLES 包含 `control-plane`

### 组件状态验证

```bash
# 查看组件健康状态
kubectl get cs

# 期望输出
NAME                 STATUS    MESSAGE             ERROR
scheduler            Healthy   ok
controller-manager   Healthy   ok
etcd-0               Healthy   {"health":"true"}
```

### Pod 状态验证

```bash
# 查看所有命名空间的 Pod
kubectl get pod -A

# 期望输出（示例）
NAMESPACE     NAME                                       READY   STATUS    AGE
kube-system   calico-kube-controllers-xxx               1/1     Running   8m
kube-system   calico-node-xxx                            1/1     Running   8m
kube-system   coredns-xxx                                1/1     Running   7m
kube-system   kube-apiserver-192.168.1.100               1/1     Running   9m
kube-system   kube-controller-manager-192.168.1.100     1/1     Running   9m
kube-system   kube-proxy-xxx                             1/1     Running   8m
kube-system   kube-scheduler-192.168.1.100               1/1     Running   9m
kube-system   metrics-server-xxx                        1/1     Running   7m
```

**成功指标：**
- 所有 Pod 状态为 `Running`
- READY 列显示 `1/1` 或 `n/n`
- 无 `ImagePullBackOff`、`CrashLoopBackOff` 等错误状态

---

## 五、应用测试

### 部署测试应用

**创建 Nginx 测试部署：**
```bash
# 创建部署
kubectl create deployment nginx-test --image=nginx:alpine

# 暴露服务
kubectl expose deployment nginx-test --port=80 --target-port=80 --name=nginx-svc

# 查看部署状态
kubectl get deployment nginx-test
kubectl get pod -l app=nginx-test
kubectl get svc nginx-svc
```

### 验证应用运行

```bash
# 查看 Pod 详情
kubectl describe pod -l app=nginx-test

# 测试服务访问
kubectl get svc nginx-svc
# 记录 CLUSTER-IP，例如：172.20.1.100

# 在集群内测试
kubectl run test-curl --rm -it --image=curlimages/curl -- curl http://<CLUSTER-IP>/

# 或使用端口转发（本地测试）
kubectl port-forward svc/nginx-svc 8080:80 &
curl http://localhost:8080/
```

**成功指标：**
- Pod 状态为 Running
- Service 分配了 ClusterIP
- curl 命令返回 Nginx 欢迎页面

### 清理测试资源

```bash
kubectl delete deployment nginx-test
kubectl delete svc nginx-svc
```

---

## 六、故障排查

### 常见问题 1：部署超时

**现象：**
```
TASK [xxx] : fatal: [192.168.1.100]: FAILED! => {"msg": "Timeout waiting for ..."}
```

**原因分析：**
- 网络问题导致镜像下载慢
- 系统资源不足
- DNS 解析问题

**解决方案：**
```bash
# 检查网络连接
ping -c 3 github.com
ping -c 3 k8s.gcr.io

# 检查系统资源
free -h
df -h /var

# 检查 DNS 解析
nslookup k8s.gcr.io

# 重试部署（从头开始）
docker exec -it kubeasz ezctl destroy default
docker exec -it kubeasz ezctl start-aio

# 或从失败步骤继续
docker exec -it kubeasz ezctl setup default <步骤编号>
```

**预防措施：**
- 确保网络畅通，必要时配置代理
- 提前下载镜像：`./ezdown -D`
- 确保系统资源充足

### 常见问题 2：镜像拉取失败

**现象：**
```
Failed to pull image "xxx": rpc error: code = Unknown
ImagePullBackOff
```

**原因分析：**
- 镜像仓库无法访问
- 镜像未预先下载

**解决方案：**
```bash
# 检查镜像是否存在
ls -lh /etc/kubeasz/down/

# 手动加载镜像
docker load -i /etc/kubeasz/down/xxx.tar

# 或重新下载
./ezdown -D

# 查看镜像列表
docker images
```

### 常见问题 3：节点 NotReady

**现象：**
```bash
kubectl get node
NAME           STATUS       ROLES           AGE   VERSION
192.168.1.100  NotReady     control-plane   10m   v1.28.0
```

**排查步骤：**
```bash
# 查看节点详情
kubectl describe node 192.168.1.100

# 查看 kubelet 日志
journalctl -u kubelet -f

# 查看网络插件状态
kubectl get pod -n kube-system | grep calico
# 或
kubectl get pod -n kube-system | grep flannel

# 检查容器运行时状态
systemctl status containerd
# 或
systemctl status docker
```

**常见原因与解决：**
- 网络插件未启动：检查 CNI Pod 状态
- 容器运行时异常：重启 containerd/docker
- 节点资源不足：释放资源或扩容

### 常见问题 4：Pod 一直处于 Pending

**现象：**
```
nginx-test-xxx   0/1   Pending   0     5m
```

**排查步骤：**
```bash
# 查看 Pod 详情
kubectl describe pod nginx-test-xxx

# 查看事件
kubectl get events --sort-by='.lastTimestamp'

# 检查节点资源
kubectl describe node 192.168.1.100 | grep -A 5 "Allocated resources"
```

**常见原因：**
- 资源不足（CPU/内存）
- 存储卷挂载失败
- 节点选择器不匹配

### 常见问题 5：CoreDNS 异常

**现象：**
```
coredns-xxx   0/1   CrashLoopBackOff   3   5m
```

**排查步骤：**
```bash
# 查看 Pod 日志
kubectl logs -n kube-system coredns-xxx

# 检查 DNS 配置
kubectl get configmap coredns -n kube-system -o yaml

# 测试 DNS 解析
kubectl run test-dns --rm -it --image=busybox -- nslookup kubernetes
```

**常见原因：**
- 网络插件未正常运行
- DNS 配置错误
- 与系统 DNS 冲突

### 常见问题 6：部署失败重新部署

**完全清理后重新部署：**
```bash
# 1. 销毁集群
docker exec -it kubeasz ezctl destroy default

# 2. 重启节点（清理网络配置）
reboot

# 3. 重新部署
docker exec -it kubeasz ezctl start-aio
```

**查看错误日志：**
```bash
# ansible 日志
docker exec -it kubeasz cat /etc/kubeasz/ansible.log

# 系统日志
journalctl -xe

# kubelet 日志
journalctl -u kubelet -n 100
```

---

## 七、后续操作

### 访问 Dashboard

如果安装了 Dashboard：
```bash
# 获取 Dashboard 服务
kubectl get svc -n kubernetes-dashboard

# 端口转发访问
kubectl port-forward -n kubernetes-dashboard service/kubernetes-dashboard 10443:443 &

# 浏览器访问
https://localhost:10443/
```

### 部署应用

参考 [03-ha-deployment.md](03-ha-deployment.md) 了解：
- 应用部署最佳实践
- 持久化存储配置
- Ingress 配置

### 扩展集群

从 AllinOne 扩展为多节点集群：
```bash
# 添加 master 节点
docker exec -it kubeasz ezctl add-master default <新节点IP>

# 添加 worker 节点
docker exec -it kubeasz ezctl add-node default <新节点IP>
```

### 清理集群

```bash
# 销毁集群
docker exec -it kubeasz ezctl destroy default

# 重启节点（清理残留配置）
reboot
```

---

## 八、参考信息

### 命令速查

| 命令 | 说明 |
|:--|:--|
| `./ezdown -D` | 下载所有必需文件 |
| `./ezdown -S` | 启动 kubeasz 容器 |
| `docker exec -it kubeasz ezctl start-aio` | 一键部署 AllinOne |
| `docker exec -it kubeasz ezctl setup default all` | 完整部署指定集群 |
| `docker exec -it kubeasz ezctl destroy default` | 销毁集群 |
| `kubectl get node` | 查看节点状态 |
| `kubectl get pod -A` | 查看所有 Pod |
| `kubectl get cs` | 查看组件状态 |
| `kubectl cluster-info` | 查看集群信息 |

### 目录结构

```
/etc/kubeasz/               # kubeasz 主目录
├── bin/                    # 二进制文件（kubectl, etcd 等）
├── down/                   # 离线镜像和系统包
│   └── packages/           # 系统依赖包
├── clusters/               # 集群配置
│   └── default/            # default 集群配置
│       ├── hosts           # 节点配置
│       └── config.yml      # 集群参数配置
└── ansible.log             # 部署日志
```

### 相关文档

- [前置条件与环境检查](01-prerequisites.md)
- [高可用集群部署指南](03-ha-deployment.md)
- [kubeasz 官方文档](https://github.com/easzlab/kubeasz)
- [ezctl 命令详解](https://github.com/easzlab/kubeasz/blob/master/docs/setup/ezctl.md)

---

**部署成功标志：**
- ✅ 节点状态为 Ready
- ✅ 组件状态为 Healthy
- ✅ 所有系统 Pod 运行正常
- ✅ 测试应用部署成功

**遇到问题？**
1. 查看本指南第六节"故障排查"
2. 检查 [前置条件](01-prerequisites.md)
3. 参考 [kubeasz Issues](https://github.com/easzlab/kubeasz/issues)