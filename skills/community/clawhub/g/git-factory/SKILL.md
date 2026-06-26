# Git Factory — Worktree Isolation for Moths

> Each moth gets its own branch, its own workspace, its own PR. No conflicts. No merge hell.

## When to Use

- **Multi-moth coding tasks** — parallel feature work on the same repo
- **Open-source PRs** — isolated branch per contribution
- **Skill packaging** — each skill gets its own worktree for clean commits
- **Any moth that writes code** — default to worktree isolation

## Quick Reference

### Provision a worktree for a moth
```powershell
# From the repo root
.\skills\git-factory\scripts\new-worktree.ps1 -RepoPath . -TaskSlug "fix-login-bug"
# Returns: C:\Users\spaz\clawd\.worktrees\fix-login-bug
```

### Finish and submit PR
```powershell
.\skills\git-factory\scripts\finish-worktree.ps1 `
  -WorktreePath ".worktrees\fix-login-bug" `
  -CommitMessage "moth(fix-login-bug): fix auth redirect loop" `
  -CreatePR -PRTitle "Fix login redirect bug" `
  -PRBody "Fixes the auth redirect loop on expired sessions"
```

### List active worktrees
```powershell
.\skills\git-factory\scripts\list-worktrees.ps1 -RepoPath .
```

### Clean up stale worktrees (>7 days)
```powershell
.\skills\git-factory\scripts\cleanup-stale.ps1 -RepoPath . -MaxAgeDays 7
```

## Moth Dispatch Integration

When spawning a coding moth, include the worktree in the task prompt:

```
Your working directory is: C:\Users\spaz\clawd\.worktrees\<task-slug>
You are on branch: moth/<task-slug>
Base branch: master

Work ONLY in this directory. When finished:
1. Stage and commit your changes
2. Push your branch: git push -u origin moth/<task-slug>
3. Report what you built and any issues

Do NOT modify files outside your worktree.
```

## Conventions

| Item | Convention |
|------|-----------|
| Worktree location | `<repo>/.worktrees/<task-slug>` |
| Branch naming | `moth/<task-slug>` |
| Commit prefix | `moth(<task-slug>): <description>` |
| PR mode | Draft by default |
| Stale threshold | 7 days (configurable) |
| `.worktrees/` | Added to `.gitignore` automatically |

## How It Works

1. `new-worktree.ps1` creates a branch `moth/<slug>` and a worktree at `.worktrees/<slug>`
2. Moth works in the isolated directory — full git repo, own branch, no conflicts
3. `finish-worktree.ps1` commits, pushes, optionally creates a draft PR, then removes the worktree
4. `cleanup-stale.ps1` runs periodically to remove abandoned worktrees

## Limitations

- Worktrees share the same `.git` directory — large repos may have lock contention on heavy git ops
- Can't have two worktrees on the same branch
- Windows file locking can prevent cleanup if processes have files open
