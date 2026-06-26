# Backup Scope

## What a git backup covers

A git backup only covers files inside the target repository.

Typical included items:

- workspace files already tracked by git
- custom skills and overrides stored inside the repo
- runtime scripts stored inside the repo
- lockfiles or docs stored inside the repo

## What it does not cover by default

These are not backed up unless they are also inside the repo, copied into the repo, or synced separately:

- state directories outside the repo
- caches outside the repo
- local companion folders created by other skills or tools
- credentials stored outside the repo

## Common gotcha

Users often assume “the app folder” and “the runtime state folders” are the same thing. They usually are not.

When documenting a backup flow, explicitly separate:

1. code/config tracked by git
2. runtime state outside git

## Scheduler self-noise

If the scheduler writes its own state inside the repo, exclude it explicitly or the backup job may generate commits from its own bookkeeping.

Examples:

- `cron`
- `cron/**`
- `.cache`
- `.cache/**`

## Promise carefully

Do not claim “everything is backed up” unless you have verified that all required state lives inside the repo or has a second backup path.
