# Example: Webhook Node

A webhook node listens for incoming HTTP requests and fires a workflow when one arrives. Unlike trigger nodes (which poll), webhook nodes are passive — the external service pushes data to n8n.

**Key difference from trigger nodes:** implements `webhook()` instead of `poll()`. n8n registers a unique URL and keeps it alive while the workflow is active.

## Table of Contents
1. [Full webhook node](#1-full-webhook-node)
2. [HMAC signature verification](#2-hmac-signature-verification)
3. [Responding to the webhook caller](#3-responding-to-the-webhook-caller)
4. [Multiple webhook events / paths](#4-multiple-webhook-events--paths)
5. [Lifecycle hooks — activate/deactivate](#5-lifecycle-hooks)

---

## 1. Full Webhook Node

```typescript
import {
  IHookFunctions,
  IWebhookFunctions,
  INodeType,
  INodeTypeDescription,
  IWebhookResponseData,
  NodeOperationError,
} from 'n8n-workflow';

export class MyServiceWebhook implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'My Service Webhook',
    name: 'myServiceWebhook',
    icon: 'file:myservice.svg',
    group: ['trigger'],
    version: 1,
    description: 'Starts workflow when My Service sends an event',
    defaults: { name: 'My Service Webhook' },
    inputs: [],
    outputs: ['main'],
    credentials: [{ name: 'myServiceApi', required: true }],

    webhooks: [
      {
        name: 'default',
        httpMethod: 'POST',    // method the external service will call
        responseMode: 'onReceived',  // respond immediately on receipt
        path: 'webhook',       // becomes part of the URL: .../webhook/UUID/webhook
      },
    ],

    properties: [
      {
        displayName: 'Events',
        name: 'events',
        type: 'multiOptions',
        options: [
          { name: 'Item Created', value: 'item.created' },
          { name: 'Item Updated', value: 'item.updated' },
          { name: 'Item Deleted', value: 'item.deleted' },
        ],
        default: ['item.created'],
        required: true,
      },
      {
        displayName: 'Verify Signature',
        name: 'verifySignature',
        type: 'boolean',
        default: true,
        description: 'Whether to verify the HMAC signature from My Service',
      },
    ],
  };

  // ── Lifecycle hooks (called when workflow is activated/deactivated) ─
  webhookMethods = {
    default: {
      // Called when workflow activates — register webhook with external service
      async checkExists(this: IHookFunctions): Promise<boolean> {
        const webhookData = this.getWorkflowStaticData('node');
        const webhookUrl  = this.getNodeWebhookUrl('default') as string;
        const credentials = await this.getCredentials('myServiceApi');

        if (!webhookData.webhookId) return false;

        // Check if our webhook still exists in the external service
        try {
          await this.helpers.httpRequest({
            method: 'GET',
            url: `https://api.myservice.com/webhooks/${webhookData.webhookId}`,
            headers: { Authorization: `Bearer ${credentials.apiToken}` },
          });
          return true;
        } catch {
          return false;
        }
      },

      async create(this: IHookFunctions): Promise<boolean> {
        const webhookUrl  = this.getNodeWebhookUrl('default') as string;
        const credentials = await this.getCredentials('myServiceApi');
        const events      = this.getNodeParameter('events') as string[];

        const response = await this.helpers.httpRequest({
          method: 'POST',
          url: 'https://api.myservice.com/webhooks',
          headers: {
            Authorization: `Bearer ${credentials.apiToken}`,
            'Content-Type': 'application/json',
          },
          body: { url: webhookUrl, events },
        }) as { id: string; secret: string };

        // Save webhook ID and secret for verification and deletion later
        const webhookData = this.getWorkflowStaticData('node');
        webhookData.webhookId  = response.id;
        webhookData.webhookSecret = response.secret;

        return true;
      },

      async delete(this: IHookFunctions): Promise<boolean> {
        const webhookData = this.getWorkflowStaticData('node');
        const credentials = await this.getCredentials('myServiceApi');

        if (!webhookData.webhookId) return true;

        try {
          await this.helpers.httpRequest({
            method: 'DELETE',
            url: `https://api.myservice.com/webhooks/${webhookData.webhookId}`,
            headers: { Authorization: `Bearer ${credentials.apiToken}` },
          });
        } catch { /* ignore — webhook may already be gone */ }

        delete webhookData.webhookId;
        delete webhookData.webhookSecret;
        return true;
      },
    },
  };

  // ── Called on every incoming HTTP request ──────────────────────────
  async webhook(this: IWebhookFunctions): Promise<IWebhookResponseData> {
    const req           = this.getRequestObject();
    const body          = this.getBodyData() as IDataObject;
    const verifySignature = this.getNodeParameter('verifySignature') as boolean;

    // ── Signature verification ─────────────────────────────────────
    if (verifySignature) {
      const webhookData  = this.getWorkflowStaticData('node');
      const secret       = webhookData.webhookSecret as string;
      const signature    = req.headers['x-my-service-signature'] as string;

      if (!signature) {
        return { webhookResponse: { code: 401, data: 'Missing signature' } };
      }

      const crypto = require('crypto');
      const rawBody = (req as any).rawBody as Buffer;
      const expected = crypto
        .createHmac('sha256', secret)
        .update(rawBody)
        .digest('hex');

      if (`sha256=${expected}` !== signature) {
        return { webhookResponse: { code: 401, data: 'Invalid signature' } };
      }
    }

    // ── Return data to workflow ────────────────────────────────────
    return {
      workflowData: [[{ json: body }]],
      // Respond 200 OK to the caller immediately
      webhookResponse: { code: 200, data: JSON.stringify({ received: true }) },
    };
  }
}
```

---

## 2. HMAC Signature Verification

Most webhook providers sign payloads so you can verify authenticity.

```typescript
import crypto from 'crypto';

