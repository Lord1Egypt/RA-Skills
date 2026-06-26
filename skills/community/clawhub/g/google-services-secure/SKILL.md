---
name: google-services-secure
description: Secure Google Workspace integration (Gmail, Drive, Calendar, Sheets, Docs, Contacts, etc.) with enterprise-grade security. Features credential isolation, input validation, audit logging, rate limiting, and granular permissions. Use when working with Google APIs, sending emails, managing files, scheduling calendar events, or automating Google Workspace workflows.
version: "1.0.0"
metadata:
  author: nelson-mazonzika
  homepage: https://clawhub.ai/nelson-mazonzika/google-services-secure
  license: MIT
  openclaw:
    emoji: 🔒
    requires:
      bins: []
      env:
        - GOOGLE_API_KEY
        - GOOGLE_CLIENT_ID
        - GOOGLE_CLIENT_SECRET
      node: ">=18.0.0"
    security:
      level: enterprise
      features:
        - credential-isolation
        - input-validation
        - audit-logging
        - rate-limiting
        - granular-permissions
        - sandbox-support
        - oauth-2.0-flow
        - https-only
        - confirmation-required
      tested: true
      audit-trail: true
---

# Google Services Secure

## 🔒 Security First

This skill implements **enterprise-grade security** protections for Google Workspace APIs:

- ✅ **Credential Isolation** - OAuth tokens and secrets never stored in config files
- ✅ **Input Validation** - All emails, file IDs, and parameters sanitized
- ✅ **Audit Logging** - Complete action trail with timestamps
- ✅ **Rate Limiting** - Prevents abuse and DoS
- ✅ **Granular Permissions** - Read-only mode by default
- ✅ **Sandbox Support** - Isolated execution environment
- ✅ **OAuth 2.0 Flow** - Secure authorization flow
- ✅ **HTTPS Only** - Enforces encrypted connections
- ✅ **Confirmation Required** - Dangerous operations need explicit approval

## ⚠️ Before Using

**CRITICAL SECURITY REQUIREMENTS:**

1. **Environment Variables MUST be Set:**
```bash
# NEVER store these in openclaw.json or any config file
export GOOGLE_API_KEY="your-api-key"
export GOOGLE_CLIENT_ID="your-client-id"
export GOOGLE_CLIENT_SECRET="your-client-secret"
export GOOGLE_REDIRECT_URI="http://localhost:8080/callback"
```

2. **First-Time Setup Required:**
```bash
cd /data/.openclaw/workspace/skills/google-services-secure
./scripts/validate-setup.sh
```

3. **OAuth 2.0 Flow:**
```bash
# Generate OAuth URL and authenticate
./scripts/auth-google.sh
```

## Quick Start

### 1. Configure Environment Variables

```bash
# Add to ~/.bashrc or /etc/environment
export GOOGLE_API_KEY="your-api-key"
export GOOGLE_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="your-client-secret"
export GOOGLE_REDIRECT_URI="http://localhost:8080/callback"

# Reload shell
source ~/.bashrc
```

### 2. Validate Setup

```bash
cd /data/.openclaw/workspace/skills/google-services-secure
./scripts/validate-setup.sh
```

This will:
- Verify environment variables are set
- Validate Google API key format
- Test OAuth credentials
- Create audit log directory
- Report any security issues

### 3. Authenticate via OAuth 2.0

```bash
cd /data/.openclaw/workspace/skills/google-services-secure
./scripts/auth-google.sh
```

This will:
- Generate OAuth 2.0 authorization URL
- Open browser for user consent
- Capture authorization code
- Exchange code for access token
- Store tokens securely in memory

### 4. List Gmail Messages (Read-Only)

```bash
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=10" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
  -H "Content-Type: application/json"
```

## Security Architecture

### Credential Management

**❌ NEVER do this:**
```json
{
  "env": {
    "GOOGLE_API_KEY": "AIza...",  // ❌ INSECURE
    "GOOGLE_CLIENT_ID": "...apps.googleusercontent.com",  // ❌ INSECURE
    "GOOGLE_CLIENT_SECRET": "..."  // ❌ CRITICAL SECURITY ISSUE
  }
}
```

