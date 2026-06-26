# n8n Monitor Skill for OpenClaw

Monitor and debug your self-hosted n8n workflow executions with automated health checks and Telegram alerts.

## How It Works

This skill connects OpenClaw to your n8n instance through a webhook workflow. The webhook exposes three endpoints that return structured execution data, which OpenClaw uses to generate health reports, detect failures, and debug errors.

```
OpenClaw (heartbeat/cron)
    |
    v
n8n Webhook Workflow (3 routes)
    |
    v
n8n API (executions, workflows)
    |
    v
Structured KPIs returned to OpenClaw
    |
    v
Formatted alert sent to Telegram
```

## Setup

### Step 1: Import the n8n Webhook Workflow

Import the monitoring workflow template into your n8n instance:

**Template:** https://n8n.supply-science.com/workflows/DevOps/AI_Agent_for_Debugging_Workflow_Executions

This workflow exposes a single POST webhook with three routes:

| Action | What it returns |
|--------|----------------|
| `get_active_workflows` | List of all active workflows (id, name, timestamps) |
| `get_workflow_executions` | Recent executions with computed KPIs (failure rate, timing, per-workflow metrics) |
| `get_execution_details` | Detailed error data for a specific workflow (error messages, failed nodes) |

After importing:
1. Open the workflow in your n8n editor
2. Replace the n8n API URL with your own instance URL in the HTTP Request nodes
3. Configure the n8n API credentials
4. Activate the workflow
5. Copy the webhook URL (production URL, not test)

For a full walkthrough, watch the video tutorial: https://youtu.be/oJzNnHIusZs

### Step 2: Set the Environment Variable

Add the webhook URL to your OpenClaw workspace `.env` file:

```
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/your-webhook-id
```

### Step 3: Install the Skill

```bash
openclaw skill install n8n-monitor
```

### Step 4: Configure Monitoring (Optional)

For automated monitoring, add a section to your `HEARTBEAT.md`:

```markdown
## n8n Monitoring Log Review

When heartbeats fire:
- Call the webhook with get_workflow_executions (limit: 5)
- If failure rate is GREEN (< 10%), stay quiet
- If YELLOW or RED, send a status update using the quick-status template
- Include hot spots with workflow names, error messages, and failed nodes
```

Or set up a dedicated cron job for more frequent checks.

## Usage

### Ask OpenClaw Directly

Once installed, you can ask OpenClaw to monitor your n8n instance:

- "Check the health of my n8n instance"
- "Which workflows are failing?"
- "Debug errors in workflow CGvCrnUyGHgB7fi8"
- "Generate a health report"

### Automated Alerts

The recommended setup for production:

1. A monitor script runs on a system cron every 30 minutes
2. It calls the webhook, calculates health status, and logs results
3. OpenClaw's heartbeat reads the log every hour
4. If status is YELLOW or RED, a formatted alert is sent to Telegram
5. GREEN status stays quiet (no notification noise)

### Alert Format

```
n8n RED | failure 40.00% (5 exec) | 2 workflows critical

n8n monitor (10:30 UTC) -> RED

Hot spots:
EventBrite - "Issue while executing query" (Merge node)
SCAI Events - "Resource not found" (Query SCAI node)
```

## Health Thresholds

| Status | Failure Rate | Meaning |
|--------|-------------|---------|
| GREEN  | < 10%       | All good, no alert |
| YELLOW | 10-25%      | Some workflows need attention |
| RED    | > 25%       | Critical failures, immediate action |

## Requirements

- A self-hosted n8n instance with API access enabled
- The webhook workflow imported and activated
- `N8N_WEBHOOK_URL` set in your workspace `.env`

## Resources

- **Workflow Template:** https://n8n.supply-science.com/workflows/DevOps/AI_Agent_for_Debugging_Workflow_Executions
- **Video Tutorial:** https://youtu.be/oJzNnHIusZs
- **Original Article:** [Deploy your AI Assistant to Monitor and Debug n8n Workflows using Claude and MCP](https://towardsdatascience.com/deploy-your-ai-assistant-to-monitor-and-debug-n8n-workflows-using-claude-and-mcp/)
- **MCP Server Source:** https://github.com/samirsaci/mcp-n8n-monitor

## Author

Samir Saci - Supply Chain Engineer & Data Scientist
- Website: https://www.samirsaci.com
- LinkedIn: https://www.linkedin.com/in/samir-saci
