# 生产环境部署指南

本指南详细介绍生产环境 Kubernetes 集群的部署流程，涵盖架构规划、配置详解、镜像拉取解决方案（重点）、部署验证及后续配置建议。

---

## 一、生产架构规划

### 1.1 推荐拓扑结构

生产环境建议采用 **3 etcd + 3 master + N worker** 的高可用架构：

```
+------------------+    +------------------+    +------------------+
| Master-01        |    | Master-02        |    | Master-03        |
| 192.168.1.1      |    | 192.168.1.2      |    | 192.168.1.3      |
| etcd ✓           |    | etcd ✓           |    | etcd ✓           |
| kube-apiserver ✓ |    | kube-apiserver ✓ |    | kube-apiserver ✓ |
| kube-scheduler ✓ |    | kube-scheduler ✓ |    | kube-scheduler ✓ |
| kube-controller  |    | kube-controller  |    | kube-controller  |
+------------------+    +------------------+    +------------------+

+------------------+    +------------------+    +------------------+
| Worker-01        |    | Worker-02        |    | Worker-03...     |
| 192.168.1.4      |    | 192.168.1.5      |    | 192.168.1.6...   |
| kubelet ✓        |    | kubelet ✓        |    | kubelet ✓        |
| kube-proxy ✓     |    | kube-proxy ✓     |    | kube-proxy ✓     |
| 应用负载         |    | 应用负载         |    | 应用负载         |
+------------------+    +------------------+    +------------------+
```

### 1.2 高可用设计要点

**etcd 集群**
- 奇数节点（1、3、5...），推荐 3 节点起步
- 所有 etcd 节点需互通、时间同步（偏差 < 50ms）
- 磁盘性能关键：建议 SSD，顺序 IOPS ≥ 500
- 独立 WAL 目录可提升性能（避免磁盘 IO 竞争）

**Master 高可用**
- 至少 2 个 master 节点，推荐 3 个
- 内置 HA：使用 nginx/haproxy 本地代理，自动负载均衡
- 外部 HA：可选外部 LB（如 HAProxy + Keepalived），提供 VIP

**Worker 节点**
- 根据应用负载规划节点数量
- 单节点建议资源：8c/32g 内存/200g 硬盘以上
- 考虑资源预留（kubelet、系统组件）

### 1.3 机器配置建议

| 角色 | 数量 | 配置建议 | 说明 |
|:-----|:-----|:---------|:-----|
| 部署节点 | 1 | 4c/8g/50g | 运行 ansible/ezctl，通常复用第一个 master |
| etcd 节点 | 3 | 4c/8g/50g SSD | etcd 集群需奇数节点，通常复用 master |
| master 节点 | 3 | 4c/8g/50g | 高可用集群至少 2 个 master |
| worker 节点 | N | 8c/32g/200g+ | 运行应用负载，按需增加 |

### 1.4 网络规划

**Pod CIDR（容器网络）**
- 默认：`172.20.0.0/16`
- 不能与节点网络重叠
- 每个节点分配子网掩码长度决定 Pod 数量上限（默认 24，每节点最多 256 个 Pod）

**Service CIDR（服务网络）**
- 默认：`10.68.0.0/16`
- 不能与节点网络、Pod CIDR 重叠
- NodePort 范围：`30000-32767`

**网络插件选择**
- **Calico**：推荐生产环境，支持 BGP、性能好、策略丰富
- **Flannel**：简单易用，适合中小规模集群
- **Cilium**：基于 eBPF，高性能、安全性强
- **Kube-OVN**：基于 OVN，支持子网隔离、IPAM

---

## 二、六步部署流程

### 步骤 1：创建集群配置实例

**AI 执行说明**：AI 将调用 `ezctl new` 命令创建集群配置目录。

```bash
# 启动 kubeasz 容器（如果尚未运行）
./ezdown -S

# 创建新集群配置，例如 k8s-01
docker exec -it kubeasz ezctl new k8s-01
# 或者使用 alias（推荐）
source ~/.bashrc  # 加载 alias dk='docker exec -it kubeasz'
dk ezctl new k8s-01
```

