---
name: openclaw-memory-upgrade
description: Complete guide to upgrading OpenClaw's memory system for persistent, searchable context across sessions. Implements 6 upgrades including enhanced memory flush, session indexing, QMD hybrid search, Mem0 plugin, and manual memory management patterns.
---

# OpenClaw Memory Upgrade

Turn your OpenClaw agent from a goldfish into an elephant. This skill implements 6 memory upgrades that give your agent persistent, searchable memory across sessions — so it actually remembers who you are, what you're working on, and what happened yesterday.

## The Problem

By default, OpenClaw agents wake up blank every session. Conversations are isolated. Context is lost at compaction. Your agent forgets decisions, preferences, and project status the moment the session ends.

## What This Fixes

After applying these upgrades, your agent will:
- Extract and save 8 categories of important information before context is lost
- Search across all past sessions and memory files before answering
- Use hybrid keyword + semantic search with diversity and recency ranking
- Auto-capture and auto-recall memories via the Mem0 plugin
- Maintain curated long-term memory separately from raw daily logs

## Prerequisites

- OpenClaw 2026.2.26 or later
- Access to `openclaw.json` config file
- npm (for Mem0 plugin installation)

---

## Upgrade 1: Enhanced memoryFlush Prompt

**What it does:** When a conversation nears compaction (context window filling up), this automatically scans for 8 categories of important information and writes them to daily memory files before context gets trimmed.

**Why it matters:** Without this, compaction silently discards conversation details. With it, decisions, preferences, technical details, and more survive compaction.

**Add to `openclaw.json` under `agents.defaults.compaction`:**

```json
{
  "compaction": {
    "mode": "safeguard",
    "reserveTokensFloor": 20000,
    "memoryFlush": {
      "enabled": true,
      "softThresholdTokens": 4000,
      "systemPrompt": "Session nearing compaction. Analyze the conversation and extract durable memories NOW before context is lost.",
      "prompt": "Scan the current conversation and write any of the following to memory/YYYY-MM-DD.md (use today's date):\n\n1. DECISIONS made (with reasoning and context)\n2. USER PREFERENCES or corrections expressed\n3. TECHNICAL DETAILS (commands, configs, API keys, endpoints, file paths)\n4. PROJECT STATUS changes or milestones\n5. PEOPLE mentioned (names, roles, contact info, relationships)\n6. WORKFLOWS or processes described\n7. ERRORS encountered and their solutions\n8. OPINIONS or feedback the user gave\n\nFor each item, include timestamps and enough context that future-you can understand it without the conversation. If nothing meaningful happened, reply with NO_REPLY."
    }
  }
}
```

**Config explained:**
- `mode: "safeguard"` — compaction mode that preserves important context
- `reserveTokensFloor: 20000` — always keep at least 20K tokens available for the agent to work with
- `softThresholdTokens: 4000` — trigger memory flush when only 4K tokens remain before compaction
- `systemPrompt` — injected as a system message to signal urgency
- `prompt` — the actual extraction instructions with 8 categories

---

## Upgrade 2: Session Indexing

**What it does:** Makes past conversation sessions searchable. Without this, each session is a black box once it ends. With it, the agent can search across old conversations to find things discussed days or weeks ago.

**Add to `agents.defaults.memorySearch`:**

```json
{
  "memorySearch": {
    "enabled": true,
    "experimental": {
      "sessionMemory": true
    },
    "sources": ["memory", "sessions"]
  }
}
```

**Config explained:**
- `sessionMemory: true` — indexes past session transcripts for search
- `sources: ["memory", "sessions"]` — searches both memory files AND past sessions

---

## Upgrade 3: Manual Memory Management

**What it does:** Establishes a two-tier file-based memory system that the agent reads at the start of every session.

**Structure:**
```
workspace/
  MEMORY.md          ← Curated long-term memory (the agent's brain)
  memory/
    YYYY-MM-DD.md    ← Daily logs (raw notes from each day)
```

**How it works:**
- `MEMORY.md` — distilled, organized knowledge. Sections for user profile, projects, decisions, preferences, contacts, workflows. Updated periodically.
- `memory/YYYY-MM-DD.md` — raw daily logs. Auto-written by memoryFlush, also written manually by the agent during conversations. One file per day.

**Agent instructions (add to AGENTS.md):**
```markdown
## Every Session
1. Read MEMORY.md — this is your long-term brain
2. Read memory/YYYY-MM-DD.md for today + yesterday
3. If something important happens, write it to today's daily file
4. Periodically review daily files and distill key learnings into MEMORY.md
5. Never rely on "mental notes" — if it matters, write it to a file
```

**Key principle:** Text > Brain. The agent's memory files ARE its continuity. Without them, it wakes up blank.

---

## Upgrade 4: QMD Backend (Hybrid Search)

**What it does:** Replaces basic memory search with QMD — a hybrid system combining keyword matching (BM25) and semantic understanding (vector embeddings), with diversity ranking and recency bias.

**Add to `openclaw.json` at the top level:**

