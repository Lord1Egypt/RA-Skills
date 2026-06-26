---
name: openclaw-backup-restore
description: Backup and restore OpenClaw configuration, agents, sessions, and workspace to/from a private Git repository. Use when the user wants to manually trigger a backup, migrate to a new machine, or restore from a previous state.
---

# OpenClaw Backup & Restore

A specialized skill for managing the lifecycle of your OpenClaw data. This skill utilizes an external Git-managed backup directory to keep your production environment clean while ensuring full recoverability.

## Strategy

1. **Isolation**: Git operations happen in a dedicated directory outside the live `.openclaw` runtime to avoid pollution.
2. **Minimalism**: Large `node_modules`, logs, and temporary files are excluded.
3. **Redundancy**: Regular backups can be scheduled via Cron.

---

## Setup

Before using this skill, you must set your private backup repository URL in `openclaw.json`. This URL is used by the scripts to push and pull data.

```bash
openclaw config set skills.entries.openclaw-backup-restore.env.OPENCLAW_BACKUP_REPO "git@github.com:your-username/your-repo.git"
```

## How to Backup

To trigger a manual backup and sync to your remote repository:
1. The agent should execute the `backup.sh` script located within this skill's `scripts/` directory.
2. The script will:
   - Read the repo URL from the OpenClaw config.
   - Sync `${HOME}/.openclaw/` to `${HOME}/openclaw-backup/` using `rsync` (respecting `.gitignore`).
   - Generate a readable commit summary from changed paths (for example workspace/config/runtime/memory).
   - Commit and push to the remote `main` branch.

**Trigger Phrases**: "Backup OpenClaw now", "Sync my data to GitHub".

---

## How to Restore

To restore your environment on a new or existing machine:
1. Ensure your SSH key is added to your Git provider (e.g., GitHub).
2. The agent should execute the `restore.sh` script located within this skill's `scripts/` directory.
3. The process involves:
   - Reading the repo URL from the OpenClaw config.
   - Cloning or pulling the latest backup from the configured repository.
   - Syncing files back to `${HOME}/.openclaw/`.
   - Reinstalling node dependencies and running `openclaw doctor --yes` to fix environment paths.
4. **Restart the Gateway**: `openclaw gateway restart`.

**Trigger Phrases**: "Restore OpenClaw from backup", "Migrate my data".

---

## Technical Details

- **Backup Directory**: `${HOME}/openclaw-backup`
- **Source Directory**: `${HOME}/.openclaw`
- **Exclusions**: Defined in the skill's `.gitignore` (includes `node_modules/`, `logs/`, `completions/`, `tmp/`, `dist/`).
- **Automatic Setup**: The `.gitignore` file is included in this skill and will be copied to `${HOME}/openclaw-backup/` during the first backup run.

---

## Recovery Checklist

If restoring to a **completely new machine**:
1. Install OpenClaw CLI first.
2. Set the `OPENCLAW_BACKUP_REPO` config value.
3. Configure SSH access for your Git provider.
4. Run the restore script provided by this skill.
5. Run `openclaw onboard` if you need to re-install the daemon service.

 