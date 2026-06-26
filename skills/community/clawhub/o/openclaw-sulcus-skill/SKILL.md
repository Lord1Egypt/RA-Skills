---
name: openclaw-sulcus-skill
description: "Equip your agent with Sulcus — thermodynamic memory with a knowledge graph. Full SIU pipeline: SIVU (quality gate) → SICU (classifier) → SILU (entity extraction) → SIRU (adaptive recall). Apache AGE knowledge graph. Multi-signal recall with learned scoring weights. Interaction-based decay. Reactive triggers. Guardrails (output + tool guard). Session-scoped memory. Temporal supersession."
author: "Digital Forge Studios"
version: "4.0.0"
metadata:
  openclaw:
    requires:
      plugins: [openclaw-sulcus]
    credentials:
      serverUrl:
        description: "Sulcus server URL (e.g., https://api.sulcus.ca). Required for cloud mode. Leave empty for local-only."
        required: false
      apiKey:
        description: "Sulcus API key. Used for memory storage, recall, and BGE-small-en-v1.5 embeddings. Get one at sulcus.ca. Required for cloud mode."
        required: false
    environment:
      SULCUS_SERVER_URL:
        description: "Mapped from config.serverUrl. Not required for local-only mode."
        required: false
      SULCUS_API_KEY:
        description: "Mapped from config.apiKey. Not required for local-only mode."
        required: false
      OPENCLAW_WORKSPACE:
        description: "OpenClaw workspace path. Used by opt-in history import. Defaults to ~/.openclaw/workspace."
        required: false
    dataFlows:
      - direction: local-only
        condition: "When serverUrl is NOT configured"
        destination: "~/.sulcus/data/ (local embedded PostgreSQL)"
        data: "Memory text, embeddings, search queries"
      - direction: outbound
        condition: "When serverUrl IS configured"
        destination: "Configured Sulcus server"
        data: "Memory text, metadata, search queries, session events, embedding requests"
        auth: "apiKey"
---

# Sulcus Memory Skill

Sulcus is a cognitive memory system for AI agents — not a simple key-value store. Every memory is automatically scored, classified, graph-linked, and subject to thermodynamic decay. The system learns what matters and keeps it accessible.

## Prerequisites

**Required plugin:** `openclaw-sulcus` (install via `openclaw plugin install openclaw-sulcus`)

