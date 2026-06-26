---
name: media-cli-local
version: 1.0.0
description: "Single-file bash CLI for the *arr media stack. Manage Sonarr, Radarr, Prowlarr, qBittorrent, Bazarr, Jellyseerr, and Tdarr from the terminal or via AI agents. Runs on the same machine as your services. No Docker, no Node, no Python packages."
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

# media-cli-local — Terminal Control for Your *arr Media Stack

One bash script to manage your entire media automation stack. Search, add, download, and monitor movies and TV shows without touching a web UI.

Designed for setups where the agent and media services run on the **same machine**. If your *arr stack runs on a different host, see [media-cli](https://clawhub.com/solomonneas/media-cli) which includes SSH remote support.

**Source:** https://github.com/solomonneas/media-cli

**Install:** Clone the repo and copy the script to your PATH. Review it first.

```bash
git clone https://github.com/solomonneas/media-cli.git
cd media-cli
cp media ~/bin/media && chmod +x ~/bin/media
media setup
```

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

The setup wizard asks for API URLs and keys, saves to `~/.config/media-cli/config` (chmod 600). All connections are localhost only.

```bash
media setup    # Interactive config wizard
media status   # Verify everything connects
```

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

## AI Agent Integration

Commands output clean, parseable text designed for AI agents:

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

## Technical Details

- Single bash script (~900 lines)
- All API calls go to localhost (no remote connections)
- Talks to *arr v3 APIs (Sonarr/Radarr), v1 (Prowlarr), v2 (qBittorrent WebUI)
- Python3 used strictly for JSON parsing (standard library)
- No telemetry, no analytics, no network calls except to your own services
- Config stored at `~/.config/media-cli/config` with chmod 600
