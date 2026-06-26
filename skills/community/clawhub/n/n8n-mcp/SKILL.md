---
name: n8n-mcp
version: "1.1.0"
description: "Operate n8n workflow automation platform via MCP (Model Context Protocol). Use when: (1) Creating, updating, or managing n8n workflows, (2) Executing or testing workflows, (3) Discovering n8n nodes and their types, (4) Managing data tables and projects, (5) Building workflows programmatically with SDK. Triggers on: 'n8n', 'workflow', 'automation', 'create workflow', 'execute workflow'."
metadata:
  openclaw:
    requires:
      env:
        - N8N_MCP_URL
        - N8N_MCP_TOKEN
      services:
        - name: n8n
          version: "2.16.1+"
          url: "http://localhost:5678"
---

# n8n MCP Integration

Connect to n8n's official MCP server to programmatically build, execute, and manage workflows.

## Version Support

- **n8n version**: 2.16.1+
- **MCP protocol**: 2024-11-05
- **Server name**: n8n MCP Server v1.1.0

## Configuration

### MCP Server Setup

In n8n UI:
1. Go to **Settings → n8n API**
2. Create an API key for REST API access
3. Create an MCP token for MCP server access

### Connection Config

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "type": "http",
      "url": "http://localhost:5678/mcp-server/http",
      "headers": {
        "Authorization": "Bearer <MCP_TOKEN>"
      }
    }
  }
}
```

### Environment Variables

```bash
export N8N_MCP_URL="http://localhost:5678/mcp-server/http"
export N8N_MCP_TOKEN="<your-mcp-token>"
```

## Available Tools (25)

### Workflow Management

| Tool | Description |
|------|-------------|
| `search_workflows` | Search workflows with filters (query, projectId, limit) |
| `get_workflow_details` | Get workflow details including trigger info |
| `publish_workflow` | Activate workflow for production execution |
| `unpublish_workflow` | Deactivate workflow |
| `archive_workflow` | Archive a workflow |
| `update_workflow` | Update workflow from validated SDK code |

### Workflow Execution

| Tool | Description |
|------|-------------|
| `execute_workflow` | Execute workflow by ID, returns execution ID immediately |
| `get_execution` | Get execution details and results |
| `test_workflow` | Test workflow with pin data (bypass external services) |
| `prepare_test_pin_data` | Generate test pin data schemas for workflow |

### Workflow Creation (SDK)

| Tool | Description |
|------|-------------|
| `get_sdk_reference` | Get SDK docs, patterns, expressions, functions |
| `search_nodes` | Search n8n nodes by service/type |
| `get_node_types` | Get TypeScript type definitions for nodes |
| `get_suggested_nodes` | Get curated node recommendations by category |
| `validate_workflow` | Validate workflow code before creating |
| `create_workflow_from_code` | Create workflow from validated SDK code |

### Data Tables

| Tool | Description |
|------|-------------|
| `search_data_tables` | Search data tables by name/project |
| `create_data_table` | Create new data table with columns |
| `rename_data_table` | Rename an existing data table |
| `add_data_table_column` | Add column to data table |
| `delete_data_table_column` | Delete column from data table |
| `rename_data_table_column` | Rename a column |
| `add_data_table_rows` | Insert rows into data table (max 1000/call) |

### Projects & Folders

| Tool | Description |
|------|-------------|
| `search_projects` | Search projects by name/type |
| `search_folders` | Search folders within a project |

## Tool Parameters Reference

### search_workflows
```json
{
  "query": "string (optional) - Filter by name or description",
  "projectId": "string (optional) - Filter by project ID",
  "limit": "integer (optional, max 200) - Limit results"
}
```

### execute_workflow
```json
{
  "workflowId": "string (required) - The workflow ID to execute",
  "executionMode": "string (optional) - 'manual' for current version, 'production' for published version",
  "inputs": "object (optional) - Inputs for chat/form/webhook workflows"
}
```

### get_execution
```json
{
  "workflowId": "string (required)",
  "executionId": "string (required)",
  "includeData": "boolean (optional) - Include node execution data",
  "nodeNames": "array (optional) - Filter data by node names",
  "truncateData": "integer (optional) - Limit data items per node"
}
```

### test_workflow
```json
{
  "workflowId": "string (required)",
  "pinData": "object (required) - Pin data for nodes. Keys are node names, values are arrays of items wrapped in 'json': [{\"json\": {\"id\": \"123\"}}]",
  "triggerNodeName": "string (optional) - For multi-trigger workflows"
}
```

### create_workflow_from_code
```json
{
  "code": "string (required) - Validated SDK workflow code",
  "name": "string (optional) - Workflow name",
  "description": "string (optional, max 255 chars)",
  "projectId": "string (optional) - Project ID",
  "folderId": "string (optional) - Folder ID (requires projectId)"
}
```

### search_nodes
```json
{
  "queries": "array (required) - Search queries: service names, trigger types, or utility nodes"
}
```

### get_node_types
```json
{
  "nodeIds": "array (required) - Node IDs or objects with discriminators: [{\"nodeId\": \"...\", \"resource\": \"...\", \"operation\": \"...\"}]"
}
```

### get_suggested_nodes
```json
{
  "categories": "array (required) - Categories: chatbot, notification, scheduling, data_transformation, data_persistence, data_extraction, document_processing, form_input, content_generation, triage, scraping_and_research"
}
```

### get_sdk_reference
```json
{
  "section": "string (optional) - 'patterns', 'expressions', 'functions', 'rules', 'import', 'guidelines', 'design', or 'all' (default)"
}
```

### create_data_table
```json
{
  "projectId": "string (required)",
  "name": "string (required) - Unique table name",
  "columns": "array (required) - Column definitions: [{\"name\": \"...\", \"type\": \"...\"}]"
}
```

### add_data_table_rows
```json
{
  "dataTableId": "string (required)",
  "projectId": "string (required)",
  "rows": "array (required, max 1000) - Row objects: [{\"column1\": \"value1\", \"column2\": \"value2\"}]"
}
```

## Usage Patterns

### 1. Creating a Workflow (Recommended Flow)

```bash
# Step 1: Get SDK reference
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_sdk_reference","arguments":{"section":"all"}}}' \
  "$N8N_MCP_URL"