**执行结果**：
```
2021-01-19 10:48:23 DEBUG generate custom cluster files in /etc/kubeasz/clusters/k8s-01
2021-01-19 10:48:23 DEBUG set version of common plugins
2021-01-19 10:48:23 DEBUG cluster k8s-01: files successfully created.
2021-01-19 10:48:23 INFO next steps 1: to config '/etc/kubeasz/clusters/k8s-01/hosts'
2021-01-19 10:48:23 INFO next steps 2: to config '/etc/kubeasz/clusters/k8s-01/config.yml'
```

生成两个关键配置文件：
- `/etc/kubeasz/clusters/k8s-01/hosts` - 节点清单和集群参数
- `/etc/kubeasz/clusters/k8s-01/config.yml` - 组件版本和详细配置

---

### 步骤 2：配置 hosts 文件

**AI 执行说明**：AI 将根据用户提供的节点信息生成 hosts 配置。

**关键配置项详解**：

```ini
# etcd 集群（奇数节点）
[etcd]
192.168.1.1
192.168.1.2
192.168.1.3

# master 节点（建议设置唯一 k8s_nodename）
[kube_master]
192.168.1.1 k8s_nodename='master-01'
192.168.1.2 k8s_nodename='master-02'
192.168.1.3 k8s_nodename='master-03'

# worker 节点
[kube_node]
192.168.1.4 k8s_nodename='worker-01'
192.168.1.5 k8s_nodename='worker-02'

# [可选] Harbor 私有仓库
[harbor]
#192.168.1.8 NEW_INSTALL=false

# [可选] 外部负载均衡器
[ex_lb]
#192.168.1.6 LB_ROLE=backup EX_APISERVER_VIP=192.168.1.250
#192.168.1.7 LB_ROLE=master EX_APISERVER_VIP=192.168.1.250

[all:vars]
# --------- 集群主要参数 ---------------
SECURE_PORT="6443"                   # apiserver 安全端口

# 容器运行时：docker 或 containerd（K8s >= 1.24 仅支持 containerd）
CONTAINER_RUNTIME="containerd"

# 网络插件：calico, flannel, kube-router, cilium, kube-ovn
CLUSTER_NETWORK="calico"

# kube-proxy 模式：iptables 或 ipvs（推荐 ipvs）
PROXY_MODE="ipvs"

# Service CIDR
SERVICE_CIDR="10.68.0.0/16"

# Pod CIDR
CLUSTER_CIDR="172.20.0.0/16"

# NodePort 范围
NODE_PORT_RANGE="30000-32767"

# 集群 DNS 域名
CLUSTER_DNS_DOMAIN="cluster.local"
```

**配置要点**：
- `k8s_nodename` 必须唯一，格式：小写字母、数字、'-' 或 '.'，开头结尾必须为字母数字
- `CONTAINER_RUNTIME`：K8s 1.24+ 必选 `containerd`
- `CLUSTER_NETWORK`：生产环境推荐 `calico`
- `PROXY_MODE`：`ipvs` 性能更好，适合大规模集群
- CIDR 配置不能与节点网络重叠

---

### 步骤 3：配置 config.yml

**AI 执行说明**：AI 将根据用户需求调整 config.yml，特别是版本选择和镜像配置。

**关键配置参数**：

