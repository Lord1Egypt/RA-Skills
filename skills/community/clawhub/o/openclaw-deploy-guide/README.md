# OpenClaw Deploy 部署指南

OpenClaw（NEUXSBOT）全平台部署指南，支持 **macOS、Windows、Linux** 三平台一键安装。

## 🎯 支持平台

| 平台 | 安装方式 | 难度 |
|------|----------|------|
| **macOS** | DMG / 脚本 / Homebrew | ⭐ 简单 |
| **Windows** | EXE / 脚本 / 绿色版 | ⭐ 简单 |
| **Linux** | DEB / RPM / 脚本 / Docker | ⭐⭐ 中等 |

## 🚀 快速开始

### macOS

```bash
# 方法 1：DMG 安装
curl -LO https://github.com/Markovmodcn/openclaw-china/releases/latest/download/NEUXSBOT.dmg
# 双击安装

# 方法 2：脚本安装
curl -fsSL https://raw.githubusercontent.com/Markovmodcn/openclaw-china/main/scripts/install.sh | bash
```

### Windows

```powershell
# 方法 1：下载安装包
# 访问 https://github.com/Markovmodcn/openclaw-china/releases/latest
# 下载 NEUXSBOT-Setup.exe

# 方法 2：PowerShell 脚本
iwr -useb https://raw.githubusercontent.com/Markovmodcn/openclaw-china/main/scripts/install.ps1 | iex
```

### Linux

```bash
# Ubuntu/Debian
wget https://github.com/Markovmodcn/openclaw-china/releases/latest/download/nexusbot_amd64.deb
sudo dpkg -i nexusbot_amd64.deb

# 或一键脚本
curl -fsSL https://raw.githubusercontent.com/Markovmodcn/openclaw-china/main/scripts/install.sh | bash

# 或 Docker
docker run -d -p 3000:3000 markovmodcn/nexusbot:latest
```

## 📖 完整文档

详见 [skill.md](skill.md) 获取完整部署指南。

## 🎨 部署流程

```
1. 系统准备 → 2. 安装软件 → 3. 配置 AI → 4. 对接平台 → 5. 验证运行
```

## 🛠️ 包含内容

- ✅ 三平台详细安装步骤
- ✅ AI 模型配置（本地/在线）
- ✅ 消息平台对接（钉钉/飞书/企微）
- ✅ Docker 部署方案
- ✅ 故障排除指南
- ✅ 更新升级说明

## 📚 参考

- [NEUXSBOT 官网](https://www.neuxsbot.com)
- [OpenClaw China](https://github.com/Markovmodcn/openclaw-china)
- [OpenClaw 文档](https://www.neuxsbot.com/docs)

---

*让 AI 助手部署变得简单*
