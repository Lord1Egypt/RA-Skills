# 🧠 Memoria — Persistent Memory for OpenClaw

**Memory that thinks like you do.** Your AI assistant remembers what matters, forgets what doesn't, and gets better over time.

**SQLite-backed · Fully local · Zero cloud · 21 memory layers · Human-like architecture**

---

## ✨ What's New in v3.22.3

### 🔄 Continuous Learning — Layer 21 *(v3.22.0)*
Memoria no longer waits for end-of-session to learn. New real-time capture via `message_received` + `llm_output` hooks:
- **3 extraction modes**: periodic (every N turns), urgent (on user frustration/error), self-error (on assistant self-admission)
- **Cross-layer integration**: extracted facts go through the full pipeline (selective dedup → embed → graph → topics → observations → clusters → sync)
- **Smart dedup with agent_end**: avoids double LLM calls when continuous already captured
- 6 bugs fixed across 3 audit rounds (v3.22.0 → v3.22.1 → v3.22.3)
- **Node 24.x compatibility** — fixed CONTINUOUS_ENABLED TDZ crash on gateways with embedded Node 24.x

### 🔍 Deep Audit — 10+6 bugs found & fixed *(v3.21.0–v3.22.3)*
Full code audit revealed critical alignment issues:
- **Hebbian learning was 100% dead** — wrong column names since creation
- **Proactive revision never triggered** — searched for obsolete lifecycle state
- **storeFact() lost 6 columns** on INSERT
- **Concurrent extraction risk** and **buffer never cleared** in continuous learning
- All 21 layers now properly aligned with the actual database schema

### 🧩 Behavioral Patterns *(v3.19.0)*
Detects repeated similar facts and consolidates them into patterns.

### 🔗 Cross-Layer Connections *(v3.20.0)*
- **Feedback → Lifecycle**: facts recalled 5+ times with positive usefulness → auto-promoted to "settled"
- **Hebbian → Topics**: strong entity relations auto-organize topics into parent/child hierarchy
- **Lifecycle → Patterns**: confirmed patterns (5+ occurrences) → settled (never forgotten)

---

## ✨ Core Features

- **21 memory layers** — from text search to procedural memory, knowledge graphs, behavioral patterns, continuous learning, and cross-layer connections
- **Semantic vs Episodic** — durable knowledge decays slowly, dated events fade (like human memory)
- **Lifecycle management** — facts evolve: fresh → settled → dormant (not "mature/archived")
- **Observations** — living syntheses that evolve as new evidence appears
- **Fact Clusters** — entity-grouped summaries with tracked membership
- **Procedural memory** — captures "how to do things" with steps, gotchas, quality scores, and failure reasons
- **Behavioral patterns** — detects repeated preferences and consolidates them
- **Adaptive recall** — injects 2-12 facts based on context load
- **Hot Tier** — frequently accessed facts (5+ recalls) always recalled
- **Feedback loop** — usefulness/recall_count/used_count tracked per fact
- **Cross-layer connections** — feedback→lifecycle, hebbian→topics, lifecycle→patterns
- **Hebbian reinforcement** — knowledge graph relations strengthen on co-occurrence, decay when unused
- **Proactive revision** — settled facts get LLM review and potential update
- **Identity-aware** — parses SOUL.md/USER.md to prioritize relevant facts
- **Expertise specialization** — topic access frequency boosts recall
- **Provider-agnostic** — Ollama, LM Studio, OpenAI, OpenRouter, Anthropic
- **Fallback chain** — if primary LLM fails, next one takes over; if all fail, facts still stored
- **Zero config** — smart defaults, 60-second setup

---

## 🚀 Quick Install

### As Plugin (recommended)
```bash
openclaw plugins install memoria-plugin
```

### From Source (review code first)
```bash
cd ~/.openclaw/extensions
git clone https://github.com/Primo-Studio/openclaw-memoria.git memoria
cd memoria && npm install
```

> 💡 Configure after install via `bash ~/.openclaw/extensions/memoria/configure.sh`

### Minimal manual config

Add to `openclaw.json`:
```json
{
  "plugins": {
    "allow": ["memoria"],
    "entries": {
      "memoria": { "enabled": true }
    }
  }
}
```

Smart defaults: Ollama + gemma3:4b + nomic-embed-text-v2-moe (local, 0€).

See [INSTALL.md](INSTALL.md) for advanced options.

---

## 🏗️ Architecture — 21 Layers

```
┌──────────────────────────────────────────────────────┐
│                   MEMORIA v3.22.3                    │
├──────────────────────────────────────────────────────┤
│                                                      │
│  RECALL (before each response):                      │
│  Budget → Observations → Hybrid Search (FTS5+embed)  │
│  → Knowledge Graph → Topics → Context Tree           │
│  → Lifecycle mult × Expertise boost × Cluster penalty│
│  → Format + Inject                                   │
│                                                      │
│  CAPTURE (after each conversation):                  │
│  LLM Extract → Selective (dedup/contradiction)       │
│  → Embed → Graph → Hebbian → Topics → Observations  │
│  → Clusters → Patterns → Cross-layer connections     │
│  → Sync .md → Auto-regen                             │
│                                                      │
│  CONTINUOUS (real-time, during conversation):         │
│  message_received + llm_output → rolling buffer      │
│  → periodic/urgent/self-error triggers               │
│  → LLM Extract → same pipeline as CAPTURE            │
│                                                      │
│  LEARNING (background):                              │
│  Feedback (usefulness/recall/used) → Lifecycle       │
│  Hebbian (co-occurrence) → Topic hierarchy           │
│  Pattern detection → Consolidation                   │
│  Proactive revision → Fact evolution                 │
│                                                      │
├──────────────────────────────────────────────────────┤
│  SQLite (FTS5 + vectors) · No cloud required         │
└──────────────────────────────────────────────────────┘
```

