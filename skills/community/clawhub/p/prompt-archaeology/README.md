# Prompt Archaeology

> An AI agent skill for excavating forgotten solutions, code snippets, and decisions from past conversation sessions — instead of re-solving problems from scratch.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Every AI session is a stratum — a sedimented layer of debugging, decision-making, and discovery. Over time, valuable artifacts sink below the surface: a one-liner that fixed a gnarly race condition, a config that satisfied a finicky build, the exact incantation that convinced a model to behave. Most agents never dig for these. **Prompt Archaeology** turns that history into a quarryable resource.

## What it gives you

- **Search strategies** — keyword, semantic-adjacent, temporal, and structural queries tuned for session transcripts.
- **Relevance scoring** — a transparent, composable ranking that surfaces the one session that actually matters (not just the one that mentions the term most).
- **Knowledge extraction patterns** — recipes for pulling *decisions* and *solutions* out of a wall of chat, not just matching text.
- **Deduplication** — collapse near-duplicate fixes across sessions into a single canonical answer.
- **`excavate.py`** — a standalone Python script that crawls session logs and markdown files, ranks them, and prints the buried artifacts. **Zero third-party dependencies** (stdlib only).

## The workflow in one breath

**Survey** what artifact you want → **Locate** it with multiple query passes → **Score** the finds with the composite ranker → **Extract** the minimal artifact (with citation) → **Deduplicate** before reporting.

## Quick start

```bash
git clone https://github.com/voronindenis5/prompt-archaeology.git
cd prompt-archaeology

# Basic keyword dig over a directory of session logs (.md/.txt/.json/.jsonl)
python3 scripts/excavate.py dig ./my-sessions --query "kafka consumer rebalance"

# Multiple terms, top 5, with per-signal score breakdown
python3 scripts/excavate.py dig ./my-sessions --query "rebalance retry backoff" --top 5 --explain

# Date window + dedup near-identical results
python3 scripts/excavate.py dig ./my-sessions \
  --query "connection pool exhaustion" \
  --after 2024-01-01 --before 2024-06-01 --dedup

# Dump just the extracted code blocks across matches
python3 scripts/excavate.py dig ./my-sessions --query "ffmpeg concatenate" --extract code
```

### Index once, query many

For large corpora, build an index and query it repeatedly:

```bash
python3 scripts/excavate.py index ./my-sessions --out sessions.idx
python3 scripts/excavate.py query sessions.idx --query "oauth refresh token" --top 3 --explain
```

### Programmatic use

```python
from excavate import ArchaeologyIndex

idx = ArchaeologyIndex()
idx.scan("./my-sessions")
for hit in idx.search("kafka rebalance", top=5, explain=True):
    print(hit.score, hit.path)
    print(hit.extraction)
```

## Why "archaeology"?

An archaeologist does not grep the desert for "pottery" and ship the first hit. They survey, triangulate, carefully extract, and catalog. This skill teaches the agent to do the same with its own past — because re-deriving a solution you already found is the most expensive way to be wrong.

## Repository layout

```
prompt-archaeology/
├── SKILL.md                          # The skill itself (Hermes/OpenClaw format)
├── README.md                         # You are here
├── LICENSE                           # MIT
├── references/
│   ├── search-strategies.md          # Locate-phase playbook
│   ├── relevance-scoring.md          # The math + how to retune weights
│   ├── extraction-patterns.md        # Fix/decision/command/rejection templates
│   ├── deduplication.md              # Exact, near-dup, and variant detection
│   └── cli-reference.md              # Every excavate.py flag
└── scripts/
    └── excavate.py                   # Stdlib-only searcher + ranker
```

## Reference docs

| Doc | What it covers |
|---|---|
| [`search-strategies.md`](references/search-strategies.md) | Query expansion, negation, temporal constraints, pass ordering |
| [`relevance-scoring.md`](references/relevance-scoring.md) | Composite score math, normalization, weight tuning |
| [`extraction-patterns.md`](references/extraction-patterns.md) | Minimal-artifact templates by artifact type |
| [`deduplication.md`](references/deduplication.md) | Exact / near-dup / variant detection in depth |
| [`cli-reference.md`](references/cli-reference.md) | Full `excavate.py` CLI reference |

## Requirements

- Python **3.8+** (uses only the standard library — no `pip install` needed)

## License

MIT © Denis Voronin
