# MCP Tools Reference

Detailed per-tool reference for the 13 MCP tools that ic-engine exposes
on `localhost:18090/mcp`. For the high-level "what can it do" overview,
see [`CAPABILITIES.md`](../CAPABILITIES.md). For the agent-readable
install / first-run / cookbook spec, see [`SKILL.md`](../SKILL.md).

Every tool is also reachable as a plain HTTP REST endpoint at
`http://127.0.0.1:18090/api/portfolio/<tool>` — useful when your
agent's MCP client is flaky or you want to drive the engine from a
shell.

---

## Tool index

| Tool | Purpose | Equivalent v2.x slash command |
|---|---|---|
| [`portfolio_ask`](#portfolio_ask) | Primary tool — natural-language portfolio question | `/portfolio ask` |
| [`portfolio_initialize_status`](#portfolio_initialize_status) | Poll init progress before first ask | (new in v4.x) |
| [`portfolio_initialize`](#portfolio_initialize) | Force `setup → refresh → seed_ask` bootstrap | (new in v4.x) |
| [`portfolio_holdings`](#portfolio_holdings) | Holdings snapshot — positions, values, weights | `/portfolio holdings` |
| [`portfolio_refresh`](#portfolio_refresh) | Force fresh data pull | `/portfolio refresh` |
| [`portfolio_setup`](#portfolio_setup) | Auto-discover portfolio files | `/portfolio setup` |
| [`portfolio_keys_status`](#portfolio_keys_status) | Report which API keys are configured | (new in v4.x — replaces direct `.env` editing) |
| [`portfolio_keys_set`](#portfolio_keys_set) | Set one or more API keys | (new in v4.x) |
| [`portfolio_keys_delete`](#portfolio_keys_delete) | Delete a configured API key | (new in v4.x) |
| [`portfolio_response_get`](#portfolio_response_get) | Retrieve a stored response by run_id | (new in v4.x) |
| [`portfolio_response_list`](#portfolio_response_list) | List recent stored responses | (new in v4.x) |
| [`portfolio_response_delete`](#portfolio_response_delete) | Permanently delete a stored response | (new in v4.x) |
| [`portfolio_response_flag_bad`](#portfolio_response_flag_bad) | Flag a stored response as bad without deleting it | (new in v4.x) |

---

## `portfolio_ask`

**Primary tool. Every portfolio question goes here.** Data is
auto-loaded; the engine routes the question to the right deterministic
analyzer internally. The narrator returns a verified natural-language
answer with envelope-quoted numbers — never fabricated.

### Input

```json
{
  "question": "string"
}
```

### Output

```json
{
  "exit_code": 0,
  "narrative": "...",     // Human-readable answer
  "ic_result": {
    "hmac": "75ca79c...",  // HMAC signature of the envelope
    "engine_version": "2.5.2",
    "command": "ask",
    "run_id": "299d36b0-..."
  }
}
```

### Example

```bash
curl -sS -X POST http://127.0.0.1:18090/api/portfolio/ask \
  -H 'Content-Type: application/json' \
  -d '{"question": "What is in my portfolio?"}' \
  --max-time 120
```

### Routing rules

- Holdings / performance / bonds / news / optimization / target
  allocation / cash flow / peer comparison / lookup / reports / setup —
  all route through `portfolio_ask`.
- "Refresh" / "fresh data" intents also route here; the engine triggers
  refresh internally.
- Concept questions ("What does YTM mean?") return a deflection
  narrative explaining the concept with disclaimer.
- Market questions ("How is the S&P doing?") return a free-form market
  narrative with disclaimer.

### Latency

- Cold cache, 100-position portfolio: 30–60 s
- Cold cache, 200+ positions: 60–180 s
- Warm cache (TTL: 30 s news, 60 s other sections): 1–3 s

---

## `portfolio_initialize_status`

Poll before the first `portfolio_ask` to check whether the container's
auto-init has completed. Cheap, side-effect-free; safe to call every
1–2 seconds.

### Input

```json
{}
```

### Output

```json
{
  "state": "ready",          // not_started | initializing | ready | failed
  "current_stage": "seed_ask",
  "stages_completed": ["setup", "refresh"],
  "elapsed_ms": 42000,
  "ready": true,
  "init_error": null         // Set if state == "failed"
}
```

### Use it

```bash
curl -sS http://127.0.0.1:18090/api/portfolio/initialize/status
# Stream:
curl -N http://127.0.0.1:18090/api/portfolio/initialize/stream
```

The container runs `IC_INITIALIZE_ON_BOOT=1` by default, so by the
time your agent connects, the cache is usually warm and `ready: true`.

---

## `portfolio_initialize`

Force a manual `setup → refresh → seed_ask` bootstrap. Use after
uploading a new portfolio file when you want the cache rebuilt
synchronously.

### Input

```json
{}
```

### Output

```json
{
  "ready": true,
  "total_duration_ms": 146971,
  "stages": ["setup:0", "refresh:0", "seed_ask:0"]
}
```

### Latency

Same as cold-cache `portfolio_ask` (30–180 s depending on portfolio
size).

---

## `portfolio_holdings`

Direct snapshot of positions, values, weights, and account
classifications. Most agents should use `portfolio_ask` instead and
let the engine route — this tool is for power users who want the raw
holdings JSON without going through the narrator.

### Input

```json
{}
```

### Output

```json
{
  "exit_code": 0,
  "narrative": "...",
  "ic_result": {
    "holdings_summary": {
      "total_value": 2636605,
      "equity_pct": 71.55,
      "bond_pct": 26.76,
      "cash_pct": 1.69,
      "positions": [...],
      "accounts": {...}
    },
    "hmac": "...",
    "engine_version": "2.5.2"
  }
}
```

### Schema

See [`docs/references/schema-holdings-fields.md`](references/schema-holdings-fields.md)
for the full per-position field reference (`security_type`, `is_etf`,
`financial_type`, `proxy_symbol`, etc.).

---

## `portfolio_refresh`

Force fresh data pull (quotes, news, analyst ratings, FRED yield curve)
without re-uploading portfolio files. Use when news / prices may have
moved or you suspect stale cache.

### Input

```json
{}
```

### Output

```json
{
  "exit_code": 0,
  "narrative": "Refresh complete (envelope hash: 3afe6ecf...).",
  "ic_result": {
    "hmac": "...",
    "command": "refresh",
    "run_id": "..."
  }
}
```

### Cache TTLs

- News: 30 s
- All other sections (holdings, performance, bonds, analyst,
  synthesis, optimize, cashflow, peer): 60 s

The auto-refresh that runs on every `portfolio_ask` already respects
these TTLs. Only call `portfolio_refresh` explicitly when you want to
flush before the TTL expires.

---

## `portfolio_setup`

Auto-discover portfolio files in the configured directory
(`/data/portfolios/` inside the container, bind-mounted from
`./portfolios/` on the host).

### Input

```json
{}
```

### Output

```json
{
  "exit_code": 0,
  "narrative": "Found 1 PDFs, 2 Excel files, 0 CSVs. Setup complete.",
  "ic_result": {
    "files_discovered": 3,
    "accounts_found": 4
  }
}
```

### When to call

- After dropping a new broker file into `./portfolios/`
- After replacing an existing file with a refreshed export
- The auto-init at container boot already calls this once; you only
  need to call it again on changes.

### Input contract

See [`docs/references/contract-input.md`](references/contract-input.md)
for the full broker-CSV column-mapping reference (recognized column
names, bond metadata extraction from description strings, guided
mapping flow).

---

## `portfolio_keys_status`

Report which API keys are currently configured in `/data/keys.env`.
Returns names only, never values.

### Input

```json
{}
```

### Output

```json
{
  "configured": ["TOGETHER_API_KEY", "FINNHUB_KEY"],
  "settable": ["ALPHA_VANTAGE_KEY", "FRED_API_KEY", "MASSIVE_API_KEY",
               "MARKETAUX_API_KEY", "NEWSAPI_KEY", "OPENAI_API_KEY"],
  "missing": []
}
```

### Use it

```bash
curl -sS -X POST http://127.0.0.1:18090/api/portfolio/keys_status \
  -H 'Content-Type: application/json' -d '{}'
```

---

## `portfolio_keys_set`

Set one or more API keys without restarting the container. Persists
atomically to `/data/keys.env` (mode 0600), takes effect on the next
`portfolio_ask` without restart.

### Input

```json
{
  "keys": {
    "TOGETHER_API_KEY": "tgp_v1_...",
    "FINNHUB_KEY": "...",
    "FRED_API_KEY": "..."
  }
}
```

### Output

```json
{
  "configured": ["FINNHUB_KEY", "FRED_API_KEY", "TOGETHER_API_KEY"],
  "rejected": [],
  "deleted": []
}
```

### Allowlist

Only the standard ic-engine key names are accepted. Arbitrary names
are rejected with a structured `{"rejected": [...], "settable": [...]}`
response.

### Recommended set by portfolio size

| Size | Required | Recommended |
|---|---|---|
| ≤ 50 symbols | `TOGETHER_API_KEY` | — |
| 50–200 | `TOGETHER_API_KEY` | `FINNHUB_KEY`, `NEWSAPI_KEY` |
| 200+ | `TOGETHER_API_KEY` + `MASSIVE_API_KEY` | `FINNHUB_KEY`, `MARKETAUX_API_KEY`, `FRED_API_KEY`, `ALPHA_VANTAGE_KEY` |

See [`SKILL.md § Optional configuration`](../SKILL.md#optional-configuration)
for the full key reference and free-tier limits.

---

## `portfolio_keys_delete`

Delete a single configured API key by name.

### Input

```json
{ "name": "OPENAI_API_KEY" }
```

### Output

```json
{
  "configured": ["TOGETHER_API_KEY"],
  "deleted": ["OPENAI_API_KEY"],
  "rejected": []
}
```

---

## `portfolio_response_get`

Retrieve a stored portfolio response by `run_id`. Returns the full
envelope as it was when the response was generated.

### Input

```json
{ "run_id": "299d36b0-7015-4f29-84d2-bed5f84754af" }
```

### Output

The full original `portfolio_ask` response object.

### Use cases

- Debug a past response that surprised the user
- Audit / compliance trail
- Compare envelope state across two runs (correlation matrix changes,
  holdings drift, etc.)

---

## `portfolio_response_list`

List recent stored responses, most-recent first.

### Input

```json
{
  "limit": 20,        // optional, default 50
  "offset": 0         // optional, default 0
}
```

### Output

```json
{
  "responses": [
    {
      "run_id": "299d36b0-...",
      "command": "ask",
      "question": "What is in my portfolio?",
      "timestamp": "2026-05-04T20:09:59Z",
      "exit_code": 0,
      "flagged_bad": false
    },
    ...
  ],
  "total": 42
}
```

---

## `portfolio_response_delete`

Permanently delete a stored response. Useful when a bad response was
generated and you don't want it polluting future audits.

### Input

```json
{ "run_id": "299d36b0-..." }
```

### Output

```json
{ "deleted": "299d36b0-...", "ok": true }
```

---

## `portfolio_response_flag_bad`

Tag a stored response as bad without permanently deleting it. The
response stays in the history for audit and analysis, but is marked
with `"flagged_bad": true` in `portfolio_response_list` output.

Use this when a response was clearly wrong but you want to keep it for
debugging — for example, if the narrator fabricated a number or the
engine returned stale data. Use `portfolio_response_delete` instead
when you want the response gone entirely.

### Input

```json
{ "run_id": "299d36b0-..." }
```

### Output

```json
{ "run_id": "299d36b0-...", "flagged_bad": true, "ok": true }
```

---

## Output contract — applies to all tools

Every tool response wraps its data in the mandatory disclaimer
envelope:

```json
{
  "disclaimer": "⚠️  EDUCATIONAL ANALYSIS - NOT INVESTMENT ADVICE",
  "is_investment_advice": false,
  "consult_professional": "Consult a qualified financial adviser",
  "data": { ... },
  "generated_at": "2026-05-04T20:09:59Z"
}
```

See [`docs/references/contract-output.md`](references/contract-output.md)
for the full output spec including the directory layout
(`./reports/` for compact agent-readable files, `./reports/.raw/` for
internal enrichment artifacts) and compact-vs-full output rules.

## Presentation rules — applies to all narrative output

Agents consuming InvestorClaw responses must:

- Preserve all quoted source text, numerical values, timestamps, and
  freshness labels exactly.
- Never fabricate market, ticker, bond, news, or optimization data.
- If the signed envelope lacks a requested fact, say InvestorClaw did
  not provide it and quote the engine's limitation verbatim.
- Echo the educational-only disclaimer when summarizing.

Full presentation contract:
[`docs/references/presentation-rules.md`](references/presentation-rules.md).
Natural-language query routing details:
[`docs/references/presentation-nl-query-routing.md`](references/presentation-nl-query-routing.md).

## See also

- [`SKILL.md`](../SKILL.md) — agent-readable install + cookbook +
  first-run timeline
- [`CAPABILITIES.md`](../CAPABILITIES.md) — high-level "what can it do"
- [`docs/references/`](references/) — input / output / schema /
  consultative-LLM contracts
- [`STONKMODE.md`](../STONKMODE.md) — narrated commentary mode
