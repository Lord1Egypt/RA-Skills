# Diagnosis Checklist — OpenClaw Gateway Linux

Run these checks in order to locate the issue.

## Quick full check (one command)

```bash
echo "=== Service status ===" && \
  systemctl --user status openclaw-gateway --no-pager | grep -E "Loaded|Active"
echo "=== Unit env vars ===" && \
  grep -E "XDG_RUNTIME|DBUS" ~/.config/systemd/user/openclaw-gateway.service \
  || echo "MISSING — apply Issue 1 fix from SKILL.md"
echo "=== Linger ===" && \
  loginctl show-user "$(whoami)" 2>/dev/null | grep Linger
echo "=== OpenClaw status ===" && \
  openclaw status 2>/dev/null | grep "Gateway service"
```

Expected output:
```
=== Service status ===
Loaded: loaded (...; enabled; ...)
Active: active (running)
=== Unit env vars ===
Environment=XDG_RUNTIME_DIR=/run/user/0
Environment=DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/0/bus
=== Linger ===
Linger=yes
=== OpenClaw status ===
│ Gateway service │ systemd installed · enabled · running (pid ...) │
```

---

## Step-by-step

### 1. Is the service running?
```bash
systemctl --user status openclaw-gateway
```
Not running? Start it: `systemctl --user start openclaw-gateway`

### 2. Does the unit file have the required env vars?
```bash
grep -E "XDG_RUNTIME|DBUS" ~/.config/systemd/user/openclaw-gateway.service
```
Missing? → Apply **Issue 1 fix** from SKILL.md.

Check the correct UID path while you're here:
```bash
id -u              # your UID, e.g. 0 for root or 1000 for regular user
ls /run/user/      # should contain a directory named after your UID
```

### 3. Can systemctl --user reach the user bus?
```bash
systemctl --user is-enabled openclaw-gateway
```
Expected: `enabled`
Got `"Failed to connect to bus: No medium found"` → env vars missing in unit file (see Step 2).

### 4. Is linger enabled?
```bash
loginctl show-user "$(whoami)" | grep Linger
```
Expected: `Linger=yes`
Fix: `loginctl enable-linger "$(whoami)"`

### 5. Does OpenClaw see correct status?
```bash
openclaw status 2>/dev/null | grep "Gateway service"
```
Expected: `systemd installed · enabled · running (pid ...)`
