---
name: npm-n8n-nodes
description: >
  Build, structure, and publish npm packages for n8n custom community nodes. Use this skill
  whenever the user wants to create a custom n8n node, publish a node to npm, add credentials
  or authentication to an n8n node, handle HTTP requests inside a node, define node UI properties,
  scaffold a new n8n node package, wire up OAuth2 / API key / header auth, handle request bodies
  and responses, work with binary files in n8n, create trigger or webhook nodes, handle errors,
  version nodes, or publish a community node to npm. Also trigger when user mentions "n8n node",
  "community node", "custom integration", "n8n-nodes-*", "IExecuteFunctions", "ICredentialType",
  "INodeType", "n8n workflow node", or "n8n trigger". This skill covers the FULL lifecycle:
  scaffold → code → credentials → test → publish.
---

# n8n Custom Node — NPM Package Skill

## Core Mental Model

Every n8n node follows one pattern:

```
getInputData()  →  loop items  →  do stuff  →  push to returnData  →  return [returnData]
```

Two file types do all the work:
- **Node file** (`nodes/MyNode/MyNode.node.ts`) — UI fields + execute logic
- **Credential file** (`credentials/MyApi.credentials.ts`) — auth definition

Everything else is project plumbing.

---

## Project Structure

```
n8n-nodes-yourservice/
├── package.json              ← CRITICAL: must have n8n section + correct keyword
├── tsconfig.json
├── .eslintrc.js
├── gulpfile.js               ← copies SVG icons to dist/
├── index.js                  ← optional explicit entry point
├── nodes/
│   └── YourService/
│       ├── YourService.node.ts
│       ├── YourService.node.json   ← optional: codex metadata
│       └── yourservice.svg
├── credentials/
│   └── YourServiceApi.credentials.ts
└── dist/                     ← compiled output (never edit manually)
```

---

## What to Read and When

This skill has focused reference files. Load only what you need:

### Node Types (pick one)
| If you need... | Read |
|---|---|
| Standard request/response node (most common) | `references/examples/nodes/programmatic-node.md` |
| Simple REST API, no complex logic | `references/examples/nodes/declarative-node.md` |
| Trigger that polls an API on a schedule | `references/examples/nodes/trigger-node.md` |
| Webhook that receives HTTP calls | `references/examples/nodes/webhook-node.md` |

### Credentials (pick what matches your auth)
| Auth type | Read |
|---|---|
| API key, Bearer token, custom header, query key | `references/examples/credentials/api-key-patterns.md` |
| OAuth2 (user login or machine-to-machine) | `references/examples/credentials/oauth2-patterns.md` |
| Basic auth, multi-field, manual inject | `references/examples/credentials/other-patterns.md` |

### Concepts (load when the topic comes up)
| Topic | Read |
|---|---|
| UI field types, displayOptions, collections, fixedCollection | `references/concepts/node-properties.md` |
| HTTP requests, bodies, headers, responses, binary | `references/concepts/http-and-binary.md` |
| Error types, continueOnFail, NodeApiError vs NodeOperationError | `references/concepts/error-handling.md` |
| pairedItem, data flow, why item tracking matters | `references/concepts/data-and-pairing.md` |
| Node versioning, updating without breaking workflows | `references/concepts/node-versioning.md` |

### Project Setup & Publishing
| Topic | Read |
|---|---|
| package.json, tsconfig, gulpfile, eslintrc, index.js | `references/templates/project-files.md` |
| Local testing, npm link, n8n start | `references/templates/local-testing.md` |
| npm publish, GitHub Actions, provenance | `references/templates/publishing.md` |
| Common gotchas and silent failures | `references/gotchas/common-gotchas.md` |

---

## Quick-Start Pattern (copy this first)

```typescript
// nodes/YourService/YourService.node.ts
import {
  IExecuteFunctions,
  INodeExecutionData,
  INodeType,
  INodeTypeDescription,
  NodeOperationError,
} from 'n8n-workflow';

export class YourService implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'Your Service',
    name: 'yourService',
    icon: 'file:yourservice.svg',
    group: ['transform'],
    version: 1,
    description: 'Interact with Your Service API',
    defaults: { name: 'Your Service' },
    inputs: ['main'],
    outputs: ['main'],
    credentials: [{ name: 'yourServiceApi', required: true }],
    properties: [
      {
        displayName: 'Endpoint',
        name: 'endpoint',
        type: 'string',
        default: '/users',
        required: true,
      },
    ],
  };

  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    const items = this.getInputData();
    const returnData: INodeExecutionData[] = [];
    const credentials = await this.getCredentials('yourServiceApi');

    for (let i = 0; i < items.length; i++) {
      try {
        const endpoint = this.getNodeParameter('endpoint', i) as string;

        const response = await this.helpers.httpRequest({
          method: 'GET',
          url: `https://api.yourservice.com${endpoint}`,
          headers: {
            Authorization: `Bearer ${credentials.apiToken}`,
          },
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

## Essential APIs Cheat Sheet

```typescript
// Input
const items = this.getInputData();

// Parameters
this.getNodeParameter('name', i) as string
this.getNodeParameter('count', i, 0) as number
this.getNodeParameter('options', i, {}) as IDataObject

// Credentials
const creds = await this.getCredentials('myCredentialName');

// HTTP
await this.helpers.httpRequest({ method, url, headers, qs, body })

// Error handling
this.continueOnFail()
throw new NodeOperationError(this.getNode(), message, { itemIndex: i })
throw new NodeApiError(this.getNode(), error)   // for API-level HTTP errors

// Output
returnData.push({ json: data, pairedItem: { item: i } })
return [returnData];
```

---

## Pre-Publish Checklist

- [ ] `keywords` in package.json includes `"n8n-community-node-package"`
- [ ] `n8n.nodes` and `n8n.credentials` arrays point to `dist/` `.js` paths
- [ ] Node `name` is camelCase; `displayName` is human-readable
- [ ] Credential `name` exactly matches string passed to `getCredentials('...')`
- [ ] Every `returnData.push()` includes `pairedItem: { item: i }`
- [ ] `continueOnFail()` is handled in all try/catch blocks
- [ ] SVG icon exists in `nodes/YourService/` and referenced as `'file:yourservice.svg'`
- [ ] `npm run build` succeeds (no TypeScript errors)
- [ ] `npm run lint` passes (required for community submission)
- [ ] Tested locally via `npm link`
- [ ] Version bumped in `package.json` before publish
