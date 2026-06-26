---
name: memory-dreaming
description: >
  A Markdown + JSON memory framework with conversation archiving for AI agents.
  Provides persistent long-term memory with biologically-inspired decay,
  recall boosting, temporal fact chains, dream-cycle consolidation, and
  channel-agnostic conversation archiving with AI-generated summaries.
  No vector database, graph store, or external service required.
  Use when you need: agent memory that persists across sessions, conversation
  context across channels/groups/topics, fact lifecycle tracking (supersession),
  or automated memory maintenance via dream cycles.
source: https://github.com/ptburkis/openclaw-memory-dreaming
homepage: https://github.com/ptburkis/openclaw-memory-dreaming
---

# Memory Dreaming

Agent-native memory and dreaming framework. Plain Markdown and JSON — no RAG,
no vector store, no graph database. Just files your human can read and edit.

> **References** (load when needed):
> - `references/architecture.md` — data model, biological inspiration, design decisions
> - `references/dream-cycle.md` — full dream cycle procedure with examples
> - `references/cold-start.md` — starting from zero memories
> - `references/cron-templates.md` — ready-to-use OpenClaw cron definitions

---

## Setup

### 1. Copy scripts to your workspace

```bash
cp skills/memory-dreaming/scripts/*.js scripts/
```

Scripts use `path.resolve(__dirname, '..')` for workspace root — they must
live in `<workspace>/scripts/`.

### 2. Bootstrap (if you have an existing MEMORY.md)

```bash
node scripts/memory-bootstrap.js          # seed memory-meta.json
node scripts/conversation-archive.js --discover  # see available channels
```

Starting from scratch? See `references/cold-start.md`.

### 3. Set up conversation archiving (optional)

Create `archives/archive-config.json` to label your groups:

```json
{
  "agentName": "YourName",
  "groups": { "<group-id>": { "name": "my-group", "label": "My Group" } },
  "topicNames": { "<group-id>": { "1": "General" } }
}
```

Then archive and summarise:

```bash
node scripts/conversation-archive.js --all
node scripts/conversation-summarise.js --all
```

---

## Two Layers

### Layer 1: Core Memory

Your curated knowledge — facts, preferences, decisions, people.

| File | Purpose |
|------|---------|
| `MEMORY.md` | Long-term memory (human-readable, agent-edited) |
| `memory/YYYY-MM-DD.md` | Daily notes (raw session logs) |
| `memory/memory-meta.json` | Decay metadata per entry |
| `memory/dream-log.md` | Dream cycle audit trail |
| `memory/archive/YYYY-MM.md` | Archived (forgotten) entries |

### Layer 2: Conversational Memory

Context from group chats, channels, topics — archived and summarised.

| File | Purpose |
|------|---------|
| `archives/<channel>/<group>/raw/` | Full conversation transcripts |
| `archives/<channel>/<group>/summaries/` | AI-generated topic summaries |
| `archives/<channel>/<group>/DIGEST.md` | Cross-topic master digest |
| `archives/<channel>/<group>/INDEX.md` | Topic index with message counts |

---

## Memory Tiers

| Tier | Age | Decays? | Notes |
|------|-----|---------|-------|
| `hot` | <48h | Yes | New entries |
| `warm` | <30d | Yes | Recent |
| `cold` | <365d | Yes | Long-term |
| `archived` | — | Removed | score<0.1 + recalls<2 |
| `crystallised` | ∞ | Never | 20+ recalls |

Structural entries (IPs, people, URLs, passwords) never decay below **0.3**.

### Decay Formula

```
baseDecay    = 1.0 - (daysSinceCreated / maxAgeDays)
recallBoost  = min(recallCount × 0.05, 0.5)
recencyBoost = lastRecalled ≤7d → 0.2 | ≤30d → 0.1 | else → 0
decayScore   = clamp(base + recall + recency, 0.0, 1.0)
```

---

## Scripts (6)

### Core Memory

| Script | Purpose | When to run |
|--------|---------|-------------|
| `memory-bootstrap.js` | Seed meta from MEMORY.md | Setup + after adding entries |
| `memory-decay.js` | Recalculate scores, tier transitions | Start of dream cycle |
| `memory-recall-logger.js` | Log recall events, boost scores | After every memory search |
| `memory-supersede.js` | Create temporal fact chains | When facts change |

### Conversation Memory

