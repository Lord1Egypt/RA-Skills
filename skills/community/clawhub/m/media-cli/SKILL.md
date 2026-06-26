---
name: media-cli
version: 1.0.0
description: "Single-file bash CLI for the *arr media stack with SSH remote support. For agents running on a different machine than the media services (e.g., VPS agent managing a home server). Tunnels API calls through existing SSH config so services stay on localhost and are never exposed. If your agent and services are on the same machine, use media-cli-local instead."
tags:
  - media
  - sonarr
  - radarr
  - plex
  - jellyfin
  - torrents
  - automation
  - homelab
  - arr
category: tools
---

# media-cli — Terminal Control for Your *arr Media Stack (Remote)

One bash script to manage your entire media automation stack from a remote machine. Search, add, download, and monitor movies and TV shows without touching a web UI.

Built for setups where the AI agent runs on a different host than the media services (e.g., a VPS running OpenClaw managing a home server's *arr stack). If everything runs on the same machine, use [media-cli-local](https://clawhub.com/solomonneas/media-cli-local) instead.

**Source:** https://github.com/solomonneas/media-cli

**Install:** Clone the repo and run the install script, or copy the `media` file to your PATH manually. See the GitHub README for details.

## Supported Services

| Service | Required | What It Does |
|---------|----------|-------------|
| Sonarr | Yes | TV show management |
| Radarr | Yes | Movie management |
| Prowlarr | Yes | Indexer management |
| qBittorrent | Yes | Download monitoring |
| Bazarr | Optional | Subtitles |
| Jellyseerr | Optional | User requests + trending |
| Tdarr | Optional | Transcode monitoring |

## Setup

```bash
# Install (clone and review the script first)
git clone https://github.com/solomonneas/media-cli.git
cd media-cli
bash install.sh

# Configure (interactive wizard)
media setup

# Test
media status
```

The setup wizard asks for API URLs and keys, saves to `~/.config/media-cli/config` (chmod 600).

## Commands

### Movies
```bash
media movies search "Interstellar"    # Search online
media movies add "Interstellar"       # Add + start downloading
media movies list                     # Library with download status
media movies missing                  # Monitored without files
media movies remove "title"           # Remove (keeps files)
```

### TV Shows
```bash
media shows search "Breaking Bad"     # Search online
media shows add "Breaking Bad"        # Add + search episodes
media shows list                      # Library with episode counts
```

### Downloads
```bash
media downloads                       # All torrents by state
media downloads active                # Active with speed + ETA
media downloads pause <hash|all>
media downloads resume <hash|all>
media downloads remove <hash> [true]  # true = delete files too
```

### Status & Monitoring
```bash
media status                          # Health + library counts + active downloads
media queue                           # Sonarr/Radarr download queues
media wanted                          # Missing episodes + movies
media calendar 14                     # Upcoming releases (next N days)
media history                         # Recent activity
media refresh                         # Trigger library rescan
media indexers                        # Prowlarr indexer status
```

### Subtitles (Bazarr)
```bash
media subs                            # Wanted subtitles
media subs history                    # Recent subtitle downloads
```

### Requests (Jellyseerr)
```bash
media requests                        # Pending user requests
media requests trending               # What's trending
media requests users                  # User list with request counts
```

### Transcoding (Tdarr)
```bash
media tdarr                           # Status + active workers
media tdarr workers                   # Per-file progress: %, fps, ETA
media tdarr queue                     # Items queued for processing
```

## Connection Modes

### Local (services on same machine)
```
MEDIA_HOST="local"
```

### Remote via SSH (services on another host)
```
MEDIA_HOST="ssh:hyperv-host"       # Uses SSH config alias
MEDIA_HOST_OS="linux"          # or "windows"
```

SSH mode tunnels all API calls through your existing SSH config. Services stay on localhost and are never exposed to the network. No additional ports or credentials needed beyond your normal SSH access. Windows hosts automatically use PowerShell's `Invoke-RestMethod` for POST requests.

## AI Agent Integration

Commands are designed for easy parsing by AI agents. Any tool that can run shell commands works:

```
"What shows am I missing episodes for?"  →  media wanted
"Add Succession"                         →  media shows add "Succession"
"What's downloading right now?"          →  media downloads active
"Pause all downloads"                    →  media downloads pause all
```

Works with OpenClaw, LangChain, Claude computer use, or any agent framework with shell execution.

## Requirements

- bash 4.0+
- curl
- python3 (standard library only, no pip)
- ssh (only for remote mode)

## Technical Details

- Single bash script (~900 lines)
- Talks to *arr v3 APIs (Sonarr/Radarr), v1 (Prowlarr), v2 (qBittorrent WebUI)
- Python3 used strictly for JSON parsing (standard library)
- No telemetry, no analytics, no network calls except to your own services
- Config stored at `~/.config/media-cli/config` with chmod 600
