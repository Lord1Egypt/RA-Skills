---
name: myopenclaw-backup-restore
description: "Cross-platform backup and restore for OpenClaw. Works on Windows, macOS, and Linux — backups created on any OS can be restored on any other OS. Use when user wants to create a snapshot, restore from backup, migrate to a new machine, or protect against data loss. Supports dry-run preview, automatic pre-restore snapshots, gateway token preservation, credential permission hardening, and a built-in HTTP server for browser-based management. Only requires Node.js (no bash/rsync/python needed)."
metadata:
  openclaw:
    requires:
      bins: ["node"]
    trust: high
    permissions:
      - read: ~/.openclaw
      - write: ~/.openclaw
      - network: listen
---

# MyOpenClaw Backup Restore — Cross-Platform

> **Part of the [MyClaw.ai](https://myclaw.ai) open skills ecosystem.**
> Full documentation (中文): see [README.md](README.md)

## Quick Start

```bash
# Backup
node scripts/backup-restore.js backup

# List backups
node scripts/backup-restore.js list

# Restore (always dry-run first!)
node scripts/backup-restore.js restore <archive> --dry-run
node scripts/backup-restore.js restore <archive>
```

No setup, no dependencies beyond Node.js.

## What Gets Backed Up

Workspace (MEMORY.md, SOUL.md, etc.) • All workspace-* dirs (multi-agent teams) • Gateway config (tokens, API keys, channels) • Skills • Extensions • Credentials & channel pairing state • Agent config & session history • Devices • Identity • Cron jobs • Guardian scripts • ClawHub registry • Delivery queue • Memory index

**Excluded:** logs, node_modules, .git, media files, browser data, .lock/.deleted.* files.

See [references/what-gets-saved.md](references/what-gets-saved.md) for full details.

## Cross-Platform

Backups use tar.gz (native on Win10+/macOS/Linux). Auto-fallback to ZIP on older Windows. Archives from any OS restore on any OS.

## Commands

### backup

```bash
node scripts/backup-restore.js backup [--output-dir <dir>]
```

Creates `openclaw-backup_{agent}_{timestamp}.tar.gz` in `~/openclaw-backups/`. Auto-prunes (keeps last 7). On non-Windows: `chmod 600` applied.

### restore

```bash
node scripts/backup-restore.js restore <archive> [--dry-run] [--overwrite-gateway-token]
```

Safety features:
- **`--dry-run`**: Preview without changes
- **Pre-restore snapshot**: Auto-saves current state before overwriting
- **Gateway token preservation**: Keeps new server's token (prevents Control UI mismatch)
- **Interactive confirmation**: Must type `yes`
- **Credential hardening**: `chmod 700/600` on non-Windows
- **Auto-restart**: Starts gateway after restore
- **Legacy compatibility**: Handles v1 (bash) and v2 archive structures

### list

```bash
node scripts/backup-restore.js list [--backup-dir <dir>]
```

## HTTP Server

```bash
node scripts/server.js --token <secret> [--port 7373] [--backup-dir <dir>]
```

- Web UI at `http://localhost:<port>/?token=<token>`
- Remote: list, download, upload only
- Localhost: backup, restore (shell execution restricted to localhost)
- Token is mandatory — server won't start without one

## Security

Archives contain bot tokens, API keys, and credentials. Store securely. Never commit to public repos. Transfer via encrypted channels.
