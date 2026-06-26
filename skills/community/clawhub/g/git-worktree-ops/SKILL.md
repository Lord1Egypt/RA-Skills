---
name: git-worktree-ops
description: 并行开发环境管理技能
domain: engineering
homepage: https://github.com/soponcd/timeflow-skills/tree/main/teams/skills/git-worktree-ops
metadata:
  clawdbot:
    emoji: 🌲
---

# Git Worktree Ops

本技能用于管理 Antigravity 的并行开发环境。通过 `git worktree` 创建物理隔离的代码工作区。

## 核心脚本
使用 `tools/git_worktree_manager.sh` 进行所有操作。

### 常用命令
- 创建: `./tools/git_worktree_manager.sh create <agent-name>`
- 销毁: `./tools/git_worktree_manager.sh remove <agent-name>`
- 列表: `./tools/git_worktree_manager.sh list`
