# k8s-ops 安装指南

## 系统要求

- kubectl 命令行工具
- 有效的 kubeconfig 文件
- Kubernetes 集群访问权限

## 安装 kubectl

### macOS

```bash
# 使用 Homebrew
brew install kubectl

# 或使用 curl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

### Linux

```bash
# 使用 curl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# 或使用包管理器
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y kubectl

# CentOS/RHEL
sudo yum install -y kubectl
```

### Windows

```powershell
# 使用 Chocolatey
choco install kubernetes-cli

# 或使用 curl
curl -LO "https://dl.k8s.io/release/v1.28.0/bin/windows/amd64/kubectl.exe"
```

## 配置 kubeconfig

### 使用云服务商配置

```bash
# AWS EKS
aws eks update-kubeconfig --name <cluster-name>

# Google GKE
gcloud container clusters get-credentials <cluster-name> --zone <zone>

# Azure AKS
az aks get-credentials --resource-group <resource-group> --name <cluster-name>
```

### 手动配置

```bash
# 创建 .kube 目录
mkdir -p ~/.kube

# 复制 kubeconfig 文件
cp /path/to/your/kubeconfig ~/.kube/config

# 设置权限
chmod 600 ~/.kube/config
```

## 验证安装

```bash
# 检查 kubectl 版本
kubectl version --client

# 检查集群连接
kubectl cluster-info

# 查看节点
kubectl get nodes
```

## 安装 k8s-ops 插件

### 使用 ClawHub

```bash
# 安装 k8s-ops 技能
clawhub install k8s-ops
```

### 手动安装

```bash
# 克隆仓库
git clone https://github.com/CN-big-cabbage/k8s-ops.git

# 进入目录
cd k8s-ops

# 查看可用工具
ls -la
```

## 配置权限

### 创建 ServiceAccount

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: k8s-ops-sa
  namespace: default
```

### 创建 ClusterRoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: k8s-ops-binding
subjects:
- kind: ServiceAccount
  name: k8s-ops-sa
  namespace: default
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
```

## 下一步

安装完成后，请参阅 [快速开始指南](02-quickstart.md) 学习基本用法。
