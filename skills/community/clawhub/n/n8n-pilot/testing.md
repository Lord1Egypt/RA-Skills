# Testing Strategy — n8n

Comprehensive testing approach for n8n workflows: validation, mock data, pre-deployment checklists, and chaos testing.

---

## Pre-Deployment Checklist

Before activating ANY workflow, verify:

- [ ] **Structure validated** — all nodes have name, type, valid connections
- [ ] **Dangerous patterns scanned** — no infinite loops, unfiltered deletes, unsecured webhooks
- [ ] **Credentials assigned** — no nodes requiring credentials that are unconfigured
- [ ] **Test data prepared** — `pinData` or test input JSON ready
- [ ] **Error handling present** — Error Trigger workflow or per-node error branches
- [ ] **Deployed inactive** — workflow created but NOT yet activated
- [ ] **Manual test run** — executed with test data, output verified
- [ ] **Error paths tested** — intentionally trigger failure conditions
- [ ] **Rate limits checked** — no API calls exceeding service limits
- [ ] **Execution timeout set** — `settings.executionTimeout` configured for long-running workflows

---

## Validation

### Structure Validation

```bash
# Validate workflow JSON structure
python3 scripts/n8n_tester.py validate --file workflow.json --pretty

# Validate existing workflow
python3 scripts/n8n_tester.py validate --id <workflow-id> --pretty
```

### What to Check Manually

1. **Every node has a name and type**
2. **All connections point to existing nodes** — no orphaned connections
3. **At least one trigger node** — Manual, Webhook, Schedule, or Error Trigger
4. **No disconnected nodes** — every node should be reachable from a trigger
5. **Webhook paths are unique** — no path conflicts with other workflows
6. **Credential types match node requirements**

### Common Structural Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Node X has no type" | Missing `type` field | Add node type |
| "Connection target Y not found" | Typo in node name | Fix connection target |
| "No trigger node" | Workflow starts with action node | Add Manual/Schedule/Webhook trigger |
| "Circular dependency" | Node A → B → A | Break the cycle with a Merge or restructure |

---

## Mock Data with pinData

`pinData` allows testing nodes without the trigger actually firing. Define mock input data per node.

```json
{
  "name": "My Workflow",
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": { "path": "test-webhook" }
    },
    {
      "name": "Process Data",
      "type": "n8n-nodes-base.code",
      "parameters": { "jsCode": "// process data" }
    }
  ],
  "pinData": {
    "Webhook": [
      {
        "json": {
          "email": "test@example.com",
          "subject": "Urgent: Server down",
          "body": "Production server not responding..."
        }
      },
      {
        "json": {
          "email": "newsletter@tech.com",
          "subject": "Weekly Tech Digest",
          "body": "This week in tech..."
        }
      }
    ]
  }
}
```

**How to use pinData:**
1. Define mock data in `pinData` for the trigger node
2. Click the trigger node in the editor — it shows pinned data
3. Execute from that node — downstream nodes use the mock data
4. Remove `pinData` before going live

### Testing with Manual Execution

```bash
# Execute workflow with test data
python3 scripts/n8n_api.py execute --id <workflow-id> \
  --data '{"email": "test@example.com", "subject": "Test"}'

# Check execution result
python3 scripts/n8n_api.py get-execution --id <execution-id> --pretty
```

**⚠️ Note:** n8n has no native dry-run mode. `execute_workflow` runs the workflow for real. Always:
1. Deploy workflows in **inactive** state
2. Test with **manual trigger** only
3. Verify output before activating

---

## Test Execution Strategy

### Level 1: Structure Test (Automated)

Validate JSON structure, connections, and node types:
```bash
python3 scripts/n8n_tester.py validate --file workflow.json --pretty
```

### Level 2: Mock Data Test (Manual)

1. Add `pinData` to trigger node
2. Execute from trigger node in editor
3. Verify each node's output matches expectations
4. Check data flows correctly through branches

### Level 3: Live Test (Staged)

1. Deploy workflow in **inactive** state
2. Use manual trigger with real test data:
   ```bash
   python3 scripts/n8n_api.py execute --id <id> --data '{"test": true"}'
   ```
3. Check execution result for correct output
4. Verify no unintended side effects (no emails sent, no data deleted)

### Level 4: Error Path Testing

Intentionally trigger failure conditions:
- Send invalid input (missing fields, wrong types)
- Temporarily break a credential (wrong API key)
- Simulate API timeout (set a very short timeout on HTTP Request)
- Verify error branches execute correctly and notifications fire

---

## Chaos Testing

### Purpose

Verify that workflows handle unexpected failures gracefully — not just happy paths.

### Test Scenarios

| Scenario | How to Simulate | Expected Behavior |
|----------|----------------|-------------------|
| API down | Set HTTP Request URL to non-existent endpoint | Error branch fires, notification sent |
| Rate limited | Set API to return 429 | Retry logic triggers (if implemented), fallback after max retries |
| Invalid input | Send data with missing/invalid fields | Validation rejects, error response sent |
| Timeout | Set very short timeout (1ms) on HTTP Request | Timeout error caught, fallback executed |
| Large payload | Send 10MB JSON body | Workflow handles or gracefully rejects |
| Concurrent execution | Trigger workflow 5 times simultaneously | No race conditions, no data corruption |
| Database connection loss | Stop database container mid-workflow | Error workflow fires, no data loss |
| Credential expiry | Use expired OAuth token | Refresh token logic works, or clear error message |

### Chaos Test Implementation

```javascript
// Code node — inject chaos for testing
const CHAOS_MODE = $env.CHAOS_MODE || 'none';

if (CHAOS_MODE === 'timeout') {
  // Simulate slow API
  await new Promise(resolve => setTimeout(resolve, 30000));
}

if (CHAOS_MODE === 'error') {
  // Simulate API error
  throw new Error('Simulated API failure: 500 Internal Server Error');
}

if (CHAOS_MODE === 'invalid_data') {
  // Simulate malformed response
  return [{ json: { invalid: true, missing_required_field: true } }];
}

// Normal flow
return $input.all();
```

---

## Workflow Doctor

### Diagnosing a Broken Workflow

1. **Check execution status:**
   ```bash
   python3 scripts/n8n_api.py list-executions --id <workflow-id> --limit 5 --pretty
   ```

2. **Get error details:**
   ```bash
   python3 scripts/n8n_api.py get-execution --id <execution-id> --pretty
   ```

3. **Common failure patterns:**

| Error | Likely Cause | Fix |
|-------|-------------|-----|
| "Credential not found" | Credential deleted or expired | Re-create credential, re-assign to node |
| "Connection refused" | External service down | Check service health, add retry logic |
| "Timeout" | API slow or unreachable | Increase timeout, add fallback |
| "Rate limit exceeded" | Too many requests | Add Wait nodes between calls, implement backoff |
| "Invalid JSON" | External API changed response format | Update parsing logic, add error handling |
| "Node not found" | Community node not installed | `npm install` + restart |
| "Maximum call stack exceeded" | Circular workflow | Break cycle with Merge or restructure |

4. **Performance analysis:**
   ```bash
   python3 scripts/n8n_optimizer.py analyze --id <workflow-id> --days 7 --pretty
   ```

### Quick Fixes

- **Workflow stuck in running:** Deactivate → check for infinite loops → add timeout → reactivate
- **Intermittent failures:** Add retry logic (Code node with exponential backoff) + error handling
- **Slow execution:** Check for sequential API calls that could run in parallel + add batch processing
- **Memory issues:** Add Split In Batches to process large datasets in chunks