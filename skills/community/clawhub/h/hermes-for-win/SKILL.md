---
name: "hermes-for-win"
description: "一键安装、部署和管理 hermes Agent 和 hermes-webui 在 Windows 系统上，包括开机自启动、后台常驻和自动更新功能。调用时机：当 Windows 用户想要快速安装和配置 hermes 生态时。"
---

# hermes-for-win

在 Windows 系统上一键安装、部署和管理 hermes Agent 和 hermes-webui，让你轻松拥有完整的 hermes 生态！

## 功能特性

- 🚀 **一键安装** - 自动下载并配置 hermes Agent 和 hermes-webui
- 🔧 **开机自启** - Windows 登录时自动启动服务
- 💻 **后台运行** - 无窗口后台常驻运行
- 🔄 **自动更新** - 支持一键检查并更新到最新版本
- 📊 **状态监控** - 查看服务运行状态和日志

## 快速开始

### 前置要求

1. Windows 10/11 (64位)
2. WSL2 已启用并安装 Ubuntu
3. 至少 4GB 可用内存

### 安装步骤

1. 下载并运行 `install-hermes.ps1`
2. 按照提示输入配置信息
3. 等待安装完成
4. 访问 http://localhost:8787 即可使用

## 使用指南

### 查看服务状态

```powershell
cd .trae\skills\hermes-for-win\scripts
.\check-status.ps1
```

### 手动启动/停止服务

```powershell
.\start-services.ps1
.\stop-services.ps1
```

### 更新到最新版本

```powershell
.\update-hermes.ps1
```

### 配置开机自启

```powershell
.\setup-autostart.ps1
```

## 目录结构

```
hermes-for-win/
├── SKILL.md              # 本文件
├── scripts/              # 所有脚本
│   ├── install-hermes.ps1       # 一键安装脚本
│   ├── start-services.ps1       # 启动服务
│   ├── stop-services.ps1        # 停止服务
│   ├── check-status.ps1         # 查看状态
│   ├── update-hermes.ps1        # 更新脚本
│   └── setup-autostart.ps1      # 配置开机自启
└── references/           # 参考文档
    └── README.md
```

## 故障排查

如果遇到问题，请检查：
1. WSL2 是否正常运行
2. 端口 8787 是否被占用
3. 查看日志文件：`~/hermes_logs/`

## 许可证

MIT License
