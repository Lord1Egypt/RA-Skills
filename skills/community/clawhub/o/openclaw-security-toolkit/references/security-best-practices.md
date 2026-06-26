# OpenClaw Security Best Practices

This document outlines security best practices for OpenClaw users.

## 1. Gateway Security

### 1.1 Bind Address

**Recommended**: `loopback` (default)
**Avoid**: `0.0.0.0` (exposes to all network interfaces)

```json
{
  "gateway": {
    "bind": "loopback"
  }
}
```

### 1.2 Authentication

Always enable token authentication:

```json
{
  "gateway": {
    "auth": {
      "mode": "token",
      "token": "your-secure-token-here"
    }
  }
}
```

**Token Requirements**:
- Minimum 32 characters
- Use mixed case, numbers, and special characters
- Rotate every 90 days

### 1.3 Remote Access

For secure remote access, use Tailscale VPN:

```json
{
  "gateway": {
    "tailscale": {
      "mode": "on"
    }
  }
}
```

**Benefits**:
- Encrypted connections
- No public port exposure
- Access control via Tailscale admin

---

## 2. Secret Management

### 2.1 Never Store Secrets in Config Files

**Bad**:
```json
{
  "models": {
    "providers": {
      "openai": {
        "apiKey": "sk-xxxxx"  // ❌ Don't do this!
      }
    }
  }
}
```

**Good**: Use environment variables
```bash
export OPENAI_API_KEY="sk-xxxxx"
```

### 2.2 Files to Check for Secrets

- `~/.openclaw/openclaw.json`
- `~/.openclaw/.env`
- `~/.openclaw/credentials/`

### 2.3 Secret Patterns to Avoid

| Pattern | Risk Level |
|---------|------------|
| `sk-*` (OpenAI) | Critical |
| `AKIA*` (AWS) | Critical |
| `cli_*` (Feishu App ID) | Medium |
| `-----BEGIN PRIVATE KEY-----` | Critical |

---

## 3. Access Control

### 3.1 Device Management

Regularly review paired devices:

```bash
openclaw-security access devices
```

Remove unused devices:
- Go to `~/.openclaw/devices/paired.json`
- Remove unwanted device entries
- Restart gateway

### 3.2 Channel Permissions

Configure user allowlists for each channel:

```json
// ~/.openclaw/credentials/feishu-default-allowFrom.json
{
  "version": 1,
  "allowFrom": [
    "ou_xxxxx"  // Only allow specific users
  ]
}
```

### 3.3 Execution Approvals

Enable command execution approvals:

```json
// ~/.openclaw/exec-approvals.json
{
  "version": 1,
  "defaults": {
    "requireApproval": true
  }
}
```

---

## 4. Network Security

### 4.1 Port Exposure

**Default Configuration** (safe):
- Port: 18789
- Bind: loopback (127.0.0.1)
- Access: Local only

**Remote Access Options**:

| Method | Security | Complexity |
|--------|----------|------------|
| Tailscale | ✅ High | Low |
| SSH Tunnel | ✅ High | Medium |
| Public IP | ❌ Low | Low |

### 4.2 Firewall Rules

If you must expose the gateway:

```bash
# Allow only specific IP
sudo ufw allow from 192.168.1.100 to any port 18789

# Or use iptables
sudo iptables -A INPUT -p tcp --dport 18789 -s 192.168.1.100 -j ACCEPT
```

---

## 5. Monitoring & Auditing

### 5.1 Regular Security Audits

Run weekly:
```bash
openclaw-security audit --deep
```

### 5.2 Log Review

Check logs regularly:
```bash
tail -f ~/.openclaw/logs/gateway.log
```

### 5.3 Token Rotation

Rotate tokens every 90 days:
```bash
openclaw-security token rotate --fix
```

---

## 6. Incident Response

### 6.1 If You Suspect a Breach

1. **Immediately rotate tokens**:
   ```bash
   openclaw-security token rotate --fix
   openclaw gateway restart
   ```

2. **Review paired devices**:
   ```bash
   openclaw-security access devices
   ```

3. **Check channel permissions**:
   ```bash
   openclaw-security access list
   ```

4. **Review logs** for suspicious activity:
   ```bash
   grep -i "error\|failed\|unauthorized" ~/.openclaw/logs/gateway.log
   ```

### 6.2 Recovery Checklist

- [ ] Rotate all tokens
- [ ] Review and remove unauthorized devices
- [ ] Check and update channel allowlists
- [ ] Scan for exposed secrets
- [ ] Update any compromised API keys
- [ ] Document the incident

---

## 7. Compliance

### 7.1 SOC 2 Alignment

- Enable token authentication
- Rotate tokens quarterly
- Maintain audit logs
- Restrict access via allowlists

### 7.2 Data Protection

- Never log sensitive data
- Use environment variables for secrets
- Encrypt backups of configuration

---

## Quick Reference

```bash
# Daily security check
openclaw-security status

# Weekly audit
openclaw-security audit --deep

# Scan for secrets
openclaw-security scan

# Generate report
openclaw-security report --format md -o security-report.md

# Apply fixes
openclaw-security harden --fix

# Restart gateway
openclaw gateway restart
```

---

*Last updated: 2026-03-11*