```yaml
############################
# 部署准备
############################
# 离线安装系统软件包：offline 或 online
INSTALL_SOURCE: "online"

############################
# role:deploy
############################
# CA 证书有效期：默认 100 年
CA_EXPIRY: "876000h"
# 组件证书有效期：默认 50 年
CERT_EXPIRY: "438000h"

# K8s 版本（根据 kubeasz 版本自动设置，可手动修改）
K8S_VER: "v1.28.2"

############################
# role:runtime [containerd,docker]
############################
# 【重点】启用镜像加速仓库（解决国内镜像拉取问题）
ENABLE_MIRROR_REGISTRY: true

# 信任的私有仓库（必须包含协议头）
INSECURE_REG:
  - "http://easzlab.io.local:5000"
  - "https://reg.yourcompany.com"

# pause 容器镜像（离线安装时已推送到本地仓库）
SANDBOX_IMAGE: "easzlab.io.local:5000/easzlab/pause:3.9"

# containerd 存储目录（可调整到独立磁盘）
CONTAINERD_ROOT_DIR: "/var/lib/containerd"

############################
# role:etcd
############################
# etcd 数据目录
ETCD_DATA_DIR: "/var/lib/etcd"
# etcd WAL 目录（独立磁盘可提升性能）
ETCD_WAL_DIR: ""

############################
# role:kube-master
############################
# master 证书额外 IP/域名（可添加公网 IP/域名）
MASTER_CERT_HOSTS:
  - "10.1.1.1"
  - "k8s.easzlab.io"

# 每个节点 Pod 子网掩码长度（默认 24，最多 256 Pod）
NODE_CIDR_LEN: 24

############################
# role:kube-node
############################
# kubelet 根目录
KUBELET_ROOT_DIR: "/var/lib/kubelet"

# 单节点最大 Pod 数
MAX_PODS: 110

# kube 组件资源预留
KUBE_RESERVED_ENABLED: "no"

############################
# role:network [calico]
############################
# Calico 覆盖网络模式：Always, CrossSubnet, Never
CALICO_ENABLE_OVERLAY: "Always"

# Calico 网络 backend：bird, vxlan, none
CALICO_NETWORKING_BACKEND: "bird"

# Calico IP 自动检测方法
IP_AUTODETECTION_METHOD: "can-reach={{ groups['kube_master'][0] }}"
```

---

### 步骤 4：验证 SSH 免密连接

**AI 执行说明**：AI 将测试所有节点的 SSH 连接。

**配置 SSH 免密登录**（部署前必须完成）：

```bash
# 在部署节点生成 SSH 密钥（如果尚未生成）
ssh-keygen -t rsa -b 2048

# 复制公钥到所有节点（包括部署节点自身）
ssh-copy-id 192.168.1.1
ssh-copy-id 192.168.1.2
ssh-copy-id 192.168.1.3
ssh-copy-id 192.168.1.4
ssh-copy-id 192.168.1.5

# 测试 SSH 连接
for ip in 192.168.1.1 192.168.1.2 192.168.1.3 192.168.1.4 192.168.1.5; do
  ssh $ip "hostname && date"
done
```

**验证结果**：所有节点应无需密码即可 SSH 登录。

---

### 步骤 5：执行部署

**AI 执行说明**：AI 将调用 ezctl 执行部署，监控进度，处理异常。

#### 方式 A：一键部署（快速但不易排查问题）

```bash
dk ezctl setup k8s-01 all
```

#### 方式 B：分步部署（推荐，便于排查）

**查看分步帮助**：
```bash
dk ezctl help setup
```

**分步执行**：
```bash
# 步骤 01：创建证书和环境准备
dk ezctl setup k8s-01 01

# 步骤 02：安装 etcd 集群
dk ezctl setup k8s-01 02

# 步骤 03：安装容器运行时（containerd/docker）
dk ezctl setup k8s-01 03

# 步骤 04：安装 kube-master 节点
dk ezctl setup k8s-01 04

# 步骤 05：安装 kube-node 节点
dk ezctl setup k8s-01 05

# 步骤 06：安装网络插件
dk ezctl setup k8s-01 06

# 步骤 07：安装集群插件（coredns、metrics-server）
dk ezctl setup k8s-01 07
```

**每步验证**（推荐做法）：
- 步骤 01 后：检查 `/etc/kubernetes/ssl/` 证书文件
- 步骤 02 后：验证 etcd 集群健康（见下文"etcd 验证"）
- 步骤 03 后：检查容器运行时服务状态
- 步骤 04 后：验证 master 节点组件
- 步骤 05 后：验证 worker 节点状态
- 步骤 06 后：检查网络插件 Pod
- 步骤 07 后：验证集群插件

---

### 步骤 6：部署验证

#### etcd 集群验证

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

# 预期结果：所有节点返回 healthy
https://192.168.1.1:2379 is healthy: successfully committed proposal: took = 2.210885ms
https://192.168.1.2:2379 is healthy: successfully committed proposal: took = 2.784043ms
https://192.168.1.3:2379 is healthy: successfully committed proposal: took = 3.275705ms
```

#### Kubernetes 集群验证

```bash
# 获取节点状态
kubectl get nodes

