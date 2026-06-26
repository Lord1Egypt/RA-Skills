---
name: gog-sync
description: Sync GOG game library, save files, and custom configs across devices
version: 1.1.0
tags: ['gog', 'gaming', 'sync', 'backup', 'config']
metadata:
  {
    "openclaw":
      {
        "emoji": "🎮",
        "requires": { "bins": ["rsync"] },
      },
  }
---

# gog-sync

Automate syncing of your GOG game library, save files, and custom configs across devices.

## Commands

| Command | Description |
|---|---|
| `sync` | Sync full GOG library + saves |
| `sync-saves` | Sync only save files |
| `sync-config` | Sync game custom configs (mods, keybinds, settings) |
| `list-games` | List installed GOG games |

## Config Sync

`sync-config` uses environment variables for paths:

- `GOG_CONFIG_DIR` — local config directory (default: `~/Games/GOG/config`)
- `GOG_CONFIG_REMOTE` — remote rsync destination (default: `user@remote:/backups/gog/config`)

Synced file types: `.ini`, `.cfg`, `.json`, `.xml`, `.bind`

## Dependencies

- `rsync` (required)
- `gogrepo` (optional, for library sync)
