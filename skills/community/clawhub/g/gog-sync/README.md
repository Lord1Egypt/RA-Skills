# gog-sync ClawHub Skill
Automate syncing of your GOG game library, save files, and custom configs across devices.

## Features
- Sync full game library with GOG servers
- Backup save files to remote storage
- **Sync game custom configs** (mods, keybinds, settings files like .ini/.cfg/.json/.xml/.bind)
- List all installed GOG games
- Integrates with tmux workflows for quick access

## Installation
```bash
clawhub install gog-sync
```

## Usage
```bash
clawhub run gog-sync sync          # Full library sync
clawhub run gog-sync sync-saves    # Save files only
clawhub run gog-sync sync-config   # Custom game configs
clawhub run gog-sync list-games    # List installed games
```

### Config Sync Details
`sync-config` backs up game-specific configuration files to a remote destination.

| Variable | Default | Description |
|---|---|---|
| `GOG_CONFIG_DIR` | `~/Games/GOG/config` | Local config directory |
| `GOG_CONFIG_REMOTE` | `user@remote:/backups/gog/config` | Remote rsync destination |

Supported file types: `.ini`, `.cfg`, `.json`, `.xml`, `.bind`

## Changelog

### v1.1.0
- Added `sync-config` command for game custom config sync
- Configurable paths via `GOG_CONFIG_DIR` / `GOG_CONFIG_REMOTE` env vars
- Selective rsync filters for common config file types

### v1.0.0
- Initial release: library sync, save sync, game listing

## Related
- Obsidian note: [[GOG Library Management]]
- Tmux workflow: [[TMUX Workflows for Game Modding]]