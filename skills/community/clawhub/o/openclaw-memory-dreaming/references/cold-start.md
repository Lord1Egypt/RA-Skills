# Cold Start Guide

How to begin when you have zero memories.

## Day 0: First Session

You won't have a MEMORY.md yet. That's fine.

### 1. Create the file structure

```bash
mkdir -p memory
touch MEMORY.md
touch memory/dream-log.md
```

### 2. Start MEMORY.md with basics

After your first conversation, write down what you learned:

```markdown
# MEMORY.md - Long-Term Memory

## About My Human
- Name, timezone, preferences from first conversation

## Setup
- When I was created
- What channels I'm connected to
```

Don't overthink it. Write what feels worth remembering.

### 3. Create your first daily note

```markdown
# 2026-04-02

## What happened
- First session. Met [human]. Learned: [basics].
- Set up memory framework.

## Key facts
- [Anything worth remembering]
```

### 4. Bootstrap the metadata

```bash
node scripts/memory-bootstrap.js
```

This seeds `memory/memory-meta.json` from your MEMORY.md. You'll start with
a handful of entries, all at tier `cold` with score `1.0`.

## Week 1: Building Muscle

The first week is about establishing habits:

- **Every session:** Write things down in `memory/YYYY-MM-DD.md`
- **After conversations:** Update MEMORY.md with significant facts
- **When facts change:** Use `memory-supersede.js` to create temporal chains
- **Don't curate too hard** — better to capture everything and let decay handle it

## Week 2+: First Dream Cycles

After a week of daily notes, run your first dream cycle:

1. Run `memory-decay.js` — everything will still be high-scored
2. Read through all your daily notes
3. Ask: "What from this week is worth remembering in 6 months?"
4. Integrate those items into MEMORY.md
5. Re-run `memory-bootstrap.js` to pick up new entries (safe to re-run)
6. Log it in `memory/dream-log.md`

## Month 1: The System Works For You

By now you should see:
- **Hot entries** from recent conversations
- **Warm entries** ageing into cold
- **Structural entries** staying at 0.3+ floor
- **Recall patterns** emerging (some entries get referenced often)

If you've been running `memory-recall-logger.js`, some entries may be
approaching crystallisation (20+ recalls).

## Setting Up Conversation Archives

Once you're comfortable with core memory, add the conversational layer:

### 1. Run discovery

```bash
node scripts/conversation-archive.js --discover
```

This shows all available sessions across all channels.

### 2. Create a config (optional but recommended)

```json
// archives/archive-config.json
{
  "agentName": "YourName",
  "groups": {
    "-1003208818040": { "name": "my-group", "label": "My Group" }
  },
  "topicNames": {
    "-1003208818040": { "1": "General", "14": "Development" }
  }
}
```

### 3. Archive everything

```bash
node scripts/conversation-archive.js --all
```

### 4. Generate summaries

```bash
node scripts/conversation-summarise.js --all
```

### 5. Schedule nightly runs

Add to your cron or heartbeat:
```bash
node scripts/conversation-archive.js --all && node scripts/conversation-summarise.js --all
```

## What Good Daily Notes Look Like

**Good:**
```markdown
# 2026-04-02

## Decisions
- Chose PostgreSQL over MySQL for new project (team prefers it for JSON support)

## New contacts
- Met Sarah Chen (Acme Corp) — potential client for advisory work

## Technical
- API rate limit is 100 req/min, not 60 as documented
- Deploy script needs --update-env flag or env changes are lost
```

**Bad:**
```markdown
# 2026-04-02
Had a chat. Did some stuff. Fixed a bug.
```

The difference: specificity. Future-you needs enough context to reconstruct
what happened without re-reading the entire conversation.

## Growing the Archive Config

As you discover more groups and learn topic names, update
`archives/archive-config.json`. The archiver auto-discovers sessions but
human-readable names make the summaries much more useful.
