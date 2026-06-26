---
name: git-deployer
description: Push static site content to GitHub Pages repositories. Clone, copy files, commit with timestamp, force-push. Use when updating GitHub Pages sites, deploying static sites, or syncing local content to a git-based host.
---

# git-deployer

Deploy static site content to GitHub Pages or any git-backed host.

## When to Use

- **GitHub Pages updates** — You have a local build/output directory and want to push it to a `username.github.io` repo or a Pages branch (`gh-pages`, `main`)
- **Static site deployment** — Hugo, Jekyll, Gatsby, Docusaurus, or any static site with a git-hosted output
- **Automated CI replacement** — Instead of setting up GitHub Actions, you want a one-command deploy from your machine
- **Syncing local → remote** — You edit content locally and need to push changes to a hosted git repository

## Workflow

```
Local Site Directory → /tmp/clone → File Copy → Commit → Force Push → Done
```

1. **Clone or init** — If the remote repo exists, clone it to `/tmp/{reponame}`. Otherwise initialize a fresh clone
2. **Copy files** — Sync your local site directory contents into the clone (clean copy, not append)
3. **Commit** — Stage all files, commit with auto-generated timestamp message
4. **Force push** — Push to remote with force flag to overwrite remote state
5. **Report** — Output success/failure with commit hash and push result

## Usage

### Via skill invocation (from agent)

Provide the following arguments:
- `site_path` — Absolute path to the local site directory (the content to deploy)
- `remote_url` — Full git URL (e.g., `https://github.com/user/repo.git` or `git@github.com:user/repo.git`)
- `branch` — Branch to deploy to (default: `main`)

### Via script directly

```bash
./scripts/deploy.sh /path/to/site git@github.com:user/repo.git [branch]
```

## Output

- **Success** — Shows commit hash, remote URL, branch, and push status
- **Failure** — Shows error message with exit code and which step failed

## Requirements

- `git` must be installed and configured with credentials for the remote
- SSH key or HTTPS token auth must be set up for the remote repository
- Site path must exist and contain files

## Notes

- Uses `--force` push — this will overwrite remote state. Use with caution on shared branches
- Clone happens in `/tmp` and is not cleaned up automatically (intentional: allows inspection)
- Commit message format: `Deploy: YYYY-MM-DD HH:MM:SS UTC`