| Script | Purpose | When to run |
|--------|---------|-------------|
| `conversation-archive.js` | Archive channel transcripts | Nightly (before summarise) |
| `conversation-summarise.js` | AI-summarise topics + digest | Nightly (after archive) |

### Usage Examples

```bash
# Core memory
node scripts/memory-decay.js --verbose
node scripts/memory-recall-logger.js --query "dev server IP" --matches "Dev server: user@203.0.113.10"
node scripts/memory-supersede.js --old "Status: pending" --new "Status: accepted"

# Conversation memory
node scripts/conversation-archive.js --discover     # list available sessions
node scripts/conversation-archive.js --all           # archive everything
node scripts/conversation-archive.js --channel telegram --group my-group
node scripts/conversation-summarise.js --all         # summarise all archived
node scripts/conversation-summarise.js --force       # re-summarise everything
```

---

## Daily Workflow

### Every session
1. Load `MEMORY.md` for context.
2. After searching memory, log recalls:
   ```bash
   node scripts/memory-recall-logger.js --query "<search>" --matches "<matched line>"
   ```

### When you learn something new
- Add to `MEMORY.md` under the right section.
- If it replaces an old fact, run `memory-supersede.js`.

### Daily notes
- Create `memory/YYYY-MM-DD.md` with what happened.
- Bullet points. Decisions, contacts, technical details, anything worth keeping.

---

## Dream Cycle

Agent-orchestrated consolidation. Run nightly or during quiet heartbeats.

1. **Decay** — `node scripts/memory-decay.js`
2. **Review** — Read recent `memory/YYYY-MM-DD.md` files
3. **Integrate** — Move significant items into `MEMORY.md`
4. **Prune** — Remove stale entries (low score, not structural)
5. **Supersede** — Chain any changed facts
6. **Log** — Append summary to `memory/dream-log.md`
7. **Re-bootstrap** — `node scripts/memory-bootstrap.js` (picks up new entries)

Full procedure with worked examples: `references/dream-cycle.md`.
Cron job definitions: `references/cron-templates.md`.

---

## Conversation Context Loading

When receiving a message from a group/topic, load context before responding:

1. Check `archives/<channel>/<group>/summaries/topic-<id>.md` for topic context
2. For cross-topic awareness, skim `DIGEST.md`
3. If summary seems stale, re-run archive + summarise for that group

This prevents the "I don't know what you're talking about" problem in
long-running group conversations.

---

## Limitations

- **No semantic search.** Recall matching is hash → substring → Jaccard word overlap.
  Good for exact/close matches. Won't find conceptually related entries.
- **Bootstrap hash is fragile.** Based on first 20 chars — editing the start of
  an entry creates a new hash and loses history.
- **Dream cycles need judgment.** The scripts provide mechanics; you provide
  the editorial sense of what's worth keeping.
- **Summarisation costs money.** Uses LLM API calls. Free-tier models work
  but quality varies. Configure `summariseModel` in archive-config.json.
- **MEMORY.md is ground truth.** Meta tracks metadata; Markdown is what you read.
  Keep them in sync.

This is a work in progress. Start simple, observe what works, add complexity
when the simple thing breaks.

---

## Credentials & Privacy

### Required credentials

**Core memory scripts (4):** No credentials needed. These are pure local
file operations — read/write Markdown and JSON in your workspace.

**Conversation summariser:** Requires an LLM API key. Set one of:
- `OPENROUTER_API_KEY` in `.env.openrouter` or environment
- `OPENAI_API_KEY` in `.env.openai` or environment

The summariser sends conversation transcripts to the configured LLM provider
for summarisation. **This means your chat content is sent to a third-party
API.** Use a self-hosted model or review transcripts before summarising if
this is a concern.

**Conversation archiver:** No credentials. Reads local OpenClaw session
transcripts and writes local Markdown files.

### What gets read

- `MEMORY.md` and `memory/` files (your workspace)
- OpenClaw session transcripts (`sessions.json` + `.jsonl` files)
- `.env.openrouter` or `.env.openai` (for API keys, summariser only)
- `archives/archive-config.json` (optional config you create)

### What gets written

- `memory/memory-meta.json`, `memory/dream-log.md`, `memory/archive/`
- `archives/<channel>/<group>/` (raw transcripts, summaries, digests)

### What gets sent externally

- **Only `conversation-summarise.js`** sends data externally (to your
  configured LLM API for summarisation). All other scripts are fully local.
- Raw conversation text is sent to the LLM. If your transcripts contain
  sensitive information, credentials, or private messages, those will be
  included unless you filter them first.
