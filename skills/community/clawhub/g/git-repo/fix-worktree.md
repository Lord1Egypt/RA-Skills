# Fix Worktree

A tool to fix incorrect worktree configuration in ghq bare repositories.

## Diagnosis (Problem Scenarios)

The following issues can occur in ghq + git worktree structures:
- `bare = false` but `core.worktree` points to a wrong path
- Worktree directory exists but is not registered in the bare repo
- Incorrect `core.worktree` config causes git commands to fail

## Usage

### Scan and fix all bare repos

```bash
scripts/git-fix-worktree.sh
```

### Fix a specific bare repo

```bash
scripts/git-fix-worktree.sh /path/to/repo.git
```

## Fix Behavior

1. **When worktree exists**: Register in bare repo's `worktrees/` directory
2. **Worktree's `.git` file**: Fix to point to subdirectory under `worktrees/`
3. **Index regeneration**: If missing, regenerate with `git read-tree HEAD` (preserves uncommitted changes)
4. **Config restoration**: Remove `core.worktree`, set `core.bare = true`

## Example Output

```
Scanning for broken bare repos in: ~/ghq
Fixed: ~/ghq/github.com/es6kr/repo.git
  Registered worktree: ~/es6kr/repo
  Updated .git -> ~/ghq/github.com/es6kr/repo.git/worktrees/repo
  Rebuilt index
Done.
```

## Register Existing Directory as Worktree

Registering a directory that already contains files (metadata-only, no fresh checkout) is the shared mechanism documented in **[worktree-register](./worktree-register.md)**. Use that topic's procedure here — pass the bare/main repo as `GITDIR`, the existing directory as `WT`, and the recovered branch.

The same mechanism is reused by [to-bare](./to-bare.md) after a regular→bare conversion. Keeping it in one place avoids drift between the two flows.

## Related Commands

```bash
# Check worktree status
git worktree list

# Check bare repo configuration
git config -f /path/to/repo.git/config --list

# Check worktree's .git file
cat /path/to/worktree/.git
```

## Notes

- Local changes (uncommitted changes) are safely preserved
- Index regeneration is based on HEAD, so staged/unstaged files remain intact
- The script only modifies metadata and does not delete actual files
