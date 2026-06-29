---
name: llm-result-cache
description: Tiny dependency-free TTL cache that skips a repeat LLM/API call entirely when the same input recurs. Fixes a common cost leak in agents that re-score/re-analyze the same URL, document, or input across separate tasks.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# LLM Result Cache

If your agent scores, classifies, or analyzes inputs that recur across
different tasks (the same competitor URL showing up across multiple client
audits, the same document type, the same recurring question), you're paying
for the same LLM call over and over even though nothing changed. This is a
~100-line, dependency-free disk cache that skips the call entirely on a hit.

Built and verified in production: added to a website-audit tool where the
same handful of competitor sites kept recurring across many different
clients' audits. First call: ~10 seconds (real LLM scoring). Repeat call on
the same input: 0.0 seconds, zero API cost.

## Why not just use `functools.lru_cache`?

`lru_cache` is in-memory only — it resets every time your process restarts,
which is most of the time for a script-based agent. This persists to disk,
survives restarts, and expires entries after a TTL you choose (so stale
data doesn't get served forever — e.g. a competitor's website score from
3 months ago shouldn't still count as "fresh").

## Setup

```python
from llm_result_cache import ResultCache, cached

cache = ResultCache("my_cache.json", ttl_seconds=14*24*3600)  # 14 days

# Option A — decorator (simplest)
@cached(cache)
def score_url(url: str) -> dict:
    ...  # your expensive LLM call here, must return a dict

# Option B — manual control
def score_url(url: str) -> dict:
    hit = cache.get(url)
    if hit is not None:
        return hit
    result = {...}  # your expensive LLM call
    cache.set(url, result)
    return result
```

For a custom cache key (e.g. normalizing a URL, or hashing multiple inputs
together), pass `key_fn` to the decorator:

```python
@cached(cache, key_fn=lambda url, **kw: url.strip().lower().rstrip("/"))
def score_url(url: str) -> dict:
    ...
```

## Design notes

- **Bounded size**: caps at `max_entries` (default 500), evicting oldest
  entries first — won't grow unbounded over a long-running process.
- **A corrupted cache file is treated as empty, not fatal** — this is a
  cache, not a source of truth, so losing it is safe. (If you need the
  opposite behavior — treating unreadable data as a hard stop rather than
  "start fresh" — see the `ad-budget-governor` skill, where that distinction
  matters because it's tracking real money, not just saving an API call.)
- **Single-process only.** This reads/writes the whole JSON file on every
  call — fine for occasional caching, not a substitute for Redis/Memcached
  under real concurrent load.
