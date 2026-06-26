
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
  - "18790:18789"  # Use 18790 externally
```

Then update `allowedOrigins` in `openclaw.json` to include the new port.

## WebSocket Disconnect: "1008: pairing required"

**Symptom:** Web UI loads, but immediately disconnects with WebSocket error 1008.

**Cause:** `dmPolicy: "pairing"` without proper authentication setup.

**Fix:**
> ⚠️ **Temporary only:** This opens access to ALL senders. Use only for diagnosis, then immediately restore restrictive settings.

Edit `openclaw.json`:
```json
{
  "gateway": {
    "dmPolicy": "open",
    "allowFrom": ["*"]
  }
}
```

After diagnosis, revert to:
```json
{
  "gateway": {
    "dmPolicy": "pairing",
    "allowFrom": ["YOUR_CHAT_ID"]
  }
}
```

Or provide a valid pairing token in the query string:
```text
http://localhost:18789?token=YOUR_TOKEN
```

Then reload the page.

## Can't Access via Tailscale

**Symptom:** Can reach `http://localhost:18789` locally, but `http://TAILSCALE_IP:18789` times out or refuses connection.

**Checklist:**

1. **Verify Tailscale is running on the host:**
   ```bash
   sudo tailscale status
   ```
   Should show your node in the tailnet.

2. **Get your Tailscale IP:**
   ```bash
   tailscale ip -4
   ```

3. **Check bind is `lan`:**
   ```bash
   docker-compose run --rm openclaw-cli doctor
   ```
   Look for `bind: lan` in the output.

4. **Verify port is mapped:**
   ```bash
   docker-compose ps
   ```
   Should show `0.0.0.0:18789->18789/tcp`

5. **Check firewall allows 18789:**
   ```bash
   sudo ufw status
   sudo ufw allow 18789/tcp
   ```

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
   ping TAILSCALE_IP
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
   chmod 755 ~/.openclaw
   chmod 644 ~/.openclaw/openclaw.json
   ```

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
  image: openclaw:latest
  profiles:
    - cli
  ...
```

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
Add swap:
```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

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

**Create systemd service:**
```bash
sudo tee /etc/systemd/system/openclaw.service > /dev/null << EOF
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
User=$USER
ExecStart=/usr/bin/node $(npm prefix -g)/bin/openclaw gateway --bind lan --port 18789
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
