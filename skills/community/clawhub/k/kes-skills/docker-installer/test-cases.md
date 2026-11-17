---
name: docker-installer
description: Docker 通用安装与配置 — 测试用例
---

# Docker 通用安装与配置测试用例

## 测试用例 1: Ubuntu 安装 Docker

**场景**：用户需要在 Ubuntu 上安装 Docker

**输入问题**："Ubuntu 怎么安装 Docker？"

**期望答案要点**：
- 卸载旧版本
- 设置存储库（GPG 密钥 + sources.list）
- 安装 docker-ce, docker-ce-cli, containerd.io
- 启用并启动 systemctl

**验证方法**：答案包含完整的安装步骤

---

## 测试用例 2: 国内镜像源配置

**场景**：Docker 拉取速度慢，需要配置国内镜像源

**输入问题**："Docker 怎么配置国内镜像源？"

**期望答案要点**：
- /etc/docker/daemon.json 配置
- registry-mirrors 列表
- systemctl daemon-reload && restart docker

**验证方法**：答案包含 daemon.json 配置和重载命令
