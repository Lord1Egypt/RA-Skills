# Example: Declarative (Low-Code) Node

Define what the HTTP request looks like — n8n executes it automatically. No `execute()` needed.

**Use when:** single resource, simple CRUD, straightforward REST API, you want to ship fast.  
**Switch to programmatic when:** you need loops, conditional logic between calls, pagination, or data transformation.

## Table of Contents
1. [Full declarative node](#1-full-declarative-node)
2. [requestDefaults and credential injection](#2-requestdefaults-and-credential-injection)
3. [routing — request, output, postReceive](#3-routing)
4. [Expressions in routing](#4-expressions-in-routing)

---

## 1. Full Declarative Node

```typescript
import { INodeType, INodeTypeDescription } from 'n8n-workflow';

export class SimpleService implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'Simple Service',
    name: 'simpleService',
    icon: 'file:simpleservice.svg',
    group: ['transform'],
    version: 1,
    subtitle: '={{$parameter["operation"]}}',
    description: 'Interact with Simple Service API',
    defaults: { name: 'Simple Service' },
    inputs: ['main'],
    outputs: ['main'],
    credentials: [{ name: 'simpleServiceApi', required: true }],

    // Base URL + headers applied to every operation.
    // Credentials with an `authenticate` block are auto-injected here.
    requestDefaults: {
      baseURL: 'https://api.simpleservice.com',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
    },

    properties: [
      {
        displayName: 'Operation',
        name: 'operation',
        type: 'options',
        noDataExpression: true,
        options: [

          // ── GET single item ────────────────────────────────────────
          {
            name: 'Get Item',
            value: 'getItem',
            action: 'Get an item',
            routing: {
              request: { method: 'GET', url: '=/items/{{$parameter.itemId}}' },
            },
          },

          // ── GET list ───────────────────────────────────────────────
          {
            name: 'Get Many Items',
            value: 'getManyItems',
            action: 'Get many items',
            routing: {
              request: { method: 'GET', url: '/items' },
              output: {
                // Unwrap { data: [...] } → return just the array
                postReceive: [
                  { type: 'rootProperty', properties: { property: 'data' } },
                ],
              },
            },
          },

          // ── POST create ────────────────────────────────────────────
          {
            name: 'Create Item',
            value: 'createItem',
            action: 'Create an item',
            routing: {
              request: { method: 'POST', url: '/items' },
              // Body is assembled from individual field routing blocks below
            },
          },

          // ── DELETE ────────────────────────────────────────────────
          {
            name: 'Delete Item',
            value: 'deleteItem',
            action: 'Delete an item',
            routing: {
              request: { method: 'DELETE', url: '=/items/{{$parameter.itemId}}' },
              output: {
                // Replace API response with a clean success object
                postReceive: [
                  { type: 'set', properties: { value: '={{ { "success": true } }}' } },
                ],
              },
            },
          },
        ],
        default: 'getItem',
      },

      // ── Item ID (used in URL for get/delete) ───────────────────────
      {
        displayName: 'Item ID',
        name: 'itemId',
        type: 'string',
        required: true,
        default: '',
        displayOptions: { show: { operation: ['getItem', 'deleteItem'] } },
      },

      // ── Create fields — each adds to the request body ──────────────
      {
        displayName: 'Name',
        name: 'name',
        type: 'string',
        required: true,
        default: '',
        displayOptions: { show: { operation: ['createItem'] } },
        routing: { request: { body: { name: '={{$value}}' } } },
      },
      {
        displayName: 'Description',
        name: 'description',
        type: 'string',
        default: '',
        displayOptions: { show: { operation: ['createItem'] } },
        routing: { request: { body: { description: '={{$value}}' } } },
      },

      // ── Query params for list ──────────────────────────────────────
      {
        displayName: 'Limit',
        name: 'limit',
        type: 'number',
        default: 50,
        typeOptions: { minValue: 1 },
        displayOptions: { show: { operation: ['getManyItems'] } },
        routing: { request: { qs: { limit: '={{$value}}' } } },
      },
      {
        displayName: 'Status Filter',
        name: 'status',
        type: 'options',
        options: [
          { name: 'All',      value: '' },
          { name: 'Active',   value: 'active' },
          { name: 'Archived', value: 'archived' },
        ],
        default: '',
        displayOptions: { show: { operation: ['getManyItems'] } },
        routing: {
          request: {
            // Only send if not empty — omit param when 'All' selected
            qs: { status: '={{$value !== "" ? $value : undefined}}' },
          },
        },
      },
    ],
  };
}
```

---

## 2. requestDefaults and Credential Injection

`requestDefaults` sets headers/baseURL for all operations. If your credential has an `authenticate` block (e.g., `Authorization: Bearer {{$credentials.apiToken}}`), n8n auto-injects it into every request made via `requestDefaults`.

**This only works for declarative nodes.** In programmatic nodes you must inject credentials manually in `execute()`.

```typescript
requestDefaults: {
  baseURL: '={{$credentials.baseUrl}}',   // baseUrl can come from credentials too
  headers: {
    Accept: 'application/json',
    // Authorization is injected automatically from credential's authenticate block
  },
},
```

---

## 3. routing

Each operation (or individual field) can have a `routing` block:

```typescript
routing: {
  request: {
    method: 'POST',
    url: '/items',
    body: { key: '={{$value}}' },     // $value = this field's current value
    qs:   { page: '={{$value}}' },
    headers: { 'X-Extra': 'value' },
  },
  output: {
    postReceive: [/* transforms */],
  },
}
```

### postReceive transforms

| Type | What it does |
|---|---|
| `rootProperty` | Unwraps `{ data: [...] }` — extracts `data` array as output |
| `set` | Replaces entire output with a fixed value (good for DELETE) |
| `filter` | Filters output array by a condition |
| `limit` | Limits output to N items |

---

## 4. Expressions in routing

Use `={{...}}` to reference values dynamically:

```typescript
// Reference another parameter
url: '=/users/{{$parameter.userId}}/posts/{{$parameter.postId}}'

// Reference this field's value
body: { name: '={{$value}}' }

// Conditional — omit param if empty
qs: { filter: '={{$value !== "" ? $value : undefined}}' }

// Reference credentials
baseURL: '={{$credentials.instanceUrl}}'
```