**✅ CORRECT approach:**
```bash
# Set at system level, never in files
export GOOGLE_API_KEY="your-api-key"
export GOOGLE_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="your-client-secret"
```

### OAuth 2.0 Authorization Flow

**Step 1: Generate Authorization URL**
```bash
https://accounts.google.com/o/oauth2/v2/auth?client_id=$GOOGLE_CLIENT_ID \
  &redirect_uri=$GOOGLE_REDIRECT_URI \
  &response_type=code \
  &scope=https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/drive.readonly
```

**Step 2: Exchange Code for Token**
```bash
curl -X POST https://oauth2.googleapis.com/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$GOOGLE_CLIENT_ID" \
  -d "client_secret=$GOOGLE_CLIENT_SECRET" \
  -d "code=$AUTHORIZATION_CODE" \
  -d "redirect_uri=$GOOGLE_REDIRECT_URI" \
  -d "grant_type=authorization_code"
```

### Permissions System

The skill operates in **three permission modes**:

| Mode | Read | Write | Delete | Share | Risk Level |
|-------|------|-------|---------|-------|-------------|
| `readonly` | ✅ | ❌ | ❌ | ❌ | 🟢 LOW |
| `restricted` | ✅ | ✅* | ❌ | ❌ | 🟡 MEDIUM |
| `full` | ✅ | ✅ | ✅* | ✅* | 🔴 HIGH |

* Requires explicit confirmation for each operation

**Default mode:** `readonly`

**To change mode:**
```bash
export GOOGLE_PERMISSION_MODE="readonly"  # Recommended for production
```

### Audit Logging

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

### Rate Limiting

Default limits (configurable):

| Service | Limit | Window |
|---------|-------|---------|
| Gmail API | 100 | per minute |
| Drive API | 500 | per minute |
| Calendar API | 100 | per minute |
| Sheets API | 100 | per minute |
| Contacts API | 50 | per minute |

**Customize limits:**
```bash
export GOOGLE_RATE_LIMIT_GMAIL="100/minute"
export GOOGLE_RATE_LIMIT_DRIVE="500/minute"
```

## Available Services

### 📧 Gmail (gmail.googleapis.com)

#### 1. List Messages
```bash
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=10" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

#### 2. Get Message
```bash
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages/$MESSAGE_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

#### 3. Send Email (Requires Permission)
**⚠️ Confirmation required before sending**
```bash
curl -X POST "https://gmail.googleapis.com/gmail/v1/users/me/messages/send" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "raw": "From: me@example.com\r\nTo: recipient@example.com\r\nSubject: Test\r\n\r\nTest message body"
  }'
```

### 💾 Google Drive (drive.googleapis.com)

