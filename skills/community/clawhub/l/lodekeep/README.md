# Lodekeep — Setup Guide

One durable memory that every AI on your box reads and writes. Built for OpenClaw
agents running on VPS boxes where session death and compaction eat decisions.

## What this does

Your agent survives three memory killers:

1. **Compaction** — long-session context gets compressed; decisions made there vanish.
2. **Session death** — a cron-launched fresh session inherits nothing.
3. **Tool switches** — Claude Code → Gemini CLI → another agent each keep separate
   histories, and hand-summarizing between them drifts fast.

Lodekeep is an MCP memory layer all your tools share. Notes carry provenance (what was
decided, why, verified against what), so stale memory says so instead of lying.

## Before you install

- [ ] OpenClaw gateway (or any MCP client) running
- [ ] Lodekeep account: https://lodekeep.com (free tier works)
- [ ] API key from dashboard → Settings

## Install

1. Copy `SKILL.md` into your agent's skills directory:

```bash
mkdir -p ~/.openclaw/skills/lodekeep
cp SKILL.md ~/.openclaw/skills/lodekeep/SKILL.md
```

2. Add the MCP server to your gateway config (`~/.openclaw/openclaw.json`) —
   it's a remote server, no npm install needed:

```json
{
  "mcpServers": {
    "lodekeep": {
      "url": "https://lodekeep.com/mcp",
      "headers": { "Authorization": "Bearer your-key-here" }
    }
  }
}
```

3. Restart the gateway.

## Verify it works

Ask your agent:

> "check lodekeep server_info"

Authenticated response with your project list = working. Then ask it to capture a test
note and recall it by meaning ("what did we capture about the test note?").

## API key discovery

The skill checks, in order:

1. Env: `LODEKEEP_API_KEY` or `MCP_LODEKEEP_API_KEY`
2. Config: `~/.config/lodekeep/credentials.json`
3. Your gateway's env block

If none are found it asks you — it never guesses.

## Known limitations

- Semantic recall, not exhaustive search — curate projects rather than dumping everything.
- Never store live secrets; store where the credential lives, not its value.
- Project-scoped recall needs the project marked "included" in your dashboard.

## Support

hello@lodekeep.com — or on Moltbook (@stevethesentinel).