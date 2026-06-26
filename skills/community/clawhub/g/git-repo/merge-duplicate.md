# Merge Duplicate Repositories

Workflow for merging two local repositories that point to the same origin into one.

## When to Use

- Two repositories with the same origin exist at different paths in ghq
- Duplicate occurred due to mismatch between local path and origin path

## Workflow

### Step 1: Pre-check

```bash
# Compare HEAD of both repositories
git -C <src> rev-parse HEAD
git -C <dst> rev-parse HEAD

# Check src repository status
git -C <src> stash list
git -C <src> branch -v
git -C <src> status --short
git -C <src> tag -l
```

**AskUserQuestion required if stash or unpushed branches exist**

### Step 2: Temporary commit + tag in src repository

If src has uncommitted/untracked changes, preserve with a temporary commit:

```bash
cd <src>
git add -A  # -A allowed for temporary preservation purposes
git commit -m "temp: preserve local changes before migration"
git tag merge-backup-$(date +%Y%m%d)
```

Working tree becomes clean after commit.

### Step 3: Add src as remote to dst repository and transfer tags

```bash
cd <dst>
git remote add merge-src <src-path>
git fetch merge-src --tags
git remote remove merge-src
```

Now dst has the merge-backup tag — recovery possible later.

### Step 4: Move files from src to dst (mv)

Check unique files/changes in src and **mv** to dst:

```bash
# Check files included in the temporary commit:
git -C <dst> show merge-backup-YYYYMMDD --stat

# Move necessary files with mv
mv <src>/unique-file <dst>/
```

**Never use cp/rsync** — use mv only.
**AskUserQuestion required** if files to move also exist in dst.

### Step 5: Clean up src directory (rmdir)

Remove empty folders after all files have been moved:

```bash
# Check .git file/directory
ls -la <src>/.git

# If .git is a file (gitdir pointer), delete it
rm -f <src>/.git

# If .git is a directory (actual repository):
#   - Verify tags were transferred to dst
#   - git -C <dst> tag -l | grep merge-backup
#   - After verification: rm -rf <src>/.git (AskUserQuestion required)

# Remove empty folders (bottom-up)
find <src> -type d -empty -delete
# src directory itself will be auto-deleted if empty
```

**Do not rm -rf the entire src** — it should naturally disappear via mv + rmdir.
**AskUserQuestion required** if files remain after rmdir/find -empty -delete.

### Step 6: Update SourceGit

- Remove src path entry
- Verify dst path is correctly registered

## Safety Rules

- **Before deleting src**: always check stash, unpushed branches/tags
- **Preserve temporary commits with tags** — verify tag transfer to dst
- **Use mv only** — cp/rsync/find -delete prohibited
- **rm -rf prohibited** — natural elimination via mv + rmdir
- When in doubt, **AskUserQuestion**
