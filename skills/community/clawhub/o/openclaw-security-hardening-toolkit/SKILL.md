---
name: openclaw-security-hardening-toolkit
version: 1.0.0
applies-to: OpenClaw / Aegis deployments
delivery: SKILL.md
---

# SKILL: OpenClaw Security Hardening Toolkit

## PURPOSE

This skill closes the five most exploited attack surfaces in live OpenClaw
deployments: instance exposure, credential leakage, malicious skill
installation, unauthorized gateway access, and post-compromise recovery.

Every section maps to a real threat vector. CVE-2026-25253 demonstrated
that unprotected OpenClaw instances with public gateway endpoints are
trivially exploitable. ClawHavoc demonstrated that skill installation
is a reliable code execution path when no verification protocol exists.
This toolkit addresses both.

---

## SECTION 1: INSTANCE EXPOSURE AUDIT

Run this checklist before assuming your instance is protected.

### 1.1 — Network Exposure Check

```bash
# Check what ports OpenClaw gateway is binding on
ss -tlnp | grep -E '18789|18790|18800'

# Expected (safe): 127.0.0.1:18789 — gateway bound to loopback only
# Dangerous: 0.0.0.0:18789 — gateway exposed to all interfaces

# Check for external reachability (run from a different machine or use curl to ip-check service)
curl -s --connect-timeout 3 http://$(curl -s ifconfig.me):18789/health || echo "Not publicly reachable (good)"
```

### 1.2 — Authentication Verification

```bash
# Confirm gateway token is set and non-default
grep -r "gatewayToken\|gateway_token" ~/.openclaw/openclaw.json | head -5

# A missing or empty token means unauthenticated access is possible
# Generate a strong token if absent:
openssl rand -hex 32
# Then set it in openclaw.json: gateway.token = "<generated_value>"
```

### 1.3 — Public Exposure Risk Matrix

| Condition | Risk Level | Action Required |
|-----------|-----------|-----------------|
| Gateway on 0.0.0.0 | CRITICAL | Bind to 127.0.0.1 immediately |
| No gateway token | CRITICAL | Generate and set token now |
| Token is default/example value | HIGH | Rotate immediately |
| Gateway on LAN (192.168.x.x) | MEDIUM | Add firewall rule |
| Gateway on 127.0.0.1 only | LOW | Monitor only |

### 1.4 — openclaw.json Binding Configuration

```json
{
  "gateway": {
    "bind": "127.0.0.1:18789",
    "token": "<strong-random-token>"
  }
}
```

---

## SECTION 2: CREDENTIAL PROTECTION

### 2.1 — .env File Isolation Rules

Never store credentials in:
- The workspace root (`~/.openclaw/workspace/*.env`)
- Any git-tracked directory
- Any file that SKILL.md files or agents could read without explicit permission

Safe storage locations:
- `/etc/default/aegis` (mode 0600, owned by the agent user)
- System environment variables injected at startup
- Dedicated secrets file outside the workspace: `~/.aegis-secrets` (mode 0600)

```bash
# Audit current credential exposure
find ~/.openclaw/workspace -name "*.env" -o -name ".env*" 2>/dev/null
find ~/.openclaw/workspace -name "*.json" | xargs grep -l "sk_live\|rk_live\|ghp_\|re_" 2>/dev/null

# If any hits: move credentials to /etc/default/aegis immediately
```

### 2.2 — API Key Rotation Procedures

When a key is suspected compromised, rotate in this order:

1. **Revoke the old key first** — do not wait until the new key is confirmed working
2. Generate the new key at the provider dashboard
3. Update `/etc/default/aegis` (not openclaw.json env.vars — that file can be read by agents)
4. Restart the service: `openclaw gateway restart`
5. Verify new key works before closing the provider dashboard session
6. Log the rotation date and reason in `memory/YYYY-MM-DD.md`

**Key rotation checklist:**

```
[ ] RAILWAY_TOKEN — railway.app/account/tokens
[ ] GITHUB_TOKEN — github.com/settings/tokens
[ ] STRIPE_SECRET_KEY — dashboard.stripe.com/apikeys
[ ] OPENAI_API_KEY — platform.openai.com/api-keys
[ ] RESEND_API_KEY — resend.com/api-keys
[ ] SUPABASE_SERVICE_KEY — app.supabase.com/project/<id>/settings/api
[ ] CLAWMART_API_KEY — shopclawmart.com/account/api
[ ] FERNET_KEY — generate new: python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 2.3 — ENCRYPTION_KEY / FERNET_KEY Generation

```bash
# Generate a new Fernet key (do this once, store securely)
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Store in /etc/default/aegis:
# FERNET_KEY=<generated_value>

