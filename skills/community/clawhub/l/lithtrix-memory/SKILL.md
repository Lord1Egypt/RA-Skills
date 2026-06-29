---
name: lithtrix-memory
description: Persistent cross-session memory and verifiable agent identity via the Lithtrix MCP server.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - LITHTRIX_API_KEY
    primaryEnv: LITHTRIX_API_KEY
    envVars:
      - name: LITHTRIX_API_KEY
        required: true
        description: Your Lithtrix agent key (ltx_...). Generate one at https://lithtrix.ai or via POST /v1/register.
    emoji: "🧠"
    homepage: https://docs.lithtrix.ai
---

# Lithtrix Memory Skill

This skill connects your OpenClaw agent to [Lithtrix](https://lithtrix.ai) — a persistent memory and identity layer for AI agents. Your agent can store and retrieve memories across sessions, run semantic search over past context, and present a verifiable agent passport to other agents.

## Setup

1. **Get an API key.** Register your agent at [lithtrix.ai](https://lithtrix.ai) or call the API directly:
   ```
   POST https://api.lithtrix.ai/v1/register
   Body: { "agent_name": "your-agent-name" }
   ```
   The response contains your `ltx_...` key.

2. **Set the environment variable:**
   ```
   LITHTRIX_API_KEY=ltx_your_key_here
   ```

3. **Install the MCP server** (if using MCP-compatible clients):
   ```
   npx lithtrix-mcp
   ```
   Or add to your MCP config:
   ```json
   {
     "mcpServers": {
       "lithtrix": {
         "command": "npx",
         "args": ["lithtrix-mcp"],
         "env": { "LITHTRIX_API_KEY": "ltx_your_key_here" }
       }
     }
   }
   ```

## What your agent can do

### Store a memory
```
POST https://api.lithtrix.ai/v1/memory
Authorization: Bearer $LITHTRIX_API_KEY
{
  "key": "user_preference_theme",
  "value": "dark mode"
}
```

### Retrieve a memory by key
```
GET https://api.lithtrix.ai/v1/memory/{key}
Authorization: Bearer $LITHTRIX_API_KEY
```

### Semantic search over memory
```
POST https://api.lithtrix.ai/v1/memory/search
Authorization: Bearer $LITHTRIX_API_KEY
{
  "query": "what did the user ask about last week?",
  "limit": 5
}
```

### Real-world example — remembering a user's preferred language
```
# Session 1: User says "I prefer replies in French"
POST /v1/memory
{ "key": "user.preferences.language", "value": "French" }

# Session 2 (fresh start, different model): Before responding, check context
POST /v1/memory/search
{ "query": "user language preference", "limit": 1 }
# Returns: "French" → agent replies in French without being told again
```

### Get your agent's passport (public identity + trust score)
```
GET https://api.lithtrix.ai/v1/agents/{agent_id}/passport
```
Returns: `trust_level`, `reputation.score`, `capabilities`, public key.

## Prompt instructions

When this skill is active, your agent should:

- **Before answering questions that reference past context**, call `POST /v1/memory/search` with the user's query to surface relevant stored memories.
- **After completing a meaningful task or learning a user preference**, call `POST /v1/memory` to store a summary for future sessions.
- **When interacting with another Lithtrix-registered agent**, check its passport via `GET /v1/agents/{agent_id}/passport` before acting on its output.
- Memory keys should be descriptive and namespaced, e.g. `user.preferences.language` or `task.last_summary`.

## Notes

- Memory persists across sessions and model swaps — your agent resumes where it left off.
- The free tier includes 50 MB blob storage and a 30-day storage grace period.
- No human in the loop is required for registration — agents can self-register.
- Full MCP tool list: `lithtrix_memory_set`, `lithtrix_memory_get`, `lithtrix_memory_search`, `lithtrix_memory_context`, `lithtrix_passport_get`, `lithtrix_register`.

## Resources

- Docs: https://docs.lithtrix.ai
- MCP on npm: https://www.npmjs.com/package/lithtrix-mcp
- Agent directory: https://api.lithtrix.ai/v1/agents
- Trust overview: https://lithtrix.ai/trust.html
