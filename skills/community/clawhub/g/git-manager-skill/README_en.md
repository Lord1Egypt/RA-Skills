# Git Manager

> Author: zhuyijun · https://zyjblogs.cn

### Overview

`git-manager` is a powerful Git repository management tool for full-featured operations across GitHub, GitLab, and Gitea platforms. It supports batch cloning, pulling, merging, rebasing, committing, staging area operations, Git LFS management, and more — all via simple command-line scripts with zero extra dependencies (Python 3.8+, standard library only).

### Features

| Feature | Description |
|---------|-------------|
| **Batch Clone** | Clone all repos from a GitHub org/user, GitLab group/user/project, or Gitea org/user by ID. Supports `--limit N`, `--lfs`, `--filter`, `--depth`, `--workers N` concurrency, `--format json`, `--recursive` subgroups |
| **Batch Pull** | Scan a local directory tree and batch `git pull`/`fetch` across all discovered repositories with concurrency support, `--dry-run` preview mode |
| **Single-repo Ops** | clone, pull, fetch, merge, rebase, branch, checkout, status, diff, log, show, blame, tag, remote, clean, gc |
| **Staging Area** | `add` (partial/full/interactive), `commit` (with `--amend`), `reset` (soft/mixed/hard) |
| **Stash** | `stash` (save/pop/list/drop/clear), preserves working directory changes safely |
| **Git LFS** | `--install`, `--track`, `--untrack`, `--fetch`, `--pull`, `--push`, `--ls-files`, `--ls-tracks`, `--migrate` |

### File Structure

```
git-manager/
├── SKILL.md                 # Skill definition file
├── README.md                # Chinese documentation
├── README_en.md             # This file (English documentation)
├── CHANGELOG.md             # Version changelog
├── scripts/
│   ├── batch_clone.py       # Batch cloning script (concurrency + JSON output)
│   ├── batch_pull.py        # Batch pull/fetch script
│   ├── git_ops.py           # Single-repo operations
│   └── git_lfs.py           # Git LFS utilities
└── references/
    ├── api_reference.md     # Platform API quick reference
    └── examples.md          # Complete usage examples
```

### Quick Start

```bash
# Python interpreter path (managed runtime)
PY=C:\Users\zhuyi\.workbuddy\binaries\python\versions\3.13.12\python.exe

# Batch clone GitHub user's first 5 repos, enable LFS, 4-thread concurrency
$PY scripts/batch_clone.py --platform github --type user --id zyjnicemoe \
  --output ./repos --limit 5 --lfs --workers 4

# Batch clone GitLab group (with subgroups, JSON output, 8 threads)
$PY scripts/batch_clone.py --platform gitlab \
  --host https://gitlab.com --type group --id 123456 \
  --token glpat-xxx --output ./repos --format json --workers 8

# Token via environment variable (more secure)
export GITLAB_TOKEN=glpat-xxx
$PY scripts/batch_clone.py --platform gitlab \
  --host https://gitlab.com --type group --id 123456 --output ./repos

# Batch clone Gitea organization
$PY scripts/batch_clone.py --platform gitea \
  --host https://git.example.com --type org --id myorg \
  --output ./repos

# Batch update all repos under ./repos (rebase mode, 4 workers)
$PY scripts/batch_pull.py ./repos --rebase --workers 4

# Single repo: clone with LFS, then commit
$PY scripts/git_ops.py clone https://github.com/user/repo.git ./my-repo --lfs
$PY scripts/git_ops.py add ./my-repo -A
$PY scripts/git_ops.py commit ./my-repo -m "Initial commit"

# Enable LFS and track common binary formats
$PY scripts/git_lfs.py ./my-repo --install
$PY scripts/git_lfs.py ./my-repo --track "*.zip" "*.tar.gz" "*.psd" "*.pdf"
```

### Key Arguments

**`batch_clone.py`**:

| Argument | Description |
|----------|-------------|
| `--platform` | Platform: `github` \| `gitlab` \| `gitea` |
| `--type` | ID type: `org` \| `group` \| `user` \| `project` |
| `--id` | Org name, group ID, username, or project ID |
| `--host` | Platform URL (GitLab/Gitea only; GitHub auto-detected) |
| `--token` | API access token (required for private repos; GitHub anonymous: 60 req/hr) |
| `--ssh` | Use SSH URLs instead of HTTPS |
| `--branch` | Clone specific branch |
| `--depth N` | Shallow clone with N commits |
| `--update` | Pull and update existing repos instead of skipping |
| `--filter <keyword>` | Filter repos by name |
| `--limit N` | Clone only the first N repos |
| `--archived` | Include archived repos |
| `--lfs` | Initialize Git LFS after clone with common binary file tracking rules |
| `--dry-run` | Preview only, no actual cloning |

**`batch_pull.py`**:

| Argument | Description |
|----------|-------------|
| `--rebase` | Use `git rebase` instead of `git merge` |
| `--fetch` | Only fetch, do not merge |
| `--stash` | Auto-stash uncommitted changes before pulling |
| `--workers N` | Number of concurrent workers (default: 4) |
| `--filter <keyword>` | Only process repos whose names contain keyword |
| `--max-depth N` | Directory scan depth (default: 3) |

**`git_ops.py`** sub-commands:

```
clone, pull, fetch, branch, checkout, merge, rebase
add, commit, reset, stash, diff, status, log, show
blame, tag, remote, clean, gc, lfs
```

### Notes

- **Token security**: Avoid exposing tokens in shell history. Use Git credential helpers or environment variables.
- **Rate limits**: GitHub unauthenticated = 60 req/hr; use a token for batch operations.
- **SSH vs HTTPS**: `--ssh` requires SSH keys configured on the target platform.
- **Rebase warning**: Never rebase already-pushed public branches.
- **Conflict handling**: Merge/rebase conflicts stop the operation; resolve manually, then `git add` + `git merge/rebase --continue`.
- **GitLab group_id**: Go to Group → Settings → General to find the numeric ID; you can also use the URL-encoded path (e.g. `my-group%2Fsub-group`).
- **Gitea pagination**: Uses `limit` parameter (not `per_page`); the script handles the difference automatically.
- **Git LFS**: Ensure `git-lfs` is installed on the machine (`git lfs install`).