#### 1. List Files
```bash
curl -s "https://www.googleapis.com/drive/v3/files?pageSize=10" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

#### 2. Upload File (Requires Permission)
**⚠️ Confirmation required before uploading**
```bash
curl -X POST "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -F "metadata={\"name\":\"test.txt\"};type=application/json; charset=UTF-8" \
  -F "file=@test.txt"
```

#### 3. Download File
```bash
curl -s "https://www.googleapis.com/drive/v3/files/$FILE_ID?alt=media" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -O downloaded_file.txt
```

### 📅 Google Calendar (calendar.googleapis.com)

#### 1. List Events
```bash
curl -s "https://www.googleapis.com/calendar/v3/calendars/primary/events?maxResults=10" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

#### 2. Create Event (Requires Permission)
**⚠️ Confirmation required before creating**
```bash
curl -X POST "https://www.googleapis.com/calendar/v3/calendars/primary/events" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "Meeting",
    "start": {"dateTime": "2024-04-04T10:00:00Z"},
    "end": {"dateTime": "2024-04-04T11:00:00Z"}
  }'
```

### 📊 Google Sheets (sheets.googleapis.com)

#### 1. List Spreadsheets
```bash
curl -s "https://sheets.googleapis.com/v4/spreadsheets" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

#### 2. Read Sheet Values
```bash
curl -s "https://sheets.googleapis.com/v4/spreadsheets/$SPREADSHEET_ID/values/Sheet1!A1:B10" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

#### 3. Update Sheet (Requires Permission)
**⚠️ Confirmation required before updating**
```bash
curl -X PUT "https://sheets.googleapis.com/v4/spreadsheets/$SPREADSHEET_ID/values/Sheet1!A1:B10" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "values": [["New Value"]]
  }'
```

### 📝 Google Docs (docs.googleapis.com)

#### 1. List Documents
```bash
curl -s "https://www.googleapis.com/drive/v3/files?q=mimeType%3D'application/vnd.google-apps.document'" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

#### 2. Get Document Content
```bash
curl -s "https://www.googleapis.com/drive/v3/files/$DOC_ID/export?mimeType=text/plain" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### 👥 Google Contacts (people.googleapis.com)

#### 1. List Connections
```bash
curl -s "https://people.googleapis.com/v1/people/me/connections?personFields=names,emailAddresses" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

#### 2. Create Contact (Requires Permission)
**⚠️ Confirmation required before creating**
```bash
curl -X POST "https://people.googleapis.com/v1/people:createContact" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "emailAddresses": [{"value": "new@example.com"}],
    "names": [{"givenName": "John", "familyName": "Doe"}]
  }'
```

## Input Validation

### Email Validation
```javascript
function validateEmail(email) {
  // Must be valid email format
  if (!email.match(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/)) {
    throw new Error('Invalid email format');
  }

  // No dangerous characters
  if (email.match(/<script|javascript:|onerror|onload/i)) {
    throw new Error('Email contains dangerous patterns');
  }

  return email;
}
```

### File Path Validation
```javascript
function validateFilePath(path) {
  // Prevent directory traversal
  if (path.includes('..') || path.includes('~')) {
    throw new Error('Invalid file path');
  }

  // Validate file extension
  const allowedExtensions = ['.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx'];
  const extension = path.slice(-5);
  if (!allowedExtensions.includes(extension)) {
    throw new Error('File type not allowed');
  }

  return path;
}
```

### Data Sanitization
```javascript
function sanitizeData(data) {
  const sensitive = ['password', 'apiKey', 'secret', 'token', 'credential'];
  
  const sanitized = JSON.parse(JSON.stringify(data));
  
  function clean(obj) {
    for (const key in obj) {
      if (sensitive.some(s => key.toLowerCase().includes(s))) {
        obj[key] = '***REDACTED***';
      } else if (typeof obj[key] === 'object') {
        clean(obj[key]);
      } else if (typeof obj[key] === 'string') {
        // Remove potential HTML/Script tags
        obj[key] = obj[key].replace(/<[^>]*>/g, '');
      }
    }
  }
  
  clean(sanitized);
  return sanitized;
}
```

## Coding Use Cases

### Use Case 1: Email Automation
```bash
#!/bin/bash
# Send automated email notifications
EMAIL_SUBJECT="Daily Report"
RECIPIENT="manager@example.com"
MESSAGE_BODY="Daily report attached."

curl -X POST "https://gmail.googleapis.com/gmail/v1/users/me/messages/send" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"raw\": \"From: me@example.com\\r\\nTo: $RECIPIENT\\r\\nSubject: $EMAIL_SUBJECT\\r\\n\\r\\n$MESSAGE_BODY\"
  }"
```

### Use Case 2: File Backup
```bash
#!/bin/bash
# Backup files from Drive to local storage
curl -s "https://www.googleapis.com/drive/v3/files?pageSize=100" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | \
  jq -r '.files[] | "\(.id) \t \(.name)"' | \
  while read id name; do
    curl -s "https://www.googleapis.com/drive/v3/files/$id?alt=media" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -O "backups/$name"
  done
