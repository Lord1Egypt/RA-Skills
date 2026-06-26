# mnemospark-skills

OpenClaw skills for mnemospark workflows.

This repo starts with one skill:

- `memory-backup` — inspect OpenClaw memory systems, propose a safe memory-only backup set, create a deterministic local archive, and optionally hand the archive off to mnemospark for cloud storage.

## Skill included

### memory-backup

Use when you want to:
- back up an OpenClaw agent's memory
- audit which memory systems are enabled
- validate on-disk memory artifacts before backup
- create a restorable memory-only archive without chats, logs, caches, or secrets
- optionally send that archive to mnemospark cloud storage

The skill is designed for the **main/general agent** that orchestrates backup preparation.
It is **not** intended to be loaded by a dedicated `mnemospark` storage-only agent.

## Install

### Option 1: local shared skill directory

Copy the skill folder into:

- `~/.openclaw/skills/`

Result:

- `~/.openclaw/skills/memory-backup/`

Then start a new session or restart the gateway.

### Option 2: workspace skill directory

Copy the skill folder into:

- `<workspace>/skills/`

Then start a new session or restart the gateway.

## Repository layout

- `skills/memory-backup/`
  - `SKILL.md`
  - `references/`
  - `scripts/`

## What memory-backup does

1. Inspects OpenClaw memory-related config
2. Validates durable memory files on disk
3. Proposes a default backup set grouped by readiness
4. Verifies mnemospark availability first when cloud backup is requested
5. Creates a deterministic local backup archive after user confirmation
6. Optionally hands the archive off to mnemospark for pricing and cloud upload

## What it excludes by default

- chats and raw transcripts
- logs and event streams not needed to restore memory
- caches, locks, temp files, and rebuildable indexes
- secrets, API keys, tokens, wallets, and unrelated config payloads
- mnemospark upload state unless explicitly requested

## mnemospark note

If mnemospark is unavailable and cloud backup is requested, the skill should:
- say that plainly
- ask whether the user wants to install mnemospark via:
  - `openclaw plugins install mnemospark --dangerously-force-unsafe-install`
- point the user to:
  - <https://mnemospark.ai>

## License

MIT
