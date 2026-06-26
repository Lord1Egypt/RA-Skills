---
name: openclaw-mem
description: >
  Manage, optimize, and troubleshoot the OpenClaw memory system — MEMORY.md curation,
  daily logs (memory/YYYY-MM-DD.md), memory_search tuning, compaction survival,
  and vector/hybrid search configuration. Use this skill whenever the user mentions
  OpenClaw memory, MEMORY.md, daily logs, memory_search, memory_get, compaction flush,
  memory indexing, QMD, memory recall problems, "the agent forgot", context window issues,
  or wants to set up, debug, or improve how their OpenClaw agent remembers things.
  Also trigger when discussing memory plugins (Mem0, Supermemory, Cognee), embedding
  providers, memory file architecture, or memory search relevance tuning.
---

# OpenClaw Memory — Setup, Optimization & Troubleshooting

## Core Principle

OpenClaw memory is **plain Markdown on disk**. The files are the single source of truth.
The model only "remembers" what gets written to disk — nothing stays in RAM between sessions.
Memory search tools are provided by the active memory plugin (default: `memory-core`).

---

## 1. Memory Architecture (Two Layers)

### Layer 1: Daily Logs — `memory/YYYY-MM-DD.md`
- **Append-only** session notes, running context, events of the day.
- OpenClaw reads **today + yesterday** at session start.
- If someone says "remember this" → write it here immediately.
- These accumulate over time; old logs are searchable via `memory_search`.

### Layer 2: Long-Term Memory — `MEMORY.md`
- **Curated** durable facts: decisions, preferences, iron-law rules, project context.
- Loaded at session start in **private/main sessions only** (never in group contexts).
- If both `MEMORY.md` and `memory.md` exist, only `MEMORY.md` is loaded.
- **Keep it short** — anything not needed every session belongs in daily logs.
- Files over ~20,000 characters get truncated (`bootstrapMaxChars`).
- Combined bootstrap cap: ~150,000 characters across all workspace files.

### Workspace Layout
```
~/.openclaw/workspace/
├── MEMORY.md              # Long-term curated memory (main session only)
├── memory/
│   ├── 2026-03-17.md      # Today's daily log
│   ├── 2026-03-16.md      # Yesterday's log (also auto-loaded)
│   └── ...                # Older logs (searchable, not auto-loaded)
├── AGENTS.md              # Operating manual, boot sequence
├── SOUL.md                # Persona, tone, values
├── USER.md                # Human profile
└── TOOLS.md               # Environment-specific config
```

### What Goes Where

| Content Type | Destination | Why |
|---|---|---|
| Durable decisions & preferences | `MEMORY.md` | Loaded every session |
| Iron-law rules the agent must always follow | `MEMORY.md` | Survives compaction |
| Today's work notes, events, context | `memory/YYYY-MM-DD.md` | Append-only log |
| One-time instructions | Chat (or daily log) | Ephemeral by design |
| Behavioral rules | `AGENTS.md` or `SOUL.md` | Always in context |

---

## 2. Memory Tools

OpenClaw exposes two agent-facing tools:

### `memory_search` — Semantic Recall
- Searches across all indexed memory files (MEMORY.md + daily logs).
- Returns snippet text (~700 chars max), file path, line range, score.
- Uses hybrid search: **vector similarity + BM25 keyword matching**.
- Vector finds paraphrases ("deployment process" matches "how we ship code").
- BM25 finds exact tokens (IDs, env vars, error strings, code symbols).
- Results are ranked by weighted fusion: `finalScore = vectorWeight × vectorScore + textWeight × textScore`.

### `memory_get` — Targeted File Read
- Reads a specific memory file by path + optional line range.
- Degrades gracefully if file doesn't exist (returns empty text, no error).
- Use when you know exactly which file has the information.

### Best Practice: Make Retrieval Mandatory
Add this rule to `AGENTS.md`:
```
## Memory Protocol
- ALWAYS run memory_search before acting on tasks that reference past context.
- Do NOT guess from conversation history alone — check your notes.
```
Without this, the agent guesses instead of checking its memory files.

