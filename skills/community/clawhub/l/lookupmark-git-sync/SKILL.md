---
name: git-sync
dependencies:
  - git CLI (https://git-scm.com)
description: >
  Manage whitelisted git repositories from chat. Status, log, diff, pull, push
  with security controls — only approved repos, write commands need confirmation.
  Repo list configurable via ~/.config/git-sync/repos.json (overrides defaults).
  Triggers on "git status", "repo status", "push thesis", "pull polito",
  "check repo", "uncommitted changes", "commit recenti".
  NOT for: arbitrary git repos, destructive operations (clean, reset --hard).
---

# Git Sync

Secure git repository management for whitelisted repos.

## Usage

```bash
# Status of all repos
python3 scripts/git_ctrl.py all

# Status of specific repo
python3 scripts/git_ctrl.py status thesis
python3 scripts/git_ctrl.py status polito

# Recent commits
python3 scripts/git_ctrl.py log thesis -n 20

# Unstaged changes
python3 scripts/git_ctrl.py diff thesis

# Branches
python3 scripts/git_ctrl.py branch thesis

# Fetch (read-only, safe)
python3 scripts/git_ctrl.py fetch thesis

# Pull (requires confirmation)
python3 scripts/git_ctrl.py pull thesis --confirm

# Push (requires confirmation)
python3 scripts/git_ctrl.py push thesis --confirm
```

## Allowed Repos

| Name | Path |
|------|------|
| `thesis` | `~/Documenti/github/thesis` |
| `polito` | `~/Documenti/github/polito` |

## Security

- **Whitelist**: Only `thesis` and `polito` repos are accessible
- **Read-only by default**: `status`, `log`, `diff`, `branch`, `fetch` run freely
- **Write requires `--confirm`**: `pull`, `push`, `merge`, `checkout` need explicit confirmation
- **Blocked commands**: `clean`, `reset --hard`, `push --force` are never allowed
- **No secrets**: Output does not expose git credentials or tokens
