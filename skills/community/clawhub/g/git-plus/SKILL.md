---
name: git-plus
description: "Enhanced Git with advanced workflows, Git hooks, CI/CD integration, monorepo support, Git LFS, and Git internals deep dive."
metadata:
  author: opencode
  version: 2.0
  tags: git, version-control, hooks, ci-cd, monorepo
  compatibility: opencode
  license: MIT
---

# Git Plus

Enhanced Git with advanced workflows, hooks, and CI/CD integration.

## Features

- **Advanced Workflows**: Gitflow, trunk-based, GitHub Flow
- **Git Hooks**: Pre-commit, pre-push, commit-msg hooks
- **CI/CD Integration**: GitHub Actions, GitLab CI pipelines
- **Monorepo Support**: Worktrees, sparse checkout, submodules
- **Git Internals**: Objects, refs, packfiles

## Quick Reference

| Task | Command |
|------|---------|
| Status | `git status -sb` |
| Log | `git log --oneline -10 --graph` |
| Diff | `git diff --stat HEAD~5` |
| Stash | `git stash push -m "description"` |
| Rebase | `git rebase -i HEAD~5` |

## Advanced Workflows

### Gitflow

```bash
# Feature
git checkout -b feature/new-feature develop
git commit -m "feat: add new feature"
git checkout develop
git merge --no-ff feature/new-feature

# Release
git checkout -b release/1.0.0 develop
git commit -m "chore: bump version"
git checkout main
git merge --no-ff release/1.0.0
git tag -a v1.0.0 -m "Release 1.0.0"

# Hotfix
git checkout -b hotfix/urgent-fix main
git commit -m "fix: urgent issue"
git checkout main
git merge --no-ff hotfix/urgent-fix
```

### Trunk-Based Development

```bash
# Short-lived feature branch
git checkout -b feature/short-lived
git commit -m "feat: quick change"
git push origin feature/short-lived
# Create PR, merge to main

# Direct commit (for small changes)
git checkout main
git pull origin main
git commit -m "feat: small change"
git push origin main
```

### GitHub Flow

```bash
# Create branch
git checkout -b feature/my-feature

# Make changes
git add .
git commit -m "feat: add feature"

# Push and create PR
git push origin feature/my-feature
# Create PR via GitHub UI

# After review, merge via GitHub
```

## Git Hooks

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run linter
npm run lint

# Run tests
npm test

# Check for secrets
if grep -r "password\|secret\|api_key" --include="*.js" --include="*.ts" .; then
  echo "Error: Potential secrets found"
  exit 1
fi
```

### Commit-msg Hook

```bash
#!/bin/bash
# .git/hooks/commit-msg

# Validate conventional commit format
commit_msg=$(cat "$1")
pattern="^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,72}"

if ! echo "$commit_msg" | grep -qE "$pattern"; then
  echo "Error: Invalid commit message format"
  echo "Format: type(scope): description"
  echo "Example: feat(auth): add login page"
  exit 1
fi
```

### Pre-push Hook

```bash
#!/bin/bash
# .git/hooks/pre-push

# Run tests before push
npm test

# Check for force push
for ref in "$@"; do
  if echo "$ref" | grep -qE "refs/heads/(main|master|develop)$"; then
    read -p "Force push to protected branch? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      exit 1
    fi
  fi
done
```

### Install Hooks

```bash
# Copy hooks to .git/hooks
cp hooks/* .git/hooks/

# Or use Husky (Node.js)
npx husky install
npx husky add .git/hooks/pre-commit "npm run lint"
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
      - run: npm run lint

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run build
      - run: npm run deploy
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - npm ci
    - npm test
    - npm run lint

build:
  stage: build
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/

deploy:
  stage: deploy
  script:
    - npm run deploy
  only:
    - main
```

## Monorepo Support

### Git Worktrees

```bash
# Add worktree for feature
git worktree add ../feature-branch feature/branch

# List worktrees
git worktree list

# Remove worktree
git worktree remove ../feature-branch
```

### Sparse Checkout

```bash
# Enable sparse checkout
git sparse-checkout init --cone

# Set directories
git sparse-checkout set packages/frontend packages/shared

# Update
git sparse-checkout disable
```

### Submodules

```bash
# Add submodule
git submodule add https://github.com/user/repo.git libs/repo

# Update submodules
git submodule update --init --recursive

# Clone with submodules
git clone --recurse-submodules https://github.com/user/repo.git
```

## Git Internals

### Objects

```bash
# View object type and size
git cat-file -t <sha>
git cat-file -s <sha>

# View object content
git cat-file -p <sha>

# List objects
git rev-list --objects --all
```

### Refs

```bash
# View refs
git show-ref

# View reflog
git reflog

# Find branches containing commit
git branch --contains <sha>
```

### Packfiles

```bash
# Create packfile
git gc

# Verify packfile
git verify-pack -v .git/objects/pack/*.idx

# View packfile statistics
git count-objects -v
```

## Advanced Commands

### Interactive Rebase

```bash
# Rebase last 5 commits
git rebase -i HEAD~5

# Commands:
# p, pick = keep commit
# r, reword = keep commit, edit message
# e, edit = keep commit, amend
# s, squash = meld into previous commit
# f, fixup = like squash, discard this commit's message
# d, drop = remove commit
```

### Cherry-Pick

```bash
# Cherry-pick single commit
git cherry-pick <sha>

# Cherry-pick range
git cherry-pick <start-sha>..<end-sha>

# Cherry-pick without committing
git cherry-pick --no-commit <sha>
```

### Bisect

```bash
# Start bisect
git bisect start
git bisect bad
git bisect good v1.0.0

# Git checks out middle commit
# Test it, then mark as good or bad
git bisect good  # or git bisect bad

# Reset
git bisect reset
```

## Best Practices

1. **Write meaningful commits** - Conventional commit format
2. **Keep commits small** - One logical change per commit
3. **Rebase before push** - Clean history
4. **Use feature branches** - Never commit directly to main
5. **Tag releases** - Semantic versioning
6. **Use Git LFS** - For large files
7. **Protect branches** - Require PR reviews
8. **Clean up regularly** - Prune stale branches
