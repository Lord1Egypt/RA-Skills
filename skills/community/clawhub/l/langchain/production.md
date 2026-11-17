# Production — Limits, Caching, Concurrency, Deployment

## Timeouts And Retries

- Set `timeout` on the model client always. A provider that stops responding otherwise holds the request until the HTTP client's own default, and a worker with it.
- Worst-case latency for one step ≈ `timeout × (client max_retries + 1)` plus backoff. With `timeout=30, max_retries=2` that is 90 s+ before your chain has done anything else — size the caller's timeout accordingly, or it will give up while the retry is still in flight.
- Count layers (SKILL.md Core Rule 4): client retries for transport and 429, `.with_retry` for parse and validation failures, and never both for the same class.
- Retry only idempotent work. A retried tool call that charges a card charges twice; put idempotency keys in the tool, not in the chain.

## Rate Limiting

```python
from langchain_core.rate_limiters import InMemoryRateLimiter
limiter = InMemoryRateLimiter(requests_per_second=5, check_every_n_seconds=0.1, max_bucket_size=10)
model = ChatOpenAI(model="…", rate_limiter=limiter)
```

- The limiter throttles requests, not tokens — a token-per-minute limit needs a smaller `requests_per_second` than the request limit alone suggests.
- `InMemoryRateLimiter` is per process. With N workers the effective rate is N × the configured value; either divide by the worker count or use a shared limiter backed by Redis.
- Pair with `max_concurrency` in batch config: the limiter smooths the rate, the concurrency cap bounds simultaneous in-flight requests.
- A 429 storm is usually one unbounded `.batch()`. Fix the caller before raising the quota.

## Caching

```python
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
set_llm_cache(SQLiteCache(database_path=".langchain.db"))
```

- The cache key is the exact prompt plus the model parameters: one extra space, a different temperature, or a timestamp injected into the system prompt makes every request a miss. Keep volatile values out of the prompt.
- Best fit: development loops, test suites, and repeated identical system prompts. Worst fit: personalized prompts, where the hit rate is near zero and the lookup is pure overhead.
- Provider-side prompt caching is a different mechanism and often the bigger win for long fixed prefixes (`prompt-caching` skill).
- Cached responses skip the provider entirely, so they also skip its usage accounting — a cache hit reports no tokens, which is correct but breaks naive dashboards.

## Concurrency And The Event Loop

- One blocking call in an async handler stalls every coroutine on that loop. Sync-only tools and lambdas need an `afunc` or `run_in_executor`.
- Runnables are stateless and safe to share across requests; build models, retrievers, and chains once at startup and reuse them. Rebuilding a retriever per request dominates p99 (SKILL.md Traps).
- Long agent runs do not belong in an HTTP request. Hand them to a worker queue, return a run id, and stream or poll the result — with a checkpointer the run survives a redeploy.
- Cancel on client disconnect. An abandoned generation keeps billing until the provider finishes.

## Deployment Shapes

| Shape | Fits | Watch |
|---|---|---|
| Script / batch job | Offline processing, evals | Checkpoint progress; a 6-hour job that dies at hour 5 must resume |
| FastAPI service | Interactive apps | Async path throughout, streaming responses, singletons at startup |
| Worker queue | Long agent runs, ingestion | Idempotency, visibility timeouts longer than the worst-case run |
| Serverless | Spiky low-volume traffic | Cold starts, per-invocation import cost, in-memory caches and rate limiters that never warm up, execution-time caps below agent worst case |
| Managed platform | Teams wanting persistence and scheduling without owning it | Cost model and lock-in on the state store |

## Configuration And Secrets

- Keys come from the environment (`OPENAI_API_KEY`, …). Never in `config.yaml`, never in `metadata` or `tags`, never in a prompt (SKILL.md Configuration).
- Read the env at startup and fail loudly if a key is missing — a missing key otherwise surfaces as an authentication error deep inside a chain during the first real request.
- Pin every langchain package in the lockfile and upgrade them together (SKILL.md Core Rule 9). Floating versions turn a routine deploy into an import error at 3am.

## Security

Prompt injection, tool blast radius, pickle deserialization, output sinks, multi-tenant isolation, and PII in traces → `security.md`. Secrets handling for the deployment itself stays above.

## Pre-Deploy Gate

SKILL.md Output Gates plus:

- Rate limiter sized for the worker count; batch calls bounded by `max_concurrency`?
- Models, retrievers, and chains constructed at startup, not per request?
- Cost per conversation measured at expected traffic, not cost per call?
- Dependencies pinned; the deployed lockfile is the tested lockfile?
