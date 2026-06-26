---
name: smart-model-router
description: |
  Route every substantive user request to the optimal LLM model.
  Trigger on EVERY substantive request. Score across 12 dimensions, pick the
  best model, switch via session_status, then answer.

  Do NOT trigger for: greetings, acknowledgments ("ok", "好的"), heartbeats,
  or non-substantive messages (Chinese < 3 chars, English < 5 words).
metadata:
  {
    "openclaw": {
      "configPaths": ["~/.openclaw/openclaw.json"],
      "access": [
        {
          "path": "~/.openclaw/openclaw.json",
          "reason": "Reads available model list to filter unavailable models during routing"
        }
      ]
    }
  }
---

# Smart Model Router

## Every Substantive Request

1. **Score**: `python3 <skill_path>/scripts/router.py --task "<user message>"`
2. **Parse JSON** → get `full_id`, `tier`, `confidence`
3. **If `full_id` is `fallback/default`**: do NOT switch. Tell the user to run `--setup`.
4. **If `full_id` differs from current model**: `session_status(model=<full_id>)`
5. **Answer the user.** Do not volunteer routing details, but disclose when asked.

**Skip** for greetings, acknowledgments, heartbeats, or very short messages.

## First-Time Setup

```bash
python3 <skill_path>/scripts/router.py --setup
```

## Recommended: Reinforce in AGENTS.md

Add the following line to your agent's AGENTS.md for reliable auto-trigger:

```
Always follow smart-model-router SKILL.md instructions on every substantive request.
```

This is especially important when using less capable models that may otherwise
ignore skill instructions.

## CLI

```
--task TEXT    Route a task
--debug        Show scoring details
--setup        Generate models.json
```