```json
{
  "memory": {
    "backend": "qmd",
    "citations": "auto",
    "qmd": {
      "includeDefaultMemory": true,
      "update": {
        "interval": "5m",
        "debounceMs": 15000
      },
      "limits": {
        "maxResults": 8,
        "timeoutMs": 5000
      },
      "sessions": {
        "enabled": true,
        "retentionDays": 90
      }
    }
  }
}
```

**Also add the query configuration under `agents.defaults.memorySearch`:**

```json
{
  "memorySearch": {
    "query": {
      "hybrid": {
        "enabled": true,
        "vectorWeight": 0.7,
        "textWeight": 0.3,
        "candidateMultiplier": 4,
        "mmr": {
          "enabled": true,
          "lambda": 0.7
        },
        "temporalDecay": {
          "enabled": true,
          "halfLifeDays": 30
        }
      }
    },
    "cache": {
      "enabled": true,
      "maxEntries": 50000
    }
  }
}
```

**Config explained:**
- `hybrid search` — combines keyword (BM25, weight 0.3) with semantic/vector (weight 0.7) for best of both worlds
- `MMR (Maximal Marginal Relevance)` — ensures search results are diverse, not 8 near-identical matches. Lambda 0.7 balances relevance vs diversity.
- `temporalDecay` — recent memories rank higher than old ones. 30-day half-life means a memory from today scores 2x higher than one from a month ago.
- `retentionDays: 90` — keeps 90 days of session history searchable
- `update interval: 5m` — re-indexes memory files every 5 minutes with 15-second debounce
- `cache: 50000 entries` — caches search results for speed

---

## Upgrade 5: Mem0 Plugin (Auto-Capture & Auto-Recall)

**What it does:** Adds a separate memory layer that automatically captures important information from conversations and automatically recalls relevant memories before the agent responds.

**Install:**
```bash
openclaw plugin install @mem0/openclaw-mem0
```

**Add to `openclaw.json` under `plugins`:**

```json
{
  "plugins": {
    "slots": {
      "memory": "openclaw-mem0"
    },
    "entries": {
      "openclaw-mem0": {
        "enabled": true,
        "config": {
          "mode": "open-source",
          "autoCapture": true,
          "autoRecall": true,
          "enableGraph": true,
          "topK": 10,
          "searchThreshold": 0.5
        }
      }
    }
  }
}
```

**Config explained:**
- `mode: "open-source"` — runs locally, no external API calls
- `autoCapture: true` — automatically saves important facts from conversations without being told
- `autoRecall: true` — automatically searches memory before responding to questions
- `enableGraph: true` — builds a knowledge graph of relationships between memories
- `topK: 10` — returns up to 10 relevant memories per search
- `searchThreshold: 0.5` — only returns memories above 50% relevance score

**Note:** Requires the Ollama npm module. If you see errors about missing `ollama` module, run:
```bash
cd ~/.openclaw/extensions/openclaw-mem0 && npm install ollama
```

---

## Upgrade 6: Cognee (Optional — Requires Docker)

**What it does:** Graph-based memory system for advanced knowledge representation.

**Status:** Optional. Requires Docker to be running. Also flagged by OpenClaw security audit for environment variable harvesting patterns in its code. Recommended to skip unless you have Docker running AND have audited the plugin source code.

**If you want to install it anyway:**
```bash
openclaw plugin install @cognee/cognee-openclaw
```

**Recommendation:** Skip this one. Upgrades 1-5 provide comprehensive memory coverage. Cognee adds complexity without proportional benefit for most setups.

---

## How It All Fits Together

```
Conversation happens
    │
    ├── Mem0 auto-captures important facts (real-time)
    │
    ├── Agent writes to memory/YYYY-MM-DD.md (manual)
    │
    ├── memoryFlush triggers before compaction (automatic, 8 categories)
    │
    └── QMD indexes everything (every 5 min)
            │
            ├── BM25 keyword search
            ├── Vector semantic search
            ├── MMR diversity ranking
            ├── Temporal decay (recent > old)
            └── Session history (90 days)

Next session starts
    │
    ├── Agent reads MEMORY.md + today's daily note
    ├── Mem0 auto-recalls relevant memories
    └── QMD searches across all files + sessions
```

## Verification

After applying all upgrades, restart the gateway:
```bash
openclaw gateway restart
```

Then verify:
```bash
openclaw status --deep
```

You should see:
- Memory: `enabled (plugin openclaw-mem0)`
- Memory backend: `qmd`
- Session indexing: active

Test by telling your agent something specific, ending the session, starting a new one, and asking about it. If the memory system is working, it should find it.

## Estimated Token Overhead

The memory system adds minimal overhead:
- memoryFlush: ~2,000-5,000 tokens per compaction event (only when needed)
- Mem0 auto-recall: ~500-1,000 tokens per query (injected relevant memories)
- QMD search: runs server-side, no token cost
- File reading (MEMORY.md + daily notes): depends on file size, typically 2,000-8,000 tokens at session start
