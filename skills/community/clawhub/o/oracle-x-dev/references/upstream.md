# Adding an upstream data source

## Go through `services/http_client.py`

Never `httpx` directly. Every helper below is wrapped in an observer that
records the outcome against a health category, and a call that skips the
wrapper is invisible to the LIVE badge — which means a dead provider reports as
healthy.

| Function | Use for |
|---|---|
| `get_json(url, *, params=None, headers=None, timeout=DEFAULT_TIMEOUT)` | ordinary JSON GET |
| `post_json(url, *, payload, headers=None, timeout=...)` | JSON-RPC and POST APIs; `payload` is untyped so a JSON-RPC *batch list* works |
| `get_text(url, *, headers, timeout, max_bytes=DEFAULT_MAX_BYTES)` | HTML — streamed, truncated at 2 MB, follows redirects |
| `get_text_impersonated(...)`, `get_json_impersonated(...)` | hosts that fingerprint TLS (curl_cffi, run in a thread) |
| `get_json_yahoo(url, *, params, headers, timeout)` | Yahoo's crumb + cookie session, reopened automatically on 401 |

Defaults: `DEFAULT_TIMEOUT = 10.0`, a `User-Agent` identifying Oracle-X. All of
them raise `httpx.HTTPStatusError` on a non-2xx and the usual transport
exceptions — the *caller* owns its fallback policy, because only the caller
knows whether a second provider exists.

## The observer

```python
def _observe(fetch):
    @functools.wraps(fetch)
    async def wrapper(url: str, *args, **kwargs):
        started = time.perf_counter()
        try:
            result = await fetch(url, *args, **kwargs)
        except BaseException as e:
            health.record_url(url, ok=False, error=e)
            raise
        health.record_url(url, ok=True, latency_ms=...)
        return result
    return wrapper
```

`record_url` resolves the host through `category_for_url`. **An unmapped host
is dropped silently** — no error, no warning, just a provider nobody is
watching.

## Mapping a new host

`backend/services/health_registry.py`, in order:

1. Add `"<registrable.domain>": "<category_key>"` to `_HOST_MAP`. Matching is
   longest-suffix-first, so `query1.finance.yahoo.com` can override a broader
   `yahoo.com` entry.
2. Add the provider's human name to that `Category`'s `providers` tuple in
   `CATEGORIES` — that tuple is what the health panel lists, so an unlisted
   provider is one the user cannot see failing.
3. Only if the new source represents a genuinely different loss, append a new
   `Category(key, label, critical, providers, stale_after_s=...)`.

Existing keys: `prices_crypto`, `stream`, `database`, `stocks`, `news`,
`onchain`, `macro`, `ai`.

Categories are grouped by **what the user loses**, not by vendor. "CoinGecko is
down" only means something to someone who knows what reads it; "Crypto Prices
degraded" means something to everyone. That is also why adding a category is
rarer than it looks — a new price provider joins `prices_crypto`, it does not
get a row of its own.

## Semantics worth knowing before you tune anything

- `critical=True` is what can turn the badge red. Reserve it for categories
  whose loss makes the app *wrong* rather than merely thinner.
- `DOWN_AFTER_FAILURES = 3`. One failure degrades; it takes three to go down.
- **429s never count toward down.** `is_rate_limited` classifies them as
  degraded, because a rate limit is a fact about our request rate, not about
  the provider's health.
- `stale_after_s=None` opts a category out of staleness entirely. Use it for
  demand-driven categories — `database`, `ai` — where silence means nobody
  asked rather than something broke.
- `summarize_error` deliberately strips hosts, URLs and keys. `/api/system/health`
  is public, so its `detail` field carries a failure class and nothing an
  attacker could use to map the backend.

## Non-HTTP sources

Anything that is not an HTTP call reports by hand:

```python
health.record("ai", ok=True)
```

That is how the LLM chain (`services/llm/client.py`) and the database wrapper
appear on the badge.
