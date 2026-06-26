---
name: openclaw-backup-skill
description: Run and schedule local OpenClaw backup operations with a bundled Bash script. Use when the user wants to create, prune, or automate local OpenClaw backups, inspect retention behavior, or manage backup retention windows.
---

# OpenClaw Backup Skill

Use the bundled script `scripts/openclaw-backup.sh` for real operations. Do not rewrite backup logic inline when the bundled script already covers the task.

## When to use

Use this skill when the user wants to:
- create a local OpenClaw backup;
- create a manual backup before risky changes;
- prune old regular backups;
- schedule recurring backup runs;
- inspect or adjust retention behavior.

## Preconditions

This skill assumes:
- Linux;
- Bash 4+;
- OpenClaw CLI installed and working;
- local filesystem access.

## Primary commands

- Show the current CLI contract directly from the script:
  - `scripts/openclaw-backup.sh --help`
- Regular backup:
  - `scripts/openclaw-backup.sh --backup`
- Manual backup:
  - `scripts/openclaw-backup.sh --manual`
- Dry-run prune:
  - `scripts/openclaw-backup.sh --prune --dry-run --keep-hours 24 --keep-days 7 --keep-weeks 4`
- Automatic backup + prune:
  - `scripts/openclaw-backup.sh --auto --keep-hours 24 --keep-days 7 --keep-weeks 4`

## Recommended scheduled run

For recurring local backups, a good default pattern is:
- `scripts/openclaw-backup.sh --auto --keep-hours 24 --keep-days 7 --keep-weeks 4`

On Linux hosts, use the system scheduler (for example cron) when the goal is a direct local script run without chat delivery.

## Operational notes

The current backup format includes:
- workspace contents, including assistant identity and continuity files (for example SOUL.md, USER.md, AGENTS.md, and other workspace-level context files);
- OpenClaw config;
- cron export and human-readable cron summary;
- software versions;
- restore instructions;
- manifest.

The current backup format intentionally excludes:
- backup storage inside a workspace (legacy support);
- temp artifacts;
- environment variables / system env / system override.

- Regular archives are subject to prune; manual archives are excluded from normal prune.
- Retention is based on UTC timestamps encoded in archive filenames, not on `mtime` / `ctime`.
- The script resolves the OpenClaw workspace/config automatically unless the caller passes an explicit output directory.
- If the user wants recurring backups, ask before installing or changing scheduled jobs.
- For the full behavior contract, retention model, and archive naming rules, read `references/spec.md`.
