# n8n OpenClaw Bridge — Automate Everything

Connect your OpenClaw agent to n8n for powerful workflow automation. This skill teaches your agent how to create, trigger, manage, and monitor n8n workflows — turning your AI assistant into a full automation operator.

## When to Use

Use this skill when:
- You want your OpenClaw agent to trigger n8n workflows (send data, kick off automations)
- You need to create n8n workflows from natural language descriptions
- You want your agent to monitor workflow execution and handle errors
- You're building AI-in-the-loop automations (agent decides → n8n executes)
- You want to manage your n8n instance without opening the UI

**Triggers:** "create a workflow", "trigger automation", "n8n workflow", "automate this process", "set up a webhook", "monitor my workflows", "workflow failed"

## Prerequisites

- n8n instance running (local Docker or cloud)
- n8n API key (Settings → API → Create API Key)
- Agent needs the API URL and key stored in environment or TOOLS.md

### Quick Setup

Add to your agent's `TOOLS.md`:
```markdown
## n8n
- **URL:** http://localhost:5678 (or your n8n cloud URL)
- **API Key:** [your-api-key]
- **Version:** 2.x+
```

Or set environment variables:
```bash
export N8N_API_URL="http://localhost:5678"
export N8N_API_KEY="your-api-key-here"
```

## Capabilities

### 1. Workflow Management

#### List Workflows
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_API_URL/api/v1/workflows" | jq '.data[] | {id, name, active}'
```

#### Get Workflow Details
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_API_URL/api/v1/workflows/{id}" | jq '.'
```

#### Activate/Deactivate Workflow
```bash
# Activate
curl -s -X PATCH -H "X-N8N-API-KEY: $N8N_API_KEY" -H "Content-Type: application/json" \
  -d '{"active": true}' "$N8N_API_URL/api/v1/workflows/{id}"

# Deactivate
curl -s -X PATCH -H "X-N8N-API-KEY: $N8N_API_KEY" -H "Content-Type: application/json" \
  -d '{"active": false}' "$N8N_API_URL/api/v1/workflows/{id}"
```

#### Delete Workflow
```bash
curl -s -X DELETE -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_API_URL/api/v1/workflows/{id}"
```

### 2. Trigger Workflows via Webhook

The most common pattern: your agent triggers an n8n workflow by sending data to a webhook.

#### Create a Webhook-Triggered Workflow

When the user says "automate X", build a workflow with a Webhook trigger node:

```json
{
  "name": "Agent-Triggered: [Description]",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "agent-trigger-[unique-id]",
        "responseMode": "lastNode",
        "options": {}
      },
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [250, 300],
      "id": "webhook-node",
      "name": "Agent Webhook"
    }
  ],
  "connections": {},
  "settings": {
    "executionOrder": "v1"
  }
}
```

#### Trigger the Webhook
```bash
curl -s -X POST "$N8N_API_URL/webhook/agent-trigger-[unique-id]" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from OpenClaw", "data": {...}}'
```

### 3. Execution Monitoring

#### List Recent Executions
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_API_URL/api/v1/executions?limit=10&status=error" | jq '.data[] | {id, workflowId, status, startedAt}'
```

#### Get Execution Details (for debugging)
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_API_URL/api/v1/executions/{id}" | jq '.'
```

#### Retry Failed Execution
```bash
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_API_URL/api/v1/executions/{id}/retry"
```

### 4. Create Workflows from Natural Language

When the user describes an automation, translate it to an n8n workflow. Follow these patterns:

#### Pattern: Webhook → Process → Notify
Use for: "When X happens, do Y, then tell me"
```
Webhook Trigger → [Processing Nodes] → Telegram/Slack/Email
```

#### Pattern: Schedule → Collect → Report
Use for: "Every morning, check X and send me a summary"
```
Schedule Trigger → HTTP Request(s) → Function (aggregate) → Message
```

#### Pattern: Webhook → AI → Action
Use for: "When I send data, have AI analyze it and take action"
```
Webhook → OpenAI/Anthropic Node → IF Node → [Action Branches]
```

#### Pattern: Monitor → Alert
Use for: "Watch for errors/changes and alert me"
```
Schedule (every 5min) → HTTP Request → IF (changed?) → Alert
```

### 5. Common Workflow Templates

#### Lead Notification Pipeline
Agent finds a lead → triggers n8n → n8n sends to CRM + sends notification

```bash
# Agent triggers this when it qualifies a lead
curl -s -X POST "$N8N_API_URL/webhook/new-lead" \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Willis Plumbing",
    "contact": "John Willis",
    "email": "john@willisplumbing.com",
    "score": 85,
    "source": "google_maps",
    "notes": "4.2 stars, 180 reviews, no website optimization"
  }'
```

#### Content Publishing Pipeline
Agent writes content → triggers n8n → n8n posts to multiple platforms

```bash
# Agent triggers this when content is approved
curl -s -X POST "$N8N_API_URL/webhook/publish-content" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "5 Ways AI Helps Local Businesses",
    "body": "...",
    "platforms": ["linkedin", "twitter", "blog"],
    "schedule": "2026-03-23T09:00:00Z"
  }'
```

