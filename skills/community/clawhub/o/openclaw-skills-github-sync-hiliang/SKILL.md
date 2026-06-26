---
name: openclaw-skills-github-sync
description: |
  将 OpenClaw skills 同步到 GitHub（非实时，需手动确认）。
  支持 Windows/Linux/Mac。
  使用场景：skill 创建或修改完成后同步到 GitHub
---

# OpenClaw Skills GitHub Sync Skill

> 将你的 OpenClaw skills 同步到 GitHub

## 功能

- ✅ 交互式配置向导
- ✅ 支持私有仓库同步
- ✅ 支持公开仓库同步
- ✅ 手动确认同步（非实时，更安全）
- ✅ 自动检测变更并提交推送
- ✅ 支持 Windows / Linux / Mac

## 支持平台

| 平台 | 脚本 |
|------|------|
| Windows | scripts/sync.ps1 |
| Linux | scripts/sync.sh |
| Mac | scripts/sync.sh |

## 安装方式

### Windows

```powershell
# 克隆到 OpenClaw skills 目录
cd $env:USERPROFILE\.openclaw\skills
git clone https://github.com/Hi-Jiajun/openclaw-skills-github-sync.git
```

### Linux / Mac

```bash
# 克隆到你的 OpenClaw skills 目录
cd ~/.openclaw/skills
git clone https://github.com/Hi-Jiajun/openclaw-skills-github-sync.git
```

## 快速开始

### Windows

```powershell
# 首次配置（交互式向导）
powershell -ExecutionPolicy Bypass -File "scripts/setup.ps1"

# 执行同步
powershell -ExecutionPolicy Bypass -File "scripts/sync.ps1"
```

### Linux / Mac

```bash
# 首次配置（交互式向导）
chmod +x scripts/setup.sh
./scripts/setup.sh

# 执行同步
chmod +x scripts/sync.sh
./scripts/sync.sh
```

## 安全说明

### 重要：排除敏感目录

本工具会自动创建 .gitignore 文件，包含以下排除项：

```
credentials/
*.key
*.pem
.DS_Store
*.log
```

**使用前请确保**：
1. 仓库中已包含 .gitignore 文件
2. 敏感目录（如 credentials/）已被排除
3. 推送前运行 `git status` 确认要推送的内容

### 同步前确认

脚本会：
1. 检查 .gitignore 是否存在，如不存在则自动创建
2. 显示将要推送的文件列表
3. 询问确认后才执行推送

## 注意事项

- 公开仓库建议设置为私有
- 同步前务必检查 .gitignore 配置
- credentials/ 目录请确保已排除
