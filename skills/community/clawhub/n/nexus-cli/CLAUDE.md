# Admirarr — Project Instructions

## Overview

Admirarr is a Go CLI for managing a Jellyfin + *Arr media server stack from the terminal. Built for both humans and AI agents. Cobra + Charm.sh for terminal UX, JSON output on every command for agent consumption.

Two roles:
1. **Universal *Arr ecosystem tool** — detects and interacts with services via HTTP APIs regardless of deployment method (Docker, native, remote)
2. **Stack management** — setup wizard, Docker Compose generation, cross-service wiring

## Architecture

- **Go 1.24+**, 4 runtime deps: cobra, viper, lipgloss, huh
- **Config**: Viper loads `~/.config/admirarr/config.yaml`
- **Service Registry**: `internal/config/registry.go` — all services with port, API version, key source, tier, category
- **API pattern**: `api.GetJSON(service, endpoint, params, &target)` — HTTP + auth injection
- **Key auto-discovery**: `docker exec` reads container config files, manual fallback
- **Media server abstraction**: `internal/media/` — `MediaServer` interface (Jellyfin, Plex)

## Project Structure

```
main.go                        # cmd.Execute()
cmd/                           # 26 commands + subcommands (thin Cobra wrappers)
internal/skills/               # Shared business logic (CLI + agents consume these)
internal/api/                  # HTTP client with registry-driven auth injection
internal/config/               # Viper config + service registry
internal/keys/                 # API key auto-discovery
internal/media/                # Media server abstraction (Jellyfin, Plex)
internal/arr/                  # *Arr service client
internal/qbit/                 # qBittorrent client
internal/seerr/                # Seerr client
internal/setup/                # Interactive setup wizard (12 phases, 0-11)
internal/doctor/               # Diagnostic engine (15 categories, 34 checks) + AI fix dispatch
internal/wire/                 # Cross-service wiring (Prowlarr, download clients, Gluetun)
internal/deploy/               # On-demand Docker service deployment
internal/migrate/              # Docker Compose generation
internal/recyclarr/            # Recyclarr integration
internal/ui/                   # Lip Gloss styles, formatting, banner, JSON output
.claude/agents/                # Claude Code agent definitions (doctor-fix, fleet-status, content-search)
.claude/skills/plex-stack/     # Claude Code skill for stack management
```

## Agent Integration

The CLI is agent-optimized by design:

- **JSON output** (`-o json`) on every read command — agents parse structured data
- **`doctor --fix`** (`internal/doctor/fix.go`) — two-tier repair: built-in fixes first, then dispatches to detected AI agent (Claude Code, OpenCode, Aider, Goose) with full diagnostic context
- **Claude Code agents** (`.claude/agents/`): `doctor-fix` (Sonnet, 20 turns), `fleet-status` (Haiku, 10 turns), `content-search` (Haiku, 15 turns)
- **Claude Code skill** (`.claude/skills/plex-stack/SKILL.md`): user-invocable `/plex-stack [status|doctor|search|downloads|fix]`
- **Auto-rebuild hook** (`.claude/settings.json`): rebuilds binary on `.go` file edits

## Build and Test

```bash
go build -ldflags "-X github.com/maxtechera/admirarr/internal/ui.Version=1.0.0" -o admirarr .
go test ./...
```

## Distribution

GoReleaser builds for linux/darwin/windows (amd64/arm64). Tag `v*` on main triggers release.

Channels: GitHub Releases, Homebrew (`maxtechera/tap`), Scoop (`maxtechera/scoop-bucket`), Docker (`ghcr.io/maxtechera/admirarr`), Snap Store, AUR (`admirarr-bin`).

## Services

**Core**: Jellyfin, Radarr, Sonarr, Prowlarr, qBittorrent, Gluetun, Seerr, Bazarr, FlareSolverr, Watchtower
**Optional**: Plex, Lidarr, Readarr, Whisparr, SABnzbd, Autobrr, Unpackerr, Recyclarr, Profilarr, Tdarr, Tautulli, Jellystat, Notifiarr, Maintainerr

## Brand

- **Name**: Admirarr (admiral + arr)
- **Tagline**: "Command your fleet."
- **Colors**: Navy (#0A1628), Gold (#D4A843), Cyan (#00BCD4)
- **Anchor**: ⚓

## Data Structure (TRaSH Guides)

```
/data/
  torrents/{movies,tv,music,books}/
  usenet/{movies,tv,music,books}/
  media/{movies,tv,music,books}/
```
