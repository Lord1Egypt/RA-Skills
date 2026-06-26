---
name: parallel-coding
version: 1.0.0
description: 使用 git worktree + 编码智能体实现多任务并行开发。当需要同时处理多个开发任务、避免串行等待、或需要在多个分支间快速切换时触发。支持 Claude Code、Codex 等编码智能体的并行调度。
---

# Git Worktree 并行开发

## 核心理念

**一个仓库，多个工作目录，多个编码智能体同时干活。**

| 方案 | 优点 | 缺点 |
|------|------|------|
| `git stash` + checkout | 简单 | 串行等待，编译缓存丢失 |
| `git worktree` | 真正并行，环境隔离 | 目录多，磁盘占用略大 |

## 快速开始

```bash
# 1. 创建 worktree（基于 main 分支）
git worktree add -b feature-a ../project-feature-a main
git worktree add -b feature-b ../project-feature-b main

# 2. 列出所有 worktree
git worktree list

# 3. 并行派发任务给编码智能体
cd ../project-feature-a && claude --permission-mode bypassPermissions --print '实现用户登录功能'
cd ../project-feature-b && codex '添加数据导出功能'

# 4. 清理 worktree
git worktree remove ../project-feature-a
git worktree prune  # 清理已删除分支的 worktree
```

## 工作流程

### 标准流程

```
1. 接收多个任务 → 规划 → 拆解
2. 为每个任务创建 worktree
3. 并行派发给编码智能体（Claude Code / Codex）
4. 智能体各自开发、测试、提交
5. 创建 PR/MR，等待审核
6. 审核通过后合并
7. 清理 worktree
```

### 命名规范

```bash
# 推荐命名：项目名-功能名
../myapp-feature-auth
../myapp-feature-export
../myapp-hotfix-login-bug
```

## 编码智能体调用

### Claude Code

```bash
# 非交互模式（推荐用于并行任务）
cd /path/to/worktree
claude --permission-mode bypassPermissions --print '任务描述'

# 注意：需要先 source shell 配置加载环境变量
source ~/.zshrc && claude --permission-mode bypassPermissions --print '任务描述'
```

### Codex

```bash
# 需要交互式终端
codex '任务描述'
```

### OpenCode

```bash
# 需要交互式终端
opencode '任务描述'
```

## 最佳实践

### 1. 合并权在用户

智能体只负责开发，**不自己合并代码**：
- 智能体：开发 → 提交 → push → 创建 PR/MR
- 用户：审核代码 → 合并到 main

### 2. 编译缓存保留

大型项目切换分支通常需要重新编译，worktree 各自保留编译缓存：
```
project-main/build/       ← main 的编译产物
project-feature-a/build/  ← feature-a 的编译产物
```

### 3. 及时清理

```bash
# 查看所有 worktree
git worktree list

# 删除指定 worktree
git worktree remove ../project-feature-a

# 清理无效引用（分支已删除但 worktree 目录还在）
git worktree prune
```

### 4. 冲突处理

如果两个 worktree 修改了同一文件：
1. 各自独立开发，各自提交
2. PR 时解决冲突
3. 或者重新规划任务边界

## 常见问题

### Q: worktree 会复制整个仓库吗？

不会。worktree 共享 `.git` 目录，只有工作目录是独立的。磁盘开销主要来自工作文件和编译产物。

### Q: 可以基于已有分支创建 worktree 吗？

```bash
# 基于已有分支
git worktree add ../project-feature existing-branch

# 基于新分支
git worktree add -b new-branch ../project-new main
```

### Q: worktree 之间可以合并吗？

可以，但通常走 PR 流程。直接合并：
```bash
cd ../project-main
git merge feature-a
```

### Q: 忘记删除 worktree 怎么办？

```bash
git worktree list          # 查看所有 worktree
git worktree prune         # 清理已删除目录的引用
```