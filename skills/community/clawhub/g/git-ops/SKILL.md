---
name: "git-ops"
description: "Git日常操作：status/pull/push/branch/log/commit/merge，基础工作流，命令行安全操作指导"
user-invocable: true
metadata:
  openclaw:
    emoji: "📦"
    tags: ["git", "version-control"]
---

# Git Ops v2.0

## 安全原则
1. `git status` 先检查再操作
2. 未保存改动先 stash/commit
3. pull前确保干净
4. 不强制回退已推送提交

## 速查

### 状态
`git status` / `git log --oneline -20` / `git diff` / `git branch -a`

### 暂存提交
`git add <file>` / `git add -A` / `git commit -m "msg"` / `git commit --amend`

### 分支
`git branch <name>` / `git checkout -b <name>` / `git merge <branch>` / `git branch -d`

### 同步
`git pull --rebase` / `git push` / `git push -u origin <branch>` / `git fetch`

### 暂存
`git stash` / `git stash pop` / `git stash list`

### 撤销
`git reset <file>` / `git checkout -- <file>` / `git revert <commit>`

### 标签
`git tag v1.0.0` / `git tag -a v1.0.0 -m "msg"` / `git push origin v1.0.0`

## 最佳实践
分支: feature/fix/chore | Commit: Conventional Commits | 经常pull | 一个大功能=一个分支+多个小commit
