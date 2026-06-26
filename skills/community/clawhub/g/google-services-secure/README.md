# Google Services Secure

🔒 **Enterprise-grade Google Workspace integration with security first**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security Level: Enterprise](https://img.shields.io/badge/Security-Enterprise-green)](https://github.com/nelmaz/openclaw-google-services-secure)
[![Version: 1.0.0](https://img.shields.io/badge/Version-1.0.0-blue)](https://clawhub.ai/nelson-mazonzika/google-services-secure)

---

## ⚠️ Why This Exists?

Google APIs provide powerful integration with Gmail, Drive, Calendar, Sheets, and more, but improper implementation can lead to:

- ❌ **Credential Exposure** - API keys and OAuth secrets stored in config files
- ❌ **No Input Validation** - Malicious data can be injected into API calls
- ❌ **No Audit Logging** - No record of what actions were taken
- ❌ **No Rate Limiting** - APIs can be abused for DoS attacks
- ❌ **No Permission Controls** - Anyone with access can do anything
- ❌ **No Confirmation** - Dangerous operations happen without approval

**This secure version implements enterprise-grade security protections for all Google services.**

---

## 🔒 Security Features

| Feature | Description | Status |
|----------|-------------|--------|
| **Credential Isolation** | OAuth tokens and secrets never stored in files | ✅ Active |
| **Input Validation** | Email, file paths, and data sanitization | ✅ Active |
| **Audit Logging** | Complete action trail with timestamps | ✅ Active |
| **Rate Limiting** | Per-service limits to prevent abuse | ✅ Active |
| **Granular Permissions** | Read-only, restricted, and full modes | ✅ Active |
| **Sandbox Support** | Isolated execution environment | ✅ Supported |
| **OAuth 2.0 Flow** | Secure authorization with refresh tokens | ✅ Active |
| **HTTPS Only** | Enforces encrypted connections | ✅ Active |
| **Confirmation Required** | Two-factor for dangerous operations | ✅ Active |

---

## 🚀 Quick Start

### 1. Install

```bash
clawhub install nelson-mazonzika/google-services-secure
```

### 2. Configure Environment Variables

```bash
# NEVER store these in files
export GOOGLE_API_KEY="your-api-key"
export GOOGLE_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="your-client-secret"
export GOOGLE_REDIRECT_URI="http://localhost:8080/callback"

# Reload shell
source ~/.bashrc
```

### 3. Validate Setup

```bash
cd /data/.openclaw/workspace/skills/google-services-secure
./scripts/validate-setup.sh
```

This checks:
- ✅ Environment variables are set
- ✅ OAuth 2.0 credentials are valid
- ✅ Audit logging is configured
- ✅ Google API connectivity works

### 4. Authenticate via OAuth 2.0

```bash
cd /data/.openclaw/workspace/skills/google-services-secure
./scripts/auth-google.sh auth
```

This will:
- Generate OAuth 2.0 authorization URL
- Open browser for user consent
- Capture authorization code
- Exchange code for access token
- Store tokens securely in memory

### 5. Use Google Services

```bash
# List Gmail messages (read-only)
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages" \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# List Drive files (read-only)
curl -s "https://www.googleapis.com/drive/v3/files" \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# List Calendar events (read-only)
curl -s "https://www.googleapis.com/calendar/v3/calendars/primary/events" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

---

## 📋 Requirements

### Environment Variables (Required)

```bash
# Google Cloud Console credentials
export GOOGLE_API_KEY="your-api-key"
export GOOGLE_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="your-client-secret"

# OAuth 2.0 configuration
export GOOGLE_REDIRECT_URI="http://localhost:8080/callback"
```

### Environment Variables (Optional)

```bash
export GOOGLE_PERMISSION_MODE="readonly"     # readonly | restricted | full
export GOOGLE_RATE_LIMIT_GMAIL="100/minute"   # Custom rate limits
export GOOGLE_RATE_LIMIT_DRIVE="500/minute"
```

### Getting Google Cloud Credentials

1. **Create Google Cloud Project:**
   - Go to: https://console.cloud.google.com/
   - Create new project

2. **Enable APIs:**
   - Gmail API
   - Drive API
   - Calendar API
   - Sheets API
   - People API (Contacts)

3. **Create OAuth 2.0 Credentials:**
   - Go to: https://console.cloud.google.com/apis/credentials
   - Create OAuth 2.0 Client ID
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:8080/callback`

4. **Create API Key:**
   - Go to: https://console.cloud.google.com/apis/credentials
   - Create API key
   - Set restrictions (IP, referrer, etc.)

### System Requirements

- **Node.js:** >= 18.0.0
- **OpenClaw:** Latest version
- **curl:** Required for API calls
- **jq:** Recommended for JSON parsing

---

## 🔐 Security Architecture

### Three Permission Levels

#### Readonly Mode (Default)
```
✅ Can: List, view, get (read-only)
❌ Cannot: Send, upload, create, update, delete
🟢 Risk: LOW
```

#### Restricted Mode
```
✅ Can: All readonly + limited write operations
❌ Cannot: Delete, share (without 2-factor)
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
   - OAuth 2.0 tokens stored in RAM only
   - Refresh tokens for long-term access
   - No file storage of secrets

2. **Layer 2: Input Validation**
   - Email format validation
   - File path validation (no directory traversal)
   - Data sanitization before API calls
   - SQL injection prevention

3. **Layer 3: Access Control**
   - Three permission levels
   - Confirmation requirements
   - Principle of least privilege
   - OAuth scope restrictions

4. **Layer 4: Monitoring & Audit**
   - Complete action logging
   - Timestamp tracking
   - Service-specific action tracking
   - Suspicious activity detection

5. **Layer 5: Rate Limiting**
   - Per-service rate limits
   - Per-operation quotas
   - DoS prevention
   - Request throttling

6. **Layer 6: Isolation**
   - Sandbox support
   - Process isolation
   - Network segmentation
   - No credential sharing between sessions

---

## 📊 Audit Logging

All actions are logged to:

```
/data/.openclaw/logs/google-services-audit.log
```

**Log format:**
```json
{
  "timestamp": "2024-04-04T00:30:45.123Z",
  "user": "nelson",
  "service": "gmail",
  "action": "LIST_MESSAGES",
  "status": "success",
  "messageCount": 10,
  "durationMs": 234,
  "permissionMode": "readonly"
}
```

**Review logs:**
```bash
# Live monitoring
tail -f /data/.openclaw/logs/google-services-audit.log

# Search for errors
grep "status\":\"error" /data/.openclaw/logs/google-services-audit.log

# Count by service
jq -r '.service' /data/.openclaw/logs/google-services-audit.log | sort | uniq -c
```

---

## 🛡️ Security Best Practices

### ✅ DO

```bash
# Set environment variables at system level
export GOOGLE_API_KEY="your-api-key"
export GOOGLE_CLIENT_ID="your-client-id.apps.googleusercontent.com"

# Use readonly mode in production
export GOOGLE_PERMISSION_MODE="readonly"

# Review audit logs regularly
tail -100 /data/.openclaw/logs/google-services-audit.log

# Validate setup before use
./scripts/validate-setup.sh

# Use OAuth 2.0 flow for authentication
./scripts/auth-google.sh auth
```

### ❌ DON'T

```bash
# NEVER store credentials in config files
{
  "env": {
    "GOOGLE_CLIENT_SECRET": "..."  # ❌ CRITICAL SECURITY ISSUE
  }
}

# NEVER use HTTP (unencrypted)
export GOOGLE_API_KEY="http://..."  # ❌ INSECURE

# NEVER share access tokens
echo "$ACCESS_TOKEN"  # ❌ LEAKS CREDENTIALS

# NEVER use broad OAuth scopes without justification
# Only request minimum required scopes
```

---

## 🔧 Configuration

### OpenClaw Agent Configuration

```json
{
  "agents": {
    "google-services": {
      "id": "google-services",
      "name": "Google Services (Secure)",
      "skills": ["google-services-secure"],
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
- **OAuth Script:** `scripts/auth-google.sh` - OAuth 2.0 flow
- **Google API Docs:** https://developers.google.com/apis

---

## 🐛 Troubleshooting

### Error: Invalid Credentials
```
Error: Invalid Credentials
```
**Solution:**
- Verify API key format
- Check OAuth client ID and secret
- Regenerate credentials in Google Cloud Console

### Error: Invalid Grant
```
Error: Invalid grant
```
**Solution:**
- Verify redirect URI matches
- Check OAuth scopes
- Ensure authorization flow is correct

### Error: Rate Limit Exceeded
```
Error: User Rate Limit Exceeded
```
**Solution:**
- Wait for quota to reset
- Reduce request frequency
- Upgrade Google Cloud quota

### OAuth Authentication Failed
```
Error: Failed to exchange authorization code
```
**Solution:**
```bash
# Revoke old tokens
./scripts/auth-google.sh revoke

# Re-authenticate
./scripts/auth-google.sh auth
```

---

## 🔄 Supported Google Services

| Service | API Endpoint | Scope |
|---------|--------------|--------|
| **Gmail** | gmail.googleapis.com | https://www.googleapis.com/auth/gmail.readonly |
| **Drive** | drive.googleapis.com | https://www.googleapis.com/auth/drive.readonly |
| **Calendar** | calendar.googleapis.com | https://www.googleapis.com/auth/calendar.events.readonly |
| **Sheets** | sheets.googleapis.com | https://www.googleapis.com/auth/spreadsheets.readonly |
| **Docs** | drive.googleapis.com | https://www.googleapis.com/auth/drive.readonly |
| **Contacts** | people.googleapis.com | https://www.googleapis.com/auth/contacts.readonly |

---

## 📄 License

MIT License - See [LICENSE.md](LICENSE.md) for details.

**SECURITY NOTICE:** This skill prioritizes security over convenience. Users are responsible for maintaining the security of their Google Cloud credentials and OAuth tokens. The authors accept no liability for security breaches resulting from improper use or configuration.

---

## 🔗 Links

- **ClawHub:** https://clawhub.ai/nelson-mazonzika/google-services-secure
- **GitHub:** https://github.com/nelmaz/openclaw-google-services-secure
- **Security Guide:** `references/security.md`
- **Google Cloud Console:** https://console.cloud.google.com/
- **OAuth Playground:** https://developers.google.com/oauthplayground/

---

## 🎯 Roadmap

- [ ] Web UI for audit log viewing
- [ ] Automatic token refresh
- [ ] Integration with more Google services (Tasks, Keep, etc.)
- [ ] Batch operation support
- [ ] Advanced error handling and retry logic
- [ ] Role-based access control (RBAC)
- [ ] Multi-factor authentication for skill usage

---

⭐ Support

- **Security Issues:** Report immediately via private channels
- **Issues:** https://github.com/nelmaz/openclaw-google-services-secure/issues
- **Documentation:** `references/` directory

---

**Remember:** Security is not a feature, it's a mindset. Every Google API interaction should be reviewed through this security lens.

🔒 Stay Secure, Stay Safe
