# n8n REST API Reference

## Authentication

All requests require the `X-N8N-API-KEY` header:
```bash
curl -H "X-N8N-API-KEY: YOUR_API_KEY" http://localhost:5678/api/v1/...
```

Generate an API key: n8n Settings > API > Create API Key

---

## Workflows

### List Workflows
```
GET /api/v1/workflows
GET /api/v1/workflows?active=true
GET /api/v1/workflows?tags=tag-id
GET /api/v1/workflows?limit=50&cursor=CURSOR
```
Response: `{ "data": [...], "nextCursor": "..." }`

### Get Workflow
```
GET /api/v1/workflows/:id
```
Response: Full workflow JSON including nodes, connections, settings

### Create Workflow
```
POST /api/v1/workflows
Content-Type: application/json

{
  "name": "My Workflow",
  "nodes": [...],
  "connections": {...},
  "settings": { "executionOrder": "v1" }
}
```
Response: Created workflow with assigned `id`

### Update Workflow
```
PUT /api/v1/workflows/:id
Content-Type: application/json

{
  "name": "Updated Name",
  "nodes": [...],
  "connections": {...},
  "settings": { "executionOrder": "v1" }
}
```
IMPORTANT: Send the COMPLETE workflow. Partial updates are not supported.

### Delete Workflow
```
DELETE /api/v1/workflows/:id
```

### Activate Workflow
```
POST /api/v1/workflows/:id/activate
```

### Deactivate Workflow
```
POST /api/v1/workflows/:id/deactivate
```

### Transfer Workflow (tags)
```
PUT /api/v1/workflows/:id/transfer
Content-Type: application/json

{ "destinationProjectId": "project-id" }
```

---

## Executions

### List Executions
```
GET /api/v1/executions
GET /api/v1/executions?workflowId=WORKFLOW_ID
GET /api/v1/executions?status=error
GET /api/v1/executions?status=success
GET /api/v1/executions?limit=10
```
Status options: `error`, `success`, `waiting`, `running`, `new`

### Get Execution
```
GET /api/v1/executions/:id
```
Response includes:
- `status` — error/success/waiting
- `startedAt`, `stoppedAt`
- `data.resultData.runData` — per-node execution data
- `data.resultData.error` — error details if failed
- `workflowId`, `workflowData`

### Delete Execution
```
DELETE /api/v1/executions/:id
```

### Run Workflow
```
POST /api/v1/workflows/:id/run
Content-Type: application/json

{
  "data": { "key": "value" }
}
```
Triggers a manual execution of the workflow. The optional `data` object is passed as input to the first node.
Response: Execution result including `executionId`, `data`, and `finished` status.

Note: The workflow does NOT need to be active to be run via API.

---

## Credentials

### List Credentials
```
GET /api/v1/credentials
```
Response: `{ "data": [{ "id": "...", "name": "...", "type": "..." }] }`

Note: Credential values/secrets are NEVER returned by the API.

### Get Credential Schema
```
GET /api/v1/credentials/schema/:credentialType
```

---

## Tags

### List Tags
```
GET /api/v1/tags
GET /api/v1/tags?limit=50
```

### Create Tag
```
POST /api/v1/tags
Content-Type: application/json

{ "name": "production" }
```

---

## Webhook Testing

To test a webhook-triggered workflow:
```bash
# For POST webhooks:
curl -X POST http://localhost:5678/webhook/YOUR-PATH \
  -H "Content-Type: application/json" \
  -d '{"message": "test data"}'

# For test webhooks (only works while editor is open):
curl -X POST http://localhost:5678/webhook-test/YOUR-PATH \
  -H "Content-Type: application/json" \
  -d '{"message": "test data"}'
```

---

## Common Patterns

### Create and Activate in One Go
```bash
# Create
WORKFLOW_ID=$(curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d @workflow.json \
  http://localhost:5678/api/v1/workflows | jq -r '.id')

# Activate
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  http://localhost:5678/api/v1/workflows/$WORKFLOW_ID/activate
```

### Get Failed Executions for a Specific Workflow
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "http://localhost:5678/api/v1/executions?workflowId=WORKFLOW_ID&status=error&limit=5"
```

### Export All Workflows (Backup)
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  http://localhost:5678/api/v1/workflows | jq '.data' > workflows-backup.json
```