# 预期结果：所有节点 Ready
NAME        STATUS   ROLES           AGE   VERSION
master-01   Ready    control-plane   5m    v1.28.2
master-02   Ready    control-plane   5m    v1.28.2
master-03   Ready    control-plane   5m    v1.28.2
worker-01   Ready    <none>          4m    v1.28.2
worker-02   Ready    <none>          4m    v1.28.2

# 检查系统 Pod
kubectl get pods -n kube-system

# 预期结果：所有系统 Pod Running
NAME                                       READY   STATUS    AGE
calico-kube-controllers-xxx                1/1     Running   4m
calico-node-xxx                            1/1     Running   4m
coredns-xxx                                1/1     Running   4m
metrics-server-xxx                         1/1     Running   4m

# 检查组件状态
kubectl get cs

# 预期结果：所有组件 Healthy
NAME                 STATUS    MESSAGE                         ERROR
controller-manager   Healthy   ok                              
scheduler            Healthy   ok                              
etcd-0               Healthy   {"health":"true","reason":""}  
etcd-1               Healthy   {"health":"true","reason":""}  
etcd-2               Healthy   {"health":"true","reason":""}  
```

---

## 三、镜像拉取解决方案（重点）

国内用户部署 Kubernetes 最常见的痛点是 **镜像拉取失败**。kubeasz 提供多种解决方案，本节详细说明每种方法的适用场景和操作步骤。

### 方案 A：离线安装模式（强烈推荐）

**适用场景**：
- 生产环境部署
- 无法访问外网的内网环境
- 需要快速稳定部署

**原理**：提前下载所有镜像到本地，推送到内置私有仓库 `easzlab.io.local:5000`

**操作步骤**：

#### 1. 在有网环境下载离线包

```bash
# 下载 ezdown 工具（kubeasz 3.6.0 示例）
export release=3.6.0
wget https://github.com/easzlab/kubeasz/releases/download/${release}/ezdown
chmod +x ./ezdown

# 下载 kubeasz 代码、二进制、默认容器镜像
./ezdown -D

# [可选] 下载额外镜像（按需）
./ezdown -X flannel
./ezdown -X prometheus
./ezdown -X cilium

# [可选] 下载离线系统包（无法使用 yum/apt 时）
./ezdown -P ubuntu_22   # Ubuntu 22.04
./ezdown -P centos_7    # CentOS 7
```

**下载结果**：
```
/etc/kubeasz/          # kubeasz 代码
/etc/kubeasz/bin/      # k8s/etcd/containerd 等二进制
/etc/kubeasz/down/     # 离线容器镜像
/etc/kubeasz/down/packages/  # 系统软件包
```

#### 2. 复制到目标部署环境

```bash
# 将整个 /etc/kubeasz 目录复制到离线服务器
scp -r /etc/kubeasz root@目标服务器:/etc/kubeasz/
```

#### 3. 在目标环境导入镜像

```bash
# 在目标服务器执行
cd /etc/kubeasz
./ezdown -D            # 导入镜像到本地仓库
./ezdown -X flannel    # 导入额外镜像（如果下载了）
./ezdown -S            # 启动 kubeasz 容器
```

#### 4. 配置离线安装

```bash
# 设置离线安装模式
sed -i 's/^INSTALL_SOURCE.*$/INSTALL_SOURCE: "offline"/g' /etc/kubeasz/clusters/k8s-01/config.yml

