---
name: layered-memory
description: "Auto-save conversation memory when reaching thresholds"
metadata: {"openclaw":{"emoji":"🧠","events":["agent:bootstrap"]}}
---

# Layered Memory Hook

Automatically monitors and saves conversation memory based on token usage and message count.

## What It Does

- Fires on `agent:bootstrap` to inject memory monitoring reminder
- Reminds agent to check memory thresholds periodically
- Provides commands for manual memory operations

## Trigger Conditions

The agent should check and save memory when:
- Token usage ≥ 75% (150k/200k)
- Message count ≥ 20 messages
- Time elapsed > 1 hour with 5+ messages

## Configuration

Enable with:

```bash
openclaw hooks enable layered-memory
```

## Manual Commands

```bash
# Save memory manually
node ~/clawd/skills/layered-memory/index.js extract --save

# Check current stats
node ~/clawd/skills/layered-memory/index.js stats

# Search memory
node ~/clawd/skills/layered-memory/index.js search "keyword" l1
```
