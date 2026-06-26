# intel-asrai-skill

Skill for [Intel](https://intel.asrai.me) — AI-powered web search via x402 micropayments on Base.

Works with **OpenClaw**, **Claude Desktop**, **Cursor**, **Cline**, and any MCP-compatible or bash-capable agent.

## Install

### One command — works everywhere

```bash
npx -y -p intel-asrai-mcp install-skill
```

Auto-detects OpenClaw, Cursor, Cline, and other agents. Copies SKILL.md to the right place. Then restart your agent or run "refresh skills".

### Manual — OpenClaw (if auto-detect fails)

```bash
git clone https://github.com/abuzerasr/intel-asrai-skill.git ~/.openclaw/workspace/skills/intel-asrai
```

### Manual — Cursor / Cline / other agents

```bash
npx skills add https://github.com/abuzerasr/intel-asrai-skill -y
```

---

## Setup by platform

### OpenClaw (bash mode — no MCP needed)

1. Set your key in `~/.env`:
```
INTEL_PRIVATE_KEY=0x<your_private_key>
```

2. That's it. The skill uses `npx` automatically — no extra install needed.

The agent runs:
```bash
npx -y -p intel-asrai-mcp intel-search "query"
```

Node.js is required (already installed with OpenClaw).

---

### Claude Desktop (MCP mode)

Add to your Claude Desktop config file:

```json
{
  "mcpServers": {
    "intel-search": {
      "command": "npx",
      "args": ["-y", "intel-asrai-mcp"],
      "env": { "INTEL_PRIVATE_KEY": "0x<your_private_key>" }
    }
  }
}
```

Config file location:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

---

### Cursor / Cline / other MCP clients

Add to your MCP config:

```json
{
  "mcpServers": {
    "intel-search": {
      "command": "npx",
      "args": ["-y", "intel-asrai-mcp"],
      "env": { "INTEL_PRIVATE_KEY": "0x<your_private_key>" }
    }
  }
}
```

---

### n8n / remote connections

- HTTP Streamable: `https://intel-mcp.asrai.me/mcp?key=0x<your_private_key>`
- SSE (legacy): `https://intel-mcp.asrai.me/sse?key=0x<your_private_key>`

---

## What this skill does

- Knows when to use Intel search vs its own knowledge
- Works via MCP tool (`intel_search`) when available
- Falls back to bash CLI (`intel-search`) on OpenClaw and other agents
- Handles all search modes: `speed`, `balanced`, `quality`
- Handles all source types: `web`, `academic`, `discussions`
- Cost-aware: $0.005 USDC per search

## MCP tool

| Tool | Description | Cost |
|---|---|---|
| `intel_search` | AI web search — synthesized answer with cited sources | $0.005 |

**Parameters:**
- `query` — the search question or topic
- `mode` — `speed` \| `balanced` \| `quality` (default: `balanced`)
- `sources` — `["web"]` \| `["academic"]` \| `["discussions"]` (default: `["web"]`)

## Links

- Landing page: [intel.asrai.me](https://intel.asrai.me)
- MCP package: [npmjs.com/package/intel-asrai-mcp](https://www.npmjs.com/package/intel-asrai-mcp)
- GitHub: [github.com/abuzerasr/intel-asrai-skill](https://github.com/abuzerasr/intel-asrai-skill)
- x402 protocol: [x402.org](https://x402.org)

## License

MIT
