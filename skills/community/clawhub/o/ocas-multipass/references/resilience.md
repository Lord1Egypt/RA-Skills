# Resilience

What to do when things fail. Read this file when anything goes wrong.

## Circuit breakers

LLMs in execution loops exhibit predictable failure patterns. These circuit breakers are mandatory. Workers must check them before every action.

### The dead endpoint rule

Before making any network call, check `log.jsonl` for the same URL+method combination. If it appears with a failure status 2 or more times, the endpoint is dead for this session. Do not call it again.

```
check: grep log.jsonl for {url}+{method} with status=failed
if count >= 2: skip, log "circuit breaker: endpoint dead after 2 failures"
```

### The variation trap

These are NOT different actions:
- Same URL with different `User-Agent` header
- Same URL with `www.` prepended or removed
- Same URL with query params reordered
- Same API call with different whitespace in the JSON body
- Same endpoint called after a `sleep`

If the URL and method match a failed call, it's the same action regardless of cosmetic changes.

### The folk theory trap

These are NOT valid reasoning:
- "The server might be busy, let me try again in a minute"
- "Maybe the data hasn't propagated yet"
- "It could be a race condition, let me slow down"
- "The previous request might have warmed up the cache"
- "Let me try without the trailing slash"
- "Maybe I need to hit the endpoint first to initialize it"
- "The API might need time to process my signup"

All of these are the agent inventing causal stories to justify retrying a failed action. When an action fails: **it failed.** Log the error, move to the next option.

The only exception is the mechanical retry logic in §Retry (3 attempts with backoff for transient 5xx/429 errors). After 3 attempts, it's done.

### Wait budget

| Wait type | Maximum | Purpose |
|-----------|---------|---------|
| Retry backoff | 5 seconds | Transient error recovery |
| Email poll interval | 10 seconds | Waiting for verification email |
| Email poll total | 2 minutes | Total time waiting for one email |
| Any other wait | 0 seconds | Not permitted |

If a worker pauses longer than 10 seconds outside email polling, it's stalling. Treat as worker failure.

### Attempt budget

| Scope | Maximum | After budget exhausted |
|-------|---------|----------------------|
| Single endpoint | 2 failures | Endpoint is dead |
| Single service | 3 failures across endpoints | Service is dead |
| Single capability gap | 5 candidates | Gap is unsolvable, report it |
| Entire task | 3 approach pivots | Produce failure report |

### Action deduplication

Every worker checks `log.jsonl` before performing an action:

```
normalize: lowercase(url) + method
search: log.jsonl for matching entries with status=failed
if matches >= threshold: skip
```

This prevents the most common LLM loop: trying the same failing action 10+ times with slight variations.

### What "move on" means

When a circuit breaker fires:
1. Log the breaker event with the reason
2. Do NOT retry, wait, or theorize
3. Try the next candidate for the same gap
4. If no candidates remain, try the next approach
5. If no approaches remain, proceed to report

Always forward. Never backward. Never circular.

## Retry logic

All network calls (web_fetch, mcporter call, API requests) use this pattern:

```
attempt 1: immediate
attempt 2: wait 2 seconds
attempt 3: wait 5 seconds
after 3 failures: skip this call, log the error, move on
```

Retryable errors: HTTP 429, 500, 502, 503, 504, connection timeout, DNS resolution failure.
Non-retryable errors: HTTP 400, 401, 403, 404, invalid URL. Skip immediately.

Never block the session on a single failing endpoint. Log and move on.

## Identity cascade

When a service requires email signup, try providers in order. If one fails, try the next.

| Priority | Provider | TTL | Create | Poll |
|----------|----------|-----|--------|------|
| 1 | BotEmail.ai | 6 months | `POST https://api.botemail.ai/api/create-account` body: `{}` | `GET https://api.botemail.ai/api/emails/{email}` header: `Authorization: Bearer {key}` |
| 2 | Mail.tm | days | `POST https://api.mail.tm/accounts` (get domains: `GET https://api.mail.tm/domains`) | `POST https://api.mail.tm/token` then `GET https://api.mail.tm/messages` with Bearer token |
| 3 | 1secmail | ~1 hour | `GET https://www.1secmail.com/api/v1/?action=genRandomMailbox` | `GET https://www.1secmail.com/api/v1/?action=getMessages&login={user}&domain={domain}` |
| 4 | Guerrilla Mail | 60 min | `GET https://api.guerrillamail.com/ajax.php?f=get_email_address` | `GET https://api.guerrillamail.com/ajax.php?f=check_email&seq=0&sid_token={token}` |

Rules:
- Prefer BotEmail (longest TTL, simplest API). Fall down the list only on failure.
- Providers 3-4 have short TTLs. If using them, complete the signup and verification immediately. Do not delay.
- If a service rejects the disposable email domain, skip the service. Do not try a different email provider for the same service.
- If all 4 providers fail, proceed without signup capability. Restrict to no-auth candidates.
- Store email + credentials only in `manifest.json`. Dies with session.

