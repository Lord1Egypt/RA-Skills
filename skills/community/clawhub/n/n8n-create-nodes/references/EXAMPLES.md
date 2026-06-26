# Examples

Complete working examples for n8n community node development. See [SKILL.md](../SKILL.md) for main skill.

---

## GenericFunctions.ts (Standard Helper)

Every programmatic node should include this shared helper file:

```typescript
import type {
  IExecuteFunctions,
  IHookFunctions,
  ILoadOptionsFunctions,
  IWebhookFunctions,
  IHttpRequestMethods,
  IRequestOptions,
  IDataObject,
  JsonObject,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function myServiceApiRequest(
  this: IExecuteFunctions | IHookFunctions | ILoadOptionsFunctions | IWebhookFunctions,
  method: IHttpRequestMethods,
  resource: string,
  body: IDataObject = {},
  qs: IDataObject = {},
  uri?: string,
  option: IDataObject = {},
): Promise<any> {
  const credentials = await this.getCredentials('myServiceApi');
  const options: IRequestOptions = {
    headers: { 'Content-Type': 'application/json' },
    method,
    qs,
    body,
    uri: uri || `${credentials.baseUrl}/api/v1${resource}`,
    json: true,
  };
  Object.assign(options, option);

  try {
    return await this.helpers.request(options);
  } catch (error) {
    throw new NodeApiError(this.getNode(), error as JsonObject);
  }
}

export async function myServiceApiRequestAllItems(
  this: IExecuteFunctions | IHookFunctions | ILoadOptionsFunctions,
  propertyName: string,
  method: IHttpRequestMethods,
  endpoint: string,
  body: IDataObject = {},
  query: IDataObject = {},
): Promise<any[]> {
  const returnData: IDataObject[] = [];
  let responseData;
  query.limit = 100;
  query.offset = 0;

  do {
    responseData = await myServiceApiRequest.call(this, method, endpoint, body, query);
    returnData.push(...(responseData[propertyName] as IDataObject[]));
    query.offset = (query.offset as number) + (query.limit as number);
  } while (responseData[propertyName]?.length === query.limit);

  return returnData;
}
```

### Pagination Variants

**Cursor-based:**
```typescript
let cursor: string | undefined;
do {
  if (cursor) query.cursor = cursor;
  responseData = await myServiceApiRequest.call(this, method, endpoint, body, query);
  returnData.push(...responseData.results);
  cursor = responseData.next_cursor;
} while (cursor);
```

**Page-number:**
```typescript
let page = 1;
do {
  query.page = page;
  responseData = await myServiceApiRequest.call(this, method, endpoint, body, query);
  returnData.push(...responseData.items);
  page++;
} while (responseData.items.length > 0);
```

---

## Minimal Declarative Node

```typescript
import { INodeType, INodeTypeDescription, NodeConnectionType } from 'n8n-workflow';

export class TodoService implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'Todo Service',
    name: 'todoService',
    icon: 'file:todoservice.svg',
    group: ['transform'],
    version: 1,
    subtitle: '={{$parameter["operation"]}}',
    description: 'Manage todos via REST API',
    defaults: { name: 'Todo Service' },
    inputs: [NodeConnectionType.Main],
    outputs: [NodeConnectionType.Main],
    credentials: [{ name: 'todoServiceApi', required: true }],
    requestDefaults: {
      baseURL: 'https://api.todoservice.com/v1',
      headers: { Accept: 'application/json' },
    },
    properties: [
      {
        displayName: 'Operation',
        name: 'operation',
        type: 'options',
        noDataExpression: true,
        options: [
          {
            name: 'Create',
            value: 'create',
            action: 'Create a todo',
            routing: {
              request: { method: 'POST', url: '/todos' },
            },
          },
          {
            name: 'Get',
            value: 'get',
            action: 'Get a todo',
            routing: {
              request: { method: 'GET', url: '=/todos/{{$parameter.todoId}}' },
            },
          },
          {
            name: 'Get Many',
            value: 'getAll',
            action: 'Get many todos',
            routing: {
              request: { method: 'GET', url: '/todos' },
              output: {
                postReceive: [
                  { type: 'rootProperty', properties: { property: 'data' } },
                ],
              },
            },
          },
        ],
        default: 'create',
      },
      {
        displayName: 'Todo ID',
        name: 'todoId',
        type: 'string',
        required: true,
        default: '',
        displayOptions: { show: { operation: ['get'] } },
      },
      {
        displayName: 'Title',
        name: 'title',
        type: 'string',
        required: true,
        default: '',
        displayOptions: { show: { operation: ['create'] } },
        routing: { send: { type: 'body', property: 'title' } },
      },
    ],
  };
  // No execute() method — handled by n8n's routing engine
}
```

