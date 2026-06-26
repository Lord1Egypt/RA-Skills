---
name: ask-to-remember
description: "Injects ATR trigger reminder and Phase B resolution rules during agent bootstrap"
metadata: {"openclaw":{"emoji":"🎯","events":["agent:bootstrap"]}}
---

# Ask-to-Remember Bootstrap Hook

Injects ATR prompt into every main-session agent run as a virtual bootstrap file.

## What It Does

- Fires on `agent:bootstrap`
- Pushes `ASK_TO_REMEMBER.md` virtual file containing:
  - A brief skill entry point that references SKILL.md for full Phase A execution logic
  - Phase B pending-question resolution rules (complete, including disambiguation priority, ignored cooldown, and same-turn concurrency)
- ATR is main-session only (enforced by prompt, not code)

## Configuration

No configuration needed. Installed automatically with the ask-to-remember skill.
