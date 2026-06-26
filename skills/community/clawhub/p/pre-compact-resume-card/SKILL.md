---
name: pre-compact-resume-card
description: Generates an operational resume card before Claude context compaction — so the next session knows exactly where it left off, what mode it was in, and what to do next. Install the PreCompact and SessionStart hooks to activate.
license: MIT
---

# Pre-Compact Resume Card

Claude forgets when context compacts. This skill installs a PreCompact hook that captures real operational state before compaction fires — branch, commit, last user intent, last assistant action, detected mode, and next step. The next session loads it automatically via SessionStart.

## What It Does

Before every context compaction, the hook:
1. Backs up the transcript to `thinking/session-logs/` (keeps last 30)
2. Parses the JSONL transcript to extract the last user intent and assistant action
3. Detects the current work mode (coding / debugging / deploy / ideation / git workflow)
4. Writes `.claude/session-resume-card.md` with all of this

At session start, the card is injected into context automatically — no manual copy-paste needed.

## Install

```bash
npx clawhub@latest install @openclaw/pre-compact-resume-card
```

Or manually: copy `scripts/pre-compact.sh` and `scripts/session-start.sh` into your project's `.claude/scripts/`, then register the hooks in `.claude/settings.json` using `references/settings-example.json` as template.

## Hook Registration

```json
{
  "hooks": {
    "PreCompact": [{ "matcher": "", "hooks": [{ "type": "command", "command": "bash .claude/scripts/pre-compact.sh" }] }],
    "SessionStart": [{ "matcher": "", "hooks": [{ "type": "command", "command": "bash .claude/scripts/session-start.sh" }] }]
  }
}
```

## The Insight

Written rules get forgotten. Mechanical hooks don't. This skill is the difference between Claude starting fresh (useless) and Claude starting exactly where you left off (valuable). The resume card costs ~200 tokens per session start — cheap insurance against rebuilding context from scratch.

## Files

- `scripts/pre-compact.sh` — fires before compaction: backup + parse transcript + write resume card
- `scripts/session-start.sh` — inject the resume card at session start
- `references/settings-example.json` — hook registration template
