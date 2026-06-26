---
name: cost-watchdog
description: Tracks LLM spend across providers live, detects runaway loops, enforces budgets. Triggers on: cost/budget/token mentions, LLM API calls, agent workflows, batch processing.
when_to_use: "TRIGGER when: cost/budget/token mentions, LLM API calls in code, agent loops, batch processing, or `/cost-watchdog` commands."
argument-hint: "[command] — session, tail, detect, audit, price, estimate, alternatives, report, errors, validate-tokens, reset"
metadata: {"openclaw": {"emoji": "💰"}}
---

# Cost Watchdog 💰

> Real-time cost tracking layer for LLM-based agents. Prices every call live,
> detects runaway loops in code, enforces budget ceilings mid-execution.

## 1. Identity

Observes LLM spend without disturbing the agent. Prevents `$2,400-overnight-loop`
disasters by making cost a first-class concern: priced at write time,
budgeted at check time, surfaced in reports.

## 2. Triggers

Activate when:

- User mentions cost, budget, tokens, billing.
- Code contains LLM API calls (Anthropic, OpenAI, OpenRouter, Google, Groq, ...).
- Agent loops or recursive workflows.
- Batch / streaming processing with unclear bounds.
- `/cost-watchdog [command]` is invoked.

## 3. Commands

Run via `python3 scripts/cost_watchdog.py <cmd>` (or hook into your own CLI).

| Command | What it does |
|---|---|
| `session` | Spend totals from `usage.jsonl` — calls, tokens, cost, top models. |
| `report` | 24h / 7d / 30d windows with top model per window. |
| `tail [--once]` | Watch OpenClaw session JSONL and log every assistant turn. |
| `detect [--json]` | Identify which model the agent is currently using (5 probes). |
| `audit <file.py>` | AST-based code risk scan: unbounded loops, recursion, missing `max_tokens`. |
| `price <model>` | Live pricing for one model, with source + cache age. |
| `estimate <model>` | Project cost for `n` iterations of a given call. |
| `alternatives <model>` | Cheaper same-unit models. |
| `errors [--limit N]` | Recent swallowed exceptions (silent failures made visible). |
| `validate-tokens <model>` | Compare our heuristic against provider's authoritative count. |
| `reset [--all]` | Clear current-day log (`--all` also clears rolled files). |

## 4. Pricing layer

### Source chain

```
openrouter/*            → OpenRouter API (live)           → static fallback
anything else           → LiteLLM JSON (live, cached 24h) → OpenRouter (permissive) → static fallback
```

- **2600+ models** indexed across chat, completion, embedding, image, audio,
  video, rerank, OCR, search modes.
- **30+ providers** in the static fallback: Anthropic, OpenAI, Google,
  Groq, Mistral, Cohere, DeepSeek, Perplexity, xAI, Bedrock, Azure, and more.
- Unit-aware: `token`, `image`, `second`, `query`, `page`, `character`,
  `pixel`. Alternatives never compare across units.
- **Circuit breaker** opens after 3 consecutive network failures for a host;
  falls through to cache/static until the cool-down ends (60s).

### Tuning

| Env var | Default | Effect |
|---|---|---|
| `CW_PRICE_TTL_SECONDS` | 86400 (24h) | Cache lifetime. `0` = hit network every call. |
| `CW_OFFLINE` | unset | If `1`, never touch the network. |
| `CW_STATIC_ONLY` | unset | If `1`, skip live sources entirely. Used by tests. |
| `CW_LOG_DIR` | `~/.cost-watchdog` | Where usage/errors/cache files live. |
| `CW_BUDGET_USD` | unset | Ceiling; wrappers raise `BudgetExceeded` when crossed. |

### Refresh static pricing

```
python3 scripts/refresh_pricing.py
```
Regenerates `references/pricing.md` from the live sources so the offline
fallback is fresh. Aborts if fewer than 100 rows came back (protects
against clobbering on a network outage).

## 5. Tracking layer — how we know what was spent

Four independent paths, all write to `~/.cost-watchdog/usage.jsonl`:

