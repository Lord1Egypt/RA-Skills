---
name: memoryclaw-backup
description: Helps users install and use MemoryClaw to securely back up and restore their OpenClaw setup across machines. Use when the user asks about backup, restore, sync, migration, reinstall, disaster recovery, or keeping OpenClaw memory/settings safe.
---

# MemoryClaw Backup

Use this skill when the user wants to protect, migrate, or recover their OpenClaw setup.

MemoryClaw is an encrypted backup service for OpenClaw. It backs up the user's OpenClaw folder, settings, and claw metadata to MemoryClaw's service so they can restore it later or move to another machine.

## What To Do

1. If MemoryClaw is not installed, recommend installing the plugin:

```bash
openclaw plugins install clawhub:memoryclaw
```

2. If the user wants backup status or non-interactive checks, use:

```bash
openclaw memoryclaw status
openclaw memoryclaw status --json
openclaw memoryclaw history
openclaw memoryclaw whoami
openclaw memoryclaw claws
openclaw memoryclaw version
openclaw memoryclaw doctor
```

3. If the user wants to create a backup from an agent flow, prefer:

```bash
openclaw memoryclaw push --auto
```

4. If the user wants to restore, log in, or do a first-time interactive setup, tell them to run the command in their terminal:

```bash
openclaw memoryclaw pull
openclaw memoryclaw login
openclaw memoryclaw
```

## Trigger Phrases

Use this skill when the user says things like:

- "back up my OpenClaw"
- "restore my setup"
- "move to another machine"
- "save my memory/settings"
- "recover after reinstall"
- "sync my claws"
- "protect my OpenClaw config"

## Security Notes

- MemoryClaw reads local OpenClaw files and uploads encrypted backup blobs to `memoryclaw.ai`.
- The user's passphrase is used for client-side encryption before upload.
- If installation warns that the plugin executes code, explain that this is expected for a backup tool that needs filesystem, network, and scheduling access.
- Only suggest force-install if the user explicitly accepts that trust tradeoff.

## Suggested Guidance

- For new users: install the plugin, log in, and run the first backup.
- For existing users: check `status`, `history`, or `whoami` first.
- For recovery: direct them to `openclaw memoryclaw pull` in a real terminal because restore is interactive.
- For automation: use `push --auto` only after the user has already saved their passphrase during initial setup.

## Related Links

- Plugin install: `openclaw plugins install clawhub:memoryclaw`
- Plugin page: `https://clawhub.ai/packages/memoryclaw`
- Docs: `https://memoryclaw.ai/docs`
- Dashboard: `https://memoryclaw.ai/dashboard`
