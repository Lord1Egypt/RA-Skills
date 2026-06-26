---
name: kinthai-self-improving-user
description: "User-level self-improvement: injects prior learnings and ensures per-user directories"
metadata:
  openclaw:
    emoji: "🧠"
    events: ["agent:bootstrap", "message:received", "agent_end"]
    requires:
      bins: ["node"]
---

# kinthai-Self-Improving-User Hook

## Events

| Event | Action |
|-------|--------|
| `agent:bootstrap` | Reads `_global/` and `{user_id}/` learnings, injects into AGENTS.md bootstrap content |
| `message:received` | Ensures user directory `.learnings/{user_id}/` exists |
| `agent_end` | Reserved for future auto-extraction |

## How It Works

1. On `agent:bootstrap`: extracts `user_id` from session key, reads accumulated learnings, and pushes a `SELF_IMPROVING_USER.md` virtual file into `bootstrapFiles`
2. On `message:received`: creates the user's learnings directory if it doesn't exist yet
3. The agent follows SKILL.md instructions to write learnings after corrections/errors

## Installation

Place this hook in one of:
- `~/.openclaw/hooks/kinthai-self-improving-user/` (managed hooks, recommended)
- `<workspace>/hooks/kinthai-self-improving-user/` (workspace hooks)

Then enable:
```bash
openclaw hooks enable kinthai-self-improving-user
```

Or configure in `openclaw.json`:
```json
{
  "hooks": {
    "internal": {
      "entries": {
        "kinthai-self-improving-user": {
          "enabled": true
        }
      }
    }
  }
}
```
