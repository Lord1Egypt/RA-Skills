# To Bare

Convert an existing **regular** repo into a **bare** repo and register its working tree as a git worktree at a custom location (e.g. `~/.agents/.claude/worktrees/<name>`), **preserving uncommitted changes**.

This is the **inverse** of [to-ghq](./to-ghq.md) (which converts bare+worktree → a regular `.git` at the ghq path).

## When to Use

- A loose regular clone (often a divergent duplicate) should become a bare repo that serves managed worktrees under `.claude/worktrees/`.
- You want the working tree (with in-progress uncommitted work) to live as a proper worktree without losing changes.

## Result

```
before:  <repo>/            (regular clone, real .git, maybe uncommitted changes)
after:   <repo>.git         (bare, core.bare=true)
         <target-path>      (worktree on the same branch, uncommitted changes intact)
```

## Script

```bash
bash ~/.claude/skills/git-repo/scripts/repo-to-bare-worktree.sh \
  --repo ~/ghq/github.com/<org>/<repo> \
  --worktree ~/.agents/.claude/worktrees/<name> \
  [--name <wt-name>] [--force]
```

| Flag | Meaning |
|------|---------|
| `--repo` | Existing regular repo (must have a real `.git` dir) |
| `--worktree` | Target path for the working tree |
| `--name` | Admin name under `<bare>/worktrees/` (default: basename of `--worktree`) |
| `--force` | Skip the lock pre-check (not recommended) |

## Procedure (what the script does)

1. **Lock pre-check (HARD STOP on Windows)** — abort if a git GUI/editor (SourceGit, VS Code, Cursor, Fork, GitKraken, TortoiseGit) is running. A Windows directory rename of `<repo>` fails with **Permission denied** while such an app holds a handle on `<repo>/.git`. Git commands still work (read/write the index) — only the filesystem rename is blocked. Close the app(s) with the repo open, then re-run.
2. `mv <repo> <target-path>` — atomic rename, preserves the `.git` and all uncommitted changes.
3. `mv <target-path>/.git <repo>.git` — extract the git dir into the bare.
4. `git -C <repo>.git config core.bare true`.
5. **Relink the worktree** via the [worktree-register](./worktree-register.md) mechanism (admin dir `HEAD`/`commondir`/`gitdir` + the worktree's `.git` file, Windows-form paths via `cygpath -m`).
6. `git -C <target-path> reset HEAD -- .` — rebuild the worktree index from HEAD; the index moved into the bare so the fresh worktree index must be rebuilt. This preserves uncommitted working files.
7. **Verify** — `worktree list` shows the new worktree; `status` shows only the real uncommitted changes; HEAD is correct.

## Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Run while SourceGit / VS Code has the repo open | Close the holder first — the rename fails with Permission denied otherwise. The script's pre-check enforces this |
| 2 | `git clone --bare` to make the bare (loses uncommitted changes) | `mv` the existing `.git` → bare so working-tree + index move intact |
| 3 | `git worktree add <target>` (fresh checkout discards the populated tree) | Metadata relink via worktree-register — keeps the existing tree |
| 4 | Leave the worktree index from the bare (everything shows as staged-deleted) | `git reset HEAD -- .` rebuilds the worktree index from HEAD |
| 5 | Forget the SourceGit registration is now stale | The old `<repo>` path is gone → update SourceGit ([sourcegit](./sourcegit.md)): remove old path, add the bare/worktree |

## Verify (post-conversion)

```bash
git -C <repo>.git worktree list                 # bare + the new worktree
git -C <target-path> status --short             # only real uncommitted changes
git -C <target-path> branch -a                  # remote branches reachable via bare
[ -e <repo> ] && echo "stale original remains" || echo "original cleaned"
```

## Notes

- If `<target-path>` is inside another repo's working tree (e.g. `~/.agents/.claude/worktrees/`), confirm that location is gitignored there so the foreign worktree does not pollute that repo's status.
- The bare's default branch can be checked out by exactly one worktree; the bare itself has no checkout, so the branch is free.
