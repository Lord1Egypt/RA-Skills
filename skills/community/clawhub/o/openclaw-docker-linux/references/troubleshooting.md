
# Troubleshooting

Common errors and how to fix them.

## Container Won't Start

**Symptom:** `docker-compose up -d` returns immediately or container exits.

**Check logs:**
```bash
docker-compose logs openclaw
```

**Common causes:**
- `gateway.mode` not set to `"local"` — see `references/gotchas.md`
- Invalid API key in `.env` — regenerate or verify `ANTHROPIC_API_KEY`
- Port 18789 already in use — see "Port Conflict" below
- Out of memory — add a 4GB swapfile (see `references/gotchas.md`)

**Fix:**
```bash
# View full logs
docker-compose logs -f openclaw

# Restart with fresh logs
docker-compose down
docker-compose up -d
docker-compose logs -f openclaw
```

## Port Conflict on 18789

**Symptom:** "Address already in use" or `bind: permission denied` when starting.

**Check what's using the port:**
```bash
sudo lsof -i :18789
```

**If another OpenClaw is running:**
```bash
# Stop global version
sudo systemctl stop openclaw

# Or kill the process
sudo kill -9 PID
```

**If something else is using 18789:**
Either stop that service or change the port in `docker-compose.yml`:
```yaml
ports:
  - "127.0.0.1:18790:18789"  # Use 18790 externally, bound to loopback only
```

Keep the `127.0.0.1:` prefix. Without it, Docker publishes the port on every
host interface, exposing the gateway to anyone who can reach the machine on
your network. For remote access, use Tailscale Serve rather than opening the
port (see the Tailscale section below).

Then update `allowedOrigins` in `openclaw.json` to include the new port.

## WebSocket Disconnect: "1008: pairing required"

**Symptom:** Web UI loads, but immediately disconnects with WebSocket error 1008.

**Cause:** `dmPolicy: "pairing"` without proper authentication setup.

**Fix:**

Do **not** open the gateway to all senders. `"dmPolicy": "open"` with
`"allowFrom": ["*"]` removes the only thing standing between the gateway and
whoever can reach the port. Fix the pairing instead.

**1. Check the pairing state first:**

```bash
docker-compose exec openclaw openclaw pairing list
docker-compose logs openclaw | grep -i pair
```

**2. Use a pairing token in the URL.** This authorizes your browser without
changing who else may talk to the gateway:

```text
http://localhost:18789?token=YOUR_TOKEN
```

**3. Pair explicitly, then keep the restrictive policy.** Get a pairing code
from the gateway and approve it from the trusted client:

```bash
docker-compose exec openclaw openclaw pairing start
# approve the code from your trusted client, then:
docker-compose exec openclaw openclaw pairing approve <CODE>
```

Your configuration should stay restrictive:

```json
{
  "gateway": {
    "dmPolicy": "pairing",
    "allowFrom": ["YOUR_CHAT_ID"]
  }
}
```

**4. If the pairing code itself is failing**, the problem is usually that the
token in the URL is expired, that the clock in the container is wrong, or that
the origin is not in `allowedOrigins`. Check those before changing access
control:

```bash
docker-compose exec openclaw date -u          # clock skew breaks token expiry
docker-compose exec openclaw openclaw health  # confirm the gateway is live
```

Never widen `allowFrom` to `["*"]` as a diagnostic step. Pair the client.

## Can't Access via Tailscale

**Symptom:** Can reach `http://localhost:18789` locally, but the Tailscale Serve URL (`https://<host>.tailnet.ts.net`) times out or refuses connection.

**Also check for a stale Serve route.** A Serve route keeps forwarding even
after the container stops, so a leftover route points at a port that is no
longer serving the gateway — and a later process binding that port would
become remotely reachable. Check and remove it explicitly:

```bash
# What is currently being served?
tailscale serve status

# Remove the route for this target (the trailing "off" is required)
tailscale serve --bg http://localhost:18789 off

# Confirm it is gone
tailscale serve status
```

