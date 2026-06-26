# OpenAI-Compatible Protocol Rules

## Catalog probes
- `GET /models`

## Inference probes
- `POST /responses`
- `POST /chat/completions`

## What to record
- HTTP status
- latency
- response object type
- returned `model`
- token accounting fields
- presence of reasoning fields

## Multi-pool indicators
- `/models` returns many unrelated model families
- `owned_by` values mixed across many vendors
- both endpoint styles work but shape looks gateway-normalized

## Focused-route indicators
- narrow or coherent catalog
- endpoint support and metadata match expected behavior
- stable schema and latency
