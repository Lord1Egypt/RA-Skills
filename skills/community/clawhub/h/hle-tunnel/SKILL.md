---
name: hle-tunnel
description: Access your AI agent's web UI from anywhere and share it securely — automatic HTTPS, SSO access control, no VPN or port forwarding needed.
version: 1.2.0
emoji: "\U0001F310"
homepage: https://hle.world/docs/integrations/openclaw
user-invocable: true
skillKey: hle
metadata:
  openclaw:
    requires:
      anyBins:
        - hle
        - pipx
        - pip
      env:
        - HLE_API_KEY
    install:
      - kind: brew
        formula: hle-world/tap/hle-client
        bins: [hle]
      - kind: uv
        package: hle-client
        bins: [hle]
---

# HLE Tunnel

Access your agent's web UI from anywhere and share it with others — secure remote access with automatic HTTPS and SSO, powered by [HLE (Home Lab Everywhere)](https://hle.world).

## When to use

Use this skill when the user wants to:
- Access their agent's Control UI (port 18789) remotely — from a phone, laptop, or another network
- Share their agent UI with a friend or collaborator via SSO (Google, GitHub)
- Expose any local service the agent manages — Home Assistant, Grafana, Portainer, Jupyter, dev servers
- Manage tunnel access control (SSO, PIN, share links, basic auth)

Do **not** use this skill for general networking, port forwarding within a LAN, or VPN setup.

## Setup

Before exposing services, the user needs an HLE account and API key:

1. Sign up at https://hle.world and create an API key in the dashboard
2. Run `hle auth login` to save the key (opens browser), or set the `HLE_API_KEY` environment variable

Check auth status with `hle auth status`.

## Usage

### Access your agent UI remotely

```bash
# Expose the Control UI so you can access it from anywhere
hle expose --service http://localhost:18789 --label my-agent

# Share access with a collaborator via SSO
hle expose --service http://localhost:18789 --label my-agent \
  --allow friend@gmail.com

# Allow multiple people
hle expose --service http://localhost:18789 --label my-agent \
  --allow teammate1@company.com --allow teammate2@company.com
```

The command runs in the foreground and prints the public URL (e.g. `https://my-agent-x7k.hle.world`). Anyone you `--allow` can log in via Google or GitHub SSO — no account sharing needed.

### Expose services your agent manages

```bash
# Home Assistant
hle expose --service http://localhost:8123 --label ha \
  --allow you@gmail.com

# Grafana dashboard — share with your team
hle expose --service http://localhost:3000 --label grafana \
  --allow dev1@company.com --allow dev2@company.com

# Dev server — share with a client for a demo
hle expose --service http://localhost:3000 --label dev \
  --allow client@company.com

# Jupyter notebook — share with a colleague
hle expose --service http://localhost:8888 --label notebook \
  --allow colleague@company.com
```

### List active tunnels

```bash
hle tunnels
```

### Access control

```bash
# Allow a specific email to access a tunnel via SSO
hle access add my-agent-x7k friend@example.com

# Set a PIN for quick access
hle pin set my-agent-x7k

# Create a temporary share link (expires in 24h by default)
hle share create my-agent-x7k --duration 1h --max-uses 5

# Set HTTP Basic Auth
hle basic-auth set my-agent-x7k
```

### Common options for `hle expose`

| Flag | Description |
|------|-------------|
| `--service URL` | Local service URL (required) |
| `--label NAME` | Subdomain label (e.g. `my-agent` -> `my-agent-x7k.hle.world`) |
| `--auth sso\|none` | Auth mode (default: `sso`) |
| `--allow EMAIL` | Allow email for SSO access (repeatable) |
| `--websocket/--no-websocket` | WebSocket proxying (default: on) |
| `--verify-ssl` | Verify local service SSL cert |
| `--upstream-basic-auth USER:PASS` | Inject Basic Auth to upstream |
| `--forward-host` | Forward browser Host header to local service |

## Run with Docker

If Docker is available, you can run HLE as a container instead of installing the CLI.

### Headless (tunnels only, no UI)

```bash
docker run -d \
  --name hle \
  -e HLE_API_KEY=your_key_here \
  -v hle-data:/data \
  ghcr.io/hle-world/hle-docker:headless

# Expose your agent's Control UI running on the Docker host
docker exec hle hle expose \
  --service http://host.docker.internal:18789 \
  --label my-agent \
  --allow you@gmail.com
```

### With Web UI

```bash
docker run -d \
  --name hle \
  -p 8099:8099 \
  -e HLE_API_KEY=your_key_here \
  -v hle-data:/data \
  ghcr.io/hle-world/hle-docker:latest
```

Open `http://localhost:8099` to manage tunnels from a browser.

### Docker Compose

```yaml
services:
  hle:
    image: ghcr.io/hle-world/hle-docker:headless
    restart: unless-stopped
    volumes:
      - hle-data:/data
    environment:
      - HLE_API_KEY=your_key_here

volumes:
  hle-data:
```

## Important notes

- The `hle expose` command runs in the foreground. To run as a background service, use `nohup`, `tmux`, `screen`, or a process manager.
- Self-signed certificates on local services are accepted by default (no `--verify-ssl` needed).
- The public URL format is `https://<label>-<user_code>.hle.world`.
- By default, only you (the account owner) can access the tunnel. Use `--allow` to grant access to others via SSO.
- API key can be set via `--api-key` flag, `HLE_API_KEY` env var, or `~/.config/hle/config.toml`.

## Installation

If `hle` is not installed:

```bash
# Homebrew (macOS/Linux)
brew install hle-world/tap/hle-client

# pip/pipx
pipx install hle-client
# or: pip install hle-client
```
