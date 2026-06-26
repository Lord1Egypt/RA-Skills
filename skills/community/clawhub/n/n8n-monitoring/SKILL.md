---
name: n8n-monitor
description: Monitor and debug n8n workflow executions via webhook. Provides health checks (GREEN/YELLOW/RED), failure analysis, error debugging, and formatted alerting templates for Telegram or other channels.
---

# n8n Monitor Skill

Monitor your self-hosted n8n instance through a webhook-based API. Get health reports, detect failing workflows, and debug errors using structured data from your n8n executions.

## Quick Workflow

1. Call the webhook with `{"action": "get_workflow_executions", "limit": 50}` to get a health overview
2. Check the `summary.failureRate` to determine status: GREEN (<10%), YELLOW (10-25%), RED (>25%)
3. If failures exist, check `workflowPerformance.topProblematicWorkflows` for the worst offenders
4. For deep debugging, call `{"action": "get_execution_details", "limit": 5, "workflow_id": "<ID>"}` to get error messages and failed nodes

## Available Endpoints

All endpoints are POST requests to the `N8N_WEBHOOK_URL` environment variable.

### get_active_workflows

Returns all active workflows with IDs, names, and metadata.

```json
{"action": "get_active_workflows"}
```

### get_workflow_executions

Returns recent executions with computed KPIs: failure rate, timing metrics, per-workflow performance, alerts.

```json
{"action": "get_workflow_executions", "limit": 50}
```

**Key response fields:**
- `summary.totalExecutions`, `summary.failureRate`, `summary.successRate`
- `timing.averageExecutionTime`, `timing.minExecutionTime`, `timing.maxExecutionTime`
- `workflowPerformance.topProblematicWorkflows` (sorted by failure rate)
- `alerts.highFailureRate` (boolean), `alerts.workflowsNeedingAttention` (list)

### get_execution_details

Returns detailed error data for a specific workflow: error messages, failed node names and types, timestamps.

```json
{"action": "get_execution_details", "limit": 5, "workflow_id": "<WORKFLOW_ID>"}
```

## Health Thresholds

| Status | Failure Rate | Action |
|--------|-------------|--------|
| GREEN  | < 10%       | No action needed |
| YELLOW | 10-25%      | Investigate flagged workflows |
| RED    | > 25%       | Immediate attention required |

## Notification Templates

### One-Line Summary

```
n8n <EMOJI> | failure <RATE>% (<N> exec) | <NOTE>
```

### Quick Status (for cron/heartbeat)

```
n8n monitor (<TIME> UTC) -> <EMOJI> <STATUS>

Hot spots:
<EMOJI> <WORKFLOW_NAME> - "<ERROR_MESSAGE>" (<FAILED_NODE> node)
```

### Full Report

Combine all three endpoints for a complete picture:
1. Active workflows summary (count, categories)
2. Health status with KPIs (failure rate, timing, execution modes)
3. Hot spots table (per-workflow failure rates)
4. Error details for critical workflows
5. Alerts and recommended actions

## Recommended Monitoring Patterns

### Automated Cron Monitoring
- Run a monitor script every 30 minutes that calls `get_workflow_executions`
- Log health status to a file
- Use a heartbeat (e.g., every hour at :32) to read the log and send alerts only when status is YELLOW or RED
- Stay quiet when everything is GREEN

### On-Demand Debugging
- Call `get_workflow_executions` to identify which workflows are failing
- Note the workflow ID
- Call `get_execution_details` with that ID for error patterns and failed node info

### Alert Deduplication
- Hash each alert payload
- Only notify when the hash changes (new error or status change)
- Prevents notification fatigue when the same error persists

## Environment

- `N8N_WEBHOOK_URL`: Your n8n webhook endpoint (required)
- Webhook timeout: 30 seconds (use lower `limit` values for large instances)

## Prompts That Work Well

- "Check the health of my n8n instance"
- "Which workflows are failing?"
- "Debug errors in workflow <ID>"
- "Generate a health report for the last 100 executions"
- "What's causing failures in my data processing workflow?"

## Failure Modes

- **Webhook timeout**: Reduce the `limit` parameter
- **Authorization errors**: Check n8n API credentials in the webhook workflow
- **Empty results**: Verify the webhook workflow is active and the URL is correct
