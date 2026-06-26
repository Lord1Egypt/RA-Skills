# Known Gotchas — OpenClaw VPS Deployment

Hard-won lessons from real deployments. Each one caused a real failure.

## 1. `openclaw gateway start` ≠ `openclaw gateway`

| Command | What it does |
|---|---|
| `openclaw gateway start` | Starts the **user-level systemd service** — requires D-Bus session |
| `openclaw gateway` | Runs the gateway **directly in foreground** — what you want in a system service |

**Symptom:** `Gateway service check failed: systemctl is-enabled unavailable: $DBUS_SESSION_BUS_ADDRESS not defined`

**Fix:** Use `openclaw gateway --bind lan --port 18789 --auth token --allow-unconfigured` as ExecStart.

---

## 2. Wrong agents config schema

**Wrong (causes "Unrecognized key: default" error):**
```json
{
  "agents": {
    "default": { "name": "Koda" }
  }
}
```

**Correct:**
```json
{
  "agents": {
    "defaults": {
      "model": { "primary": "anthropic/claude-sonnet-4-6" }
    },
    "list": [
      { "id": "main", "default": true, "name": "Koda" }
    ]
  }
}
```

---

## 3. `gateway.mode` must be set

Without it: `Gateway mode is unset; gateway start will be blocked.`

Set `"mode": "remote"` in `gateway` config, or pass `--allow-unconfigured` flag.

---

## 4. `XDG_RUNTIME_DIR` missing in systemd

**Symptom:** Service starts, immediately exits with D-Bus error.

**Fix:** Add to systemd unit and create the directory:
```ini
Environment=XDG_RUNTIME_DIR=/run/user/0
```
```bash
mkdir -p /run/user/0 && chmod 700 /run/user/0
```

---

## 5. `allowedOrigins` blocks the UI

When `bind=lan`, OpenClaw seeds `allowedOrigins` to only `localhost`. Accessing via public IP returns a CORS/origin error.

**Fix:** Add public IP to config:
```json
"gateway": {
  "controlUi": {
    "allowedOrigins": [
      "http://localhost:18789",
      "http://127.0.0.1:18789",
      "http://YOUR.IP.HERE:18789"
    ]
  }
}
```

---

## 6. mcporter config path is CWD-relative

When the gateway calls `mcporter` via `execAsync`, it looks for `./config/mcporter.json` relative to the **current working directory** of the process — not `$HOME`. This means if the gateway's CWD differs from the user's shell CWD, mcporter won't find its servers.

**Fix:** Always pass `--config /absolute/path/to/mcporter.json` when calling mcporter from a subprocess.

---

## 7. paramiko auth on Hostinger VPS

Hostinger VPS instances typically disable password auth after initial setup (or set a specific root password during creation that may differ from what you specified in a failed API purchase attempt).

**Fix:** Always use key-based auth. In WSL2, the Windows SSH key is at `/mnt/c/Users/<username>/.ssh/id_ed25519`.

```python
client.connect(ip, port=port, username=user, key_filename="/tmp/vps_key")
```

Copy the key to `/tmp/vps_key` with `chmod 600` before using.

---

## 8. Performance on small VPS (KVM 1)

KVM 1 = 1 vCPU, 4GB RAM. OpenClaw runs fine but Node.js startup is slower without these:

```ini
Environment=OPENCLAW_NO_RESPAWN=1
Environment=NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
```

Always set both in the systemd unit.

---

## 9. Gateway auth token configuration

`--auth token` sets the **mode** but the token itself must be in config:
```json
"gateway": {
  "auth": {
    "mode": "token",
    "token": "your-token-here"
  }
}
```

Or generate one: `openssl rand -hex 24`

---

## 10. Build from git repo (custom fork)

If deploying a custom fork instead of the npm package:
1. Install `pnpm` first: `npm install -g pnpm`
2. Clone: `git clone --depth 1 <repo> /opt/openclaw`
3. Build: `cd /opt/openclaw && pnpm install --frozen-lockfile && pnpm build`
4. Binary is at `/opt/openclaw/dist/index.js` — symlink to `/usr/local/bin/openclaw`
