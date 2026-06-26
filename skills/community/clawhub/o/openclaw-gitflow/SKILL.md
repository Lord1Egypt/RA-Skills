---
name: git-workflow
description: Git workflow assistant. Generates commit messages, PR descriptions, branch management suggestions, and automates common Git operations.
---

# Git Workflow

Git 工作流助手，生成提交信息、PR 描述、分支管理建议，自动化常见 Git 操作。

**Version**: 1.0  
**Features**: 智能提交信息、PR 描述生成、分支策略建议、Git 自动化

---

## Quick Start

### 1. 生成 Commit Message

```bash
# 根据暂存区变更生成提交信息
python3 scripts/main.py suggest-commit

# 自定义类型
python3 scripts/main.py suggest-commit --type feat
```

### 2. 生成 PR 描述

```bash
# 根据分支对比生成 PR 描述
python3 scripts/main.py pr-description --base main --head feature-branch
```

### 3. 分支管理建议

```bash
# 获取分支策略建议
python3 scripts/main.py branch-strategy

# 检查过时分支
python3 scripts/main.py check-branches
```

### 4. 智能提交

```bash
# 自动暂存、生成信息、提交
python3 scripts/main.py smart-commit
```

---

## Commands

| 命令 | 说明 | 示例 |
|------|------|------|
| `suggest-commit` | 生成提交信息 | `suggest-commit` |
| `pr-description` | 生成 PR 描述 | `pr-description --base main` |
| `branch-strategy` | 分支策略 | `branch-strategy` |
| `check-branches` | 检查分支 | `check-branches` |
| `smart-commit` | 智能提交 | `smart-commit` |

---

## Commit Message Generation

### 常规提交

```bash
$ python3 scripts/main.py suggest-commit

📝 Suggested commit message:
feat(auth): add OAuth2 login support

- Implement Google OAuth2 provider
- Add token refresh mechanism
- Update login UI

Files changed:
- src/auth/oauth.py (+45 lines)
- src/ui/login.js (+23 lines)
- tests/test_oauth.py (+67 lines)
```

### Conventional Commits 格式

自动遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>[(scope)]: <description>

[body]

[footer]
```

类型自动检测：
- `feat` - 新功能
- `fix` - Bug 修复
- `docs` - 文档更新
- `style` - 代码格式
- `refactor` - 重构
- `test` - 测试
- `chore` - 构建/工具

---

## PR Description Generation

```bash
$ python3 scripts/main.py pr-description --base main --head feature/api-v2

📝 PR Description
================

## Summary
Implement API v2 with improved performance and new endpoints.

## Changes
- ✨ New endpoint `/api/v2/users`
- ⚡ Optimize database queries
- 📚 Update API documentation

## Testing
- [x] Unit tests added
- [x] Integration tests pass
- [ ] Performance benchmarks

## Breaking Changes
None

## Related Issues
Closes #123
```

---

## Branch Strategy

```bash
$ python3 scripts/main.py branch-strategy

🌿 Branch Strategy
==================

Current branch: feature/payment
Base branch: main

Recommended workflow:
1. Keep feature branch up to date:
   git fetch origin
   git rebase origin/main

2. Squash commits before merge:
   git rebase -i HEAD~3

3. Merge strategy:
   git checkout main
   git merge --no-ff feature/payment

⚠️  Warning: Branch is 5 commits behind main
```

---

## Smart Commit

一键完成提交流程：

```bash
$ python3 scripts/main.py smart-commit

🔍 Checking repository status...
📦 Staging all changes...
📝 Generating commit message...

Suggested: feat(payment): add Stripe integration

Use this message? [Y/n/e(edit)]: y

✅ Committed: feat(payment): add Stripe integration

Next steps:
- git push origin feature/payment
- Create PR: https://github.com/user/repo/compare/main...feature/payment
```

---

## Branch Cleanup

```bash
$ python3 scripts/main.py check-branches

🧹 Branch Cleanup
=================

Stale branches (merged to main):
- feature/old-login (last updated 30 days ago)
- hotfix/temp-fix (last updated 45 days ago)

Active branches:
- feature/new-ui (2 days ago)
- bugfix/auth-error (1 day ago)

Delete stale branches?
[y/N]: y

✅ Deleted 2 stale branches
```

---

## Configuration

`.git-workflow.json`:

```json
{
  "commit_style": "conventional",
  "pr_template": ".github/pull_request_template.md",
  "auto_stage": false,
  "commit_types": {
    "feat": "✨",
    "fix": "🐛",
    "docs": "📚",
    "style": "💎",
    "refactor": "♻️",
    "test": "🧪",
    "chore": "🔧"
  }
}
```

---

## Git Aliases

添加到 `.gitconfig`：

```ini
[alias]
    cm = !python3 /path/to/git-workflow/scripts/main.py suggest-commit
    pr = !python3 /path/to/git-workflow/scripts/main.py pr-description
    smart = !python3 /path/to/git-workflow/scripts/main.py smart-commit
```

使用：
```bash
git cm      # 生成提交信息
git pr      # 生成 PR 描述
git smart   # 智能提交
```

---

## CI/CD Integration

```yaml
# .github/workflows/pr.yml
name: PR Helper
on:
  pull_request:
    types: [opened]

jobs:
  description:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Generate PR Description
        run: |
          DESC=$(python3 skills/git-workflow/scripts/main.py pr-description --base main)
          echo "$DESC" >> $GITHUB_STEP_SUMMARY
```

---

## Examples

### 场景 1：日常开发提交流程

```bash
# 1. 开发完成，查看变更
git diff

# 2. 生成提交信息
python3 main.py suggest-commit

# 3. 提交
git commit -m "feat: add user authentication"

# 4. 推送
git push origin feature/auth
```

### 场景 2：创建 PR

```bash
# 1. 推送到远程
git push origin feature/api-v2

# 2. 生成 PR 描述
python3 main.py pr-description --base main --head feature/api-v2

# 3. 复制输出到 GitHub PR
```

### 场景 3：清理过时分支

```bash
# 检查分支状态
python3 main.py check-branches

# 删除已合并分支
python3 main.py check-branches --delete-merged
```

---

## Files

```
skills/git-workflow/
├── SKILL.md                    # 本文件
└── scripts/
    ├── main.py                 # ⭐ 统一入口
    ├── commit_generator.py     # 提交信息生成
    ├── pr_generator.py         # PR 描述生成
    └── branch_manager.py       # 分支管理
```

---

## Roadmap

- [x] Commit message generation
- [x] PR description generation
- [x] Branch strategy suggestions
- [ ] Git hook integration
- [ ] GitHub CLI integration
