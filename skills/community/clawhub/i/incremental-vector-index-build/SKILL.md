---
name: incremental-vector-index-build
description: Build or repair an incremental indexer that copies growing local data (SQLite transcripts, event tables) into a local vector database with a watermark, so an agent can retrieve history without carrying it in context. Covers the counter bug that makes a run add one row and idle, and the monotonic watermark trap.
version: 1.0.0
license: MIT
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Incremental vector index build

Goal: a background job that reads **only new rows** from a local source table and
embeds them into a local vector store, so an agent can retrieve relevant history
on demand instead of carrying it in every prompt.

Pick an **embedded, file-based store** (ChromaDB persistent client) over a
server-based one (pgvector/Postgres, Qdrant) when the index must be portable and
nobody wants to administer a database — an embedded store is just a directory of
files. Embeddings from a local model (for example Ollama `nomic-embed-text`)
keep the whole thing free.

## Build

1. **Read the source through a backup copy, not the live file.** Open SQLite with
   `file:<path>?mode=ro` and use `src.backup(dst)` into a temp file. Reading a
   live DB directly (especially from another tool) can be refused or can see a
   torn WAL view. Some external `sqlite3` binaries also refuse paths under an
   active state directory — copy out first, then read the copy.

2. **Write a stable point id.** Use a content hash, not Python `hash()` — the
   builtin is salted per process, so the same chunk gets a new id each run and the
   store fills with duplicates.

   ```python
   pid = f"{rowid}-" + hashlib.sha1(chunk.encode()).hexdigest()[:16]
   ```

   Stable across runs, so `upsert` is idempotent.

3. **Filter junk in SQL, not in Python.** Event tables are mostly rows with no
   usable text (tool results, statuses, NULL payloads). `WHERE event_json IS NOT
   NULL` still returns them. Filter on real content:

   ```sql
   AND event_json LIKE '%"type":"text"%' AND length(event_json) > 120
   ```

   Measure the filter's yield with a count query before a long run. In one real
   table, of ~43k rows only ~12k had text worth embedding.

4. **Batch the embedder and put vectors in explicitly.** One HTTP call per N
   chunks (`/api/embed` with an `input` list) is far faster than N calls. With
   ChromaDB >= 1.x, either implement `embed_documents`/`embed_query` on the
   embedding function **or** pass `embeddings=[...]` to `upsert` and skip the
   function entirely. A bare `__call__` alone fails `query` with
   `'...' object has no attribute 'embed_query'`.

## The accounting bug that makes it idle

5. **Keep two separate counters**: `added` = fragments added **this run**, and
   `count` = cumulative total stored. The stop condition compares the **per-run**
   counter to the limit.

   - Correct: `if added >= limit: break`
   - Broken: `if st["count"] + added >= limit: break` — with a persisted
     `count` (945) larger than the run `limit` (400), this is true on the
     **first** row, so the run adds **one** fragment and exits.

   Symptom: every run reports `added: 1` and the watermark never advances. Fix
   the comparison, and do not fold the run total into the cumulative `count`
   before the check.

6. **Persist the watermark monotonically**: `seen_row = max(seen_row, rowid)`,
   saved **after each batch**. Without `max`, a filtered pass can write a
   **smaller** watermark than before (observed 5873 -> 35), so the next run
   re-scans from near the start. Saving after each batch also means an interrupted
   run resumes instead of repeating.

## Drive it and verify it advances

7. **Detach the loop.** Start cleanup/setup with `setsid`. A `pkill -f <script>`
   in the same shell can kill the parent and the freshly started loop with it
   (observed: the loop died and left a 0-byte log). Relaunch with
   `nohup setsid ./loop.sh &` and confirm the pid is alive.

8. **Tolerate a bad parse.** A shell loop wrapping the indexer must not abort on
   one malformed JSON line. Treat a non-numeric `added` as a stop only when it is
   genuinely `0`.

9. **Completion check, not intent.** Run twice and confirm the second run's
   watermark is strictly **greater** and `added` is non-trivial (>1 with a
   backlog), or `added == 0` at true end-of-data. Then query the store:
   `collection.count()` rises, and `search("<real question>")` returns the
   expected fragment with a sensible score.

   Distinct gates: process started -> wrote rows -> store count rose -> semantic
   query returns the right item. Never report indexing as "running" or "done"
   from intent alone; inspect the process and the store count.

10. **Schedule the increment.** Point a cron or automation at the same script with
    a small `--limit` and the saved watermark, so only new rows are added.
    Idempotent ids mean a re-run costs time, not duplicates.

## What this does not solve

Embedding quality. If retrieval misses, the chunking and the filter are the first
suspects, not the vector store. Check what actually got embedded before tuning the
model.
