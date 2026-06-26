---
name: mcp-server-setup-kit
version: 1.0.0
price: 19
bundle: ai-setup-productivity-pack
bundle_price: 79
last_validated: 2026-03-07
---

# MCP Server Setup Kit

**Framework: The 5-Minute Connect Protocol**
*Worth $200/hr consultant time. Yours for $19.*

---

## What This Skill Does

Guides you through connecting Claude to Notion, Linear, Slack, and GitHub using the Model Context Protocol (MCP) — in one focused workflow. No trial-and-error. No missing steps. Just a working integration you can test in under 5 minutes per tool.

**Problem it solves:** MCP setup friction is the #1 reason teams abandon agent workflows in 2026. The docs exist but the path is scattered. This skill gives you the straight line.

---

## The 5-Minute Connect Protocol

A structured checklist that takes any MCP server from "never heard of it" to "Claude is using it" in 5 minutes or less.

### Phase 1 — Qualify (30 seconds)

Answer these before touching any config:

| Question | Yes → Continue | No → Fix First |
|----------|----------------|----------------|
| Do you have a Claude Desktop or OpenClaw installation? | ✅ | Install first |
| Do you have an API key / OAuth token for the target tool? | ✅ | Generate it now |
| Do you know where your `claude_desktop_config.json` lives? | ✅ | Find it (see below) |
| Is Node.js 18+ or Python 3.10+ installed? | ✅ | Install via homebrew/nvm |

**Config file locations:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- OpenClaw: `~/.openclaw/openclaw.json` (mcpServers block)

---

### Phase 2 — Install (2 minutes)

**Universal install pattern:**

```bash
# For NPX-based MCP servers (most common)
npx -y @modelcontextprotocol/server-{toolname}

# For Python-based MCP servers
pip install mcp-server-{toolname}
uvx mcp-server-{toolname}
```

**Verify the binary works before touching config:**
```bash
npx -y @modelcontextprotocol/server-github --help
# Should print usage/options — if it errors, fix here before config
```

---

### Phase 3 — Configure (1 minute)

Add the server block to your config. Universal template:

```json
{
  "mcpServers": {
    "{tool-name}": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-{tool-name}"],
      "env": {
        "{TOOL}_API_KEY": "your-key-here"
      }
    }
  }
}
```

---

### Phase 4 — Test (90 seconds)

Use these verification prompts immediately after restart:

```
"List my available MCP tools"
"What can you do with [tool-name]?"
"[Tool-specific test prompt from templates below]"
```

**If Claude doesn't see the tool:** restart Claude Desktop / OpenClaw gateway completely (not just refresh).

---

### Phase 5 — Validate (30 seconds)

✅ Claude lists the tool when asked
✅ Tool-specific test prompt returns real data
✅ Write operation (if applicable) succeeds
✅ No auth errors in logs

**Log check:** `~/Library/Logs/Claude/mcp*.log` (macOS)

---

## 5 Pre-Built Integration Templates

### Template 1: GitHub MCP

**Use case:** Let Claude read repos, issues, PRs, and push code.

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

**Token scopes needed:** `repo`, `read:user`, `read:org`
**Generate at:** github.com → Settings → Developer Settings → Personal Access Tokens

**5-Minute Connect test prompts:**
1. `"List my open GitHub issues across all repos"`
2. `"What PRs are waiting for my review?"`
3. `"Show me the README for [your-repo]"`

---

### Template 2: Notion MCP

**Use case:** Let Claude read/write Notion pages and databases.

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notion"],
      "env": {
        "NOTION_API_TOKEN": "secret_your_token_here"
      }
    }
  }
}
```

**Token setup:** notion.com → Settings → Connections → Develop integrations → New integration
**Critical step:** Share target pages with your integration (Notion doesn't auto-grant access)

**5-Minute Connect test prompts:**
1. `"List my Notion pages"`
2. `"Search Notion for [topic]"`
3. `"Create a new page titled 'MCP Test' in [workspace]"`

---

### Template 3: Slack MCP

**Use case:** Let Claude read channels, send messages, search history.

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-token",
        "SLACK_TEAM_ID": "T0XXXXXXX"
      }
    }
  }
}
```

**Token setup:** api.slack.com → Create App → OAuth & Permissions
**Scopes needed:** `channels:read`, `chat:write`, `channels:history`, `users:read`

**5-Minute Connect test prompts:**
1. `"List my Slack channels"`
2. `"What was discussed in #general today?"`
3. `"Send 'MCP connected!' to #general"`

---

### Template 4: Linear MCP

**Use case:** Let Claude read/create/update Linear issues and projects.

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-linear"],
      "env": {
        "LINEAR_API_KEY": "lin_api_your_key_here"
      }
    }
  }
}
```

**Key setup:** linear.app → Settings → API → Personal API Keys

**5-Minute Connect test prompts:**
1. `"What issues are assigned to me in Linear?"`
2. `"Show my current sprint"`
3. `"Create a new Linear issue: 'Test MCP connection' in [Team]"`

---

### Template 5: Multi-Tool Stack (All 4 at Once)

For teams who want the full setup in one shot:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..." }
    },
    "notion": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notion"],
      "env": { "NOTION_API_TOKEN": "secret_..." }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-...",
        "SLACK_TEAM_ID": "T0..."
      }
    },
    "linear": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-linear"],
      "env": { "LINEAR_API_KEY": "lin_api_..." }
    }
  }
}
```

**Cross-tool test prompt:**
`"Using my connected tools: summarize my open Linear issues, find related Notion docs, check GitHub for open PRs, and post a summary to #standup in Slack"`

---

## Troubleshooting Decision Tree

```
Claude doesn't see my MCP tool
├── Did you restart Claude completely? (not just refresh)
│   └── No → Restart fully → Try again
├── Is the config JSON valid?
│   └── Check: jsonlint.com → paste your config
├── Does the server binary work standalone?
│   └── Run: npx -y @modelcontextprotocol/server-{name} --help
│       ├── Error → npm/node version issue → upgrade node
│       └── Works → config path or key issue
├── Auth error in logs?
│   └── Yes → Regenerate API key → check scopes
└── Tool shows but returns empty data?
    └── Notion: did you share pages with integration?
    └── Slack: check bot scopes
    └── GitHub: check token permissions
```

---

## Scoring Rubric: Are You Connected?

Score your setup after completing Phase 5:

| Check | Points |
|-------|--------|
| Tool appears in Claude's tool list | 20 |
| Read test prompt returns real data | 30 |
| Write test prompt succeeds | 30 |
| No errors in MCP logs | 10 |
| Cross-tool prompt works (multi-stack) | 10 |

**80-100:** Fully connected. Ship it.
**60-79:** Partial connection. Check scopes and restart.
**Below 60:** Go back to Phase 2. Something in install/config is broken.

---

## Example Session

**User prompt:**
> "Use this skill to connect me to GitHub"

**Agent response:**
1. Runs Phase 1 checklist aloud (asks for token if missing)
2. Provides Template 1 config block (pre-filled with user's token)
3. Instructs restart
4. Runs test prompts and confirms output
5. Scores the setup using the rubric
6. Suggests next integration (Notion → Slack → Linear)

---

## Bundle Note

This skill is part of the **AI Setup & Productivity Pack** ($79 bundle):
- MCP Server Setup Kit ($19) — *you are here*
- Agentic Loop Designer ($29)
- AI OS Blueprint ($39)
- Context Budget Optimizer ($19)
- Non-Technical Agent Quickstart ($9)

Save $36 with the full bundle. Built by [@Remy_Claw](https://remyclaw.com).
