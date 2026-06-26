---
name: n8n-create-nodes
description: Build production-ready n8n community nodes as npm packages, covering declarative and programmatic node styles. Use when user says "create an n8n node", "build an n8n integration", "scaffold n8n node package", "create n8n credential type", "create webhook trigger node", "create poll trigger", "publish n8n community node", or works with INodeType, n8n-workflow-SDK, n8n-nodes-starter, declarative routing, programmatic execute, or versioned nodes. Do NOT use for n8n workflow building or general workflow automation this skill is specifically for node package development.
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["n8n", "community-nodes", "node-development", "npm-package", "workflow-sdk"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/n8n-create-nodes", "emoji": "🟧" } }
---

# n8n Community Node Creation

Build production-ready n8n community nodes as npm packages. This skill covers both **declarative** (REST API wrapping) and **programmatic** (custom logic) node styles.

**References:** [CREDENTIAL_PATTERNS.md](references/CREDENTIAL_PATTERNS.md) | [TRIGGER_PATTERNS.md](references/TRIGGER_PATTERNS.md) | [EXAMPLES.md](references/EXAMPLES.md) | [COMMON_MISTAKES.md](references/COMMON_MISTAKES.md)

---

## Quick Reference: Declarative vs Programmatic

| Aspect | Declarative | Programmatic |
|--------|------------|--------------|
| **Best for** | Simple REST API wrappers | Custom logic, transforms, multi-call flows |
| **HTTP handling** | Automatic via `routing` keys | Manual in `execute()` method |
| **Key property** | `requestDefaults` in description | `async execute()` method |
| **Imports needed** | `INodeType`, `INodeTypeDescription` | + `IExecuteFunctions`, `INodeExecutionData` |
| **Complexity** | Lower — declare routes, n8n handles requests | Higher — full control over execution |
| **Pagination** | Via `operations.pagination` config | Manual loop in `apiRequestAllItems` helper |
| **When to choose** | API maps 1:1 to operations, no transforms | Need data manipulation, conditional logic, or chained calls |

**Decision rule:** If every operation is a single HTTP request with simple input→body mapping and the response can be used as-is (or with minor `postReceive` transforms), use **declarative**. Otherwise, use **programmatic**.

---

## Getting Started

> **IMPORTANT:** Always start by cloning the official n8n-nodes-starter repository. Do NOT scaffold a project from scratch. The starter provides the correct TypeScript config, build tooling, linting, and project structure that n8n expects.

### 1. Clone the n8n-nodes-starter (Mandatory First Step)

```bash
# Clone the official starter — this is always the first step
git clone https://github.com/n8n-io/n8n-nodes-starter.git n8n-nodes-<yourservice>
cd n8n-nodes-<yourservice>

# Remove the starter's git history and reinitialize
rm -rf .git
git init

# Install dependencies
npm install
```

The starter repo provides:
- Pre-configured `tsconfig.json` with the correct compiler options for n8n
- Working `package.json` with build scripts (`build`, `dev`, `lint`, `lintfix`)
- ESLint/Prettier configuration matching n8n conventions
- Example node and credential files to use as a starting reference
- Correct `n8n` object structure in `package.json` pointing to `dist/` outputs

After cloning, rename/replace the example node and credential files with your own, and update `package.json` with your package name (`n8n-nodes-<yourservice>`), description, and the `n8n.nodes` / `n8n.credentials` arrays.

### 2. Required Files

| File | Purpose |
|------|---------|
| `nodes/<Name>/<Name>.node.ts` | Main node class (logic + description) |
| `nodes/<Name>/<Name>.node.json` | Codex file (categories, doc links) |
| `nodes/<Name>/<name>.svg` | Node icon (SVG, 60×60px recommended) |
| `credentials/<Name>Api.credentials.ts` | Credential/auth definition |
| `package.json` | npm config with `n8n` object linking nodes & credentials |

**Critical rules:**
- npm package name **must** start with `n8n-nodes-`
- Class name **must** match filename (class `MyService` → `MyService.node.ts`)
- Icon filename is **lowercase** (`myservice.svg`)

### 3. Package.json n8n Config

```json
{
  "name": "n8n-nodes-myservice",
  "version": "0.1.0",
  "n8n": {
    "n8nNodesApiVersion": 1,
    "nodes": [
      "dist/nodes/MyService/MyService.node.js"
    ],
    "credentials": [
      "dist/credentials/MyServiceApi.credentials.js"
    ]
  }
}
```

---

## Node Class Structure

Every node implements `INodeType` with a `description` object:

```typescript
import { INodeType, INodeTypeDescription, NodeConnectionType } from 'n8n-workflow';

export class MyService implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'My Service',
    name: 'myService',
    icon: 'file:myservice.svg',
    group: ['transform'],
    version: 1,
    subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
    description: 'Interact with My Service API',
    defaults: { name: 'My Service' },
    inputs: [NodeConnectionType.Main],
    outputs: [NodeConnectionType.Main],
    credentials: [
      { name: 'myServiceApi', required: true },
    ],
    properties: [
      // Resource and operation selectors, then parameter fields
    ],
  };
}
```

### Required Description Properties

| Property | Type | Notes |
|----------|------|-------|
| `displayName` | `string` | Shown in node panel |
| `name` | `string` | camelCase internal ID, unique across all nodes |
| `icon` | `string` | `'file:icon.svg'` — ref to SVG in node folder |
| `group` | `string[]` | `['transform']`, `['output']`, `['input']`, or `['trigger']` |
| `version` | `number` | Start at `1`, increment for breaking changes |
| `subtitle` | `string` | Expression template shown below node name |
| `description` | `string` | Short one-liner for node panel |
| `defaults` | `object` | `{ name: 'Display Name' }` |
| `inputs` | `array` | `[NodeConnectionType.Main]` — empty `[]` for triggers |
| `outputs` | `array` | `[NodeConnectionType.Main]` |
| `credentials` | `array` | `[{ name: 'credName', required: true }]` |
| `properties` | `INodeProperties[]` | UI fields — resources, operations, parameters |

---

## Resource & Operation Pattern

The standard way to organize a node with multiple API resources:

```typescript
properties: [
  // 1. Resource selector
  {
    displayName: 'Resource',
    name: 'resource',
    type: 'options',
    noDataExpression: true,       // REQUIRED on resource/operation selectors
    options: [
      { name: 'Contact', value: 'contact' },
      { name: 'Deal', value: 'deal' },
    ],
    default: 'contact',
  },
  // 2. Operation selector (per resource)
  {
    displayName: 'Operation',
    name: 'operation',
    type: 'options',
    noDataExpression: true,
    displayOptions: { show: { resource: ['contact'] } },
    options: [
      { name: 'Create', value: 'create', action: 'Create a contact' },
      { name: 'Delete', value: 'delete', action: 'Delete a contact' },
      { name: 'Get', value: 'get', action: 'Get a contact' },
      { name: 'Get Many', value: 'getAll', action: 'Get many contacts' },
      { name: 'Update', value: 'update', action: 'Update a contact' },
    ],
    default: 'create',
  },
  // 3. Operation-specific fields
  {
    displayName: 'Contact ID',
    name: 'contactId',
    type: 'string',
    required: true,
    default: '',
    displayOptions: {
      show: { resource: ['contact'], operation: ['get', 'update', 'delete'] },
    },
    description: 'The ID of the contact',
  },
  // 4. returnAll / limit pair for getAll
  {
    displayName: 'Return All',
    name: 'returnAll',
    type: 'boolean',
    default: false,
    displayOptions: { show: { resource: ['contact'], operation: ['getAll'] } },
    description: 'Whether to return all results or only up to a given limit',
  },
  {
    displayName: 'Limit',
    name: 'limit',
    type: 'number',
    default: 50,
    typeOptions: { minValue: 1 },
    displayOptions: {
      show: { resource: ['contact'], operation: ['getAll'], returnAll: [false] },
    },
    description: 'Max number of results to return',
  },
  // 5. Additional fields (optional params)
  {
    displayName: 'Additional Fields',
    name: 'additionalFields',
    type: 'collection',
    placeholder: 'Add Field',
    default: {},
    displayOptions: { show: { resource: ['contact'], operation: ['create', 'update'] } },
    options: [
      { displayName: 'Email', name: 'email', type: 'string', default: '' },
      { displayName: 'Phone', name: 'phone', type: 'string', default: '' },
    ],
  },
],
```

**Key rules:**
- Always set `noDataExpression: true` on resource and operation selectors
- Always include `action` on each operation option (used for the node action list)
- Standard operation values: `create`, `get`, `getAll`, `update`, `delete`, `upsert`
- Use `displayOptions.show` to conditionally display fields per resource/operation

---

## Declarative Style

Add `requestDefaults` to description and `routing` to each operation. **No `execute()` method.**

```typescript
description: INodeTypeDescription = {
  // ...standard properties...
  requestDefaults: {
    baseURL: 'https://api.myservice.com/v1',
    headers: { Accept: 'application/json' },
  },
  properties: [
    {
      displayName: 'Operation', name: 'operation', type: 'options',
      noDataExpression: true,
      options: [
        {
          name: 'Create', value: 'create', action: 'Create an item',
          routing: {
            request: { method: 'POST', url: '/items' },
          },
        },
        {
          name: 'Get', value: 'get', action: 'Get an item',
          routing: {
            request: { method: 'GET', url: '=/items/{{$parameter.itemId}}' },
          },
        },
      ],
      default: 'create',
    },
    // Map field values to request body/query
    {
      displayName: 'Name', name: 'name', type: 'string', default: '',
      routing: { send: { type: 'body', property: 'name' } },
    },
    {
      displayName: 'Tag', name: 'tag', type: 'string', default: '',
      routing: { send: { type: 'query', property: 'tag' } },
    },
  ],
};
```

### Routing Keys

| Key | Purpose | Example |
|-----|---------|---------|
| `routing.request` | HTTP method, URL, headers per operation | `{ method: 'POST', url: '/items' }` |
| `routing.send` | Map parameter to body/query | `{ type: 'body', property: 'name' }` |
| `routing.output.postReceive` | Transform response | `[{ type: 'rootProperty', properties: { property: 'data' } }]` |
| `routing.operations.pagination` | Auto-pagination config | `{ type: 'offset', properties: { ... } }` |

### postReceive Transforms

```typescript
routing: {
  output: {
    postReceive: [
      { type: 'rootProperty', properties: { property: 'data' } },     // Extract nested data
      { type: 'filter', properties: { pass: '={{$responseItem.active}}' } },
      { type: 'limit', properties: { maxResults: '={{$parameter.limit}}' } },
      { type: 'set', properties: { value: '={{ { "id": $response.body.id } }}' } },
    ],
  },
},
```

---

## Programmatic Style

Add an `async execute()` method for full control:

```typescript
import {
  IExecuteFunctions, INodeExecutionData, INodeType,
  INodeTypeDescription, NodeConnectionType,
} from 'n8n-workflow';

export class MyService implements INodeType {
  description: INodeTypeDescription = { /* ...same as above, minus requestDefaults/routing... */ };

  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    const items = this.getInputData();
    const returnData: INodeExecutionData[] = [];
    const resource = this.getNodeParameter('resource', 0) as string;
    const operation = this.getNodeParameter('operation', 0) as string;

    for (let i = 0; i < items.length; i++) {
      try {
        let responseData;

        if (resource === 'contact') {
          if (operation === 'create') {
            const email = this.getNodeParameter('email', i) as string;
            const additionalFields = this.getNodeParameter('additionalFields', i) as IDataObject;
            const body: IDataObject = { email, ...additionalFields };
            responseData = await myServiceApiRequest.call(this, 'POST', '/contacts', body);
          }
          if (operation === 'getAll') {
            const returnAll = this.getNodeParameter('returnAll', i) as boolean;
            if (returnAll) {
              responseData = await myServiceApiRequestAllItems.call(
                this, 'contacts', 'GET', '/contacts',
              );
            } else {
              const limit = this.getNodeParameter('limit', i) as number;
              responseData = await myServiceApiRequest.call(
                this, 'GET', '/contacts', {}, { limit },
              );
              responseData = responseData.contacts;
            }
          }
        }

        const executionData = this.helpers.constructExecutionMetaData(
          this.helpers.returnJsonArray(responseData),
          { itemData: { item: i } },
        );
        returnData.push(...executionData);

      } catch (error) {
        if (this.continueOnFail()) {
          const executionErrorData = this.helpers.constructExecutionMetaData(
            this.helpers.returnJsonArray({ error: error.message }),
            { itemData: { item: i } },
          );
          returnData.push(...executionErrorData);
          continue;
        }
        throw error;
      }
    }

    return [returnData];
  }
}
```

### Key Programmatic Helpers

| Method | Purpose |
|--------|---------|
| `this.getInputData()` | Get input items array |
| `this.getNodeParameter(name, index)` | Read a user-configured parameter |
| `this.getCredentials('credName')` | Retrieve stored credentials |
| `this.helpers.returnJsonArray(data)` | Wrap response as `INodeExecutionData[]` |
| `this.helpers.constructExecutionMetaData(data, { itemData })` | Link output to input items |
| `this.continueOnFail()` | Check if user enabled "Continue On Fail" |
| `this.helpers.request(options)` | Make HTTP request |
| `this.helpers.requestWithAuthentication('credName', options)` | Authenticated HTTP request |

---

## UI Property Types

| Type | Description | Common typeOptions |
|------|-------------|-------------------|
| `string` | Text input | `password: true`, `rows: N` (multiline) |
| `number` | Numeric input | `minValue`, `maxValue`, `numberPrecision` |
| `boolean` | Toggle | — |
| `options` | Single-select dropdown | — |
| `multiOptions` | Multi-select dropdown | — |
| `collection` | "Add Field" group of optional params | — |
| `fixedCollection` | Structured key-value groups | `multipleValues: true` |
| `json` | JSON code editor | — |
| `dateTime` | Date/time picker | — |
| `color` | Color picker | — |
| `resourceLocator` | Find by ID/URL/search | `mode: ['list', 'url', 'id']` |
| `resourceMapper` | Map fields to external schema | — |
| `notice` | Info box (not a parameter) | — |

### Dynamic Options (Load from API)

```typescript
{
  displayName: 'Channel',
  name: 'channelId',
  type: 'options',
  typeOptions: { loadOptionsMethod: 'getChannels' },
  default: '',
}

// In the node class:
methods = {
  loadOptions: {
    async getChannels(this: ILoadOptionsFunctions) {
      const credentials = await this.getCredentials('myServiceApi');
      const channels = await myServiceApiRequest.call(this, 'GET', '/channels');
      return channels.map((c: any) => ({ name: c.name, value: c.id }));
    },
  },
};
```

---

## Codex File (.node.json)

```json
{
  "node": "n8n-nodes-myservice.myService",
  "nodeVersion": "1.0",
  "codexVersion": "1.0",
  "categories": ["Miscellaneous"],
  "resources": {
    "credentialDocumentation": [{ "url": "" }],
    "primaryDocumentation": [{ "url": "" }]
  }
}
```

The `node` field format is `<package-name>.<node-internal-name>`.

---

## Error Handling

### Two Error Classes

| Class | Use For | Import From |
|-------|---------|-------------|
| `NodeApiError` | External API failures | `n8n-workflow` |
| `NodeOperationError` | Internal logic errors | `n8n-workflow` |

```typescript
// In GenericFunctions.ts — wrap API errors:
throw new NodeApiError(this.getNode(), error as JsonObject);

// In execute() — wrap logic errors:
throw new NodeOperationError(this.getNode(), 'Unsupported operation', { itemIndex: i });
```

### continueOnFail Pattern (ALWAYS use in execute loops)

See the programmatic style example above for the full pattern. The key structure:
1. Wrap each item's processing in `try/catch`
2. On catch: if `this.continueOnFail()`, push error data and `continue`
3. Otherwise, re-throw the error

---

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Node class | PascalCase | `MyService` |
| Trigger class | PascalCase + Trigger | `MyServiceTrigger` |
| Node file | `{Class}.node.ts` | `MyService.node.ts` |
| Credential class | PascalCase + Api | `MyServiceApi` |
| Credential file | `{Class}.credentials.ts` | `MyServiceApi.credentials.ts` |
| Internal name | camelCase | `myService` |
| npm package | `n8n-nodes-{name}` | `n8n-nodes-myservice` |
| Operation values | camelCase verbs | `create`, `get`, `getAll`, `update`, `delete` |

---

## Versioning Nodes

When making breaking changes, version the node instead of modifying in place:

```typescript
import { INodeTypeBaseDescription, INodeTypeDescription, VersionedNodeType } from 'n8n-workflow';

export class MyService extends VersionedNodeType {
  constructor() {
    const baseDescription: INodeTypeBaseDescription = {
      displayName: 'My Service',
      name: 'myService',
      icon: 'file:myservice.svg',
      group: ['transform'],
      defaultVersion: 2,
      description: 'Interact with My Service',
    };
    const nodeVersions: IVersionedNodeType['nodeVersions'] = {
      1: new MyServiceV1(baseDescription),
      2: new MyServiceV2(baseDescription),
    };
    super(nodeVersions, baseDescription);
  }
}
```

Each version is a separate class with its own full `INodeTypeDescription`. Place in `V1/` and `V2/` subdirectories.

---

## Testing & Publishing

### Local Testing

```bash
# Build the node package
npm run build

# Link it into your n8n installation
npm link
cd ~/.n8n
npm link n8n-nodes-myservice

# Restart n8n — your node appears in the editor
n8n start
```

### Publishing to npm

```bash
npm login
npm publish
```

After publishing, users install via: **Settings → Community Nodes → Install → `n8n-nodes-myservice`**

Ensure your `package.json` has:
- `"n8n"` object with `nodes` and `credentials` arrays pointing to `dist/` files
- Correct `main` and `files` fields
- `"keywords": ["n8n-community-node-package"]`

---

## Best Practices

**Do:**
- Use `noDataExpression: true` on resource/operation selectors
- Include `action` on every operation option
- Use `constructExecutionMetaData` with `itemData` for proper item linking
- Implement `continueOnFail()` in every execute loop
- Create `GenericFunctions.ts` for shared API request helpers
- Use `NodeConnectionType.Main` instead of string `'main'`
- Use `typeOptions: { password: true }` for secret fields in credentials
- Use `returnAll`/`limit` pair for list operations

**Don't:**
- Modify v1 when adding features — create v2 instead
- Forget the codex `.node.json` file
- Use inputs other than `[]` for trigger nodes
- Hard-code API base URLs in execute — use credentials or requestDefaults
- Skip error wrapping — always use `NodeApiError`/`NodeOperationError`
- Create large monolithic node files — split descriptions into separate files per resource

---

## Troubleshooting

Quick reference for common issues. For the full catalog of 16+ errors with fixes, see [references/COMMON_MISTAKES.md](references/COMMON_MISTAKES.md).

### Node not appearing in editor
1. Check `package.json` → `n8n.nodes` paths point to `dist/` (not source)
2. Rebuild: `npm run build`
3. Re-link if using `npm link` and restart n8n

### "Cannot find credential"
- Verify the `name` in your credential class matches the name in the node's `description.credentials` array (case-sensitive)
- Ensure credential file is listed in `package.json` → `n8n.credentials`

### displayOptions not working
- Resource/operation `value` strings must match exactly (case-sensitive) between the selector and `displayOptions.show`

### Empty response data
- For declarative nodes: verify `postReceive` → `rootProperty` extracts the correct JSON path from the API response

### Item linking broken in output
- Add `constructExecutionMetaData` with `{ itemData: { item: i } }` wrapping every `returnJsonArray` call

---

## Related Files

- [references/CREDENTIAL_PATTERNS.md](references/CREDENTIAL_PATTERNS.md) — API key, OAuth2, and custom auth patterns
- [references/TRIGGER_PATTERNS.md](references/TRIGGER_PATTERNS.md) — Webhook, poll, and event trigger implementations
- [references/EXAMPLES.md](references/EXAMPLES.md) — Complete working node examples and helper patterns
- [references/COMMON_MISTAKES.md](references/COMMON_MISTAKES.md) — Error catalog with fixes