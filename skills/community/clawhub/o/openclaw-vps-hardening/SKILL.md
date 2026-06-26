---
name: openclaw-vps-hardening
description: >
  Harden a Hostinger VPS running OpenClaw agents against unauthorized access, brute force, and
  exposure. Use when securing a publicly-deployed OpenClaw instance, locking down a VPS after
  initial deployment, setting up Cloudflare Tunnel + Access as an identity gate, or implementing
  defense-in-depth for AI agent infrastructure. Covers UFW firewall lockdown, SSH hardening,
  Fail2Ban, OpenClaw loopback binding, Cloudflare Tunnel, Cloudflare Access per-agent policies,
  unattended security upgrades, and file permission hardening.
---

# OpenClaw VPS Server Hardening

Seven-layer defense-in-depth strategy for OpenClaw agents on Hostinger VPS. Built around
Cloudflare Tunnel + Access as the primary access layer — port 18789 is never exposed to the internet.

## The Strategy (Cloudflare-Based)

```
Internet → Cloudflare Edge
             ├── Cloudflare Access (identity check — blocked if unauthenticated)
             └── Cloudflare Tunnel (outbound-only from VPS)
                   └── localhost:18789 (OpenClaw — loopback only)
                         └── OpenClaw token auth (second factor)

Internet → port 2222 (SSH — key-only, fail2ban)
Internet → port 18789 ✗ (denied by UFW — invisible to port scan)
```

With Cloudflare active: the VPS has **one open port** (SSH). Everything else is invisible.

---

## Quick Start

### Step 1 — Deploy OpenClaw first
Use the `openclaw-vps-deploy` skill. Get the agent running before hardening.

### Step 2 — Set up Cloudflare Tunnel + Access
Use the `cloudflare-agent-tunnel` skill. Verify the agent is accessible at `https://agent.yourdomain.com` **before** closing port 18789.

### Step 3 — Run the hardening script
```bash
# Copy script to VPS
scp scripts/harden.sh root@SERVER_IP:/tmp/harden.sh

# Dry run first — see what will change
ssh root@SERVER_IP "bash /tmp/harden.sh --dry-run"

# Apply (opens new terminal first to test SSH on new port)
ssh root@SERVER_IP "bash /tmp/harden.sh --ssh-port 2222"
```

### Step 4 — Test before closing old session
```bash
# In a NEW terminal — verify SSH works on new port BEFORE closing old session
ssh -p 2222 root@SERVER_IP "echo OK"

# If that works, close old session. If it fails, revert:
# ssh root@SERVER_IP "cp /etc/ssh/sshd_config.bak.YYYYMMDD /etc/ssh/sshd_config && systemctl reload sshd"
```

---

## The Seven Layers

### Layer 1 — UFW Firewall
- Default deny all inbound
- Allow only SSH on custom port (default: 2222)
- Deny 18789 explicitly (served via Cloudflare Tunnel — never public)
- Port 18789 invisible to internet port scans

### Layer 2 — SSH Hardening
- Move SSH off port 22 (eliminates automated scanner noise)
- Disable root login (`PermitRootLogin no`)
- Key-only auth (`PasswordAuthentication no`)
- Max 3 auth attempts, 30s login grace period
- Auto-disconnect idle sessions after 10 minutes

### Layer 3 — Fail2Ban
- Protects SSH: 3 failures = 24-hour ban
- DDoS variant: 10 attempts in 60s = 1-hour ban
- With Cloudflare handling app layer, no custom OpenClaw filter needed

### Layer 4 — OpenClaw Loopback Binding
- Change `gateway.bind` from `"lan"` to `"loopback"`
- OpenClaw listens only on `127.0.0.1` — unreachable from outside VPS
- Even if UFW rules are wrong, direct access is impossible

### Layer 5 — Unattended Security Upgrades
- Auto-applies Ubuntu security patches
- No automatic reboots (manual reboot control)
- Patches CVEs without manual intervention

### Layer 6 — File Permissions
- `~/.openclaw/` → mode 700
- `openclaw.json`, `secrets.json` → mode 600
- `~/.cloudflared/` → mode 700, credentials → mode 600
- SSH authorized_keys → mode 600

### Layer 7 — Cloudflare Access (Identity Gate)
- Every request requires authentication before reaching VPS
- Supports Google SSO, email OTP, GitHub
- Per-agent policies (each subdomain has its own allowlist)
- Service tokens for native phone app connections (no browser flow required)
- Free up to 50 users; $3/user/month Access-only beyond that

See `references/cloudflare-access.md` for full setup walkthrough including phone app service token configuration.

---

## Cloudflare Access for Native Phone Apps

For a native mobile app connecting directly to agents without browser-based login:

1. Create a **Service Token** in Zero Trust → Access → Service Auth
2. App sends two headers on every request:
   ```
   CF-Access-Client-Id: <id>.access
   CF-Access-Client-Secret: <secret>
   ```
3. No browser redirect, no JWT expiry — token is permanent until rotated
4. One service token per app, revoke if compromised

See `references/cloudflare-access.md` → Phone App Integration for full details.

---

## Script Options

```bash
bash harden.sh [options]

--ssh-port 2222        SSH port to open (default: 2222)
--openclaw-user koda   Service user for OpenClaw (default: koda)
--openclaw-dir /path   OpenClaw config directory (default: /root/.openclaw)
--dry-run              Print changes without applying
--skip-ufw             Skip UFW configuration
--skip-ssh             Skip SSH hardening
--skip-fail2ban        Skip Fail2Ban installation
--skip-upgrades        Skip unattended upgrades
```

---

## Order of Operations (Critical)

**Wrong order = lockout.** Always:

1. ✅ Deploy OpenClaw (`openclaw-vps-deploy`)
2. ✅ Set up Cloudflare Tunnel + verify HTTPS access works
3. ✅ Dry-run harden.sh
4. ✅ Apply harden.sh
5. ✅ Test SSH on new port in new terminal
6. ✅ Verify agent still accessible via Cloudflare URL
7. ✅ Close old terminal

---

## Threat Model

See `references/threat-model.md` for full attack surface analysis, what each layer defends against, and residual risks.

**Security posture after hardening:** A-
One open port (SSH). Agents invisible to port scan. Identity gate on every connection. TLS everywhere. Brute-force protection. Auto-patched OS.
