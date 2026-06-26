---
name: lucid-dreamer
version: 0.7.8
description: "Nightly AI memory reasoning system. Lucid runs every night while you sleep — it reads your daily notes and memory files, detects stale facts, unresolved todos, recurring problems, forgotten decisions, and can optionally perform aggressive cleanup and contradiction detection. Includes optional session debrief for quick end-of-day memory capture. Zero dependencies, no database, no embeddings. Just a cron job and markdown files. Use when you want your AI agent to automatically maintain and improve its long-term memory over time. Triggers on \"memory dreamer\", \"nightly memory review\", \"lucid\", \"auto memory\", \"memory cleanup\", \"memory hygiene\"."
metadata: {"openclaw":{"requires":{"bins":["git","date","python3"],"note":"Set CLAWD_DIR to your workspace path before running. Auto-apply and aggressive cleanup are disabled by default. python3 required for trend detection."}}}
---

# Lucid Dreamer 🧠

> *Your AI sleeps. Lucid dreams.*

Lucid keeps your AI's memory clean. Every night, it reads what happened, checks what your AI already knows, and suggests what's outdated, missing, or forgotten.

See `README.md` for full setup, `ARCHITECTURE.md` for internals, and `config/` for configuration.

## Quick Setup

1. Set your workspace path in the config:
   ```bash
   export CLAWD_DIR=/path/to/your/workspace
   ```

2. Create a nightly cron job using OpenClaw's cron tool — run the prompt in `prompts/nightly-review.md` at 3 AM.

   Optional: add a lightweight session debrief cron around 18:00 using `prompts/session-debrief.md`. This is a faster daily capture pass than the nightly review — it reads today's daily note and writes durable decisions/facts straight into memory without creating a review report.

3. Wake up to a review report in `memory/review/YYYY-MM-DD.md`.

4. Approve or reject suggestions — Lucid tracks state in `memory/review/state.json`.

## Optional Session Debrief Cron

Use `prompts/session-debrief.md` for a quick end-of-day memory pass around 18:00. It is designed to run faster than the nightly review: read today's daily note, capture durable decisions/facts/action items, and write them directly into memory.

Recommended OpenClaw cron settings:

```bash
openclaw cron add \
  --name "lucid-debrief" \
  --cron "0 18 * * *" \
  --tz "Europe/Vienna" \
  --model "your-preferred-model" \  # e.g. anthropic/claude-haiku-4-5 or opencode-go/minimax-m2.7
  --session isolated \
  --wake-mode now \
  --message "$(cat prompts/session-debrief.md)"
```

What it does:
- Reads today's daily note (`memory/TODAY.md`)
- Captures key decisions, durable facts, and concrete action items
- Writes those updates directly into long-term memory
- Skips the full review report to stay quick and cheap

## Files

- `prompts/nightly-review.md` — the main nightly review prompt
- `prompts/session-debrief.md` — optional quick-capture prompt for ~18:00
- `config/` — thresholds and behavior settings
- `examples/` — sample review output and state file

## Security

**Files read at runtime:**
- `MEMORY.md` — long-term agent memory summary
- `USER.md` — user profile and preferences
- Last 7 daily notes (`memory/YYYY-MM-DD.md`)

**Files written at runtime:**
- `memory/review/YYYY-MM-DD.md` — the generated review report
- `memory/review/state.json` — approval/rejection tracking state

**What this skill is designed to avoid:**
- Avoid suggesting or outputting passwords, API keys, tokens, or other credentials in generated memory updates
- Never accesses files outside the configured workspace directory
- Never pushes to remote git automatically — all commits are local only, and no `git push` is performed unless you explicitly run it
- Announce/notification delivery is opt-in and off by default — no messages are sent without explicit configuration

**Recommendations:**
- Set `CLAWD_DIR` explicitly in your environment to ensure the skill operates on the correct workspace
- This skill reads workspace markdown files such as `MEMORY.md`, `USER.md`, and recent daily notes. Do not run it on a workspace containing unencrypted API keys or other secrets in plain markdown files.
- Review generated reports before approving suggestions — Lucid proposes changes, but you remain in control
