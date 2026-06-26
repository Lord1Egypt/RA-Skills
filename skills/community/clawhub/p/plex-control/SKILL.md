---
name: Plex Standalone Skill
description: A standalone command-line skill to interact with and manage Plex Media Server directly, featuring playback controls and secured temporary caching.
env:
  - PLEX_URL
  - PLEX_TOKEN
---

# Plex Standalone Skill

This skill allows the OpenClaw agent to directly query and manage a Plex Media Server using a standalone Python CLI script. 

## Requirements

1. **Environment Variables**:
   - `PLEX_URL`: Your Plex server address (e.g., `http://192.168.1.100:32400`).
   - `PLEX_TOKEN`: Your private Plex authentication token.

2. **Python**:
   - The script uses `plexapi`. Dependencies are managed automatically via `uv`.

## How to Use the Skill

The agent invokes the script via the command line. The output is structured JSON.

### Command Syntax

```bash
uv run scripts/plex_cli.py <action> [arguments]
```

### Supported Actions

- **`info`**: Get basic server info.
- **`sync`**: Refresh the lightning-fast search cache (stored in the system's temporary directory).
- **`search <query>`**: Instantly search for movies, shows, episodes, actors, or genres using the local cache.
- **`clients`**: List active playback devices.
- **`play <client_name> <query_or_key>`**: Tell a device to play a specific item.
- **`pause/resume/stop <client_name>`**: Basic playback control.
- **`continue`**: List items currently in "Continue Watching".

## Security & Configuration

This skill is designed for maximum security and minimal footprint:

- **Registry Metadata**: Detailed requirements, including required environment variables (`PLEX_URL`, `PLEX_TOKEN`) and required binaries (`uv`, `python3`), are formally declared in [metadata.json](./metadata.json).
- **Environment Handling**: Credentials are injected directly into the execution environment. The skill does **not** read local `.env` files, preventing accidental credential exposure.
- **Privacy & Caching**:
  - The skill caches an index of your **library names, genres, and artist names** in the OS temporary directory for search performance.
  - **Live Metadata (sessions, usernames, playback states)** is fetched in real-time and is **never** stored or cached.
  - The cache is transient and resides in the system's temporary storage, which is automatically cleaned by the OS.
