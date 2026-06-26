# Memory Dreaming 🧠💤

A memory and dreaming framework for AI agents. Built on plain Markdown and JSON.

> *Your agent doesn't need a vector database. It needs a journal and a good night's sleep.*

## What is this?

Memory Dreaming gives your OpenClaw agent persistent memory across sessions using only files — no RAG pipeline, no vector embeddings, no graph database, no external services. Everything is human-readable Markdown and JSON that you can inspect, edit, and understand.

It has two layers:

**Core Memory** — A curated `MEMORY.md` with metadata tracking (decay scores, recall counts, tier promotion, temporal fact chains) and daily notes.

**Conversational Memory** — Channel-agnostic archiving and AI summarisation of group chats, so your agent maintains context across every conversation without holding it all in the context window.

## Why not RAG?

We built this because we wanted to understand what was happening. Vector databases are black boxes — you embed text, run a similarity search, and hope the right chunks come back. That works, but:

- **The agent IS the retrieval engine.** When an LLM searches `MEMORY.md`, it understands context, nuance, and relevance in ways cosine similarity never will.
- **Dream cycles are reflection, not retrieval.** The nightly consolidation — reviewing daily notes, integrating significant items, pruning stale facts — forces synthesis. That's where the real value is.
- **Temporal chains solve stale facts.** Instead of overwriting, we track when facts change and why. "Status: pending" → "Status: accepted" with timestamps and chains.
- **You can read it.** Open `MEMORY.md` in a text editor. See exactly what your agent remembers, how often it's recalled each fact, what's decaying, what's crystallised.

We'll graduate to RAG/graph when the simple approach breaks. It hasn't yet. That says something.

## How it works

### Memory Tiers

Inspired by the Ebbinghaus forgetting curve and spaced repetition research:

```
┌─────────────────────────────────────────────────────┐
│                    CRYSTALLISED                      │
│              (20+ recalls, never decays)             │
├─────────────┬─────────────┬─────────────┬───────────┤
│     HOT     │    WARM     │    COLD     │ ARCHIVED  │
│   (<48h)    │   (<30d)    │  (<365d)    │(forgotten)│
│  score: 1.0 │ score: 0.6  │ score: 0.3  │score:<0.1 │
└─────────────┴─────────────┴─────────────┴───────────┘
        ←── time passes, score decays ──→
        ←── recalls boost score back ──→
```

Every memory entry has a decay score calculated from age, recall frequency, and recency. Structural entries (IPs, people, passwords, URLs) get a floor of 0.3 — they age but never fully decay. Entries recalled 20+ times crystallise permanently.

### Dream Cycles

The biological metaphor is deliberate. During sleep, humans consolidate short-term memories into long-term storage, prune unneeded connections, and integrate new experiences with existing knowledge.

Your agent does the same:

1. **Decay** — Recalculate all scores (some entries age out)
2. **Review** — Read recent daily notes
3. **Integrate** — Move significant items into long-term memory
4. **Prune** — Remove stale entries
5. **Supersede** — Chain any changed facts
6. **Log** — Record what happened

### Conversational Memory

For agents that participate in multiple group chats, channels, or topics:

```
conversation-archive.js  →  raw transcripts per topic
conversation-summarise.js →  AI summaries + master digest
```

When the agent receives a message from a group topic, it loads the relevant summary instead of the full transcript. This gives context without burning the whole context window.

Works with any OpenClaw channel: Telegram, Discord, WhatsApp, Signal, Slack, IRC.

### Temporal Fact Chains

Facts change. Instead of silently overwriting:

```bash
node scripts/memory-supersede.js \
  --old "Project Alpha: awaiting outcome" \
  --new "Project Alpha: offer accepted" \
  --when "2026-04-01"
```

This creates a chain: the old entry gets `validUntil` and `supersededBy` pointing to the new one. You can trace the history of any fact.

## Quick Start

### 1. Install the skill

Copy to your OpenClaw workspace:
```bash
cp -r memory-dreaming/scripts/*.js /path/to/workspace/scripts/
```

### 2. Bootstrap

