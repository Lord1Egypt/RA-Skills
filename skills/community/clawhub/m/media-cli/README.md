# media-cli

Single-file bash CLI for the *arr media stack. Manage Sonarr, Radarr, Prowlarr, qBittorrent, Bazarr, Jellyseerr, and Tdarr from the terminal. Works locally or over SSH to remote hosts (including Windows).

## Install

```bash
git clone https://github.com/solomonneas/media-cli.git
cd media-cli
cp media ~/bin/media && chmod +x ~/bin/media
media setup
```

## Highlights

- **One script, no dependencies** (just bash, curl, python3)
- **SSH remote mode** for headless servers. Services stay on localhost, CLI tunnels through SSH
- **Windows support** via PowerShell Invoke-RestMethod over SSH
- **AI-friendly** output designed for agent parsing
- **7 services** managed from one command

## Source

https://github.com/solomonneas/media-cli

## Tags

media, sonarr, radarr, plex, jellyfin, torrents, automation, homelab, arr
