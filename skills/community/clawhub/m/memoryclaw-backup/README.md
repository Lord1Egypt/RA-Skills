# memoryclaw-skill

Companion ClawHub skill for discovering and onboarding users to MemoryClaw.

## What This Repo Is

This repository contains the standalone ClawHub skill that helps users and agents:

- discover MemoryClaw through skill search
- understand when MemoryClaw is useful
- install the actual plugin package
- use safe commands for backup, status, and restore workflows

## What This Repo Is Not

This repository is **not** the executable plugin.

The installable MemoryClaw plugin lives in the separate repository:

- `ngsrv/memoryclaw`

Users install the plugin with:

```bash
openclaw plugins install clawhub:memoryclaw
```

## Relationship To `memoryclaw` Repo

The `memoryclaw` plugin repo includes a `SKILL.md` file because the plugin ships its own embedded skill/instructions.

This repo is different:

- `memoryclaw` repo: installable code plugin with packaged instructions
- `memoryclaw-skill` repo: standalone discovery skill published to ClawHub skill search

## Publish

Publish this skill with:

```bash
npx clawhub@latest publish . --slug memoryclaw-backup --name "MemoryClaw Backup" --version 1.0.0 --tags latest
```
