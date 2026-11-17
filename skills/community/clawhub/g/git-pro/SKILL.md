---
name: "git-pro"
description: "Git高级操作：smart-commit/rebase/bisect/worktree/reflog/conflict-resolution/submodule/PR流程"
user-invocable: true
metadata:
  openclaw:
    emoji: "🔧"
    tags: ["git", "advanced", "rebase", "worktree"]
---

# Git Pro v2.0

## 智能 Commit
分析暂存区→生成 Conventional Commits(feat/fix/refactor/docs/chore/test/style/perf/ci/build)

## Rebase
`git rebase -i HEAD~3` → pick/reword/squash/fixup/drop
`git pull --rebase`(推荐)

## Bisect
`git bisect start` → `bad`/`good` → 二分测试 → `git bisect reset`

## Worktree
`git worktree add ../hotfix hotfix`(同时多分支开发)

## Reflog
`git reflog` → 恢复误删分支/文件(后悔药)

## Cherry-pick
`git cherry-pick <hash>` (单个/范围)

## 子树子模块
submodule add/update / subtree add/pull/push

## PR流程
创建分支→rebase main→推送→review→amend→`--force-with-lease`

## 安全
✅ `--force-with-lease` / ✅ 只rebase自己的分支 / ✅ 不amend已推送公共提交