| Path | When to use | Covers streams? |
|---|---|---|
| `openclaw_tailer.py --watch` | Running OpenClaw. Zero code changes. | yes (reads completed turns) |
| `track_openai(client)` | You call OpenAI-compatible SDK (covers OpenRouter, Groq, DeepSeek, Mistral, Together, Fireworks, Cerebras, Anyscale, ...). | yes (tee'd iterator, auto-injects `stream_options={"include_usage": True}`) |
| `track_anthropic(client)` | Direct Anthropic SDK. | yes (wraps `messages.stream()`) |
| `track_gemini(model)` / `track_cohere(client)` / `track_bedrock(client)` | Direct provider SDKs. | no (add wrappers if you need streams) |
| `install_global_capture()` (httpx) | Any modern Python SDK using httpx. | **no** — streams are flagged into `errors.jsonl` so the gap is visible. Use the SDK wrappers for stream coverage. |

Usage log rotates daily: `usage.YYYY-MM-DD.jsonl`. `session_total(since=...)`
skips files outside the window before scanning.

Aggregation uses `canonical_family()` so
`claude-haiku-4-5-20251001`, `claude-haiku-4-5`, and `claude-haiku-4.5`
are one row in reports.

## 6. Budget enforcement

Two mechanisms:

1. **Write-time check** (race-safe): `append_usage(entry, budget_ceiling=X)`
   takes an `fcntl.flock` on a sidecar, sums the current session, and
   refuses the write (raises `BudgetExceeded`) if the call would cross `X`.
2. **Post-write check**: wrappers compare cumulative spend to `CW_BUDGET_USD`
   after logging and raise if over. Used when the wrapper doesn't know the
   ceiling at call time.

Either path stops the agent mid-loop; the LLM call still returns to the
caller, but the next one blocks.

## 7. Code audit (AST)

```
python3 scripts/cost_watchdog.py audit path/to/agent.py
```

Walks the AST and reports:

- **CRITICAL** — `while True` with an LLM call and no `max_iterations`-style bound.
- **CRITICAL** — function that recurses and calls an LLM API with no depth argument.
- **HIGH** — plain `while` that calls an API with no retry/iteration counter.
- **MEDIUM** — LLM call missing `max_tokens` / `max_completion_tokens`.
- **MEDIUM** — function with ≥5 sequential LLM calls (batching candidate).

Every finding has a file line number. No more `count('def ') > 3 and
count('self.') > 5 → "recursion detected"` false positives.

## 8. Detection — "what model is the agent using?"

```
python3 scripts/cost_watchdog.py detect
```

Five probe layers, ranked by confidence:

| Probe | Confidence |
|---|---|
| OpenClaw session JSONL | high |
| Claude Code session JSONL | high |
| Most recent usage-log entry | high |
| Claude Code `settings.json` | medium |
| Env vars (`ANTHROPIC_MODEL`, `OPENAI_MODEL`, ...) | medium |

Emits a table or `--json`.

## 9. Files

| Path | Purpose |
|---|---|
| `scripts/_pricing.py` | Router: picks LiteLLM / OpenRouter / static per query. |
| `scripts/_sources.py` | Three `PricingSource` classes + disk cache + circuit breaker. |
| `scripts/tokenizer.py` | Provider-aware token counting (tiktoken for OpenAI; calibrated heuristics for others). |
| `scripts/model_canon.py` | `canonical_family()` — collapses model variants. |
| `scripts/code_audit.py` | AST cost-risk walker. |
| `scripts/usage_log.py` | JSONL writer + rotation + aggregation. |
| `scripts/tracker.py` | SDK wrappers + streaming + budget enforcement. |
| `scripts/http_capture.py` | `install_global_capture()` — httpx transport hook. |
| `scripts/openclaw_tailer.py` | Watches OpenClaw sessions. |
| `scripts/detect_model.py` | Multi-layer detector. |
| `scripts/errors.py` | `errors.jsonl` writer + reader. |
| `scripts/io_utils.py` | `write_json_atomic` / `read_json`. |
| `scripts/refresh_pricing.py` | Regenerates static `pricing.md` from live sources. |
| `scripts/cost_watchdog.py` | Unified CLI dispatcher. |
| `references/pricing.md` | Static fallback (regenerated; ~2600 models). |
| `tests/test_cost_watchdog.py` | 73 tests: router, cache, AST, tokenizer, rotation, cassettes, circuit breaker, canonicalization. |

## 10. Quality checklist

- [x] Live pricing from LiteLLM + OpenRouter, 24h-cached, with static fallback.
- [x] Exact-match model lookup (no substring conflation).
- [x] Multi-modal (token / image / second / query / page / character).
- [x] Unit-aware alternatives (never compares tokens to images).
- [x] AST-based code audit with line numbers.
- [x] Provider-aware tokenization (no more tiktoken-for-Claude).
- [x] Variance-based confidence (no `+= 0.05` theater).
- [x] Atomic writes to all shared state files.
- [x] `fcntl.flock`-guarded budget check-and-log (no race).
- [x] Circuit breaker on flaky networks (no 5s hang per call).
- [x] Streaming capture via SDK wrappers; streams flagged in `errors.jsonl` via HTTP capture.
- [x] Daily log rotation + date-scoped aggregation.
- [x] Canonical model families (variants collapse in reports).
- [x] `errors.jsonl` surfaces silent failures; `cost_watchdog errors` shows them.
- [x] Cassette tests for LiteLLM + OpenRouter parse paths (schema-drift safety net).
- [x] 73 logic tests passing.

## 11. Known limits (be honest)

- **Tokenizer heuristics** for Claude/Gemini/etc. are calibrated from docs,
  not measured. Run `cost_watchdog validate-tokens <model>` to check drift
  against the provider's authoritative count when you have an API key.
- **`install_global_capture()` can't see streaming responses** — httpx exposes
  an empty body until the user reads the stream. Use `track_openai` /
  `track_anthropic` for stream coverage; `http_capture` logs skipped streams
  to `errors.jsonl` so the gap is visible.
- **Non-httpx SDKs** (older Cohere, boto3 with custom transport) need the
  per-SDK wrappers — HTTP capture won't see them.
- **LiteLLM community data** can lag 24-48h on brand-new models. OpenRouter's
  API is truly live for anything it routes.

## 12. Testing

```
python3 -m unittest tests.test_cost_watchdog     # 73 tests
python3 scripts/code_audit.py test_risky_code.py # sample risks
python3 scripts/cost_watchdog.py report          # current spend summary
```
