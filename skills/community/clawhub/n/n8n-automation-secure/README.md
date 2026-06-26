# N8N Automation Secure

🔒 **Enterprise-grade n8n workflow automation with security first**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security Level: Enterprise](https://img.shields.io/badge/Security-Enterprise-green)](https://github.com/nelson-mazonzika/openclaw-n8n-automation-secure)
[![Version: 1.0.0](https://img.shields.io/badge/Version-1.0.0-blue)](https://clawhub.ai/nelson-mazonzika/n8n-automation-secure)

---

## ⚠️ Why This Exists?

The original `n8n-code-automation-nelmaz` skill had **critical security vulnerabilities**:

- ❌ Hardcoded URLs pointing to specific domains
- ❌ API keys stored in plain text config files
- ❌ No input validation or sanitization
- ❌ No audit logging or tracking
- ❌ No rate limiting or abuse prevention
- ❌ No permission controls
- ❌ No confirmation for dangerous operations

**This secure version fixes ALL of those issues** with enterprise-grade security protections.

---

## 🔒 Security Features

| Feature | Description | Status |
|----------|-------------|--------|
| **Credential Isolation** | API keys never stored in files | ✅ Active |
| **Input Validation** | URL and data sanitization | ✅ Active |
| **Audit Logging** | Complete action trail | ✅ Active |
| **Rate Limiting** | Prevents abuse and DoS | ✅ Active |
| **Granular Permissions** | Read-only by default | ✅ Active |
| **Sandbox Support** | Isolated execution | ✅ Supported |
| **HTTPS Only** | Enforced encrypted connections | ✅ Active |
| **Confirmation Required** | Two-factor for dangerous ops | ✅ Active |

---

## 🚀 Quick Start

### 1. Install

```bash
clawhub install nelson-mazonzika/n8n-automation-secure
```

### 2. Configure Environment Variables

```bash
# NEVER store these in files
export N8N_URL="https://your-n8n-instance.com"
export N8N_API_KEY="your-api-key"

# Reload shell
source ~/.bashrc
```

### 3. Validate Setup

```bash
cd /data/.openclaw/workspace/skills/n8n-automation-secure
./scripts/validate-setup.sh
```

This checks:
- ✅ Environment variables are set
- ✅ URL format is valid (HTTPS only)
- ✅ No credentials in config files
- ✅ Audit logging is configured
- ✅ API connectivity works

### 4. Use Safely

```bash
# List workflows (read-only)
curl -X GET "$N8N_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"

# Execute workflow (with confirmation)
curl -X POST "$N8N_URL/api/v1/workflows/{id}/executions" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
```

---

## 📋 Requirements

### Environment Variables (Required)

```bash
export N8N_URL="https://your-n8n-instance.com"  # Your n8n instance URL
export N8N_API_KEY="your-api-key"               # From n8n settings
```

### Environment Variables (Optional)

```bash
export N8N_PERMISSION_MODE="readonly"     # readonly | restricted | full
export N8N_RATE_LIMIT="10/minute"       # API rate limit
export N8N_EXECUTION_LIMIT="5/minute"    # Execution rate limit
```

### System Requirements

- **Node.js:** >= 18.0.0
- **OpenClaw:** Latest version
- **n8n Instance:** Self-hosted or cloud
- **Network:** HTTPS access to n8n instance

---

## 🔐 Security Architecture

### Three Permission Levels

#### Readonly Mode (Default)
```
✅ Can: List, view, execute (with confirmation)
❌ Cannot: Create, update, delete
🟢 Risk: LOW
```

#### Restricted Mode
```
✅ Can: All readonly + create, execute
❌ Cannot: Update/delete (without 2-factor)
🟡 Risk: MEDIUM
```

#### Full Mode
```
✅ Can: All operations (with confirmation)
🔴 Risk: HIGH (isolated environments only)
```

### Defense in Depth

1. **Layer 1: Credential Management**
   - Environment variables only
   - No file storage
   - Runtime validation

2. **Layer 2: Input Validation**
   - URL format validation
   - Data sanitization
   - SQL injection prevention

3. **Layer 3: Access Control**
   - Three permission levels
   - Confirmation requirements
   - Principle of least privilege

4. **Layer 4: Monitoring & Audit**
   - Complete action logging
   - Timestamp tracking
   - Suspicious activity detection

5. **Layer 5: Rate Limiting**
   - Per-operation limits
   - Per-user quotas
   - DoS prevention

6. **Layer 6: Isolation**
   - Sandbox support
   - Process isolation
   - Network segmentation

---

## 📊 Audit Logging

All actions are logged to:

```
/data/.openclaw/logs/n8n-audit.log
```

**Log format:**
```json
{
  "timestamp": "2024-04-04T00:30:45.123Z",
  "user": "nelson",
  "session": "main",
  "action": "WORKFLOW_EXECUTE",
  "workflowId": "abc123",
  "workflowName": "CI Build",
  "status": "success",
  "durationMs": 234,
  "ip": "127.0.0.1",
  "userAgent": "curl/7.68.0",
  "inputHash": "a1b2c3d4",
  "permissionMode": "readonly"
}
```

**Review logs:**
```bash
# Live monitoring
tail -f /data/.openclaw/logs/n8n-audit.log

# Search for errors
grep "status\":\"error" /data/.openclaw/logs/n8n-audit.log

# Count by user
jq -r '.user' /data/.openclaw/logs/n8n-audit.log | sort | uniq -c
```

---

## 🛡️ Security Best Practices

### ✅ DO

```bash
# Set environment variables at system level
export N8N_URL="https://your-n8n.com"
export N8N_API_KEY="your-key"

# Use readonly mode in production
export N8N_PERMISSION_MODE="readonly"

# Review audit logs regularly
tail -100 /data/.openclaw/logs/n8n-audit.log

# Validate setup before use
./scripts/validate-setup.sh
```

### ❌ DON'T

```bash
# NEVER store credentials in config files
{
  "env": {
    "N8N_API_KEY": "..."  # ❌ CRITICAL SECURITY ISSUE
  }
}

# NEVER use HTTP (unencrypted)
export N8N_URL="http://..."  # ❌ INSECURE

# NEVER use full mode in production
export N8N_PERMISSION_MODE="full"  # ❌ HIGH RISK
```

---

## 🔧 Configuration

### OpenClaw Agent Configuration

```json
{
  "agents": {
    "n8n-automation": {
      "id": "n8n-automation",
      "name": "n8n Automation (Secure)",
      "skills": ["n8n-automation-secure"],
      "sandbox": "require",
      "tools": {
        "allowlist": ["curl", "read", "write"],
        "denylist": ["exec", "eval", "shell"]
      },
      "filesystem": {
        "read": [
          "/data/.openclaw/logs/",
          "/tmp/"
        ],
        "write": [
          "/data/.openclaw/logs/"
        ]
      }
    }
  }
}
```

---

## 📚 Documentation

- **Main Guide:** `SKILL.md` - Complete usage documentation
- **Security Guide:** `references/security.md` - Detailed security architecture
- **Validation Script:** `scripts/validate-setup.sh` - Setup verification
- **N8N API Docs:** https://docs.n8n.io/api/

---

## 🐛 Troubleshooting

### Error: Environment Variables Not Set

```
ERROR: N8N_URL and N8N_API_KEY environment variables are required
```

**Solution:**
```bash
export N8N_URL="https://your-n8n.com"
export N8N_API_KEY="your-api-key"
```

### Error: Invalid URL

```
ERROR: Invalid N8N URL. Must be HTTPS and properly formatted.
```

**Solution:**
- Ensure URL starts with `https://`
- No credentials in URL
- Valid domain format

### Error: Rate Limit Exceeded

```
ERROR: Rate limit exceeded. Wait before retrying.
```

**Solution:**
- Wait for rate limit window to reset
- Adjust rate limit configuration
- Check audit logs for patterns

### Error: Permission Denied

```
ERROR: Operation not permitted in current permission mode.
```

**Solution:**
```bash
# Check current mode
echo $N8N_PERMISSION_MODE

# Switch if necessary
export N8N_PERMISSION_MODE="restricted"
```

---

## 🔄 Migration from Insecure Version

If you were using the insecure `n8n-code-automation-nelmaz` skill:

1. **Install secure version:**
```bash
clawhub install nelson-mazonzika/n8n-automation-secure
```

2. **Remove credentials from config:**
```bash
# Edit ~/.openclaw/openclaw.json
# REMOVE any N8N_URL or N8N_API_KEY entries
```

3. **Set environment variables:**
```bash
export N8N_URL="https://your-n8n.com"
export N8N_API_KEY="your-api-key"
```

4. **Validate setup:**
```bash
cd /data/.openclaw/workspace/skills/n8n-automation-secure
./scripts/validate-setup.sh
```

5. **Remove insecure skill:**
```bash
clawhub remove n8n-code-automation-nelmaz
```

---

## 🤝 Contributing

Security is the top priority. All contributions must:

1. ✅ Maintain security guarantees
2. ✅ Include audit logging
3. ✅ Pass validation checks
4. ✅ Update documentation
5. ✅ Add tests for security features

**Don't:**
- ❌ Remove security validations
- ❌ Add features without security review
- ❌ Store credentials in files
- ❌ Remove confirmation requirements

---

## 📄 License

MIT License - See [LICENSE.md](LICENSE.md) for details.

**SECURITY NOTICE:** This skill prioritizes security over convenience. Users are responsible for maintaining the security of their N8N instances and API keys. The authors accept no liability for security breaches resulting from improper use.

---

## 🔗 Links

- **ClawHub:** https://clawhub.ai/nelson-mazonzika/n8n-automation-secure
- **GitHub:** https://github.com/nelson-mazonzika/openclaw-n8n-automation-secure
- **Security Guide:** `references/security.md`
- **N8N API:** https://docs.n8n.io/api/

---

## 🎯 Roadmap

- [ ] Web UI for audit log viewing
- [ ] Automatic threat detection
- [ ] Integration with SIEM systems
- [ ] Advanced anomaly detection
- [ ] Role-based access control (RBAC)
- [ ] Multi-factor authentication
- [ ] Secret management integration (Vault, AWS Secrets Manager)

---

## ⭐ Support

- **Security Issues:** Report immediately via private channels
- **Issues:** https://github.com/nelson-mazonzika/openclaw-n8n-automation-secure/issues
- **Documentation:** `references/` directory

---

**Remember:** Security is not a feature, it's a mindset. Every interaction should be reviewed through this security lens.

🔒 **Stay Secure, Stay Safe**
