---
name: memoryai
description: Long-term memory for AI agents. Your AI remembers everything — preferences, decisions, context — across sessions, forever.
version: 2.4.0
metadata: {"openclaw": {"emoji": "🧠", "requires": {"bins": ["python3"], "env": ["HM_API_KEY"]}, "primaryEnv": "HM_API_KEY"}}
---

# MemoryAI — Your AI Never Forgets 🧠

> **Session ends. Memory stays.**

MemoryAI gives your AI persistent long-term memory. It remembers what you said, what you decided, what you prefer — not for hours, but **forever**.

### How it works:

> **Day 1:** "I prefer dark mode, use TypeScript, deploy via GitHub Actions"
>
> **3 months later:** Your AI already knows. Zero repetition. It just *remembers*.

## Setup

1. Get API key from https://memoryai.dev
2. Edit `{baseDir}/config.json`:
```json
{
  "endpoint": "https://memoryai.dev",
  "api_key": "hm_sk_your_key_here"
}
```

3. Test: `python {baseDir}/scripts/memory.py health`

## Commands

### Remember something
```bash
python {baseDir}/scripts/memory.py store "User prefers dark mode" --type preference
```

Types: `fact`, `decision`, `preference`, `identity`, `goal`, `procedure`, `life_event`

### Recall memories
```bash
python {baseDir}/scripts/memory.py recall "what does user prefer"
```

### Wake up (start of session)
```bash
python {baseDir}/scripts/memory.py bootstrap "working on payment feature"
```
Returns identity + mood + context in ~800 tokens. Ready to work immediately.

### Track a message (keeps context healthy)
```bash
python {baseDir}/scripts/memory.py track "message content" --role user
```
Call on every user/assistant message. The brain keeps your context healthy automatically and lets you know when it's time to save and start fresh. See "Context Guard" below.

### Check brain health
```bash
python {baseDir}/scripts/memory.py health
```

### Save session context
```bash
python {baseDir}/scripts/memory.py save "summary of what happened this session"
```

### Who is this user?
```bash
python {baseDir}/scripts/memory.py profile
```
Returns cognitive profile: persona, mood, goals, entities, procedures.

## When to Use

| Trigger | Command |
|---------|---------|
| Start of session | `bootstrap` |
| Every user message | `track` (keeps context healthy automatically) |
| User says "remember this" | `store` with appropriate type |
| Need past context | `recall` |
| Decision made | `store --type decision` |
| Task completed | `store --type fact` |
| End of session | `save` with session summary |
| User seems different | `profile` to check mood/state |

## Context Guard (Auto)

MemoryAI protects your context window and keeps memory continuous across a long conversation. You don't manage any of this — the brain handles it.

### How to use it:

1. **Session start:** call `bootstrap` once to wake up with full context (~800 tokens).
2. **Every message:** call `track`. The brain keeps context healthy on its own.
3. **When `track` says to save:** call `save` with a short summary. The brain persists everything and gives you a clean slate to continue.

That's the whole loop: `bootstrap` → `track` each message → `save` when prompted. No cron jobs, no manual tuning.

> **Note:** Older versions used a periodic background command. That approach is retired — just use the per-message flow above. If you set up a recurring `sync` job before, remove it; it's no longer needed.

## Rules

- **Bootstrap at session start** — always. One call, full context.
- **Recall before guessing** — if you need past context, recall first.
- **Store important things** — decisions, preferences, outcomes. Not every message.
- **Present naturally** — integrate memories into responses, don't show raw output.
- **Trust the brain** — MemoryAI handles decay, consolidation, protection automatically.

## Memory Types

| Type | What | Lifespan |
|------|------|----------|
| `preference` | User likes/dislikes | Forever (DNA) |
| `decision` | Choices made | Forever (DNA) |
| `identity` | Who the user is | Forever (DNA) |
| `procedure` | How to do things | Forever (DNA) |
| `fact` | General knowledge | Decays if unused |
| `goal` | Active objectives | Until completed |
| `life_event` | Major transitions | Forever (DNA) |

DNA memories never decay. They're the core of who the user is.

## Data & Privacy

- All data sent over HTTPS to configured endpoint only
- No automatic transmission — all calls require explicit invocation
- Zero dependencies — pure Python stdlib
- Source fully readable and auditable
