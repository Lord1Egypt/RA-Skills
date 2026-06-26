---
name: n8n-code-automation
description: Integrate n8n workflow automation into coding tasks. Use when building automated workflows, integrating n8n into development pipelines, executing existing workflows, modifying workflow configurations, or creating new automation solutions. Triggers on phrases like "create n8n workflow", "run n8n workflow", "integrate n8n", "automate with n8n", "modify n8n workflow", "execute workflow".
---

# N8N Code Automation

## Overview

Enable n8n workflow automation capabilities for coding tasks. Use n8n to build, manage, and execute automated workflows that integrate with your development processes, CI/CD pipelines, data processing, and API integrations.

## Configuration

### Connection Details

- **URL:** https://n8n.nelflow.cloud
- **API Key:** Available in n8n (Settings → API → API Key)
- **Header:** `X-N8N-API-KEY`
- **Base Path:** `/api`

### Authentication

Add to OpenClaw configuration (`~/.openclaw/openclaw.json`):

```json
{
  "env": {
    "N8N_URL": "https://n8n.nelflow.cloud",
    "N8N_API_KEY": "your-api-key-here"
  }
}
```

## Available Actions

### 1. List Workflows

List all workflows on your n8n instance.

**Command:**
```bash
curl -X GET "https://n8n.nelflow.cloud/api/v1/workflows" \
  -H "X-N8N-API-KEY: your-api-key" \
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

### 2. Execute Workflow (Manual)

Execute a workflow by triggering it manually.

**Command:**
```bash
curl -X POST "https://n8n.nelflow.cloud/api/v1/workflows/abc123/executions" \
  -H "X-N8N-API-KEY: your-api-key" \
  -H "Content-Type: application/json"
```

**Parameters (optional):**
```json
{
  "data": {
    "contextData": {},
    "manualExecution": true
  }
}
```

---

### 3. Execute Workflow (with Inputs)

Execute a workflow with specific input data.

**Command:**
```bash
curl -X POST "https://n8n.nelflow.cloud/api/v1/workflows/abc123/executions" \
  -H "X-N8N-API-KEY: your-api-key" \
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

### 4. Get Workflow Status

Check if a workflow is active and view execution history.

**Command:**
```bash
curl -X GET "https://n8n.nelflow.cloud/api/v1/workflows/abc123" \
  -H "X-N8N-API-KEY: your-api-key" \
  -H "Content-Type: application/json"
```

---

### 5. Clone Workflow

Create a copy of an existing workflow.

**Command:**
```bash
curl -X POST "https://n8n.nelflow.cloud/api/v1/workflows/abc123/clone" \
  -H "X-N8N-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cloned Workflow"
  }'
```

---

### 6. Update Workflow

Modify an existing workflow (PUT replaces entire workflow, PATCH updates specific parts).

**Command (PUT - Replace):**
```bash
curl -X PUT "https://n8n.nelflow.cloud/api/v1/workflows/abc123" \
  -H "X-N8N-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Workflow Name",
    "nodes": [...],
    "connections": {...}
  }'
```

**Command (PATCH - Update parts):**
```bash
curl -X PATCH "https://n8n.nelflow.cloud/api/v1/workflows/abc123" \
  -H "X-N8N-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "nodes": [
      {
        "parameters": {...}
      }
    ]
  }'
```

---

### 7. Delete Workflow

Remove a workflow (requires admin permission).

**Command:**
```bash
curl -X DELETE "https://n8n.nelflow.cloud/api/v1/workflows/abc123" \
  -H "X-N8N-API-KEY: your-api-key"
```

**Confirmation:**
Enter confirmation message or type `confirm` to proceed.

---

### 8. Get Executions

List workflow executions and their status.

**Command:**
```bash
curl -X GET "https://n8n.nelflow.cloud/api/v1/workflows/abc123/executions" \
  -H "X-N8N-API-KEY: your-api-key"
```

**Filter options:**
- `?limit=10` - Limit results
- `?startDate=2024-01-01` - Start date
- `?endDate=2024-01-31` - End date
- `?status=success` - Filter by status

