# 前置条件与环境检查

本文档帮助你验证部署环境是否符合 kubeasz 集群安装要求。**务必在开始部署前完成所有检查项**，避免因环境问题导致部署失败。

---

## 一、系统要求

### 支持的操作系统

kubeasz 支持以下 Linux 发行版：

| 操作系统 | 支持版本 | 备注 |
|:-|:-|:-|
| **Ubuntu** | 16.04, 18.04, 20.04, 22.04, 24.04 | 推荐 Ubuntu 22.04/24.04 |
| **CentOS/RHEL** | 7, 8, 9 | 推荐 CentOS 7/8 |
| **Debian** | 10, 11 | 需注意配置差异 |
| **Alma Linux** | 8, 9 | CentOS 替代方案 |
| **Rocky Linux** | 8, 9 | CentOS 替代方案 |
| **Alibaba Linux** | 2.1903, 3.2104 | 阿里云发行版 |
| **Anolis OS** | 8.x RHCK, 8.x ANCK | 阿里云开源发行版 |
| **Fedora** | 34, 35, 36, 37 | 测试环境可选 |
| **Kylin Linux** | V10 Tercel/Lance/Halberd | 麒麟操作系统 |
| **openEuler** | 22.03 LTS, 24.03 LTS | 华开源操作系统 |
| **openSUSE** | Leap 15.x | 需注意配置差异 |

### 系统版本验证

**检查命令：**
```bash
# Ubuntu/Debian
cat /etc/os-release

# CentOS/RHEL
cat /etc/redhat-release

# 通用方法
uname -a
```

**期望结果：** 系统版本在上述支持列表中。

---

## 二、系统资源建议

### AllinOne 快速体验（单节点测试）

**最低配置（仅供测试）：**
- CPU: 2核
- 内存: 4GB
- 硬盘: 30GB+

**推荐配置：**
- CPU: 4核
- 内存: 8GB
- 硬盘: 50GB+

### 生产环境部署（多节点高可用）

**节点配置建议：**

| 角色 | 数量 | CPU | 内存 | 硬盘 | 说明 |
|:-|:-|:-|:-|:-|:-|
| 部署节点 | 1 | 2核+ | 2GB+ | 20GB+ | 运行 ansible/ezctl 命令，通常复用第一个 master |
| etcd 节点 | 3 | 2核+ | 4GB+ | 50GB+ | 必须奇数节点(1/3/5)，通常复用 master |
| master 节点 | 2+ | 4核+ | 8GB+ | 50GB+ | 高可用至少 2 个 master |
| worker 节点 | N | 8核+ | 32GB+ | 200GB+ | 根据应用负载调整配置 |

**注意事项：**
- 默认配置下容器运行时和 kubelet 占用 `/var` 磁盘空间
- 如磁盘分区特殊，可在 config.yml 中设置：
  - `CONTAINERD_STORAGE_DIR`：容器运行时数据目录
  - `DOCKER_STORAGE_DIR`：Docker 数据目录（如使用 Docker）
  - `KUBELET_ROOT_DIR`：kubelet 数据目录

### 资源验证

**检查命令：**
```bash
# CPU 核数
lscpu | grep "CPU(s):"

# 内存信息
free -h

# 磁盘信息
df -h /var
```

---

## 三、网络要求

### 必需端口列表

**控制节点（Master）端口：**

| 端口 | 协议 | 组件 | 说明 |
|:-|:-|:-|:-|
| 6443 | TCP | kube-apiserver | Kubernetes API 服务端口 |
| 2379-2380 | TCP | etcd | etcd 客户端和集群通信端口 |
| 10250 | TCP | kubelet | kubelet API 端口 |
| 10251 | TCP | kube-scheduler | scheduler 端口 |
| 10252 | TCP | kube-controller-manager | controller-manager 端口 |

**工作节点（Worker）端口：**

| 端口 | 协议 | 组件 | 说明 |
|:-|:-|:-|:-|
| 10250 | TCP | kubelet | kubelet API 端口 |
| 30000-32767 | TCP | NodePort | Service NodePort 范围（可配置） |

**网络插件端口（视选择的插件而定）：**

