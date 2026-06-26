---
name: git-backup
version: 1.0.0
description: Backup OpenClaw workspace to Git repository (Gitee/GitHub/GitLab). Use when: (1) setting up backup for the first time, (2) manually triggering a backup, (3) configuring auto-backup, (4) user mentions "备份", "backup", "git", "gitee", "github", or asks about preserving workspace data.
---

# Git Backup

Backup OpenClaw agent workspace to Git repository for data safety and migration capability.

**Author**: 徐琛 (nicolasxu93@163.com)  
**License**: Apache 2.0

## ⚠️ 使用前必读

**使用此技能前，你需要准备：**

| 信息 | 如何获取 |
|------|----------|
| **Git 平台 Token** | Gitee: https://gitee.com/profile/personal_access_tokens<br>GitHub: https://github.com/settings/tokens<br>GitLab: https://gitlab.com/-/profile/personal_access_tokens |
| **Git 用户名** | 你的 Git 平台用户名 |
| **Agent 名称** | 你的 agent 标识符（用于仓库命名） |

**Token 权限要求：**
- `projects` / `repo` - 创建和管理仓库
- `user_info` / `read:user` - 读取用户信息

## Quick Start

### 1. 创建仓库

```bash
# Gitee
curl -X POST "https://gitee.com/api/v5/user/repos" \
  -H "Content-Type: application/json" \
  -d '{
    "access_token": "YOUR_TOKEN",
    "name": "openclaw-agent-YOUR_AGENT_NAME",
    "description": "OpenClaw Agent Backup",
    "private": true,
    "auto_init": true
  }'

# GitHub (使用 gh cli)
gh repo create openclaw-agent-YOUR_AGENT_NAME --private --description "OpenClaw Agent Backup"
```

### 2. 执行备份

```bash
export GITEE_TOKEN="your_token_here"
export GITEE_REPO="https://gitee.com/YOUR_USERNAME/openclaw-agent-YOUR_AGENT_NAME.git"
export AGENT_NAME="your_agent_name"

./scripts/backup-to-gitee.sh "Backup message"
```

### 3. 配置自动备份（可选）

在你的 `HEARTBEAT.md` 中添加：

```markdown
### 文件变更检测与备份
- 检查核心文件变更时自动备份
- 脚本: /path/to/git-backup/scripts/watch-and-backup.sh
```

## 备份内容

| 类型 | 文件 |
|------|------|
| 核心文档 | `AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, `MEMORY.md`, `TOOLS.md`, `HEARTBEAT.md` |
| 记忆 | `memory/` 目录 |
| 技能 | `skills/` 目录 |

**不备份**: 数据库、任务脚本、临时文件、`.env`、密钥等

## 脚本说明

| 脚本 | 用途 |
|------|------|
| `setup-gitee.sh` | 初始化配置（创建仓库、保存配置） |
| `backup-to-gitee.sh` | 执行备份 |
| `create-repo.sh` | 快速创建仓库工具 |
| `watch-and-backup.sh` | 文件变更监控（用于心跳检测） |

## 环境变量

| 变量 | 必需 | 说明 |
|------|------|------|
| `GITEE_TOKEN` | 是 | Git 平台的 Personal Access Token |
| `GITEE_REPO` | 是 | 仓库 URL |
| `AGENT_NAME` | 是 | Agent 标识符 |
| `WORKSPACE_DIR` | 否 | 工作区路径，默认 `~/.openclaw/workspace` |

## 安全提示

1. **不要将 Token 提交到公开仓库**
2. 使用环境变量或配置文件存储敏感信息
3. 定期轮换 Token
4. 使用私有仓库备份敏感数据

## 支持的平台

- ✅ Gitee（默认）
- ✅ GitHub（修改 API 端点即可）
- ✅ GitLab（修改 API 端点即可）
- ✅ 自建 Git 服务器