function verifyHmac(
  secret: string,
  rawBody: Buffer,
  signatureHeader: string,
  algorithm: 'sha256' | 'sha1' = 'sha256',
): boolean {
  const expected = crypto
    .createHmac(algorithm, secret)
    .update(rawBody)
    .digest('hex');

  const received = signatureHeader.replace(`${algorithm}=`, '');

  // Use timingSafeEqual to prevent timing attacks
  return crypto.timingSafeEqual(
    Buffer.from(expected, 'hex'),
    Buffer.from(received, 'hex'),
  );
}

// Usage in webhook():
const rawBody = (this.getRequestObject() as any).rawBody as Buffer;
if (!verifyHmac(secret, rawBody, signature)) {
  return { webhookResponse: { code: 401, data: 'Signature mismatch' } };
}
```

> ⚠️ Always use `rawBody` (unparsed bytes) for HMAC — using the parsed body object may produce different bytes.

---

## 3. Responding to the Webhook Caller

Control what the external service receives as the HTTP response:

```typescript
// Immediate 200 (most common)
return {
  workflowData: [[{ json: body }]],
  webhookResponse: {
    code: 200,
    data: JSON.stringify({ status: 'received' }),
  },
};

// Custom headers in response
return {
  workflowData: [[{ json: body }]],
  webhookResponse: {
    code: 200,
    headers: { 'X-Processed-By': 'n8n' },
    data: 'OK',
  },
};

// Reject with an error (no workflow execution)
return {
  webhookResponse: { code: 400, data: 'Bad request' },
};
```

---

## 4. Multiple Webhook Events / Paths

```typescript
webhooks: [
  {
    name: 'default',
    httpMethod: 'POST',
    responseMode: 'onReceived',
    path: 'events',       // → /webhook/UUID/events
  },
  {
    name: 'ping',
    httpMethod: 'GET',
    responseMode: 'onReceived',
    path: 'ping',         // → /webhook/UUID/ping  (for health check)
  },
],

// In webhook(), check which was called:
async webhook(this: IWebhookFunctions): Promise<IWebhookResponseData> {
  const webhookName = this.getWebhookName();  // 'default' | 'ping'

  if (webhookName === 'ping') {
    return { webhookResponse: { code: 200, data: 'pong' } };
  }

  // handle 'default' ...
}
```

---

## 5. Lifecycle Hooks

`webhookMethods` hooks fire when the workflow is activated/deactivated — use them to register/unregister with the external service:

| Method | When called | Use for |
|---|---|---|
| `checkExists` | On activation | Check if a previous registration still exists |
| `create` | On activation (if checkExists returns false) | Register webhook URL with the API |
| `delete` | On deactivation | Unregister from the API |

Always persist the webhook ID in `getWorkflowStaticData('node')` so `delete` can find it later.

> ⚠️ If your external API doesn't support programmatic webhook registration, skip `webhookMethods` entirely and show the webhook URL as a read-only field the user copies manually.
