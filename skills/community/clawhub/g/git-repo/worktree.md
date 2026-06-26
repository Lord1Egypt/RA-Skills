# Worktree

Unified workflow for acquiring a git worktree: inventory existing ones, identify inactive candidates, reuse via rename/move, or create new at the default path.

## When to Use

- Need an isolated working directory for a branch (PR verification, plan testing, parallel work)
- Before running `git worktree add` — always check for reusable worktrees first

## Procedure

### 1. Inventory existing worktrees

```bash
cd /path/to/repo
git worktree list
```

Also scan for unregistered worktree directories:

```bash
ls .claude/worktrees/ 2>/dev/null   # Claude Code default path
```

### 2. Identify inactive candidates

A worktree is **inactive** (reuse candidate) if any of:

| Condition | How to check |
|-----------|-------------|
| Branch was merged and deleted | `git branch -d <branch>` succeeds or remote branch gone |
| Commit hash matches a merge commit on base branch | `git log --oneline <base> \| grep <hash>` |
| Not currently checked out by any session | No editor/terminal has `cwd` in that worktree |
| Stale fix/refactor branch with no recent commits | `git log -1 --format=%ci <branch>` older than 7 days |

### 3. Decision — reuse or create

```
inactive candidates found?
├─ YES → AskUserQuestion: which one to reuse?
│        ├─ User selects one → Step 4A (rename/move)
│        └─ User says "create new" → Step 4B (new)
└─ NO  → Step 4B (new)
```

**AskUserQuestion options must include both reuse and new-create** when inactive candidates exist.

### 4A. Reuse via rename or move

Delegate to the appropriate sub-topic:

| Situation | Topic |
|-----------|-------|
| Worktree is registered (`git worktree list` shows it) | [rename-worktree](./rename-worktree.md) — rename dir + metadata + switch branch |
| Worktree dir exists but not registered | [move-worktree](./move-worktree.md) Scenario A — register + switch branch |
| Worktree in wrong location (`.worktrees/`) | [move-worktree](./move-worktree.md) Scenario B — relocate to `.claude/worktrees/` |

After rename/move, verify:

```bash
git worktree list                    # confirm registration
cd <worktree-path>
git branch --show-current            # confirm target branch
git status --short                   # confirm clean state
```

### 4B. Create new worktree

**Default path**: `<repo>/.claude/worktrees/<branch-name>`

```bash
cd /path/to/repo
git worktree add .claude/worktrees/<branch-name> <branch>
```

If the branch does not exist yet:

```bash
git worktree add -b <new-branch> .claude/worktrees/<new-branch> <start-point>
```

Post-create verification:

```bash
git worktree list
cd .claude/worktrees/<branch-name>
git branch --show-current
```

### 5. Post-acquisition check (MANDATORY)

Before writing any code in the worktree:

```bash
cd <worktree-path>
git branch --show-current   # must match intended branch
```

If branch mismatch → do NOT proceed with Write/Edit. Fix first (checkout or re-create).

## Default Path Rules

| Environment | Worktree path |
|-------------|--------------|
| Claude Code (any) | `<repo>/.claude/worktrees/<name>` |
| vibe-kanban | Managed by vibe-kanban (do not override) |
| Other plugins / agents | Honor the path declared in their context (project `CLAUDE.md`, plugin settings, env var) |

**Default**: this skill standardizes on `<repo>/.claude/worktrees/<name>`. If the active environment context (project `CLAUDE.md`, plugin settings such as vibe-kanban, or environment variables) pins a different worktree path, honor that path instead. Creating `<repo>/.worktrees/` ad hoc — without any environment context declaring it — is discouraged because it splinters the worktree root across tools.

## Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | `git worktree add` as first action | `git worktree list` first → check for reusable candidates |
| 2 | Present only "create new" in AskUserQuestion | Include "reuse worktree X" option when inactive candidates exist |
| 3 | Create worktree in `.worktrees/` | Use `.claude/worktrees/` |
| 4 | Start coding without branch verification | `git branch --show-current` before any Write/Edit |
| 5 | Delete inactive worktrees to "clean up" | Reuse them — rename is cheaper than delete+create (subject to count limit below) |