# 确保 hosts 文件中启用本地仓库
# config.yml 中 SANDBOX_IMAGE 使用 easzlab.io.local:5000 地址
```

**优势**：
- ✅ 完全解决镜像拉取问题
- ✅ 部署速度快、稳定可靠
- ✅ 适合无外网环境
- ✅ 版本可控，避免镜像版本不一致

**注意事项**：
- 需提前在有网环境下载
- 离线包较大（约 1-2GB），确保磁盘空间充足
- 不同 kubeasz 版本离线包不同，需匹配版本

---

### 方案 B：镜像加速器配置

**适用场景**：
- 有外网访问但速度较慢
- 能连接 docker.io 但经常超时
- 不方便提前下载离线包

**原理**：kubeasz 自动配置国内镜像加速器，加速 docker.io 镜像拉取

**kubeasz 内置加速器列表**（自动配置）：
```json
"registry-mirrors": [
  "https://docker.1ms.run",
  "https://hub1.nat.tf",
  "https://docker.1panel.live",
  "https://hub.rat.dev",
  "https://docker.amingg.com"
]
```

**配置方式**：

#### 1. 在 config.yml 启用镜像加速

```yaml
############################
# role:runtime
############################
# 启用镜像加速仓库（默认已启用）
ENABLE_MIRROR_REGISTRY: true
```

#### 2. 部署时自动生效

```bash
# 执行步骤 03（安装容器运行时）时自动配置加速器
dk ezctl setup k8s-01 03

# 验证配置（containerd）
cat /etc/containerd/certs.d/docker.io/hosts.toml

# 验证配置（docker）
cat /etc/docker/daemon.json | grep registry-mirrors
```

**生效机制**：
- **containerd**：配置 `/etc/containerd/certs.d/docker.io/hosts.toml`
- **docker**：配置 `/etc/docker/daemon.json` 的 `registry-mirrors`
- 拉取 `docker.io/xxx` 镜像时自动从加速器拉取

**优势**：
- ✅ 无需手动下载离线包
- ✅ kubeasz 自动配置，简单易用
- ✅ 多个加速器互备，提高成功率
- ✅ 对原有镜像地址无需修改

**注意事项**：
- 依赖加速器服务稳定性（可能变化）
- 某些镜像可能不在加速器缓存中
- 适合可访问外网的环境

**加速器状态查询**：
https://status.1panel.top/status/docker （查看当前可用加速器）

---

### 方案 C：国内镜像源

**适用场景**：
- k8s.gcr.io 镜像无法拉取
- 需要手动修改镜像地址

**原理**：kubeasz 使用 easzlab 镜像仓库替代 k8s.gcr.io

**kubeasz 默认镜像源**：
- **pause**：`easzlab.io.local:5000/easzlab/pause:3.9`
- **coredns**：`easzlab.io.local:5000/easzlab/coredns:1.9.3`
- **metrics-server**：`easzlab.io.local:5000/easzlab/metrics-server:v0.5.0`

**离线安装时自动使用本地仓库**：
- 离线镜像已推送到 `easzlab.io.local:5000`
- 配置文件中镜像地址已修改为本地仓库

**手动配置国内镜像源**（如果未使用离线安装）：

```yaml
# config.yml 中修改镜像地址
SANDBOX_IMAGE: "easzlab/pause:3.9"  # 使用 easzlab 镜像
```

**其他常用国内镜像源**：
- **阿里云**：`registry.cn-hangzhou.aliyuncs.com/google_containers/`
- **腾讯云**：`ccr.ccs.tencentyun.com/google_containers/`
- **网易云**：`hub-mirror.c.163.com/google_containers/`

**使用示例**（手动修改镜像地址）：
```yaml
# 例如 coredns 镜像
# 原地址：k8s.gcr.io/coredns/coredns:v1.9.3
# 替换为：registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:v1.9.3
```

**优势**：
- ✅ 解决 k8s.gcr.io 无法访问问题
- ✅ 国内镜像源速度快
- ✅ kubeasz 已内置常用镜像源

**注意事项**：
- 需手动确认镜像源是否有对应镜像
- 不同镜像源镜像版本可能不同
- 部分镜像可能需要手动拉取并改名

---

### 方案 D：手动拉取并重命名

**适用场景**：
- 特定镜像无法从任何加速器或镜像源拉取
- 需要使用特定版本镜像
- 临时解决个别镜像拉取失败

**原理**：从可用源拉取镜像，重新打 tag 为目标名称

**操作步骤**：

#### 1. 从国内镜像源拉取

```bash
# 示例：拉取 pause 镜像
# 目标：k8s.gcr.io/pause:3.9
# 替代源：阿里云

docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/pause:3.9

# 或者使用 easzlab 源
docker pull easzlab/pause:3.9
```

#### 2. 重命名镜像

```bash
# 重命名为目标名称
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/pause:3.9 \
  k8s.gcr.io/pause:3.9

