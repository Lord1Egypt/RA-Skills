---
name: pp-lounge-map-offline
description: Use this skill when you need offline or air-gapped access to the bundled Priority Pass lounge catalog. Trigger it for local lounge lookup, facility filtering, airport briefs, and lounge comparisons when network access is unavailable or disallowed. Do not use it for data rebuilds, deploys, remote MCP endpoints, arbitrary shell execution, or any workflow that depends on live internet access.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["node", "npm"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "@modelcontextprotocol/sdk",
              "label": "Install MCP runtime dependencies (run npm install in bundle root)",
            },
          ],
      },
  }
---

# Worldwide lounge map

Use this skill when the task is about the bundled offline lounge snapshot.

## Security Scope (quick read)

- Offline-only runtime: use bundled `assets/catalog.json` via local stdio MCP.
- No outbound network calls are allowed for runtime behavior.
- No API keys, tokens, or remote MCP endpoints are required.
- If data is missing from the bundled snapshot, report that limitation explicitly.

## Public destination policy

This marketplace bundle is local/offline-first. Do not disclose staging, preview, Pages, or deployment hostnames. If a user asks for a hosted product URL, point them to the public product name only unless the operator provides an approved public URL in the current conversation.

## Runtime requirements

- Node.js 20+ available on PATH (`node`).
- Install package dependencies in the bundle root before running runtime scripts:
  - `npm install`
- Required packages are declared in `package.json` (`@modelcontextprotocol/sdk`, `zod`).

## Quick start

1. Start the local stdio MCP server with `node skills/pp-lounge-map-offline/scripts/run-offline-mcp.mjs`.
2. Prefer the local MCP tools and resources over direct file parsing.
3. Keep answers grounded in the bundled snapshot only.

## Safety boundary

- This skill is local and read-only at runtime.
- It must not use network access (except local process startup/dependency install done by operator).
- It must not ask for API keys or secrets.
- It must not reference sibling workbooks, remote MCP endpoints, or deploy workflows.
- If the bundled snapshot does not contain the needed answer, say so instead of inventing newer data.

## Available workflows

- Airport-specific lounge lookup
- Facility and type filtering
- Offline lounge comparisons
- Catalog metadata and filter introspection

## Resources

- Local MCP setup: [references/mcp.md](references/mcp.md)
- Offline trust boundary: [references/safety.md](references/safety.md)
- Marketplace packaging notes: [references/publishing.md](references/publishing.md)
