---
name: git-ops
description: "Local git operations for project management. Use when: (1) creating branches for new features/issues, (2) committing and pushing code, (3) pulling latest changes, (4) managing branches, (5) viewing git log/diff/status, (6) preparing code for merge requests or pull requests. Triggers on: git, branch, commit, push, pull, merge, checkout, diff, log, 分支, 提交, 推送."
---

# Git Ops Skill

Local git operations for managing project code.

## Branch Naming Convention

For new features/issues, create branches with pattern:
```
feature/issue-{number}-{brief-description}
```

For bug fixes:
```
fix/issue-{number}-{brief-description}
```

## Standard Workflow

### Start new feature from an issue

```bash
cd /path/to/project
git checkout main
git pull origin main
git checkout -b feature/issue-1-add-dark-mode
```

### After coding is done

```bash
git add -A
git commit -m "feat: add dark mode support (closes #1)"
git push -u origin feature/issue-1-add-dark-mode
```

### Create PR/MR after push

- GitHub: use `github` skill → `gh pr create`
- GitLab: use `gitlab-ops` skill → `glab mr create`

## Common Commands

```bash
# Status
git status
git log --oneline -10
git diff
git diff --staged

# Branch management
git branch -a
git checkout main
git checkout -b feature/xxx
git branch -d old-branch

# Sync
git pull origin main
git fetch --all
git rebase main

# Stash
git stash
git stash pop
git stash list
```

## Known Project Paths

| Project | Path | Remote |
|---------|------|--------|
| yeahmobiEverything | /Users/zhujinqi/Documents/javacode/learn/yeahmobiEverything | GitHub (zhulaoqi) |
| ad-pex-ai | TBD | GitLab (ad-pex/ad-pex-ai) |

## Commit Message Convention

Use conventional commits:
- `feat:` new feature
- `fix:` bug fix
- `refactor:` code refactoring
- `style:` UI/style changes
- `docs:` documentation
- `chore:` maintenance

## Notes

- Always pull latest before creating new branches
- Never force push to main/master
- Ask user before any destructive operations (reset --hard, force push)
