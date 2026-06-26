---
name: memory-dreaming
description: "Reminds agent about dreaming capabilities during bootstrap"
metadata: {"openclaw":{"emoji":"💤","events":["agent:bootstrap"]}}
---

# Memory Dreaming Hook

Optional bootstrap hook that reminds the agent about the dreaming skill.

## What It Does

- Fires on `agent:bootstrap`
- Adds a brief reminder about manual dream triggers and the dreaming log

## Enable

```bash
openclaw hooks enable memory-dreaming
```
