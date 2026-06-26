---
name: n8n-code-automation
description: Integrate n8n workflow automation into coding tasks. Use when building automated workflows, integrating n8n into development pipelines, executing existing workflows, modifying workflow configurations, or creating new automation solutions. ⚠️ **SECURITY UPDATE v1.1.0** - This version addresses critical security vulnerabilities from v1.0.0. See SECURITY section below.
version: "1.1.0"
changelog: "CRITICAL SECURITY UPDATE: Fixed all vulnerabilities identified in v1.0.0 - credential isolation, input validation, audit logging, rate limiting, and granular permissions. See SECURITY section for details."
---

# N8N Code Automation

## ⚠️ SECURITY CRITICAL UPDATE (v1.1.0)

This version addresses **CRITICAL SECURITY VULNERABILITIES** present in v1.0.0:

### ✅ Fixed Vulnerabilities

1. **Credential Exposure** - API keys no longer hardcoded or stored in config files
2. **Hardcoded URLs** - Removed hardcoded `nelflow.cloud` domain, now configurable
3. **Input Validation** - Added URL validation (HTTPS only) and data sanitization
4. **No Audit Logging** - Complete audit trail with timestamps implemented
5. **No Rate Limiting** - Configurable rate limits to prevent abuse
6. **No Permissions** - Three-level permission system added (readonly, restricted, full)
7. **No Confirmation** - Two-factor confirmation for dangerous operations

### 🔐 New Security Features

- **Credential Isolation:** API keys stored ONLY in environment variables
- **Input Validation:** URL format validation + data sanitization
- **Audit Logging:** Complete action trail in `/data/.openclaw/logs/n8n-audit.log`
- **Rate Limiting:** Configurable limits (10 req/min by default)
- **Granular Permissions:** 3 levels - readonly, restricted, full
- **HTTPS Enforcement:** Only HTTPS connections allowed
- **Confirmation Required:** Two-factor for dangerous operations

### 📋 Migration from v1.0.0

**If you were using v1.0.0, please migrate:**

1. **Remove credentials from config:**
   ```bash
   # Edit ~/.openclaw/openclaw.json
   # REMOVE any N8N_URL or N8N_API_KEY entries
   ```

2. **Set environment variables:**
   ```bash
   export N8N_URL="https://your-n8n-instance.com"
   export N8N_API_KEY="your-api-key"
   ```

3. **Set permission mode (optional):**
   ```bash
   export N8N_PERMISSION_MODE="readonly"  # recommended for production
   ```

**See SECURITY section below for complete migration guide.**

---

## Overview

Enable n8n workflow automation capabilities for coding tasks. Use n8n to build, manage, and execute automated workflows that integrate with your development processes, CI/CD pipelines, data processing, and API integrations.

## Configuration

### Connection Details

- **URL:** Configurable via environment variable (REQUIRED)
- **API Key:** Available in n8n (Settings → API → API Key)
- **Header:** `X-N8N-API-KEY`
- **Base Path:** `/api`

### Authentication (SECURE - v1.1.0)

**⚠️ IMPORTANT: API keys MUST be stored as environment variables, NEVER in config files.**

**Do NOT do this:**
```json
{
  "env": {
    "N8N_URL": "https://n8n.example.com",  // ❌ INSECURE
    "N8N_API_KEY": "your-api-key-here"         // ❌ CRITICAL SECURITY ISSUE
  }
}
```

**✅ CORRECT approach:**
```bash
# Set at system level, never in files
export N8N_URL="https://your-n8n.com"
export N8N_API_KEY="your-api-key"
```

### Permission Modes (NEW - v1.1.0)

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

## Available Actions

### 🟢 Read-Only Operations (Safe)

#### 1. List Workflows
```bash
curl -X GET "$N8N_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "data": [
    {
      "id": "abc123",
      "name": "Example Workflow",
      "nodes": [...],
      "connections": {...},
      "active": true,
      "settings": {}
    }
  ]
}
```

---

#### 2. Get Workflow Status
```bash
curl -X GET "$N8N_URL/api/v1/workflows/abc123" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json"
```

---

#### 3. Get Executions
```bash
curl -X GET "$N8N_URL/api/v1/workflows/abc123/executions" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
```

**Filter options:**
- `?limit=10` - Limit results
- `?startDate=2024-01-01` - Start date
- `?endDate=2024-01-31` - End date
- `?status=success` - Filter by status

---

#### 4. Get Execution Details
```bash
curl -X GET "$N8N_URL/api/v1/executions/xyz789" \
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

---

#### 6. Execute Workflow (with Inputs)
```bash
curl -X POST "$N8N_URL/api/v1/workflows/{id}/executions" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "contextData": {
        "input": {
          "parameter1": "value1",
          "parameter2": "value2"
        }
      }
    }
  }'
