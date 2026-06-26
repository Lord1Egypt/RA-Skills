
# Critical Gotchas

> **Note:** Some of these issues may already be resolved in newer OpenClaw versions. Run `openclaw doctor --fix` first — it catches most config issues automatically. The structural/networking gotchas below are fundamental and apply regardless of version.

---

## bind: "loopback" vs "lan"

**Problem:** Container starts, but you can't access the gateway from the host machine on port 18789.

**Wrong:**
```json
{ "gateway": { "bind": "loopback" } }
```

**Right:**
```json
{ "gateway": { "bind": "lan" } }
```

- `loopback` = only accessible inside the container
- `lan` = accessible from the host via port mapping

## Tailscale Runs on Host, Not Inside Container

**Problem:** Set up Tailscale inside the Docker container, but remote devices can't reach the gateway.

Install and run Tailscale on the Ubuntu **host**, not inside Docker:
```bash
sudo tailscale up
```

The container talks to the host's Docker network. Tailscale on the host makes the host IP available to your tailnet.

## One Install Method Only

**Problem:** Global OpenClaw installed, now running Docker version too. Port 18789 is bound twice, configs conflict.

Stop the global version first:
```bash
sudo systemctl stop openclaw
sudo systemctl disable openclaw
docker-compose up -d
```

Never run Docker and global install simultaneously on the same machine.

## Docker Group Requires Full Logout

**Problem:** Ran `sudo usermod -aG docker $USER` but still get "permission denied".

`newgrp docker` only affects the current shell. A full logout/login is required for the group to take effect system-wide.

## Config Path Mapping

Host `~/.openclaw/` maps to container `/home/node/.openclaw/` via volume mount. They're the same files — changes on the host reflect instantly in the container. If you're editing config and seeing no effect, verify the volume is mounted correctly in docker-compose.yml.

## allowedOrigins Missing Tailscale IP

**Problem:** Can access OpenClaw locally but get CORS errors via Tailscale IP.

Add your Tailscale IP to `allowedOrigins` in `openclaw.json`:
```json
{
  "gateway": {
    "allowedOrigins": [
      "http://localhost:18789",
      "http://YOUR_TAILSCALE_IP:18789"
    ]
  }
}
```

If using MagicDNS hostname (recommended), add that instead of the IP:
```json
{
  "gateway": {
    "allowedOrigins": [
      "http://localhost:18789",
      "https://YOUR_MACHINE_NAME.YOUR_TAILNET.ts.net"
    ]
  }
}
```

Get your Tailscale IP: `tailscale ip -4`
Get your MagicDNS hostname: `tailscale status | head -1`

---

## Still applies to most versions

**Snap Docker has filesystem confinement issues** — always use APT:
```bash
sudo apt install docker.io docker-compose
```

**ARM64 vs AMD64** — Intel Macs (2012–2019) need AMD64 Ubuntu, not ARM64.

**Out of memory during build** — add a 4GB swapfile:
```bash
sudo fallocate -l 4G /swapfile && \
  sudo chmod 600 /swapfile && \
  sudo mkswap /swapfile && \
  sudo swapon /swapfile
```
