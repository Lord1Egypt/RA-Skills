# TOOLS.md

> Tool configurations, gotchas, and local notes.

---

## What Goes Here

Environment-specific details that skills need:

- API keys (or where they're stored)
- Service endpoints
- Local paths and directories
- Preferred tools/alternatives
- Known issues and workarounds

---

## Current Setup

### Credentials

Stored in: `~/.openclaw/.env`

- TAVILYAPIKEY: Tavily Search API
- [Add more as needed]

### Preferred Tools

- **Web Search:** Tavily (fallback: Brave Search)
- **Browser:** Chrome via OpenClaw browser control
- **Shell:** PowerShell (Windows)

### Local Paths

- Workspace: `~/.openclaw/workspace`
- Skills: `~/.openclaw/workspace/skills`
- Memory: `~/.openclaw/workspace/memory`

---

## Known Issues & Workarounds

### [Issue Name]

**Problem:** [Description]
**Workaround:** [Solution]
**Status:** [Open/Resolved]

---

## Tool-Specific Notes

### Tavily Search

- Free tier: 1000 searches/month
- Rate limit: [X] requests/minute
- Format: `python skills/tavily-search/tavily_search.py "<query>" --num=5`

---

*Add your own notes as you configure tools.*
