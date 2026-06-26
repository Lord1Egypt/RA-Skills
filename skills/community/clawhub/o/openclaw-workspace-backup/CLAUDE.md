# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`workspace-backup` is an OpenClaw workspace backup skill. Backs up each configured workspace git repo to a dedicated remote branch. Runs automatically at 03:00 daily via OpenClaw cron.

## Commands

```bash
# Install
pip install -e .

# Backup all workspaces (default)
workspace
workspace --backup --force   # force push to avoid non-fast-forward errors

# Status
workspace --status
workspace --help
```

## Architecture

**Entry point:** `workspace_backup/cli.py`

- `load_env()` — merges `workspace_backup/.env` + `~/.config/workspace/.env` (user wins)
- `load_workspaces()` — extracts `WORKSPACE_<id>=<path>` entries → `[{id, workspace}]`
- `git()` — thin subprocess wrapper for all git calls
- `backup_workspace(path, branch)` — add → diff → commit → push
- `cmd_backup()` / `cmd_status()` — command handlers
- All events logged to `~/.openclaw/logs/backup.log`

## Configuration

`workspace_backup/.env` (or `~/.config/workspace/.env`):

```dotenv
WORKSPACE_main=/home/ubuntu/.openclaw/workspace
WORKSPACE_formulas=/home/ubuntu/.openclaw/workspace-formulas
```

`<id>` is used as the git branch name. See `workspace_backup/.env.example` for reference.

**Prerequisites:** SSH key for passwordless push; each workspace must be a git repo with a remote set.
