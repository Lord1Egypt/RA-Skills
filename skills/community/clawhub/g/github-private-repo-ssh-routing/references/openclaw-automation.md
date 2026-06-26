# OpenClaw + Automation Notes

Use this file when GitHub repo access is part of OpenClaw backup, restore, plugins, or automation.

## The key rule

Do not fix only the live repo remote if a script or config file is the true source of the repo URL.

## Common OpenClaw cases

### Backup/restore skill

A backup repo may have:

- the live repo remote in the clone
- a config value storing the repo URL
- a script that rewrites `origin`

Fix all three if needed.

Example config source:

```bash
openclaw config set skills.entries.openclaw-backup-restore.env.OPENCLAW_BACKUP_REPO "git@github.com-backup:OWNER/REPO.git"
```

### Plugin repo vs backup repo

Keep them separate mentally:

- plugin repo = source code / plugin changes
- backup repo = environment state / snapshots

They may need different keys, aliases, and permissions.

### Cron and unattended jobs

When a scheduled job pushes to GitHub:

- verify the repo remote
- verify the SSH alias
- verify the key permissions
- check whether the job mutates remotes on startup

### Repeated drift symptom

If a remote keeps reverting, search for:

- config values
- bootstrap scripts
- backup scripts
- install/onboard steps
- cron jobs

## Safe OpenClaw workflow

1. Inspect the current repo remote.
2. Inspect the config source that stores the repo URL.
3. Fix the SSH alias/key mapping.
4. Fix the repo remote.
5. Fix the config source.
6. Run the automation once manually.
7. Only then trust the scheduled path.
