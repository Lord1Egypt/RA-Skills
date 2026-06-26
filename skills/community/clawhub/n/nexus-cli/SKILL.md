---
name: admirarr
description: Manage a Jellyfin/Plex + *Arr media server stack — check status, add content, monitor downloads, diagnose issues, restart services. Use this when the user asks about their media server, downloads, movies, TV shows, or streaming setup.
---

# Admirarr

CLI for self-hosted media server stacks. One binary, 20+ services, JSON output everywhere.

## Commands

### Status & Diagnostics

| Command | Description |
|---------|-------------|
| `admirarr status [-o json] [--live]` | Fleet dashboard — services, libraries, queues, disk |
| `admirarr health [-o json]` | Health warnings from Radarr, Sonarr, Prowlarr |
| `admirarr disk [-o json]` | Disk space breakdown |
| `admirarr docker [-o json]` | Docker container status |
| `admirarr doctor [-o json]` | 15 diagnostic categories, 34 checks |
| `admirarr doctor --fix` | Built-in fixes → AI agent for the rest |

### Library

| Command | Description |
|---------|-------------|
| `admirarr movies [-o json]` | Movie library with file status |
| `admirarr shows [-o json]` | TV shows with episode counts |
| `admirarr recent [-o json]` | Recently added (Jellyfin or Plex) |
| `admirarr history [-o json]` | Watch history |
| `admirarr missing [-o json]` | Monitored without files |
| `admirarr requests [-o json]` | Seerr media requests |

### Search & Add

| Command | Description |
|---------|-------------|
| `admirarr search <query> [-o json]` | Search all Prowlarr indexers |
| `admirarr find <query> [-o json]` | Search Radarr releases |
| `admirarr add-movie <query>` | Interactive: search → pick → add to Radarr |
| `admirarr add-show <query>` | Interactive: search → pick → add to Sonarr |

### Downloads

| Command | Description |
|---------|-------------|
| `admirarr downloads [-o json]` | Active qBittorrent torrents |
| `admirarr downloads pause [hash\|all]` | Pause torrents |
| `admirarr downloads resume [hash\|all]` | Resume torrents |
| `admirarr downloads remove <hash> [--delete-files]` | Remove a torrent |
| `admirarr queue [-o json]` | Radarr + Sonarr import queues |

### Indexers

| Command | Description |
|---------|-------------|
| `admirarr indexers [-o json]` | Prowlarr indexer status |
| `admirarr indexers setup` | Interactive indexer wizard |
| `admirarr indexers add <name>` | Add an indexer |
| `admirarr indexers remove <name>` | Remove an indexer |
| `admirarr indexers test` | Test all indexer connectivity |
| `admirarr indexers sync` | Sync indexers to config.yaml |

### Quality Profiles

| Command | Description |
|---------|-------------|
| `admirarr recyclarr` | Recyclarr status |
| `admirarr recyclarr sync [instance]` | Run Recyclarr sync |
| `admirarr recyclarr verify` | Check quality profiles |
| `admirarr recyclarr instances` | List configured instances |

### Management

| Command | Description |
|---------|-------------|
| `admirarr scan` | Trigger media server library scan |
| `admirarr restart <service>` | Restart a Docker container |
| `admirarr logs <service>` | Recent logs |
| `admirarr setup` | Full setup wizard (12 phases) |
| `admirarr migrate` | Generate Docker Compose stack |

## Services

**Default stack:** Jellyfin, Radarr, Sonarr, Prowlarr, qBittorrent, Gluetun, Seerr, Bazarr, FlareSolverr, Watchtower

**Optional:** Plex, Lidarr, Readarr, Whisparr, SABnzbd, Autobrr, Unpackerr, Recyclarr, Profilarr, Tdarr, Tautulli, Jellystat, Notifiarr, Maintainerr

Auto-detects media server (Jellyfin first, then Plex). Services detected via HTTP regardless of deployment method.

## Agent Integration

**Claude Code agents** in `.claude/agents/`: `doctor-fix` (Sonnet), `fleet-status` (Haiku), `content-search` (Haiku)

**Claude Code skill** `/plex-stack` — dispatches by argument: status, doctor, fix, search, downloads

**`doctor --fix`** — detects installed agents (Claude Code, OpenCode, Aider, Goose), runs built-in fixes first, then dispatches remaining issues to the agent with full diagnostic context

**JSON output** (`-o json`) on every read command — agents parse structured data, never scrape terminal output

## Config

`~/.config/admirarr/config.yaml` — service URLs, API keys (auto-discovered from Docker containers), quality profiles, indexer config.
