---
name: openclaw-memory-resilience
description: "Configure OpenClaw agent memory to survive compaction and session restarts. Use when: (1) setting up a new OpenClaw agent or workspace, (2) agents are forgetting instructions or context between sessions, (3) configuring the pre-compaction memory flush, (4) setting up the file archival pattern for memory/archive/, (5) diagnosing why an agent forgot something, or (6) tuning compaction headroom and context pruning. Covers Layer 1 (gateway compaction config) and Layer 3 (file architecture) of the three-layer memory defense."
---

# OpenClaw Memory Resilience

Covers the two highest-impact layers of memory durability for OpenClaw agents.

## The Four Memory Layers (quick reference)

| Layer | What it is | Survives compaction? |
|-------|-----------|---------------------|
| Bootstrap files (SOUL.md, AGENTS.md, etc.) | Injected from disk at every session start | Yes — reloaded from disk |
| Session transcript (JSONL on disk) | Conversation history | Lossy — summarized on compaction |
| LLM context window | What the model currently sees | No — fixed size, overflows |
| Retrieval index (memory_search / QMD) | Searchable index over memory files | Yes — rebuilt from files |

**Core rule:** If it's not written to a file, it doesn't exist after compaction.

## Three Failure Modes

- **Failure A** — Instruction only existed in conversation, never written to a file. Most common.
- **Failure B** — Compaction summarized it away. Lossy. Nuance lost.
- **Failure C** — Session pruning trimmed old tool results. Temporary, lossless.

Diagnostic: *Forgot a preference?* → Failure A. *Forgot what a tool returned?* → Failure C. *Forgot the whole thread?* → Failure B.

## Layer 1: Gateway Compaction Config

Apply via `gateway config.patch`. This is a global default — applies to all agents:

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "mode": "safeguard",
        "reserveTokensFloor": 40000,
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 4000,
          "systemPrompt": "Session nearing compaction. Store durable memories now.",
          "prompt": "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store."
        }
      },
      "contextPruning": {
        "mode": "cache-ttl",
        "ttl": "1h"
      }
    }
  }
}
```

See `references/config-explained.md` for why each value is set the way it is.

## Layer 3: File Architecture

See `references/file-architecture.md` for the full pattern — bootstrap files, daily notes, archival, and QMD indexing.

## Context Footer Standard

Add to every agent's SOUL.md. This gives you real-time visibility into context fill and compaction count — the single fastest way to know when to act before you hit the bad compaction path.

```markdown
## Context Management (Auto-Applied)
**Every response:** fetch live status via `session_status`, append footer: `🧠 [used]/[total] ([%]) | 🧹 [compactions]`
- Auto-clear: **85% context** OR **6 compactions**
- Warn: **70% context** OR **4 compactions**
- Before clearing: file critical info to memory, then reset
```

See `references/context-footer.md` for why this matters and how to tune the thresholds.

## Diagnosing Problems

Run `/context list` in any OpenClaw session to see:
- Which bootstrap files loaded and at what size
- Whether any files are TRUNCATED (over per-file limit)
- Total injected chars vs raw chars

If a file shows TRUNCATED: reduce it or raise `bootstrapMaxChars` in config.
If a file is missing entirely: check the workspace path in agent config.
