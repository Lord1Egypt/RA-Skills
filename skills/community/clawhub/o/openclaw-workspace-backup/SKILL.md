---
name: workspace-backup
description: 将工作空间 git 仓库备份到 GitHub 各分支。通过 .env 配置目录列表，每天 03:00 自动执行。当用户说"workspace-backup"、"备份工作空间"、"工作空间备份"时触发。
metadata: {"openclaw":{"emoji":"💾","requires":{"bins":["git"]},"install":"pip install -e {baseDir}"}}
---

# Workspace Backup

将多个本地 git 工作空间自动备份到 GitHub，每个目录对应一个同名远程分支。

## 使用

```bash
workspace                    # 备份所有工作空间
workspace --backup --force   # 强制推送（解决 non-fast-forward 错误）
workspace --status           # 查看各工作空间状态及最近备份日志
```

每天 03:00 由 OpenClaw cron 自动执行。

## 配置

在 `workspace_backup/.env`（或 `~/.config/workspace/.env`）中配置备份目录：

```dotenv
WORKSPACE_main=/home/ubuntu/.openclaw/workspace
WORKSPACE_formulas=/home/ubuntu/.openclaw/workspace-formulas
```

`WORKSPACE_<id>` 的 `<id>` 即为目标 GitHub 分支名。用户级 `.env` 优先于包级 `.env`。
复制 `workspace_backup/.env.example` 为 `.env` 后修改路径即可。

## 前提条件

- SSH Key 已配置，可免密 `git push`
- 各工作空间目录已初始化为 git 仓库并设置远程
