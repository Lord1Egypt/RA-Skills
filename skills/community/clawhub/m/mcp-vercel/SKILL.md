---
name: mcp-vercel
description: "Deploy a remote MCP server on Vercel with Next.js and mcp-handler. Use this skill whenever the user wants to create an MCP server, deploy MCP to Vercel, set up a remote MCP endpoint, add MCP tools to a Next.js app, or host an MCP server in the cloud. Also triggers on: 'deploy MCP', 'remote MCP', 'MCP endpoint', 'mcp-handler', 'MCP on Vercel', 'Streamable HTTP MCP', 'Claude connector backend', 'host MCP server for Claude Desktop'. Even if the user just says 'I want to make my API available to Claude' or 'set up an MCP server', use this skill."
license: MIT
metadata:
  author: lucaperret
  version: "1.0.0"
  openclaw:
    emoji: "\u25B2"
    homepage: https://github.com/lucaperret/agent-skills
---

# Deploy MCP Server on Vercel

Create a production-ready remote MCP server on Vercel using Next.js and `mcp-handler`. The server communicates via Streamable HTTP and works with Claude Desktop, claude.ai, Smithery, and any MCP client.

## Why this approach

Vercel's serverless functions are ideal for MCP servers because MCP's Streamable HTTP transport is stateless — each request is independent, which maps perfectly to serverless. No persistent connections needed. The `mcp-handler` package from Vercel handles all the protocol details.

## Quick setup

### 1. Install dependencies

```bash
npm install mcp-handler @modelcontextprotocol/sdk zod
```

### 2. Create the MCP route

Create `app/api/mcp/route.ts`:

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { createMcpHandler } from 'mcp-handler';
import { z } from 'zod';

const handler = createMcpHandler(
  (server: McpServer) => {
    // Register your tools here
    server.tool(
      'example_tool',
      'What this tool does — be specific',
      { query: z.string().describe('What the parameter is for') },
      { readOnlyHint: true, destructiveHint: false, title: 'Example Tool' },
      async ({ query }) => ({
        content: [{ type: 'text', text: `Result for: ${query}` }],
      }),
    );
  },
  {
    serverInfo: { name: 'my-server', version: '1.0.0' },
  },
  {
    streamableHttpEndpoint: '/api/mcp',
    maxDuration: 60,
  },
);

export { handler as GET, handler as POST, handler as DELETE };
```

### 3. Deploy and test

```bash
vercel deploy --prod

# Verify
curl -X POST https://your-app.vercel.app/api/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}},"id":1}'
```

You should get back `serverInfo` with your server name and version.

## Tool design

### Safety annotations (required)

Every tool must have annotations. MCP clients use these to decide how cautiously to invoke tools.

```typescript
// Read-only (search, get, list, fetch)
{ readOnlyHint: true, destructiveHint: false, title: 'Search Items' }

// Write but not destructive (create, add, update)
{ readOnlyHint: false, destructiveHint: false, title: 'Create Item' }

// Destructive (delete, remove, overwrite)
{ readOnlyHint: false, destructiveHint: true, title: 'Delete Item' }
```

### Parameter descriptions

Every parameter needs a `.describe()` — this is how MCP clients know what to pass.

```typescript
{
  query: z.string().describe('Search query text'),
  limit: z.number().optional().default(10).describe('Max results to return'),
  type: z.enum(['artist', 'album', 'track']).describe('Type of content'),
}
```

### MCP prompts (optional but recommended)

Prompt templates improve discoverability on Smithery and give users ready-made starting points.

```typescript
server.prompt('find_items', 'Search for items by name',
  { name: z.string().describe('Item name') },
  ({ name }) => ({
    messages: [{
      role: 'user' as const,
      content: { type: 'text' as const, text: `Find ${name} and show details` },
    }],
  }),
);
```

## Routing — the `streamableHttpEndpoint` gotcha

Use `streamableHttpEndpoint`, NOT `basePath`:

```typescript
// CORRECT — endpoint at /api/mcp
{ streamableHttpEndpoint: '/api/mcp' }

// WRONG — creates endpoint at /api/mcp/mcp (doubled path)
{ basePath: '/api/mcp' }
```

The `basePath` option appends `/mcp` to whatever you give it. Since your route file is already at `app/api/mcp/route.ts`, that creates `/api/mcp/mcp`.

## Vercel deployment pitfalls

### Root Directory isolation

If your Vercel project uses a Root Directory (like `site/`), the deployed function CANNOT access files outside that directory. This means `import from '../../dist/'` will fail at runtime even if it compiles locally.

**Solution:** Copy compiled files into the site directory and commit them. Use a prebuild script to keep them in sync:

```javascript
// scripts/copy-deps.js
const fs = require('fs');
const path = require('path');
const src = path.resolve(__dirname, '../../dist');
const dest = path.resolve(__dirname, '../lib/deps');
fs.mkdirSync(dest, { recursive: true });
for (const file of fs.readdirSync(src)) {
  if (file.endsWith('.js') || file.endsWith('.d.ts')) {
    fs.copyFileSync(path.join(src, file), path.join(dest, file));
  }
}
```

Add to package.json: `"prebuild": "node scripts/copy-deps.js"`

### Serverless read-only filesystem

Vercel functions run on a read-only filesystem with no home directory. If your code writes files (sessions, temp data), wrap in try/catch:

```typescript
try {
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(filepath, data);
} catch {
  // Serverless environment — skip filesystem writes
}
```

### Turbopack CJS/ESM mismatch

If importing CommonJS `.js` files while the parent `package.json` doesn't have `"type": "module"`, Turbopack will error. Solution: import from compiled `.js` files bundled within the site directory, not from TypeScript source files in the parent.

## Adding authentication

For OAuth-protected servers, see the `mcp-oauth` skill which covers the complete OAuth 2.0 PKCE flow with `withMcpAuth`, including dynamic client registration and token storage.

## Publishing to Smithery

After deploying, publish to [Smithery](https://smithery.ai) for broader distribution:

1. Go to https://smithery.ai/new
2. Enter your MCP server URL
3. Choose a namespace/server-id
4. Smithery scans your tools automatically

If your server requires auth, Smithery will prompt you to connect during scanning.

## Reference

- [mcp-handler](https://github.com/vercel/mcp-handler)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Vercel MCP docs](https://vercel.com/docs/mcp)
