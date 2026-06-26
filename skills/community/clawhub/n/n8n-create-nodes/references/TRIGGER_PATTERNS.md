# Trigger Node Patterns

Reference for creating n8n trigger nodes. See [SKILL.md](../SKILL.md) for main skill.

n8n supports three trigger mechanisms: **webhook**, **poll**, and **event/stream**.

---

## Key Differences from Action Nodes

| Aspect | Action Node | Trigger Node |
|--------|------------|--------------|
| `group` | `['transform']`, `['output']` | `['trigger']` |
| `inputs` | `[NodeConnectionType.Main]` | `[]` (EMPTY) |
| Method | `execute()` | `webhook()`, `poll()`, or `trigger()` |
| Class name | `MyService` | `MyServiceTrigger` |
| File name | `MyService.node.ts` | `MyServiceTrigger.node.ts` |

---

## Pattern 1: Webhook Trigger (Auto-Registered)

The external service supports API-based webhook registration. n8n registers/deregisters automatically.

```typescript
import {
  IHookFunctions, IWebhookFunctions, INodeType,
  INodeTypeDescription, IWebhookResponseData,
  NodeConnectionType,
} from 'n8n-workflow';

export class MyServiceTrigger implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'My Service Trigger',
    name: 'myServiceTrigger',
    icon: 'file:myservice.svg',
    group: ['trigger'],
    version: 1,
    subtitle: '={{$parameter["event"]}}',
    description: 'Starts workflow when My Service events occur',
    defaults: { name: 'My Service Trigger' },
    inputs: [],                            // NO inputs for triggers
    outputs: [NodeConnectionType.Main],
    credentials: [{ name: 'myServiceApi', required: true }],
    webhooks: [
      {
        name: 'default',
        httpMethod: 'POST',
        responseMode: 'onReceived',
        path: 'webhook',
      },
    ],
    properties: [
      {
        displayName: 'Event',
        name: 'event',
        type: 'options',
        options: [
          { name: 'Contact Created', value: 'contact.created' },
          { name: 'Deal Updated', value: 'deal.updated' },
        ],
        default: 'contact.created',
        required: true,
      },
    ],
  };

  webhookMethods = {
    default: {
      async checkExists(this: IHookFunctions): Promise<boolean> {
        const webhookData = this.getWorkflowStaticData('node');
        const webhookUrl = this.getNodeWebhookUrl('default');
        // Check if webhook already registered with external API
        // Return true if exists, false if needs creation
        if (webhookData.webhookId) {
          return true;
        }
        return false;
      },

      async create(this: IHookFunctions): Promise<boolean> {
        const webhookData = this.getWorkflowStaticData('node');
        const webhookUrl = this.getNodeWebhookUrl('default');
        const event = this.getNodeParameter('event') as string;

        // Register webhook with external API
        const response = await myServiceApiRequest.call(this, 'POST', '/webhooks', {
          url: webhookUrl,
          events: [event],
        });

        // Store registration ID for cleanup
        webhookData.webhookId = response.id;
        return true;
      },

      async delete(this: IHookFunctions): Promise<boolean> {
        const webhookData = this.getWorkflowStaticData('node');
        const webhookId = webhookData.webhookId as string;

        if (webhookId) {
          await myServiceApiRequest.call(this, 'DELETE', `/webhooks/${webhookId}`);
          delete webhookData.webhookId;
        }
        return true;
      },
    },
  };

  async webhook(this: IWebhookFunctions): Promise<IWebhookResponseData> {
    const bodyData = this.getBodyData();
    return {
      workflowData: [this.helpers.returnJsonArray(bodyData)],
    };
  }
}
```

### Lifecycle

1. **Workflow activated** → `checkExists()` → if false → `create()` registers webhook
2. **Event received** → `webhook()` processes payload → triggers workflow
3. **Workflow deactivated** → `delete()` removes webhook registration

### Static Data

Use `this.getWorkflowStaticData('node')` to persist data (webhook IDs) between lifecycle calls. This data survives n8n restarts.

---

## Pattern 2: Simple Webhook (Manual URL)

No auto-registration — the user manually configures the webhook URL in the external service.

