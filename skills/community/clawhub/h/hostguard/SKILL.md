---
name: claw-guard
description: Check whether OpenClaw is listening beyond localhost or running with elevated privileges, then offer a conservative lockdown fix. 检查OpenClaw安全配置。
version: 1.1.0
license: MIT-0
metadata: {"openclaw": {"emoji": "🛡️", "requires": {"bins": [], "env": []}}}
---

# ClawGuard

Security assistant for OpenClaw. Check whether the local OpenClaw service is reachable beyond localhost and whether it is running with elevated privileges.

## Features

- 🔒 **Network Binding Check**: Detect if OpenClaw is exposed beyond localhost
- 🔐 **Privilege Check**: Detect if running with elevated privileges (root/admin)
- 📋 **Configuration Analysis**: Review host/port settings in env files
- 🔧 **Conservative Fix**: Offer safe lockdown recommendations

## Trigger Conditions

- "Check OpenClaw security" / "检查OpenClaw安全"
- "Is OpenClaw exposed?" / "OpenClaw是否暴露?"
- "Check if running as root" / "检查是否以root运行"
- "Lockdown OpenClaw" / "锁定OpenClaw"
- "claw-guard"

---

## Quick Check Commands

### Check Network Binding (macOS/Linux)

```bash
# Find OpenClaw process and check binding
PORT=${OPENCLAW_PORT:-18789}
echo "Checking port $PORT..."
lsof -i :$PORT -P -n 2>/dev/null | grep LISTEN || echo "No listener on port $PORT"
```

### Check Privilege

```bash
# Check if running as root
if [ "$(id -u)" = "0" ]; then
  echo "⚠️ Running as root (elevated privileges)"
else
  echo "✅ Running as user $(whoami) (uid=$(id -u))"
fi
```

### Check Configuration

```bash
# Check env files for HOST setting
for f in .env.local .env.development .env.production .env; do
  if [ -f "$f" ]; then
    HOST_VAL=$(grep -E "^(OPENCLAW_HOST|HOST)=" "$f" 2>/dev/null | cut -d= -f2)
    if [ -n "$HOST_VAL" ]; then
      echo "Found HOST=$HOST_VAL in $f"
    fi
  fi
done
```

### Full Security Check

```bash
# Run all checks
echo "🛡️ ClawGuard Security Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Check user
echo ""
echo "🔐 User/Privilege:"
if [ "$(id -u)" = "0" ]; then
  echo "  ⚠️ Running as root"
else
  echo "  ✅ Running as $(whoami) (uid=$(id -u))"
fi

# 2. Check port
PORT=${OPENCLAW_PORT:-18789}
echo ""
echo "🔌 Network Binding (port $PORT):"
LISTEN_INFO=$(lsof -i :$PORT -P -n 2>/dev/null | grep LISTEN)
if [ -n "$LISTEN_INFO" ]; then
  echo "  $LISTEN_INFO"
  if echo "$LISTEN_INFO" | grep -q "127.0.0.1"; then
    echo "  ✅ Loopback only (safe)"
  elif echo "$LISTEN_INFO" | grep -q "0.0.0.0\|::"; then
    echo "  ⚠️ Listening on all interfaces (may be exposed)"
  else
    echo "  ℹ️ Check binding manually"
  fi
else
  echo "  ℹ️ No listener detected"
fi

# 3. Check config
echo ""
echo "📋 Configuration:"
for f in .env.local .env.development .env.production .env; do
  if [ -f "$f" ]; then
    HOST_VAL=$(grep -E "^(OPENCLAW_HOST|HOST)=" "$f" 2>/dev/null | cut -d= -f2)
    if [ -n "$HOST_VAL" ]; then
      echo "  $f: HOST=$HOST_VAL"
    fi
  fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

---

## What to Check

### 1. Configuration Check

Read local env files in this order:
- `.env.local`
- `.env.development`
- `.env.production`
- `.env`

Look for:
- `OPENCLAW_HOST` or `HOST`
- `OPENCLAW_PORT` or `PORT`
- Default port: `18789`

### 2. Network Binding Check

Use system commands to check if the port is listening:
- `lsof -i :{port}` (macOS/Linux)
- `netstat -tlnp | grep {port}` (Linux)
- `netstat -ano | findstr :{port}` (Windows)

Classify the binding:
- **loopback only** (127.0.0.1, ::1) → ✅ Safe
- **wildcard** (0.0.0.0, ::) → ⚠️ May be exposed
- **private network** (10.x, 192.168.x) → ⚠️ Local network only
- **public address** → ❌ Potentially exposed

### 3. Privilege Check

Check if running with elevated privileges:
- Unix: Check if `uid == 0` (root)
- Windows: Check for Administrator group membership

---

## Reporting Behavior

- Distinguish runtime listener state from config file state
- Do not claim definite public exposure based only on `0.0.0.0` or `::`
- Use wording like "may be reachable beyond localhost" unless you have stronger evidence
- If no active listener is detected, say so explicitly
- Elevated privileges are a warning, not proof of compromise

---

## Fix Behavior

- **Never modify files without explicit user permission**
- Only offer a fix when an existing `HOST` or `OPENCLAW_HOST` entry is present
- Before editing, create a `.bak` backup beside the file
- Change only the host value to `127.0.0.1`
- Preserve comments and quoting where possible
- If no existing host entry is found, explain that the active config source may be elsewhere

---

## Example Report

```
🛡️ ClawGuard Security Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Configuration
├─ Host: 127.0.0.1 (from .env)
├─ Port: 18789
└─ Status: ✅ Loopback only

🔌 Network Binding
├─ Listening: Yes
├─ Binding: 127.0.0.1:18789
└─ Assessment: ✅ Local only

🔐 Privileges
├─ User: bingo (uid=501)
└─ Status: ✅ Not elevated

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Conclusion: ✅ Secure configuration
```

---

## Error Handling

```
No env file found     → "⚠️ No configuration file found"
Port not listening    → "ℹ️ No active listener detected"
Permission denied     → "❌ Cannot check privileges"
Command not available → "⚠️ Required tool not available"
```

---

## Notes

- This is a read-only security assessment tool
- No files are modified without explicit permission
- All checks are conservative and non-invasive
- Use system tools (lsof, netstat, whoami) for detection