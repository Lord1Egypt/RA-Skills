# Errors, Retries, and Rate Limits

Notion errors are well-shaped: a status, a `code`, and a `message` that usually names the offending field. Most wasted time comes from not reading the body.

**Contents:** [The Error Body](#the-error-body) · [Status by Layer](#status-by-layer) · [Error Codes Worth Recognizing](#error-codes-worth-recognizing) · [Rate Limits](#rate-limits) · [Retry Policy](#retry-policy) · [What Is Safe to Retry](#what-is-safe-to-retry) · [SDK Exceptions Hide the Body](#sdk-exceptions-hide-the-body) · [Debug Ladder](#debug-ladder)

## The Error Body

```json
{"object": "error", "status": 400, "code": "validation_error",
 "message": "body.properties.Status.status.name should be defined, instead was `undefined`."}
```

`message` names the path in your payload. Print it verbatim, always — summarizing it into "invalid request" throws away the diagnosis.

## Status by Layer

| Status | Layer | Meaning |
|---|---|---|
| 400 | Payload | Malformed JSON, wrong shape for a type, a read-only property, missing `Notion-Version` |
| 401 | Token | Invalid, revoked or rotated credential (`auth.md`) |
| 403 | Capability | The token is valid but the integration lacks the capability for this operation |
| 404 | Access | Not shared, wrong object type, or genuinely gone — in that order of likelihood (SKILL.md Rule 3) |
| 409 | Concurrency | A conflicting transaction on the same object; retry after a short delay |
| 429 | Pace | Over the rate limit; `Retry-After` in seconds |
| 502 / 503 / 504 | Notion | Transient upstream; retry with backoff |
| 500 | Notion | Retry once; if a specific payload reproduces it, the payload is usually pathological (huge rich text, deep nesting) |

## Error Codes Worth Recognizing

| `code` | Real cause | Move |
|---|---|---|
| `unauthorized` | Token wrong or revoked | `/v1/users/me` |
| `restricted_resource` | Capability missing for this operation | Capabilities table in `auth.md` |
| `object_not_found` | Not connected to the integration, far more often than deleted | Check connections before ids |
| `validation_error` | Shape, type, or a name that does not exist | Read `message`; re-read the schema |
| `invalid_json` | Malformed body — usually shell quoting in a curl one-liner | Send the body from a file |
| `invalid_request_url` / `invalid_request` | Endpoint does not exist on this API version, or wrong method | Endpoint map in `data-sources.md` |
| `missing_version` | `Notion-Version` header absent | Add it everywhere, not just here |
| `conflict_error` | Two writes to the same object at once | Serialize writes per object; retry |
| `rate_limited` | Over ~3 req/s | `Retry-After`, then fix the pacing |
| `internal_server_error` | Notion | Retry with backoff; escalate a reproducible one |

## Rate Limits

- **~3 requests per second per integration, averaged, with short bursts tolerated.** The budget belongs to the token, not to the process: your cron job, your migration and an interactive session all spend from it.
- A 429 carries `Retry-After` in seconds. Honour it exactly; sleeping less is how a 429 becomes a wall of 429s.
- Size limits produce 400, not 429: 500 KB request body, 2,000 characters per rich text object, 100 items per rich text array (SKILL.md Limits).
- The fix for repeated 429s is pacing, not retrying. A central token bucket at `rate_limit_rps` is the design; retry handles the exception (`bulk.md`).

## Retry Policy

```python
def request_with_retry(method, url, max_attempts=4, **kw):
    for attempt in range(max_attempts):
        r = http(method, url, **kw)
        if r.status_code == 429:
            sleep(float(r.headers.get("Retry-After", 2 ** attempt)))
            continue
        if r.status_code in (409, 500, 502, 503, 504):
            sleep((2 ** attempt) + random.uniform(0, 0.5))   # jitter, or workers resynchronize
            continue
        if r.status_code >= 400:
            raise NotionError(r.json())      # 400/401/403/404 never improve on retry
        return r
    raise NotionError(f"gave up after {max_attempts} attempts: {url}")
```

- **Never retry a 4xx other than 429 and 409.** A `validation_error` retried four times is four identical failures and four spent requests.
- Jitter is not optional with more than one worker: without it, retries land in the same millisecond forever.
- Cap attempts and raise with the last error body attached, so the failure list in `runs/<year>.md` carries the reason (`bulk.md`).

## What Is Safe to Retry

| Operation | Safe? | Why |
|---|---|---|
| Any GET / query | Yes | No side effect |
| `PATCH` a page or block | Yes | Idempotent — the same payload produces the same state |
| Archive / restore | Yes | Setting a state you already know |
| `POST /v1/pages` | **No** | A timeout may hide a success; retrying creates a duplicate. Filter on `external_id` first (SKILL.md Rule 6) |
| `PATCH .../children` (append) | **No** | The same blocks get appended twice; verify by reading the parent before retrying |
| `POST /v1/comments` | **No** | Duplicate comments, and there is no delete endpoint (`comments.md`) |
| File upload send | Depends | Re-sending a part is usually fine; re-attaching is not — check the target property first (`files.md`) |

Timeout is the dangerous case for every "No" above: the request may have succeeded. Read before you re-write.

## SDK Exceptions Hide the Body

Official clients raise a typed exception, and the `code`/`message` pair often ends up nested inside it or logged at a level nobody reads. Two habits:

- Catch the client's API error type and log `code` and `message` explicitly, not `str(e)`.
- When a failure resists diagnosis, reproduce it with raw HTTP and print the body. Five minutes with curl beats an hour reading a wrapper.

## Debug Ladder

Each rung is one request and eliminates a class:

1. `GET /v1/users/me` — token and version header.
2. `GET` the object by id — access. 404 here means connection, not payload (`auth.md`).
3. `GET` the schema — names, types, option lists (`databases.md`).
4. Query with no filter, `page_size: 1` — the source has rows and is reachable.
5. Send the write with one property only — isolates which field the 400 belongs to.
6. Add the rest back one at a time.

**When a failure took real digging**, write the cause and the fix where it will be found again: a wrong property name or a stale option list goes into `~/Clawic/data/notion-api-integration/schemas/<data-source>.md`; a workspace-specific quirk goes into `## Gotchas` in `memory.md`; a payload that finally worked goes into `artifacts/query-<what>.md` with its `## Boxes` line, in the same turn.
