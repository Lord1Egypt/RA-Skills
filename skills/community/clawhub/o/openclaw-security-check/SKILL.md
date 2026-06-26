---
name: openclaw-security-check
description: |
  Security self-check for OpenClaw deployments. Audits openclaw.json config and host security
  in one pass: gateway exposure, auth mode, token strength, channel DM/group policies, file
  permissions, plaintext secrets, host firewall, SSH hardening, and exposed ports.
  Outputs a 10-item PASS/WARN/FAIL report with optional auto-fix.
  Use when: user asks "run a security check", "am I secure?", "audit my config",
  "check security settings", or on periodic heartbeat/cron.
  Complements the built-in healthcheck skill (OS-level hardening workflow) with a fast,
  focused config-and-host audit.
---

# OpenClaw Security Check

Fast 10-point security audit for OpenClaw config + host. Read-only by default, optional auto-fix.

## Quick Start

Run the bundled script for a non-interactive report:

```bash
scripts/security-check.sh        # human-readable
scripts/security-check.sh --json # structured output
```

Or tell the agent: "run a security check" / "audit my OpenClaw config".

## What It Checks

| # | Check | Severity if failed | What it looks at |
|---|-------|--------------------|-----------------|
| 1 | Gateway Bind | CRITICAL | `gateway.bind` — must be loopback, not `0.0.0.0` |
| 2 | Gateway Auth | CRITICAL | `gateway.auth.mode` — must not be `off`/`none` |
| 3 | Token Strength | HIGH | `gateway.auth.token` — must be ≥32 chars |
| 4 | DM Policy | HIGH | Per-channel `dmPolicy` — `open` without `allowFrom` is dangerous |
| 5 | Group Policy | HIGH | Per-channel `groupPolicy` — `open`/`any` allows strangers to trigger the agent |
| 6 | Config Permissions | MEDIUM | File mode of `openclaw.json` — should be 600 or 400 |
| 7 | Plaintext Secrets | MEDIUM | Scans config values for keys matching password/secret/apiKey/privateKey |
| 8 | Host Firewall | HIGH | UFW or firewalld must be installed and active |
| 9 | SSH Hardening | MEDIUM | PasswordAuthentication and PermitRootLogin in sshd_config |
| 10 | Exposed Ports | MEDIUM | Count of non-loopback listening ports (>8 = FAIL) |

## Auto-Fix Flow

If any item is FAIL or WARN, offer fixes. **Always confirm with the user first.**

### Fix Recipes

**#1 Gateway Bind → FAIL:**
Set `gateway.bind` to `"loopback"`. Use `openclaw` CLI if available, otherwise edit openclaw.json.

**#2 Gateway Auth → FAIL:**
Set `gateway.auth.mode` to `"token"`. Generate a strong token if missing:
```bash
openssl rand -hex 24
```

**#3 Token Strength → FAIL/WARN:**
Replace with a new 48-char hex token: `openssl rand -hex 24`.
Warn user that paired clients will need the new token.

**#4 DM Policy → FAIL:**
Set affected channels to `"dmPolicy": "pairing"`, or add specific IDs to `allowFrom`.

**#5 Group Policy → FAIL:**
Set affected channels to `"groupPolicy": "allowlist"`.

**#6 Config Permissions → FAIL/WARN:**
```bash
chmod 600 ~/.openclaw/openclaw.json
```

**#7 Plaintext Secrets → WARN:**
Cannot auto-fix safely. Advise moving secrets to environment variables or `.env.local`.

**#8 Host Firewall → FAIL:**
```bash
sudo apt install ufw -y
sudo ufw default deny incoming
sudo ufw default allow outgoing
# IMPORTANT: Allow SSH before enabling!
sudo ufw allow from <trusted_ip_or_subnet> to any port 22 proto tcp
sudo ufw enable
```

**#9 SSH Hardening → WARN:**
```bash
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
sudo sed -i 's/^#*PasswordAuthentication .*/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/^#*PermitRootLogin .*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sshd -t && sudo systemctl reload ssh
```
CRITICAL: Ensure key-based SSH access works in a separate session before closing current one.

**#10 Exposed Ports → WARN/FAIL:**
Review with `ss -ltnp`, close unnecessary services, or restrict with firewall rules.

### Fix Rules

- **Backup first:** `cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak`
- **Merge, don't overwrite:** Modify only the specific keys, preserve everything else.
- **SSH changes need special care:** Always test access in a second session before closing the first.
- **Firewall: allow SSH first, enable second.** Getting this backwards locks you out.
- **After config changes:** `openclaw gateway restart` to apply.
- **Re-run the check after fixes** to confirm everything passes.

## Integration

### Heartbeat
Add to HEARTBEAT.md for periodic checks:
```
- Every heartbeat: Run scripts/security-check.sh, alert on any FAIL
```

### Cron
Schedule via OpenClaw cron for standalone audits:
```bash
openclaw cron add --name "security-check" --schedule "0 8 * * *" --task "Run scripts/security-check.sh and report results"
```

### Combining with healthcheck skill
This skill focuses on **fast config + host audit** (10 checks, <5 seconds).
The built-in `healthcheck` skill provides a **full hardening workflow** (risk profiling, remediation planning, guided execution).
Use this skill for quick checks; escalate to healthcheck for comprehensive hardening.
