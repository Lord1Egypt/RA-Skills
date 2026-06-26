# Example: Trigger Node (Polling)

A trigger node starts a workflow automatically on a schedule. It polls an API, checks for new data, and fires the workflow when something new appears.

**Key difference from regular nodes:** implements `poll()` instead of `execute()`. Uses `group: ['trigger']`. Has no input connection — it's always the first node.

## Table of Contents
1. [Full polling trigger](#1-full-polling-trigger)
2. [Deduplication — avoiding duplicate fires](#2-deduplication)
3. [Storing state between polls](#3-storing-state-between-polls)
4. [Manual execution for testing](#4-manual-execution-for-testing)

---

## 1. Full Polling Trigger

```typescript
import {
  IPollFunctions,
  INodeExecutionData,
  INodeType,
  INodeTypeDescription,
  NodeOperationError,
} from 'n8n-workflow';

export class MyServiceTrigger implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'My Service Trigger',
    name: 'myServiceTrigger',
    icon: 'file:myservice.svg',
    group: ['trigger'],              // ← must be 'trigger'
    version: 1,
    description: 'Starts workflow when new items appear in My Service',
    defaults: { name: 'My Service Trigger' },
    inputs: [],                      // ← triggers have no inputs
    outputs: ['main'],
    credentials: [{ name: 'myServiceApi', required: true }],

    // How often to poll — user can override in workflow settings
    polling: true,

    properties: [
      {
        displayName: 'Event',
        name: 'event',
        type: 'options',
        options: [
          { name: 'New Item Created', value: 'itemCreated' },
          { name: 'Item Updated',     value: 'itemUpdated' },
        ],
        default: 'itemCreated',
        required: true,
      },
      {
        displayName: 'Resource',
        name: 'resource',
        type: 'options',
        options: [
          { name: 'Task',    value: 'task' },
          { name: 'Comment', value: 'comment' },
        ],
        default: 'task',
      },
    ],
  };

  // poll() is called on each polling interval (set by user in n8n schedule)
  async poll(this: IPollFunctions): Promise<INodeExecutionData[][] | null> {
    const credentials = await this.getCredentials('myServiceApi');
    const event    = this.getNodeParameter('event') as string;
    const resource = this.getNodeParameter('resource') as string;

    // Get the last time we ran (stored by n8n between polls)
    const webhookData = this.getWorkflowStaticData('node');
    const lastChecked = webhookData.lastChecked as string | undefined;

    // First run — set baseline, don't fire
    if (!lastChecked) {
      webhookData.lastChecked = new Date().toISOString();
      return null;  // returning null = no new data, don't trigger workflow
    }

    try {
      const response = await this.helpers.httpRequest({
        method: 'GET',
        url: `https://api.myservice.com/${resource}s`,
        headers: { Authorization: `Bearer ${credentials.apiToken}` },
        qs: {
          event,
          created_after: lastChecked,
          limit: 100,
        },
      }) as { items: IDataObject[] };

      // Update timestamp for next poll
      webhookData.lastChecked = new Date().toISOString();

      if (!response.items || response.items.length === 0) {
        return null;  // nothing new
      }

      // Return each new item as a separate workflow execution
      return [
        response.items.map((item) => ({
          json: item,
        })),
      ];

    } catch (error) {
      throw new NodeOperationError(this.getNode(), error.message);
    }
  }
}
```

---

## 2. Deduplication

If the API doesn't support `created_after`, track seen IDs manually:

```typescript
async poll(this: IPollFunctions): Promise<INodeExecutionData[][] | null> {
  const webhookData = this.getWorkflowStaticData('node');

  // Initialize set of seen IDs
  if (!webhookData.seenIds) {
    webhookData.seenIds = [];
  }
  const seenIds = webhookData.seenIds as string[];

  const response = await this.helpers.httpRequest({
    method: 'GET',
    url: 'https://api.myservice.com/items',
    headers: authHeader,
    qs: { limit: 100, sort: 'created_desc' },
  }) as { items: Array<{ id: string; [key: string]: unknown }> };

  // Filter to items we haven't seen
  const newItems = response.items.filter((item) => !seenIds.includes(item.id));

  if (newItems.length === 0) return null;

  // Remember these IDs (keep list bounded to last 1000)
  webhookData.seenIds = [...seenIds, ...newItems.map((i) => i.id)].slice(-1000);

  return [newItems.map((item) => ({ json: item }))];
}
```

---

## 3. Storing State Between Polls

`this.getWorkflowStaticData('node')` returns a persistent object saved between poll runs:

```typescript
const state = this.getWorkflowStaticData('node');

// Read
const cursor = state.cursor as string | undefined;
const lastId = state.lastId as number | undefined;

// Write (automatically persisted after poll() returns)
state.cursor  = 'abc123';
state.lastId  = 99;
state.lastRun = new Date().toISOString();

// Reset (useful for testing)
delete state.cursor;
```

> ⚠️ `getWorkflowStaticData('global')` is shared across all nodes in the workflow. `getWorkflowStaticData('node')` is scoped to this node instance — use 'node' unless you specifically need cross-node sharing.

---

## 4. Manual Execution for Testing

When a user clicks "Test Workflow" on a trigger node, n8n calls `poll()` with `this.getMode() === 'manual'`. You can return mock/recent data in this case:

```typescript
async poll(this: IPollFunctions): Promise<INodeExecutionData[][] | null> {
  const isManual = this.getMode() === 'manual';

  // In manual mode, return last 5 items regardless of lastChecked
  const limit = isManual ? 5 : 100;
  const qs: IDataObject = { limit };

  if (!isManual) {
    const state = this.getWorkflowStaticData('node');
    if (state.lastChecked) {
      qs.created_after = state.lastChecked;
    }
  }

  const response = await this.helpers.httpRequest({
    method: 'GET',
    url: 'https://api.myservice.com/items',
    headers: authHeader,
    qs,
  }) as { items: IDataObject[] };

  if (!response.items?.length) return null;

  if (!isManual) {
    this.getWorkflowStaticData('node').lastChecked = new Date().toISOString();
  }

  return [response.items.map((item) => ({ json: item }))];
}
```
