---
name: op-helper
description: Manage and maintain OpenClaw chat sessions. Use when the user wants to compact the current session context, start a fresh session, or reset their session. Handles /compact (compress context), /new (new session), and /reset (reset session). Always ask for user confirmation before running /compact or /new. Triggers on phrases like "session feels stale", "context is bloated", "compact session", "fresh slate", "new session", "reset session", "/compact", "/new", "/reset".
---

# op-helper

Maintain OpenClaw chat sessions by compacting or resetting them. **Always confirm with the user before running /compact or /new.**

## Commands

| Command | Purpose | When to use |
|---|---|---|
| `/compact` | Summarize + compress current context | Session feels stale, too long conversation, context bloated |
| `/new` | Start a brand-new session (new session ID) | Need a completely fresh slate |
| `/reset` | Reset current session state | Quick reset without a new ID |

## Workflow

### Detecting when to suggest session maintenance

Suggest session maintenance when:
- Conversation history is very long (many tool calls, repeated context)
- User mentions context feeling slow, stale, or confused
- User explicitly asks to compact, reset, or start fresh session

### Running /compact

1. **Always ask first**: "Your session context is getting large. Want me to run `/compact` to summarize and compress it?"
2. Wait for explicit confirmation (yes/sure/go ahead)
3. Run the command in the terminal:

```bash
openclaw session compact
```

Or use the slash command in chat if supported: `/compact`

### Running /new

1. **Always ask first**: "This will start a completely fresh session with a new session ID. Confirm?"
2. Wait for explicit confirmation
3. Run: `/new` or `openclaw session new`

### Running /reset

`/reset` is a lighter operation (no new session ID). Confirm is still recommended but less critical than `/new`.

## Key Rules

- **Never run /compact or /new without user confirmation** — these are disruptive actions
- `/compact` is preferred over `/new` when the user just wants to reduce context bloat
- `/new` is for when the user explicitly wants a clean slate or different context(switch to a new task)
- After compacting, let the user know what was summarized and that the session is lighter
