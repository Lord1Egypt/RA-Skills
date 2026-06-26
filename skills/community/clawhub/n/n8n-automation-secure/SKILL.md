---
name: n8n-automation-secure
description: Secure n8n workflow automation integration for coding tasks. This skill implements enterprise-grade security with credential isolation, input validation, audit logging, rate limiting, and granular permissions. Use when building automated workflows, integrating n8n into development pipelines, executing existing workflows, modifying workflow configurations, or creating new automation solutions. Triggers on phrases like "create n8n workflow", "run n8n workflow", "integrate n8n", "automate with n8n", "modify n8n workflow", "execute workflow".
version: "1.0.0"
metadata:
  author: nelson-mazonzika
  homepage: https://clawhub.ai/nelson-mazonzika/n8n-automation-secure
  license: MIT
  openclaw:
    emoji: 🔒
    requires:
      bins: []
      env:
        - N8N_URL
        - N8N_API_KEY
    security:
      level: enterprise
      features:
        - credential-isolation
        - input-validation
        - audit-logging
        - rate-limiting
        - granular-permissions
        - sandbox-support
---

# N8N Automation Secure

## 🔒 Security First

This skill implements **enterprise-grade security** protections:

- ✅ **Credential Isolation** - API keys never stored in config files
- ✅ **Input Validation** - All endpoints and data sanitized
- ✅ **Audit Logging** - Complete action trail with timestamps
- ✅ **Rate Limiting** - Prevents abuse and DoS
- ✅ **Granular Permissions** - Read-only mode by default
- ✅ **Sandbox Support** - Isolated execution environment
- ✅ **HTTPS Only** - Enforces encrypted connections
- ✅ **Confirmation Required** - Dangerous operations need explicit approval

## ⚠️ Before Using

**CRITICAL SECURITY REQUIREMENTS:**

1. **Environment Variables MUST be Set:**
```bash
# NEVER store these in openclaw.json or any config file
export N8N_URL="https://your-n8n-instance.com"
export N8N_API_KEY="your-api-key"
```

2. **First-Time Setup Required:**
```bash
cd skills/n8n-automation-secure
./scripts/validate-setup.sh
```

3. **HTTPS Only:**
- Only HTTPS URLs are accepted
- Self-signed certificates will be rejected
- URL validation is enforced on every request

## Quick Start

### 1. Configure Environment Variables

```bash
# Add to ~/.bashrc or /etc/environment
export N8N_URL=""
export N8N_API_KEY=""

# Reload shell
source ~/.bashrc
```

### 2. Validate Setup

```bash
cd /data/.openclaw/workspace/skills/n8n-automation-secure
./scripts/validate-setup.sh
```

This will:
- Verify environment variables are set
- Validate N8N_URL format and HTTPS
- Test API connectivity
- Create audit log directory
- Report any security issues

### 3. List Workflows (Read-Only)

```bash
curl -X GET "$N8N_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json"
```

## Security Architecture

### Credential Management

**❌ NEVER do this:**
```json
{
  "env": {
    "N8N_URL": "https://n8n.example.com",  // ❌ INSECURE
    "N8N_API_KEY": "secret-key-here"         // ❌ CRITICAL SECURITY ISSUE
  }
}
```

**✅ CORRECT approach:**
```bash
# Set at system level, never in files
export N8N_URL="https://your-n8n.com"
export N8N_API_KEY="your-key"
```

### Permissions System

The skill operates in **three permission modes**:

| Mode | Read | Execute | Create | Update | Delete | Risk Level |
|-------|------|----------|---------|---------|--------|-------------|
| `readonly` | ✅ | ✅ | ❌ | ❌ | ❌ | 🟢 LOW |
| `restricted` | ✅ | ✅ | ✅* | ✅* | ❌ | 🟡 MEDIUM |
| `full` | ✅ | ✅ | ✅ | ✅ | ✅* | 🔴 HIGH |

* Requires explicit confirmation for each operation

**Default mode:** `readonly`

**To change mode:**
```bash
export N8N_PERMISSION_MODE="full"  # DANGEROUS - only for trusted environments
```

### Audit Logging

All actions are logged to:
```
/data/.openclaw/logs/n8n-audit.log
```

**Log format:**
```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "user": "nelson",
  "action": "WORKFLOW_EXECUTE",
  "workflowId": "abc123",
  "workflowName": "CI Build",
  "status": "success",
  "ip": "127.0.0.1",
  "userAgent": "curl/7.68.0",
  "durationMs": 234
}
```

**Review audit logs:**
```bash
tail -f /data/.openclaw/logs/n8n-audit.log
```

