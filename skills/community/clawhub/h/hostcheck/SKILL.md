---
version: 1.0.0
name: hostcheck
description: Free host health check for OpenClaw deployments. Check system status, updates, security settings, and provide recommendations. No paid tools required.
metadata: {"openclaw": {"emoji": "🖥️", "keywords": ["system", "health", "check", "security", "updates", "status"]}}
---

# Host Health Check - Free Edition

A free skill that checks your OpenClaw host for basic health, security posture, and maintenance status. Provides recommendations without requiring paid antivirus software.

## What It Checks

### 1. System Status
- Uptime
- Memory usage
- Disk space
- CPU load

### 2. Update Status (apt)
- Pending security updates
- Outdated packages
- Last update check

### 3. Security Posture
- SSH configuration (password auth, root login)
- Firewall status (ufw)
- Open ports
- Failed login attempts

### 4. Backup Status
- Backup cron jobs
- Recent backup files
- Disk space for backups

### 5. OpenClaw Status
- Gateway running
- Services status
- Recent errors

## Usage

When user asks for system health, security check, or similar:

```
/hostcheck
```

Or just describe what you want:
- "Check my system"
- "Is everything up to date?"
- "Security status"

## Output Format

Provide a clear status report:

```
## 🖥️ System Health Report

### ✅ System Status
- Uptime: 5 days
- Memory: 45% used
- Disk: 62% used

### ⚠️ Updates Available
- 3 security updates (run: sudo apt upgrade)
- Last check: 3 days ago

### 🔒 Security
- SSH: Password auth disabled ✓
- Firewall: Active ✓
- Failed logins: 0 (last 24h)

### 💾 Backups
- Last backup: Yesterday
- Next backup: Tomorrow 02:00

### 🔧 OpenClaw
- Gateway: Running ✓
- Services: All active ✓
```

## Recommendations

If issues found, provide actionable advice:
- Run `sudo apt update && sudo apt upgrade`
- Check firewall with `sudo ufw status`
- Review logs with `journalctl --user -u trading-*`
- Set up backups with rsync or Borg

## Notes

- This is READ-ONLY by default
- Ask before making any changes
- Does NOT include virus scanning (requires ClamAV)
- Does NOT include real-time protection
- UFW requires manual installation (sudo apt install ufw)

## Current Host Status (Example)

| Check | Status | Note |
|-------|--------|------|
| SSH | ✅ Secure | Keys only, no password auth |
| UFW | ⚠️ Not installed | Tailscale provides network-level security |
| Updates | ✅ Current | Ubuntu 25.10, 4 phased updates |
