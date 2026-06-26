# Worktree Register

Register an existing **populated** directory as a git worktree using **metadata manipulation only** — no fresh checkout, no file moves, uncommitted changes preserved.

This is the shared low-level mechanism used by both [fix-worktree](./fix-worktree.md) (recover a broken bare-worktree link) and [to-bare](./to-bare.md) (link the working tree after a regular→bare conversion). Both reference this topic instead of duplicating the steps.

## When to Use

- A directory already contains files but is **not** listed in `git worktree list` and you want to register it as a worktree (without `git worktree add`, which refuses a non-empty directory).
- After moving a `.git` out to a bare repo, the now-`.git`-less working tree needs to be re-linked to the bare.

## Why not `git worktree add`

`git worktree add` creates a **fresh checkout** and **rejects a directory that already contains files**. When the target already holds the working tree (with uncommitted changes), a fresh checkout would either fail or discard those changes. Metadata-only registration preserves everything.

## Pre-check (mandatory)

```bash
git -C <bare-or-main-repo> worktree list   # the target must NOT already be listed
```

If it is already listed, skip — it is registered.

## Procedure

Inputs:
- `GITDIR` — the common git dir: a bare repo (`<repo>.git`) or a main repo's `.git`
- `WT` — the absolute path to the worktree directory (already populated)
- `NAME` — admin name under `<GITDIR>/worktrees/<NAME>` (usually `basename "$WT"`)
- `BRANCH` — the branch this worktree should be on

```bash
# Windows-form absolute paths (git metadata files are not MSYS-path aware)
to_win() { command -v cygpath >/dev/null 2>&1 && cygpath -m "$1" || echo "$1"; }
GITDIR_W="$(to_win "$GITDIR")"
WT_W="$(to_win "$WT")"

# 1. Ensure the branch exists (create from a commit if needed)
git -C "$GITDIR" rev-parse --verify "refs/heads/$BRANCH" >/dev/null 2>&1 \
  || git -C "$GITDIR" branch "$BRANCH" <commit-sha>

# 2. Create the worktree admin dir
mkdir -p "$GITDIR/worktrees/$NAME"
echo "ref: refs/heads/$BRANCH" > "$GITDIR/worktrees/$NAME/HEAD"
echo "../.."                    > "$GITDIR/worktrees/$NAME/commondir"
echo "$WT_W/.git"               > "$GITDIR/worktrees/$NAME/gitdir"

# 3. Point the worktree's .git file at the admin dir
echo "gitdir: $GITDIR_W/worktrees/$NAME" > "$WT/.git"

# 4. Rebuild the worktree index from HEAD (resolves the all-files-"deleted"
#    status; preserves uncommitted working files — does NOT touch the tree)
git -C "$WT" reset HEAD -- .
```

## Verify

```bash
git -C "$GITDIR" worktree list        # the worktree now appears
git -C "$WT" status --short           # shows only real uncommitted changes
git -C "$WT" log --oneline -1         # correct HEAD
```

## Key Principles

| # | Don't | Do |
|---|-------|-----|
| 1 | `git worktree add` onto a populated directory | Create the metadata by hand (it accepts an existing tree) |
| 2 | Move/copy files to "set up" the worktree | Only create `.git` + admin metadata — leave the tree untouched |
| 3 | `git read-tree HEAD` to fix the index | `git reset HEAD -- .` — rebuilds from HEAD without destroying working files |
| 4 | Write MSYS paths (`/c/Users/...`) into gitdir/`.git` | Use `cygpath -m` → `C:/Users/...`; git resolves the Windows form |
| 5 | Skip the `worktree list` pre-check | Always check first — registering a duplicate corrupts the admin dir |

## Notes

- Uncommitted (staged/unstaged) changes are safely preserved — only metadata is created and the index is rebuilt from HEAD.
- The same branch cannot be checked out in two worktrees. For a bare common dir, the bare itself has no checkout, so its default branch is free to use in one worktree.
