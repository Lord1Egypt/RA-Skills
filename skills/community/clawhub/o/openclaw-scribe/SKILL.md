---
name: scribe
description: Autonomous session scribe — reads today's OpenClaw session logs, extracts decisions, preferences, framework sentences, and project updates, then writes a structured daily memory file. Use when setting up automated memory extraction for an AI agent, or when manually triggering a memory consolidation pass. Works as a cron job (isolated session) or on-demand.
---

# Scribe

An autonomous "stenographer" agent that watches your OpenClaw session history and extracts what matters into persistent, structured memory files — so your agent remembers across sessions without relying on context window compaction.

## Install & Setup

**1. Copy the skill to your workspace:**
```bash
cp -r skills/public/scribe ~/.openclaw/workspace/skills/public/scribe
```

**2. Register the nightly cron job (one command):**
```bash
python3 skills/public/scribe/scripts/setup-cron.py
```

That's it. Scribe will run every night at 23:30 and write `memory/YYYY-MM-DD.md` to your workspace.

**3. Run manually anytime:**
```bash
python3 skills/public/scribe/scripts/scribe.py
```

## How It Works

1. Scans today's session JSONL files from `~/.openclaw/agents/main/sessions/`
2. Filters out heartbeats, system messages, and noise
3. Sends user messages to an LLM (via OpenRouter, reads your existing OpenClaw API key)
4. Extracts: decisions, preferences, framework sentences, project updates, todos
5. Writes structured output to `{workspace}/memory/YYYY-MM-DD.md`

## Output Format

```markdown
# YYYY-MM-DD Memory (Scribe)

## 🔑 Decisions Made
## 💡 Preferences & Rules
## 🗣️ Framework Sentences
## 📦 Project Updates
## ✅ Todos / Follow-ups
```

## Configuration

Environment variables (all optional — defaults work out of the box):

| Variable | Default | Description |
|---|---|---|
| `SCRIBE_SESSION_DIR` | `~/.openclaw/agents/main/sessions` | Session JSONL location |
| `SCRIBE_WORKSPACE` | `~/.openclaw/workspace` | Where memory files are written |
| `SCRIBE_DAYS` | `1` | Days back to scan |
| `SCRIBE_MODEL` | `anthropic/claude-haiku-4-5` | LLM model (OpenRouter ID) |
| `SCRIBE_APPEND_LONGTERM` | `false` | Also append to MEMORY.md |
| `OPENROUTER_API_KEY` | *(from OpenClaw config)* | Override API key |

## References

- **Cron setup details**: `references/cron-setup.md` — manual config, launchd, timezone changes
- **Signal classification**: `references/signal-guide.md` — how the LLM decides what's worth extracting