# Step 2: Get suggested nodes for your use case
curl -X POST ... -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_suggested_nodes","arguments":{"categories":["notification","scheduling"]}}}'

# Step 3: Search specific nodes
curl -X POST ... -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"search_nodes","arguments":{"queries":["schedule trigger","slack","set"]}}}'

# Step 4: Get node types (CRITICAL - don't guess parameter names)
curl -X POST ... -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"get_node_types","arguments":{"nodeIds":["n8n-nodes-base.scheduleTrigger","n8n-nodes-base.slack"]}}}'

# Step 5: Validate workflow code
curl -X POST ... -d '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"validate_workflow","arguments":{"code":"..."}}}'

# Step 6: Create workflow
curl -X POST ... -d '{"jsonrpc":"2.0","id":6,"method":"tools/call","params":{"name":"create_workflow_from_code","arguments":{"code":"...","name":"My Workflow","description":"..."}}}'
```

### 2. Executing and Monitoring a Workflow

```bash
# Execute workflow
curl -X POST ... -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"execute_workflow","arguments":{"workflowId":"xxx"}}}'

# Get execution result (with data)
curl -X POST ... -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_execution","arguments":{"workflowId":"xxx","executionId":"yyy","includeData":true}}}'
```

### 3. Testing a Workflow (Before Publishing)

```bash
# Prepare test pin data
curl -X POST ... -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"prepare_test_pin_data","arguments":{"workflowId":"xxx"}}}'

# Test with pin data (pinData format is CRITICAL)
curl -X POST ... -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"test_workflow","arguments":{"workflowId":"xxx","pinData":{"NodeName":[{"json":{"field":"value"}}]}}}}'
```

### 4. Working with Data Tables

```bash
# Search data tables
curl -X POST ... -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_data_tables","arguments":{"query":"users"}}}'

# Add rows to data table
curl -X POST ... -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"add_data_table_rows","arguments":{"dataTableId":"xxx","projectId":"yyy","rows":[{"name":"John","email":"john@example.com"}]}}}'
```

## SDK Workflow Example

```typescript
import { workflow, trigger, node } from 'n8n-workflow-sdk';

export default workflow({
  name: 'Daily Slack Notification',
  description: 'Send daily summary to Slack',
  nodes: [
    trigger.schedule({
      name: 'Schedule',
      rule: { interval: [{ field: 'hours', hoursInterval: 24 }] }
    }),
    node.set({
      name: 'Prepare Message',
      values: { text: 'Daily report ready!' }
    }),
    node.slack({
      name: 'Send to Slack',
      resource: 'message',
      operation: 'send',
      channel: '#general',
      text: '={{ $node["Prepare Message"].json.text }}'
    })
  ],
  connections: [
    { from: 'Schedule', to: 'Prepare Message' },
    { from: 'Prepare Message', to: 'Send to Slack' }
  ]
});
```

## MCP Protocol Notes

- **Transport**: HTTP with SSE (Server-Sent Events)
- **Content-Type**: `application/json`
- **Accept**: `application/json, text/event-stream` (required)
- **Auth**: Bearer token in Authorization header

## Common Errors

| Error | Solution |
|-------|----------|
| "Not Acceptable" | Add `Accept: application/json, text/event-stream` header |
| "Unauthorized" | Check MCP token is valid |
| "Not found" | Verify MCP server URL is correct |
| Invalid workflow | Always call `validate_workflow` before `create_workflow_from_code` |
| Wrong pinData format | Wrap items in `json`: `[{"json": {...}}]` not `[{}]` |

## Best Practices

1. **Always get SDK reference first** - Call `get_sdk_reference` before building workflows
2. **Use get_node_types** - Never guess parameter names; get exact types from the API
3. **Validate before creating** - Always call `validate_workflow` before `create_workflow_from_code`
4. **Test before publishing** - Use `test_workflow` with pin data to verify workflow logic
5. **Use suggested nodes** - Call `get_suggested_nodes` for curated recommendations by category
6. **Correct pinData format** - Items must be wrapped in `json` property: `[{"json": {...}}]`

## References

- **SDK Reference**: See [references/sdk-patterns.md](references/sdk-patterns.md) for detailed SDK patterns
- **Node Types**: See [references/common-nodes.md](references/common-nodes.md) for frequently used nodes
