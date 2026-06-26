# Example: Programmatic Node (Full Pattern)

The programmatic style uses an `execute()` method with full TypeScript control.

**Use when:** multiple resources, multiple operations, conditional logic, pagination, multiple API calls per item, or anything that needs real code.

## Table of Contents
1. [Minimal working node](#1-minimal-working-node)
2. [Resources + Operations pattern](#2-resources--operations-pattern)
3. [Dynamic dropdowns via loadOptions](#3-dynamic-dropdowns-via-loadoptions)
4. [Pagination — cursor and page-based](#4-pagination)
5. [Full execute() with all operations](#5-full-execute)

---

## 1. Minimal Working Node

```typescript
import {
  IExecuteFunctions,
  INodeExecutionData,
  INodeType,
  INodeTypeDescription,
  NodeOperationError,
} from 'n8n-workflow';

export class MyNode implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'My Node',
    name: 'myNode',
    icon: 'file:mynode.svg',
    group: ['transform'],
    version: 1,
    description: 'Does something useful',
    defaults: { name: 'My Node' },
    inputs: ['main'],
    outputs: ['main'],
    credentials: [{ name: 'myNodeApi', required: true }],
    properties: [
      {
        displayName: 'User ID',
        name: 'userId',
        type: 'string',
        default: '',
        required: true,
      },
    ],
  };

  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    const items = this.getInputData();
    const returnData: INodeExecutionData[] = [];
    const credentials = await this.getCredentials('myNodeApi');

    for (let i = 0; i < items.length; i++) {
      try {
        const userId = this.getNodeParameter('userId', i) as string;

        const response = await this.helpers.httpRequest({
          method: 'GET',
          url: `https://api.example.com/users/${userId}`,
          headers: { Authorization: `Bearer ${credentials.apiToken}` },
        });

        returnData.push({ json: response, pairedItem: { item: i } });

      } catch (error) {
        if (this.continueOnFail()) {
          returnData.push({ json: { error: error.message }, pairedItem: { item: i } });
          continue;
        }
        throw new NodeOperationError(this.getNode(), error, { itemIndex: i });
      }
    }

    return [returnData];
  }
}
```

---

## 2. Resources + Operations Pattern

The standard pattern for nodes that cover multiple entities (users, posts) with multiple actions each.

```typescript
properties: [
  // ── Step 1: Resource selector ─────────────────────────────────────
  {
    displayName: 'Resource',
    name: 'resource',
    type: 'options',
    noDataExpression: true,   // ← prevents expression mode on this field
    options: [
      { name: 'User', value: 'user' },
      { name: 'Post', value: 'post' },
    ],
    default: 'user',
  },

  // ── Step 2: Operations per resource ───────────────────────────────
  {
    displayName: 'Operation',
    name: 'operation',
    type: 'options',
    noDataExpression: true,
    displayOptions: { show: { resource: ['user'] } },
    options: [
      { name: 'Create', value: 'create', description: 'Create a user', action: 'Create a user' },
      { name: 'Delete', value: 'delete', description: 'Delete a user', action: 'Delete a user' },
      { name: 'Get',    value: 'get',    description: 'Get a user',    action: 'Get a user' },
      { name: 'Get Many', value: 'getAll', description: 'Get many users', action: 'Get many users' },
      { name: 'Update', value: 'update', description: 'Update a user', action: 'Update a user' },
    ],
    default: 'get',
  },

  // ── Step 3: Fields per operation ──────────────────────────────────
  {
    displayName: 'User ID',
    name: 'userId',
    type: 'string',
    required: true,
    default: '',
    displayOptions: {
      show: {
        resource: ['user'],
        operation: ['get', 'update', 'delete'],
      },
    },
  },
  {
    displayName: 'Name',
    name: 'name',
    type: 'string',
    default: '',
    required: true,
    displayOptions: { show: { resource: ['user'], operation: ['create'] } },
  },
  {
    displayName: 'Email',
    name: 'email',
    type: 'string',
    placeholder: 'name@email.com',
    default: '',
    required: true,
    displayOptions: { show: { resource: ['user'], operation: ['create'] } },
  },

  // ── Return All / Limit pattern ─────────────────────────────────────
  {
    displayName: 'Return All',
    name: 'returnAll',
    type: 'boolean',
    default: false,
    description: 'Whether to return all results or only up to a given limit',
    displayOptions: { show: { resource: ['user'], operation: ['getAll'] } },
  },
  {
    displayName: 'Limit',
    name: 'limit',
    type: 'number',
    default: 50,
    typeOptions: { minValue: 1 },
    displayOptions: {
      show: { resource: ['user'], operation: ['getAll'], returnAll: [false] },
    },
  },

  // ── Additional Options (optional extras) ──────────────────────────
  {
    displayName: 'Additional Options',
    name: 'options',
    type: 'collection',
    placeholder: 'Add Option',
    default: {},
    displayOptions: { show: { resource: ['user'], operation: ['create', 'update'] } },
    options: [
      {
        displayName: 'Role',
        name: 'role',
        type: 'options',
        options: [
          { name: 'Admin',  value: 'admin' },
          { name: 'Member', value: 'member' },
        ],
        default: 'member',
      },
      { displayName: 'Active', name: 'active', type: 'boolean', default: true },
    ],
  },

  // ── subtitle trick: shows current operation in node header ─────────
  // Add to description object (not properties):
  // subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}'
],
```

---

## 3. Dynamic Dropdowns via loadOptions

Populates a dropdown from a live API call (e.g. list of projects, workspaces, tags).

```typescript
// In the node description properties:
{
  displayName: 'Project',
  name: 'projectId',
  type: 'options',
  typeOptions: {
    loadOptionsMethod: 'getProjects',  // ← matches method name below
  },
  default: '',
  required: true,
  description: 'Choose from projects in your account. Loaded live from API.',
}

