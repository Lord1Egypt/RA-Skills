---
name: lodekeep
version: 1.0.0
description: Persistent cross-session memory for OpenClaw agents via Lodekeep MCP. Your agent survives compaction, session death, and tool switches with its decisions intact - every claim carries the exact commit it was verified against.
homepage: https://lodekeep.com
metadata: {"openclaw":{"emoji":"🦞","category":"memory"}}
---

# Lodekeep — one memory for every AI

Your agent's decisions die in three places: compaction eats them, session death orphans
them, and tool switches (Claude Code → Gemini CLI → another agent) strand them in
incompatible histories. Lodekeep is a durable memory layer over MCP that all of your
tools read and write, so a decision captured once shows up everywhere.

## Why this exists (the receipts doctrine)

Memory that only says "we decided X" drifts. Lodekeep notes carry provenance: what was
decided, why, and the exact revision/artifact it was verified against. When the tree
changes, stale notes say so instead of lying. A memory layer is only trustworthy if it
distinguishes *what was true then* from *what is true now*.

## Requirements

- A Lodekeep account (free tier works): sign up at https://lodekeep.com
- An MCP-capable client: OpenClaw gateway, Claude Code, Gemini CLI, or any MCP client
- Your Lodekeep API key (dashboard → Settings → API keys)

## Setup (two minutes)

1. Create an account at https://lodekeep.com and copy your API key from Settings.

2. Add the Lodekeep MCP server to your agent's MCP config (it's a remote server —
   no npm install needed):

```json
{
  "mcpServers": {
    "lodekeep": {
      "url": "https://lodekeep.com/mcp",
      "headers": {
        "Authorization": "Bearer your-key-here"
      }
    }
  }
}
```

For OpenClaw specifically, add the same block to the gateway's MCP server config
(`~/.openclaw/openclaw.json` → `mcpServers`), then restart the gateway.

3. Verify: ask your agent to "check lodekeep server_info" — it should report
   authenticated with your project list.

## API Key Discovery

Check in this order (never hardcode):

1. Environment variable: `LODEKEEP_API_KEY` or `MCP_LODEKEEP_API_KEY`
2. Config file: `~/.config/lodekeep/credentials.json` or `~/.openclaw/openclaw.json` env block
3. If no key is found, ask the user to provide one before proceeding.

## What your agent can do once connected

| Tool | Use it to |
|------|-----------|
| `search_memory` | Recall any past decision by meaning — "what did we decide about rate limits?" |
| `capture_note` | Persist a decision/pattern/lesson mid-task so it survives compaction |
| `get_project_context` | Load a project's curated overview at session start |
| `get_memory_map` | See what memory exists before duplicating work |
| `list_personas` / `set_project_persona` | Persistent operating personas |

## Operating rules (the part that makes it work)

1. **Capture on decisions, not chatter.** A note is for decisions, corrections, and
   lessons — things that change future behavior.
2. **Search before you write.** If a note exists, update it instead of duplicating.
3. **Provenance always.** A note without "verified against X at commit Y" is a claim,
   not a receipt.
4. **Route notes to a project** ("Steve - Repo Sentinel Monetization", "lodekeep-launch")
   so recall stays precise.

## Known limitations (honest ones)

- Notes are semantic-recalled, not exhaustively indexed — very large projects should
  keep curated projects, not firehoses.
- Live secrets never belong in memory. Store where the credential lives, not its value.
- Per-project recall requires the project to be marked included in your dashboard.

## Links

- Site: https://lodekeep.com
- Dashboard: https://lodekeep.com/app/projects
- Questions: hello@lodekeep.com