| 插件 | 端口 | 说明 |
|:-|:-|:-|
| Calico | 179 (BGP), 4789 (VXLAN) | BGP 或 VXLAN 模式端口 |
| Flannel | 8472 (VXLAN), 4789 (VXLAN) | VXLAN 端口 |
| Cilium | 多端口 | 根据配置而定 |

### 网络互通性要求

**必需条件：**
1. 所有节点之间网络互通（部署节点能访问所有其他节点）
2. 所有节点能访问互联网（如使用在线安装）或本地镜像仓库（离线安装）
3. 节点时间同步（建议配置 NTP 或 chrony）
4. 节点主机名唯一且可解析（建议配置 DNS 或 `/etc/hosts`）

### 网络验证

**检查命令：**
```bash
# 检查节点间网络互通
ping <其他节点IP>

# 检查时间同步
date
timedatectl status

# 检查主机名解析
hostname
cat /etc/hosts
```

---

## 四、依赖工具

### 部署节点必需工具

**核心工具：**
- **Docker**：运行 kubeasz 容器（ansible 容器化运行方式）
- **SSH**：免密登录所有集群节点
- **wget/curl**：下载 kubeasz 工具脚本

**说明：**
- kubeasz 使用 Docker 容器运行 Ansible，无需在宿主机安装 Ansible 和 Python
- 容器内已包含完整的 Ansible 环境和所需依赖

### 集群节点系统工具

**自动安装的工具（由 kubeasz prepare 步骤安装）：**
- ipset、ipvsadm
- conntrack、socat
- libseccomp
- jq、psmisc
- 其他系统基础工具

**可选安装：**
- Python（如不使用容器化部署，需 Python 2.7 或 Python 3.5+）

### 工具验证

**检查命令：**
```bash
# 检查 Docker（部署节点）
docker version

# 检查 wget
wget --version

# 检查 SSH
ssh -V
```

---

## 五、环境检查流程

以下 5 个检查步骤必须在部署前完成：

### ✅ 检查 1：验证操作系统版本

**目的：** 确认系统版本在支持列表中。

**执行命令：**
```bash
cat /etc/os-release
```

**期望结果：**
- Ubuntu 显示 VERSION_ID 为 "16.04"/"18.04"/"20.04"/"22.04"/"24.04"
- CentOS 显示 VERSION 为 "7"/"8"/"9"
- 其他系统在支持列表中

**失败处理：**
- 升级到支持版本
- 或选择其他在列表中的操作系统

---

### ✅ 检查 2：验证系统资源

**目的：** 确认 CPU、内存、磁盘满足部署要求。

**执行命令：**
```bash
# 检查 CPU
echo "CPU 核数: $(lscpu | grep '^CPU(s):' | awk '{print $2}')"

# 检查内存
echo "总内存: $(free -h | grep 'Mem:' | awk '{print $2}')"

# 检查磁盘
echo "根分区可用空间: $(df -h / | tail -1 | awk '{print $4}')"
echo "/var 分区可用空间: $(df -h /var | tail -1 | awk '{print $4}')"
```

**期望结果（AllinOne）：**
- CPU ≥ 2核
- 内存 ≥ 4GB
- 磁盘 ≥ 30GB

**期望结果（生产环境）：**
- Master: CPU ≥ 4核, 内存 ≥ 8GB, 磁盘 ≥ 50GB
- Worker: CPU ≥ 8核, 内存 ≥ 32GB, 磁盘 ≥ 200GB

**失败处理：**
- 增加虚拟机配置
- 清理磁盘空间释放容量

---

### ✅ 检查 3：验证网络连通性

**目的：** 确认所有节点之间网络互通，时间同步。

**执行命令：**
```bash
# 检查节点互通（替换为实际节点IP）
ping -c 3 <node-ip-1>
ping -c 3 <node-ip-2>

# 检查时间同步
date && timedatectl status

# 检查主机名
hostnamectl
```

**期望结果：**
- ping 成功，延迟正常
- 所有节点时间一致（误差 < 1秒）
- 主机名唯一且可解析

**失败处理：**
- 配置网络路由或防火墙规则
- 安装 chrony 服务同步时间
- 配置 `/etc/hosts` 或 DNS

---

### ✅ 检查 4：验证 SSH 免密登录

**目的：** 确认部署节点可 SSH 免密登录所有集群节点。

