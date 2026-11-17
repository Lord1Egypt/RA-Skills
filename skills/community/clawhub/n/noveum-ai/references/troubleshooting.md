# Troubleshooting

## No traces arriving

1. `python scripts/send_test_trace.py` — isolates key/endpoint/network from SDK issues.
   - 401 → wrong key (keys look like `nv_…`; the older `noveum_…` format also exists).
   - Connection error → check `NOVEUM_ENDPOINT`. It must be the API **base**
     (`https://api.noveum.ai/api`) — the SDK appends `/v1/traces` itself. A value ending
     in `/v1/traces` double-appends and 404s.
2. Test trace works but app traces missing → almost always **flush**: the batch thread
   (100 traces / 5s) didn't flush before process exit. Add
   `atexit.register(noveum_trace.shutdown)`.
3. Still nothing → `NOVEUM_DEBUG=true NOVEUM_LOG_LEVEL=DEBUG` and watch the SDK's send
   logs; `NOVEUM_DEV_MODE=true` to dump traces to `.noveum_trace_dev/` locally.

## Traces exist but are incomplete

- **No LLM spans:** calls bypass the integration. Grep for direct provider-SDK calls and
  wrap them (`integrate-openai-manual.md` §2).
- **No message content:** `capture_response(resp)` not called; or content deliberately not
  set — if that's a privacy decision, record it as an accepted gap.
- **Streaming calls missing tokens/TTFT:** use the streaming helpers, not a plain
  `trace_llm_call`.
- **No conversation grouping:** set `session_id` metadata / use thread helpers.
- **Voice: latency scorers all N/A:** LiveKit STT/TTS wrappers or Pipecat observer not
  installed — evals cannot measure what telemetry doesn't carry.

## SDK behavior gotchas

- `init()` is one-shot (second call no-ops) — `shutdown()` before re-configuring.
- If the SDK isn't initialized, tracing calls return no-op spans silently: code "works",
  nothing is sent. Check init actually ran in the entrypoint that serves traffic.
- Queue backpressure: at >1000 queued traces new ones are dropped with a `TransportError`;
  raise `transport_config={"max_queue_size": ...}` for high-throughput apps.
- Sampling: `tracing_config={"sample_rate": 0.1}` exists; default is 1.0.

## Platform-side

- ETL run completed but 0 items → mapper didn't match the trace shape; re-generate with
  representative `traceIds`, or smoke-test via `POST /v1/etl-jobs/run-mapper`.
- Eval run stuck `queued` → workers are queue-based; keep polling per the cadence table.
  Minutes-long queues can be normal; hours are not — tell the user to check org status.
- Dataset item content looks cut off mid-string → list views truncate some long columns
  **silently, with no marker** (`content`, `metadata`, `agent_response`, `system_prompt`,
  `conversation_context`). Read the single item (`GET .../items/:itemId` — returns full
  content) or stream the full list to disk with `scripts/fetch_to_file.py` — never
  `fullContent=true` inline on a list (see `context-safety.md`).
- 429s: rate-limit 429 → exponential backoff; `CREDIT_QUOTA_EXCEEDED` → stop, report.

## When stuck

Read `noveum://org-status` (MCP) or `GET /v1/status`; re-read the live docs
(`https://noveum.ai/docs`, `https://noveum.ai/agents.md`); then ask the user rather than
guessing — especially before anything that spends credits or edits code.