// In the node class, add a methods block alongside description:
methods = {
  loadOptions: {
    async getProjects(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
      const credentials = await this.getCredentials('myNodeApi');

      const response = await this.helpers.httpRequest({
        method: 'GET',
        url: 'https://api.example.com/projects',
        headers: { Authorization: `Bearer ${credentials.apiToken}` },
      }) as Array<{ id: string; name: string }>;

      return response.map((project) => ({
        name: project.name,   // shown in dropdown
        value: project.id,    // stored value
      }));
    },

    // Multiple loadOptions methods are fine
    async getCategories(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
      // ...same pattern
      return [];
    },
  },
};
```

Import needed: `ILoadOptionsFunctions, INodePropertyOptions` from `'n8n-workflow'`

---

## 4. Pagination

### Page-based (page=1, page=2, ...)

```typescript
const returnAll = this.getNodeParameter('returnAll', i) as boolean;
const limit     = returnAll ? Infinity : this.getNodeParameter('limit', i, 50) as number;

let page = 1;
const allItems: unknown[] = [];

while (true) {
  const result = await this.helpers.httpRequest({
    method: 'GET',
    url: 'https://api.example.com/items',
    headers: authHeader,
    qs: { page, per_page: 100 },
  }) as { data: unknown[]; has_more: boolean };

  allItems.push(...result.data);

  if (!result.has_more || allItems.length >= limit) break;
  page++;
}

const sliced = returnAll ? allItems : allItems.slice(0, limit);
for (const item of sliced) {
  returnData.push({ json: item as IDataObject, pairedItem: { item: i } });
}
```

### Cursor-based (next_cursor)

```typescript
let cursor: string | undefined;
const allItems: unknown[] = [];

do {
  const result = await this.helpers.httpRequest({
    method: 'GET',
    url: 'https://api.example.com/items',
    headers: authHeader,
    qs: { cursor, limit: 100 },
  }) as { data: unknown[]; next_cursor?: string };

  allItems.push(...result.data);
  cursor = result.next_cursor;
} while (cursor);
```

---

## 5. Full execute()

```typescript
async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
  const items     = this.getInputData();
  const returnData: INodeExecutionData[] = [];
  const resource  = this.getNodeParameter('resource', 0) as string;
  const operation = this.getNodeParameter('operation', 0) as string;
  const credentials = await this.getCredentials('myNodeApi');

  const baseURL    = 'https://api.example.com';
  const authHeader = { Authorization: `Bearer ${credentials.apiToken}` };
  const jsonHeader = { ...authHeader, 'Content-Type': 'application/json' };

  for (let i = 0; i < items.length; i++) {
    try {
      let responseData: unknown;

      if (resource === 'user') {

        if (operation === 'get') {
          const userId = this.getNodeParameter('userId', i) as string;
          responseData = await this.helpers.httpRequest({
            method: 'GET',
            url: `${baseURL}/users/${userId}`,
            headers: authHeader,
          });

        } else if (operation === 'create') {
          const name    = this.getNodeParameter('name', i) as string;
          const email   = this.getNodeParameter('email', i) as string;
          const options = this.getNodeParameter('options', i, {}) as IDataObject;

          responseData = await this.helpers.httpRequest({
            method: 'POST',
            url: `${baseURL}/users`,
            headers: jsonHeader,
            body: { name, email, ...options },
          });

        } else if (operation === 'update') {
          const userId  = this.getNodeParameter('userId', i) as string;
          const options = this.getNodeParameter('options', i, {}) as IDataObject;

          responseData = await this.helpers.httpRequest({
            method: 'PATCH',
            url: `${baseURL}/users/${userId}`,
            headers: jsonHeader,
            body: options,
          });

        } else if (operation === 'delete') {
          const userId = this.getNodeParameter('userId', i) as string;
          await this.helpers.httpRequest({
            method: 'DELETE',
            url: `${baseURL}/users/${userId}`,
            headers: authHeader,
          });
          responseData = { success: true, id: userId };

        } else if (operation === 'getAll') {
          // See pagination patterns above
          responseData = { message: 'use pagination pattern from section 4' };
        }

      } else if (resource === 'post') {
        // same pattern for each resource
      }

      returnData.push({
        json: responseData as IDataObject,
        pairedItem: { item: i },
      });

    } catch (error) {
      if (this.continueOnFail()) {
        returnData.push({
          json: { error: error.message, statusCode: error.statusCode ?? 'unknown' },
          pairedItem: { item: i },
        });
        continue;
      }
      // NodeApiError for HTTP errors (has statusCode), NodeOperationError for logic errors
      if (error.statusCode) {
        throw new NodeApiError(this.getNode(), error, { itemIndex: i });
      }
      throw new NodeOperationError(this.getNode(), error.message, { itemIndex: i });
    }
  }

  return [returnData];
}
```
