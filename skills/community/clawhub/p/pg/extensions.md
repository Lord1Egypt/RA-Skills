# Extensions — Which One Solves This

`CREATE EXTENSION name;` installs into the current database only — every database needs its own. Some require `shared_preload_libraries` and a restart. `SELECT * FROM pg_available_extensions` lists what the server can install; managed platforms publish their own allowlist.

## By Problem

| Problem | Extension | Note |
|---|---|---|
| Which query is eating the server | `pg_stat_statements` | Preload + restart. Install this on day one on every server |
| Slow statements without knowing which | `auto_explain` | Preload; logs plans over a duration threshold |
| Substring and typo-tolerant search | `pg_trgm` | GIN or GiST trigram index; also powers `similarity()` |
| Vector similarity / embeddings | `pgvector` | HNSW and IVFFlat indexes |
| Mixing scalar equality into a GIN/GiST index | `btree_gin` / `btree_gist` | Required for `(tenant_id, tsvector)` and most exclusion constraints |
| Case-insensitive text column | `citext` | Behaviour follows the database collation; an expression index is more explicit |
| Hashing, HMAC, column encryption | `pgcrypto` | `gen_random_uuid()` is in core since 13 — no longer a reason to install it |
| Rebuild a bloated table online | `pg_repack` | Needs disk for a second copy and a brief exclusive lock at swap |
| Exact bloat measurement | `pgstattuple` | Full scan; `pgstattuple_approx` samples |
| Scheduled jobs inside the database | `pg_cron` | Preload; runs as a background worker, one schedule per database |
| Automated partition creation and retention | `pg_partman` | Pairs with pg_cron for rollover |
| Test an index before building it | `hypopg` | Hypothetical indexes visible to EXPLAIN only |
| Verify index/heap integrity | `amcheck` | Run after hardware incidents or storage migrations |
| Query another Postgres or a CSV file as a table | `postgres_fdw`, `file_fdw` | Push-down works for simple predicates; verify with EXPLAIN |
| Hierarchies and paths | `ltree` | Or a recursive CTE for occasional traversal |
| Key/value column | `hstore` | JSONB superseded it for new work; still fine where it exists |
| Geospatial | `postgis` | Its own discipline; upgrades are version-coupled and need planning |
| See what is in shared buffers | `pg_buffercache` | Diagnostic for "is my working set actually cached" |
| Warm the cache after a restart | `pg_prewarm` | Optional autoprewarm background worker |
| Crosstab / pivot | `tablefunc` | Or `FILTER (WHERE ...)` aggregates in plain SQL first |
| Audit trail for a compliance regime | `pgaudit` | Per-object and per-class logging |
| Anything else | Search `pg_available_extensions` before writing application code | The answer is often already installed |

## pgvector, Concretely

```sql
CREATE EXTENSION vector;
ALTER TABLE docs ADD COLUMN embedding vector(1536);
CREATE INDEX ON docs USING hnsw (embedding vector_cosine_ops);
```

- Match the operator class to the distance you query with: `vector_cosine_ops` for `<=>`, `vector_l2_ops` for `<->`, `vector_ip_ops` for `<#>`. A mismatch means the index is silently unused.
- **HNSW**: slower to build, more memory, better recall/latency, and usable immediately on an empty table. The default choice. Tune recall with `hnsw.ef_search` (default 40) at query time.
- **IVFFlat**: fast to build, needs representative data *before* the build. `lists ≈ rows / 1000` up to a million rows, `≈ sqrt(rows)` beyond; query with `ivfflat.probes ≈ sqrt(lists)`. Rebuild after the data distribution shifts.
- Indexes cap at 2000 dimensions for `vector`; `halfvec` doubles that at half the storage and slight precision loss.
- Filtered vector search (`WHERE tenant_id = ? ORDER BY embedding <=> ?`) is the hard case: the index returns k nearest overall, then the filter discards most of them. Partial indexes per high-cardinality filter, or a partitioned table, beat hoping.

## Operating Extensions

- Version them: `SELECT extname, extversion FROM pg_extension;` and upgrade explicitly with `ALTER EXTENSION x UPDATE;` after a server upgrade — binaries move, catalog definitions do not.
- `shared_preload_libraries` is a comma-separated list requiring a restart; adding one entry while forgetting the existing ones disables the rest. Read the current value first.
- Extensions that add background workers (pg_cron, timescaledb, pg_partman's worker) consume `max_worker_processes` slots and compete with parallel query workers.
- Trusted extensions (PostgreSQL >=13) can be installed by a non-superuser database owner; the useful ones (`pg_trgm`, `btree_gin`, `citext`, `hstore`, `ltree`, `pgcrypto`, `tablefunc`) are trusted, and `pg_stat_statements` is not.
- Every extension is a dependency at upgrade time: a major-version upgrade needs a compatible build of each one present *before* the upgrade starts (upgrade sequence in the upgrades guide).
- On managed platforms the allowlist is the constraint that decides architectures; check it before designing around `pg_cron` or `pg_repack` (differences per provider in the managed guide).
