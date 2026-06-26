# GrayMatter MCP Server

An MCP (Model Context Protocol) server that wraps the ValkyrAI `api-0` REST API, exposing GrayMatter durable memory, SwarmOps graph state, and live business schema as tools for Claude.ai, Claude Code, Cursor, and any other MCP-compatible host.

## Quick Start

```bash
git clone https://github.com/ValkyrLabs/GrayMatter.git
cd GrayMatter/mcp-server
npm install
export VALKYR_AUTH_TOKEN=<your-token>
npm start
```

The server runs on `http://localhost:3333` by default.

For Codex plugin-managed launch, use stdio:

```bash
npm run stdio
```

The repo-level `.mcp.json` points Codex at `node mcp-server/index.js --stdio`.

## Environment Variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `VALKYR_AUTH_TOKEN` | Recommended | none | Bearer token from `scripts/gm-login`. Can also be passed per request through `X-Valkyr-Token`. |
| `VALKYR_API_BASE` | No | `https://api-0.valkyrlabs.com/v1` | API base to target. Use hosted api-0, a self-hosted api-0, or a local GrayMatter Light ThorAPI instance. |
| `GRAYMATTER_WIDGET_DOMAIN` | No | `https://graymatter.valkyrlabs.com` | Public widget origin advertised in Apps SDK resource metadata for ChatGPT app review. |
| `PORT` | No | `3333` | HTTP port to listen on. |

Get a hosted token:

```bash
scripts/gm-login
```

For local GrayMatter Light, start the ThorAPI instance and point the MCP server at it:

```bash
scripts/gm-light-up
source .graymatter-light/.graymatter-light-env
cd mcp-server
VALKYR_API_BASE=http://localhost:8080 GRAYMATTER_LIGHT_MODE=true npm start
```

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/sse` | SSE stream; connect Claude.ai here with the paired message endpoint. |
| `POST` | `/message` | JSON-RPC message endpoint paired with `/sse`. |
| `POST` | `/mcp` | Public Apps SDK MCP endpoint for ChatGPT connector setup and app review. |
| `POST` | `/` | Direct JSON-RPC endpoint for simpler clients and tests. |
| `GET` | `/health` | Readiness check with configured API base and exposed tools. |

Stdio mode exposes the same JSON-RPC methods over newline-delimited stdin/stdout and does not print startup text to stdout.

The server also implements `resources/list` and `resources/read` for the Apps SDK overview widget at `ui://graymatter/overview.html`. Tool descriptors include Apps SDK security scheme mirrors, tool invocation status text, and action annotations for review.

## Available Tools

| Tool | Backing API path | Description |
| --- | --- | --- |
| `memory_write` | `POST /MemoryEntry` | Write a durable `MemoryEntry` (`decision`, `todo`, `context`, `artifact`, or `preference`). |
| `memory_read` | `GET /MemoryEntry/{id}` | Read a `MemoryEntry` by ID. |
| `memory_query` | `POST /MemoryEntry/query` | Semantic search across GrayMatter memory. Hosted api-0 may consume credits. |
| `graph_get` | `GET /SwarmOps/graph` | Inspect the SwarmOps shared object graph. |
| `entity_list` | `GET /{entityType}` | List business entities such as `Customer`, `Task`, `Invoice`, or `Goal`. |
| `entity_get` | `GET /{entityType}/{id}` | Fetch a single entity by type and ID. |
| `entity_create` | `POST /{entityType}` | Create one entity when RBAC permits it. |
| `schema_summary` | `GET /api-docs` | Summarize the live ValkyrAI OpenAPI schema. |

## Scoped Memory

`memory_write` and `memory_query` accept optional scope fields so agents can retrieve memory for the current chat, workspace, automation, or session without relying on loose tag matching.

Supported fields:
- `sourceChannel`
- `scope`
- `runtime`
- `user`
- `workspaceKey`
- `chatKey`
- `sessionKey`
- `automationId`
- `artifactPath`
- `scopePath`

When `sourceChannel` is not provided, the server derives it from the strongest available scope. A path like `$HOME/.codex/automations/mcp-and-skill-hunter/memory.md` becomes `codex:automation:mcp-and-skill-hunter`; a Codex workspace path under `Documents/Codex/<date>/<slug>` becomes `codex:workspace:<date>/<slug>`. `memory_write` preserves the hierarchy in a compact `[graymatter-scope]` header inside `MemoryEntry.text`, while `memory_query` sends the derived value as the api-0 `source` filter.

## Connect to Claude.ai

1. Run the server somewhere Claude.ai can reach it.
2. In Claude.ai, add an MCP server integration using `https://your-host/sse`.
3. Add header `X-Valkyr-Token: <your-token>`.

For local testing, expose port `3333` with a tunnel and use the tunnel URL plus `/sse`.

```bash
npm start &
ngrok http 3333
```

## Connect to Claude Code

Add an HTTP MCP server entry that points at the message endpoint:

```json
{
  "graymatter": {
    "transport": "http",
    "url": "http://localhost:3333/message",
    "headers": {
      "X-Valkyr-Token": "<your-token>"
    }
  }
}
```

## Per-Request Auth

For multi-tenant deployments, do not set a shared `VALKYR_AUTH_TOKEN`. Pass each user's token through `X-Valkyr-Token` so all api-0 calls stay scoped to that user's RBAC permissions.

## Production Notes

Railway, Fly.io, and Docker deployments all work as long as the server can reach `VALKYR_API_BASE` and callers provide auth through either `VALKYR_AUTH_TOKEN` or `X-Valkyr-Token`.

For ChatGPT app submission:

1. Deploy this server on a public HTTPS domain.
2. Submit the connector URL as `https://your-host/mcp`.
3. Set `GRAYMATTER_WIDGET_DOMAIN` to the public origin that hosts the widget surface.
4. Provide the GrayMatter privacy policy URL, screenshots, test prompts, and reviewer test credentials through the OpenAI Platform Dashboard only.
5. Do not commit reviewer passwords, tokens, OAuth secrets, or MFA recovery material.

Minimal Dockerfile:

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY index.js ./
EXPOSE 3333
CMD ["node", "index.js"]
```

## Credits

Some hosted GrayMatter operations, notably `memory_query`, consume api-0 credits. Fresh signups should receive 500 starter credits automatically. Recharge at <https://valkyrlabs.com/buy-credits>.
