# Observability — Callbacks, Tracing, Tokens, Cost

## Callbacks: The Inheritance Rule

- **Request-time** (`chain.invoke(x, config={"callbacks": [h], "tags": ["prod"], "metadata": {"user": uid}})`) — inherited by every child runnable. This is what you want in almost every case.
- **Constructor** (`ChatOpenAI(callbacks=[h])`) — applies to that object only, and does NOT reach its children. The classic surprise: a handler attached to the model sees model events but nothing about the retriever in the same chain.
- Handler methods (`on_llm_new_token`, `on_tool_start`, `on_chain_error`, …) are called synchronously in the run path: slow handler, slow chain. Use `AsyncCallbackHandler` on the async path and ship anything expensive to a queue.
- An exception inside a handler can take down the run. Wrap handler bodies defensively.
- On Python ≤3.10 async, callbacks reach children only if `config` is threaded through custom functions (SKILL.md Core Rule 8).

## Tracing

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=...
export LANGSMITH_PROJECT=my-app-prod      # per environment, not one shared project
```

- Older code uses `LANGCHAIN_TRACING_V2` / `LANGCHAIN_API_KEY`; both names appear in the wild, they configure the same thing.
- Tracing is off unless the env var is set, and it fails silently when the key is wrong — verify one run appears before assuming instrumentation works.
- Name your runs: `.with_config(run_name="retrieve")`. A trace of forty `RunnableSequence` nodes is unreadable; a trace of named steps is a debugger.
- Tag by environment and version, and put the user/session id in `metadata` — that is what makes "show me every failing run for this customer since the deploy" a query instead of an archaeology project.
- `@traceable` traces plain functions that are not runnables, so the non-LangChain half of a request appears in the same trace.
- Set `tracing: otel` in config when the org standard is OpenTelemetry; the alternative to a vendor backend is not "no tracing", it is spans in your existing collector.

## Privacy In Traces

Traces are the highest-value PII sink in the app — full prompts, retrieved documents, tool arguments. What to mask, where to mask it, and how `trace_pii` gates all of it → `security.md`.

## Token Accounting

```python
resp = model.invoke("hi")
resp.usage_metadata          # {'input_tokens': …, 'output_tokens': …, 'total_tokens': …}
```

- `usage_metadata` on the AIMessage is the provider's own count — authoritative. Local estimates with a tokenizer are for pre-flight budgeting only.
- Streaming responses omit usage unless the client is told to include it (`stream_usage=True` on clients that support it); otherwise the last chunk carries no counts and your accounting silently reads zero.
- For a whole chain or agent run, accumulate with a usage-collecting callback handler rather than summing by hand — intermediate steps are where the tokens actually go.
- Cached input tokens are reported separately by providers that support caching; count them at the cached rate or your cost model will be wrong in the safe direction only by accident.
- Reasoning models bill hidden reasoning tokens as output: the visible answer is a fraction of what you pay for.

## What To Actually Monitor

| Signal | Why |
|---|---|
| p50/p95 latency, split first-token vs total | A streaming regression shows up in first-token only |
| Tokens per request, and per step for agents | The quadratic growth (SKILL.md) appears here first |
| Cost per conversation, not per call | The per-call number always looks acceptable |
| Steps per agent run, and rate of hitting `recursion_limit` | A rising tail means a tool started failing |
| Tool error rate by tool | One broken tool inflates every other metric |
| Structured-output parse failure rate | Silent quality regression after a model change |
| Retrieval empty-result rate | Empty context reaches the model as an invitation to hallucinate |

Alert on the derivatives (cost per conversation, parse failure rate), not on raw volume.

## Feedback And Evaluation Loops

Log a run id with every response so a thumbs-down maps back to an exact trace, and attach user feedback to it. Runs that failed in production are the only dataset that matters — export them into your test fixtures instead of inventing test cases.
