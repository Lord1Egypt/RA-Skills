---
name: openclaw-memory-pro
version: 0.0.7
description: "Enhanced AI memory system — vector store, document-level MSA, knowledge graph, collision engine, executable skills, and closed-loop skill evolution."
tags:
  - memory
  - ai
  - second-brain
  - knowledge-graph
  - skills
metadata:
  openclaw:
    emoji: "🧬"
    requires:
      anyBins: ["python3"]
---

# OpenClaw Memory Pro System

An AI memory assistant that turns fragmented notes and conversations into searchable long-term memory, auto-distills actionable skills via a closed-loop feedback pipeline, and proactively reminds you.

## When to Use

| Goal | Command |
|------|---------|
| Store a memory | `memory-cli remember "Learned X today" --tag thought -i 0.8` |
| Assembled recall (skills + KG + evidence) | `memory-cli recall "X"` |
| Deep multi-hop reasoning | `memory-cli deep-recall "complex question"` |
| Inspiration collision (7 strategies) | `memory-cli collide` |
| Daily briefing | `memory-cli briefing` |
| List skills with utility stats | `memory-cli skills` |
| KG contradiction detection | `memory-cli contradictions` |
| KG blind spot scan | `memory-cli blindspots` |
| Thought threads | `memory-cli threads` |
| Skill feedback | `memory-cli skill-feedback <id> success` |

## When Not to Use

- For ephemeral throwaway messages that don't need persistence.
- For real-time streaming data (this is a batch/on-demand system).

## Architecture

```
Fragments --> [Ingest + Tag] --> Unified Corpus (Memora vectors + MSA documents)
                                        |
                              +---------+-----------+
                              v         v           v
                          [KG Weave] [Distill]  [Collide]
                          structural compression  novelty
                           _gain      _value      (1-5)
                              |         |           |
                              +----+----+-----+-----+
                                   |    v     |
                              [Skill Proposer]     <-- triggered when 2-of-3 scores pass
                                   v
                            [Skill Registry]       <-- utility tracking + feedback loop
                           (draft -> active -> deprecated)
                                   |
                         +---------+-----------+
                         v         v           v
                    [Question-   [Scheduled  [Nebius
                     Driven       Push]       Fine-
                     Recall]                  Tuning]
                         |
             +-----------+-----------+
             v           v           v
         [Skills]   [KG Relations] [Evidence]   <-- three-layer assembled output
             |
             v
        Use -> Feedback -> utility update -> low-utility auto-rewrite
```

## Subsystems

| Layer | Module | Role |
|-------|--------|------|
| **Corpus** | **Memora** | Primary vector store (nomic-embed-text, JSONL). All content enters here. |
| | **MSA** | Document-level storage for long text (>=100 words) or high importance (>=0.85). LLM-powered multi-hop interleave. |
| **Intelligence** | **Second Brain** | KG weaving, distillation, collision (7 strategies with attention focus + recency weighting). |
| | **Skill Proposer** | Auto-generates draft skills when 2-of-3 scores meet thresholds. |
| **Skill** | **Skill Registry** | Versioned skills with utility tracking, feedback loop, executable action bindings (prompt_template / tool_call / webhook). |
| **Training** | **Chronos** | Replay buffer, personality profile generation, training data export. |

## Ingestion Routing

- All content -> Memora (always)
- Long text (>=100 words) OR high importance (>=0.85) -> also MSA
- High importance (>=0.85) -> also Chronos
- Always writes daily log file
- Post-remember hooks: KG extraction, access tracking

## Recall

Three-layer assembled response with token budget control (default 4000 tokens):

1. **Skills** (score 1.0) — active skills matched by vector similarity, with executable prompts
2. **KG Relations** (score 0.9) — knowledge graph nodes + logical edges
3. **Evidence** (score 0.0-1.0) — Memora snippets + MSA documents

## Collision Engine

7 strategies with attention-aware anchor selection:
- RAG-based: Semantic Bridge, Dormant Revival, Temporal Echo, Chronos Cross-Ref, Digest Bridge
- KG-driven: Contradiction-Based, Blind Spot-Based

Before each round, extracts 3-5 focus keywords from recent memories. Anchor selection biased toward current focus topics with recency weighting.

## Requirements

- Python 3.9+
- macOS (Apple Silicon) or Linux
- LLM API key: OpenRouter (preferred) or xAI (fallback)

## Setup

See [setup.md](setup.md) for installation instructions.

## Source

GitHub: [FluffyAIcode/openclaw-memory-pro-system](https://github.com/FluffyAIcode/openclaw-memory-pro-system)
