# openclaw-backup Repository Setup

## Source of Truth
- **Repository:** `https://github.com/nz365guy/openclaw-backup`
- **Branch strategy:** single `main` branch mirroring the live `/home/node/.openclaw/workspace`
- **Remote name:** `origin`
- **Visibility:** private (contains internal files + automation secrets)

## Authentication
- Personal Access Token (PAT) stored in `/home/node/.openclaw/workspace/.env.local` using the key `GITHUB_TOKEN`.
- The PAT must have `repo` and `workflow` scopes to cover backups and skill packaging.
- Rotate the token by updating `.env.local`, then run `source .env.local` (or restart the shell) before the next push.

## Safety Rules
1. **Never commit `.env.local`** — it contains the PAT. The workspace `.gitignore` already excludes it. Double-check with `git status` before every commit.
2. Treat `memory/` files as sensitive; keep the repo private and review diffs for personal data before pushing.
3. Back up only from a clean, trusted workspace. If automation modifies files, review them before running the backup script.

## Connection Test
Use this curl call to verify the token before Git operations:
```bash
source .env.local
curl -s -H "Authorization: token ${GITHUB_TOKEN}" https://api.github.com/user | jq '.login'
```
A response of `"nz365guy"` confirms the token is valid.
