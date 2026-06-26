---
name: hippocortex
description: Give your OpenClaw agent persistent long-term memory powered by Hippocortex. Automatically remembers conversations, facts, preferences, and procedures across sessions. Use when you want your agent to remember things between sessions, recall past conversations, or build up knowledge over time. Triggers on: memory, remember, recall, hippocortex, persistent memory, long-term memory.
---

# Hippocortex -- Persistent Memory for OpenClaw

## Setup

### 1. Get an API key

Sign up at https://dashboard.hippocortex.dev and create an API key.

### 2. Configure credentials

Set environment variables (preferred):

```bash
export HIPPOCORTEX_API_KEY="hx_live_..."
# Optional -- defaults to https://api.hippocortex.dev
export HIPPOCORTEX_BASE_URL="https://api.hippocortex.dev"
```

Or create `.hippocortex.json` in your workspace root:

```json
{
  "apiKey": "hx_live_...",
  "baseUrl": "https://api.hippocortex.dev",
  "sessionId": "my-agent"
}
```

### 3. Resolve configuration

On every invocation, resolve config in this order:
1. Environment variables (`HIPPOCORTEX_API_KEY`, `HIPPOCORTEX_BASE_URL`)
2. `.hippocortex.json` in workspace root
3. Fail gracefully if neither exists -- warn once, then proceed without memory

Set `BASE_URL` to `$HIPPOCORTEX_BASE_URL` or fall back to `https://api.hippocortex.dev`.
Set `SESSION_ID` from `.hippocortex.json` field `sessionId`, or default to `"openclaw"`.

For self-hosted setup details, see [references/setup-guide.md](references/setup-guide.md).

---

## Automatic Memory Flow (MANDATORY)

Follow this flow on every interaction. All API calls use:

```
Authorization: Bearer $HIPPOCORTEX_API_KEY
Content-Type: application/json
```

### Before answering ANY user message: Synthesize

Query memory for relevant context before composing your response.

```bash
curl -s -X POST "$BASE_URL/v1/synthesize" \
  -H "Authorization: Bearer $HIPPOCORTEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "'"$SESSION_ID"'",
    "query": "<rephrase the user message as a memory query>",
    "maxTokens": 2000
  }'
```

Response contains a `memories` array. Incorporate relevant memories into your answer naturally. Do not dump raw memory output to the user.

**If synthesize fails:** Still answer the user. Memory is additive, not blocking. Log the error silently and continue.

### After important exchanges: Capture

Store the conversation when it contains memorable content.

```bash
curl -s -X POST "$BASE_URL/v1/capture" \
  -H "Authorization: Bearer $HIPPOCORTEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "'"$SESSION_ID"'",
    "type": "conversation",
    "payload": {
      "messages": [
        {"role": "user", "content": "<user message>"},
        {"role": "assistant", "content": "<your response>"}
      ]
    },
    "metadata": {
      "extractedMemories": [
        "User prefers dark mode",
        "Project X uses PostgreSQL 16"
      ]
    }
  }'
```

The `extractedMemories` array is critical -- it stores discrete semantic facts directly. Extract 1-5 concise facts from the exchange.

**If capture fails:** Still respond to the user. Log the error and retry on next opportunity.

### During heartbeats: Compile

Run compile once per hour to consolidate memory patterns.

```bash
curl -s -X POST "$BASE_URL/v1/compile" \
  -H "Authorization: Bearer $HIPPOCORTEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "'"$SESSION_ID"'"
  }'
```

Track the last compile timestamp. Skip if less than 60 minutes have passed.

**If compile fails:** Not urgent. Retry on next heartbeat.

---

## API Reference

All endpoints require `Authorization: Bearer $HIPPOCORTEX_API_KEY`.

### POST /v1/synthesize

Query stored memories.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| sessionId | string | yes | Agent session identifier |
| query | string | yes | Natural language query |
| maxTokens | number | no | Max tokens in response (default: 2000) |

Returns: `{ "memories": [...] }`

### POST /v1/capture

Store a conversation or fact.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| sessionId | string | yes | Agent session identifier |
| type | string | yes | `"conversation"` or `"fact"` |
| payload | object | yes | Message array or fact content |
| metadata.extractedMemories | string[] | no | Discrete facts to store directly |

Returns: `{ "id": "...", "status": "captured" }`

### POST /v1/compile

Consolidate and optimize stored memories.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| sessionId | string | yes | Agent session identifier |

Returns: `{ "status": "compiled", "stats": {...} }`

---

## When to Capture

Capture after exchanges that contain:
- User preferences, corrections, or personal facts
- Important decisions or conclusions
- Explicit requests ("remember this", "keep track of...")
- New information about people, projects, or processes
- Procedures or workflows the user explains

## When NOT to Capture

Skip capture for:
- Casual greetings or small talk
- Simple yes/no confirmations
- Pure command execution (just running a script)
- Repeated information already in memory

---

## Error Handling Summary

| Endpoint | On failure | Action |
|----------|-----------|--------|
| synthesize | Answer without memory context | Log error, continue |
| capture | Respond normally | Log error, retry later |
| compile | Skip this cycle | Retry next heartbeat |

Never block a user response because a memory API call failed. Memory enhances responses but is never required for them.

---

## Extracting Good Memories

When writing `extractedMemories`, follow these guidelines:

- Keep each fact to one sentence
- Be specific: "User's dog is named Max" not "User has a dog"
- Include context: "User prefers Python for data scripts" not "User likes Python"
- Capture corrections: "User's name is spelled Vince, not Vincent"
- Store preferences: "User wants responses in German for work emails"
- Record project facts: "Project Aurora uses Next.js 15 with Supabase"
