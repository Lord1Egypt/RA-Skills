---
name: git-repo
metadata:
  author: es6kr
  version: "0.1.2"
depends-on:
  - commit-tidy
description: |
  Git repository and SourceGit integration. Topics — clone (ghq get + auto SourceGit register), fix-worktree (bare repo recovery), merge-duplicate (same-origin merge), to-ghq (bare+worktree → ghq, formerly migrate), to-bare (regular repo → bare + worktree, lock-aware), worktree-register (shared metadata register/relink), patrol (batch inspect), move-worktree (register / reclaim merged PR), rename-worktree (rename dir + metadata), sourcegit (preference.json), ssh-key (multi-account SSH map), worktree (inventory + reuse + create). Use when: "ghq get", "sourcegit", "ghq migrate", "repo patrol", "duplicate repo", "worktree fix", "rename worktree", "reuse worktree", "move worktree", "to bare", "convert to bare", "bare convert", "multi-account clone", "core.sshCommand", "Repository not found", "worktree create" triggers.
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash(ghq:*)
  - Bash(git:*)
  - Bash(mv:*)
  - Bash(ls:*)
  - Bash(pgrep:*)
  - Bash(cat:*)
---

# Git Repo

Git repository management and SourceGit GUI client integration.

## Topics

| Topic | Description | Guide |
|-------|-------------|-------|
| clone | ghq get with automatic SourceGit registration (multi-account support) | [clone.md](./clone.md) |
| fix-worktree | bare repo worktree configuration recovery | [fix-worktree.md](./fix-worktree.md) |
| merge-duplicate | merge duplicate repositories with the same origin | [merge-duplicate.md](./merge-duplicate.md) |
| migrate | **renamed → to-ghq** (backward-compat alias) | [migrate.md](./migrate.md) |
| move-worktree | move/register unregistered worktrees to .claude/worktrees/, reclaim merged PR worktrees | [move-worktree.md](./move-worktree.md) |
| patrol | batch inspection of ghq repositories (status, stash, unpushed + commit-splitter integration) | [patrol.md](./patrol.md) |
| rename-worktree | rename worktree directory and metadata (cross-platform, Windows safe) | [rename-worktree.md](./rename-worktree.md) |
| sourcegit | SourceGit preference.json management (add repos, workspaces, folder rename) | [sourcegit.md](./sourcegit.md) |
| ssh-key | per-repo SSH key mapping for multi-account GitHub (core.sshCommand + IdentityAgent) | [ssh-key.md](./ssh-key.md) |
| to-bare | convert a regular repo → bare + worktree at a custom location, preserving uncommitted changes (inverse of to-ghq; helper: `scripts/repo-to-bare-worktree.sh`) | [to-bare.md](./to-bare.md) |
| to-ghq | migrate bare+worktree → regular `.git` at the ghq path (formerly `migrate`) | [to-ghq.md](./to-ghq.md) |
| worktree | unified worktree acquisition: inventory, reuse inactive, or create new at `.claude/worktrees/` | [worktree.md](./worktree.md) |
| worktree-register | shared: register a populated directory as a worktree via metadata only (used by fix-worktree + to-bare) | [worktree-register.md](./worktree-register.md) |

## Topic Dependencies

```
worktree (entry point — inventory + decision)
  └─→ rename-worktree (reuse registered worktree)
  └─→ move-worktree (register unregistered or relocate)

worktree-register (shared metadata register/relink mechanism)
  ├─← fix-worktree (recover a broken bare-worktree link)
  └─← to-bare (link the working tree after a regular→bare conversion)

to-bare  ←inverse→  to-ghq (formerly `migrate`)
```

## Worktree decision tree (HARD STOP — every time a worktree is needed)

**Whenever a worktree is needed (plan/build/test without switching branches, PR verification, isolated work environment, new commit while main branch has another in-flight task), check for inactive worktree reuse before creating a new one.**

### Flow

