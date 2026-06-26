# memory-lancedb-pro Full Technical Reference

## Database Schema

LanceDB table `memories`:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string (UUID) | Primary key |
| `text` | string | Memory text (FTS indexed) |
| `vector` | float[] | Embedding vector |
| `category` | string | `preference` / `fact` / `decision` / `entity` / `other` |
| `scope` | string | Scope identifier (e.g., `global`, `agent:main`) |
| `importance` | float | Importance score 0–1 |
| `timestamp` | int64 | Creation timestamp (ms) |
| `metadata` | string (JSON) | Extended metadata |

Common `metadata` keys in v1.1.0: `l0_abstract`, `l1_overview`, `l2_content`, `memory_category`, `tier`, `access_count`, `confidence`, `last_accessed_at`

---

## Source Code Structure (31 Files)

### Core Storage & Retrieval
- `store.ts` (30.6 KB) — Primary storage operations
- `retriever.ts` (34.3 KB) — Hybrid retrieval system
- `embedder.ts` (24.7 KB) — Embedding providers & LRU caching
- `chunker.ts` (7.7 KB) — Document segmentation

### Smart Features
- `smart-extractor.ts` (27.9 KB) — LLM-powered 6-category extraction
- `smart-metadata.ts` (13.4 KB) — Metadata management & contextual support
- `decay-engine.ts` (7.0 KB) — Weibull decay modeling
- `tier-manager.ts` (5.8 KB) — Three-tier promotion system
- `noise-filter.ts` (3.0 KB) — Quality filtering
- `noise-prototypes.ts` (5.8 KB) — Embedding-based noise detection

### Advanced Features
- `scopes.ts` (10.3 KB) — Multi-scope isolation & access control
- `access-tracker.ts` (10.5 KB) — Access metadata tracking
- `adaptive-retrieval.ts` (3.9 KB) — Intelligent retrieval triggering
- `reflection-store.ts` (20.8 KB) — Reflection storage & ranking
- `session-recovery.ts` (5.1 KB) — Session path resolution

### Infrastructure
- `llm-client.ts` (3.7 KB) — LLM integration (OpenAI-compatible)
- `extraction-prompts.ts` (8.2 KB) — Prompt templates
- `memory-categories.ts` (2.0 KB) — Classification system
- `tools.ts` (44.0 KB) — Utility functions
- `migrate.ts` (10.0 KB) — Data migration
- `memory-upgrader.ts` (12.6 KB) — Memory enhancement

### Reflection Subsystem
- `reflection-metadata.ts`, `reflection-event-store.ts`, `reflection-item-store.ts`
- `reflection-mapped-metadata.ts`, `reflection-ranking.ts`, `reflection-retry.ts`, `reflection-slices.ts`

### Governance
- `self-improvement-files.ts` (4.2 KB) — Learning tracking

---

## Retrieval Pipeline Details

### Hybrid Search Architecture
```
Query → Vector Embedding + BM25 → RRF Fusion → Rerank → Lifecycle Decay Boost → Length Norm → Filter
```

### Scoring Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `vectorWeight` | 0.7 | Semantic relevance contribution |
| `bm25Weight` | 0.3 | Keyword match contribution |
| `recencyHalfLifeDays` | 14 | Decay window for recency bonus |
| `recencyWeight` | 0.1 | Additive boost for newer entries |
| `timeDecayHalfLifeDays` | 60 | Multiplicative penalty for old entries |
| `lengthNormAnchor` | 500 | Reference length (chars) for normalization |
| `hardMinScore` | 0.35 | Final threshold post-reranking |
| `reinforcementFactor` | 0.5 | Access-based half-life extension |
| `maxHalfLifeMultiplier` | 3 | Max access reinforcement cap |

### Post-Retrieval Scoring Stages
1. **Recency Boost:** `boost = exp(-ageDays / halfLife) × weight`
2. **Importance Weighting:** `score × (0.7 + 0.3 × importance)`
3. **Length Normalization:** `1 / (1 + 0.5 × log₂(charLen/anchor))`
4. **Time Decay:** `score *= 0.5 + 0.5 × exp(-ageDays / effectiveHalfLife)`
5. **Cross-Encoder Reranking:** 60% API scores + 40% original fused scores
6. **MMR Diversity:** Demotes candidates with cosine similarity > 0.85

---

## Weibull Decay Model

### Formula
```
recency = exp(-lambda × daysSince^beta)
```

### Tier-Specific Parameters

| Tier | Beta | Behavior | Decay Floor |
|------|------|----------|------------|
| Core | 0.8 | Sub-exponential (gentle decline) | 0.9 |
| Working | 1.0 | Standard exponential | 0.7 |
| Peripheral | 1.3 | Super-exponential (rapid fade) | 0.5 |

### Half-Life Calculation
```
effectiveHL = baseHalfLife × exp(importance_coefficient × importance)
```

### Composite Decay Score
- Recency (40%): Time-based decay modulated by importance
- Frequency (30%): Logarithmic saturation of access count
- Intrinsic (30%): Importance × confidence product

---

## Embedding Configuration

### EmbeddingConfig Interface

| Option | Description |
|--------|-------------|
| `apiKey` | Single key or array for round-robin failover |
| `model` | Embedding model identifier |
| `baseURL` | Custom endpoint (optional) |
| `dimensions` | Vector size override |
| `taskQuery` / `taskPassage` | Task-specific parameters |
| `normalized` | Request normalized embeddings |
| `chunking` | Auto-chunk documents (enabled by default) |