---

### 9. Get Execution Details

Get detailed information about a specific execution.

**Command:**
```bash
curl -X GET "https://n8n.nelflow.cloud/api/v1/executions/xyz789" \
  -H "X-N8N-API-KEY: your-api-key"
```

---

### 10. Execute Webhook

Trigger a workflow via webhook URL.

**Command:**
```bash
curl -X POST "https://n8n.nelflow.cloud/webhook/your-webhook-key" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "input1": "value1",
      "input2": "value2"
    }
  }'
```

---

## Coding Use Cases

### Use Case 1: CI/CD Integration

**Scenario:** Trigger build/test workflows from code commits.

**Prompt:**
```
"Create a GitHub Actions workflow that triggers the n8n workflow 'CI Build' after a successful commit. The workflow should accept the commit SHA and repository URL as parameters."
```

**Implementation:**
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
        run: |
          curl -X POST "https://n8n.nelflow.cloud/api/v1/workflows/YOUR_WORKFLOW_ID/executions" \
            -H "X-N8N-API-KEY: ${{ secrets.N8N_API_KEY }}" \
            -H "Content-Type: application/json" \
            -d "{\"data\": {\"contextData\": {\"commitSha\": \"${{ github.sha }}\", \"repoUrl\": \"${{ github.server_url }}/${{ github.repository }}\"}}}"
```

---

### Use Case 2: Data Processing Pipeline

**Scenario:** Process and transform data automatically.

**Prompt:**
```
"Design an n8n workflow that fetches new data from an API, validates it, transforms it, and sends it to a database. Use HTTP Request nodes for API calls, Function nodes for validation and transformation, and Database nodes for storage."
```

---

### Use Case 3: Automated Testing

**Scenario:** Run test suites automatically and send results to Slack.

**Prompt:**
```
"Create an n8n workflow that runs a Python test suite, captures the output, and sends the results to a Slack channel. Include HTTP Request nodes to trigger tests and a Slack node to send formatted results."
```

---

### Use Case 4: Scheduled Maintenance

**Scenario:** Execute periodic maintenance tasks.

**Prompt:**
```
"Set up an n8n workflow that runs every morning at 6 AM to:
1. Check database performance metrics
2. Backup important files
3. Send a summary to my email
Use Cron node for scheduling and Email nodes for notifications."
```

---

### Use Case 5: API Integration

**Scenario:** Connect multiple services via automated workflows.

**Prompt:**
```
"Create an n8n workflow that:
1. Monitors a monitoring service (like Datadog or Prometheus)
2. If an alert is triggered
3. Notifies Slack and Telegram
4. Creates a ticket in Jira/Trello
5. Sends an email to the team
Include Webhook nodes for monitoring, Slack and Telegram nodes for notifications, and a database node to track incidents."
```

---

## Best Practices

### Security

1. **Never hardcode API keys** in code or workflows
2. **Use environment variables** or secrets management
3. **Restrict workflow permissions** in n8n settings
4. **Enable rate limiting** to prevent abuse

### Organization

1. **Name workflows descriptively** (e.g., "GitLab CI Trigger" vs "Workflow 1")
2. **Use consistent naming conventions** across your organization
3. **Document workflow purposes** in the description field
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

---

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

---

## References

- **N8N Documentation:** https://docs.n8n.io
- **N8N API Reference:** https://docs.n8n.io/api/
- **N8N Webhooks:** https://docs.n8n.io/workflows/webhooks/
- **Community Workflows:** https://community.n8n.io/
- **Node Reference:** https://docs.n8n.io/nodes/

---

## Quick Start

**1. Get your API Key:**
- Go to n8n → Settings → API → Create API Key

**2. Configure OpenClaw:**
```bash
# Set environment variables
export N8N_URL="https://n8n.nelflow.cloud"
export N8N_API_KEY="your-api-key"
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

---

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

---

**Need help?** Check N8N community forums or documentation at https://community.n8n.io/