1. `git -C <repo> worktree list` to enumerate existing worktrees
2. Identify inactive candidates:
   - **Merged-PR worktrees** (commit hash equals the base branch's merge commit)
   - **Stale fix/refactor branch worktrees** (confirm with the user)
3. If an inactive worktree exists → **reuse via the `rename-worktree` topic** (rename the directory + metadata, switch branch)
4. If no inactive worktree exists or the user opts for new → `git worktree add`

### New-commit-start trigger (HARD STOP — paired with git.md)

**When committing new work on a main/master/develop branch, if `git status` shows uncommitted changes from another task, worktree splitting is mandatory.**

#### Entry conditions (any one)

- Current branch = main/master/develop
- `git status` shows 1+ changed files outside the new work (e.g., another task's unstaged files)
- Unpushed commits include another task's work

#### Decision tree on entry

```
git status (check for other changes)
  ├─ 0 other changes, branch = PR/feature → commit in place
  ├─ 0 other changes, branch = main/master/develop
  │    → AskUserQuestion: (a) create PR branch from current (b) create PR branch in a new worktree
  ├─ 1+ other changes, branch = main/master/develop
  │    → worktree split required. Leave other changes in place, isolate new work in a new worktree
  └─ Another task running on a PR branch with stray changes on main
       → Report to the user (confirm intent of stray changes) → decide worktree split + stray cleanup
```

#### Worktree split procedure

1. Leave the new work's diff in place — do NOT stash (preserve the working directory)
2. `git -C <repo> worktree list` to inspect inactive worktrees (per the decision tree above)
3. Inactive candidate present → reuse via `rename-worktree`; otherwise `git -C <repo> worktree add .claude/worktrees/<branch>` (or the worktree path defined by the active environment context — see `worktree.md` "Default Path Rules")
4. cd into the new worktree, then `git checkout -b <new-branch>` (or use the existing inactive branch)
5. **Re-apply the same diff in the new worktree via Edit** (the original main changes stay on main)
6. add → commit → push → PR inside the new worktree

#### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | main has other changes; add the new file + commit + push anyway | Run `git status` → if other changes exist → split into a worktree → commit in the new worktree |
| 2 | Hide other changes with `git stash` and commit on main | stash breaks the other task's intent/sequence. Worktree split is safer |
| 3 | Assume "my changes only — no conflict" | Other working-directory changes can spill over (tests, builds, IDE state) |
| 4 | Omit "worktree split" from the AskUserQuestion commit options | If branch is main/master/develop and other changes exist, "split into worktree + create PR branch" must be the first option |

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Default to `git worktree add <path> <branch>` whenever a worktree is needed | `git worktree list` first → check inactive candidates → consider `rename-worktree` |
| 2 | "Temporary verification — create new and delete" pattern (wastes resources) | Reuse a merged-PR worktree (e.g., one stuck at the merge commit) via rename |
| 3 | AskUserQuestion options offer only "create new worktree" | Include "reuse an existing worktree by rename" whenever an inactive worktree exists |
| 4 | Decide on the worktree autonomously before asking the user | When inactive candidates exist, ask which one to reuse |
| 5 | Ignore merged-PR worktrees | Reclaim them with move-worktree or rename-worktree |
| 6 | **Place "create new worktree" as option 1/Recommended when inactive candidates exist** | **Reuse is Recommended/option 1.** New is option 2 or below |
| 7 | "Unknown purpose for the inactive candidate → recommend safe new" thinking | Inspect the inactive candidate state (`git log`, `git status`) first. If still ambiguous, ask the user which to reuse — but keep reuse as option 1 |

### Recommended placement rule (HARD STOP — prevent 2nd recurrence)

**When building AskUserQuestion options for worktree selection**:

| Inactive candidates | Option order + Recommended |
|--------------|------------------------|
| 0 | Option 1: New worktree (Recommended). Option 2: Hold |
| 1 | **Option 1: Reuse inactive by rename (Recommended)**. Option 2: New worktree. Option 3: Hold |
| 2+ | **Option 1: Rename inactive A (Recommended)**. Option 2: Rename inactive B. Option 3: New worktree. Option 4: Hold |

**The Recommended marker must attach to the reuse option.** "Safer to default to new because purpose is unclear" is an autonomous judgment — instead, document the "verify current commit/branch before reuse" procedure in the rename option description so the user can decide.

### Self-check (before any worktree work)

1. Did you call `git -C <repo> worktree list`?
2. Does any worktree in the output match (a) the same commit as HEAD or (b) a merge commit hash? → inactive candidate
3. If inactive candidates exist, include both the new-add option and the reuse option in AskUserQuestion
4. **Is the Recommended marker attached to the reuse option?** (apply the "Recommended placement rule" table)
5. Use new-add only when 0 inactive candidates exist OR the user explicitly chose new

### Typical failure mode

When a worktree is needed for plan verification, defaulting to "create new + remove later" wastes resources. `git worktree list` often shows merged-PR worktrees stuck on the merge commit hash — these are reuse candidates. Always inventory first before creating a new worktree.

## Quick Reference

### ghq Clone (automatic SourceGit registration)

When `ghq get <url>` is executed, the following happens automatically:
1. Clone the repository
2. Register in SourceGit (under the appropriate group)
3. Auto-create the group if it doesn't exist

**Proceeds automatically without user confirmation**

[Detailed guide](./clone.md)

### SourceGit Management

Directly edit the SourceGit GUI client's configuration file to add repositories, create workspaces, rename folders, etc.

Key features:
- Add/remove repositories
- Create workspaces
- Sync ghq repositories
- Update paths on folder rename

[Detailed guide](./sourcegit.md)

### ghq Migration (to-ghq) / Bare conversion (to-bare)

- **to-ghq** (formerly `migrate`): bare+worktree → regular `.git` at the ghq path (`~/ghq/host/group/repo/`). Auto bare+worktree conversion, optional symlink, nested groups. [Detailed guide](./to-ghq.md)
- **to-bare** (inverse): regular repo → bare + worktree at a custom location (e.g. `.claude/worktrees/`), preserving uncommitted changes. Includes a Windows lock pre-check (SourceGit/VS Code handle on `.git` blocks the rename). [Detailed guide](./to-bare.md)

### Repo Patrol (batch inspection)

Batch inspect and clean up the status of repositories under ghq.

Key features:
- Parallel collection of status, stash, unpushed for all repositories
- Status-based processing (commit-splitter integration, stash pop, push)
- Optional fetch all at the end

[Detailed guide](./patrol.md)

## Common Workflow

1. **Repository migration**: Migrate to ghq structure with `to-ghq` topic (or `to-bare` for the inverse)
2. **SourceGit update**: Register new paths with `sourcegit` topic
3. **Batch inspection**: Clean up uncommitted/unpushed changes with `patrol` topic

## Scripts

- `./scripts/repo-to-ghq.sh` - Move a repository to the ghq path (bare+worktree → regular)
- `./scripts/repo-to-bare-worktree.sh` - Convert a regular repo → bare + worktree (inverse)
