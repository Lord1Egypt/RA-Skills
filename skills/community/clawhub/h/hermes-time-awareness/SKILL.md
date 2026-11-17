---
name: hermes-time-awareness
description: "Inject current time and idle detection into every LLM turn."
version: 1.0.0
author: mfang0126
license: MIT
metadata:
  hermes:
    tags: [hermes, time, awareness, hook, plugin, idle-detection]
  platforms: [macos, linux, windows]
---

# hermes-time-awareness

Time awareness for [Hermes Agent](https://github.com/NousResearch/hermes-agent). Injects current time and idle detection into every LLM turn via `pre_llm_call` hook.

## When to Use

- Agent needs to know what time it is (scheduling, reminders, time-sensitive tasks)
- Detect user idle/away time for context-aware responses
- Zero core changes, prompt-cache safe, ~30 tokens per turn

## What It Does

Every turn, the model sees:

```
[time: 2026-08-29 18:00 AEST +10:00 Sat]
[idle: 2h15m]
```

## Quick Start

```bash
git clone https://github.com/mfang0126/hermes-time-awareness.git
cp -r hermes-time-awareness ~/.hermes/plugins/
# Restart Hermes — hook auto-activates
```

## How It Works

Uses Hermes `pre_llm_call` hook mechanism:
1. Reads current system time + timezone
2. Calculates idle duration since last user message
3. Appends compact time block to user message
4. ~30 tokens overhead per turn

## Requirements

- Hermes Agent (any recent version)
- Python 3.8+
