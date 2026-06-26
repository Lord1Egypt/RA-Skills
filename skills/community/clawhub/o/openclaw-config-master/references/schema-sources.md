# OpenClaw Config: Schema Sources

This skill is designed to prevent schema bugs (wrong key/type/missing constraint) that can stop the OpenClaw Gateway from starting or cause unsafe behavior changes.
The config format is **JSON5**, and most config objects are **strict** (unknown keys fail validation).

Reference source version: `openclaw/openclaw@v2026.3.28` (schema generated 2026-03-22).
Fields can change across versions, so prefer the schema from the OpenClaw version you are actually running.

## Priority: How To Confirm A Field Exists

1. When the Gateway is running (recommended)
   - Fetch the JSON Schema:
     - `openclaw gateway call config.schema --params '{}'`
   - Use `jq` or grep/search on the schema to confirm the field path exists before writing keys.

2. When the Gateway is not running / you need source-level constraints
   - Clone source:
     - `git clone https://github.com/openclaw/openclaw.git`
     - `git checkout v2026.3.28`
   - Key schema files:
     - Root schema: `src/config/zod-schema.ts` (`OpenClawSchema`)
     - `$include` semantics: `src/config/includes.ts`
     - agents/tools: `src/config/zod-schema.agents.ts`, `src/config/zod-schema.agent-defaults.ts`, `src/config/zod-schema.agent-runtime.ts`
     - models: `src/config/zod-schema.core.ts` (`ModelsConfigSchema`)
     - channels: `src/config/zod-schema.providers.ts`, `src/config/zod-schema.providers-core.ts`, `src/config/zod-schema.providers-whatsapp.ts`
     - session/messages/commands: `src/config/zod-schema.session.ts`
     - approvals: `src/config/zod-schema.approvals.ts`
     - acp: `src/config/zod-schema.acp.ts` (**new in 2026.3.28**)
     - mcp: `src/config/zod-schema.mcp.ts` (**new in 2026.3.28**)
   - Repo docs with lots of examples:
     - `docs/gateway/configuration.md`

## Fast Navigation (Do Not Guess Keys)

Run from the openclaw repo root:

```bash
git checkout v2026.3.28

rg -n "export const OpenClawSchema" src/config/zod-schema.ts
rg -n "\\bgateway:\\s*z" src/config/zod-schema.ts
rg -n "\\bskills:\\s*z" src/config/zod-schema.ts
rg -n "\\bplugins:\\s*z" src/config/zod-schema.ts

rg -n "export const ChannelsSchema" src/config/zod-schema.providers.ts
rg -n "DiscordConfigSchema|TelegramConfigSchema|SlackConfigSchema" src/config/zod-schema.providers-core.ts

rg -n "export const ModelsConfigSchema" src/config/zod-schema.core.ts
rg -n "export const ToolsSchema" src/config/zod-schema.agent-runtime.ts
```

## Schema Notes for v2026.3.28

### `bindings` — Structure Changed
The `bindings` schema changed from an **object** of route entries to an **array** of route objects:
```json
bindings: [{
  type: "route",
  agentId: string,
  match: { channel, accountId, peer, ... }
}]
```
When migrating configs, restructure `bindings` from object form to array form.

### New Top-Level Keys
The following root keys **did not exist** in `openclaw/openclaw@875324e`:
- `acp` — ACP runtime configuration (dispatch, backend, stream settings, defaultAgent, etc.)
- `mcp` — MCP (Model Context Protocol) servers configuration
- `cli` — CLI-specific configuration
- `secrets` — Secrets management

### New Schema Files (not present in older versions)
- `src/config/zod-schema.acp.ts` — ACP runtime schema
- `src/config/zod-schema.mcp.ts` — MCP servers schema
- `src/config/zod-schema.approvals.ts` — Approvals policy (exec/plugin modes)

## How To Read Validation Errors

`openclaw doctor` issues usually include:
- `path`: failing field path (most important)
- `message`: why it failed (type mismatch, unknown key, missing required key, cross-field constraint, etc.)

Fix strategy:
- **Unknown key**: the key does not exist in the schema (or is misspelled). Confirm the correct name in schema.
- **Type mismatch**: change to the schema's expected type (number/string/boolean/object/array).
- **Constraint failure (superRefine)**: satisfy related fields described by the message (for example: some channels require `allowFrom` to include `"*"` when `dmPolicy="open"`).