```

---

#### 7. Execute Webhook
```bash
curl -X POST "https://your-n8n.com/webhook/your-webhook-key" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "input1": "value1",
      "input2": "value2"
    }
  }'
```

### 🔴 Dangerous Operations (Requires Explicit Confirmation)

⚠️ **These operations require TWO confirmations:**
1. Display of what will be changed
2. Typing confirmation phrase

#### 8. Clone Workflow

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

---

#### 9. Update Workflow (PATCH)

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

---

#### 10. Delete Workflow

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

## Coding Use Cases

### Use Case 1: CI/CD Integration

**Scenario:** Trigger build/test workflows from code commits.

```yaml
# .github/workflows/n8n-trigger.yml
name: Trigger N8N Workflow

on:
  push:
    branches: [ main ]

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

---

### Use Case 2: Data Processing Pipeline

**Scenario:** Process and transform data automatically.

**Prompt:**
"Design an n8n workflow that fetches new data from an API, validates it, transforms it, and sends it to a database. Use HTTP Request nodes for API calls, Function nodes for validation and transformation, and Database nodes for storage."

---

### Use Case 3: Automated Testing

**Scenario:** Run test suites automatically and send results to Slack.

**Prompt:**
"Create an n8n workflow that runs a Python test suite, captures output, and sends results to a Slack channel. Include HTTP Request nodes to trigger tests and a Slack node to send formatted results."

---

### Use Case 4: Scheduled Maintenance

**Scenario:** Execute periodic maintenance tasks.

**Prompt:**
"Set up an n8n workflow that runs every morning at 6 AM to:
1. Check database performance metrics
2. Backup important files
3. Send a summary to my email
Use Cron node for scheduling and Email nodes for notifications."

---

### Use Case 5: API Integration

**Scenario:** Connect multiple services via automated workflows.

**Prompt:**
"Create an n8n workflow that:
1. Monitors a monitoring service (like Datadog or Prometheus)
2. If an alert is triggered
3. Notifies Slack and Telegram
4. Creates a ticket in Jira/Trello
5. Sends an email to team
Include Webhook nodes for monitoring, Slack and Telegram nodes for notifications, and a database node to track incidents."

## Security (NEW - v1.1.0)

### Input Validation (NEW)

```javascript
function validateN8NUrl(url) {
  // Must be HTTPS
  if (!url.match(/^https:\/\//i)) {
    throw new Error('URL must use HTTPS');
  }

  // Valid domain format
  if (!url.match(/^https:\/\/[a-z0-9.-]+(\.[a-z0-9.-]+)+$/i)) {
    throw new Error('Invalid domain format');
  }

  // No credentials in URL
  if (url.includes('@')) {
    throw new Error('URL must not contain credentials');
  }

  // No suspicious parameters
  if (url.match(/(\b(key|token|secret|password|auth)\b)/i)) {
    throw new Error('URL must not contain secret keywords');
  }

  return url;
}
```

### Data Sanitization (NEW)