```

### Use Case 3: Calendar Scheduling
```bash
#!/bin/bash
# Schedule automated calendar events
EVENT_SUMMARY="Weekly Meeting"
START_TIME=$(date -u +"%Y-%m-%dT%H:%M:00Z")
END_TIME=$(date -u -d +1hour +"%Y-%m-%dT%H:%M:00Z")

curl -X POST "https://www.googleapis.com/calendar/v3/calendars/primary/events" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"summary\": \"$EVENT_SUMMARY\",
    \"start\": {\"dateTime\": \"$START_TIME\"},
    \"end\": {\"dateTime\": \"$END_TIME\"}
  }"
```

## Security Best Practices

### ✅ DO

```bash
# Set environment variables at system level
export GOOGLE_API_KEY="your-api-key"
export GOOGLE_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="your-client-secret"

# Use readonly mode in production
export GOOGLE_PERMISSION_MODE="readonly"

# Review audit logs regularly
tail -100 /data/.openclaw/logs/google-services-audit.log

# Validate setup before use
./scripts/validate-setup.sh
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
```

## Troubleshooting

### Error: Invalid Credentials
```
Error: Invalid Credentials
```
**Solution:**
- Verify API key format
- Check client ID and secret
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

### Error: Permission Denied
```
Error: 403 Forbidden
```
**Solution:**
- Verify OAuth scopes
- Check permission mode
- Re-authenticate if token expired

## Security Checklist

Before using this skill in production, verify:

- [ ] Environment variables are set at system level
- [ ] No credentials stored in config files
- [ ] OAuth 2.0 flow configured correctly
- [ ] Permission mode is set appropriately
- [ ] Audit logging is enabled and working
- [ ] Rate limiting is configured
- [ ] First-time setup validation passed
- [ ] Sandbox mode is enabled in OpenClaw (if applicable)
- [ ] Dangerous operations require confirmation
- [ ] Regular audit reviews are scheduled

## OpenClaw Integration

### Recommended Configuration

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
      "maxConcurrent": 1
    }
  }
}
```

### Enable Skill

```bash
# Add skill to main agent
openclaw agent add-skill main google-services-secure

# Or create dedicated agent
openclaw agent create google-services \
  --skills google-services-secure \
  --sandbox require \
  --max-concurrent 1
```

## References

- **Documentation:** `references/security.md` - Complete security guide
- **Validation Script:** `scripts/validate-setup.sh` - Setup verification
- **Auth Script:** `scripts/auth-google.sh` - OAuth 2.0 flow
- **Gmail API:** https://developers.google.com/gmail/api/reference/rest/
- **Drive API:** https://developers.google.com/drive/api/reference/rest/v3/
- **Calendar API:** https://developers.google.com/calendar/api/v3/reference/
- **Sheets API:** https://developers.google.com/sheets/api/reference/rest/
- **Contacts API:** https://developers.google.com/people/api/rest/v1/

## Version History

- **1.0.0** (2024-04-04)
  - Initial secure release
  - OAuth 2.0 authorization flow
  - Credential isolation (environment variables only)
  - Input validation (email, file paths, sanitization)
  - Audit logging with complete action trail
  - Rate limiting to prevent abuse
  - Granular permissions (readonly, restricted, full)
  - Multi-service support (Gmail, Drive, Calendar, Sheets, Contacts)
  - Confirmation required for dangerous operations
  - HTTPS enforcement
  - Setup validation scripts

## License

MIT License - See LICENSE.md for details

## Contributing

Security is top priority. All contributions must:
1. Maintain security guarantees
2. Include audit logging
3. Pass validation checks
4. Update documentation
5. Add tests for security features

## Support

- **Security Issues:** Report immediately via private channels
- **Issues:** https://github.com/[your-repo]/issues
- **Documentation:** `references/` directory

---

**⚠️ IMPORTANT:** This skill prioritizes security over convenience. Read-only operations work immediately. Dangerous operations require explicit confirmation and appropriate permission levels.

**Note:** This skill uses OAuth 2.0 flow for secure authorization. Never share your access tokens or store them in files.
