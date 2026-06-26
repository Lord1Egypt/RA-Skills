---
name: github-backup
description: Automate OpenClaw workspace backups and skill version control to the private GitHub repo `nz365guy/openclaw-backup`. Use this when staging/committing workspace changes, rotating the PAT, or running the backup script to push updates.
---

# GitHub Backup & Version Control

## Overview
Centralizes the `/home/node/.openclaw/workspace` inside the private repo `nz365guy/openclaw-backup` so every configuration file, memory note, and custom skill stays versioned. Includes a scripted backup workflow, token-handling guidance, and commit conventions for both routine snapshots and skill-specific changes.

## Quick Start Checklist
1. **Auth loaded** – `source .env.local` to expose `GITHUB_TOKEN` (repo+workflow scopes). Never commit `.env.local`.
2. **Remote sanity** – `git remote -v` should show `origin https://github.com/nz365guy/openclaw-backup.git`. If missing, run `git remote add origin ...`.
3. **Clean status review** – `git status -sb` before any backup; eyeball diffs for secrets.
4. **Reference doc** – See [`references/repo-setup.md`](references/repo-setup.md) for repo details, token rotation steps, and safety rules.

## Routine Backup Workflow
1. **Inspect changes**
   ```bash
   cd /home/node/.openclaw/workspace
   git status -sb
   git diff
   ```
2. **Run the helper script** (preferred for automation):
   ```bash
   skills/github-backup/scripts/backup_openclaw.sh "Backup: <short summary>"
   ```
   - Auto-sources `.env.local`, stages everything (respecting `.gitignore`), commits, and pushes via token-auth URL.
   - Exits early if there are no modifications.
3. **Manual fallback** (if you need bespoke staging):
   ```bash
   git add <files>
   git commit -m "<message>"
   source .env.local
   git push https://nz365guy:${GITHUB_TOKEN}@github.com/nz365guy/openclaw-backup.git main
   ```
4. **Verify on GitHub** – `gh repo view` or open the repo URL to confirm the new commit landed.

## Skill & Repo Hygiene
- **Commit messages** – Prefix with `Skill:` when touching `/skills/**`, `Config:` for workspace settings, `Memory:` for journal updates. The backup script accepts any custom message, so pass a descriptive summary when a change is more than a routine snapshot.
- **New skills** – After creating/updating a skill folder, re-run the backup workflow so the packaged assets live in GitHub alongside the rest of the workspace.
- **Token rotation** – Update `.env.local`, re-source the shell, and test with the curl snippet in [`references/repo-setup.md`](references/repo-setup.md#connection-test) before attempting the next push.
- **Sensitive files** – Keep `.env.local` and any raw secrets out of git. Expand `.gitignore` here if new secret files are introduced.

## Resources
- [`scripts/backup_openclaw.sh`](scripts/backup_openclaw.sh): one-command backup helper (stage → commit → push) that reads the PAT from `.env.local` and targets `main`.
- [`references/repo-setup.md`](references/repo-setup.md): authoritative repo/token metadata, safety guardrails, and verification commands.
