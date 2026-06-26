---
name: git-manager
description: Execute common Git operations: status, commit, push, pull, branch management, PR creation. Use when user mentions Git, repository, commit, push, pull, branch, merge, or code versioning. Provides safe, auditable operations with dry-run support.
---

# Git Manager Skill

This skill safely executes common Git commands. It wraps `git` CLI with additional safety checks and structured output.

## Capabilities

- `status` - Show working tree status
- `commit` - Stage changes and commit (with message)
- `push` - Push to remote
- `pull` - Pull from remote (rebase or merge)
- `branch` - Create, list, delete branches
- `checkout` - Switch branches
- `merge` - Merge branches
- `stash` - Stash/apply changes
- `log` - Show commit history
- `diff` - Show changes

## Safety Features

- **No force push** by default (`--force` must be explicit)
- **Protected branches**: Cannot delete or commit directly to `main`/`master`/`production`
- **Dry-run mode**: Preview operations before execution
- **Auto-commit message quality check** (LLM can improve messages)
- **All operations logged** to `~/.openclaw/logs/git-manager.log`

## When to Use

User says:
- "查看Git状态"
- "提交代码"
- "推送到远程仓库"
- "拉取最新代码"
- "创建新分支"
- "合并分支"
- "查看提交历史"

## Invocation

```bash
# Status
git-manager --action status --repo /path/to/repo

# Commit all changes
git-manager --action commit --repo /path/to/repo --message "feat: add user auth"

# Commit specific files
git-manager --action commit --repo /path/to/repo --files [file1,file2] --message "fix: bug in payment"

# Push
git-manager --action push --repo /path/to/repo --branch feature-xyz

# Pull
git-manager --action pull --repo /path/to/repo --branch main

# Create branch
git-manager --action branch --repo /path/to/repo --create new-branch --from main

# Checkout
git-manager --action checkout --repo /path/to/repo --branch feature-xyz

# Diff
git-manager --action diff --repo /path/to/repo --files [file1]
```

## Output Format

JSON with fields:
- `success`: boolean
- `output`: string (raw git output)
- `error`: string (if failed)
- `changed_files`: array (for commit)
- `commit_sha`: string (after commit)
- `branch`: current branch

Example:
```json
{
  "success": true,
  "action": "commit",
  "commit_sha": "abc123def",
  "changed_files": ["src/auth.py", "tests/test_auth.py"],
  "output": "[main abc123] feat: add user auth\n 2 files changed, 45 insertions(+)"
}
```

## Configuration via Environment

- `GIT_MANAGER_LOG`: path to activity log (default `~/.openclaw/logs/git-manager.log`)
- `GIT_MANAGER_DRY_RUN`: set "1" to default to dry-run
- `GIT_MANAGER_PROTECTED_BRANCHES`: comma-separated list (default `main,master,production`)

## Integration with OpenClaw

When used from a developer role session:
- Automatically respects the session's `cwd` as the repo if `--repo` not provided
- Can chain operations: `status` -> `commit` -> `push` in one go
- Suggest commit messages based on `git diff` (if `--message` omitted)

## Examples in OpenClaw Sessions

```python
# Developer session
sessions_spawn(
  task="提交刚才修改的登录页面样式",
  config="configs/developer.yaml",
  attachments=[]
)
# The skill will: git add . && git commit -m "style: improve login page" && git push
```

## Limitations

- Does not handle merge conflicts automatically (requires human)
- No rebase interactive (complex history edits)
- Assumes standard Git flow (no custom hooks)
- SSH keys must be pre-configured for push/pull

## Troubleshooting

| Issue | Check |
|-------|-------|
| Permission denied (publickey) | SSH agent running? `ssh-add -l` |
| Not a git repository | `--repo` path correct? |
| Branch protected | Cannot commit to main; create feature branch first |
| Merge conflict | Resolve manually; skill only detects conflict |

## Future Enhancements

- PR creation via GitHub CLI (`gh pr create`)
- Auto-version bump based on commit messages (semantic-release)
- Branch cleanup (delete merged branches)