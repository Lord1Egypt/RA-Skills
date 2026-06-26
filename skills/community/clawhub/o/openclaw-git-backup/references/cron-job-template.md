# Cron Job Template

Use this reference when wiring the backup into OpenClaw cron.

## Fill these placeholders first

- `<repo-root>`
- `<runtime-script>`
- `<timezone>`
- `<remote>`
- `<branch>`
- `<exclude-patterns>`

Example exclude patterns:

```text
cron,cron/**
```

## Recommended env wrapper

```bash
BACKUP_REMOTE='<remote>' \
BACKUP_BRANCH='<branch>' \
BACKUP_TZ='<timezone>' \
BACKUP_AUTHOR_NAME='OpenClaw Backup' \
BACKUP_AUTHOR_EMAIL='backup@local' \
BACKUP_EXCLUDES='<exclude-patterns>' \
bash -lc '<runtime-script> <repo-root>'
```

## agentTurn message template

```text
You are running a scheduled git backup for <repo-root>. Requirements: 1) commit if there are staged changes after exclusions, 2) use the bundled backup script so the commit subject includes +added ~modified -deleted counts and the commit body lists changed files, 3) push to <remote>/<branch>, 4) still run push even if there was no new commit so older local commits are flushed, 5) do not ask the user questions. First run this exact command, then summarize the result briefly:

BACKUP_REMOTE='<remote>' BACKUP_BRANCH='<branch>' BACKUP_TZ='<timezone>' BACKUP_AUTHOR_NAME='OpenClaw Backup' BACKUP_AUTHOR_EMAIL='backup@local' BACKUP_EXCLUDES='<exclude-patterns>' bash -lc '<runtime-script> <repo-root>'
```

## Suggested cron job shape

- schedule: user preference
- sessionTarget: isolated
- delivery: none unless the user wants alerts
- timeoutSeconds: 600
- thinking: low

## Acceptance check

After add or update:

1. force-run once
2. inspect the latest commit subject and body
3. confirm push succeeded
4. confirm the repo is no longer ahead of the remote, if push was expected
