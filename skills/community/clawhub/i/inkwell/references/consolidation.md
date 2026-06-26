# Daily Consolidation

A cron job that reviews all sessions from the day and extracts knowledge into your memory system.

## Table of Contents

- [Setup](#setup)
- [The Consolidation Prompt](#the-consolidation-prompt)
- [Configuration Options](#configuration-options)
- [Manual Execution](#manual-execution)
- [Checking Run History](#checking-run-history)

## Setup

Add the consolidation cron job:

```bash
openclaw cron add \
  --schedule "0 20 * * *" \
  --model "anthropic/claude-sonnet-4-20250514" \
  --channel "<your-channel>" \
  --prompt "$(cat <<'EOF'
Daily consolidation: Review all sessions from today and extract knowledge.

1. Read memory/YYYY-MM-DD.md (today's date) to see what's already captured.
2. Review recent session activity for anything not yet captured.
3. For each significant item found:
   - Decisions made → update relevant file in life/ or create a new ADR in life/resources/decisions/
   - Lessons learned → update MEMORY.md under "Lessons Learned"
   - Project updates → update the relevant file in life/projects/
   - Action items → add to MEMORY.md under "Open Items"
   - New knowledge → create or update files in life/resources/
4. Update today's daily note (memory/YYYY-MM-DD.md) with a consolidation summary.
5. Report what was updated in a brief summary message.

Be concise. Only extract genuinely useful knowledge — skip routine chatter.
EOF
)"
```

Replace `<your-channel>` with your delivery channel:
- Telegram: `telegram`
- Discord: `discord` or `discord:<channel-id>`

### Schedule Examples

| Schedule | Cron Expression |
|----------|----------------|
| 8 PM daily (default) | `0 20 * * *` |
| 6 PM weekdays only | `0 18 * * 1-5` |
| 10 PM daily | `0 22 * * *` |
| Every 12 hours | `0 8,20 * * *` |

## The Consolidation Prompt

The prompt above covers the core workflow. Customize it based on your needs:

**Minimal version** (cheaper, faster):
```
Review today's sessions. Update memory/YYYY-MM-DD.md with key decisions, lessons, and action items. Update MEMORY.md if any tacit knowledge was gained. Brief summary.
```

**Thorough version** (for knowledge-heavy days):
```
Deep consolidation: Review all sessions comprehensively.
1. Extract decisions, lessons, action items, project updates, new knowledge
2. Cross-reference with existing life/ files for updates
3. Check if any Open Items in MEMORY.md were completed today
4. Look for patterns or recurring themes worth documenting
5. Update all relevant files and report changes
```

## Configuration Options

### Model

Use a cheaper model for consolidation — it's a structured extraction task, not creative work:

| Model | Cost | Quality | Recommendation |
|-------|------|---------|----------------|
| Claude Sonnet | $$ | Good | Default — best balance |
| Claude Haiku | $ | Adequate | Budget option for simple days |
| Claude Opus | $$$$ | Excellent | Only if consolidation quality matters a lot |

### Channel

The `--channel` flag controls where the consolidation summary is delivered. If omitted, it runs silently (output only in cron logs).

### Timezone

Cron runs in the gateway's system timezone. Ensure your schedule accounts for this:
```bash
# Check gateway timezone
date  # or on Windows: Get-Date
```

## Manual Execution

Run consolidation on demand:

```bash
# List cron jobs to find the consolidation job ID
openclaw cron list

# Run it immediately
openclaw cron run <job-id>
```

## Checking Run History

```bash
# View recent cron runs
openclaw cron history

# View a specific run's output
openclaw cron history <run-id>
```

## Tips

- **Skip if recently ran**: The sign-off routine checks whether consolidation already ran. No need to duplicate.
- **Morning consolidation**: Some prefer running at 8 AM to process overnight sessions. Both work.
- **Cost awareness**: Each run costs one model call. Sonnet at daily frequency is very affordable.
- **Session coverage**: The cron job has access to session transcripts if QMD session indexing is enabled. Without it, it relies on daily notes and file changes.
