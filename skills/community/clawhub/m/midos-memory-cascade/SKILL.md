---
name: midos-memory-cascade
description: Auto-escalating multi-tier memory search that cascades from in-memory cache through SQLite, grep, and LanceDB vector search to find the best answer with minimal latency.
metadata:
  {}
---

# MidOS Memory Cascade

A self-tuning, auto-escalating search engine that tries each memory tier from fastest to slowest, stopping as soon as it finds a high-confidence answer.

## What It Does

Instead of the agent deciding which storage layer to query, the cascade tries each tier automatically:

| Tier | Storage | Latency | Strategy |
|------|---------|---------|----------|
| T0 | In-memory session cache | <1ms | Exact + fuzzy key match |
| T1 | JSON state files | <5ms | Filename + key match |
| T2 | SQLite (pipeline_synergy.db) | <5ms | Structured SQL LIKE |
| T3 | SQLite FTS5 | <1ms | Full-text keyword on 22K rows |
| T4 | Grep over 46K chunks | ~3s | Brute-force ripgrep fallback |
| T5 | LanceDB keyword (BM25) | slow | 670K vector rows, no embeddings |
| T5b | LanceDB semantic | 3–30s | Embedding similarity, last resort |

**Question routing:** Queries starting with how/what/why/etc. skip keyword tiers and route directly to semantic search.

**Self-learning:** The cascade records which tier resolves each query. After enough history, `evolve()` learns shortcuts (skip directly to the winning tier) and marks consistently-empty tiers for skip.

## Usage

### Python API

```python
from tools.memory.memory_cascade import recall, store

# Search across all tiers
result = recall("adaptive alpha reranking")
# → {"answer": {...}, "tier": "T5:lancedb", "latency_ms": 340, "confidence": 0.87}

# Write to the right storage automatically
store("pattern", content="...", tags=["ml", "reranking"])
```

### CLI

```bash
# Search
python memory_cascade.py recall "query here"

# View tier resolution stats
python memory_cascade.py stats

# Run self-evolution (learn shortcuts + tier skips)
python memory_cascade.py evolve
```

### `recall()` Options

```python
recall(
    query: str,
    min_confidence: float = 0.5,  # stop escalating at this threshold
    max_tier: int = 6             # 0=T0 only, 6=all tiers
)
```

Returns:
```json
{
  "answer": { "source": "...", "text": "..." },
  "confidence": 0.87,
  "latency_ms": 340.2,
  "tiers_tried": 3,
  "resolved_at": "T5:lancedb",
  "shortcut": null,
  "question_routed": false,
  "escalation": [...]
}
```

## Requirements

- Python 3.10+ (stdlib only for core cascade logic)
- Optional: `hive_commons` for LanceDB tiers (T5/T5b)
- Optional: `tools.memory.memory_router` for `store()` routing

The cascade degrades gracefully — if LanceDB is unavailable, it stops at grep (T4). All stdlib tiers (T0–T4) work with zero dependencies.

## Architecture Notes

- **Thread-safe:** Session cache uses `threading.Lock`; stats writes use separate locks
- **Cross-process safe:** JSONL writes use OS-level file locking (`msvcrt` on Windows, `fcntl` on Unix)
- **Confidence scoring:** Term overlap × score × content richness → normalized 0–1
- **Stats persistence:** `knowledge/SYSTEM/cascade_stats.json` accumulates hit rates per tier

Built with MidOS. 1 of 200+ skills. Full ecosystem at midos.dev/pro
