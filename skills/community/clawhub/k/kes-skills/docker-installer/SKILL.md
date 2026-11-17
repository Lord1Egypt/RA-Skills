---
name: docker-installer
name_for_command: docker-installer
description: Docker 通用安装与配置指南。当用户提到 Docker 安装、Docker Desktop、Docker Engine、镜像源、Aliyun 加速器、WSL 2、Homebrew Docker 时，必须使用此技能。
---

# Docker 通用安装与配置指南

本技能提供 Docker 在各平台上的安装和配置方法，是 `kes-docker` 的前置依赖。

## Linux 安装

### Ubuntu/Debian

```bash
# 卸载旧版本
sudo apt-get remove docker docker-engine docker.io containerd runc

# 设置存储库
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 启动
sudo systemctl enable docker
sudo systemctl start docker
```

### CentOS/Rocky/AlmaLinux

```bash
# 卸载旧版本
sudo yum remove docker docker-client docker-containerd docker-engine

# 设置存储库
sudo dnf install -y dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 安装
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 启动
sudo systemctl enable docker
sudo systemctl start docker
```

### Fedora

```bash
sudo dnf install -y docker buildah podman-docker
sudo systemctl enable --now docker
```

## 国内镜像源配置

### Docker 镜像加速器（阿里云）

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json << 'EOF'
{
  "registry-mirrors": [
    "https://docker.1panel.live",
    "https://hub.rat.dev",
    "https://huecker.io"
  ]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

> 阿里云个人镜像加速器需登录阿里云控制台获取专属地址。

## Windows 安装

### Docker Desktop（推荐 Windows 10/11）

1. 下载 Docker Desktop for Windows
2. 运行安装程序
3. 启用 WSL 2（安装程序会引导）
4. 重启后启动 Docker Desktop

### WSL 2 安装

```powershell
# 以管理员身份运行 PowerShell
wsl --install

# 重启后设置默认分发版
wsl --set-default Ubuntu

# 安装 Docker
wsl docker -v
```

## macOS 安装

### Homebrew

```bash
brew install --cask docker
```

### 手动安装

1. 下载 Docker Desktop for Mac
2. 拖拽到 Applications
3. 启动并登录

## 验证安装

```bash
docker --version
docker run --rm hello-world
docker compose version
```

## 常用配置

### 非 root 用户使用 Docker

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

### Docker Compose

```bash
# 检查是否已安装
docker compose version

# 如未安装，单独安装
sudo curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## 相关技能

- **kes-docker** — KingbaseES Docker 容器化部署

## 参考文档

```
docker-installer/
├── SKILL.md          # 本文件
└── test-cases.md
```
