# Hybrid Memory Stack Connections

| Layer | Purpose | Host | Port | Auth / Notes |
| ----- | ------- | ---- | ---- | ------------- |
| PostgreSQL (`facts`) | Durable fact store (structured) | `localhost` | `55432` | `postgres://oc_memory:***@localhost:55432/oc_facts` (pgvector enabled) |
| Redis (`state`) | Short-lived status / control plane | `localhost` | `56379` | No password by default; prefer TTL + namespaces (`state:<entity>:<attr>`) |
| Qdrant (`vectors`) | Semantic recall store | `localhost` | HTTP `6335`, gRPC `6336` | Default collection `oc_memory` (1536-dim cosine) |

## Environment file

All scripts/source expect `/home/va/.openclaw/workspace/infra/memory-stack/.env` (generated from `.env.example`).

```
POSTGRES_USER=oc_memory
POSTGRES_PASSWORD=...
POSTGRES_DB=oc_facts
POSTGRES_PORT=55432
REDIS_PORT=56379
QDRANT_HTTP_PORT=6335
QDRANT_GRPC_PORT=6336
```

Override with env vars before running scripts if needed:

```
export MEMORY_STACK_ROOT=/custom/path
export MEMORY_PG_URL=postgres://...
```

## Fact schema quick reference

```sql
CREATE TABLE facts (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  subject text NOT NULL,
  predicate text NOT NULL,
  object jsonb NOT NULL,
  source text,
  confidence real CHECK (confidence BETWEEN 0 AND 1),
  tags text[] DEFAULT '{}',
  embedding vector(1536),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);
```

## Redis key patterns

- `state:<entity>:<attribute>` → JSON or scalar string
- `state:lock:<topic>` → TTL-backed locks
- `state:session:<id>` → ephemeral session metadata

## Qdrant payload template

```json
{
  "points": [
    {
      "id": "uuid-or-int",
      "vector": [/* 1536 floats */],
      "payload": {
        "subject": "user:42",
        "kind": "memory",
        "text": "...",
        "tags": ["project", "preference"],
        "timestamp": "2026-03-18T18:55:00Z"
      }
    }
  ]
}
```
