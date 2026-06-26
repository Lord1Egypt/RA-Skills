---
name: memory-hybrid-stack
description: Use this skill to read/write the hybrid memory stack (Postgres facts, Redis realtime state, Qdrant vector recall) that lives under `infra/memory-stack`. Provides shell helpers for SQL, key-value, and Qdrant HTTP calls plus schema/usage guidance. Trigger when the assistant needs durable facts, volatile status, or semantic recall beyond Markdown memory.
---

# Memory Hybrid Stack

## Overview
This stack splits agent memory across three stores:

1. **Postgres + pgvector (`facts`)** — structured, durable knowledge with optional embeddings.
2. **Redis (`state`)** — low-latency values that expire (locks, session flags, device status).
3. **Qdrant (`vectors`)** — semantic recall for long-form text chunks, keyed by collection `oc_memory`.

All services run via Docker Compose (`infra/memory-stack/docker-compose.yml`). Connection defaults live in `infra/memory-stack/.env`; scripts in this skill auto-source that file unless you override `MEMORY_STACK_ENV` / `MEMORY_STACK_ROOT`.

## Quick Start
1. Ensure the stack is running: `cd infra/memory-stack && docker compose ps` (all three should be `healthy`).
2. `cd skills/memory-hybrid-stack/scripts` or call scripts via absolute path.
3. Use the helper scripts listed below (they inject host/port/user from `.env`).
4. For schema/endpoint details, open `references/connection-map.md` when needed.

| Layer | Script | Purpose |
| ----- | ------ | ------- |
| Postgres facts | `scripts/facts_sql.sh` | Run SQL/psql with pgvector enabled |
| Redis state | `scripts/state_kv.sh` | Get/Set/Delete simple keys with optional TTL |
| Qdrant vectors | `scripts/qdrant_request.sh` | Make raw HTTP calls (`GET/POST/PUT/DELETE`) with inline JSON or `@file` payloads |

## Facts Layer (Postgres + pgvector)
- **Use when**: recording validated facts, relationships, high-confidence summaries, or when you need SQL joins/filtering.
- **Connection**: `postgres://oc_memory:…@localhost:55432/oc_facts`. Credentials auto-loaded from `.env`.

### Common operations

```bash
# Run ad-hoc SQL (string argument)
./scripts/facts_sql.sh "SELECT subject, object->>'value' AS value FROM facts WHERE tags @> ARRAY['preference'];"

# Pipe a multiline query
cat <<'SQL' | ./scripts/facts_sql.sh
INSERT INTO facts (subject, predicate, object, source, confidence, tags)
VALUES (
  'user:xiaobai',
  'prefers_language',
  jsonb_build_object('value', 'zh-CN'),
  'chat/2026-03-18',
  0.92,
  ARRAY['preference','language']
)
ON CONFLICT (subject, predicate)
DO UPDATE SET object = EXCLUDED.object, updated_at = now();
SQL
```

Tips:
- Store raw text inside `object` JSON, e.g. `{ "value": "...", "summary": "..." }`.
- Use `embedding` column when you already have a 1536-d vector (set via `UPDATE facts SET embedding = '[...]'::vector WHERE id = ...`).
- Always tag rows (`tags text[]`) so downstream filters are cheap.

## State Layer (Redis)
- **Use when**: caching short-lived context (current task, device status, throttles, locks).
- **Key pattern**: `state:<entity>:<attribute>`; keep payloads as JSON strings for readability.

### Commands
```bash
# Fetch
./scripts/state_kv.sh get state:user:xiaobai:current-task

# Set with 10-minute TTL
./scripts/state_kv.sh set state:user:xiaobai:current-task '{"summary":"researching", "started_at":"2026-03-18T19:00:00Z"}' 600

# Delete
./scripts/state_kv.sh del state:user:xiaobai:current-task
```

Guidelines:
- Keep TTLs short (seconds/minutes) unless the value is truly session-scoped.
- Use Redis for coordination (e.g., `state:lock:calendar-sync`) with low TTL to avoid deadlocks.

## Vector Layer (Qdrant)
- **Use when**: storing or retrieving semantic chunks that exceed Markdown recall.
- **Endpoints**: HTTP `http://localhost:6335`, gRPC `http://localhost:6336`.
- **Default collection**: `oc_memory` (1536-d cosine). Created via `scripts/init_qdrant.sh`.

### Helper usage
```bash
# Check collections
./scripts/qdrant_request.sh GET /collections

# Upsert points from a file
cat > /tmp/points.json <<'JSON'
{
  "points": [
    {
      "id": "memo-001",
      "vector": [/* 1536 floats */],
      "payload": {
        "subject": "user:xiaobai",
        "text": "Prefers in-depth, sourced answers.",
        "tags": ["preference"],
        "timestamp": "2026-03-18T19:05:00Z"
      }
    }
  ]
}
JSON
./scripts/qdrant_request.sh PUT /collections/oc_memory/points @/tmp/points.json

# Semantic search (vector or filter payload inline)
./scripts/qdrant_request.sh POST /collections/oc_memory/points/search '{
  "vector": [/* query vector */],
  "limit": 5,
  "with_payload": true,
  "filter": {"must": [{"key": "subject", "match": {"value": "user:xiaobai"}}]}
}'
```

Notes:
- The script accepts raw JSON strings or `@/path/file.json`.
- Generate embeddings via your preferred model (e.g., OpenAI `text-embedding-3-small`); ensure dimension = 1536.
- Keep payload timestamps (`timestamp`) to enforce recency filtering.

## Workflow Recommendations
1. **Ephemeral -> Durable**: log immediate events in Redis, then promote confirmed facts into Postgres/Qdrant.
2. **Fan-out writes**: when capturing a new preference, update Postgres (structured) and Qdrant (semantic search) in the same turn.
3. **Read order**: Redis (latest state) → Postgres (authoritative fact) → Qdrant (related context) → Markdown fallback.
4. **Tags & filters**: align `tags` (Postgres) with Qdrant payload keys so cross-store correlation is simple.

## Troubleshooting
- `docker compose ps` shows unhealthy containers → check host ports (stack uses 55432/56379/6335/6336 to avoid clashes with `ai-stack-*`).
- Scripts complain about missing `.env` → copy `.env.example` → `.env`, or set env vars manually.
- Qdrant health stuck on "starting" → ensure you rebuilt using `memory-qdrant:local` (curl installed) or adjust healthcheck.

## References
- [connection-map.md](references/connection-map.md) — Ports, schemas, payload templates, and key conventions.
