---
name: git-log-tracker
displayName: "Git Log Tracker (Commit Index & Query CLI)"
version: 0.6.0
description: |
  Git post-commit hook + SQLite commit index tool. Automatically records every commit's metadata (hash, author, branch, repo, subject) into a local SQLite database, then provides a CLI to query, list, stats, delete, and update records.
  Trigger: managing git hooks, querying commit history across repos, finding which repo a commit belongs to, viewing commit statistics, recording commits to a local index.
  Use this skill whenever the user mentions commit logging, commit indexing, finding commits across repos, git hook management, or wants to query their commit history in a structured way — even if they don't explicitly name the tool.
---

# Git Log Tracker

- **Author**: [LeeShunEE](https://github.com/LeeShunEE)
- **Organization**: [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)
- **GitHub**: https://github.com/KinemaClawWorkspace/git-log-tracker

## ⚠️ Before First Use | 首次使用必读

**首次使用此 skill 前，必须先读取 [references/ONBOARDING.md](references/ONBOARDING.md) 完成环境配置。**

references/ONBOARDING.md 采用**交互式流程**：
- **Agent 必须先询问用户使用意图**（仅当前 repo / 多个 repo / 全局模式）
- **根据用户选择执行相应步骤**，切勿自动执行全部命令

- **首次配置** → 读取 references/ONBOARDING.md，按 Step 0 询问用户后执行
- **环境不可用**（命令不存在、依赖缺失、连接失败）→ 读取 references/ONBOARDING.md Troubleshooting 排查修复
- **配置完成后** → 直接使用下方 Run Commands

## Overview

Git Log Tracker 在每次 `git commit` 后自动将 commit 元数据写入本地 SQLite 数据库。通过 CLI 可以跨仓库查询、统计、修改和删除 commit 记录。

数据存储在 `~/.commit-logs/index.db`，配置文件在 `~/.commit-logs/config.toml`。

## Run Commands

所有命令通过 `git-log-tracker <subcommand>` 运行。

### 初始化

首次安装后初始化配置和数据库：

```bash
git-log-tracker setup
```

### Hook 管理

安装 hook 到指定 repo（之后每次 commit 自动记录）：

```bash
git-log-tracker install /path/to/repo
git-log-tracker install .                              # 当前 repo
```

检查 hook 状态：

```bash
git-log-tracker status /path/to/repo
git-log-tracker status .
```

移除 hook：

```bash
git-log-tracker uninstall /path/to/repo
```

扫描目录中的 git 仓库：

```bash
git-log-tracker scan /path/to/directory                     # 扫描并列出仓库
git-log-tracker scan /path/to/directory --depth 3           # 控制扫描深度
git-log-tracker scan /path/to/directory --install-missing   # 自动安装缺失 hook 的仓库
git-log-tracker scan /path/to/directory --interactive       # 交互式选择安装
git-log-tracker scan /path/to/directory --exclude "*/temp/*" --exclude "*/.cache/*"  # 排除路径
```

`scan` 输出示例：
```
Scanning D:\modular_dev for git repositories (depth=5)...

Found 15 repositories:
+----------------------------------------------------+--------------+--------------------+
| Repo Path                                          | Hook Status  | Branches           |
+----------------------------------------------------+--------------+--------------------+
| D:\modular_dev\kinema_skills                       | [OK]         | main (3)           |
| D:\modular_dev\other_project                       | [--]         | master (1)         |
| D:\modular_dev\legacy_app                          | [--]         | develop (5)        |
+----------------------------------------------------+--------------+--------------------+

Summary: 1 installed, 2 missing
```

全局模式（新 repo 自动带 hook）：

```bash
git-log-tracker global          # 启用
git-log-tracker global --off    # 关闭
```

### 数据查询

按 hash 查找（支持前缀匹配）：

```bash
git-log-tracker find abc1234
```

`find` 输出示例：
```
commit  abc1234def5678901234567890123456789012
author  Lee <lee@example.com>
date    2025-05-29T14:30:00+08:00
repo    D:/modular_dev/task-tracker
branch  master
subject test(frontend): Phase 4 完成
```

列出最近 commit：

```bash
git-log-tracker list                     # 最近 20 条
git-log-tracker list -n 50               # 最近 50 条
git-log-tracker list --repo task-tracker  # 按仓库名筛选
git-log-tracker list --author lee@example.com  # 按作者筛选
git-log-tracker list --since 2025-01-01   # 按日期筛选
git-log-tracker list --branch main        # 按分支筛选
git-log-tracker list --label work         # 按仓库标签筛选
```

`list` 输出为表格格式：`HASH | DATE | AUTHOR | REPO | SUBJECT`

统计信息：

```bash
git-log-tracker stats
git-log-tracker stats --label work        # 只统计带该标签的仓库
```

### 标签管理

给仓库打**仓库级标签**（label），用于按"组"过滤查询（如 work / personal）。标签是 `repo_path` 的属性，改标签立即对该仓库全部历史 commit 生效。

```bash
git-log-tracker label add . work               # 给当前仓库加 work 标签
git-log-tracker label add /path/to/repo work personal  # 一次加多个标签
git-log-tracker label rm . work                # 移除标签
git-log-tracker label list .                   # 查看某仓库的标签
git-log-tracker label list                     # 列出所有标签映射
```

标签存储在 `~/.commit-logs/labels.json`，结构为 `{ "归一化repo_path": ["label1", ...] }`。

### 数据修改

手动记录某个 repo 的最新 commit：

```bash
git-log-tracker record .           # 当前 repo
git-log-tracker record /path/to/repo
```

删除记录：

```bash
git-log-tracker delete abc1234
```

更新记录字段（可编辑字段：branch, commit_subject, commit_body, repo_path, repo_name）：

```bash
git-log-tracker update abc1234 branch main
```

重置数据目录：

```bash
git-log-tracker reinstall              # 删除数据目录并重新初始化
git-log-tracker reinstall --keep-config  # 只重置数据库，保留配置
```

### 配置

编辑 `~/.commit-logs/config.toml` 管理排除列表：

```toml
[hooks]
exclude = [
    "/tmp/*",
    # "/path/to/specific/repo",
]

[database]
path = "index.db"
```

## Architecture

安装后的系统结构：

```
~/.commit-logs/          # 数据目录（不含代码）
├── config.toml          # 排除列表和数据库路径配置
├── labels.json          # 仓库级标签映射（repo_path -> [labels]）
├── index.db             # SQLite 数据库

.git/hooks/post-commit   # Hook 文件，调用 git-log-tracker hook
```

CLI 工具通过 `uv tool install` 安装到系统，不在 ~/.commit-logs 中存放代码。

## SQLite Schema

```sql
commits(
    id, commit_hash, short_hash, author_name, author_email, author_ts,
    committer_name, committer_email, commit_subject, commit_body,
    branch, repo_path, repo_name, parent_hashes, recorded_at
)
```

索引：`commit_hash`(UNIQUE), `repo_path`, `author_email`, `recorded_at`