### Rate Limiting

Default limits (configurable):

| Operation | Limit | Window |
|-----------|-------|---------|
| API requests | 10 | per minute |
| Workflow executions | 5 | per minute |
| Bulk operations | 1 | per 5 minutes |

**Customize limits:**
```bash
export N8N_RATE_LIMIT="15/minute"
export N8N_EXECUTION_LIMIT="10/minute"
```

## Available Actions

### 🟢 Read-Only Operations (Safe)

#### 1. List Workflows
```bash
curl -X GET "$N8N_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json"
```

#### 2. Get Workflow Details
```bash
curl -X GET "$N8N_URL/api/v1/workflows/{id}" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json"
```

#### 3. Get Execution Status
```bash
curl -X GET "$N8N_URL/api/v1/executions/{id}" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
```

#### 4. Get Executions History
```bash
curl -X GET "$N8N_URL/api/v1/workflows/{id}/executions?limit=10" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
```

### 🟡 Execute Operations (Requires Permission)

#### 5. Execute Workflow (Manual)

**Confirmation required:** The skill will ask for approval before execution.

```bash
# Step 1: Review workflow
curl -X GET "$N8N_URL/api/v1/workflows/{id}" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"

# Step 2: Execute (with confirmation)
curl -X POST "$N8N_URL/api/v1/workflows/{id}/executions" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"data": {"contextData": {}, "manualExecution": true}}'
```

#### 6. Execute Webhook
```bash
curl -X POST "https://your-n8n.com/webhook/{webhook-key}" \
  -H "Content-Type: application/json" \
  -d '{"data": {"input1": "value1"}}'
```

### 🔴 Dangerous Operations (Requires Explicit Confirmation)

⚠️ **These operations require TWO confirmations**:
1. Display of what will be changed
2. Typing confirmation phrase

#### 7. Clone Workflow

```bash
# Step 1: Show what will be cloned
curl -X GET "$N8N_URL/api/v1/workflows/{source-id}" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"

# Step 2: Execute with confirmation
curl -X POST "$N8N_URL/api/v1/workflows/{source-id}/clone" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Cloned Workflow"}'
```

#### 8. Update Workflow (PATCH)

```bash
# Step 1: Show current state
curl -X GET "$N8N_URL/api/v1/workflows/{id}" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"

# Step 2: Show diff
# (Display what will change)

# Step 3: Execute with confirmation
curl -X PATCH "$N8N_URL/api/v1/workflows/{id}" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"nodes": [{"parameters": {...}}]}'
```

#### 9. Delete Workflow

```bash
# Step 1: Show workflow details
curl -X GET "$N8N_URL/api/v1/workflows/{id}" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"

# Step 2: Type confirmation
# DELETE: Workflow Name - Type "I confirm deletion" to proceed

# Step 3: Execute
curl -X DELETE "$N8N_URL/api/v1/workflows/{id}" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
```

## Input Validation

All inputs are validated before API calls:

### URL Validation
```javascript
function validateN8NUrl(url) {
  // Must be HTTPS
  if (!url.match(/^https:\/\/[a-z0-9.-]+(\.[a-z0-9.-]+)+$/i)) {
    throw new Error('Invalid N8N URL. Must be HTTPS and properly formatted.');
  }

  // No credentials in URL
  if (url.includes('@') || url.includes(':')) {
    throw new Error('URL must not contain credentials');
  }

  // No query parameters with secrets
  if (url.match(/\b(key|token|secret|password)\b/i)) {
    throw new Error('URL must not contain secret keywords');
  }

  return url;
}
```

### Data Sanitization
```javascript
function sanitizeData(data) {
  // Remove sensitive keys
  const sensitive = ['password', 'apiKey', 'secret', 'token', 'credential'];
  
  const sanitized = JSON.parse(JSON.stringify(data));
  
  function clean(obj) {
    for (const key in obj) {
      if (sensitive.some(s => key.toLowerCase().includes(s))) {
        obj[key] = '***REDACTED***';
      } else if (typeof obj[key] === 'object') {
        clean(obj[key]);
      }
    }
  }
  
  clean(sanitized);
  return sanitized;
}
```

## Coding Use Cases

### Use Case 1: CI/CD Integration (Safe)