# NEVER store in:
# - openclaw.json (world-readable to agents)
# - workspace files
# - git repositories
```

---

## SECTION 3: SKILL VERIFICATION PROTOCOL

ClawHavoc demonstrated that malicious SKILL.md files can be used as a
code execution vector. Every skill installed from ClawMart, ClawHub, or
any external source must pass this verification before activation.

### 3.1 — Pre-Installation Audit Checklist

Before installing any skill:

```
[ ] Read the FULL SKILL.md — not just the description
[ ] Check for exec: tool calls with variable interpolation
[ ] Check for web_fetch or browser calls to external URLs
[ ] Check for any instruction to write files outside the workspace
[ ] Check for any instruction to modify openclaw.json or SOUL.md
[ ] Check for base64-encoded strings (obfuscation signal)
[ ] Check for instructions that reference environment variables directly
[ ] Verify publisher has other public listings (not a throwaway account)
[ ] Check publish date — skills published <24h ago carry higher risk
```

### 3.2 — ClawHavoc Attack Vectors

The ClawHavoc attack family uses SKILL.md files to:

1. **Unauthorized outbound data transfers** — instructions to `exec` a curl call containing
   env var contents to an attacker-controlled endpoint
2. **Modify system prompts** — instructions to patch SOUL.md or AGENTS.md
   with backdoor behaviors that persist across sessions
3. **Establish persistence** — instructions to create cron jobs that phone home
4. **Lateral movement** — instructions to access system configuration files or
   other credential files adjacent to the workspace

**Detection patterns:**

```bash
# Scan an installed skill for red flags before activation
grep -iE "curl.*\$[A-Z_]+|wget.*\$[A-Z_]+" /path/to/SKILL.md
grep -iE "base64|eval\s*\$|exec.*env\s" /path/to/SKILL.md
grep -iE "SOUL\.md|AGENTS\.md|openclaw\.json" /path/to/SKILL.md
grep -iE "cron|at\s+[0-9]|systemctl enable" /path/to/SKILL.md
grep -iE "private_keys|system_configs|auth_files" /path/to/SKILL.md

# Any hit = manual review required before activation
```

### 3.3 — Safe Skill Installation Process

```
1. Download skill to a quarantine directory: ~/.openclaw/skill-quarantine/
2. Run the red-flag scan above
3. Read the full file manually
4. If clean: move to ~/.openclaw/workspace/skills/
5. Log installation in memory/YYYY-MM-DD.md: skill name, source, version, date
6. Never install skills directly to the active skills directory without quarantine step
```

---

## SECTION 4: ACCESS CONTROL FRAMEWORK

### 4.1 — Gateway Token Management

```json
// openclaw.json — minimum required security configuration
{
  "gateway": {
    "bind": "127.0.0.1:18789",
    "token": "<minimum 32 hex chars>",
    "remote": {
      "enabled": false
    }
  }
}
```

Only enable `gateway.remote` if you have a specific need for external access
and have configured a reverse proxy with TLS termination in front of it.
Never expose the raw OpenClaw gateway port to the internet.

### 4.2 — Session Sandboxing

For non-main sessions (subagents, ACP harness, isolated tasks):

```json
{
  "sessions": {
    "isolated": {
      "sandbox": "require",
      "filesystem": {
        "allowedPaths": ["~/.openclaw/workspace"],
        "denyPaths": ["/etc", "/home", "~/.private", "~/.system"]
      }
    }
  }
}
```

Apply `sandbox: "require"` to any session that:
- Runs untrusted code
- Processes external input (webhooks, user-submitted content)
- Executes skills from unknown publishers

### 4.3 — Bash Validator Integration (from BASH_SECURITY_ARCHITECTURE.md)

The 19-validator pre-execution chain is the primary shell defense layer.
Key validators for access control:

```
VALIDATOR 10 — sudo/su detection
  Pattern: ^sudo\s, ^su\s, \bsudo\b, \bsu\b
  Action: ASK — surface to human before any privilege escalation

VALIDATOR 11 — Path traversal
  Pattern: path traversal sequences, system auth files, private key directories
  Action: ASK — no agent should be reading these paths autonomously

