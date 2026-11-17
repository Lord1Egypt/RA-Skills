
# Critical Gotchas

> **Note:** Some of these issues may already be resolved in newer OpenClaw versions. Run `openclaw doctor --fix` first — it catches most config issues automatically. The structural/networking gotchas below are fundamental and apply regardless of version.

---

## bind: "loopback" vs "lan"

**Problem:** Container starts, but you can't access the gateway from the host machine on port 18789.

**Inside the container, you need `lan`:**
```json
{ "gateway": { "bind": "lan" } }
```

- `loopback` = only reachable from inside the container's own network namespace
- `lan` = reachable via the container's published port

**This is not the same as exposing the gateway on your network.** The two
layers are independent:

| Layer | Setting | Exposure |
|---|---|---|
| Inside the container | `gateway.bind: "lan"` | Required for Docker port publishing to work at all |
| On the host | `ports: - "127.0.0.1:18789:18789"` | **This** is what limits who can reach it |

The host-side mapping is the security boundary. With `127.0.0.1:` on the
left, only processes on the host can connect, even though the container
itself listens on all interfaces. Use Tailscale Serve for remote access
rather than changing the host mapping to `0.0.0.0`.

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
      "https://YOUR_MACHINE.tailnet.ts.net"
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

Get your serve hostname: `tailscale serve status` (it shows the `https://<host>.tailnet.ts.net` address to use)
Get your MagicDNS hostname: `tailscale status | head -1`

---

## Still applies to most versions

**Snap Docker has filesystem confinement issues** — always use APT:
```bash
sudo apt install docker.io docker-compose
```

**ARM64 vs AMD64** — Intel Macs (2012–2019) need AMD64 Ubuntu, not ARM64.

**Out of memory during build** — add a 4GB swapfile. Check first that the
path is free and there is room on disk, so you do not overwrite an existing
swapfile:
The block below aborts on its own if `/swapfile` already exists or there is
not enough free space:

```bash
# Refuses to run if /swapfile already exists or there is not enough free
# space. Each check aborts before any destructive command runs.
set -euo pipefail

SWAP_PATH=/swapfile
SWAP_PATH_DIR=/
NEEDED_GB=4

if [ -e "$SWAP_PATH" ]; then
  echo "ABORT: $SWAP_PATH already exists. Not touching it."
  echo "If it is a valid inactive swapfile, enable it with:"
  echo "  sudo swapon $SWAP_PATH"
  echo "Otherwise choose a different path and re-run."
  exit 1
fi

# Portable free-space check: df -Pk gives POSIX 1K blocks on both GNU and BSD.
AVAIL_KB=$(df -Pk "$SWAP_PATH_DIR" 2>/dev/null | awk 'NR==2 {print $4}')
if [ -z "${AVAIL_KB:-}" ]; then
  echo "ABORT: could not determine free space for $SWAP_PATH_DIR."
  echo "Check free space manually with 'df -h $SWAP_PATH_DIR', then re-run."
  exit 1
fi
AVAIL_GB=$((AVAIL_KB / 1024 / 1024))
if [ "$AVAIL_GB" -lt $((NEEDED_GB + 1)) ]; then
  echo "ABORT: only ${AVAIL_GB}GB free on $SWAP_PATH_DIR, need at least $((NEEDED_GB + 1))GB."
  echo "Free space first, then re-run."
  exit 1
fi

sudo fallocate -l ${NEEDED_GB}G "$SWAP_PATH"
sudo chmod 600 "$SWAP_PATH"
sudo mkswap "$SWAP_PATH"
sudo swapon "$SWAP_PATH"
```

If it aborts because `/swapfile` exists, enable the existing one with
`sudo swapon /swapfile` or pick a different path. If it aborts on space,
free space first; the build will fail anyway.