`./docker-setup.sh stop` does this for you and tells you if it could not
remove the route, rather than reporting success unconditionally.

**Checklist:**

1. **Verify Tailscale is running on the host:**
   ```bash
   sudo tailscale status
   ```
   Should show your node in the tailnet.

2. **Get your Tailscale IP:**
   ```bash
   tailscale serve status
   ```

3. **Check bind is `lan`:**
   ```bash
   docker-compose run --rm openclaw-cli doctor
   ```
   Look for `bind: lan` in the output.

4. **Verify port is mapped to localhost:**
   ```bash
   docker-compose ps
   ```
   Should show `127.0.0.1:18789->18789/tcp`.

   If it shows `0.0.0.0:18789->18789/tcp`, the container is reachable from every
   network interface. Fix the mapping in `docker-compose.yml` first:
   ```yaml
   ports:
     - "127.0.0.1:18789:18789"
   ```
   Then recreate the container: `docker-compose down && docker-compose up -d`.

   Use Tailscale Serve or MagicDNS for remote access instead of binding to all
   interfaces. Do not bind to `0.0.0.0` to make remote access work.

5. **Check firewall allows 18789 from localhost only:**
   ```bash
   sudo ufw status
   ```

   If you need the port reachable, restrict the rule to loopback rather than
   opening it to every source:
   ```bash
   sudo ufw allow from 127.0.0.1 to any port 18789 proto tcp
   ```

   Never use a bare `sudo ufw allow 18789/tcp` — it accepts traffic from every
   network your host is attached to. Remote access should go through Tailscale,
   not an open firewall port.

6. **Add Tailscale IP to allowedOrigins:**
   ```json
   {
     "gateway": {
       "allowedOrigins": [
         "http://localhost:18789",
         "http://100.x.x.x:18789"
       ]
     }
   }
   ```

7. **Ping the host from a remote device:**
   ```bash
   tailscale ping $(hostname)   # confirm this host is on your tailnet
   ```
   If unreachable, check your tailnet settings in Tailscale console.

## Permission Denied on Volume Mount

**Symptom:** Container starts but logs show "permission denied" when accessing `~/.openclaw/`.

**Cause:** Docker group not active or volume mount permissions issue.

**Fix:**

1. **Verify docker group is active:**
   ```bash
   groups $USER
   ```
   Should list `docker`.

   If not, log out and back in after running:
   ```bash
   sudo usermod -aG docker $USER
   ```

2. **Check volume mount:**
   ```bash
   docker-compose run --rm openclaw-cli ls -la /home/node/.openclaw/
   ```

3. **Fix permissions on host:**
   ```bash
   chmod 700 ~/.openclaw
   chmod 600 ~/.openclaw/openclaw.json
   ```

   Keep these private. `755` on the directory and `644` on the config let
   every local user read your gateway token, model API keys, and session
   data. The container runs as its own uid — if it cannot read the files,
   fix the ownership with `sudo chown -R "$(id -u):$(id -g)" ~/.openclaw`
   instead of widening the permissions.

## gateway.mode Not Set (Won't Start)

**Symptom:** Container runs, but gateway doesn't respond; `docker logs` shows nothing about the gateway.

**Check config:**
```bash
docker-compose run --rm openclaw-cli cat /home/node/.openclaw/openclaw.json | grep -A5 gateway
```

**If `mode` is missing or not `"local"`:**
```bash
docker-compose run --rm openclaw-cli doctor --fix
```

This auto-sets `gateway.mode` to `"local"`.

## Can't Run CLI Commands (docker-compose run fails)

**Symptom:** `docker-compose run --rm openclaw-cli onboard` fails with "no such service" or "profile error".

