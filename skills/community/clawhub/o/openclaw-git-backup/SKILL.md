---
name: openclaw-git-backup
description: Create, update, validate, or troubleshoot automated git backup workflows for OpenClaw repositories. Use when a user wants a scheduled commit-and-push backup job, wants commit messages to summarize added or modified or deleted files, needs git credential setup for HTTPS pushes, or needs to debug why an OpenClaw cron backup is not running or not pushing.
---

# OpenClaw Git Backup

Use this skill to build a reusable nightly git backup workflow for an OpenClaw repo.

What this workflow does:

- stages repo changes
- optionally excludes scheduler noise or other paths
- creates a commit only when tracked changes exist
- writes a commit subject with `+added ~modified -deleted` counts
- writes a commit body listing changed files
- still runs `git push` even if there was no new commit, so older unpushed commits are flushed
- integrates with OpenClaw cron and should always be force-run once after setup or edits

## Inputs to Confirm

Before changing anything, confirm these values:

- repo root, e.g. `<repo-root>`
- runtime script path, e.g. `<runtime-script>`
- timezone, e.g. `<timezone>`
- remote name, usually `origin`
- branch behavior: current branch or explicit branch
- exclude patterns, if any
- whether HTTPS token setup is needed

If the user already implied these values, proceed without turning it into an interview.

## Defaults

Reasonable defaults for a fresh setup:

- remote: `origin`
- timezone: `UTC`
- author name: `OpenClaw Backup`
- author email: `backup@local`
- branch: current branch, else `main` when detached
- exclude patterns: none unless the repo has scheduler self-noise

## Bundled Script

This skill includes `scripts/nightly_git_backup.sh`.

Prefer using the bundled script as the implementation source, then copy it into the runtime location the user wants the cron job to call.

Typical install step:

```bash
install -D -m 755 <skill-dir>/scripts/nightly_git_backup.sh <runtime-script>
bash -n <runtime-script>
```

## Configuration Model

The bundled script supports these env vars:

- `BACKUP_REMOTE` — default `origin`
- `BACKUP_BRANCH` — optional explicit target branch
- `BACKUP_TZ` — default `UTC`
- `BACKUP_AUTHOR_NAME` — default `OpenClaw Backup`
- `BACKUP_AUTHOR_EMAIL` — default `backup@local`
- `BACKUP_EXCLUDES` — comma-separated git pathspec exclude patterns, e.g. `cron,cron/**,.cache,.cache/**`

The first positional argument is the repo path. If omitted, the script uses `BACKUP_REPO` or the current directory.

## Recommended Flow

### 1. Inspect current state

Check:

- `git -C <repo-root> rev-parse --show-toplevel`
- `git -C <repo-root> status --short --branch`
- `git -C <repo-root> remote -v`
- `openclaw cron list` or equivalent cron listing

### 2. Install or update the runtime script

Copy the bundled script into the runtime path the cron job will execute.

### 3. Configure push auth only if needed

If HTTPS push is already working, leave auth alone.

If the user explicitly provides a GitHub HTTPS token, prefer repo-local credential storage instead of embedding credentials in the remote URL:

```bash
git -C <repo-root> config credential.helper 'store --file=<repo-root>/.git/credentials'
git -C <repo-root> config credential.useHttpPath true
printf 'protocol=https\nhost=github.com\npath=OWNER/REPO.git\nusername=x-access-token\npassword=TOKEN\n' | git -C <repo-root> credential approve
chmod 600 <repo-root>/.git/credentials
git -C <repo-root> ls-remote --heads <remote> <branch>
```

Rules:

- never write the token into the remote URL
- never store the real token inside this skill
- tighten credential file permissions to `600`

### 4. Create or update the cron job

Read `references/cron-job-template.md`.

Set the job so it executes:

```bash
bash -lc '<runtime-script> <repo-root>'
```

Typical cron settings:

- isolated agentTurn
- low thinking
- timeout 600s
- silent delivery unless the user wants alerts

### 5. Force-run once immediately

Do not stop at “job created”. Always test the full path.

After force-run, check:

- latest commit subject
- latest commit body
- `git status --short --branch`
- `git rev-list --left-right --count <remote>/<branch>...HEAD` if push is expected

## Validation Checklist

### Script

- `bash -n <runtime-script>`

### Git

- `git -C <repo-root> status --short --branch`
- `git -C <repo-root> remote -v`
- `git -C <repo-root> ls-remote --heads <remote> <branch>`

### Cron

- list jobs
- force-run the backup job
- inspect recent run results

### Expected Outcome

- if staged changes exist after exclusions, a new commit is created and pushed
- if no new changes exist, push still runs to flush older local commits
- exclude patterns prevent scheduler self-noise from generating fake backup commits

## Commit Message Contract

The bundled script writes:

### Subject

```text
backup: snapshot YYYY-MM-DD HH:MM:SS +0000 | +A ~M -D
```

### Body

```text
Added(n)
- ...

Modified(n)
- ...

Deleted(n)
- ...

Renamed(n)
- old -> new
```

Keep the body factual and file-oriented.

## Common Pitfalls

### Scheduler self-noise

Some repos contain scheduler state that changes every run. Exclude it explicitly with `BACKUP_EXCLUDES`.

Example:

```bash
BACKUP_EXCLUDES='cron,cron/**'
```

### Runtime state outside the repo

Git only backs up files inside the target repo. If a workflow also depends on directories outside the repo, they are not covered unless the user explicitly adds a second sync or mirrors them into the repo.

See `references/backup-scope.md`.

### Wrong success criteria

“Cron job exists” is not enough.

The real success condition is:

1. force-run works
2. commit format is correct
3. push succeeds
4. remote catches up

## Output Style

When reporting back, keep it concrete:

- what was configured
- what was tested
- whether push worked
- what is still outside backup scope