---

## Minimal Programmatic Node

```typescript
import type { IExecuteFunctions, IDataObject, INodeExecutionData } from 'n8n-workflow';
import { INodeType, INodeTypeDescription, NodeConnectionType, NodeApiError } from 'n8n-workflow';
import { myServiceApiRequest, myServiceApiRequestAllItems } from './GenericFunctions';

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
    credentials: [{ name: 'myServiceApi', required: true }],
    properties: [
      // ... resource/operation selectors and fields (see SKILL.md)
    ],
  };

  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    const items = this.getInputData();
    const returnData: INodeExecutionData[] = [];
    const resource = this.getNodeParameter('resource', 0) as string;
    const operation = this.getNodeParameter('operation', 0) as string;

    for (let i = 0; i < items.length; i++) {
      try {
        let responseData;

        if (resource === 'task') {
          if (operation === 'create') {
            const name = this.getNodeParameter('name', i) as string;
            const additionalFields = this.getNodeParameter('additionalFields', i) as IDataObject;
            responseData = await myServiceApiRequest.call(
              this, 'POST', '/tasks', { name, ...additionalFields },
            );
          }
          if (operation === 'get') {
            const taskId = this.getNodeParameter('taskId', i) as string;
            responseData = await myServiceApiRequest.call(this, 'GET', `/tasks/${taskId}`);
          }
          if (operation === 'getAll') {
            const returnAll = this.getNodeParameter('returnAll', i) as boolean;
            if (returnAll) {
              responseData = await myServiceApiRequestAllItems.call(
                this, 'tasks', 'GET', '/tasks',
              );
            } else {
              const limit = this.getNodeParameter('limit', i) as number;
              const response = await myServiceApiRequest.call(
                this, 'GET', '/tasks', {}, { limit },
              );
              responseData = response.tasks;
            }
          }
          if (operation === 'delete') {
            const taskId = this.getNodeParameter('taskId', i) as string;
            responseData = await myServiceApiRequest.call(
              this, 'DELETE', `/tasks/${taskId}`,
            );
          }
        }

        const executionData = this.helpers.constructExecutionMetaData(
          this.helpers.returnJsonArray(responseData as IDataObject[]),
          { itemData: { item: i } },
        );
        returnData.push(...executionData);

      } catch (error) {
        if (this.continueOnFail()) {
          const executionErrorData = this.helpers.constructExecutionMetaData(
            this.helpers.returnJsonArray({ error: (error as Error).message }),
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

---

## Codex File Template (MyService.node.json)

```json
{
  "node": "n8n-nodes-myservice.myService",
  "nodeVersion": "1.0",
  "codexVersion": "1.0",
  "categories": ["Miscellaneous"],
  "resources": {
    "credentialDocumentation": [
      { "url": "https://docs.myservice.com/api/auth" }
    ],
    "primaryDocumentation": [
      { "url": "https://docs.myservice.com/api" }
    ]
  }
}
```

**`node` field format:** `<npm-package-name>.<node-internal-name>`

---

## package.json Template

```json
{
  "name": "n8n-nodes-myservice",
  "version": "0.1.0",
  "description": "n8n node for My Service",
  "keywords": ["n8n-community-node-package"],
  "license": "MIT",
  "main": "index.js",
  "files": ["dist"],
  "scripts": {
    "build": "tsc && gulp build:icons",
    "dev": "tsc --watch",
    "lint": "eslint nodes credentials --ext .ts",
    "lintfix": "eslint nodes credentials --ext .ts --fix"
  },
  "n8n": {
    "n8nNodesApiVersion": 1,
    "nodes": [
      "dist/nodes/MyService/MyService.node.js"
    ],
    "credentials": [
      "dist/credentials/MyServiceApi.credentials.js"
    ]
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "gulp": "^4.0.2",
    "n8n-workflow": "*",
    "typescript": "~5.0"
  },
  "peerDependencies": {
    "n8n-workflow": "*"
  }
}
```

**Key points:**
- `name` must start with `n8n-nodes-`
- `keywords` must include `"n8n-community-node-package"` for discovery
- `n8n.nodes` and `n8n.credentials` point to compiled `dist/` paths
- `n8n-workflow` is a peer dependency, not bundled
