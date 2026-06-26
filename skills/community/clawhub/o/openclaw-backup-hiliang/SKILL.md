---
name: openclaw-backup
description: |
  自动备份 OpenClaw 本地存储配置文件。支持 Windows/Linux/Mac。
  使用场景：(1) 定期备份配置 (2) 迁移配置 (3) 恢复配置
  
  这是一个 OpenClaw 备份工具 skill，提供交互式配置向导。
---

# OpenClaw Backup Skill

> 自动备份 OpenClaw 配置，让数据永不丢失

## 功能

- ✅ 交互式配置向导
- ✅ 每日自动备份（可配置时间）
- ✅ 保留最近 N 个备份
- ✅ 旧备份自动转移和清理
- ✅ 按容量自动清理旧备份
- ✅ 支持 Windows / Linux / Mac

## 支持平台

| 平台 | 脚本 |
|------|------|
| Windows | scripts/backup.ps1 |
| Linux | scripts/backup.sh |
| Mac | scripts/backup.sh |

## 安装方式

### Windows

```powershell
# 克隆到 OpenClaw skills 目录
cd $env:USERPROFILE\.openclaw\skills
git clone https://github.com/Hi-Jiajun/openclaw-backup.git
```

### Linux / Mac

```bash
# 克隆到你的 OpenClaw skills 目录
cd ~/.openclaw/skills
git clone https://github.com/Hi-Jiajun/openclaw-backup.git
```

## 快速开始

### Windows

```powershell
# 首次配置（交互式向导）
powershell -ExecutionPolicy Bypass -File "scripts/setup.ps1"

# 执行备份
powershell -ExecutionPolicy Bypass -File "scripts/backup.ps1"
```

### Linux / Mac

```bash
# 首次配置（交互式向导）
chmod +x scripts/setup.sh
./scripts/setup.sh

# 执行备份
chmod +x scripts/backup.sh
./scripts/backup.sh
```

## 配置文件说明

### setup.ps1 / setup.sh 会生成配置文件

首次运行 setup.ps1 或 setup.sh 会创建配置文件，保存你的配置。

### backup.ps1 / backup.sh 会自动加载配置

脚本会自动读取配置文件，无需手动修改。

## 备份内容

| 目录/文件 | 说明 |
|-----------|------|
| openclaw.json | 主配置文件 |
| agents/ | Agent 配置 |
| credentials/ | 凭证文件（含 API 密钥） |
| cron/ | 定时任务 |
| devices/ | 配对设备 |
| identity/ | 身份配置 |
| skills/ | 全局技能 |

## 注意事项

1. credentials/ 包含敏感信息 - 妥善保管备份
2. 首次使用建议运行交互式配置
3. 建议设置自动备份任务防止数据丢失