```yaml
# .github/workflows/n8n-trigger.yml
name: Trigger N8N Workflow

on:
  push:
    branches: [main]

jobs:
  trigger-n8n:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger N8N workflow
        env:
          N8N_URL: ${{ secrets.N8N_URL }}
          N8N_API_KEY: ${{ secrets.N8N_API_KEY }}
        run: |
          curl -X POST "$N8N_URL/api/v1/workflows/${{ secrets.N8N_WORKFLOW_ID }}/executions" \
                -H "X-N8N-API-KEY: $N8N_API_KEY" \
                -H "Content-Type: application/json" \
                -d '{"data": {"contextData": {"commitSha": "${{ github.sha }}"}}}'
```

### Use Case 2: Data Processing Pipeline

```python
#!/usr/bin/env python3
import os
import requests

N8N_URL = os.environ.get('N8N_URL')
N8N_API_KEY = os.environ.get('N8N_API_KEY')

def execute_workflow(workflow_id, data):
    """Execute n8n workflow with input validation"""
    
    # Validate inputs
    if not N8N_URL or not N8N_API_KEY:
        raise ValueError('N8N_URL and N8N_API_KEY environment variables are required')
    
    if not N8N_URL.startswith('https://'):
        raise ValueError('N8N_URL must use HTTPS')
    
    # Sanitize data
    sanitized_data = sanitize(data)
    
    # Execute
    response = requests.post(
        f'{N8N_URL}/api/v1/workflows/{workflow_id}/executions',
        headers={
            'X-N8N-API-KEY': N8N_API_KEY,
            'Content-Type': 'application/json'
        },
        json={'data': {'contextData': sanitized_data}}
    )
    
    response.raise_for_status()
    return response.json()

def sanitize(data):
    """Remove sensitive data"""
    sensitive_keys = ['password', 'apiKey', 'secret', 'token']
    # ... sanitization logic
    return data
```

## Security Best Practices

### 1. Environment Variables

✅ **DO:**
```bash
# Set at system level
export N8N_URL="https://your-n8n.com"
export N8N_API_KEY="your-key"

# Or in script execution
N8N_URL="https://your-n8n.com" N8N_API_KEY="your-key" ./script.sh
```

❌ **DON'T:**
```bash
# Never in config files
export N8N_URL="..."  # Saved in ~/.bashrc (risk if compromised)
```

### 2. Permission Principle

- Use **readonly mode** by default
- Only switch to **restricted** when necessary
- Use **full mode** only in isolated environments
- Review audit logs regularly

### 3. Confirmation Workflow

For dangerous operations:
1. Show exactly what will happen
2. Require typing confirmation phrase
3. Log the action with full details
4. Send notification (if configured)

### 4. Regular Audits

```bash
# Review recent activity
tail -100 /data/.openclaw/logs/n8n-audit.log

# Check for suspicious patterns
grep -i "delete\|remove\|dangerous" /data/.openclaw/logs/n8n-audit.log

# Monitor for errors
grep "error\|failed\|unauthorized" /data/.openclaw/logs/n8n-audit.log
```

## Troubleshooting

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
- No query parameters with secrets

### Error: Rate Limit Exceeded
```
ERROR: Rate limit exceeded. Wait before retrying.
```

**Solution:**
- Wait for the rate limit window to reset
- Adjust rate limit configuration
- Check audit logs for activity patterns

### Error: Permission Denied
```
ERROR: Operation not permitted in current permission mode.
```

**Solution:**
- Check current permission mode: `echo $N8N_PERMISSION_MODE`
- Switch mode if necessary: `export N8N_PERMISSION_MODE="restricted"`

## Security Checklist

Before using this skill in production, verify:

- [ ] Environment variables are set at system level
- [ ] N8N_URL uses HTTPS only
- [ ] N8N_API_KEY is not stored in any file
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
    "n8n-automation": {
      "id": "n8n-automation",
      "name": "n8n Automation (Secure)",
      "skills": ["n8n-automation-secure"],
      "sandbox": "require",
      "tools": {
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
openclaw agent add-skill main n8n-automation-secure

# Or create dedicated agent
openclaw agent create n8n-automation \
  --skills n8n-automation-secure \
  --sandbox require \
  --max-concurrent 1
```

## References

- **Documentation:** `references/security.md` - Complete security guide
- **Validation Script:** `scripts/validate-setup.sh` - Setup verification
- **Audit Logger:** `scripts/audit-logger.sh` - Log management
- **N8N API Docs:** https://docs.n8n.io/api/
- **OpenClaw Security:** https://docs.openclaw.ai/security

## Version History

- **1.0.0** (2024-04-04)
  - Initial secure release
  - Credential isolation
  - Input validation
  - Audit logging
  - Rate limiting
  - Granular permissions

## License

MIT License - See LICENSE.md for details

## Contributing

Security is the top priority. All contributions must:
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
