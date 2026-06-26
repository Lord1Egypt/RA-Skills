---
name: human-like-memory
description: "HumanLike Memory / Human-Like Memory is a persistent AI agent memory system for long-term memory search, recall, and save. It helps agents store facts, preferences, and decisions and keep context across sessions for conversation continuity."
homepage: https://plugin.human-like.me
license: Apache-2.0
user-invocable: true
metadata: {"openclaw":{"emoji":"🧠","homepage":"https://plugin.human-like.me","requires":{"bins":["node"],"config":["skills.entries.human-like-memory.apiKey"]},"primaryEnv":"HUMAN_LIKE_MEM_API_KEY"}}
---

# Human-Like Memory Skill

Persistent AI agent memory system for Human-Like Memory.

HumanLike Memory, Human-Like Memory, and human like memory all refer to the same skill. It helps agents search long-term memory, recall past context, save durable information, and store facts, preferences, and decisions across sessions.

## Search Aliases

- HumanLike Memory
- Human-Like Memory
- human like memory
- agent memory
- long-term memory
- memory recall
- memory search
- memory save
- conversation continuity

This skill supports both:

- Agent-triggered recall and save when the model judges memory is useful
- Explicit user invocation when the user directly asks to recall or store memory

This skill is intentionally **not always-on**:

- It should **not** recall on every turn by default
- It should **not** silently save every conversation turn by default
- It does **not** read `~/.openclaw/secrets.json` or per-skill `config.json`
- It reads configuration from OpenClaw config or injected environment variables only

If you want always-on automatic recall/storage, use the Human-Like Memory plugin instead of this skill.

## Data And Network Disclosure

When the agent or user invokes this skill:

- `recall` / `search` sends your query, `user_id`, and `agent_id` to `https://plugin.human-like.me` or your configured base URL
- `save` / `save-batch` sends the conversation content you explicitly pass to the same service
- No local files, shell history, or unrelated environment variables are read or uploaded
- The runtime reads only the documented allowlisted `HUMAN_LIKE_MEM_*` environment variables

## Use When

- You want to explicitly search past memory
- You want to explicitly save a user fact, decision, preference, or summary
- The agent needs past context to answer well
- The agent should save a durable preference, decision, correction, or summary

## Do Not Use When

- You want every-turn automatic recall or hook-level background saving
- You need hidden or silent network activity
- You want zero remote data transfer

## Setup

### 1. Get API Key

Visit [plugin.human-like.me](https://plugin.human-like.me) and copy your `mp_xxx` key.

### 2. Configure Through OpenClaw

```bash
openclaw config set skills.entries.human-like-memory.enabled true --strict-json
openclaw config set skills.entries.human-like-memory.apiKey "mp_your_key_here"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_BASE_URL "https://plugin.human-like.me"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_USER_ID "openclaw-user"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_AGENT_ID "main"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_RECALL_ENABLED "true"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_AUTO_SAVE_ENABLED "true"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_SAVE_TRIGGER_TURNS "5"
```

If the user explicitly gives the API key in the current environment, the agent may run these `openclaw config set` commands on the user's behalf. Otherwise, do not invent or request a secret implicitly.

### 3. Verify

```bash
node {baseDir}/scripts/memory.mjs config
```

Expected output includes:

```json
{
  "apiKeyConfigured": true
}
```

## Commands

### Recall Or Search Memory

```bash
node {baseDir}/scripts/memory.mjs recall "<query>"
node {baseDir}/scripts/memory.mjs search "<query>"
```

### Save One Turn

```bash
node {baseDir}/scripts/memory.mjs save "<user_message>" "<assistant_response>"
```

### Save A Batch

```bash
echo '[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]' | node {baseDir}/scripts/memory.mjs save-batch
```

### Inspect Runtime Configuration

```bash
node {baseDir}/scripts/memory.mjs config
```

## Agent Invocation Style

This skill may be called by the agent when memory is clearly useful.

Recommended behavior:

- Use `recall` / `search` when the user references prior work, prior preferences, prior decisions, or asks to continue something from earlier
- Use `save` when the user explicitly asks to remember something, corrects identity details, states a stable preference, or confirms an important decision
- Use `save-batch` after a meaningful multi-turn discussion if `HUMAN_LIKE_MEM_AUTO_SAVE_ENABLED=true` and the current conversation has accumulated roughly `HUMAN_LIKE_MEM_SAVE_TRIGGER_TURNS` turns
- Do not call memory APIs for simple greetings or generic single-turn questions with no continuity value

This gives the agent autonomy, but keeps the skill in a smart-trigger mode instead of an always-on mode.

For practical examples, memory taxonomy, and extended guidance, see [README.md](./README.md) and [SECURITY.md](./SECURITY.md).
