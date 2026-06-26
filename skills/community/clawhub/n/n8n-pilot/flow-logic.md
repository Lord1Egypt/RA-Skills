# Flow Logic — n8n

Detailed guide to branching, merging, looping, sub-workflows, and error handling in n8n.

---

## Branching

### IF Node — Binary Decisions

```json
{
  "type": "n8n-nodes-base.if",
  "parameters": {
    "conditions": {
      "boolean": [
        {
          "value1": "={{ $json.status }}",
          "operation": "equal",
          "value2": "active"
        }
      ]
    }
  }
}
```

**Outputs:** `true` (index 0) and `false` (index 1)

**Conditions available:** equal, notEqual, contains, notContains, startsWith, endsWith, regex, gt, lt, gte, lte, between, notBetween, exists, notExists

**Expressions in conditions:** Use `={{ }}` syntax to reference data:
- `={{ $json.fieldName }}` — current item field
- `={{ $itemIndex }}` — current item index
- `={{ $now }}` — current date/time

### Switch Node — Multi-Way Decisions

```json
{
  "type": "n8n-nodes-base.switch",
  "parameters": {
    "rules": [
      {
        "output": 0,
        "conditions": { "string": [{ "value1": "={{ $json.priority }}", "operation": "equal", "value2": "high" }] }
      },
      {
        "output": 1,
        "conditions": { "string": [{ "value1": "={{ $json.priority }}", "operation": "equal", "value2": "medium" }] }
      }
    ],
    "fallbackOutput": 2
  }
}
```

**Fallback output:** Routes items that don't match any rule. Always set this to avoid data loss.

---

## Merging

### Merge Node — Combining Branches

| Mode | Description | Use When |
|------|-------------|----------|
| `append` | Combine all items from all inputs | Simple concatenation |
| `mergeByPosition` | Zip items by index (1st with 1st, 2nd with 2nd) | Matching ordered lists |
| `mergeByKey` | Join on shared field (like SQL JOIN) | Enriching data from different sources |
| `combineByPosition` | Same as mergeByPosition but merges fields | Merging related records |
| `combineByKey` | Same as mergeByKey but merges fields | Combining records with shared key |

**Example — Enriching user data:**
```
Branch A: Fetch users from API (id, name, email)
Branch B: Fetch payment data from DB (user_id, amount)
Merge (mode: mergeByKey, key: id/user_id)
Result: Combined items with user + payment data
```

### Merging Tips

- **Input order matters:** Input 1 is the "primary" dataset. In `mergeByKey`, Input 1 fields take precedence on conflict.
- **Missing matches:** Items without a match are excluded by default. To keep them, use `mergeByKey` with `options.outputUnmatched` = true.
- **Performance:** `append` is fastest. `mergeByKey` requires loading all items into memory for matching.

---

## Looping

### Split In Batches — Recommended for Large Datasets

```json
{
  "type": "n8n-nodes-base.splitInBatches",
  "parameters": {
    "batchSize": 50,
    "options": {
      "reset": false
    }
  }
}
```

**How it works:**
1. Takes all input items
2. Outputs first batch (50 items)
3. Downstream nodes process the batch
4. Loop back to Split In Batches input
5. Outputs next batch
6. When all batches processed, continues to "done" output

**⚠️ ALWAYS set `batchSize`** — without it, all items process at once, which can:
- Exceed API rate limits
- Cause memory exhaustion
- Result in partial failures that are hard to trace

### Loop Over Items — For Small Datasets

```json
{
  "type": "n8n-nodes-base.loopOverItems",
  "parameters": {
    "batchSize": 1
  }
}
```

Processes items one at a time. Simpler than Split In Batches but less efficient for large datasets.

### Manual Loop with Code Node (for pagination)

```javascript
// Fetch all pages from a paginated API
const items = [];
let cursor = null;
let hasMore = true;

while (hasMore) {
  const url = cursor
    ? `https://api.example.com/items?cursor=${cursor}`
    : `https://api.example.com/items`;

  const response = await this.helpers.httpRequest({
    url,
    method: 'GET',
    headers: { 'Authorization': 'Bearer xxx' },
  });

  items.push(...response.items);

  if (response.next_cursor && items.length < 10000) { // Safety limit
    cursor = response.next_cursor;
  } else {
    hasMore = false;
  }
}

return items.map(item => ({ json: item }));
```

**⚠️ Safety:** Always include a maximum iteration count to prevent infinite loops.

---

## Sub-Workflows

### Calling a Sub-Workflow

```json
{
  "type": "n8n-nodes-base.executeWorkflow",
  "parameters": {
    "workflowId": "abc123-def456",
    "mode": "eachItem"
  }
}
```

**Modes:**
- `eachItem` — Runs sub-workflow once per input item (receives individual items)
- `allItems` — Runs sub-workflow once with all input items

### Creating a Sub-Workflow (Called by Parent)

The sub-workflow must start with a **Workflow Trigger** node (not Manual or Webhook):

```json
{
  "type": "n8n-nodes-base.workflowTrigger",
  "parameters": {}
}
```

**Sub-workflow returns data** by ending with a Set node or any node whose output becomes the return value.

### Sub-Workflow Gotchas

- Changes to sub-workflows affect ALL parent workflows — test carefully
- Sub-workflows can be nested (max 3 levels recommended)
- Sub-workflows have their own execution context and credentials
- Error handling in sub-workflows is independent — use Error Trigger or error branches within the sub

---

## Error Handling

### Strategy 1: Error Trigger (Global Monitoring)

Create a **separate** error-handling workflow:

```
Error Trigger
  → Set (format error: workflow name, node, message)
  → Switch (by severity)
    → Critical: Telegram alert + PagerDuty
    → Warning: Slack notification
    → Info: Log to database
```

This workflow receives errors from ALL other workflows.

### Strategy 2: Per-Node Error Branches

Enable "Continue on Fail" on individual nodes, then check for errors:

```
HTTP Request (continue on fail = true)
  → IF (error exists in output)
    → Yes: Log error + fallback action
    → No: Continue normal flow
```

**How to detect errors:**
```javascript
// In Code node, checking if previous node had an error
const items = $input.all();
const hasError = items.some(item => item.json.error !== undefined);
```

### Strategy 3: Retry Logic in Code Node

```javascript
const maxRetries = 3;
const baseDelay = 1000;

for (let attempt = 1; attempt <= maxRetries; attempt++) {
  try {
    const result = await this.helpers.httpRequest({
      url: 'https://api.example.com/data',
      method: 'GET',
    });
    return [{ json: result }];
  } catch (error) {
    if (attempt === maxRetries) {
      return [{ json: { error: error.message, attempt } }];
    }
    const delay = baseDelay * Math.pow(2, attempt - 1);
    await new Promise(resolve => setTimeout(resolve, delay));
  }
}
```

### Error Handling Best Practices

1. **Always add error handling to:**
   - External API calls (HTTP Request nodes)
   - Database operations
   - File I/O
   - Webhook processing

2. **Never let a workflow fail silently:**
   - If a node can fail, add an error branch
   - Use Error Trigger for global monitoring
   - Log errors to a database for analysis

3. **Graceful degradation:**
   - If an enrichment API fails, continue with the base data
   - If a notification fails, retry or queue for later
   - Never let one failed branch crash the entire workflow