# 推送到本地仓库（如果集群使用私有仓库）
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/pause:3.9 \
  easzlab.io.local:5000/easzlab/pause:3.9
docker push easzlab.io.local:5000/easzlab/pause:3.9
```

#### 3. 更新配置文件

```yaml
# config.yml 中使用重命名后的镜像地址
SANDBOX_IMAGE: "k8s.gcr.io/pause:3.9"
# 或使用本地仓库地址
SANDBOX_IMAGE: "easzlab.io.local:5000/easzlab/pause:3.9"
```

#### 4. 分发到所有节点

```bash
# 如果不使用私有仓库，需在每个节点手动拉取
for node in 192.168.1.1 192.168.1.2 192.168.1.3; do
  ssh $node "docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/pause:3.9"
  ssh $node "docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/pause:3.9 k8s.gcr.io/pause:3.9"
done
```

**常见需要手动拉取的镜像**：
- `k8s.gcr.io/pause:*`
- `k8s.gcr.io/coredns/coredns:*`
- `k8s.gcr.io/metrics-server/metrics-server:*`
- `docker.io/calico/*`
- `quay.io/calico/*`

**优势**：
- ✅ 解决任何镜像拉取失败问题
- ✅ 灵活控制镜像版本
- ✅ 适合特殊镜像需求

**注意事项**：
- 需手动操作，工作量较大
- 需确保所有节点镜像一致
- 新增节点时需重复操作

---

### 方案选择建议

| 方案 | 适用场景 | 推荐度 | 工作量 | 稳定性 |
|:-----|:---------|:-------|:-------|:-------|
| A - 离线安装 | 生产环境、无外网环境 | ★★★★★ | 中等 | 最高 |
| B - 镜像加速器 | 有外网、速度慢 | ★★★★☆ | 低 | 高 |
| C - 国内镜像源 | k8s.gcr.io 无法访问 | ★★★☆☆ | 中等 | 中 |
| D - 手动拉取 | 特殊镜像、临时解决 | ★★☆☆☆ | 高 | 中 |

**推荐组合**：
- **生产环境**：方案 A（离线安装）为主，确保稳定可靠
- **测试环境**：方案 B（镜像加速器）即可，简单快速
- **应急解决**：方案 D（手动拉取）解决个别镜像问题

---

## 四、部署后验证

### 4.1 集群健康检查

```bash
# 检查节点状态（所有节点应为 Ready）
kubectl get nodes -o wide

# 检查组件状态（scheduler、controller-manager、etcd 应为 Healthy）
kubectl get cs

# 检查系统 Pod（所有 Pod 应为 Running）
kubectl get pods -n kube-system -o wide

# 检查网络插件 Pod（Calico 示例）
kubectl get pods -n kube-system -l k8s-app=calico-node

# 检查 DNS Pod
kubectl get pods -n kube-system -l k8s-app=kube-dns

# 检查 metrics-server
kubectl get pods -n kube-system -l k8s-app=metrics-server
```

### 4.2 功能验证测试

#### Pod 网络测试

```bash
# 创建测试 Pod
kubectl run test-net --image=busybox --restart=Never -- sleep 3600

# 测试 Pod 间网络
kubectl exec test-net -- ping <其他 Pod IP>

# 清理测试 Pod
kubectl delete pod test-net
```

#### Service 测试

```bash
# 创建测试 Deployment
kubectl create deployment nginx --image=nginx

# 创建 Service
kubectl expose deployment nginx --port=80 --target-port=80

# 测试 Service 访问
kubectl run test-svc --image=busybox --restart=Never -- wget -q nginx:80

# 清理
kubectl delete deployment nginx
kubectl delete svc nginx
kubectl delete pod test-svc
```

#### DNS 测试

```bash
# 测试 DNS 解析
kubectl run test-dns --image=busybox --restart=Never -- nslookup kubernetes.default

# 预期结果
Server:    10.68.0.2
Address 1: 10.68.0.2 kube-dns.kube-system.svc.cluster.local

Name:      kubernetes.default
Address 1: 10.68.0.1 kubernetes.default.svc.cluster.local
```

### 4.3 验证成功标志

**集群部署成功的标志**：
- ✅ 所有节点状态为 `Ready`
- ✅ etcd 集群所有节点 `healthy`
- ✅ scheduler、controller-manager 状态 `Healthy`
- ✅ 系统所有 Pod 状态为 `Running`
- ✅ Pod 间网络互通
- ✅ Service 可以正常访问
- ✅ DNS 解析正常

---

## 五、部署后配置建议

### 5.1 持久化存储

**推荐方案**：
- **Local PV**：单节点存储，适合开发测试
- **NFS PV**：简单共享存储，适合小规模集群
- **Ceph RBD**：分布式存储，适合生产环境
- **GlusterFS**：分布式存储，开源方案

**快速配置 NFS 存储**：

```bash
# 安装 NFS provisioner（参考 kubeasz docs/setup/08-cluster-storage.md）
kubectl apply -f https://raw.githubusercontent.com/kubernetes-incubator/external-storage/master/nfs-client/deploy/deployment.yaml

# 创建 StorageClass
kubectl apply -f https://raw.githubusercontent.com/kubernetes-incubator/external-storage/master/nfs-client/deploy/class.yaml

# 测试 PVC
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
```

### 5.2 Ingress 控制器

**推荐方案**：
- **Nginx Ingress**：最成熟、功能丰富
- **Traefik**：云原生、动态配置
- **HAProxy Ingress**：高性能、TCP/UDP 支持

**安装 Nginx Ingress**：

```bash
# 安装
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml

# 验证
kubectl get pods -n ingress-nginx
```

### 5.3 监控系统

**推荐方案**：
- **Prometheus + Grafana**：开源监控标准方案
- **kube-prometheus-stack**：一站式监控栈

**快速安装**：

```bash
# 使用 kubeasz 额外镜像
./ezdown -X prometheus

# 安装 Prometheus（参考 kubeasz docs/guide/prometheus.md）
```

### 5.4 日志系统

**推荐方案**：
- **ELK Stack**：Elasticsearch + Logstash + Kibana
- **EFK Stack**：Elasticsearch + Fluentd + Kibana
- **Loki**：云原生日志系统，轻量级

### 5.5 Dashboard

**安装 Kubernetes Dashboard**：

```bash
# 安装
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

# 创建访问令牌
kubectl create serviceaccount dashboard-admin -n kubernetes-dashboard
kubectl create clusterrolebinding dashboard-admin --clusterrole=cluster-admin --serviceaccount=kubernetes-dashboard:dashboard-admin
kubectl create token dashboard-admin -n kubernetes-dashboard

# 访问（需配置 Ingress 或 NodePort）
kubectl proxy
# 浏览器访问：http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```

---

## 六、集群扩容方法

### 6.1 增加 worker 节点

**AI 执行说明**：AI 将调用 `ezctl add-node` 命令添加节点。

```bash
# 前置准备
# 1. 新节点配置 SSH 免密登录
ssh-copy-id 192.168.1.6

# 2. 新节点系统准备（参考前置条件检查）
#    - 系统版本一致
#    - 时间同步
#    - 禁用 swap
#    - 网络互通

# 添加节点
dk ezctl add-node k8s-01 192.168.1.6

# 验证
kubectl get nodes
```

### 6.2 增加 master 节点

**AI 执行说明**：AI 将调用 `ezctl add-master` 命令添加 master。

```bash
# 前置准备同 worker 节点

# 添加 master
dk ezctl add-master k8s-01 192.168.1.7

# 验证
kubectl get nodes
kubectl get cs  # etcd 应新增成员
```

### 6.3 增加 etcd 节点

**注意**：etcd 通常复用 master 节点。如需单独 etcd 节点：

```bash
# 添加 etcd 节点
dk ezctl add-etcd k8s-01 192.168.1.8

# 验证 etcd 集群
etcdctl member list
```

### 6.4 删除节点

**删除 worker 节点**：

```bash
# 先驱逐 Pod
kubectl drain 192.168.1.6 --delete-emptydir-data --ignore-daemonsets

# 删除节点
dk ezctl del-node k8s-01 192.168.1.6

# 验证
kubectl get nodes
```

**删除 master 节点**（谨慎操作）：

```bash
# 确保剩余 master ≥ 2
kubectl drain 192.168.1.7 --delete-emptydir-data --ignore-daemonsets
dk ezctl del-master k8s-01 192.168.1.7
```

---

## 七、常见问题与排查

### 7.1 部署阶段常见问题

**镜像拉取失败**：
- 现象：Pod 状态 `ImagePullBackOff` 或 `ErrImagePull`
- 排查：`kubectl describe pod <pod-name>`
- 解决：参考"镜像拉取解决方案"，优先使用离线安装

**etcd 启动失败**：
- 现象：etcd 服务无法启动，日志报错
- 排查：`journalctl -u etcd`
- 原因：时间不同步、证书错误、磁盘性能不足、网络不通
- 解决：检查时间同步、证书、磁盘、网络

**网络插件失败**：
- 现象：calico/flannel Pod 无法启动
- 排查：`kubectl logs -n kube-system <calico-node>`
- 原因：内核版本过低、网卡配置错误、端口冲突
- 解决：升级内核、检查网卡配置、调整 Calico 配置

**节点 NotReady**：
- 现象：节点状态 `NotReady`
- 排查：`kubectl describe node <node-name>`
- 原因：kubelet 未启动、网络插件未就绪、证书错误
- 解决：检查 kubelet 服务、网络插件、证书

### 7.2 运维阶段常见问题

**Pod 无法调度**：
- 现象：Pod 状态 `Pending`
- 排查：`kubectl describe pod <pod-name>`
- 原因：资源不足、节点污点、PVC 未绑定
- 解决：扩容节点、调整 Pod 配置、配置存储

**DNS 解析失败**：
- 现象：Pod 无法解析域名
- 排查：`kubectl exec <pod> -- nslookup kubernetes`
- 原因：coredns Pod 异常、网络不通、配置错误
- 解决：检查 coredns Pod、Pod 网络、DNS 配置

### 7.3 获取帮助

**日志收集**：

```bash
# 收集 etcd 日志
journalctl -u etcd --no-pager > etcd.log

# 收集 kubelet 日志
journalctl -u kubelet --no-pager > kubelet.log

# 收集 containerd 日志
journalctl -u containerd --no-pager > containerd.log
```

**诊断命令汇总**：

```bash
# 集群信息
kubectl cluster-info
kubectl get nodes -o wide
kubectl get cs
kubectl get pods -n kube-system -o wide

# 资源使用
kubectl top nodes
kubectl top pods -n kube-system

# 事件查看
kubectl get events --sort-by='.lastTimestamp'

# 组件日志
kubectl logs -n kube-system <pod-name>
journalctl -u etcd -u kubelet -u containerd
```

**参考资源**：
- kubeasz 文档：https://github.com/easzlab/kubeasz/tree/master/docs
- Kubernetes 官方文档：https://kubernetes.io/docs/
- kubeasz Issues：https://github.com/easzlab/kubeasz/issues

---

## 八、总结

生产环境部署 Kubernetes 集群的关键要点：

1. **架构规划**：3 etcd + 3 master + N worker，确保高可用
2. **配置准确**：hosts 文件节点信息、config.yml 版本参数
3. **镜像拉取**：优先使用离线安装，解决国内镜像问题
4. **分步部署**：推荐分步执行，便于排查问题
5. **验证完整**：etcd 健康、节点 Ready、系统 Pod Running、网络互通、DNS 正常
6. **后续配置**：存储、Ingress、监控、日志
7. **扩容灵活**：ezctl 命令轻松增加节点

**AI 助手能力**：
- AI 可评估环境、生成配置、执行部署、验证结果、诊断问题
- 遇到镜像拉取问题时，AI 会推荐离线安装方案
- 部署失败时，AI 会根据日志诊断并提供解决方案

**下一步**：
- 部署后验证：参考 [04-post-deploy.md](./04-post-deploy.md)
- 故障排查：参考 [troubleshooting.md](../troubleshooting.md)
- 集群运维：参考 kubeasz `docs/op/` 目录

---

**文档版本**：v1.0.0  
**更新日期**：2026-04-08  
**参考文档**：kubeasz docs/setup/