### Caching
- LRU cache with 30-minute TTL
- Hit rate monitoring for performance

### Rate Limit Handling
- Automatic key rotation on 429/503 errors
- Attempts each key in pool before failure

---

## Document Chunking

### Default Parameters
- Maximum chunk size: 4,000 characters
- Overlap: 200 characters
- Minimum chunk: 200 characters
- Line limit: 50 lines per chunk

### Splitting Hierarchy
1. Line boundaries (if exceeding max lines)
2. Sentence endings (`.!?。！？`)
3. Newline boundaries
4. Whitespace (last space before limit)
5. Hard split (character limit)

### Smart Chunking (adaptive to model)
- Max chunk: 70% of model's context limit
- Overlap: 5% of model's context limit
- Minimum: 10% of model's context limit

---

## Smart Metadata System

### Three-Tier Content Fields
- `l0_abstract`: Concise summary
- `l1_overview`: Formatted bullet points
- `l2_content`: Full text

### Contextual Support Tracking
- Normalization: 20+ language variants → canonical labels
- Slice-based: Confirmation/contradiction counts (capped at 8 slices)
- Global strength: Evidence weighting across contexts

### Data Size Limits (Bounded Arrays)
- Sources: 20 items max
- History: 50 items max
- Relations: 16 items max
- Support contexts: 8 slices max

### Normalization Functions
- `clamp01()`: Constrains confidence 0–1
- `clampCount()`: Non-negative integers
- `normalizeTier()`: Validates tier types

---

## LLM Client Configuration

### LlmClientConfig Interface
- `apiKey`: Authentication credential
- `model`: LLM model identifier
- `baseURL` (optional): Custom endpoint
- `timeoutMs` (optional, default 30,000ms): Request timeout
- `log` (optional): Diagnostic callback

### API Integration Details
- System prompt: "You are a memory extraction assistant. Always respond with valid JSON only."
- Temperature: 0.1 (low randomness for deterministic extraction)
- Response parsing: Markdown fence extraction → balanced brace matching
- Error recovery: Network/empty/invalid JSON → logging + null return (graceful degradation)

---

## Noise Filter Details

### Built-in Noise Categories
1. **Agent Denials:** "I don't have information", "I wasn't able to find"
2. **Meta-Questions:** "Do you remember?", "你还记得" (Chinese)
3. **Session Boilerplate:** "hi", "hello", "good morning"
4. **Diagnostic Artifacts:** Synthetic summaries with "no explicit solution"
5. **Embedding-based Detection:** Cosine similarity ≥ 0.82 against noise prototype bank

### Automatic Learning
- Learns new noise prototypes when extraction yields zero memories
- New prototype deduplication threshold: 0.95 similarity
- Bank cap: 200 entries
- Degeneracy detection: Disables if prototypes become too similar (> 0.98)

---

## Adaptive Retrieval — Full Logic

### Skip Conditions
- Greetings: "hi", "hello", "good morning"
- Commands: Slash commands, git, npm, docker
- Affirmations: "yes", "okay", "thanks"
- Continuations: "go ahead", "proceed", "continue"
- System messages: Heartbeats, metadata prefixes
- Short queries: <5 chars OR <15 chars (English) / <6 chars (CJK) without "?"

### Force Retrieval Conditions
- Memory keywords: "remember", "recall", "forgot", "memory"
- Temporal: "last time", "before", "previously", "yesterday"
- Personal data: "my name", "my email", "my preference"
- Query patterns: "what did I", "did I tell", "did I say"
- CJK equivalents: "你记得", "之前"

### Query Normalization
- Strips metadata headers
- Removes OpenClaw cron wrappers: `[cron:jobId jobName]`
- Removes timestamp prefixes: `[Mon 2026-03-02 04:21 GMT+8]`

---

## Access Tracking & Reinforcement

### Metadata Tracked
- `accessCount`: Number of accesses (valid range: 0–10,000)
- `lastAccessedAt`: Timestamp of last access

### Debounced Write-Back
- Default timer: 5 seconds
- Synchronous in-memory accumulation
- Automatic queueing if writes arrive during flush

### Reinforcement Effect
- Frequently accessed memories decay more slowly
- Logarithmic curve applied to access counts
- Freshness decays exponentially over 30 days
- Diminishing returns: Additional accesses yield smaller extensions
- Configurable multiplier cap: `maxHalfLifeMultiplier` (default 3)

---

## Reflection Storage

### Storage Types
- `"event"`, `"item-invariant"`, `"item-derived"`, `"combined-legacy"`

### Importance Weighting
- Invariant items: 0.82
- Derived items: 0.78
- Combined legacy: 0.75
- Events: 0.55

### Retrieval Limits
- Max entries retrieved: 160 most recent per agent
- Returns: Up to 8 invariants, 10 derived items
- Max age: 14 days (derived), 60 days (mapped)

### Quality Scoring
- Range: 0.2 to 1.0
- Formula: `0.55 + min(6, n) × 0.075` (based on non-placeholder lines)

### Deduplication
- Default threshold: 0.97 similarity

---

## Package Information

- **Name:** memory-lancedb-pro
- **Version:** 1.1.0-beta.8
- **Type:** ES module
- **License:** MIT
- **Author:** win4r

### Core Dependencies
- `@lancedb/lancedb`: ^0.26.2
- `@sinclair/typebox`: 0.34.48
- `openai`: ^6.21.0

### Dev Dependencies
- `commander`: ^14.0.0
- `jiti`: ^2.6.0
- `typescript`: ^5.9.3