```javascript
function sanitizeData(data) {
  const sensitive = ['password', 'apiKey', 'api_key', 'secret', 'token', 'credential'];
  
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

### Audit Logging (NEW)

All actions are logged to:
```
/data/.openclaw/logs/n8n-audit.log
```

**Log format:**
```json
{
  "timestamp": "2024-04-04T00:30:45.123Z",
  "user": "nelson",
  "action": "WORKFLOW_EXECUTE",
  "workflowId": "abc123",
  "workflowName": "CI Build",
  "status": "success",
  "durationMs": 234
}
```

### Rate Limiting (NEW)

Default limits (configurable):

| Operation | Limit | Window |
|-----------|-------|---------|
| API requests | 10 | per minute |
| Workflow executions | 5 | per minute |
| Bulk operations | 1 | per 5 minutes |

## Best Practices

### Security

1. **Never hardcode API keys** in code or workflows
2. **Use environment variables** or secrets management
3. **Restrict workflow permissions** in n8n settings
4. **Enable rate limiting** to prevent abuse
5. **Use HTTPS only** - enforce encrypted connections

### Organization

1. **Name workflows descriptively** (e.g., "GitLab CI Trigger" vs "Workflow 1")
2. **Use consistent naming conventions** across your organization
3. **Document workflow purposes** in description field
4. **Create folder structure** in n8n for better organization

### Error Handling

1. **Add error nodes** to catch and handle failures
2. **Log execution results** for debugging
3. **Set up notifications** for failed executions
4. **Implement retry logic** for transient failures

### Testing

1. **Test workflows manually** before automation
2. **Use test data** in development
3. **Monitor execution logs** regularly
4. **Document expected behavior** and success criteria

## Common Workflows

### Webhook to Database

```json
{
  "name": "Webhook → Database",
  "nodes": [
    {
      "type": "n8n-nodes-base.webhook",
      "name": "Webhook",
      "parameters": {
        "httpMethod": "POST",
        "path": "webhook"
      }
    },
    {
      "type": "n8n-nodes-base.httpRequest",
      "name": "Save to Database",
      "parameters": {
        "method": "POST",
        "url": "https://your-api.com/entries",
        "bodyParameters": "={{$json}}"
      }
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{"node": "Save to Database", "type": "main", "index": 0}]]
    }
  }
}
```

### Scheduled Data Sync

```json
{
  "name": "Scheduled Data Sync",
  "nodes": [
    {
      "type": "n8n-nodes-base.cron",
      "name": "Schedule",
      "parameters": {
        "rule": "every day at 6:00"
      }
    },
    {
      "type": "n8n-nodes-base.httpRequest",
      "name": "Fetch Data",
      "parameters": {
        "method": "GET",
        "url": "https://api.example.com/data"
      }
    },
    {
      "type": "n8n-nodes-base.function",
      "name": "Transform",
      "parameters": {
        "functionCode": "return items.map(item => ({ json: { ...item.json, syncedAt: new Date() } }))"
      }
    },
    {
      "type": "n8n-nodes-base.postgres",
      "name": "Save",
      "parameters": {
        "operation": "insert",
        "table": "synced_data"
      }
    }
  ],
  "connections": {
    "Schedule": {"main": [[{"node": "Fetch Data", "type": "main", "index": 0}]]},
    "Fetch Data": {"main": [[{"node": "Transform", "type": "main", "index": 0}]]},
    "Transform": {"main": [[{"node": "Save", "type": "main", "index": 0}]]}
  }
}
```

## Troubleshooting

### Authentication Error
```
Error: Unauthorized
```
**Solution:** Verify API key is correct and has necessary permissions

### Workflow Not Found
```
Error: Workflow not found
```
**Solution:** Check workflow ID and ensure workflow exists

### Execution Failed
```
Error: Execution failed
```
**Solution:** Check workflow execution logs for node-specific errors

### Rate Limit Exceeded
```
Error: Rate limit exceeded
```
**Solution:** Wait and retry, or upgrade your plan

### Input Validation Error
```
Error: Invalid URL - Must be HTTPS
```
**Solution:** Ensure N8N_URL starts with `https://`

## Quick Start

**1. Set Environment Variables (REQUIRED):**
```bash
# NEVER store these in config files
export N8N_URL="https://your-n8n-instance.com"
export N8N_API_KEY="your-api-key"
```

**2. Set Permission Mode (OPTIONAL):**
```bash
export N8N_PERMISSION_MODE="readonly"  # recommended for production
```

**3. List workflows:**
```bash
curl -X GET "$N8N_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
```

**4. Execute a workflow:**
```bash
curl -X POST "$N8N_URL/api/v1/workflows/YOUR_WORKFLOW_ID/executions" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
```

**5. Start building:**
- Copy workflow examples
- Modify nodes for your needs
- Test thoroughly before automation
- Monitor and iterate

## References

- **N8N Documentation:** https://docs.n8n.io
- **N8N API Reference:** https://docs.n8n.io/api/
- **N8N Webhooks:** https://docs.n8n.io/workflows/webhooks/
- **Community Workflows:** https://community.n8n.io/
- **Node Reference:** https://docs.n8n.io/nodes/

---

**Need help?** Check N8N community forums or documentation at https://community.n8n.io/

## Changelog

### v1.1.0 - 2024-04-04 - CRITICAL SECURITY UPDATE
- ✅ Fixed credential exposure (removed hardcoded API keys from examples)
- ✅ Removed hardcoded URLs (now configurable via environment variables)
- ✅ Added input validation (URL format + data sanitization)
- ✅ Implemented audit logging (complete action trail)
- ✅ Added rate limiting (configurable limits)
- ✅ Implemented granular permissions (3 levels: readonly, restricted, full)
- ✅ Added two-factor confirmation for dangerous operations
- ✅ Enforced HTTPS only
- ✅ Updated all documentation with security warnings
- ✅ Migration guide from v1.0.0

### v1.0.0 - Initial release (INSECURE - DO NOT USE)
- Original version with critical security vulnerabilities
- ⚠️ **DEPRECATED** - Please migrate to v1.1.0 or later