---

## 3. Compaction & Memory Flush

### The Problem
Long conversations fill the context window. When it hits the threshold, OpenClaw
**compacts** (summarizes/truncates) older messages. Anything only in the conversation
— including instructions typed in chat — can vanish.

### The Safety Net: Automatic Memory Flush
Before compaction fires, OpenClaw triggers a **silent agentic turn** that reminds
the model to write durable notes to disk.

**Default config:**
```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "reserveTokensFloor": 20000,
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 4000,
          "systemPrompt": "Session nearing compaction. Store durable memories now.",
          "prompt": "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store."
        }
      }
    }
  }
}
```

### Key Points
- **Soft threshold**: flush triggers at `contextWindow - reserveTokensFloor - softThresholdTokens`.
- **One flush per compaction cycle** (tracked in `sessions.json`).
- **Silent**: agent replies with `NO_REPLY` so user doesn't see it.
- **Requires writable workspace**: skipped if `workspaceAccess: "ro"` or `"none"`.
- Verify it's working: check config and ensure `memoryFlush.enabled = true` with enough buffer.

### Survival Rules
1. **Put durable rules in files, not chat.** MEMORY.md and AGENTS.md survive compaction.
2. **Verify memory flush is enabled** and has enough buffer to trigger.
3. **Make retrieval mandatory** via AGENTS.md rules.

---

## 4. Vector Memory Search Configuration

### Embedding Providers (auto-selection order)
1. `local` — if `memorySearch.local.modelPath` is configured + file exists
2. `openai` — if OpenAI API key is available
3. `gemini` — if Gemini API key is available
4. `voyage` — if Voyage API key is available
5. `mistral` — if Mistral API key is available
6. Disabled if none configured

Also supported: `ollama` (local/self-hosted, not auto-selected).

**Important:** Codex OAuth covers only chat/completions — it does NOT work for
embeddings. You need a separate API key for your embedding provider.

### Hybrid Search Config
```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "provider": "openai",
        "model": "text-embedding-3-small",
        "query": {
          "hybrid": true
        }
      }
    }
  }
}
```

### Indexing Details
- Chunks: ~400 token target, 80-token overlap.
- Storage: per-agent SQLite at `~/.openclaw/memory/<agentId>.sqlite`.
- File watcher: debounce 1.5s, re-indexes on change.
- Auto-reindex when provider/model/chunking params change.

---

## 5. Advanced: Post-Processing Pipeline

```
Vector + Keyword → Weighted Merge → Temporal Decay → Sort → MMR → Top-K Results
```

### Temporal Decay (Recency Boost)
Old notes can outrank recent ones by raw similarity. Enable decay to fix this:
- Applies exponential multiplier based on age.
- Today's note (score 0.82 × 1.00 = 0.82) beats a 148-day-old note (score 0.91 × 0.03 = 0.03).
- **When to enable:** months of daily notes where stale info outranks current context.

### MMR Re-Ranking (Diversity)
Near-duplicate daily logs can crowd out diverse results. MMR removes redundancy:
- Penalizes results too similar to already-selected ones.
- **When to enable:** `memory_search` returns redundant/near-duplicate snippets.

---

## 6. QMD Backend (Experimental)

For power users who want better search quality:

```json
{
  "memory": {
    "backend": "qmd",
    "citations": "auto",
    "qmd": {
      "includeDefaultMemory": true,
      "update": { "interval": "5m", "debounceMs": 15000 },
      "limits": { "maxResults": 6, "timeoutMs": 4000 },
      "paths": [
        { "name": "docs", "path": "~/notes", "pattern": "**/*.md" }
      ]
    }
  }
}
```

- QMD combines BM25 + vectors + reranking locally via Bun + node-llama-cpp.
- Requires separate install: `bun install -g https://github.com/tobi/qmd`.
- Falls back to builtin SQLite if QMD fails or is missing.
- First search may be slow (downloads GGUF models on first run).
- Session indexing available: `memory.qmd.sessions.enabled = true`.

---

## 7. Additional Memory Paths

