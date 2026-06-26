---
name: openclaw-gateway-linux-fix
description: Fix and diagnose OpenClaw Gateway service issues on Linux. Use when the gateway service shows "disabled" status despite running, when `openclaw gateway status` or `openclaw status` reports incorrect service state, or when systemctl --user fails with "No medium found" or "Failed to connect to bus". The most common fix — adding XDG_RUNTIME_DIR to shell environment — does NOT work. The correct fix is adding these vars to the systemd unit file so the gateway process itself can query its own status. Also covers safe restart without self-kill and shell escalation gotchas.
---

# OpenClaw Gateway — Linux Fixes

## Issue 1: Gateway shows "disabled" despite running

**Symptom:** `openclaw status` or `openclaw gateway status` shows `disabled`, but the service is actually running.

**Root cause:** The gateway process spawns `systemctl --user is-enabled` without `XDG_RUNTIME_DIR` and `DBUS_SESSION_BUS_ADDRESS` in its environment. Without these, systemd user bus is unreachable → `"Failed to connect to bus: No medium found"`.

**⚠️ Common wrong fix:** Adding these vars to `~/.bashrc` or shell environment does NOT help — the gateway daemon doesn't inherit your shell env.

**Correct fix:** Add the vars directly to the systemd unit file:

```bash
RUNTIME_DIR="/run/user/$(id -u)"
UNIT=~/.config/systemd/user/openclaw-gateway.service

# Append env vars after [Service] line (idempotent check first)
grep -q "XDG_RUNTIME_DIR" "$UNIT" || UNIT="$UNIT" RUNTIME="$RUNTIME_DIR" python3 -c "
import re, os
unit, runtime = os.environ['UNIT'], os.environ['RUNTIME']
content = open(unit).read()
insert = '\nEnvironment=XDG_RUNTIME_DIR=' + runtime + '\nEnvironment=DBUS_SESSION_BUS_ADDRESS=unix:path=' + runtime + '/bus'
content = re.sub(r'(\[Service\])', r'\1' + insert, content, count=1)
open(unit, 'w').write(content)
print('Unit file updated.')
"

# Reload and restart safely (see Issue 2 for post-restart status check)
systemctl --user daemon-reload
nohup bash -c 'sleep 2 && systemctl --user restart openclaw-gateway' > /tmp/gw-restart.log 2>&1 &
```

Expected result: `Service: systemd (enabled)`

---

## Issue 2: Safe gateway restart

**Problem:** `openclaw gateway restart` and `systemctl --user restart openclaw-gateway` send SIGTERM to the gateway, which also **kills the entire process tree** — including the agent turn that triggered the restart. Any work scheduled after the restart command in the same process will never execute.

**Root cause:** The agent runs as a child process of the gateway. SIGTERM propagates down the tree on shutdown.

### Step 1: Schedule post-restart work via cron

Since the agent dies with the gateway, any follow-up work must be **pre-scheduled** before the restart using `openclaw cron add --at`.

The cron scheduler runs inside the gateway and fires independently once the gateway comes back up (~5–7 seconds). Schedule it ~15 seconds ahead to be safe.

```bash
AT=$(date -u +"%Y-%m-%dT%H:%M:%S+00:00" --date="+15 seconds") && \
openclaw cron add \
  --name "gw-restart-notify" \
  --at "$AT" \
  --message "Gateway was restarted. Check status: systemctl --user status openclaw-gateway --no-pager | head -4 and report back." \
  --announce \
  --to <TELEGRAM_CHAT_ID> \
  --channel telegram \
  --delete-after-run \
  --session isolated
```

### Step 2: Trigger the restart

```bash
nohup bash -c 'sleep 2 && systemctl --user restart openclaw-gateway' > /tmp/gw-restart.log 2>&1 &
```

`sleep 2` + `&` detaches the restart from the current process tree before the gateway shuts down.

⚠️ Do NOT chain status checks after this command (e.g. `&& sleep 5 && systemctl status`) — they will be killed too.

### Passing context across the restart

If the agent needs to continue a task after restart, save context to a file before restarting and reference it in the cron message:

```bash
echo "Was doing X, next step is Y, params: Z" > /tmp/restart-context.txt

AT=$(date -u +"%Y-%m-%dT%H:%M:%S+00:00" --date="+15 seconds") && \
openclaw cron add \
  --name "gw-restart-continue" \
  --at "$AT" \
  --message "Continue the task. Context is in /tmp/restart-context.txt — read it and proceed." \
  --announce \
  --to <TELEGRAM_CHAT_ID> \
  --channel telegram \
  --delete-after-run \
  --session isolated
```

The isolated agent spawned by cron will read the file and continue from where the previous agent left off.

### What does NOT work

- `sleep N && systemctl status` chained after restart — killed by SIGTERM
- `setsid` / `systemd-run` for post-restart notification — process survives but cannot reach Telegram (direct API access blocked in some regions; gateway is the only working path)
- `curl` directly to Telegram API — may time out if blocked at network level

---

## Issue 3: `openclaw gateway status` shows "disabled" in SSH session

This is a separate issue from Issue 1 — the gateway itself works fine, but your shell session lacks `XDG_RUNTIME_DIR`.

**Affected:** `sudo su` (without `-`), non-login shells, cron, `sudo openclaw`.

**Fix:** Add to `~/.bashrc` and `/etc/profile.d/openclaw-env.sh`:
```bash
export XDG_RUNTIME_DIR=/run/user/$(id -u)
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus
```

**Shell escalation cheatsheet:**

| Command | Result | Why |
|---|---|---|
| `sudo su -` | ✅ works | Full login shell, reads `.bashrc` |
| `sudo -i` | ✅ works | Login shell (if vars in `.bashrc`) |
| `sudo su` | ❌ fails | Non-login shell, env not loaded |
| `sudo openclaw` | ❌ fails | Clean env, vars stripped by sudo |

---

## Issue 4: Service not persisting after reboot

OpenClaw runs as a **user-scope** systemd service (`~/.config/systemd/user/`), not system-scope. Without linger, user services stop when the last session closes.

```bash
loginctl enable-linger $(whoami)   # persist after logout
systemctl --user enable openclaw-gateway  # auto-start on boot
```

---

See `references/diagnosis.md` for a full diagnostic checklist.