## Inactive Worktree Count Limit (HARD STOP)

Reuse via rename is the default for inactive worktrees (Don't/Do rule #5). However, **unbounded reuse accumulation pollutes `git worktree list` and increases the cognitive cost of every future "reuse vs create" decision**. Cap inactive reuse candidates at **5**; beyond that, `git worktree remove` is the correct action.

### Count basis (HARD STOP)

- Count = "inactive" worktrees only (excluding the main worktree at repo root and any currently in-progress feature worktrees the user is actively committing on)
- A worktree is **inactive** by the same criteria as §2 above (no recent commits / merged or deleted branch / dirty stash but no upstream work)
- Active worktrees (claude, currently-edited feature) are **not** counted toward the limit

### Decision matrix

| Inactive count (after cleanup of just-completed worktree) | Action for the just-completed worktree | Rationale |
|-----------------------------------------------------------|----------------------------------------|-----------|
| ≤ 5 | **B: reuse** — `git checkout --detach origin/main` + `git branch -D <feature>` | Pool is healthy. Reuse avoids the cost of fresh worktree creation (~10-30s + ENOSPC risk on small `.git/worktrees`) |
| > 5 | **A: remove** — `git worktree remove <path>` + `git branch -D <feature>` | Pool is full. Removing the just-completed worktree (rather than an older inactive one) avoids touching others' historical workspaces |

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Keep every just-completed worktree as a reuse candidate regardless of count | Apply the matrix above; remove beyond 5 inactive |
| 2 | Choose A (remove) when inactive count is ≤ 5 to "be tidy" | Reuse is cheaper than create. B is default until the cap is hit |
| 3 | Remove an *older* inactive worktree to make room for the just-completed one | Remove the **just-completed** one. Older inactive worktrees may have stashes / unpushed branches worth preserving |
| 4 | Count active worktrees (claude, in-progress feature) toward the limit | Active = currently used. Only inactive worktrees count |

### Self-check (every time after a worktree's branch is merged/deleted)

1. Run `git worktree list` → count entries excluding repo root + active worktrees
2. If count > 5 after this just-completed worktree → choose A (remove)
3. If count ≤ 5 → choose B (detach + branch -D) for reuse
4. Always pull main worktree to `origin/main` regardless of A or B

### Origin

User decision 2026-05-24 after PR #160 merge cleanup of `agent-abbddf41` worktree (8 total worktrees, 5 inactive after cleanup — at the limit, B chosen). Rule extracted from the trade-off between "rename is cheaper than delete+create" (existing Don't/Do #5) and "unbounded accumulation pollutes the worktree list".

## Pre-commit worktree matrix check (HARD STOP)

**Before starting any new commit (in any worktree, including the main repo), inspect the entire worktree matrix to confirm no other worktree has active in-flight work the user is still arranging.** Failing this check leads to "the user was reorganizing another worktree and I committed without noticing" — a high-cost recovery (sometimes amend/rebase, sometimes user objection).

**Why**:
- `git worktree list` shows commit hash per worktree but not staged/dirty state. A worktree may have active commits the user just authored or is staging
- The user may be mid-cleanup across multiple worktrees in parallel (e.g., reorganizing inactive worktrees while you commit in the main). Your commit collides with their intent
- Worktree commit hash equal to a merge commit on a published branch does NOT mean inactive — it could be a freshly checked-out reuse target the user is preparing

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | `git worktree list` only checks commit hash, skip per-worktree state inspection | For each worktree, run `git -C <path> log -3 --oneline` + `git -C <path> status --short` before commit |
| 2 | Trust "worktree branch is not my work branch, so it's safe" | Other worktree's branch may carry user's WIP. Read its recent commits + dirty state |
| 3 | Skip the matrix check when committing on main/master/develop | Especially required on shared branches — multiple worktrees may share dependent state |
| 4 | "User said the main is clean, so all worktrees are clean" | User may be focused on one worktree. Matrix check covers all worktrees regardless |
| 5 | After the check, commit without noting unfamiliar worktrees | If a worktree's branch/commits are unfamiliar, ask the user about that worktree's purpose before committing in another worktree |

### Procedure (before EVERY commit)

1. `git worktree list` — enumerate paths + branches + commit hashes
2. For each worktree path `<W>` other than the current commit target:
   - `git -C <W> log -3 --oneline` — recent commits in that worktree's branch
   - `git -C <W> status --short` — dirty / staged state
3. Classify each worktree using the same inactive criteria as the **Inactive Worktree Count Limit** section above:
   - **Active**: recent commits look like user's WIP or branch is unfamiliar → halt, report to user
   - **Stale**: branch matches a known merged PR or matches a known stale pattern → safe to ignore
4. If 1+ active worktree found → halt commit, ask the user about that worktree's recent activity
5. Only after all other worktrees classified as Stale → proceed with commit in the target worktree

### Self-check (commit-time, every time)

1. Did you run `git worktree list`?
2. Did you run `git -C <W> log -3` + `status --short` for EACH worktree other than the commit target?
3. Did any other worktree show unfamiliar commits or dirty state?
4. If Yes to #3, did you halt and ask before committing?

**Verdict**: Failing any of items 1-4 = matrix check skipped = rule violation

## Inactive worktree inventory before creating a new one (HARD STOP)

**When a worktree is needed, inspect existing worktrees before creating a new one with `git worktree add`.**

| # | Don't | Do |
|---|-------|-----|
| 1 | Default to creating a new worktree with `git worktree add` whenever one is needed | Run `git worktree list` first → identify inactive / merged-PR worktrees → reuse via `/git-repo rename-worktree` or `/git-repo move-worktree` |
| 2 | AskUserQuestion options default to "create new and remove later" | Include "rename and reuse an inactive worktree" whenever at least one inactive candidate exists |
| 3 | Ignore worktrees pinned at the merge commit of a merged PR | The base commit hash matching a merge commit = a reuse candidate |

See the "Worktree decision tree" section above for the full procedure.

## Branch state check before starting a new commit (HARD STOP)

**Before committing new work (or before presenting commit-method options via AskUserQuestion), check whether the current branch has uncommitted changes from another task.** When other work is mixed in on a shared branch (main/master/develop), the commit can conflict with that other intent, and `git push` risks conflict/rollback. When detected, **split into a worktree or create a new branch first**.

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Right after Edit, present commit options (PR branch / master push / hold) via AskUserQuestion without checking | Before composing the options, run `git status` — if other-task changes are present, include the "split into worktree" option |
| 2 | Current branch is main/master/develop with unstaged/staged changes; still run `git add <new-file>` | Run `git status` → if changes belong to another task, split via `/git-repo` into a new worktree → commit there |
| 3 | Assume "only my changes are staged, so other changes don't matter" | The same push can include unpushed commits from another task, and other dirty working-directory state can leak into the next step |
| 4 | Omit "split into worktree" from the commit-options AskUserQuestion list | When branch is main/master/develop AND there are 1+ other-task changes, "split into worktree" is a required option |
| 5 | Leave another task's unstaged changes in place and push only the new commit | Confirm the other-task intent (report to the user) → split into a worktree or separate it into another task |
| 6 | **Place "create new worktree" as option 1 / Recommended when inactive candidates exist** | **If 1+ inactive worktree candidates exist, place "rename and reuse" as option 1 / Recommended**. New goes to option 2 or lower |
| 7 | Assume "worktree split = move the working-tree changes out of the current repo" (stash + checkout) when the current repo is a live runtime environment whose working tree state is actively consumed by the user (e.g., `~/.agents` — rules are loaded always_on, skills are hardlinked to `~/.claude/skills/`) | Distinguish two split modes: **(a) move** — stash + checkout to a new branch (default for one-off feature work) vs **(b) copy** — leave the source working tree untouched + replicate the diff into a separate worktree via `cp`/`rsync` and commit there. Use (b) whenever the source repo's working tree is a live runtime environment. The source working tree must not change state for the user during commit/PR |

### Self-check (every time before presenting commit options)

1. `git -C <repo> status --short` — list of changed files
2. `git -C <repo> branch --show-current` — current branch
3. Branch is main/master/develop AND ≥2 changes (mine + other) → **worktree split is mandatory**
4. Only my single-task change AND branch is PR/feature → commit in place
5. Unpushed commits present → `git log @{u}..HEAD --oneline` — if another task's commits are mixed in, a separate push strategy is needed

### worktree split decision tree

```text
git status (changes)
  ├─ Only mine (1 task), branch = PR/feature → commit in place
  ├─ Mine + other-task, branch = main/master/develop → /git-repo worktree split mandatory
  ├─ Only mine, branch = main/master/develop → present both "create PR branch in place" and "split into worktree + create PR branch"
  └─ Another task in progress on a PR branch → leave it alone. Return to main and create a new worktree
```

### Failure case

See failed-attempts.md HOT entry "worktree split option missing in commit-method ask".

## Branch verification before editing code on issue work (HARD STOP)

**When making a code change tied to an issue number (#N), verify the current branch is the issue's branch BEFORE running Edit/Write.**

| # | Don't | Do |
|---|-------|-----|
| 1 | Editing for #326 while on `feat/222-backchannel-logout` | `git branch --show-current` → issue number mismatch → create the issue branch first |
| 2 | After registering a task via /wip, edit code without verifying branch | Register → `git branch --show-current` → for a github-flow project, ensure issue branch → Edit |
| 3 | "It's a small fix, current branch is fine" thinking | Even a one-line change: a github-flow project requires the issue branch (MEMORY.md reference) |

**Self-check (every time before Edit/Write)**:
1. Does the current branch name include the in-flight issue number?
2. If not, is this project github-flow? (check MEMORY.md)
3. github-flow + issue number mismatch → `gh issue develop --name "<tag>/<issue-number>-<desc>"` or `git checkout -b` first, then work

## Branch verification before implementation in worktree (HARD STOP)

**Before editing code in a worktree via Write/Edit, verify the branch is the intended one.**

The verification timing is **before implementation starts** — not before commit. Once a file is written into the wrong environment, the damage is done.

1. Right after `git worktree add`, **immediately** verify:
   ```bash
   cd "path/to/worktree" && git branch --show-current
   ```
2. If the output does not match the intended branch, **forbid Write/Edit** — re-create the worktree or checkout
3. Starting Write/Edit without this verification = procedural violation

## cd consistency on worktree entry (HARD STOP)

**When the user specifies a worktree path (`.worktrees/<name>` or `.claude/worktrees/<name>`), run every subsequent git command in that worktree directory for the rest of the session.** Forbid `cd` back to the main repo to run git commands — the worktree and the main repo can have **different HEADs**, so `git log HEAD`, `git status`, `git branch --show-current` all return different results.

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Run the first command with `cd <worktree>`, then `cd <main repo> && git fetch ...` on the next | From the first to the last command, stay in the **same worktree only**. Even fetch can run inside the worktree (the `.git` is shared) |
| 2 | "The `.git` is shared between worktree and main, so the results are identical" assumption | Shared `.git` ≠ identical HEAD. Each worktree has its own HEAD/index. `git log HEAD` differs |
| 3 | Ignore that cwd resets between separate Bash calls, and omit `cd` | Add `cd <worktree>` to every Bash call, or use the `git -C <worktree>` flag |
| 4 | Treat `git log origin/develop..HEAD` output as the worktree's commits without verifying where it ran | Before running, check current location via `pwd` or `git rev-parse --show-toplevel`, then report |

### Self-check (before EVERY Bash call during worktree work)

1. The user-specified worktree path = `<W>`
2. Does the Bash command include `cd <W>` or `git -C <W>`?
3. If not, add it. `cd ~/ghq/.../<repo>` (main repo) alone, with no worktree path, is a violation
4. When interpreting command results, self-ask: "is this measured against the worktree or the main repo?"

### Recommended pattern (using the `git -C` flag)

```bash
WT=~/ghq/github.com/daegunsoftDev/deps-provisioning/.worktrees/fix-18-dev38-launch-url
git -C "$WT" branch --show-current
git -C "$WT" log --oneline origin/develop..HEAD
git -C "$WT" fetch origin develop
```

No cwd change required, no confusion with the main repo.

## Topic Dependencies

```
worktree (this topic — entry point)
  └─→ rename-worktree (reuse registered worktree)
  └─→ move-worktree (register unregistered or relocate)
```
