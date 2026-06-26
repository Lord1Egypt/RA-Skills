---
name: news-digest
description: "Injects time-aware push schedule reminder during agent bootstrap. Checks current hour to determine active slot (morning/noon/evening) and reminds the agent to execute the push workflow."
metadata: {"openclaw":{"emoji":"📰","events":["agent:bootstrap"]}}
---

# News Digest Hook

Injects a push schedule reminder during agent bootstrap based on the current time.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Checks the current hour against the push schedule:
  - 07:00-09:00 → Reminds to execute **金融早报** (morning, finance/crypto)
  - 11:00-13:00 → Reminds to execute **AI午报** (noon, AI/Agent)
  - 17:00-19:00 → Reminds to execute **晚间热点** (evening, general tech)
- Outside push windows, shows next scheduled push and available query commands
- Skips sub-agent sessions to avoid redundant reminders

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable news-digest
```