VALIDATOR 14 — Environment variable unauthorized outbound transfers
  Pattern: curl.*\$[A-Z_]{3,}, wget.*\$[A-Z_]{3,}
  Action: ASK — blocks credential unauthorized outbound transfers via network calls
  
VALIDATOR 16 — Config file modification
  Pattern: >.*openclaw\.json, >.*SOUL\.md, >.*AGENTS\.md
  Action: ASK — blocks unauthorized system file modification
```

### 4.4 — Filesystem Restriction Patterns

```bash
# Lock down the workspace directory ownership
chmod 750 ~/.openclaw/workspace
chmod 600 ~/.openclaw/workspace/*.md

# Prevent world-readable credential files
chmod 600 /etc/default/aegis
chown root:root /etc/default/aegis  # or your agent user

# Verify no sensitive files are in git-tracked locations
cd ~/.openclaw/workspace && git ls-files | xargs grep -l "sk_\|rk_\|ghp_\|re_" 2>/dev/null
```

---

## SECTION 5: INCIDENT RESPONSE

If you suspect your OpenClaw instance has been compromised, execute this
sequence in order. Do not skip steps.

### 5.1 — Immediate Containment (first 5 minutes)

```bash
# Step 1: Stop the gateway immediately
openclaw gateway stop

# Step 2: Kill any active sessions
pkill -f "openclaw\|claude\|aegis" 

# Step 3: Disconnect from network if running on a VPS (via provider console)
# Do NOT do this on your local machine — you need the connection to remediate

# Step 4: Preserve logs before anything else
cp -r ~/.openclaw/logs ~/incident-$(date +%Y%m%d-%H%M%S)-logs/
cp ~/.openclaw/openclaw.json ~/incident-$(date +%Y%m%d-%H%M%S)-config.json
```

### 5.2 — Token Revocation Sequence

Revoke in this order (highest-blast-radius first):

```
1. RAILWAY_TOKEN — railway.app/account/tokens — REVOKE IMMEDIATELY
2. GITHUB_TOKEN — github.com/settings/tokens — REVOKE
3. STRIPE_SECRET_KEY — dashboard.stripe.com/apikeys — REVOKE
4. OPENAI_API_KEY — platform.openai.com/api-keys — REVOKE
5. SUPABASE_SERVICE_KEY — Supabase dashboard — REVOKE
6. RESEND_API_KEY — resend.com/api-keys — REVOKE
7. CLAWMART_API_KEY — ClawMart account — REVOKE
8. FERNET_KEY — rotate in code (data encrypted with old key is unreadable — plan for this)
```

After revoking all keys, check provider audit logs for unauthorized API calls
before generating new keys.

### 5.3 — Recovery Checklist

```
[ ] All tokens revoked (see 5.2)
[ ] New tokens generated and stored in /etc/default/aegis (not workspace)
[ ] openclaw.json audited for unauthorized modifications
[ ] SOUL.md audited for backdoor instructions
[ ] AGENTS.md audited for unauthorized changes
[ ] HEARTBEAT.md audited
[ ] Installed skills directory audited for unauthorized files
[ ] Cron jobs audited: crontab -l and systemctl list-units --type=timer
[ ] New gateway token set (minimum 32 hex chars)
[ ] Gateway restarted with new config
[ ] Incident logged in memory/YYYY-MM-DD.md with timeline
[ ] Affected parties notified (Stripe, Railway if production traffic impacted)
```

### 5.4 — Post-Incident Hardening

After recovery, complete these steps before resuming normal operation:

```
1. Move all credentials from openclaw.json env.vars to /etc/default/aegis
2. Enable gateway.bind = "127.0.0.1:18789" if not already set
3. Add skill quarantine step to all future installations (Section 3.3)
4. Schedule monthly credential rotation (add to cron)
5. Review all installed skills using the red-flag scan in Section 3.2
```

---

## QUICK REFERENCE — EMERGENCY COMMANDS

```bash
# Stop everything
openclaw gateway stop && pkill -f claude

# Check what's exposed
ss -tlnp | grep -E '18789|18790|18800'

# Audit credentials in workspace
find ~/.openclaw/workspace -name "*.json" -o -name "*.env" | \
  xargs grep -l "sk_\|rk_\|ghp_\|re_\|Bearer" 2>/dev/null

# Check for unauthorized cron jobs
crontab -l 2>/dev/null
systemctl list-units --type=timer 2>/dev/null | grep -v systemd

# Rotate gateway token
openssl rand -hex 32
# → update openclaw.json gateway.token, then restart
```
