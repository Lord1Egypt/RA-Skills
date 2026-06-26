---
name: laomo-github
slug: laomo-github
description: "老默 GitHub 助手 - 多账户管理、PR 一键推送/清理、代码审查、通知推送。v2.0 完整功能。"
---

# laomo-github - 老默 GitHub 助手 v2.0

## 📖 概述

GitHub 技能是一套完整的 GitHub 自动化工具集，支持多账户管理、PR 操作、代码审查、通知推送等功能。

## 🔧 安装

GitHub 技能已包含 OpenClaw 核心技能。如果需要更新：

```bash
clawhub skill update github
```

## 📂 结构

```
skills/github/
├── github-accounts.sh    # 多账户管理
├── github-pr-push.sh     # PR 推送工具
├── github-pr-cleanup.sh  # PR 清理工具
├── github-review.sh      # 代码审查工具
├── github-notify.sh      # 通知推送工具
├── SKILL.md             # 技能文档
└── _meta.json           # 元数据
```

## 🔍 功能

### 1️⃣ 多账户管理 (`github-accounts.sh`)

管理多个 GitHub 账户，支持切换、验证和配置。

**命令**:
- `list` - 列出所有账户
- `add` - 添加新账户
- `switch` - 切换账户
- `remove` - 删除账户
- `validate` - 验证账户状态
- `current` - 显示当前账户

**用法**:
```bash
# 添加新账户
github-accounts.sh add personal

# 切换账户
github-accounts.sh switch work

# 验证所有账户
github-accounts.sh validate

# 显示当前账户
github-accounts.sh current
```

### 2️⃣ PR 推送工具 (`github-pr-push.sh`)

创建、推送和管理 Pull Requests。

**命令**:
- `create` - 创建新的 PR
- `push` - 推送分支到远程
- `update` - 更新现有 PR
- `merge` - 合并 PR

**选项**:
- `-m, --message` - 自定义 PR 描述
- `-i, --issue` - 关联的 Issue 编号
- `-t, --title` - 自定义 PR 标题
- `-l, --labels` - 添加标签
- `-r, --reviewers` - 添加审查人
- `-d, --draft` - 创建草稿 PR
- `-f, --force` - 强制推送

**用法**:
```bash
# 创建新的 PR
github-pr-push.sh create feature/new-feature

# 创建并关联 Issue
github-pr-push.sh create -m "描述内容" -i 123,456

# 推送分支
github-pr-push.sh push main

# 合并 PR
github-pr-push.sh merge 123
```

### 3️⃣ PR 清理工具 (`github-pr-cleanup.sh`)

清理已合并的 PR、删除陈旧分支、处理冲突。

**命令**:
- `merged` - 清理已合并的 PR 分支
- `old` - 删除过期的临时分支
- `conflicts` - 处理冲突的 PR
- `stale` - 标记陈旧 PR

**选项**:
- `-r, --repo` - GitHub 仓库 (owner/repo)
- `-d, --days` - 过期天数（默认：30）
- `-l, --limit` - 获取 PR 数量限制
- `-y, --yes` - 自动确认所有操作
- `-n, --dry-run` - 仅显示将要执行的操作

**用法**:
```bash
# 清理已合并的 PR
github-pr-cleanup.sh merged

# 删除过期的分支
github-pr-cleanup.sh old --days 14

# 处理冲突的 PR
github-pr-cleanup.sh conflicts

# 标记陈旧 PR
github-pr-cleanup.sh stale
```

### 4️⃣ 代码审查工具 (`github-review.sh`)

下载 PR 代码、进行本地审查、添加评论。

**命令**:
- `download` - 下载 PR 代码
- `review` - 审查 PR
- `comment` - 添加审查评论
- `approve` - 批准 PR
- `decline` - 驳回 PR

**选项**:
- `-r, --repo` - GitHub 仓库
- `-o, --output` - 下载目录
- `-l, --lines` - 审查行数限制
- `-f, --file` - 审查特定文件
- `-v, --verbose` - 显示详细信息