**执行命令（在部署节点）：**
```bash
# 生成 SSH 密钥（如已有则跳过）
ssh-keygen -t rsa -b 2048 -N '' -f ~/.ssh/id_rsa

# 复制公钥到所有节点（替换为实际节点IP）
ssh-copy-id root@<node-ip-1>
ssh-copy-id root@<node-ip-2>
ssh-copy-id root@<node-ip-3>

# 验证免密登录
ssh root@<node-ip-1> 'hostname'
ssh root@<node-ip-2> 'hostname'
```

**期望结果：**
- SSH 登录无需密码输入
- 能成功执行远程命令

**失败处理：** 参考「六、环境不满足时的处理 - 1. 配置 SSH 免密登录」

---

### ✅ 检查 5：验证 Docker 安装

**目的：** 确认部署节点已安装 Docker（用于运行 kubeasz 容器）。

**执行命令：**
```bash
docker version
docker ps
```

**期望结果：**
- Docker 版本正常显示
- Docker 服务正常运行

**失败处理：** 参考「六、环境不满足时的处理 - 2. 安装 Docker」

---

## 六、环境不满足时的处理

### 1. 配置 SSH 免密登录

**如检查 4 未通过，执行以下步骤：**

```bash
# 在部署节点生成 SSH 密钥
ssh-keygen -t rsa -b 2048 -N '' -f ~/.ssh/id_rsa

# 复制公钥到所有目标节点（需输入目标节点 root 密码）
ssh-copy-id root@<node-ip>

# 验证免密登录成功
ssh root@<node-ip> 'echo SSH免密登录配置成功'
```

**批量配置方法（多个节点）：**

```bash
# 假设节点IP列表
NODE_IPS="192.168.1.1 192.168.1.2 192.168.1.3"

# 循环复制公钥
for ip in $NODE_IPS; do
  ssh-copy-id root@$ip
done

# 验证所有节点
for ip in $NODE_IPS; do
  ssh root@$ip 'hostname'
done
```

---

### 2. 安装 Docker

**如检查 5 未通过，执行以下步骤：**

**Ubuntu/Debian 系统：**

```bash
# 更新软件源
apt-get update

# 安装 Docker
apt-get install -y docker.io

# 启动 Docker 服务
systemctl start docker
systemctl enable docker

# 验证
docker version
```

**CentOS/RHEL 系统：**

```bash
# 安装必要工具
yum install -y yum-utils device-mapper-persistent-data lvm2

# 添加 Docker 官方源
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 安装 Docker
yum install -y docker-ce docker-ce-cli containerd.io

# 启动 Docker 服务
systemctl start docker
systemctl enable docker

# 验证
docker version
```

**国内镜像加速（可选）：**

```bash
# 创建 Docker 配置目录
mkdir -p /etc/docker

# 配置镜像加速器
cat > /etc/docker/daemon.json <<EOF
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}
EOF

# 重启 Docker
systemctl daemon-reload
systemctl restart docker
```

---

### 3. 安装 kubeasz

**如 Docker 已安装，下载并安装 kubeasz：**

```bash
# 设置 kubeasz 版本（参考 README.md 中的版本对照表）
export release=3.6.7

# 下载 ezdown 工具脚本
wget https://github.com/easzlab/kubeasz/releases/download/${release}/ezdown
chmod +x ./ezdown

# 下载 kubeasz 代码、二进制、默认容器镜像
# 国内环境使用
./ezdown -D

# 海外环境使用
# ./ezdown -D -m standard

# 启动 kubeasz 容器（包含 Ansible 环境）
./ezdown -S

# 验证 kubeasz 容器运行
docker ps | grep kubeasz
```

**说明：**
- `./ezdown -D`：下载 kubeasz 代码、二进制文件、容器镜像
- `./ezdown -S`：启动 kubeasz 容器，容器内已包含完整的 Ansible 环境
- 下载完成后，所有文件位于 `/etc/kubeasz` 目录

---

### 4. 配置时间同步（chrony）

**如节点时间不同步，安装 chrony 服务：**

**Ubuntu/Debian：**

```bash
apt-get install -y chrony
systemctl start chrony
systemctl enable chrony
```

**CentOS/RHEL：**

```bash
yum install -y chrony
systemctl start chronyd
systemctl enable chronyd
```

