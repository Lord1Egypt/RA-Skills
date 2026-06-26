# Muster — Troubleshooting

---

## Setup Issues

### Docker Not Found
**Linux:** `curl -fsSL https://get.docker.com | sh && sudo usermod -aG docker $USER`
**macOS:** `brew install --cask docker` → open Docker Desktop → accept license.

### Port in Use
install.sh auto-detects and increments. To change after install: edit `~/muster/.env` → `PORT=3001` → `pm2 restart muster`. Update `MUSTER_ENDPOINT` in OpenClaw config.

### PostgreSQL Won't Start
**Homebrew (macOS default):** `brew services restart postgresql@16` then `pg_isready`. Reset: `dropdb muster && createdb muster && npx drizzle-kit migrate` (destroys data).
**Docker:** `cd ~/muster && docker compose ps` then `docker compose logs db`. Reset: `docker compose down -v && docker compose up -d && npx drizzle-kit migrate` (destroys data).

### .env Missing
```bash
cat > ~/muster/.env << EOF
MUSTER_DB_URL=postgresql://muster:muster@localhost:5432/muster
PORT=3000
EOF
```

### npm Install Fails
Check `node --version` (≥ 20). Try: `cd ~/muster && rm -rf node_modules package-lock.json && npm install`

---

## Connection Issues

### connect.sh: "needs_identity"
Provide `--name`, `--title`, `--slug` or ensure your soul.md has a name in the first heading or a `Name:` field.

### connect.sh: 409 Conflict
Slug already registered. Use a different `--slug`, or connect with `--key` using the existing agent's API key.

### Can't Reach MCP Endpoint
`pm2 status` → `curl -s http://localhost:3000/api/health`. Check `MUSTER_ENDPOINT` ends in `/mcp`. Check tunnel: `pm2 logs muster-tunnel`.

### 401 Unauthorized
Keys start with `sk-muster-`. May have been regenerated in the UI. Check OpenClaw config matches.

### AGENT_NOT_FOUND
Run `connect.sh` — you haven't registered yet.

### HEARTBEAT.md Not Updated
connect.sh appends the Muster checklist. Check if `HEARTBEAT_MUSTER.md` exists in the skill directory. Manually append it: `cat {baseDir}/HEARTBEAT_MUSTER.md >> ~/.openclaw/workspace/HEARTBEAT.md`

### Agent Not Calling Muster Heartbeat
Check `~/.openclaw/workspace/HEARTBEAT.md` has the "Muster check-in" section. If missing, re-run `connect.sh` or append `HEARTBEAT_MUSTER.md` manually. Also verify OpenClaw's heartbeat interval is enabled (default 30 min).

---

## Task Issues

### Task Stuck in `in_progress`
Crashed mid-task. On next heartbeat, Muster returns it. Resume or call `update_status` → `failed` with explanation.

### INVALID_TRANSITION
Allowed: `queued`→`in_progress`→`done`|`failed`|`pending_review`→`done`|`failed`.

### When to Use `pending_review`
Only when oversight is configured for that task type. Otherwise `done`.

---

## Service Issues

### launchd (macOS)

**Not Running:**
`launchctl list com.bai.muster` — check exit status. Restart: `launchctl kickstart -k "gui/$(id -u)/com.bai.muster"`.

**Keeps Crashing:**
Check logs: `tail -50 ~/muster/logs/launchd-stderr.log`. Common: PostgreSQL down, port conflict, bad build, missing `.env`.

**Service Not Loaded:**
`launchctl bootstrap "gui/$(id -u)" ~/Library/LaunchAgents/com.bai.muster.plist`

### pm2 (Linux/fallback)

**Not Running After Reboot:**
`pm2 resurrect`. If empty: restart manually, `pm2 save`, re-run `pm2 startup`.

**Keeps Crashing:**
`pm2 logs muster --lines 50`. Common: PostgreSQL down, port conflict, bad build, missing `.env`.

---

## Tunnel Issues

### URL Changed After Restart
Expected behavior for quick tunnels.
**macOS:** `grep -o 'https://[^ ]*trycloudflare.com' ~/muster/logs/tunnel-stderr.log | tail -1`
**pm2:** `pm2 logs muster-tunnel --lines 20 --nostream | grep -o 'https://[^ ]*trycloudflare.com'`
Update `~/.muster/tunnel.json`, notify human.

### Tunnel Down
**macOS:** `launchctl kickstart -k "gui/$(id -u)/com.bai.muster-tunnel"`. Check `tail -50 ~/muster/logs/tunnel-stderr.log`.
**pm2:** `pm2 restart muster-tunnel`. Check `pm2 logs muster-tunnel --lines 50`.

### Custom Domain Token Permissions (Settings)
Custom Token with: Account → Cloudflare Tunnel → Edit, Zone → DNS → Edit.

---

## Update Issues

### Major Version Detected
Don't auto-update. Notify human, share changelog, wait for confirmation. See UPDATE.md.

### Update Failed
update.sh auto-rolls back. Check JSON report. Create a task to investigate.

### Skill Version Mismatch
`clawhub update muster`. Start new session.

---

## Future: Machine Migration
Not yet supported. Workaround: `uninstall.sh --export DIR` → fresh install on new machine → import database dump.
