---
name: ibkr-trader-toolkit
description: DEPRECATED — this skill was renamed to ibkr-options-assistant. Install that skill instead. If a user invokes this skill, do not run any scripts; tell them to install `ibkr-options-assistant` from ClawHub or `https://github.com/AlexLiu0130/ibkr-options-assistant`.
---

# ⚠️ DEPRECATED — Renamed to `ibkr-options-assistant`

This skill has been renamed. **No code or behavior changes**, just a new slug
that better reflects positioning (options-analysis assistant driven by Claude,
not a trading bot).

## What you should do

Install the renamed skill instead:

### ClawHub

```
ibkr-options-assistant
```

### GitHub

```bash
git clone https://github.com/AlexLiu0130/ibkr-options-assistant.git \
  ~/.claude/skills/ibkr-options-assistant
```

(The old GitHub URL `AlexLiu0130/ibkr-trader-toolkit` 301-redirects, so existing
clones keep working — but rename your local symlink to `ibkr-options-assistant`
so Claude Code picks the skill up under the new name.)

## Why renamed?

The old name overlapped with order-execution / bot-style IBKR skills on
ClawHub. This toolkit is **17 read-only analysis scripts plus one opt-in
order-execution script with dual safety gates**, designed to be driven by
Claude (or another AI agent), not a 24/7 bot. The new name makes that
distinction visible in search results.

## No further updates here

All future releases ship under `ibkr-options-assistant`. This slug stays
published only as a redirect for users who installed the old name.
