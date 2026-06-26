---
name: pctx
description: MCP aggregation and Code Mode execution layer for token-efficient agent workflows. Wraps portofcontext/pctx — connects agents to Linear, GitHub, and other MCP servers via a single local endpoint. Use when agents need to call MCP tools or batch multiple tool calls into a single TypeScript execution to reduce token cost.
homepage: https://github.com/portofcontext/pctx
metadata: {"clawdis":{"emoji":"🔌","requires":{"tools":["brew","npm","node"]}}}
---

# pctx — MCP Aggregation & Code Mode Execution

## What is pctx?

pctx is a local server that:
1. **Aggregates MCP servers** — connects to Linear, GitHub, and other MCP backends behind one endpoint
2. **Code Mode** — instead of sequential tool calls, agents write TypeScript that runs in a Deno sandbox; only the result comes back (up to 98% token reduction on complex workflows)

**Live endpoint:** `http://127.0.0.1:8080/mcp`
**Connected MCPs:** Linear (42 tools), GitHub (41 tools)
**Config:** `~/.config/pctx/pctx.json`
**Logs:** `/tmp/pctx.log` | `/tmp/pctx.err`

---

## When to use

- Agent needs to call Linear or GitHub tools via MCP
- Agent is doing multi-step tool workflows (pctx batches them into one TypeScript call)
- Any workflow where sequential tool calls return large intermediate payloads

---

## Quick Start

```bash
# Check if pctx is running
{baseDir}/pctx-skill.sh status

# List connected MCP servers + tool counts
{baseDir}/pctx-skill.sh mcp-list

# Test a tool call
{baseDir}/pctx-skill.sh test linear linear_getOrganization
{baseDir}/pctx-skill.sh test github list_issues
```

---

## Commands

### Daemon Management

```bash
# Status — shows port, uptime
{baseDir}/pctx-skill.sh status

# Start daemon (launchd)
{baseDir}/pctx-skill.sh start

# Stop daemon
{baseDir}/pctx-skill.sh stop

# Restart
{baseDir}/pctx-skill.sh restart
```

### MCP Server Management

```bash
# List all connected MCPs + tool counts + connection health
{baseDir}/pctx-skill.sh mcp-list

# Add an upstream MCP — examples:
# stdio MCP with npm package
{baseDir}/pctx-skill.sh mcp-add memory --command "npx" --arg "-y" --arg "@modelcontextprotocol/server-memory"

# stdio MCP with installed binary
{baseDir}/pctx-skill.sh mcp-add linear --command "mcp-linear" --env "LINEAR_API_TOKEN=your_token"

# HTTP MCP
{baseDir}/pctx-skill.sh mcp-add stripe https://mcp.stripe.com

# Remove an MCP
{baseDir}/pctx-skill.sh mcp-remove <name>
```

### Config & Backup

```bash
# Backup pctx.json (always done automatically before mcp-add/remove)
{baseDir}/pctx-skill.sh config-backup

# Restore from backup (interactive if no timestamp given)
{baseDir}/pctx-skill.sh config-restore
{baseDir}/pctx-skill.sh config-restore 20260422-092733
```

### Testing

```bash
# Test a specific MCP tool via pctx
{baseDir}/pctx-skill.sh test linear linear_getOrganization
{baseDir}/pctx-skill.sh test linear linear_getTeams
{baseDir}/pctx-skill.sh test github list_issues
{baseDir}/pctx-skill.sh test github get_file_contents
```

### Install (idempotent)

```bash
# Run on new VMs or after full rollback
{baseDir}/install.sh
```

---

## Calling pctx from Agent Code

The pctx server exposes an MCP endpoint at `http://127.0.0.1:8080/mcp`. Agents can call tools directly via JSON-RPC, or use Code Mode for batched TypeScript execution.

### Simple tool call via curl

```bash
# Initialize + get session context
curl -s -X POST http://127.0.0.1:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"my-agent","version":"1.0"}}}'

# Call a tool (Code Mode — batched TypeScript)
curl -s -X POST http://127.0.0.1:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"execute_typescript","arguments":{"script":"const org = await linear.linear_getOrganization({}); const teams = await linear.linear_getTeams({}); return { org, teams };"}}}'
```

### Code Mode — batch multiple calls

The `execute_typescript` tool is the key feature. Write one script wrapped in `async function run()` that calls all tools needed:

**Important:** field name is `code` (not `script`). Code must be wrapped in `async function run() { ... }`.

Namespaces: `Linear` (capital L), `Github` (capital G, no 'b').

```typescript
// BAD — multiple round-trips (traditional MCP)
const org = await Linear.linearGetOrganization({});
// ... agent receives result, burns tokens ...
const teams = await Linear.linearGetTeams({});
// ... agent receives result, burns tokens ...

// GOOD — one Code Mode call, one result
async function run() {
  const org = await Linear.linearGetOrganization({});
  const teams = await Linear.linearGetTeams({});
  const issues = await Linear.linearSearchIssues({ query: "urgent" });
  return JSON.stringify({ org, teams, issues }, null, 2);
}

// GitHub example
async function run() {
  const branches = await Github.listBranches({ owner: "MJM-Agents", repo: "rolling-reno-theme" });
  return JSON.stringify(branches, null, 2);
}
```

---

## Currently Connected MCPs

| Name | Binary | Transport | Auth | Tools |
|------|--------|-----------|------|-------|
| linear | mcp-linear | stdio | LINEAR_API_TOKEN | 42 |
| github | github-mcp-server stdio | stdio | GITHUB_PERSONAL_ACCESS_TOKEN | 41 |

---

## Rollback

Full rollback instructions: `ROLLBACK-MCP-PCTX.md` in workspace root.

Quick rollback — remove one MCP:
```bash
{baseDir}/pctx-skill.sh mcp-remove linear   # removes Linear, leaves GitHub
{baseDir}/pctx-skill.sh mcp-remove github   # removes GitHub, leaves Linear
```

Full nuclear rollback:
```bash
{baseDir}/pctx-skill.sh stop
brew uninstall pctx github-mcp-server
npm uninstall -g @tacticlaunch/mcp-linear
rm -rf ~/.config/pctx/ ~/Library/LaunchAgents/ai.openclaw.pctx.plist
```

---

## Config

| Variable | Default | Description |
|----------|---------|-------------|
| `PCTX_CONFIG` | `~/.config/pctx/pctx.json` | Path to pctx config |
| `PCTX_PORT` | `8080` | Port pctx listens on |
| `PCTX_HOST` | `127.0.0.1` | Host pctx binds to |
| `PCTX_BIN` | auto-detected | Path to pctx binary |

---

## Notes

- pctx.json is chmod 600 — contains API keys, never commit
- Deno sandbox: 10s execution timeout, no filesystem/env/system access
- OAuth not yet supported in pctx (v0.7.1) — remote Linear/GitHub MCPs require OAuth; use stdio/local for now
- Config auto-backed-up before every `mcp-add` / `mcp-remove`
- PAT registered under `mjm-dex` GitHub account — swap if needed
