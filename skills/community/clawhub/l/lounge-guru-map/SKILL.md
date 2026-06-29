---
name: lounge-guru-map
description: Use this skill when you need offline or air-gapped access to a bundled airport lounge catalog across participating lounge programs and sources. Trigger it for any lounge lookup, facility filtering, airport lounge briefs, and lounge comparisons when network access is unavailable or disallowed. Do not use it for data rebuilds, deploys, remote MCP endpoints, arbitrary shell execution, or any workflow that depends on live internet access.
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

# Lounge Guru Map

Use this skill when the task is about lounges covered by the bundled offline airport-lounge snapshot. The catalog is program-agnostic from the user perspective: answer for any lounge present in the data, not only one lounge network.

## Security Scope (quick read)

- Offline-only runtime: use bundled `assets/catalog.json` via local stdio MCP. Treat it as a general airport-lounge catalog, not a single-program entitlement source.
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

1. Start the local stdio MCP server with `node skills/lounge-guru-map/scripts/run-offline-mcp.mjs`.
2. Prefer the local MCP tools and resources over direct file parsing.
3. Keep answers grounded in the bundled snapshot only.

## Safety boundary

- This skill is local and read-only at runtime.
- It must not use network access (except local process startup/dependency install done by operator).
- It must not ask for API keys or secrets.
- It must not reference sibling workbooks, remote MCP endpoints, or deploy workflows.
- If the bundled snapshot does not contain the needed answer, say so instead of inventing newer data.

## Available workflows

- Airport-specific lookup for any covered lounge
- Facility, access, network, terminal, and type filtering when present in the catalog
- Offline lounge comparisons across all covered lounge records
- Catalog metadata and filter introspection

## Resources

- Local MCP setup: [references/mcp.md](references/mcp.md)
- Offline trust boundary: [references/safety.md](references/safety.md)
- Marketplace packaging notes: [references/publishing.md](references/publishing.md)
