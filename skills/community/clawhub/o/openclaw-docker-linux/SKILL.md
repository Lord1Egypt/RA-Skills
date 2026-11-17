---






name: openclaw-docker-linux
description: "Run OpenClaw inside Docker on Linux with Tailscale remote access. ⚠️ Involves sudo, Docker, Tailscale, and credential mounting — review security section before use. Complete setup guide covering installation, configuration, and critical gotchas. Trigger phrases: docker openclaw, openclaw in docker, setup openclaw docker, tailscale openclaw, docker-compose openclaw."
metadata: {"clawdbot":{"emoji":"\ud83d\udc0b","requires":{"bins":["docker","docker-compose"],"env":["ANTHROPIC_API_KEY","OPENCLAW_GATEWAY_TOKEN"]},"os":["linux"],"homepage":"https://clawhub.com/djc00p/openclaw-docker-linux","version":"1.0.16"},"version":"1.0.16"}
---







# OpenClaw Docker Setup

## ⚠️ Security Considerations

This skill involves elevated privileges and credential management. Review before running:

- **sudo operations** — All Docker setup commands require elevated trust. Review `references/docker-setup.sh` before executing.
- **Tailscale remote access** — Enables network access to your OpenClaw instance. Ensure your Tailscale network policy allows this and review your firewall rules.
- **Credential mounting** — Mounting `~/.config/gh` or other credential directories into containers exposes them to the container image. Only do this if you fully trust the image source.
- **Host file exposure** — Volume mounts give containers access to host files. Be careful which directories you mount and which containers you run.
- **Port 18789 exposure** — Do not expose port 18789 to the public internet. Bind to localhost (127.0.0.1) unless you have explicit firewall rules protecting it. For remote access, use Tailscale (see `references/docker-config.md`).
- **Token safety** — The management script never prints the gateway token. It shows only the first 4 characters as a confirmation marker; the full token is not written to terminal output, logs, or the displayed URL. Read the real value from `.env` when you need it.
- **Bind mode** — The shipped `docker-compose.yml` binds the gateway to `127.0.0.1`. Keep it that way. Do not bind to `0.0.0.0` to make remote access work; use Tailscale Serve or MagicDNS instead. The host-level global-install path in `references/troubleshooting.md` is optional, explicitly gated, and binds to `loopback` rather than `lan`.
- **Image pinning** — Use specific version tags (e.g., `ghcr.io/openclaw/openclaw:v1.2.3`) instead of `:latest` for reproducible builds. The latest tag can change between container restarts. Pin the digest too (`tag@sha256:...`) and verify it against the registry before deploying — an unverified digest placeholder tells you nothing. See `references/docker-config.md` for the verification command.
- **Docker group is a lasting root grant** — `sudo usermod -aG docker $USER` gives your user permanent, passwordless root-equivalent access to the host through the Docker socket. Any process that can talk to that socket can start a privileged container and mount the host filesystem. Only add it if you trust every process running as your user, and remove it (`sudo gpasswd -d $USER docker`) if you no longer use Docker.

Run OpenClaw inside Docker on Linux (Ubuntu 24.04+) with Tailscale for remote access.

## Quick Start

1. **Install Docker via APT** (not Snap):
   ```bash
   sudo apt install docker.io docker-compose && \
   sudo usermod -aG docker $USER
   ```
   Then log out and back in — `sudo usermod` doesn't take effect with `newgrp`.

   ⚠️ **This is a permanent root-equivalent grant.** Membership in the `docker`
   group is equivalent to passwordless sudo, because the Docker socket lets
   any member start a privileged container that mounts the host filesystem.
   Only do this if you trust every process that runs as your user. See
   `references/gotchas.md` for how to verify or remove it.

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
   Access at `http://localhost:18789` — read the token from `.env` with
   `grep OPENCLAW_GATEWAY_TOKEN .env` when you need to authenticate.

## Key Concepts

- **bind: lan vs loopback** — `lan` = accessible from the host via port mapping; `loopback` = locked inside container.
- **Tailscale on host, not container** — Run Tailscale on the Ubuntu host for remote access.
- **One method only** — Docker OR global install, never both (port + config conflicts).
- **Config path mapping** — Host `~/.openclaw/` → Container `/home/node/.openclaw/` (same files, different paths).
- **Docker group login** — `sudo usermod -aG docker` requires full logout/login, not `newgrp`.


## References

- `references/common-usage.md` — Day-to-day commands
- `references/docker-config.md` — docker-compose.yml, .env template, permissions, Tailscale, management script
- `references/quickstart.md` — Simple 5-minute setup guide
- `references/docker-setup.sh` — Management script (start/stop/logs/doctor/tailscale/approve_telegram)
- `references/gotchas.md` — Critical mistakes and how to avoid them
- `references/troubleshooting.md` — Common errors and fixes