**验证时间同步：**

```bash
chronyc sources -v
chronyc tracking
```

---

### 5. 配置防火墙规则

**如节点间网络不通，检查并配置防火墙：**

**关闭防火墙（测试环境）：**

```bash
# CentOS/RHEL 7
systemctl stop firewalld
systemctl disable firewalld

# Ubuntu
systemctl stop ufw
systemctl disable ufw
```

**生产环境推荐开放端口：**

```bash
# CentOS/RHEL 7（firewalld）
firewall-cmd --permanent --add-port=6443/tcp
firewall-cmd --permanent --add-port=2379-2380/tcp
firewall-cmd --permanent --add-port=10250/tcp
firewall-cmd --permanent --add-port=30000-32767/tcp
firewall-cmd --reload

# Ubuntu（ufw）
ufw allow 6443/tcp
ufw allow 2379:2380/tcp
ufw allow 10250/tcp
ufw allow 30000:32767/tcp
```

---

## 七、环境检查清单

完成以下检查清单后，可以开始部署：

| 检查项 | 命令 | 期望结果 | 状态 |
|:-|:-|:-|:-|
| 操作系统版本 | `cat /etc/os-release` | 在支持列表中 | ☐ |
| CPU 资源 | `lscpu | grep 'CPU(s):'` | ≥ 2核（AllinOne）/≥ 4核（生产） | ☐ |
| 内存资源 | `free -h | grep 'Mem:'` | ≥ 4GB（AllinOne）/≥ 8GB（生产） | ☐ |
| 磁盘空间 | `df -h /var` | ≥ 30GB（AllinOne）/≥ 50GB（生产） | ☐ |
| 节点互通 | `ping <node-ip>` | ping 成功 | ☐ |
| 时间同步 | `date && timedatectl` | 时间一致 | ☐ |
| SSH 免密 | `ssh root@<node-ip>` | 无需密码 | ☐ |
| Docker 安装 | `docker version` | 版本显示正常 | ☐ |

---

## 八、常见问题

### 问题 1：操作系统不支持

**症状：** `cat /etc/os-release` 显示不在支持列表中的版本。

**解决：**
- 升级操作系统到支持版本
- 选择支持列表中的其他操作系统
- 参考 [multi_os.md](https://github.com/easzlab/kubeasz/blob/master/docs/setup/multi_os.md) 查看特殊系统配置

### 问题 2：磁盘空间不足

**症状：** `df -h` 显示可用空间 < 30GB。

**解决：**
- 清理系统日志：`journalctl --vacuum-size=100M`
- 清理旧容器镜像：`docker system prune -a`
- 扩展磁盘分区或增加虚拟机磁盘大小

### 问题 3：SSH 免密登录失败

**症状：** SSH 登录仍需输入密码。

**解决：**
- 检查目标节点 `/root/.ssh/authorized_keys` 是否包含公钥
- 检查目标节点 SSH 配置 `PermitRootLogin yes`
- 检查目标节点 `/root/.ssh` 目录权限（700）
- 检查 `authorized_keys` 文件权限（600）

### 问题 4：节点时间不同步

**症状：** 多个节点 `date` 显示时间不一致。

**解决：**
- 安装 chrony 服务
- 配置相同的时间服务器
- 验证 chrony 同步状态

### 问题 5：Docker 安装失败

**症状：** `docker version` 报错或无响应。

**解决：**
- 检查系统软件源配置
- 使用官方安装脚本：`curl -fsSL https://get.docker.com | bash`
- 国内用户可使用阿里云镜像源

---

## 九、下一步

环境检查全部完成后，请根据你的需求选择：

- **快速体验测试环境** → 参考 [02-allinone-quickstart.md](02-allinone-quickstart.md)
- **生产环境高可用部署** → 参考 [03-production-deploy.md](03-production-deploy.md)

---

## 十、参考资源

- [kubeasz 项目首页](https://github.com/easzlab/kubeasz)
- [系统支持说明](https://github.com/easzlab/kubeasz/blob/master/docs/setup/multi_os.md)
- [离线安装文档](https://github.com/easzlab/kubeasz/blob/master/docs/setup/offline_install.md)
- [chrony 时间同步配置](https://github.com/easzlab/kubeasz/blob/master/docs/guide/chrony.md)