---
name: openclaw-readonly-consumer
description: Keep an OpenClaw-style local runtime on the snapshot-first, thin-BFF-first, read-only Campus Copilot path.
---

# OpenClaw-Style Read-Only Consumer

Use this skill when your local operator/runtime behaves like an OpenClaw-style shell and you want Campus Copilot to stay on the **snapshot-first / thin-BFF-first / read-only** side.

Think of Campus Copilot as the labeled binder on the desk:

- Campus Copilot provides structured academic context
- your local runtime decides how to consume that context
- Campus Copilot does **not** become a browser-control plugin or write-capable operator loop

## Start with the narrowest path

1. If you need cross-site health, provider readiness, read-only ask, or export tools, start with:
   - `pnpm --filter @campus-copilot/mcp-server start`
2. If you only need one site's snapshot records, use:
   - `pnpm --filter @campus-copilot/mcp-readonly start:<site>`
3. If you only need local provider status or cited-AI chat on the Campus semantic contract, use:
   - `pnpm start:api`

## Inputs

- one local snapshot such as `examples/workspace-snapshot.sample.json`
- one local runtime that can launch stdio commands
- optional support for the same `mcpServers` JSON shape used by Codex/Claude-style MCP setups

## Recommended flow

1. Export a safe snapshot path:
   - `export CAMPUS_COPILOT_SNAPSHOT="$PWD/examples/workspace-snapshot.sample.json"`
2. Start with the generic MCP server unless you already know you only need one site.
3. If your runtime explicitly accepts the same `mcpServers` JSON shape, adapt:
   - `examples/integrations/codex-mcp.example.json`
   - `examples/integrations/claude-code-mcp.example.json`
4. If it does **not** accept that exact shape, stay with the direct command snippets from:
   - `examples/openclaw-readonly.md`
5. Keep all claims snapshot-scoped and read-only.

## Good fit

- OpenClaw-style local consumers that need one truthful starting recipe
- imported snapshot review without reopening live browser automation
- read-only MCP or local BFF consumption over Campus-owned semantics

## Not a fit

- live browser takeover
- posting, replying, or submitting on external sites
- inventing an official plugin or marketplace contract
- hosted autonomy positioning

## Recommended repo-local references

- `examples/openclaw-readonly.md`
- `examples/README.md`
- `skills/read-only-workspace-analysis/SKILL.md`
- `skills/site-mcp-consumer/SKILL.md`