**审查类型**:
- `-s, --style` - 代码风格审查
- `-b, --bug` - Bug 修复审查
- `-p, --performance` - 性能审查
- `-a, --security` - 安全审查
- `-c, --complexity` - 复杂度审查

**用法**:
```bash
# 下载 PR 代码
github-review.sh download 123

# 审查 PR
github-review.sh review 123 --style --bug

# 添加评论
github-review.sh comment 123 -m "LGTM!"

# 批准 PR
github-review.sh approve 123

# 驳回 PR
github-review.sh decline 123 -m "需要修改"
```

### 5️⃣ 通知推送工具 (`github-notify.sh`)

推送 GitHub 事件到各种平台。

**目标平台**:
- `discord` - 推送到 Discord
- `dingtalk` - 推送到钉钉
- `telegram` - 推送到 Telegram
- `slack` - 推送到 Slack
- `all` - 推送到所有平台

**选项**:
- `-t, --type` - 事件类型 (issue, pr, release, commit, workflow)
- `-m, --message` - 自定义消息内容
- `-s, --status` - 事件状态
- `-u, --url` - 相关 URL
- `-a, --author` - 作者
- `-l, --label` - 标签
- `-r, --repo` - GitHub 仓库
- `-n, --number` - 问题/PR 编号
- `-T, --title` - 标题
- `-d, --desc` - 描述
- `--dry-run` - 仅显示消息内容

**用法**:
```bash
# 推送到 Discord
github-notify.sh discord --type pr --status open

# 推送到钉钉
github-notify.sh dingtalk --type issue --number 123

# 推送到所有平台
github-notify.sh all --type commit --title "New release"

# 预览消息
github-notify.sh telegram --message "测试消息" --dry-run
```

## ⚙️ 配置

### GitHub CLI

确保已安装并配置 `gh`：

```bash
# 安装 gh CLI
brew install gh

# 认证
gh auth login
```

### Webhook URL (可选)

如需使用通知推送功能，配置 Webhook URL：

```bash
# Discord
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."

# 钉钉
export DINGTALK_WEBHOOK_URL="https://oapi.dingtalk.com/robot/send?access_token=..."

# Telegram
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_CHAT_ID="..."

# Slack
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

## 🛠️ 前提条件

1. **GitHub CLI**：`brew install gh`
2. **jq**：`brew install jq` (用于通知推送)
3. **Git**：已配置远程仓库
4. **认证**：`gh auth login`

## 📝 使用示例

### 完整的 PR 工作流

```bash
# 1. 创建功能分支
git checkout -b feature/my-feature

# 2. 提交代码
git commit -m "Add new feature"
git push origin feature/my-feature

# 3. 创建 PR
github-pr-push.sh create feature/my-feature --issue 123

# 4. 下载代码审查
github-review.sh download 123
cd ~/github-pr-download/pr-123
# ... 进行代码审查 ...

# 5. 批准 PR
github-review.sh approve 123

# 6. 合并 PR
github-pr-push.sh merge 123

# 7. 清理已合并的分支
github-pr-cleanup.sh merged

# 8. 发送通知
github-notify.sh all --type pr --number 123 --status merged
```

### 多账户协作

```bash
# 列出所有账户
github-accounts.sh list

# 添加工作账户
github-accounts.sh add work

# 添加个人账户
github-accounts.sh add personal

# 切换到工作账户
github-accounts.sh switch work

# 切换到个人账户
github-accounts.sh switch personal
```

## 🐛 故障排除

### 1. `gh CLI 未安装`

```bash
brew install gh
gh auth login
```

### 2. `jq 未安装`

```bash
brew install jq
```

### 3. `远程仓库未配置`

```bash
git remote add origin https://github.com/USER/REPO.git
```

### 4. `权限问题`

```bash
# 验证认证状态
gh auth status

# 重新认证
gh auth login
```

## 📚 相关技能

- `laomo-github` - 基础 GitHub 操作
- `clawhub` - 技能管理

## 📄 许可证

MIT License

---

*版本：v2.0 (2026-03-15)*  
*维护者：老默科技*  
*频道：Discord*