**Two operating modes:**
- **Local-only (no credentials needed):** All memory stays in `~/.sulcus/data/`. Zero network calls. Requires native dylibs (`libsulcus_store`, `libsulcus_vectors`) or WASM fallback.
- **Cloud mode (requires serverUrl + apiKey):** Memories are stored on and recalled from the configured Sulcus server. Embedding (BGE-small-en-v1.5) uses the same `apiKey` — no separate credentials. Get a key at [sulcus.ca](https://sulcus.ca).

**No additional databases or infrastructure needed by the agent.** PostgreSQL, pgvector, and Apache AGE run server-side (managed by the Sulcus server). The plugin communicates via REST API.

## What Sulcus Is

- **Thermodynamic memory** — memories have heat that decays over time and interaction patterns. High-utility memories stay hot; irrelevant ones cool and disappear.
- **Apache AGE knowledge graph** — temporal graph over all stored memories. Entities and relationships are extracted automatically. Graph queries reveal connections across time.
- **SIU v2 pipeline** — every `memory_store` fires: SIVU (utility scoring) → SICU (type classification) → SILU (entity extraction) → AGE graph update → trigger evaluation.
- **Guardrails** — output guard intercepts agent messages for PII/preference violations before delivery; tool guard evaluates tool calls against stored objectives before execution.
- **Session-scoped memory** — ephemeral per-conversation scratch-pad, auto-purged on session end.
- **Temporal supersession** — when newer memories contradict older ones, the older ones are automatically marked and deprioritized.
- **Curator (sleep cycle)** — background process that reclassifies, consolidates, summarizes, and re-vectorizes memories. No manual cleanup needed.
- **Reactive triggers** — rules that fire automatically on memory events.
- **SIRU** — adaptive recall unit that learns per-namespace scoring weights from accumulated recall sessions.

## Memory Lifecycle

### Storing

```
memory_store(content, memory_type)
  → SIVU scores utility (0–1)
  → SICU classifies type (if not specified)
  → SILU extracts entities and relationships
  → AGE graph node created/updated
  → Triggers evaluated (on_store)
  → Memory persisted with heat, confidence, provenance
```

### Recalling

```
memory_recall(query, limit)
  → Semantic embedding search (pgvector)
  → Base score = similarity × sim_weight + heat × heat_weight
  → Keyword overlap boost (exact word matches)
  → Temporal proximity boost (time-referenced queries)
  → Namespace ownership boost (agent's own memories preferred)
  → Diversity filter (MMR-lite — near-duplicates dropped)
  → Temporal supersession penalty (50% on superseded items)
  → Recall-boost applied (heat += boost_delta, spaced repetition)
  → Triggers evaluated (on_recall)
  → Graph context available alongside results
```

### Automatic Context Injection

The plugin automatically injects relevant memories into every turn via `before_prompt_build` using a **multi-signal recall pipeline**:

```
User sends message
  → Signal 1: Semantic Search (query against memory embeddings)
  → Signal 2: Hot Context (top 5 highest-heat memories, no query needed)
  → Signal 3: Entity Context (graph neighbors of entities mentioned in message)
  → Signal 4: Profile (user preferences + facts, periodic refresh)
  → Dedup by memory ID across all signals
  → Diversity Filter (MMR-lite: prevents near-duplicate flooding)
  → Temporal Supersession (older conflicting memories penalized 50%)
  → Composite Scoring: Similarity (40%) + Heat (30%) + Recency (20%) + Source Boost (10%)
  → Token Budget Assembly: top-scored memories packed by heat descending
  → Injected via prependContext every turn
```

This replaces manual `memory_recall` for context loading. The agent doesn't need to search — the memory layer surfaces what matters automatically.

### Recall Pipeline Details

**Topic Shift Detection** — The plugin tracks topic tokens (Jaccard overlap) across turns. When the topic is stable (overlap ≥ 0.25), cached results are served instantly with zero API cost. When a topic shift is detected, fresh recall fires automatically. Hard TTL of 5 minutes ensures staleness doesn't accumulate.

**Bi-gram Re-ranking** — After vector recall, results are re-ranked using phrase-level Dice coefficient against the user's query. This captures multi-word phrase matches that unigram similarity misses. Max 40% score boost. Falls back to server order when no phrase signal exists.

**Graph-Hop Expansion** — On fresh recall, the top 2 vector results seed an AGE graph traversal. Direct neighbors (1-hop) with heat ≥ 0.2 are folded into the result set (capped at 4 neighbors). This surfaces memories that are *related* to relevant ones, not just similar. Fully graceful — graph failure never degrades vector recall.

**Query Expansion** — When vector search returns < 3 results, the entity graph is queried for synonym terms and directly-connected memories. A second vector search fires with the expanded query. Thin recall is rescued without user intervention.

**Diversity Filter (MMR-lite)** — After recall, near-duplicate memories are removed to prevent context flooding. Ensures a broader spread of unique, relevant information fits within the token budget.

**Polarity-Aware Profile** — Preference memories are classified as positive ("always", "prefers"), negative ("never", "avoid", "don't"), or neutral. The injected context separates these into `<do>` and `<dont>` directive blocks.

### Structured XML Context

The injected context block uses structured XML with typed sections:

```xml
<sulcus_context token_budget="4000" namespace="my-agent" memories="12">
  <directives>
    <do>
      <memory id="..." heat="85%" type="preference">User prefers TypeScript strict mode</memory>
    </do>
    <dont>
      <memory id="..." heat="72%" type="preference">Never use var declarations</memory>
    </dont>
  </directives>
  <profile>
    <memory id="..." heat="90%" type="fact" age="2d ago">Primary IDE is VS Code</memory>
  </profile>
  <knowledge>
    <memory id="..." heat="60%" type="semantic">Sulcus uses Apache AGE for graph</memory>
    <memory id="..." heat="45%" type="procedural">Deploy: build → test → push → notify</memory>
  </knowledge>
  <recent>
    <memory id="..." heat="30%" type="episodic" age="1h ago" stale="true">Checked logs on April 1</memory>
    <memory id="..." heat="20%" type="episodic" superseded="true">Old deploy process (superseded)</memory>
  </recent>
</sulcus_context>
```

Each `<memory>` element includes `type`, `heat`, `age`, and optionally `stale="true"` (memories >30 days old) and `superseded="true"` (memories contradicted by newer information). XML-escaped labels prevent structure breaks.

### Temporal Supersession

When newer memories contradict older ones, the system automatically identifies the superseded item using:
- **Negation markers** — explicit contradictions ("no longer", "not anymore", "replaced by")
- **Topic overlap** — high content similarity between two memories
- **Temporal recency** — the newer memory wins

Superseded memories receive a **50% score penalty** and are tagged with `superseded="true"` in the XML. They remain visible (providing historical context) but rank below current information. This replaces the older conflict detection system.

### Context Rebuild Post-Compaction

When context compaction fires (the model's context window is trimmed from ~150k to ~20k tokens), the plugin:

1. **`before_compaction`** — extracts full session knowledge (summary + key decisions + user intents) and stores them as semantic memories
2. **Next turn** — injects a rich Sulcus context rebuild (configurable token budget, default 4000, max 10000) so the agent regains its bearings from memory rather than degraded compacted context

This ensures continuity through context window resets. Configure with `contextRebuild.tokenBudget` (default 4000).

### Session Lifecycle Hooks

- **`before_prompt_build`** — auto-recall injection (main recall path)
- **`agent_end`** — SIVU auto-capture from conversation + session memory purge
- **`before_compaction`** — pre-compaction session capture + sets rebuild flag
- **`before_tool_call`** — tool guard evaluation (when enabled)
- **`llm_output`** — output guard scan + optional assistant capture
- **`message_sending`** — PII redaction delivery (reversible or replace)

## Memory Types — Choose Carefully

Decay rates differ significantly. Wrong type = memory disappears too fast or lingers too long.

| Type | Decay | Use For |
|---|---|---|
| `episodic` | Fast | Events, sessions, one-off observations |
| `semantic` | Slow | Concepts, relationships, domain knowledge |
| `preference` | Slower | User preferences, opinions, style choices |
| `fact` | Slow | Stable factual knowledge, ground truth |
| `procedural` | Slowest | How-tos, processes, workflows, playbooks |

**Best practices:**
- Store user preferences as `preference` — they survive long and surface reliably
- Store how-tos and processes as `procedural` — these should never decay quickly
- Store facts as `fact` — stable, slow decay, always available
- Use `episodic` for events and session context — fast decay is correct here
- Use `semantic` for domain concepts and relationships

## Auto-Capture

SIVU auto-capture runs on `agent_end` to mine the conversation for memory-worthy content. It passes user messages through the SIVU quality gate before storing.

**Correction detection:** When the user corrects the agent ("actually, that's wrong", "no, I meant..."), the auto-capture system detects the correction and heat-boosts related memories that were contradicted — surfacing them more prominently next turn.

**Assistant capture:** When `captureFromAssistant: true`, the plugin also captures assistant responses through the SIVU quality gate. Long responses are summarized before storage.

Config:
- `autoCapture: true` — enable auto-capture (default: `false`)
- `captureFromAssistant: true` — also capture assistant responses (default: `false`)

## Guardrails System

Guardrails are **disabled by default**. Enable them in plugin config under `guardrails`.

### Output Guard

Intercepts agent output **before delivery** and scans for:
- **PII patterns** — email addresses, phone numbers, SSNs, credit card numbers, IP addresses (built-in). Custom regex patterns supported.
- **Preference violations** — output contradicts stored negative preferences ("don't say X", "never do Y"). Fetched from the agent's memory namespace.

**Actions on violation:**
- `redact` (default for PII) — replaces matched spans with `[REDACTED]`. Reversible mode: stores a mapping so redactions can be undone.
- `replace` (default for preference violations) — replaces the entire output with a configurable message.
- `block` — cancels output delivery entirely.

**Audit trail** — every guard event is stored as an episodic memory and written to the inspect buffer (visible via `memory_inspect`).

**Fail modes:**
- `fail-open` (default) — if guard throws an error, output passes through
- `fail-closed` — if guard throws, output is blocked

```json
{
  "guardrails": {
    "outputGuard": {
      "enabled": true,
      "pii": {
        "enabled": true,
        "patterns": ["email", "phone", "ssn", "credit_card", "ip_address"],
        "onViolation": "redact",
        "reversible": true,
        "customPatterns": [
          { "name": "internal_id", "regex": "\\bINT-\\d{6}\\b" }
        ]
      },
      "preferenceViolation": {
        "enabled": true,
        "onViolation": "replace",
        "replacementMessage": "⚠️ I stopped myself — this output would violate a stored preference."
      },
      "failMode": "fail-open",
      "auditTrail": true
    }
  }
}
```

### Tool Guard

Evaluates tool calls **before execution** (`before_tool_call` hook). For sensitive tools, checks whether the call conflicts with stored objectives or user preferences.

**Three outcomes:**
1. `allow` — tool runs normally
2. `requireApproval` — pauses execution, presents the tool call + reason for human review
3. `block` — hard-blocks the tool call with a reason

**Severity levels:** `info`, `warning`, `critical`. The `requireApprovalThreshold` config controls which severity triggers `requireApproval`.

**Tool evaluation logic:**
- **Allowlist** — tools in the allowlist always pass immediately, no evaluation
- **Blocklist** — tools in the blocklist are always hard-blocked
- **Sensitive tools** — tools in `sensitiveTools` go through objective alignment check
- **Non-sensitive tools** — pass without evaluation

**Objective alignment check:** Searches agent memory for objectives and preferences related to the tool. If a stored preference explicitly prohibits the action ("never run shell commands", "don't modify files"), the call gets `critical` severity.

```json
{
  "guardrails": {
    "toolGuard": {
      "enabled": true,
      "sensitiveTools": ["exec", "write", "edit", "delete", "message"],
      "allowlist": ["memory_recall", "memory_store"],
      "blocklist": [],
      "objectiveCheck": true,
      "requireApprovalThreshold": "warning",
      "failMode": "fail-open",
      "auditTrail": true
    }
  }
}
```

### Checking Guardrail Status

Use `guardrail_status` to see what's active and what's been blocked:
- Active outputGuard/toolGuard config (enabled, patterns, actions)
- Cached negative preference count
- Last 5 blocked/flagged events with reasons

Use `memory_inspect` for the full debug view including last recall injection details.

## Session-Scoped Memory

Short-term scratch-pad for per-conversation context. Memories stored here are **automatically purged when the session ends** — they never accumulate in the main namespace.

**Use cases:**
- Intermediate reasoning steps you want to reference later in the same conversation
- User context that's only relevant to this exchange ("user is asking about X project today")
- Draft/work-in-progress notes

```
session_store(content="User is currently debugging a memory leak in service X", memory_type="episodic")
session_recall(query="what service is the user debugging")
```

Session memories are stored with high initial heat (0.95) so they surface immediately in the same turn. They're tracked by ID in a module-scope set and deleted on `agent_end`.

## SIRU — Adaptive Recall Unit

SIRU learns which memories are most useful for a given query by analyzing accumulated recall sessions, then replaces the default heuristic scoring with **per-namespace learned weights**.

### How SIRU Works

1. **Data Collection (automatic)** — Every recall session is logged to the server: query text, memory IDs selected, composite scores, signal sources, token budget vs actual usage, candidate counts.

2. **Training** — When ≥20 recall sessions have accumulated, trigger training:
   ```
   siu_retrain()  →  POST /api/v2/siu/retrain { "model": "siru" }
   ```

3. **Adaptive Scoring** — The plugin fetches learned weights every 30 minutes and uses them in composite scoring:

| Weight | Default | Controls |
|---|---|---|
| `similarity_weight` | 0.40 | Semantic similarity signal |
| `heat_weight` | 0.30 | Thermodynamic heat signal |
| `recency_weight` | 0.20 | Time since last update |
| `source_boost_semantic` | 0.00 | Boost for semantic search results |
| `source_boost_hot` | 0.05 | Boost for hot-context results |
| `source_boost_entity` | 0.10 | Boost for graph entity neighbors |
| `source_boost_profile` | 0.15 | Boost for preference + fact results |

4. **Fallback** — If no trained weights exist or server is unreachable, heuristic defaults are used.

### SIRU Feedback

Submit explicit feedback to accelerate SIRU training:
```
POST /api/v1/agent/recall-feedback
{ "session_id": 42, "signal": "helpful" }
```
Valid signals: `helpful`, `unhelpful`, `partial`. Feedback sessions are weighted more heavily during training.

## Trigger System

Triggers fire automatically on server-side memory events. Evaluate explicitly with `evaluate_triggers`.

**Events:** `on_store`, `on_recall`, `on_boost`, `on_decay`

**Actions:** `notify`, `boost`, `pin`, `tag`, `deprecate`, `webhook`, `chain`

## Curator (Sleep Cycle)

Background process that runs independently:
- **Reclassifies** memories where SICU confidence is low
- **Consolidates** near-duplicate memories (merges or deprecates)
- **Summarizes** clusters of episodic memories into semantic nodes
- **Re-vectorizes** memories whose embeddings are stale
- **Resolves conflicts** flagged by the supersession system

Runs on a schedule — no manual intervention needed. Use `consolidate` for manual cleanup.

## SILU Output Evaluation

SILU can act as a recursive LM supervisor — evaluating agent outputs against stored memories for alignment issues.

**What it checks:** Contradictions, preference drift, stale references, hallucination risk.

Enable in plugin config:
```json
{
  "hooks": {
    "llm_output_evaluation": { "enabled": true }
  }
}
```

When enabled, every LLM response is evaluated fire-and-forget. Misalignment findings are stored as episodic memories.

## sulcus.toml Config Layer

File-based configuration at `~/.sulcus/sulcus.toml` (or project-level). Provides defaults that the OpenClaw plugin config can override.

**Precedence: plugin config (openclaw.json) → sulcus.toml → built-in defaults**

Example `~/.sulcus/sulcus.toml`:
```toml
[recall]
tokenBudget = 6000
profileFrequency = 5
boostOnRecall = true

[decay]
mode = "hybrid"

[autoCapture]
enabled = true
captureFromAssistant = false

[contextRebuild]
enabled = true
tokenBudget = 6000

[guardrails.outputGuard]
enabled = false

[guardrails.toolGuard]
enabled = false
```

Supports `[sections]` which map to nested objects. Config values in `sulcus.toml` are the baseline; `openclaw.json` plugin config takes precedence.

## Tool Reference

### Core Memory Tools

| Tool | What It Does |
|---|---|
| `memory_store` | Store a memory. SIU pipeline (SIVU → SICU → SILU) fires automatically. |
| `memory_recall` | Semantic search with relevance weighting, diversity filter, and supersession. |
| `memory_get` | Fetch a specific memory by UUID. Returns full details including graph edges and metadata. (cloud only) |
| `memory_list` | Browse memories with pagination, type filter, sort by heat/date. (cloud only) |
| `memory_update` | Update content, type, pinned status, or heat on an existing memory in-place. Preserves graph edges. (cloud only) |
| `memory_delete` | Delete by ID. Optional SIVU training to reject similar content. |
| `memory_status` | Backend status, hot nodes, decay mode, curator state, recall quality metrics. |
| `memory_profile` | Rich memory health snapshot: type distribution, hot nodes, top preferences and facts. |
| `memory_namespace` | Switch the recall namespace at runtime. Useful for reading from project-specific or shared namespaces. |

### Session Memory Tools

| Tool | What It Does |
|---|---|
| `session_store` | Store ephemeral context for the current conversation only. Auto-purged on session end. |
| `session_recall` | Search only current session's memories (not prior sessions). |

### Diagnostic Tools

| Tool | What It Does |
|---|---|
| `memory_inspect` | Debug window: last recall injection details, last 10 guardrail events, blocked items. |
| `guardrail_status` | Active guardrail config, negative preference cache, last 5 blocked events. |

### SIU / Training Tools

| Tool | What It Does |
|---|---|
| `siu_label` | Classify text through SIU v2 — SIVU store/reject decision + SICU type classification. |
| `siu_status` | Check SIU v2 model availability, deployed versions, training signal statistics. |
| `siu_retrain` | Trigger async retrain of SIU v2 models from accumulated training signals. |
| `trigger_feedback` | Record feedback on a trigger fire for SITU training. |

### Maintenance Tools

| Tool | What It Does |
|---|---|
| `consolidate` | Merge and prune cold memories below a heat threshold. |
| `export_markdown` | Export all namespace memories as Markdown. |
| `import_markdown` | Import memories from a Markdown document. |
| `evaluate_triggers` | Evaluate reactive triggers against an event + context. |
| `evaluate_output` | (MCP) Evaluate LLM output against memory for semantic alignment. |

### Cross-Agent Tools (disabled by default)

| Tool | What It Does |
|---|---|
| `memory_share` | Share a memory with another agent's namespace. |
| `memory_cross_recall` | Search another agent's memories for cross-agent context. |

Enable both in plugin config:
```json
{
  "tools": {
    "memory_share": { "enabled": true },
    "memory_cross_recall": { "enabled": true }
  },
  "sharedNamespaces": ["agent-b"]
}
```

## Temporal Search

Search queries with time references are automatically enhanced. The server parses natural language time expressions and boosts memories from the matching time window.

**Supported:** yesterday, today, last week, this week, last month, N days ago, last monday/friday/etc., explicit YYYY-MM-DD dates.

```
memory_recall("what happened yesterday")   → +30% boost for memories from yesterday
memory_recall("deploy issues last week")   → boost for last week's memories
memory_recall("deploy the server")         → no time reference, pure semantic
```

Temporal search is **additive** — boosts, not filters. Most relevant content always surfaces.

For programmatic use:
```
memory_recall(query="deployment issues", time_from="2026-04-01T00:00:00Z", time_to="2026-04-07T23:59:59Z")
```

## Plugin Configuration

All fields in `openclaw.json` → `plugins.entries.openclaw-sulcus.config`:

### Connection

| Field | Type | Default | Description |
|---|---|---|---|
| `serverUrl` | string | — | Sulcus server URL (e.g., `https://api.sulcus.ca`). Leave empty for local-only mode. |
| `apiKey` | string | — | API key from [sulcus.ca](https://sulcus.ca). Required for cloud mode. |
| `agentId` | string | — | Agent identifier. |
| `namespace` | string | — | Memory namespace (usually same as agentId). Sanitized to lowercase, hyphen-normalized. |

### Recall Behavior

| Field | Type | Default | Description |
|---|---|---|---|
| `autoRecall` | boolean | `false` | Enable automatic multi-signal context injection via `before_prompt_build`. Opt-in. |
| `tokenBudget` | number | `4000` | Max tokens for injected context block. Increase to 8000+ for large-context models (Opus, Gemini). |
| `profileFrequency` | number | `10` | Refresh profile (preferences + facts) every N turns. Turn 1 always includes full profile. Lower = fresher but more API calls. |
| `boostOnRecall` | boolean | `true` | Apply spaced-repetition heat boost to recalled memories. |
| `maxRecallResults` | number | `5` | Max memories per search. |

### Auto-Capture

| Field | Type | Default | Description |
|---|---|---|---|
| `autoCapture` | boolean | `false` | Enable SIVU auto-capture on `agent_end` and compaction. Opt-in. |
| `captureFromAssistant` | boolean | `false` | Also capture assistant responses through SIVU quality gate. |

### Context Rebuild

| Field | Type | Default | Description |
|---|---|---|---|
| `contextRebuild.enabled` | boolean | `true` | Inject rich Sulcus context after compaction instead of relying on degraded compacted summary. |
| `contextRebuild.tokenBudget` | number | `4000` | Max tokens for post-compaction rebuild (max 10000). |

### SILU Output Evaluation

| Field | Type | Default | Description |
|---|---|---|---|
| `hooks.llm_output_evaluation.enabled` | boolean | `false` | Evaluate every LLM response against stored memories for alignment. |

### Guardrails

| Field | Type | Default | Description |
|---|---|---|---|
| `guardrails.outputGuard.enabled` | boolean | `false` | Enable output guard (PII + preference violation scanning). |
| `guardrails.outputGuard.pii.enabled` | boolean | `false` | Enable PII pattern scanning within output guard. |
| `guardrails.outputGuard.pii.patterns` | string[] | all built-in | Active PII patterns: `email`, `phone`, `ssn`, `credit_card`, `ip_address`. |
| `guardrails.outputGuard.pii.onViolation` | string | `"redact"` | Action on PII: `redact`, `replace`, or `block`. |
| `guardrails.outputGuard.pii.reversible` | boolean | `true` | Store redaction mapping for later reversal. |
| `guardrails.outputGuard.pii.customPatterns` | array | `[]` | Custom PII patterns: `[{ name, regex, replacement? }]`. |
| `guardrails.outputGuard.preferenceViolation.enabled` | boolean | `true` | Scan output against negative preferences. |
| `guardrails.outputGuard.preferenceViolation.onViolation` | string | `"replace"` | Action: `replace`, `warn`, or `block`. |
| `guardrails.outputGuard.preferenceViolation.replacementMessage` | string | built-in | Message to replace output with on preference violation. |
| `guardrails.outputGuard.failMode` | string | `"fail-open"` | `fail-open` (pass on error) or `fail-closed` (block on error). |
| `guardrails.outputGuard.auditTrail` | boolean | `true` | Store guard events as episodic memories. |
| `guardrails.toolGuard.enabled` | boolean | `false` | Enable tool guard (objective alignment check before sensitive tool calls). |
| `guardrails.toolGuard.sensitiveTools` | string[] | `["exec","write","edit","delete","message"]` | Tools that trigger objective alignment check. |
| `guardrails.toolGuard.allowlist` | string[] | `[]` | Tools that always pass without evaluation. |
| `guardrails.toolGuard.blocklist` | string[] | `[]` | Tools that are always blocked. |
| `guardrails.toolGuard.objectiveCheck` | boolean | `true` | Search memory for objectives before evaluating sensitive tools. |
| `guardrails.toolGuard.requireApprovalThreshold` | string | `"warning"` | Severity that triggers `requireApproval`: `info`, `warning`, or `critical`. |
| `guardrails.toolGuard.failMode` | string | `"fail-open"` | `fail-open` or `fail-closed`. |
| `guardrails.toolGuard.auditTrail` | boolean | `true` | Store tool guard events as episodic memories. |

### Other

| Field | Type | Default | Description |
|---|---|---|---|
| `importHistory` | boolean | `false` | One-time import of `MEMORY.md` and daily notes from OpenClaw workspace into Sulcus. Runs once then marks itself done. |
| `extractionHints` | object | — | Domain hints for SILU entity extraction. See **Extraction Hints** below. |

**⚠️ Critical: `hooks.allowPromptInjection` must be `true`** for `before_prompt_build` to inject context.

### Minimal working config (local-only, no network):
```json
{
  "plugins": {
    "entries": {
      "openclaw-sulcus": {
        "enabled": true,
        "config": {
          "agentId": "your-agent",
          "namespace": "your-agent"
        }
      }
    }
  }
}
```

### Cloud mode config (recommended):
```json
{
  "plugins": {
    "entries": {
      "openclaw-sulcus": {
        "enabled": true,
        "hooks": { "allowPromptInjection": true },
        "config": {
          "serverUrl": "https://api.sulcus.ca",
          "apiKey": "YOUR_API_KEY",
          "agentId": "your-agent",
          "namespace": "your-agent",
          "autoRecall": true,
          "autoCapture": true,
          "tokenBudget": 4000,
          "contextRebuild": {
            "enabled": true,
            "tokenBudget": 4000
          }
        }
      }
    }
  }
}
```

### Cloud mode with guardrails:
```json
{
  "plugins": {
    "entries": {
      "openclaw-sulcus": {
        "enabled": true,
        "hooks": { "allowPromptInjection": true },
        "config": {
          "serverUrl": "https://api.sulcus.ca",
          "apiKey": "YOUR_API_KEY",
          "agentId": "your-agent",
          "namespace": "your-agent",
          "autoRecall": true,
          "autoCapture": true,
          "tokenBudget": 4000,
          "guardrails": {
            "outputGuard": {
              "enabled": true,
              "pii": { "enabled": true, "onViolation": "redact" },
              "preferenceViolation": { "enabled": true, "onViolation": "replace" }
            },
            "toolGuard": {
              "enabled": true,
              "requireApprovalThreshold": "warning"
            }
          }
        }
      }
    }
  }
}
```

## Extraction Hints

Domain-specific hints guide SILU's entity extraction without overriding its judgment. Configure in plugin config:

```json
{
  "extractionHints": {
    "entity_types": ["person", "tool", "project", "service"],
    "focus_areas": ["infrastructure", "memory systems", "deployment"],
    "suppress_types": ["location"],
    "expected_type": "procedural",
    "context_note": "This agent manages cloud infrastructure and memory systems"
  }
}
```

| Field | Type | Description |
|---|---|---|
| `entity_types` | string[] | Entity types expected in this domain |
| `focus_areas` | string[] | Domain focus areas |
| `suppress_types` | string[] | Entity types to suppress (e.g., `["location"]` if irrelevant) |
| `expected_type` | string | Soft hint for expected memory type — SILU may override |
| `context_note` | string | Free-form context note (max 500 chars, injected verbatim into SILU prompt) |

All fields are optional. SILU uses hints as guidance, not commands — it overrides when content clearly indicates otherwise.

## Usage Patterns

### Start of session
Context is injected automatically via `before_prompt_build` when `autoRecall: true`. No manual recall needed — the multi-signal pipeline surfaces your most important memories every turn.

For explicit search when you need specific context:
```
memory_recall(query="[current task or project]", limit=5)
```

### Capturing preferences
```
memory_store(content="User prefers TypeScript strict mode", memory_type="preference")
```

### Capturing a process
```
memory_store(content="Deploy process: build → test → tag → push → notify #releases", memory_type="procedural")
```

### Session scratch-pad
```
session_store(content="User is debugging a race condition in the scheduler", memory_type="episodic")
session_recall(query="what bug is user debugging")
```

### Checking memory health
```
memory_profile()         # rich snapshot: hot nodes, preferences, facts, stats
memory_status()          # backend status, recall quality metrics
memory_inspect()         # debug: last recall injection + guardrail events
guardrail_status()       # guardrail config + blocked events
```

### Checking what SIU thinks of a piece of text
```
siu_label(text="User likes dark mode")
# Returns: { store: true, store_confidence: 0.84, memory_type: "preference" }
```

### Fetching and updating a memory
```
memory_list(memory_type="preference", sort_by="current_heat")
memory_get(id="uuid-of-memory")
memory_update(id="uuid", is_pinned=true, heat=0.9)
```

### Triggering SIRU retraining
```
siu_status()    # check if enough signals accumulated
siu_retrain()   # trigger async retrain
```

### Periodic cleanup
```
consolidate(min_heat=0.1)
```
Run occasionally to merge near-duplicates and prune cold noise.

## Server Recall Tuning

These fields are tuned server-side via `PATCH /api/v1/settings/thermo`:

| Field | Default | Effect |
|---|---|---|
| `recall.similarity_weight` | 0.7 | Weight for semantic similarity |
| `recall.heat_weight` | 0.3 | Weight for memory heat |
| `recall.keyword_weight` | 0.15 | Boost for exact word matches |
| `recall.temporal_max_boost` | 0.4 | Max boost for time-referenced queries |
| `recall.temporal_decay_days` | 7.0 | Days over which temporal boost decays |
| `recall.namespace_boost` | 0.1 | Boost for agent's own namespace memories |

## Recall Quality Metrics

The plugin tracks recall health metrics across the session, visible via `memory_status`:

| Metric | Description |
|---|---|
| `fresh_recalls` | Turns where a fresh API call was made (topic shifted) |
| `cache_hits` | Turns where cached recall was served (topic stable) |
| `total_items_served` | Cumulative recall items injected across all turns |
| `zero_result_turns` | Turns where recall returned nothing |
| `graph_hop_contrib` | Total graph-hop items folded into recall |
| `graph_hop_turns` | Turns with at least one graph-hop item |
| `avg_relevance` | Average heat of recalled items (proxy for relevance) |

## Interaction-Based Decay

Sulcus supports 3 decay modes (configured server-side):

- **Time-only** — classic: memory cools based on wall-clock time since last access
- **Interaction-only** — memories decay per agent interaction; great for high-frequency agents
- **Hybrid** (default) — combination of both; high-utility memories resist decay

High-utility memories (`procedural`, `fact`, high-SIVU score) decay slowly. Low-utility noise (`episodic`, low-SIVU) cools quickly and gets consolidated.

## Confidence Levels

Every memory carries a confidence level:

- `observed` (default) — directly observed fact or event
- `inferred` — derived from other memories or reasoning
- `asserted` — explicitly stated by user or system

## Troubleshooting

- **Plugin not responding** — ensure `openclaw-sulcus` is installed and enabled in `~/.openclaw/openclaw.json`. Run `openclaw gateway restart` after config changes.
- **No context injection** — check that `hooks.allowPromptInjection: true` is set. Without it, `before_prompt_build` can't inject.
- **No cloud sync** — `serverUrl` and `apiKey` required. Get a key at [sulcus.ca](https://sulcus.ca). Without them, plugin runs local-only.
- **Local mode** — `sulcus-local` binary manages embedded PostgreSQL. Check `memory_status` to confirm backend mode.
- **Memories not persisting** — verify namespace matches across sessions (`agentId` / `namespace` in config). Check that namespace isn't being sanitized to a different value.
- **Memories decaying too fast** — check decay mode via `memory_status`. Switch to `Hybrid` mode server-side, or use `procedural`/`fact` types for long-lived knowledge.
- **Superseded memories still appearing** — this is intentional. Superseded items carry `superseded="true"` and rank lower, but remain visible as historical context. Delete them with `memory_delete` if you want them gone entirely.
- **Guardrail blocking unexpected output** — check `guardrail_status` for active rules and `memory_inspect` for the last blocked event. Review stored negative preferences with `memory_list(memory_type="preference")`. Disable `preferenceViolation` in config if too aggressive.
- **Tool guard requiring approval too often** — raise `requireApprovalThreshold` from `warning` to `critical`, or add frequently-used tools to the `allowlist`.
- **Output guard not activating** — ensure `guardrails.outputGuard.enabled: true` AND `guardrails.outputGuard.pii.enabled: true` (PII sub-section is separately gated).
- **Session memories surviving after session end** — session memories are purged on `agent_end` hook. If the gateway was killed mid-session, they may persist. Use `memory_list` to find and delete any orphaned session memories.
- **Context too small / memories missing** — increase `tokenBudget` in plugin config. The default (4000 tokens) fits ~30 memories; increase to 8000+ for large-context models.
- **Profile not reflecting recent preferences** — lower `profileFrequency` in config (default: 10 turns). Set to 1 for always-fresh profile (more API calls).
- **Recall seems stale within a session** — the plugin detects topic shifts automatically. If Jaccard overlap drops below 0.25, fresh recall fires immediately. 5-minute hard TTL ensures refresh even within a stable topic. For immediate refresh, use explicit `memory_recall`.
- **High LLM cache-write costs** — verify plugin version ≥ 5.5.1. Earlier versions inject volatile relevance percentages and timestamps that bust the prompt cache on every turn. v5.5.1+ uses stable confidence bands and a recall TTL.
- **`memory_get`/`memory_list`/`memory_update` not available** — these require cloud backend (`serverUrl` + `apiKey` configured). They are not available in local-only mode.
- **SIU tools failing** — `siu_label`, `siu_status`, `siu_retrain` all require cloud backend. Check that `serverUrl` and `apiKey` are set.
- **Context not rebuilding after compaction** — ensure `contextRebuild.enabled` is not explicitly set to `false`. Check logs for `pre_compaction_capture` events. If the gateway was restarted between compaction and the next turn, the rebuild flag resets (this is correct behavior — the gateway restart itself is a fresh session).
- **Agent knocked offline after plugin update** — ensure the plugin version matches the server version. The plugin falls back gracefully on older servers but with reduced functionality.
