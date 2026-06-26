---
name: qordinate-structured-memory
description: |
  Qordinate is an AI-native platform that gives your OpenClaw agent durable structured memory — documents, contacts, tasks, reminders, web search, and connected apps. Connect via MCP using an API key.
compatibility: Requires MCP client support (Streamable HTTP transport)
metadata:
  author: qordinate
  version: "0.3"
  openclaw:
    requires:
      env:
        - QORDINATE_API_KEY
      bins:
        - curl
    primaryEnv: QORDINATE_API_KEY
---

# Qordinate - AI-Native Memory & Productivity for OpenClaw Agents

Qordinate is an AI agent platform that becomes **durable, structured memory and productivity infrastructure** for your users and agents.

Instead of your OpenClaw agent trying to keep all state in its own scratchpad or a custom DB, it can connect to Qordinate via **MCP (Model Context Protocol)** and use the Qordinate AI agent to:

- Store and retrieve **documents** (notes, files, PDFs)
- Manage **contacts** (people, companies, leads)
- Maintain **lists and tasks** with statuses, due dates, and reminders
- **Search the web** for up-to-date information
- Interact with **connected apps** the user has linked to Qordinate
- Create and manage **forms** and collect **submissions**
- Set up **automations** that run on schedules or triggers

The agent talks to Qordinate's AI agent through a single powerful tool — `query_agent` — using natural language.

---

## Connection Details

| Field | Value |
|-------|-------|
| **Protocol** | MCP (Model Context Protocol) — Streamable HTTP |
| **MCP Server URL** | `https://api.qordinate.ai/mcp` |
| **Auth Method** | Bearer token — `Authorization: Bearer qk_YOUR_API_KEY` |
| **API Key Format** | Prefixed with `qk_` |

---

## User Setup (what the agent should tell the user once)

Before the agent can connect, the user needs a Qordinate account and an API key:

1. **Sign up** at [https://app.qordinate.ai](https://app.qordinate.ai) using their phone number + OTP
2. Go to **Profile → API Keys → New API Key** to create an API key
3. Give the API key (starts with `qk_`) to the agent

The API key is shown only once at creation time. The user can set an expiry (1–365 days) or leave it non-expiring.

---

## MCP Tool: `query_agent`

Qordinate's MCP server exposes one tool — `query_agent` — which is a natural-language interface to the full Qordinate AI agent. The agent has access to the user's documents, contacts, lists, web search, and all connected apps.

### Input Schema

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | ✅ | Your question or request for the Qordinate agent |
| `session_id` | string | ❌ | Optional session ID for multi-turn conversations |

### How to use `session_id`

- Omit `session_id` for standalone queries
- To have a multi-turn conversation, capture the session ID from the first response and pass it in subsequent calls
- This lets the Qordinate agent maintain context across multiple queries

---

## What the agent can do through `query_agent`

The `query_agent` tool invokes the full Qordinate AI agent, which can do everything a user interacting directly with Qordinate can do:

### Structured Memory (Lists & Tasks)
- Create, update, and query **lists** (tasks, contacts, leads, projects, resources, etc.)
- Set **due dates**, **statuses**, and **reminders** on list items
- Qordinate manages reminders and notifications over time

### Documents
- Create, read, update, and delete documents
- Upload and retrieve files (PDFs, images, etc.)
- Share documents with other users

### Contacts
- Store and retrieve contact information
- Import contacts (including VCF format)
- Search contacts by name, company, role, etc.

### Web Search
- Search the web for current information
- The agent can ask Qordinate to research topics and return results

### Connected Apps
- Interact with third-party apps the user has connected to Qordinate
- Query data from connected services

### Forms & Automations
- Create forms and collect submissions
- Set up automations that trigger on schedules or events

---

## Example Interactions

Your OpenClaw agent sends these as the `query` parameter to `query_agent`:

### Managing tasks
```
Add a new task: Follow up with ACME about the reorder pilot, due next Tuesday 3pm, status todo, notes: important client meeting
```

### Storing contacts
```
Save a new contact: Harpinder Singh, Co-founder at qordinate.ai, building Qordinate
```

### Querying information
```
Show me all my open tasks due this week
```

### Searching the web
```
Search the web for the latest pricing of OpenAI GPT-4o API
```

### Working with documents
```
Create a new document titled "Meeting Notes - ACME Q1 Review" with the following content: ...
```

### Updating items
```
Mark the task "Follow up with ACME" as done
```

---

## How the agent should think about Qordinate

- **Treat Qordinate as the source of truth** for "what needs doing" and "who is who" across time
- **Offload anything the user will care about later** — don't keep it in ephemeral memory
- **Use natural language** — the query_agent tool understands plain English requests
- **Use session_id for related queries** — if you're doing a multi-step workflow (e.g., "list tasks" then "mark task X as done"), use the same session_id
- **Be specific** — include list names, field values, dates, and context in your queries

---

## User Channels (optional, for the user)

Users can also interact with Qordinate directly on their preferred messaging platform. This is independent of the agent's MCP connection:

- **WhatsApp**: connect via [https://qordinate.ai/whatsapp](https://qordinate.ai/whatsapp)
- **Telegram**: connect via [https://qordinate.ai/telegram](https://qordinate.ai/telegram)
- **Slack**: connect via [https://qordinate.ai/slack](https://qordinate.ai/slack)

Everything the user does on these channels is reflected in the same account the agent accesses via MCP — they share the same data.