Index files outside the default workspace:
```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "extraPaths": ["../team-docs", "/srv/shared-notes/overview.md"]
      }
    }
  }
}
```
- Directories scanned recursively for `.md` files.
- Symlinks ignored.
- Multimodal indexing (images/audio) available with Gemini Embedding 2.

---

## 8. Troubleshooting

### Diagnosis: Always Start Here
Run `/context list` in your OpenClaw session to check:
- Is `MEMORY.md` loading? If "missing" → not in context → zero effect.
- Is anything **TRUNCATED**? Files over 20,000 chars get cut.
- Do injected chars match raw chars? If not → content is being trimmed.

### Common Problems

| Symptom | Cause | Fix |
|---|---|---|
| Agent "forgot" a rule | Rule was in chat, not a file | Move to MEMORY.md or AGENTS.md |
| memory_search returns nothing | Embedding provider not configured | Set API key for openai/gemini/ollama |
| memory_search returns stale results | No temporal decay | Enable decay in memorySearch config |
| memory_search returns duplicates | No MMR re-ranking | Enable MMR diversity filter |
| MEMORY.md not loading | File too large or in group session | Trim file; check session type is private |
| 401 errors on search | Wrong/missing embedding API key | Set correct key (Codex OAuth won't work) |
| Agent loses context mid-conversation | Compaction wiped it | Enable memoryFlush; put rules in files |

### Health Check Checklist
1. `MEMORY.md` exists and is < 10,000 chars (ideal) or < 20,000 chars (max)
2. `memory/` directory exists with recent daily logs
3. `memoryFlush.enabled = true` in compaction config
4. Embedding provider is configured and API key is valid
5. `AGENTS.md` includes "search memory before acting" rule
6. Run `wc -c ~/.openclaw/workspace/*.md` to audit file sizes

---

## 9. Memory Plugins (External)

For users who need memory beyond the built-in system:

### Mem0 (`@mem0/openclaw-mem0`)
- Stores memory **outside** the context window → survives compaction.
- Auto-Capture: extracts facts from conversations automatically.
- Auto-Recall: injects relevant memories before every response.
- Separates long-term (user-scoped) and short-term (session-scoped) memory.
- Cloud or self-hosted (Ollama + Qdrant + any LLM).

### Cognee (Knowledge Graph)
- Adds **relational reasoning** to memory ("Alice manages auth team" → graph traversal).
- Scans memory files on startup, syncs after each session.
- Good for: cross-project context, "who should I talk to about X?" queries.
- Requires Docker for the Cognee server.

### Supermemory (`openclaw-supermemory`)
- Cloud-based persistent memory with user profiles.
- Custom container routing (work vs personal).
- No local infrastructure required.

---

## 10. Memory Maintenance Routine

### Weekly
- Review `MEMORY.md` — remove outdated facts, promote important daily-log entries.
- Check daily logs aren't growing excessively large.

### Monthly (Memory Distillation)
- Scan `memory/*.md` for recurring patterns and hard-won rules.
- Promote mature rules to `MEMORY.md` or to skill SKILL.md files.
- Archive old daily logs (> 30 days) if desired.

### Backup
```bash
cd ~/.openclaw/workspace
git init  # if not already
git add memory/ MEMORY.md
git commit -m "Memory backup $(date +%Y-%m-%d)"
```
**Exclude:** `~/.openclaw/credentials/` and `openclaw.json` (contain secrets).

---

## Quick Reference: File Priority

| File | Loaded When | Scope | Survives Compaction |
|---|---|---|---|
| `AGENTS.md` | Every session start | All sessions | ✅ Yes |
| `SOUL.md` | Every session start | All sessions | ✅ Yes |
| `MEMORY.md` | Session start (private only) | Main session | ✅ Yes |
| `memory/today.md` | Session start | Main session | ✅ Yes |
| `memory/yesterday.md` | Session start | Main session | ✅ Yes |
| `memory/older.md` | Via memory_search only | On-demand | ✅ Yes |
| Chat instructions | During conversation | Current context | ❌ No |