```typescript
export class MyServiceTrigger implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'My Service Trigger',
    name: 'myServiceTrigger',
    group: ['trigger'],
    version: 1,
    description: 'Starts workflow on My Service webhook',
    defaults: { name: 'My Service Trigger' },
    inputs: [],
    outputs: [NodeConnectionType.Main],
    webhooks: [
      {
        name: 'default',
        httpMethod: 'POST',
        responseMode: 'onReceived',
        path: 'webhook',
      },
    ],
    properties: [],
  };

  // No webhookMethods needed — user configures URL manually
  async webhook(this: IWebhookFunctions): Promise<IWebhookResponseData> {
    const bodyData = this.getBodyData();
    return {
      workflowData: [this.helpers.returnJsonArray(bodyData)],
    };
  }
}
```

---

## Pattern 3: Poll Trigger

n8n polls the external API on a schedule, checking for new data since last poll.

```typescript
import {
  IPollFunctions, INodeType, INodeTypeDescription,
  INodeExecutionData, NodeConnectionType,
} from 'n8n-workflow';

export class MyServiceTrigger implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'My Service Trigger',
    name: 'myServiceTrigger',
    group: ['trigger'],
    version: 1,
    description: 'Starts workflow when new items appear',
    defaults: { name: 'My Service Trigger' },
    inputs: [],
    outputs: [NodeConnectionType.Main],
    polling: true,                         // REQUIRED for poll triggers
    credentials: [{ name: 'myServiceApi', required: true }],
    properties: [
      {
        displayName: 'Poll Times',
        name: 'pollTimes',
        type: 'fixedCollection',
        typeOptions: { multipleValues: true },
        default: {},
        options: [
          {
            displayName: 'Item',
            name: 'item',
            values: [
              { displayName: 'Mode', name: 'mode', type: 'options',
                options: [
                  { name: 'Every Minute', value: 'everyMinute' },
                  { name: 'Every Hour', value: 'everyHour' },
                ],
                default: 'everyMinute',
              },
            ],
          },
        ],
      },
    ],
  };

  async poll(this: IPollFunctions): Promise<INodeExecutionData[][] | null> {
    const webhookData = this.getWorkflowStaticData('node');
    const lastChecked = webhookData.lastTimeChecked as string
      || new Date().toISOString();

    // Query API for items created/updated since lastChecked
    const items = await myServiceApiRequest.call(
      this, 'GET', '/items', {}, { since: lastChecked },
    );

    // Update last checked time
    webhookData.lastTimeChecked = new Date().toISOString();

    if (items.length === 0) {
      return null;                         // Return null = no new data, don't trigger
    }

    return [this.helpers.returnJsonArray(items)];
  }
}
```

**Key points:**
- Set `polling: true` in description
- `poll()` returns `INodeExecutionData[][] | null` — return `null` for no new items
- Track state with `getWorkflowStaticData('node')`

---

## Pattern 4: Event/Stream Trigger

Long-running listener (message queues, SSE, WebSocket):

```typescript
import {
  ITriggerFunctions, ITriggerResponse, INodeType,
  INodeTypeDescription, NodeConnectionType,
} from 'n8n-workflow';

export class MyServiceTrigger implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'My Service Trigger',
    name: 'myServiceTrigger',
    group: ['trigger'],
    version: 1,
    inputs: [],
    outputs: [NodeConnectionType.Main],
    properties: [/* ... */],
  };

  async trigger(this: ITriggerFunctions): Promise<ITriggerResponse> {
    // Set up listener
    const client = new MyServiceClient(/* ... */);
    client.on('message', (data) => {
      this.emit([this.helpers.returnJsonArray(data)]);
    });
    await client.connect();

    // Return cleanup + manual trigger functions
    const closeFunction = async () => {
      await client.disconnect();
    };
    const manualTriggerFunction = async () => {
      // Emit test data for manual workflow runs
      this.emit([this.helpers.returnJsonArray({ test: true })]);
    };

    return { closeFunction, manualTriggerFunction };
  }
}
```

**Key points:**
- `this.emit()` pushes data into the workflow whenever an event arrives
- `closeFunction` runs on workflow deactivation — clean up connections
- `manualTriggerFunction` provides test data when user clicks "Test Workflow"

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Trigger node with `inputs: [NodeConnectionType.Main]` | Use `inputs: []` — triggers have NO inputs |
| Missing `polling: true` on poll trigger | Required for n8n to schedule the poll |
| Not storing webhook ID in static data | Use `getWorkflowStaticData('node')` to persist between restarts |
| `poll()` returning empty array instead of null | Return `null` for no new data (empty array triggers with no items) |
| Using `IExecuteFunctions` in trigger | Use `IWebhookFunctions`, `IPollFunctions`, or `ITriggerFunctions` |
| Forgetting `delete()` in webhookMethods | Always clean up webhook registrations on deactivation |
