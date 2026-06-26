---
name: git
description: 快速处理各种 Git 指令的技能。适用于：git 操作、代码提交、分支管理、合并冲突、版本回退、远程仓库同步、查看提交历史、撤销修改等场景。触发词：git、提交、推送、拉取、分支、合并、rebase、reset、revert、stash、cherry-pick、tag、diff、log、status。
---

# Git 快捷操作技能

## 概述

此技能帮助快速执行各种 Git 操作，包括代码提交、分支管理、远程同步、历史查看和撤销操作等。

## 使用指南

### 提交相关

```bash
# 查看状态
git status

# 添加文件
git add <file>           # 添加指定文件
git add .                # 添加所有更改

# 提交
git commit -m "message"  # 提交并附带消息

# 推送
git push origin <branch>
git push -u origin <branch>  # 首次推送并设置上游分支

# 拉取
git pull origin <branch>
git pull --rebase origin <branch>  # 变基拉取
```

### 分支管理

```bash
# 查看分支
git branch               # 本地分支
git branch -a            # 所有分支（含远程）
git branch -r            # 仅远程分支

# 创建分支
git branch <name>        # 创建新分支
git checkout -b <name>   # 创建并切换
git switch -c <name>     # 新语法：创建并切换

# 切换分支
git checkout <name>
git switch <name>        # 新语法

# 删除分支
git branch -d <name>     # 安全删除（已合并）
git branch -D <name>     # 强制删除

# 合并分支
git merge <branch>       # 合并指定分支到当前
git merge --no-ff <branch>  # 禁用快进合并

# 变基
git rebase <branch>      # 变基到指定分支
git rebase -i HEAD~n     # 交互式变基最近n次提交
```

### 查看历史

```bash
# 查看日志
git log                  # 完整日志
git log --oneline        # 简洁日志
git log --graph          # 图形化显示
git log -n               # 最近n条

# 查看差异
git diff                 # 工作区与暂存区
git diff --staged        # 暂存区与上次提交
git diff <commit1> <commit2>  # 两个提交间

# 查看文件历史
git log --follow -p <file>  # 文件完整历史
git blame <file>         # 每行最后修改信息
```

### 撤销操作

```bash
# 撤销工作区修改
git restore <file>       # 新语法
git checkout -- <file>   # 旧语法

# 撤销暂存
git restore --staged <file>  # 新语法
git reset HEAD <file>    # 旧语法

# 回退提交
git reset --soft HEAD~1  # 保留更改在暂存区
git reset --mixed HEAD~1 # 保留更改在工作区（默认）
git reset --hard HEAD~1  # 完全删除更改

# 创建反向提交
git revert <commit>      # 安全撤销指定提交
```

### 暂存与恢复

```bash
git stash                # 暂存当前更改
git stash list           # 查看暂存列表
git stash pop            # 恢复并删除最新暂存
git stash apply          # 恢复但保留暂存
git stash drop           # 删除最新暂存
```

### 远程仓库

```bash
# 查看远程
git remote -v

# 添加远程
git remote add origin <url>

# 获取更新
git fetch origin

# 删除远程分支引用
git remote prune origin
```

### 标签

```bash
git tag                  # 列出标签
git tag <name>           # 创建轻量标签
git tag -a <name> -m "message"  # 创建附注标签
git push origin <tag>    # 推送标签
git push origin --tags   # 推送所有标签
git tag -d <name>        # 删除本地标签
```

### 其他常用

```bash
# Cherry-pick
git cherry-pick <commit>

# 查看某个提交
git show <commit>

# 清理未跟踪文件
git clean -fd            # 删除未跟踪文件和目录
git clean -fdn           # 预览将删除的文件

# 压缩提交
git rebase -i HEAD~n     # 交互式变基，使用 squash 压缩
```

## 注意事项

1. **永远不要在公共分支上使用 `reset --hard`**
2. **推送前检查分支状态**：`git status`
3. **合并冲突时**：手动编辑冲突文件，然后 `git add` 和 `git commit`
4. **回退前备份**：可使用 `git branch backup-branch` 创建备份分支
5. **避免在 rebase 过程中修改已推送的提交**
