# scribe — OpenClaw Memory Skill

> An autonomous stenographer for your AI agent. Extracts decisions, preferences, and key insights from your daily sessions and writes them to persistent memory files.

## The Problem

AI agents forget everything between sessions. Context window compaction is lossy and passive. You end up re-explaining yourself constantly.

## The Solution

Scribe runs every night as an isolated cron job, scans your OpenClaw session logs, and extracts what actually matters — structured, searchable, durable.

```markdown
# 2026-03-04 Memory (Scribe)

## 🔑 Decisions Made
- Chose Plan B (cron + skill) for the stenographer architecture

## 🗣️ Framework Sentences
- "一步一步来" — prefers incremental execution
- "做不到就换个方法" — zero tolerance for blocking

## 📦 Project Updates
- scribe skill: scripts complete, publishing to ClawdHub
```

## Install

```bash
# 1. Install via ClawdHub (once published)
clawdhub install scribe

# 2. Register nightly cron
python3 skills/public/scribe/scripts/setup-cron.py

# 3. Run manually
python3 skills/public/scribe/scripts/scribe.py
```

## Requirements

- [OpenClaw](https://openclaw.ai) with an active gateway
- OpenRouter API key (reads from your existing OpenClaw config automatically)

## Files

```
scribe/
├── SKILL.md                    # Skill definition + onboarding
├── scripts/
│   ├── scribe.py               # Core extraction script
│   └── setup-cron.py           # One-command cron registration
└── references/
    ├── cron-setup.md           # Cron config details
    └── signal-guide.md         # How signals are classified
```

## License

MIT
