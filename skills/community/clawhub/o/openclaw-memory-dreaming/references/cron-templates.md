# Cron Templates

Ready-to-use OpenClaw cron job definitions for automated memory maintenance.

## Nightly Dream Cycle

Runs the full dream cycle at 3am UTC in an isolated session.

```json
{
  "name": "dream-cycle",
  "schedule": { "kind": "cron", "expr": "0 3 * * *", "tz": "UTC" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run a dream cycle. Steps:\n1. Run: node scripts/memory-decay.js\n2. Read today's and yesterday's memory/YYYY-MM-DD.md files\n3. For each significant item, integrate into MEMORY.md if not already there\n4. Prune stale entries from MEMORY.md (decayScore < 0.2, not structural)\n5. Run memory-supersede.js for any facts that changed\n6. Append summary to memory/dream-log.md\n7. Re-run memory-bootstrap.js to pick up new MEMORY.md entries\n\nBe selective. Only integrate what's worth remembering in 6 months.",
    "timeoutSeconds": 300
  },
  "delivery": { "mode": "none" }
}
```

**Notes:**
- `delivery: none` keeps it silent — dream cycles are background work
- Adjust timezone to your human's timezone so it runs while they sleep
- 300s timeout is generous; typical cycles take 30-60s

## Nightly Conversation Archive + Summarise

Archives all channel conversations and generates summaries. Run before the
dream cycle so fresh summaries are available.

```json
{
  "name": "conversation-archive",
  "schedule": { "kind": "cron", "expr": "30 2 * * *", "tz": "UTC" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run conversation archiving:\n1. node scripts/conversation-archive.js --all\n2. node scripts/conversation-summarise.js --all\n\nReport any errors but don't alert the user unless something is broken.",
    "timeoutSeconds": 600
  },
  "delivery": { "mode": "none" }
}
```

**Notes:**
- Runs at 2:30am, 30 minutes before the dream cycle
- 600s timeout because summarisation involves LLM calls with rate limiting
- Archive runs first (fast, local), then summarise (slower, API calls)

## Weekly Memory Review

A deeper review — checks for stale entries, updates MEMORY.md structure,
prunes sections that have grown unwieldy.

```json
{
  "name": "weekly-memory-review",
  "schedule": { "kind": "cron", "expr": "0 4 * * 0", "tz": "UTC" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Weekly memory maintenance:\n1. Run memory-decay.js --verbose\n2. Review the last 7 days of memory/YYYY-MM-DD.md files\n3. Check MEMORY.md for:\n   - Duplicated information\n   - Outdated facts (use memory-supersede.js)\n   - Sections that are too long (summarise)\n   - Missing information from daily notes\n4. Review memory/dream-log.md for patterns\n5. Update MEMORY.md structure if needed\n6. Log findings to dream-log.md",
    "timeoutSeconds": 600
  },
  "delivery": { "mode": "announce" }
}
```

**Notes:**
- Runs Sunday 4am, after the nightly cycle
- `delivery: announce` sends a summary to chat — useful for weekly reviews
- This is where structural improvements to MEMORY.md happen

## Installing Cron Jobs

Use the OpenClaw cron API or CLI:

```bash
# Via the gateway cron tool
cron add --job '<json above>'
```

Or in conversation: "Add a cron job for the nightly dream cycle" and paste
the JSON definition.

## Heartbeat Alternative

If you prefer heartbeat-based execution over cron, add to your HEARTBEAT.md:

```markdown
## Memory Maintenance
Every 6 hours, run memory-decay.js and check for unprocessed daily notes.
If unprocessed notes exist, run a mini dream cycle (steps 1-3 only).
Track last run in memory/heartbeat-state.json under "lastDreamCycle".
```

This is less precise but batches well with other heartbeat tasks.