## Gates that require a handler

When the execute worker hits a gate, search for an installed handler before skipping.

**Search order:** `mcporter list` for MCP tools, `clawhub list` for installed skills, then check session's downloaded skills.

**Max handler search depth: 1.** Search for a handler for the gate. Do not search for handlers of handlers. If the handler itself hits a gate, skip the entire service.

| Gate type | What to search for | If no handler |
|-----------|-------------------|---------------|
| CAPTCHA / challenge | Skill or MCP that accepts challenge input | Skip service |
| Browser login flow | Headless browser MCP or skill | Skip service |
| Phone/SMS verification | Disposable phone API or SMS skill | Skip service |
| OAuth-only flow | Browser automation that can drive OAuth | Skip service |
| Credit card required | Nothing -- violates free-only constraint | Skip service |
| KYC / identity docs | Nothing -- requires real documents | Skip service |

The worker does not need to know how the handler works. It recognizes the gate type, calls the handler if available, and continues.

## Reframing tactics

When no candidate works for a gap, try these before reporting failure:

1. **Different data source.** Commodity data (weather, exchange rates, country codes, stock prices) almost always has a no-auth alternative. Check `references/scoring.md` §Known zero-auth free APIs.

2. **Compose from smaller pieces.** Two free APIs composed often beat one premium API.

3. **Scrape instead of API.** Data on a public webpage? `web_fetch` + parse HTML.

4. **Reduce scope.** If the blocker is scale (rate limits, pagination), do fewer items and note the limitation. Partial completion beats total failure.

5. **Use static data.** Country codes, timezone lists, language codes, ISO standards -- these don't need an API. Download once to workspace.

6. **Ask the user for an existing credential.** Last resort. "This task needs a GitHub token. Do you have one?" Credential lives only in session dir. This is the ONE exception to the no-check-in rule: it's not asking for permission, it's asking for a fact the skill can't generate on its own.

## Checkpoint corruption

Workers crash mid-write. The checkpoint file may contain partial JSON.

**Read pattern:**
```
try: parse checkpoints/{worker_id}.json
if parse fails:
  log: "checkpoint corrupted for {worker_id}"
  treat worker as if it produced no results
  do not crash the orchestrator
```

Never trust a checkpoint without parsing it first. A corrupted checkpoint means that worker's results are lost, not that the session is lost.

## Spawn failure

If `sessions_spawn` returns an error:
- Log the error.
- Execute that worker's task inline (in the orchestrator's own context).
- This is slower but functionally identical.
- Do not retry the spawn. If the first spawn failed, subsequent spawns will likely also fail.

If ALL spawns fail, the orchestrator runs the entire discovery phase inline, single-threaded. Slower but complete.

## mcporter not installed

If mcporter is not available:
- MCP servers over HTTP are just REST endpoints. Call them directly with `web_fetch`.
- MCP server endpoints accept JSON-RPC: `POST {url}` with `{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "{tool}", "arguments": {...}}, "id": 1}`
- MCP servers over stdio are inaccessible without mcporter. Skip those candidates.
- Log: "mcporter not available, using direct HTTP for MCP servers."

## Graceful degradation

| Condition | Degradation | Impact |
|-----------|-------------|--------|
| `maxSpawnDepth < 2` | Single-threaded discovery | Slower |
| `maxSpawnDepth == 0` | Multipass runs inline, no sub-agents at all | Much slower, still works |
| mcporter missing | Direct HTTP for MCP, no stdio servers | Fewer MCP candidates |
| All email providers down | No-auth candidates only | Fewer candidates |
| All discovery workers fail | Inline discovery | Slower |
| All approaches fail | Failure report | User gets diagnosis, not silence |

The bottom row is the floor. Multipass always produces an output, even if that output is "here's what I tried and why it didn't work."

## Replay health

Every replay script includes:

**Health checks** -- curl commands that verify endpoints are live:
```bash
curl -s -o /dev/null -w "%{http_code}" {endpoint}  # expect 200
```

**Version pins** -- API versions, npm package versions, dates of verification.

**Bitrot warnings** -- flag APIs that are beta, single-developer, or have no SLA.

**"What might break"** -- explicit list of things that could change: rate limits, auth requirements, endpoint URLs, free tier limits.

## Progress visibility

The orchestrator writes `status.txt` after every checkpoint poll. One line, overwritten:

```
[1/4] Searching ClawHub and Skills.sh (7 candidates found)
[2/4] Resolving: best candidate is Open-Meteo (score 0.94)
[3/4] Executing: fetching data (2 of 3 endpoints done)
[done] Task complete. Output in sessions/{id}/output/
```

The main agent reads this file if the user asks about progress. Multipass does not use sub-agent announce for intermediate updates.
