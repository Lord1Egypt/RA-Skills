---
name: hg-to-git
description: Convert Mercurial (hg) repositories to Git. Use when migrating from Mercurial to Git, converting hg repos to git format, preserving history and branches during VCS migration, or when working with legacy Mercurial repositories that need to be moved to Git.
---

# Mercurial to Git Converter

Convert Mercurial repositories to Git while preserving full history, branches, and tags.

## Prerequisites

- `hg` (Mercurial) installed
- `git` installed
- `hg-fast-export` (auto-installed if missing)

## Quick Start

```bash
# Basic conversion
hg-to-git.sh /path/to/hg-repo /path/to/git-repo

# Large repository with progress
hg-to-git-large.sh /path/to/hg-repo /path/to/git-repo

# Extract authors first (recommended)
hg-authors.sh /path/to/hg-repo authors.map
# Edit authors.map, then run conversion
```

## Scripts

### `scripts/hg-to-git.sh`
Standard conversion for most repositories.

**Usage:**
```bash
hg-to-git.sh <hg-repo-path> [git-repo-path]
```

**Features:**
- Auto-installs hg-fast-export if missing
- Preserves all branches and tags
- Handles author mapping

### `scripts/hg-to-git-large.sh`
Optimized for large repositories with progress feedback.

**Usage:**
```bash
hg-to-git-large.sh <hg-repo-path> [git-repo-path]
```

**Features:**
- Shows progress dots during conversion
- Displays revision count upfront
- Summarizes results at end

### `scripts/hg-authors.sh`
Extract and map Mercurial authors to Git format.

**Usage:**
```bash
hg-authors.sh <hg-repo-path> [output-file]
```

**Output format:**
```
"Mercurial Author"="Git Author <email>"
```

Edit the output file to fix email addresses before conversion.

## Workflow

1. **Extract authors** (optional but recommended):
   ```bash
   hg-authors.sh /path/to/hg-repo authors.map
   ```

2. **Edit author map** - Update email addresses in `authors.map`

3. **Run conversion**:
   ```bash
   hg-to-git.sh /path/to/hg-repo /path/to/git-repo
   ```

4. **Verify**:
   ```bash
   cd /path/to/git-repo
   git log --oneline -10
   git branch -a
   git tag -l
   ```

## Troubleshooting

### hg-fast-export not found
The scripts auto-install from GitHub if not present in PATH.

### Author mapping issues
Use `hg-authors.sh` to generate a mapping file, edit it, then pass to fast-export with `-A authors.map`.

### Large repositories
Use `hg-to-git-large.sh` for better progress visibility.

### Branches not converted
Run `git branch -a` in the new repo. Remote branches may need to be checked out locally.
