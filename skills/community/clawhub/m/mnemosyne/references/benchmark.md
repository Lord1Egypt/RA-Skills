# Benchmark Methodology

## Memory-Native Evaluation (80 queries, 11 systems)

Four query types: cross-session recall, temporal reasoning, conflict resolution, profile inference.

| System | nDCG@10 |
|---|---|
| Mnemosyne early version | 0.046 |
| Raw BM25 baseline | 0.185 |
| Embedding systems (Mem0, LlamaIndex, qwen-agent…) | 0.12–0.16 |
| **Mnemosyne (v6.3+)** | **0.238** |

## Key findings

- Retrieval ranking must be decoupled from memory importance (imp): importance decides what to store, not what ranks first.
- Chinese questions hit a bigram vocabulary gap vs answers; unigram fallback + stopword removal fixes it.
- True Okapi BM25 (k1=1.5, b=0.75) + sigmoid normalization into the compound-cue formula.

## Latency

- keyword search ~7ms (P50), hard budget < 50ms.
