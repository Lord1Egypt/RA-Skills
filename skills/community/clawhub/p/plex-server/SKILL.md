---
name: "Plex Server"
description: "Manage Plex Media Server with optional Nvidia Shield ADB device management."
allowed-tools: ["exec"]
user-invocable: true
---

# Plex Media Server Manager

Primary focus: Plex Media Server management via HTTP API. Optional: Nvidia Shield device management via ADB.

## Onboarding

### Step 1: Get your Plex token

1. Open Plex Web (app.plex.tv), play any media
2. Click "⋯" → "Get Info" → "View XML"
3. In the URL, find `X-Plex-Token=...` — that's your token

### Step 2: Discover your servers

```bash
node scripts/shield-cli.js discover <plex_token>
```

Lists all Plex servers on your account with name, version, platform, and local URL.

### Step 3: Configure

```bash
# Plex only (auto-discovers first server)
node scripts/shield-cli.js setup <plex_token>

# Pick a specific server (if you have multiple)
node scripts/shield-cli.js setup <plex_token> 0    # first server
node scripts/shield-cli.js setup <plex_token> 1    # second server

# Plex + Shield ADB
node scripts/shield-cli.js setup <plex_token> 0 192.168.70.2
```

No username/password needed — the Plex token is the universal key. The script calls `plex.tv/api/resources` to auto-discover IP and port.

Config stored at `~/.openclaw/shield/config.json` (chmod 600).

## Commands

### Plex (no ADB needed)

| Command | Args | Notes |
|---------|------|-------|
| `discover` | `<token>` | List all Plex servers on account |
| `setup` | `<token> [idx] [shield_ip]` | Auto-discover + configure |
| `plex-status` | — | Server version, platform |
| `search` | `<query>` | Search with full metadata |
| `format` | — | Pipe search JSON → readable text |
| `sessions` | — | Active streams |
| `libraries` | — | Library sections with IDs |
| `scan` | `<section_id>` | Refresh a library |
| `recently-added` | — | Last 20 additions |
| `updater-status` | — | Plex update availability |
| `health` | — | Plex status + sessions (+ ADB if configured) |

### Shield ADB (requires shield_ip)

| Command | Notes |
|---------|-------|
| `connect` | ADB connect |
| `adb-health` | Uptime, memory, disk, battery |
| `reboot` | Reboot Shield |
| `restart-plex` | Force stop + start Plex app |

## Search + Format Pipeline

```bash
node scripts/shield-cli.js search "query" | node scripts/shield-cli.js format
```

Produces channel-agnostic formatted output with emoji, suitable for Discord, WhatsApp, Telegram, etc.

## Search Output Fields

- **Basic:** title, year, type, source (local/streaming), library, summary
- **Genres:** genre tags from Plex metadata
- **Quality:** resolution (4k/1080p/720p), video codec, bitrate, container, file size
- **Audio:** codec, channels, language per track
- **Subtitles:** codec, language per track
- **Meta:** duration, studio, content rating, view count

## Gotchas

- Plex token = full server admin access. Config file is chmod 600.
- No login/password needed — the token is the universal key for all Plex API calls.
- Multiple servers? Use `discover` to list them, then `setup <token> <index>` to pick.
- Shield on Wi-Fi may change IP. Use DHCP reservation for ADB.
- Always pipe search through `format` for user-facing output.
- ADB features are optional — Plex-only setup works without Shield/ADB.
