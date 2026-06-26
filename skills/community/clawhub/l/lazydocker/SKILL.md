---
name: lazydocker
description: lazydocker - Docker 和 Docker Compose 的终端 UI 管理工具
version: 0.1.1
metadata:
  openclaw:
    requires:
      bins:
        - docker
        - lazydocker
    emoji: 🐳
    homepage: https://github.com/jesseduffield/lazydocker
---

# lazydocker Docker 终端 UI 管理助手

## 技能概述

本技能帮助用户通过 lazydocker 的终端 UI 界面管理 Docker 容器、镜像、卷和网络，支持以下场景：
- **容器管理**: 查看、启动、停止、重启、删除容器，实时查看日志和资源占用
- **镜像管理**: 列出、拉取、删除镜像，查看镜像层信息
- **卷管理**: 查看和删除 Docker 卷
- **Docker Compose**: 管理 Compose 服务的完整生命周期
- **实时监控**: 查看 CPU、内存、网络 I/O 等实时统计信息

**支持平台**: macOS、Linux、Windows（WSL2）、Docker Desktop

## 使用流程

AI 助手将引导你完成以下步骤：
1. 检查并安装 lazydocker（如未安装）
2. 确认 Docker 守护进程正在运行
3. 启动 lazydocker 并进入 TUI 界面
4. 根据需求执行容器/镜像/卷操作
5. 验证操作结果

## 关键章节导航

- [安装指南](./guides/01-installation.md)
- [快速开始](./guides/02-quickstart.md)
- [高级用法](./guides/03-advanced-usage.md)
- [常见问题](./troubleshooting.md)

## AI 助手能力

当你向 AI 描述 Docker 管理需求时，AI 会：
- 自动检测系统环境并安装 lazydocker
- 验证 Docker 守护进程状态
- 指导键盘快捷键操作
- 解析容器/镜像/卷的状态信息
- 协助调试容器启动失败问题
- 生成 Docker Compose 配置并通过 lazydocker 管理服务

## 核心功能

- 容器面板：查看所有容器状态、日志、统计信息
- 镜像面板：浏览本地镜像，支持删除和拉取
- 卷面板：管理 Docker 持久化卷
- 服务面板：Docker Compose 服务管理（需在 compose 项目目录启动）
- 网络面板：查看 Docker 网络配置
- 实时日志：容器日志流式展示，支持搜索
- 自定义命令：支持在 config.yml 中配置自定义操作
- 键盘驱动：完整键盘导航，无需鼠标

## 界面布局

```
┌─────────────────────────────────────────────────────────────┐
│  Containers │  Services │  Images │  Volumes │  Networks    │
├─────────────┴───────────┴─────────┴──────────┴──────────────┤
│ 左侧面板：列表视图                                           │
│  container1  running   nginx:latest                          │
│  container2  exited    redis:7.0                             │
├──────────────────────────────────────────────────────────────┤
│ 右侧面板：详情/日志/统计                                     │
│  [Logs] [Stats] [Config] [Env] [Exec]                        │
└──────────────────────────────────────────────────────────────┘
```

## 常用键盘快捷键速查

| 按键 | 功能 |
|------|------|
| `[` / `]` | 切换左侧面板标签（容器/服务/镜像/卷/网络） |
| `↑` / `↓` | 在列表中上下移动 |
| `←` / `→` | 切换右侧详情标签 |
| `enter` | 进入容器（exec bash/sh） |
| `s` | 停止容器 |
| `r` | 重启容器 |
| `d` | 删除容器/镜像/卷 |
| `u` | 拉取最新镜像（在服务面板） |
| `l` | 查看日志 |
| `e` | 打开文件编辑器 |
| `x` | 显示可用命令菜单 |
| `q` | 退出 lazydocker |
| `?` | 打开帮助界面 |

## 快速示例

```bash
# 启动 lazydocker
lazydocker

# 在项目目录中启动（自动识别 Docker Compose）
cd /path/to/compose-project && lazydocker

# 指定 Docker 上下文
DOCKER_HOST=tcp://remote-host:2375 lazydocker
```

## 安装要求

- Docker Engine 或 Docker Desktop
- Go 1.19+（仅从源码编译时需要）
- 终端支持 256 色（推荐）
- 支持 macOS 10.15+、Ubuntu 18.04+、Windows 10（WSL2）

## 许可证

MIT License

## 项目链接

- GitHub: https://github.com/jesseduffield/lazydocker
- 作者: Jesse Duffield（同时是 lazygit 的作者）
