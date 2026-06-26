---
name: openclaw-docker-setup
description: "Run OpenClaw inside Docker on Linux with Tailscale remote access. ⚠️ Involves sudo, Docker, Tailscale, and credential mounting — review security section before use. Complete setup guide covering installation, configuration, and critical gotchas. Trigger phrases: docker openclaw, openclaw in docker, setup openclaw docker, tailscale openclaw, docker-compose openclaw."
metadata: {"clawdbot":{"emoji":"🐋","requires":{"bins":["docker","docker-compose"]},"env":["ANTHROPIC_API_KEY","OPENCLAW_GATEWAY_TOKEN"],"os":["linux"],"homepage":"https://clawhub.com/djc00p/openclaw-docker-linux"},"version":"1.0.7"}
---

# OpenClaw Docker Setup

## ⚠️ Security Considerations

This skill involves elevated privileges and credential management. Review before running:

- **sudo operations** — All Docker setup commands require elevated trust. Review `references/docker-setup.sh` before executing.
- **Tailscale remote access** — Enables network access to your OpenClaw instance. Ensure your Tailscale network policy allows this and review your firewall rules.
- **Credential mounting** — Mounting `~/.config/gh` or other credential directories into containers exposes them to the container image. Only do this if you fully trust the image source.
- **Host file exposure** — Volume mounts give containers access to host files. Be careful which directories you mount and which containers you run.
- **Port 18789 exposure** — Do not expose port 18789 to the public internet. Bind to localhost (127.0.0.1) unless you have explicit firewall rules protecting it. For remote access, use Tailscale (see `references/docker-config.md`).
- **Token safety** — The management script no longer prints full gateway tokens in terminal output. Tokens are masked to show only the first 4 characters.
- **Image pinning** — Use specific version tags (e.g., `ghcr.io/openclaw/openclaw:v1.2.3`) instead of `:latest` for reproducible builds. The latest tag can change between container restarts.

Run OpenClaw inside Docker on Linux (Ubuntu 24.04+) with Tailscale for remote access.

## Quick Start

1. **Install Docker via APT** (not Snap):
   ```bash
   sudo apt install docker.io docker-compose && \
   sudo usermod -aG docker $USER
   ```
   Then log out and back in — `sudo usermod` doesn't take effect with `newgrp`.

2. **Run onboard** to configure gateway and get your token:
   ```bash
   docker-compose run --rm openclaw-cli onboard
   ```

3. **Create `docker-compose.yml`** using the token from onboard.
   See `references/docker-config.md` for the full template and .env setup.

4. **Start the container:**
   ```bash
   docker-compose up -d
   ```
   Access at `http://localhost:18789?token=YOUR_TOKEN`

## Key Concepts

- **bind: lan vs loopback** — `lan` = accessible from the host via port mapping; `loopback` = locked inside container.
- **Tailscale on host, not container** — Run Tailscale on the Ubuntu host for remote access.
- **One method only** — Docker OR global install, never both (port + config conflicts).
- **Config path mapping** — Host `~/.openclaw/` → Container `/home/node/.openclaw/` (same files, different paths).
- **Docker group login** — `sudo usermod -aG docker` requires full logout/login, not `newgrp`.

## Common Usage

**Generate a secure token:**
```bash
openssl rand -hex 32
```

**View container logs:**
```bash
docker-compose logs -f openclaw
```

**Run CLI commands inside container:**
```bash
docker-compose run --rm openclaw-cli COMMAND_HERE
```

**Fix volume permissions (Linux):**
```bash
sudo chown -R 1000:1000 ~/.openclaw ~/openclaw
```

**Approve Telegram pairing:**
```bash
docker-compose run --rm openclaw-cli pairing approve telegram YOUR_CODE
```

**Access via Tailscale (recommended — HTTPS):**
```bash
sudo apt install tailscale
sudo tailscale up
./docker-setup.sh tailscale  # Starts tailscale serve on port 18789
```
Then visit `https://YOUR_MACHINE_NAME.YOUR_TAILNET.ts.net?token=YOUR_TOKEN` from any device on your tailnet. Use MagicDNS hostname over raw IP — it's HTTPS by default and more stable.

## References

- `references/docker-config.md` — docker-compose.yml, .env template, permissions, Tailscale, management script
- `references/quickstart.md` — Simple 5-minute setup guide
- `references/docker-setup.sh` — Management script (start/stop/logs/doctor/tailscale/approve_telegram)
- `references/gotchas.md` — Critical mistakes and how to avoid them
- `references/troubleshooting.md` — Common errors and fixes
