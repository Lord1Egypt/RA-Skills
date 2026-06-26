# LiteRAG optimization playbook

Use this only when a specific library has a real problem: slow indexing, weak hits, too much noise, or bad result ordering.
Do not preload it by default.

## When to read this

Read this file when:

- indexing is too slow for a real corpus
- hybrid/vector/fts quality looks off
- a library needs corpus-specific chunking or ranking overrides
- a query family keeps missing obvious documents
- search works but the top hit ordering is dumb

## Tuning order

Do not random-walk through knobs.
Use this order:

1. Verify index health
2. Verify query shape
3. Benchmark before changing config
4. Change one family of knobs at a time
5. Reindex only when required
6. Benchmark again
7. Keep only changes that measurably help

## 1) Verify index health first

Run:

```bash
python scripts/literag-status.py <library>
python scripts/literag-meta.py <library>
```

Check:

- sqlite file exists
- document/chunk/embedding counts look sane
- `vector_backend` is what you expect
- compatibility flags are all true
- reindex warning is absent unless you intentionally changed config

If health is bad, fix that first. Do not tune retrieval on a broken index.

## 2) Classify the query problem

Most retrieval failures are one of these:

### A. Exact-term / API-name lookup

Examples:

- `bpy.types.Object constraints`
- `ThemeTextEditor cursor`
- class names, method names, property names, enum names

Bias toward:

- FTS health
- chunk boundaries around API sections
- lower chunk sizes for dense reference docs

### B. Conceptual lookup

Examples:

- `geometry nodes simulation zone`
- `how to parent without transform`
- `remote gateway pairing`

Bias toward:

- hybrid or vector retrieval
- better headings
- overlap and chunk size tuning

### C. Navigation/noise problem

Symptoms:

- top hits are `References`, nav pages, index pages, changelogs

Bias toward:

- `exclude`
- ranking penalties
- smaller, cleaner corpora

## 3) Benchmark before touching config

Use the benchmark tool with a fixed query set.

```bash
python scripts/literag-benchmark.py <library> \
  --query "query one" \
  --query "query two" \
  --warmup --repeat 3
```

What to compare:

- `fts` speed and exact hits
- `vector` semantic usefulness
- `hybrid` whether fusion actually beats either side

If hybrid is not clearly better for the target query family, do not assume it deserves the default crown.

## 4) Knobs that actually matter

### Chunking

Use chunking changes when:

- reference pages are too broad
- answers are split awkwardly
- headings are not aligning with the returned chunk

Main knobs:

- `chunking.maxChars`
- `chunking.overlapChars`
- `chunking.minChars`
- `chunking.preferHeadings`

Guidelines:

- API/reference docs: usually smaller chunks win
  - try `1600-2200` max chars
- narrative/manual docs: usually larger chunks win
  - try `2200-3200` max chars
- if related context is split too hard, increase overlap a bit
- if headings are meaningful, keep `preferHeadings: true`

### Retrieval

Main knobs:

- `retrieval.vector.topK`
- `retrieval.hybrid.ftsWeight`
- `retrieval.hybrid.vectorWeight`
- `retrieval.hybrid.rrfK`

Guidelines:

- exact API lookup: let FTS matter more
- conceptual search: let vector matter more
- if hybrid feels noisy, reduce `topK` or lower the weaker side's weight
- if hybrid misses good candidates from one side, increase that side's contribution first

### Ranking penalties

Use only when junk is crowding the top.

Main knobs:

- `ranking.referencesPenalty`
- `ranking.navigationPenalty`
- `ranking.tablePenalty`
- `ranking.headingTermBoost`
- `ranking.textTermBoost`

Guidelines:

- if `References` keeps floating up, increase `referencesPenalty`
- if nav/TOC pages dominate, increase `navigationPenalty`
- if giant table-like pages pollute results, increase `tablePenalty`
- if the right heading exists but ranks too low, bump `headingTermBoost` carefully

## 5) Indexing throughput tuning

Only do this when indexing speed is the problem.

Main knobs:

- `embedding.batchSize`
- `embedding.maxConcurrency`
- `embedding.timeoutMs`
- `embedding.maxRetries`
- `embedding.retryBackoffMs`
- CLI `--embedding-batch-size`

Guidelines:

- raise `embedding.batchSize` when the embedding backend handles larger requests well
- raise `embedding.maxConcurrency` only if the backend and machine can actually sustain it
- do not crank concurrency blindly; local endpoints can get slower when overloaded
- retries are for transient failures, not for hiding a fundamentally broken endpoint

## 6) Reindex rules

Full reindex is worth it when:

- chunking changed
- retrieval/ranking config changed enough to trigger warnings
- source layout changed dramatically
- you suspect stale/broken metadata

Do not full-reindex just because you changed benchmark queries.

## 7) Safe experiment pattern

Use this loop:

1. capture baseline benchmark
2. change one config family
3. run index/reindex as needed
4. rerun benchmark
5. keep or revert

If you change chunking and ranking and retrieval all at once, you learn nothing.

## Recommended mini-playbooks

### For API/reference corpora

Try first:

- smaller chunks
- stronger heading relevance
- slightly stronger FTS presence in hybrid
- penalties against `References` and nav junk

### For manuals and conceptual docs

Try first:

- larger chunks
- moderate overlap
- stronger vector contribution in hybrid
- less aggressive penalties

### For mixed corpora

Prefer splitting into separate libraries if one part is dense API reference and the other is prose manuals.
That is usually cleaner than torturing one config into serving both perfectly.

## Red flags

Stop and rethink if you are about to:

- tune against one pet query and call it optimization
- keep reindexing without saving before/after numbers
- crank concurrency until the embedding endpoint melts
- use hybrid by habit when FTS alone is already best
- keep junk documents instead of excluding them

## Bottom line

Optimize LiteRAG by evidence, not vibes.
Baseline first, change one thing, re-measure, keep only what wins.
