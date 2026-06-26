---
name: git-worktree
version: 1.0.0
description: Git Worktree 多需求并行开发助手。在当前 worktree 目录下独立开发、修改、提交代码，不跨目录操作。基于目录命名规范自动识别仓库归属（如 main-repo-feature-a → main-repo 仓库）。遵循最小改动原则，从需求分析到 commit 交付全流程负责。触发场景：用户在 worktree 目录下发起开发任务、提到 worktree、提到多需求并行开发。
author: weidongkl
license: MIT
repository: https://github.com/weidongkl/openclaw-workspace-orchestrator
tags:
  - git
  - worktree
  - parallel-development
  - code-management
---

# git-worktree - Git Worktree 多需求并行开发

---

## 🏗️ 目录命名规范

```
/workspace/main-repo                ← 主仓库（main 分支）
/workspace/main-repo-feature-a      ← main-repo 的需求 A
/workspace/main-repo-bugfix-c       ← main-repo 的修复 C
/workspace/other-repo-feature-d     ← other-repo 的需求 D
```

规则：**前缀 = 仓库名**，**后缀 = 需求标识**。

---

## 📋 执行流程

### 1. 识别仓库与需求

从目录名解析：`main-repo-feature-a` → 仓库 `main-repo`，需求 `feature-a`

> 目录名不规范时，通过 `git remote -v` 确认归属。

### 2. 确认工作区状态

```bash
git branch
git status
git log -5 --oneline
```

⚠️ 脏工作区先提醒，不覆盖未提交内容。

### 3. 理解需求上下文

优先读取：`TASK.md` / `README.md` / `ARCH.md` / 构建文件（go.mod、pom.xml 等）。

### 4. 开发

- 最小改动，复用现有代码
- 保持风格一致，不做无关重构
- 只改当前需求涉及的代码

### 5. 完成输出

- 修改文件清单 + 摘要
- 设计理由 + 风险点
- 测试建议 + commit message 建议

---

## ⚠️ 规则

| 允许 ✅ | 禁止 ❌ |
|---------|---------|
| 当前目录开发当前需求 | 切换其他 worktree 目录 |
| 当前分支提交代码 | 修改其他需求代码 |
| 分析当前目录代码 | 操作其他仓库/分支 |
| 从目录名解析归属 | `git reset --hard` / `clean -fd`（除非要求） |

---

## 🔄 新任务初始化

1. 解析目录名 → 确认仓库和需求
2. 查看 git 状态
3. 输出执行计划
4. 等待确认后开始

---

**最后更新**: 2026-04-20