**Fix:**
Ensure `openclaw-cli` service has `profiles: ["cli"]` in `docker-compose.yml`:
```yaml
openclaw-cli:
  image: ghcr.io/openclaw/openclaw:2026.10.10@sha256:REPLACE_WITH_VERIFIED_DIGEST
  profiles:
    - cli
  ...
```

Use the same pinned image and digest as the `openclaw` service in your
`docker-compose.yml` — a floating `:latest` tag can differ between the two
services and makes the setup non-reproducible. See the digest verification
steps in `references/docker-config.md`.

Then run with the profile flag:
```bash
docker-compose run --rm -p cli openclaw-cli onboard
```

Or without profile flag if you edited the service.

## High Memory Usage / Container Keeps Crashing

**Symptom:** Container runs for a few minutes then crashes; `docker stats` shows high memory.

**Check logs:**
```bash
docker-compose logs --tail 50 openclaw
```

**Common causes:**
- Memory leak in OpenClaw (rare)
- Docker daemon not enough RAM — check `docker ps` for other containers
- OS running low on RAM

**Temporary fix:**
Add swap. Check that `/swapfile` does not already exist and that the
filesystem has room for it before creating it:
The block below aborts on its own if `/swapfile` already exists or there is
not enough free space, so it cannot overwrite an existing swapfile:

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
`sudo swapon /swapfile` instead of recreating it. If it aborts on space,
free space first — the build will fail regardless.

**Long-term:**
Monitor with:
```bash
docker stats openclaw
```

Or reduce OpenClaw's memory limit in `docker-compose.yml`:
```yaml
openclaw:
  ...
  deploy:
    resources:
      limits:
        memory: 512M
```

## CORS Errors in Browser Console

**Symptom:** Web UI loads but API calls fail with CORS errors.

**Fix:**
Ensure your Tailscale/access IP is in `allowedOrigins`:
```json
{
  "gateway": {
    "allowedOrigins": [
      "http://localhost:18789",
      "http://100.x.x.x:18789",
      "http://192.168.1.x:18789"
    ]
  }
}
```

Then reload the browser (hard refresh: Ctrl+Shift+R or Cmd+Shift+R).

## Migrating from Global to Docker Install

**Before:**
```bash
# Stop the global version
sudo systemctl stop openclaw
sudo systemctl disable openclaw

# Check it's stopped
sudo systemctl status openclaw  # Should show "inactive"
```

**During:**
```bash
docker-compose up -d
docker-compose logs -f openclaw
```

**Verify:**
```bash
# Old install shouldn't be running
systemctl is-active openclaw  # Should output "inactive"

# New Docker version should work
curl http://localhost:18789
```

**Cleanup (optional):**
```bash
# Remove systemd service files
sudo rm /etc/systemd/system/openclaw.service
sudo systemctl daemon-reload

# Or uninstall global OpenClaw
npm uninstall -g openclaw
```

## Migrating from Docker to Global Install

**Before:**
```bash
docker-compose down
```

**Update paths in openclaw.json:**
Change `/home/node/.openclaw` references to `/home/YOUR_USERNAME/.openclaw` (your actual username).

**Install globally:**
```bash
npm install -g openclaw
```

> **Optional — only if you want a host-level global install.**
> This is **outside the primary Docker deployment scope**. The Docker path above
> runs OpenClaw in a container and needs no host service. Skip this section
> unless you specifically want OpenClaw running directly on the host, and
> understand that `systemctl enable` creates a persistent service that starts
> on boot with your user privileges.
>
> If you do continue, keep the gateway bound to localhost (`--bind loopback`,
> not `--bind lan`) and use Tailscale Serve or MagicDNS for remote access.

**Create systemd service:**
```bash
sudo tee /etc/systemd/system/openclaw.service > /dev/null << EOF
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
User=$USER
ExecStart=/usr/bin/node $(npm prefix -g)/bin/openclaw gateway --bind loopback --port 18789
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable openclaw
sudo systemctl start openclaw
sudo systemctl status openclaw
```

**Verify:**
```bash
curl http://localhost:18789
```
