# LangSmith API Reference

Base URL: `https://api.smith.langchain.com`
Auth: `x-api-key: <LANGSMITH_API_KEY>` header

## Key Endpoints

### GET /runs
Fetch runs for a project.

Query params:
- `project_name` (string) — project name
- `start_time` (ISO 8601) — earliest start time
- `end_time` (ISO 8601) — latest start time
- `status` (string) — `error`, `success`, `pending`
- `limit` (int) — max results, default 20, max 100
- `offset` (int) — pagination

Response: `{ "runs": [...] }` or a list directly.

### GET /runs/{run_id}
Fetch a single run by ID.

## Run Object Schema

```json
{
  "id": "uuid",
  "name": "string",              // chain/agent name
  "run_type": "chain|llm|tool",
  "status": "success|error|pending",
  "start_time": "2024-01-01T00:00:00Z",
  "end_time": "2024-01-01T00:00:05Z",
  "latency": 5.0,                // seconds (may be absent)
  "total_tokens": 1234,
  "prompt_tokens": 800,
  "completion_tokens": 434,
  "inputs": {},                  // chain inputs (varies)
  "outputs": {},                 // chain outputs (varies)
  "error": "string or null",
  "feedback_stats": {
    "score": { "n": 10, "avg": 0.85 }
  },
  "tags": ["string"],
  "metadata": {}
}
```

## Pagination
Use `offset` to page through results. Max `limit` per request is typically 100.
For large fetches, loop with offset increments.

## Projects
List projects: `GET /sessions` → `{ "sessions": [{ "name": "...", "id": "..." }] }`

## Feedback
Post feedback: `POST /feedback`
```json
{
  "run_id": "uuid",
  "key": "score",
  "score": 0.9,
  "comment": "string"
}
```

## Notes
- Timestamps are ISO 8601 UTC
- `latency` field availability varies; calculate from `end_time - start_time` as fallback
- `total_tokens` is only populated for LLM runs, not chain-level runs
- For LangGraph: each node is a separate run with `parent_run_id` linking them