### Layer Map

| # | Layer | File | LLM? | Purpose |
|---|-------|------|------|---------|
| 1 | SQLite Core + FTS5 | `db.ts` | ❌ | Storage, full-text search |
| 2 | Temporal Scoring | `scoring.ts` | ❌ | Decay, hot tier (5+ accesses) |
| 3 | Selective Memory | `selective.ts` | ✅ | Dedup, contradiction check |
| 4 | Embeddings + Hybrid | `embeddings.ts` | ❌ | Cosine similarity (embed only) |
| 5 | Knowledge Graph | `graph.ts` | ✅ | Entity/relation extraction |
| 6 | Context Tree | `context-tree.ts` | ❌ | Hierarchical organization |
| 7 | Adaptive Budget | `budget.ts` | ❌ | Auto-adjust facts injected |
| 8 | Emergent Topics | `topics.ts` | ✅ | Keyword extraction, topic naming |
| 9 | Observations | `observations.ts` | ✅ | Living syntheses from evidence |
| 10 | Fact Clusters | `fact-clusters.ts` | ✅ | Entity-grouped summaries |
| 11 | .md Sync + Regen | `sync.ts`, `md-regen.ts` | ❌ | Write facts to workspace files |
| 12 | Fallback Chain | `fallback.ts` | all | Ollama → OpenAI → LM Studio |
| 13 | Procedural Memory | `procedural.ts` | ✅ | How-to steps, quality, gotchas |
| 14 | Lifecycle | `lifecycle.ts` | ❌ | fresh → settled → dormant |
| 15 | Feedback Loop | `feedback.ts` | ❌ | usefulness, recall_count, used_count |
| 16 | Hebbian | `hebbian.ts` | ❌ | Strengthen co-occurring relations |
| 17 | Identity Parser | `identity-parser.ts` | ❌ | Parse SOUL.md/USER.md |
| 18 | Expertise | `expertise.ts` | ❌ | Topic access → recall boost |
| 19 | Proactive Revision | `revision.ts` | ✅ | Revise settled facts via LLM |
| 20 | Behavioral Patterns | `patterns.ts` | ✅ | Detect + consolidate repetitions |
| 21 | Continuous Learning | `index.ts` (hooks) | ✅ | Real-time capture during conversation |

**9 layers use LLM** via the Fallback Chain. **12 layers are pure algorithmic.**

For scoring formulas, decay rates, and detailed pipeline descriptions, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## ⚙️ Configuration

```json
{
  "autoRecall": true,
  "autoCapture": true,
  "recallLimit": 12,
  "captureMaxFacts": 8,
  "syncMd": true,

  "llm": {
    "provider": "ollama",
    "model": "gemma3:4b"
  },

  "embed": {
    "provider": "ollama",
    "model": "nomic-embed-text-v2-moe",
    "dimensions": 768
  },

  "fallback": [
    { "provider": "ollama", "model": "gemma3:4b" },
    { "provider": "lmstudio", "model": "auto" }
  ]
}
```

### Supported Providers

| Provider | LLM | Embeddings | Cost |
|----------|-----|------------|------|
| **Ollama** | ✅ | ✅ | Free (local) |
| **LM Studio** | ✅ | ✅ | Free (local) |
| **OpenAI** | ✅ | ✅ | ~$0.50/month |
| **OpenRouter** | ✅ | ✅ | Varies |
| **Anthropic** | ✅ | — | Varies |

---

## 📊 Benchmarks

Tested on LongMemEval-S (30 questions, 5 categories):

| Version | Accuracy | Retrieval | Key improvement |
|---------|----------|-----------|-----------------|
| v3.2.0 | 73% | 50% | Contradiction supersession + procedural |
| v3.3.0 | 75% | 43% | Query expansion + topic recall |
| v3.4.0 | 82% | 50% | Fact Clusters (multi-session +75%) |
| v3.5.0 | 82%+ | 50% | Feedback loop + cross-layer cascade |

> v3.14–3.21 benchmarks pending (Sol benchmark planned).

Detailed methodology and scripts in [benchmarks/](benchmarks/).

---

## 🗺️ Roadmap

| Version | Feature | Status |
|---------|---------|--------|
| v3.0–3.5 | Core layers (1-12): FTS5, scoring, selective, graph, topics, observations, clusters, feedback, cascade | ✅ Done |
| v3.6–3.7 | Identity-aware, lifecycle, hebbian, expertise, procedural | ✅ Done |
| v3.8–3.12 | Procedural quality (reflection, alternatives, gotchas), capture quality, error detection | ✅ Done |
| v3.14–3.17 | Smarter extraction, cluster-aware recall, security/packaging fixes | ✅ Done |
| v3.18 | Cluster members table, topic hierarchy with parent inference | ✅ Done |
| v3.19 | Behavioral pattern detection (Layer 20) | ✅ Done |
| v3.20 | Cross-layer connections (feedback→lifecycle, hebbian→topics, lifecycle→patterns) | ✅ Done |
| v3.21 | Deep audit: 10 bugs fixed, full type alignment, all 20 layers validated | ✅ Done |
| v3.22 | Layer 21: Continuous Learning (real-time capture) + 6 more bug fixes | ✅ Done |
| v3.23+ | Image memory, interest profiles, LCM bridge, Sol/Luna benchmarks | 🔜 Next |

---

## 📄 License

Apache License 2.0 — see [LICENSE](LICENSE).

Copyright 2026 Primo-Studio by Neto Pompeu.
