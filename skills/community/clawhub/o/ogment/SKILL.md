---
name: ogment
description: Invoke MCP tools via Ogment CLI — secure access to Linear, Notion, Gmail, PostHog, and 100+ SaaS integrations through Ogment's governance layer.
version: 1.0.3
metadata:
  openclaw:
    requires:
      bins:
        - ogment
      anyBins:
        - jq
    install:
      - kind: node
        package: "@ogment-ai/cli"
        bins: [ogment]
      - kind: brew
        formula: jq
        bins: [jq]
    emoji: "🔌"
    homepage: https://ogment.ai
---

# Ogment CLI Skill

Securely invoke MCP tools via the Ogment CLI. Access your connected SaaS tools (Linear, Notion, Gmail, Slack, Supabase, etc.) through Ogment's governance layer.

## Quick Start

### Step 1: Check Auth
```bash
ogment auth status
```
- If `loggedIn: true` → skip to Step 3
- If `loggedIn: false` → continue to Step 2

### Step 2: Login (if needed)
```bash
ogment auth login
```

Extract `verificationUri` from the response and **send it to your human as a clickable link:**

> **🔐 Approve Ogment access:**
> 👉 [Click to approve](https://dashboard.ogment.ai/cli/approve?authRequestId=...)

Wait for approval, then verify with `ogment auth status`.

### Step 3: Discover What's Available
```bash
ogment catalog
ogment catalog <serverId>
```

### Step 4: Summarize to Your Human
> **✅ Connected to Ogment!** Here's what I can access:
> - **Gmail:** 11 tools (messages, threads, drafts)
> - **Notion:** 5 tools (search, fetch, comments)
> - **Slack:** 7 tools (conversations, users)
>
> What would you like me to help with?

## Core Workflow

```
auth status → catalog → catalog <server> → invoke <server> <tool>
```

### Discover servers
```bash
ogment catalog
```

### List tools
```bash
ogment catalog <serverId>
```

### Inspect tool schema
```bash
ogment catalog <serverId> <toolName>
```

### Invoke a tool
```bash
ogment invoke <serverId> <toolName> --input '<json>'
```

## Common Patterns

### Gmail (requires `userId: "me"`)
```bash
ogment invoke <server> gmail_listMessages --input '{"userId": "me", "maxResults": 10}'
ogment invoke <server> gmail_getMessage --input '{"userId": "me", "messageId": "<id>"}'
```

### Notion
```bash
ogment invoke <server> Notion_notion-search --input '{"query": "quarterly review"}'
```

### Supabase
```bash
ogment invoke <server> Supabase_execute_sql --input '{"query": "SELECT * FROM users LIMIT 5"}'
```

### Linear
```bash
ogment invoke <server> Linear_list_issues --input '{}'
```
