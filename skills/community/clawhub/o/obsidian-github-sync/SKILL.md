---
name: obsidian-github-sync
description: |
  Automated GitHub synchronization for Obsidian vault with conflict detection and notification.
  
  Use when the user wants to:
  - Sync their Obsidian vault to a GitHub repository
  - Set up automatic daily synchronization
  - Handle git conflicts in Obsidian vault
  - Configure git-based backup for Obsidian notes
  
  Triggers on phrases like: "sync obsidian", "obsidian github", "vault backup", 
  "sync my notes", "setup obsidian git sync"
---

# Obsidian GitHub Sync

Automated synchronization of Obsidian vault with GitHub repository using git with conflict detection.

## Features

- **Automatic sync**: `git pull --rebase` → commit → push
- **Conflict detection**: Detects and flags merge conflicts
- **Configurable**: Environment variable based configuration
- **Notification**: Optional conflict notifications
- **Safe**: Uses rebase to maintain clean history

## Quick Start

### 1. Set Environment Variables

```bash
export OBSIDIAN_VAULT_DIR="/path/to/your/obsidian-vault"
export GITHUB_REMOTE_URL="git@github.com:username/repo.git"
```

### 2. Run Initial Sync

```bash
./scripts/obsidian-sync.sh
```

### 3. Setup Auto-sync (Cron)

```bash
# Daily at 3 AM
0 3 * * * /path/to/scripts/obsidian-sync.sh

# Check conflicts at 9 AM
0 9 * * * /path/to/scripts/check-conflict.sh
```

## Scripts

### obsidian-sync.sh

Main synchronization script. Located at `scripts/obsidian-sync.sh`.

**What it does:**
1. Checks for uncommitted changes and commits them
2. Pulls from GitHub with `--rebase`
3. Pushes to GitHub
4. Creates conflict flag if rebase fails

**Environment Variables:**
- `OBSIDIAN_VAULT_DIR` (required): Path to Obsidian vault
- `GITHUB_REMOTE_URL` (required): GitHub repository URL
- `GIT_USER_NAME` (optional): Git user name
- `GIT_USER_EMAIL` (optional): Git user email
- `SYNC_LOG_FILE` (optional): Log file path (default: `/tmp/obsidian-sync.log`)
- `CONFLICT_FLAG_FILE` (optional): Conflict flag path (default: `/tmp/obsidian-sync-conflict.flag`)

### check-conflict.sh

Conflict checking script. Located at `scripts/check-conflict.sh`.

**What it does:**
- Checks if conflict flag file exists
- Outputs conflict details if found
- Returns exit code 1 on conflict, 0 on clean state

## Workflow

### Normal Sync Flow

```
User modifies notes in Obsidian
        ↓
Cron runs obsidian-sync.sh at 3 AM
        ↓
Auto-commit local changes
        ↓
git pull --rebase origin master
        ↓
git push origin master
        ↓
Sync complete ✓
```

### Conflict Flow

```
Sync runs
    ↓
pull --rebase fails (remote has divergent changes)
    ↓
Create conflict flag file
    ↓
Exit with error
    ↓
Morning check-conflict.sh detects flag
    ↓
Notify user
    ↓
User resolves conflicts manually
    ↓
Re-run sync
```

## Handling Conflicts

When conflicts occur:

1. Check conflict flag file location (default: `/tmp/obsidian-sync-conflict.flag`)
2. Navigate to vault directory
3. Resolve conflicts using standard git workflow:

```bash
cd $OBSIDIAN_VAULT_DIR
git status                    # See conflicted files
# Edit files to resolve conflicts
git add -A                    # Stage resolved files
git rebase --continue         # Complete rebase
git push origin master        # Push resolved state
```

## Configuration Reference

See [references/setup-guide.md](references/setup-guide.md) for detailed setup instructions including:
- SSH key configuration
- Multi-device sync best practices
- Troubleshooting guide
- Cron setup examples

## Integration Examples

### With OpenClaw

```bash
# Add sync cron job
openclaw cron add --name "obsidian-sync" \
  --cron "0 3 * * *" \
  --command "/path/to/obsidian-sync.sh"

# Add conflict check
openclaw cron add --name "obsidian-check" \
  --cron "0 9 * * *" \
  --command "/path/to/check-conflict.sh"
```

### With Systemd (Linux)

Create `~/.config/systemd/user/obsidian-sync.service`:

```ini
[Unit]
Description=Obsidian Vault Git Sync

[Service]
Type=oneshot
Environment="OBSIDIAN_VAULT_DIR=/path/to/vault"
Environment="GITHUB_REMOTE_URL=git@github.com:user/repo.git"
ExecStart=/path/to/obsidian-sync.sh
```

Create `~/.config/systemd/user/obsidian-sync.timer`:

```ini
[Unit]
Description=Run Obsidian sync daily at 3 AM

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable:
```bash
systemctl --user daemon-reload
systemctl --user enable obsidian-sync.timer
systemctl --user start obsidian-sync.timer
```

## Best Practices

1. **Close Obsidian** during sync to avoid file lock issues
2. **Commit regularly** in Obsidian to reduce conflict chances
3. **Sync before switching devices**
4. **Use `.gitignore`** to exclude Obsidian's cache files:

```gitignore
# Obsidian
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/plugins/*/data.json
.trash/
```

## License

MIT
