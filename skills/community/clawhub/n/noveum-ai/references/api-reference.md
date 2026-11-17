# API reference essentials

Base URL: `https://api.noveum.ai/api` (self-hosted deployments override; the SDK env var is
`NOVEUM_ENDPOINT`). Every request: `Authorization: Bearer $NOVEUM_API_KEY`. The key is
org-scoped — the org is inferred from it; do not pass org headers with API-key auth.

Authoritative schemas: the MCP server's tools (generated from the live OpenAPI spec) or
`https://noveum.ai/docs`. This file covers what an agent needs constantly.

## Ingest contract (what the SDK sends — also usable directly)

```
POST /v1/traces          body: { "traces": [ <Trace>, ... ] }   (max 1000/request)
POST /v1/traces/single   body: <Trace>
```

Minimal valid Trace:

```json
{ "name": "chat-request", "project": "<project>", "environment": "production",
  "start_time": "2026-07-16T00:00:00Z", "end_time": "2026-07-16T00:00:01Z",
  "duration_ms": 1000, "status": "ok", "span_count": 1,
  "sdk": { "name": "noveum-trace", "version": "1.x" },
  "spans": [ { "span_id": "s1", "trace_id": "t1", "name": "llm.call",
      "start_time": "2026-07-16T00:00:00Z", "end_time": "2026-07-16T00:00:01Z",
      "duration_ms": 1000, "status": "ok",
      "attributes": { "llm.model": "gpt-4o", "llm.provider": "openai",
                      "llm.input_tokens": 12, "llm.output_tokens": 30,
                      "llm.input.messages": "[...]", "llm.output.response": "..." } } ] }
```

Notes: the format is Noveum's own JSON (not OTLP). `project` auto-creates the project.
Ingest is async (returns job ids) — confirmation = querying the trace back, not the 2xx.

## Query traces (params live-validated)

```
GET /v1/traces?project=<p>&size=20&from=0&sort=start_time:desc      // metadata only — cheap
      &status=error&service_version=<v>&sessionId=<s>&userId=<u>
      &searchTerm=<q>&environment=<e>&span_count_lte=<n>
GET /v1/traces/:id                  // LARGE for span-heavy traces (~145 KB at 49 spans)
GET /v1/traces/:traceId/spans       // same — fetch via scripts/fetch_to_file.py
GET /v1/traces/filter-values        // facet values incl. serviceVersions; grows with org
GET /v1/traces/connection-status    // has this org ever connected telemetry
```

**`includeSpans=true` is a context hazard** — size scales with span_count, not trace
count (one 49-span trace ≈ 145 KB). Query metadata first, then fetch the few traces you
actually need to disk: `python scripts/fetch_to_file.py "/v1/traces/<id>" --out /tmp/t.json`.
See `context-safety.md` before any bulk read.

Response envelopes (live-verified): list →
`{ success, traces[], pagination{total, limit, offset, has_more}, timestamp }` (use
`pagination.has_more` + `from` to page); single trace → `{ success, data: <trace> }`
(note `data`, not `trace`); spans → `{ success, trace_id, spans[] }`. Note the asymmetry:
query params are camelCase (`includeSpans`, `sessionId`), while payload fields are
snake_case (`span_count`, `session_id` under `metadata`). `service_version` is the
literal string `"unknown"` when the app never set one. **Timestamps in trace/item bodies
are ClickHouse strings** (`"2025-11-23 19:55:18.591000000"`, no `T`, no zone) while
job/run objects use ISO-8601 — don't parse them with one format.

## Polling contract (memorize this)

Heavy work runs in background workers. After a kickoff POST returns an id, poll the
matching GET until a terminal status. Never call queued work "done".

| Work | Poll | Cadence | Terminal |
|---|---|---|---|
| ETL run | `GET /v1/etl-jobs/:id/runs` | 3s active / 15s idle | completed·failed·cancelled |
| Mapper codegen | `GET /v1/etl-jobs/:id/novaeval/:runId` | 2s (cap ~5m) | completed·failed·cancelled |
| Recommend scorers | `GET /v1/eval-jobs/recommend-scorers/:jobId` | 3s (cap ~5m) | completed·failed·cancelled |
| Eval run | `GET /v1/eval-jobs/:id/runs/:runId` | 3s active / 15s idle | completed·failed·cancelled |
| NovaPilot | `GET /v1/novapilot/reports?projectId=<p>&limit=5` (list — the by-id response inlines the full report on completion; see `context-safety.md` rule 7) | 5s | completed·failed |

## Credits & quotas (say the number before spending)

- Eval: 1 credit × items × premium(LLM-judge) scorers; rule-based scorers free; if any
  premium scorers are used, minimum 5 (else 400 `MIN_PREMIUM_SCORERS_REQUIRED`).
  Tell premium from free via `config.evaluationType` on `GET /v1/scorers` entries:
  `"llm-based"` = premium, `"rule-based"` = free (live-verified; rule-based-only jobs
  charge 0 and skip the min-5 rule).
- NovaPilot: per analyzed item (preview count via `POST /v1/novapilot/filter-preview`).
- Out of credits → 429 `CREDIT_QUOTA_EXCEEDED` (with `Retry-After`). Stop; tell the user.
  Buying credits is a human/dashboard action — never attempt it.
- Usage snapshot: `GET /v1/status` → `{ status, plan{key, period_*}, usage{spans_this_period,
  credits_used, rate_limit_*}, quotas{...} }` (live-validated shape) — also the cheapest
  "is my key valid" probe.

## Common errors

| Code | Meaning | Action |
|---|---|---|
| 401 | Bad/expired key | Ask the user for a valid key; never invent one |
| 403 `ORG_CONTEXT_MISMATCH` | Org header conflicts with the key's org | Drop the org override |
| 400 validation | Payload mismatch | Re-check against the live OpenAPI/MCP schema |
| 429 (rate limit vs credit) | Read the error code | Backoff vs stop-and-report |

## What this key CANNOT do (by design — don't try)

Create/rotate API keys, manage billing or buy credits, create organizations or manage
members, access another org's data. These are dashboard/human actions.
