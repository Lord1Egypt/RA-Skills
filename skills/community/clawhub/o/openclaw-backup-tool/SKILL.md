---
name: openclaw-backup
description: OpenClaw 备份还原工具。每次安装调试功能前自动备份，支持终端一键还原和重启。让技术小白也能放心折腾。
metadata: {"clawdbot":{"emoji":"🛡️"}}
---

# OpenClaw 备份还原工具

保护你的 OpenClaw 配置，防止折腾坏掉没退路。

## 功能

1. **自动备份** - 每次安装/调试功能前自动备份
2. **一键还原** - 终端输入命令选择时间节点恢复
3. **重启网关** - 一条命令重启 OpenClaw Gateway

## 使用方法

### 备份脚本

```bash
bash ~/.openclaw/workspace/skills/openclaw-backup/scripts/backup.sh
```

或通过 alias（需添加到 ~/.zshrc）：
```bash
alias ocl-backup="bash ~/.openclaw/workspace/skills/openclaw-backup/scripts/backup.sh"
```

### 还原脚本

```bash
bash ~/.openclaw/workspace/skills/openclaw-backup/scripts/restore.sh
```

会列出所有可用备份，选择后确认还原。

### 重启 Gateway

```bash
bash ~/.openclaw/workspace/skills/openclaw-backup/scripts/restart.sh
```

或通过 alias：
```bash
alias ocl-restart="bash ~/.openclaw/workspace/skills/openclaw-backup/scripts/restart.sh"
```

## 备份内容

- IDENTITY.md
- USER.md  
- MEMORY.md
- SOUL.md
- TOOLS.md
- openclaw.json
- memory/ 目录

## 添加 Alias（推荐）

在 ~/.zshrc 中添加：
```bash
alias ocl-backup="bash ~/.openclaw/workspace/skills/openclaw-backup/scripts/backup.sh"
alias ocl-restore="bash ~/.openclaw/workspace/skills/openclaw-backup/scripts/restore.sh"
alias ocl-restart="bash ~/.openclaw/workspace/skills/openclaw-backup/scripts/restart.sh"
```

然后执行 `source ~/.zshrc` 生效。

## 规则

**重要**：当用户让你安装、调试、配置任何 OpenClaw 功能之前，必须先运行备份脚本！
