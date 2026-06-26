---
name: k3s-deploy
description: 自动化部署 K3s Kubernetes 集群到多台 Linux 服务器。支持自动镜像拉取、网络配置检测、CNI 插件安装。使用场景：(1) 从零部署 K3s 集群，(2) 修复 NotReady 节点，(3) 批量部署多节点集群。触发条件：用户提到 K3s、Kubernetes 部署、集群安装、节点加入等。
---

# K3s 自动化部署技能

## 快速开始

```bash
# 使用部署脚本（推荐）
./scripts/deploy-k3s.sh \
  --master 10.1.9.177 \
  --masters-user root \
  --masters-pass 'your-password' \
  --worker 10.1.9.178,10.1.9.179 \
  --workers-user root \
  --workers-pass 'your-password'
```

## 工作流程

### 1. 部署前检查
- 检查服务器连通性
- 验证 SSH 凭据
- 检测操作系统版本（支持 CentOS 7+/Ubuntu 18.04+）

### 2. 安装 K3s
- Master 节点：安装 K3s server
- Worker 节点：加入集群

### 3. 部署网络插件
- 自动检测网络接口（ens192/eth0 等）
- 拉取国内镜像源 flannel
- 创建 CNI 配置文件

### 4. 健康检查
- 验证所有节点 Ready
- 验证 CoreDNS 运行
- 测试 Pod 调度

## 可用脚本

| 脚本 | 用途 |
|------|------|
| `scripts/deploy-k3s.sh` | 一键部署完整集群 |
| `scripts/pull-images.sh` | 预拉取必要镜像 |
| `scripts/check-cluster.sh` | 集群健康检查 |

## 故障排查

常见问题见 `references/troubleshooting.md`

### 快速诊断

```bash
# 检查节点状态
kubectl get nodes

# 检查系统 Pod
kubectl get pods -n kube-system

# 查看 Pod 详情
kubectl describe pod <pod-name> -n kube-system

# 查看 kubelet 日志
journalctl -u kubelet -n 50
```

## 配置说明

### 网络接口自动检测

脚本会自动执行以下命令检测默认路由接口：
```bash
ip route | grep default | awk '{print $5}'
```

### 镜像源

默认使用华为云镜像：
- Flannel: `swr.cn-north-4.myhuaweicloud.com/ddn-k8s/quay.io/coreos/flannel:v0.15.1`
- Pause: `registry.aliyuncs.com/google_containers/pause:3.9`

### CNI 配置

Flannel v0.15.1 需要手动创建 CNI 配置文件，脚本会自动完成：
```bash
# 在所有节点创建 /etc/cni/net.d/10-flannel.conflist
```

## 最佳实践

1. **提前拉取镜像** - 使用 `pull-images.sh` 在所有节点预拉取
2. **统一时间** - 确保所有节点 NTP 同步
3. **防火墙** - 关闭防火墙或开放必要端口
4. **Swap** - K3s 要求关闭 Swap

## 输出

部署完成后生成：
- `cluster-info.md` - 集群配置摘要
- `deployment-log.txt` - 详细部署日志
