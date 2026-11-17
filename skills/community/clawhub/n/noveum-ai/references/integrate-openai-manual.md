# Integrate: direct OpenAI / Anthropic / any LLM SDK (manual wrapping)

The noveum-trace SDK does **not** monkey-patch LLM clients and has **no decorators** —
tracing is explicit, via context managers. Every LLM call site must be wrapped; un-wrapped
calls produce zero telemetry.

## 1. Install and initialize

```bash
pip install noveum-trace
```

Initialize once at process startup (config falls back to env vars — prefer env in prod):

```python
import noveum_trace

noveum_trace.init(
    project="<NOVEUM_PROJECT>",          # or env NOVEUM_PROJECT
    # api_key from env NOVEUM_API_KEY — do not hardcode
    environment="production",            # or env NOVEUM_ENVIRONMENT
)
```

Env vars: `NOVEUM_API_KEY`, `NOVEUM_PROJECT`, `NOVEUM_ENVIRONMENT`,
`NOVEUM_ENDPOINT` (default `https://api.noveum.ai/api`), `NOVEUM_SERVICE_VERSION`
(set this to the app's release/commit — it powers version comparison and fix verification).

`init()` is idempotent: a second call silently no-ops. To re-configure, call
`noveum_trace.shutdown()` first.

## 2. Wrap each LLM call

```python
import noveum_trace

with noveum_trace.trace_llm_call(model="gpt-4o", provider="openai") as span:
    resp = client.chat.completions.create(model="gpt-4o", messages=messages)
    span.capture_response(resp)   # auto-extracts tokens, cost, finish_reason
```

`capture_response` understands OpenAI, Anthropic, and Google response objects. For other
providers set usage explicitly: `span.set_usage_attributes(input_tokens=…, output_tokens=…)`.

Also capture what was sent/received when the app's privacy policy allows it — evals need it:

```python
    span.set_attribute("llm.system_prompt", system_prompt)   # NovaPilot fixes depend on this
    span.set_attribute("llm.input.messages", json.dumps(messages))
    span.set_attribute("llm.output.response", resp.choices[0].message.content)
```

Custom business attributes are welcome (`span.set_attribute("txn_category", ...)`) and
power segmented analysis — but flag PII fields to the user before capturing them.

## 3. Group work into traces and label agents/tools

If no trace is active, each context manager auto-creates one. For multi-step requests,
create one trace per request/job so spans nest:

```python
with noveum_trace.trace_operation("handle-chat-request"):
    with noveum_trace.trace_agent_operation(agent_type="planner", operation="plan"):
        ...
    with noveum_trace.trace_llm_call(model="gpt-4o", provider="openai") as span:
        ...
```

For multi-turn conversations, group turns with the thread helpers
(`noveum_trace.create_thread`, `trace_thread_llm`) and set a per-conversation
`session_id` in trace metadata so the platform can reconstruct conversations across
requests. **In production data, almost no integration sets `session_id` — it is the most
common gap, and conversational scorers depend on it.** Do not skip this in
request-per-turn apps.

## 4. Streaming

A plain `trace_llm_call` around a streamed generator will not capture token deltas or
time-to-first-token. Use the streaming helpers:
`noveum_trace.trace_streaming` / `streaming_llm`, or
`create_openai_streaming_callback` / `create_anthropic_streaming_callback`.

## 5. Lifecycle — the #1 integration bug

Traces are batched on a background thread (batch size 100 / 5s timeout). Short-lived
processes (CLIs, cron jobs, serverless handlers, test runs) exit before the batch flushes
and **lose all traces**. Always ensure shutdown:

```python
import atexit
atexit.register(noveum_trace.shutdown)   # or call flush()/shutdown() explicitly
```

For FastAPI/long-running servers, initialize in the lifespan/startup hook and call
`noveum_trace.shutdown()` on shutdown. Per-request flushing is not needed.

## 6. Where to put the changes

- Init: the app's real entrypoint (not a random module import).
- Wrapping: every call site that hits an LLM. Find them all
  (`grep -rn "chat.completions.create\|messages.create\|generate_content"`), wrap each.
- Config: add the `NOVEUM_*` variables to `.env.example` (placeholders only, never real keys)
  and the deployment manifests the repo already uses.

Then proceed to `verify-traces.md` — integration is not done until verification passes.