```bash
# If you have an existing MEMORY.md
node scripts/memory-bootstrap.js

# Starting from scratch? See references/cold-start.md
```

### 3. Set up conversation archiving

```bash
# See what channels/groups are available
node scripts/conversation-archive.js --discover

# Archive everything
node scripts/conversation-archive.js --all
node scripts/conversation-summarise.js --all
```

### 4. Schedule dream cycles

Add a nightly cron job (see `references/cron-templates.md` for ready-to-use definitions):

```json
{
  "name": "dream-cycle",
  "schedule": { "kind": "cron", "expr": "0 3 * * *" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run a dream cycle: decay → review daily notes → integrate → prune → log."
  }
}
```

## File Layout

```
workspace/
├── MEMORY.md                              # Long-term memory
├── memory/
│   ├── memory-meta.json                   # Decay metadata
│   ├── dream-log.md                       # Dream cycle audit log
│   ├── YYYY-MM-DD.md                      # Daily notes
│   └── archive/YYYY-MM.md                 # Forgotten entries
├── archives/
│   └── <channel>/<group>/
│       ├── INDEX.md                       # Topic listing
│       ├── DIGEST.md                      # Cross-topic digest
│       ├── raw/topic-<id>.md              # Full transcripts
│       └── summaries/topic-<id>.md        # AI summaries
└── scripts/
    ├── memory-bootstrap.js                # Seed metadata
    ├── memory-decay.js                    # Recalculate scores
    ├── memory-recall-logger.js            # Track recalls
    ├── memory-supersede.js                # Fact chains
    ├── conversation-archive.js            # Archive channels
    └── conversation-summarise.js          # Summarise archives
```

## Data Model

Each entry in `memory-meta.json`:

```json
{
  "key": "First 60 chars of the bullet point",
  "section": "Section heading from MEMORY.md",
  "created": "2026-02-06T00:00:00Z",
  "lastRecalled": "2026-04-01T14:30:00Z",
  "recallCount": 12,
  "tier": "warm",
  "decayScore": 0.72,
  "structural": true,
  "validFrom": "2026-02-06T00:00:00Z",
  "validUntil": null,
  "supersededBy": null
}
```

Full data model documentation: `references/architecture.md`

## Security & Privacy

**Core memory scripts** (bootstrap, decay, recall, supersede) are fully local.
They read and write files in your workspace. No network calls, no credentials
needed.

**Conversation archiver** is fully local. It reads OpenClaw session transcripts
and writes Markdown files. No network calls.

**Conversation summariser** sends conversation text to an external LLM API
(OpenRouter or OpenAI) for summarisation. This means:

- Your chat transcripts are sent to a third-party API
- **Built-in redaction** automatically strips common secret patterns (API keys,
  tokens, passwords, AWS credentials, Bearer headers) before sending
- Configure `excludePatterns` in `archive-config.json` to filter additional
  sensitive content
- You can run summarisation with a self-hosted model to keep everything local

**Required credentials:**
- `OPENROUTER_API_KEY` or `OPENAI_API_KEY` — only needed for the summariser
- Set in `.env.openrouter`, `.env.openai`, or environment variables

## Status

**Work in progress.** We're actively using this in production and iterating. The approach is deliberately simple — we add complexity only when the simple thing breaks.

Known limitations:
- No semantic search (uses hash → substring → Jaccard matching)
- Bootstrap hash is based on first 20 chars (fragile to edits)
- Dream cycles need agent judgment (that's a feature, not a bug)
- Summarisation requires LLM API calls (free-tier models work)

## Credits

Built by [Peter Rossi](https://linkedin.com/in/peterrossi) and James (an [OpenClaw](https://github.com/openclaw/openclaw) agent).

Born from the observation that AI agents don't need bigger databases — they need better habits.

## License

MIT

## Links

- [OpenClaw](https://github.com/openclaw/openclaw) — the agent framework this skill runs on
- [ClaWHub](https://clawhub.com) — find more OpenClaw skills
- [OpenClaw Discord](https://discord.com/invite/clawd) — community
