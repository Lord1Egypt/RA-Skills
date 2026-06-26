---
name: openclaw-teleport
description: Migrate, backup, or restore an OpenClaw agent workspace to/from a single .soul file. Use when the user wants to move an agent to a new machine, back up their workspace, restore from a backup, or mentions teleport, migration, pack, unpack, .soul files, or "搬家". Wraps the npm package @kagura-agent/openclaw-teleport.
---

# openclaw-teleport

One-command agent migration: pack identity, memory, config, credentials, cron jobs, and workspace into a single `.soul` archive, then unpack on a new machine for full restoration.

## Install

```bash
npm install -g @kagura-agent/openclaw-teleport
```

Or use `npx` without installing:

```bash
npx @kagura-agent/openclaw-teleport pack
```

## Commands

### Pack (export)

```bash
# Pack the default (first) agent
openclaw-teleport pack

# Pack a specific agent by name
openclaw-teleport pack kagura
```

Produces a `<name>_<date>.soul` file (tar.gz) containing:
- Full workspace (identity files, memory, skills, workflows, databases — excluding git repo subdirectories)
- Agent config + channel credentials from `openclaw.json`
- Cron job definitions
- GitHub repo list (re-cloned on unpack)

### Unpack (import/restore)

```bash
# Restore to default workspace (~/.openclaw/workspace)
openclaw-teleport unpack kagura_20260320.soul

# Restore to a custom workspace
openclaw-teleport unpack kagura_20260320.soul --workspace /path/to/workspace
```

Unpack automatically:
1. Installs OpenClaw if missing
2. Restores workspace files
3. Writes config + credentials to `openclaw.json`
4. Restores cron jobs
5. Clones GitHub repos via `gh`
6. Starts the gateway
7. Prints a welcome summary

### Inspect

```bash
openclaw-teleport inspect kagura_20260320.soul
```

Shows manifest metadata without unpacking: agent name, pack date, file count, repos, channels, cron jobs.

## Security

⚠️ `.soul` files contain **plaintext credentials** (API tokens, bot tokens, app secrets). Treat them like password files:
- Never commit to git or share publicly
- Transfer via encrypted channels (SSH, encrypted USB)
- Delete after unpacking
- Optionally encrypt with `gpg -c agent.soul`

## When to Use

- **Moving to a new machine** — pack on old, unpack on new
- **Backup** — periodic `pack` to save current state
- **Disaster recovery** — `unpack` from a saved `.soul` file
- **Cloning an agent setup** — share a `.soul` file (minus secrets) as a template