#### Website Monitor
n8n checks competitor sites on schedule, sends changes to agent via webhook

#### Email Digest
n8n collects emails/notifications → sends daily summary to agent's channel

### 6. Building Workflows Programmatically

#### Create a Complete Workflow via API
```bash
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  "$N8N_API_URL/api/v1/workflows" \
  -d @workflow.json
```

#### Workflow JSON Structure
Every n8n workflow follows this structure:
```json
{
  "name": "Workflow Name",
  "nodes": [
    {
      "parameters": {},
      "type": "n8n-nodes-base.nodeName",
      "typeVersion": 1,
      "position": [x, y],
      "id": "unique-id",
      "name": "Display Name"
    }
  ],
  "connections": {
    "Source Node Name": {
      "main": [
        [
          {
            "node": "Target Node Name",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "settings": {
    "executionOrder": "v1"
  }
}
```

**Critical rules for valid workflows:**
- Every workflow needs at least one trigger node
- `connections` reference nodes by their `name` field (not `id`)
- Node positions should be spaced ~200px apart horizontally
- Use `typeVersion` 2 for Webhook nodes (v2 supports response modes)
- Always set `executionOrder: "v1"` in settings

### 7. Credential Management

#### List Available Credentials
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_API_URL/api/v1/credentials" | jq '.data[] | {id, name, type}'
```

**Note:** You can list and reference credentials by ID, but you cannot read credential secrets via the API (security). To use a credential in a workflow node, reference it by ID:
```json
{
  "parameters": {...},
  "credentials": {
    "telegramApi": {
      "id": "1",
      "name": "Telegram Bot"
    }
  }
}
```

## Agent Integration Patterns

### The Dispatch Pattern (Recommended)
Your OpenClaw agent acts as the brain. n8n acts as the hands.

```
User Request → Agent (understands intent, plans) → Triggers n8n Webhook → n8n Executes
                                                                              ↓
User ← Agent (formats response) ← Webhook Callback ← n8n Returns Result
```

**How to implement:**
1. Create n8n workflows with webhook triggers for each automation
2. Store webhook URLs in TOOLS.md
3. Agent decides WHEN to trigger based on context
4. n8n handles the HOW (API calls, data transforms, multi-step processes)

### The Monitor Pattern
n8n runs scheduled checks. When something interesting happens, it notifies the agent.

```
n8n (scheduled) → Checks data source → Changed? → Sends to Agent webhook/channel
                                          ↓
                                     Agent processes notification, decides next action
```

### The Approval Pattern
Agent needs human approval before n8n executes an action.

```
Agent → Asks user for approval (Telegram/Discord) → User approves
  ↓
Agent triggers n8n webhook with approved payload → n8n executes
```

## Error Handling

When a workflow execution fails:

1. **Check execution status** — List recent failed executions
2. **Read error details** — Get the specific execution to see which node failed and why
3. **Common fixes:**
   - Authentication expired → Re-authenticate the credential in n8n UI
   - Rate limited → Add a Wait node before the failing node
   - Data format wrong → Add a Function node to transform data before the failing node
   - Webhook timeout → Increase timeout or use async response mode
4. **Retry** — Use the retry API endpoint
5. **Alert user** — If the workflow is critical and keeps failing

## Best Practices

1. **Name workflows clearly** — Prefix with "Agent:" so you know which ones the agent manages
2. **Use test webhooks first** — n8n provides test webhook URLs; use those during development
3. **Store webhook URLs in TOOLS.md** — The agent needs to know where to send data
4. **Add error handling nodes** — Every workflow should have an Error Trigger node that notifies the agent
5. **Log executions** — Keep execution history enabled for debugging
6. **One workflow per automation** — Don't create mega-workflows; keep them focused
7. **Use environment variables** — Store API keys in n8n's environment, not in workflow nodes
8. **Version your workflows** — Export important workflows as JSON backups

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Webhook not responding | Check workflow is activated (`active: true`) |
| 401 on API calls | Verify API key is correct and has required scopes |
| Workflow creates but won't activate | Check for validation errors in nodes |
| Execution succeeds but no output | Check response mode on webhook (should be `lastNode`) |
| Can't find credential ID | List credentials via API, match by name |
| Connection refused | Verify n8n URL is accessible (Docker networking, firewall) |

## Quick Reference

```bash
# Health check
curl -s "$N8N_API_URL/healthz"

# List all workflows
curl -s -H "X-N8N-API-KEY: $KEY" "$N8N_API_URL/api/v1/workflows" | jq '.data[] | .name'

# Trigger webhook
curl -s -X POST "$N8N_API_URL/webhook/[path]" -H "Content-Type: application/json" -d '{...}'

# Check failed executions
curl -s -H "X-N8N-API-KEY: $KEY" "$N8N_API_URL/api/v1/executions?status=error&limit=5"

# Create workflow from file
curl -s -X POST -H "X-N8N-API-KEY: $KEY" -H "Content-Type: application/json" "$N8N_API_URL/api/v1/workflows" -d @workflow.json
```

---

*Built by Max | Part of the OpenClaw Setup Service ecosystem | https://marlowne12.github.io/openclaw-setup-service/*
