# OpenClaw Diagnostics — Symptom → Fix

## Control UI / Webchat Broken

**Symptoms:** Dashboard unreachable at `http://127.0.0.1:18789/`, blank page, websocket errors in logs

**Fix sequence:**
1. `openclaw gateway status` — is it running?
2. If not running: `openclaw gateway start`
3. If running but unresponsive: `openclaw gateway restart`
4. Check port conflict: `lsof -i :18789 | grep -v openclaw` — kill if another process owns it
5. Check logs: `openclaw logs --limit 50` for startup errors
6. If "closed before connect" warnings only (code=1005) — harmless, browser reconnecting; ignore

**Verify:** Load `http://127.0.0.1:18789/` — should respond


## Gateway Won't Start

**Symptoms:** `openclaw gateway start` fails, "EADDRINUSE", "config error", "fatal"

**Fix sequence:**
1. Check for port conflict: `lsof -i :18789`
2. Kill stale process: `pkill -f openclaw` then retry start
3. Check config: `openclaw config list 2>&1` for syntax errors
4. Check logs: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
5. Validate config file: `cat ~/.openclaw/config.json | python3 -m json.tool`

**Escalate if:** config file is corrupted (can't fix without knowing Jake's settings)


## Gateway Crashed / Keeps Restarting

**Symptoms:** Repeated SIGTERM/SIGKILL in logs, gateway restarts in loop, `pid` keeps changing in status

**Fix sequence:**
1. Check LaunchAgent: `launchctl list | grep openclaw`
2. View crash logs: `log show --predicate 'processImagePath contains "openclaw"' --last 10m`
3. Try clean restart: `openclaw gateway stop && sleep 5 && openclaw gateway start`
4. Check disk space: `df -h ~` — low disk can cause crashes
5. Check memory pressure: `vm_stat` — swap storms can kill Node processes

**Escalate if:** crash loops persist after 2 restarts


## Channel Offline (Discord / Telegram)

**Symptoms:** Channel shows `ERROR` or `disconnected` in `openclaw status`, messages not delivered

**Discord-specific:**
1. Check token: `openclaw status` shows token truncation — verify it's not blank
2. Check Discord status: `curl -s https://discordstatus.com/api/v2/status.json | python3 -m json.tool | grep status`
3. Restart gateway: `openclaw gateway restart` (reconnects all channels)
4. If "Invalid Token": token expired — escalate to Jake (needs new bot token)

**Telegram-specific:**
1. Same gateway restart approach
2. "Unauthorized" error = token invalid — escalate to Jake
3. Menu truncation warning is cosmetic — ignore

**Verify:** `openclaw status` shows channel state = `OK`


## Memory Plugin Unavailable

**Symptoms:** `memory: enabled (plugin memory-core) · unavailable` in status

**Fix sequence:**
1. This is usually a plugin load error — check: `openclaw logs --limit 50 | grep memory`
2. Restart gateway: `openclaw gateway restart`
3. If persists: check plugin config `openclaw config get plugins`

**Note:** Memory unavailable doesn't break chat — it just means I can't search indexed transcripts.


## Pairing Required / Auth Errors

**Symptoms:** `GatewayClientRequestError: pairing required`, CLI commands fail with auth errors

**Context:** This happens when CLI scope-upgrade is rejected — the CLI needs elevated operator permissions.

**Fix sequence:**
1. From Control UI, approve the pairing request if visible
2. Or: `openclaw pair --approve` (check exact command with `openclaw help`)
3. Gateway restart may clear stale pairing state: `openclaw gateway restart`

**Escalate if:** pairing UI doesn't appear or `--approve` command fails


## Sessions Broken / History Lost

**Symptoms:** Session history not loading, "chat.history" errors in logs, blank chat in UI

**Fix sequence:**
1. Check sessions file: `ls -la ~/.openclaw/agents/main/sessions/`
2. Check for JSON corruption: `python3 -m json.tool ~/.openclaw/agents/main/sessions/sessions.json`
3. Gateway restart clears in-memory session state: `openclaw gateway restart`

**Escalate if:** sessions.json is corrupted (data loss risk — don't touch without Jake's OK)


## High Memory / Slow Performance

**Symptoms:** Mac sluggish, openclaw process consuming >1GB RAM, responses very slow

**Fix sequence:**
1. Check: `ps aux | grep openclaw | awk '{print $6}' | head -5` (RSS in KB)
2. If >500MB: `openclaw gateway restart` (clears Node heap)
3. Long-running sessions accumulate context — `/reset` in UI also helps

**Note:** 200k context window sessions are memory-intensive by design.


## Heartbeat Failures

**Symptoms:** Heartbeat not firing, `openclaw status` shows heartbeat interval but no recent triggers

**Fix sequence:**
1. Verify: `openclaw status | grep Heartbeat`
2. Check cron jobs: `openclaw cron list` (if available)
3. Gateway restart resets heartbeat timer: `openclaw gateway restart`


## Log File Locations

| Log | Path |
|-----|------|
| Current day | `/tmp/openclaw/openclaw-YYYY-MM-DD.log` |
| Previous day | Same pattern, prior date |
| macOS crash | `~/Library/Logs/DiagnosticReports/` |
| LaunchAgent | `~/Library/Logs/openclaw-gateway.log` (if exists) |


## Escalation Checklist

Escalate to Jake when:
- [ ] Fix requires editing `~/.openclaw/config.json` significantly
- [ ] Credentials/tokens need to be rotated
- [ ] Session history at risk of data loss
- [ ] Issue persists after 2 restart attempts
- [ ] Gateway crashes immediately on start (not a transient issue)
