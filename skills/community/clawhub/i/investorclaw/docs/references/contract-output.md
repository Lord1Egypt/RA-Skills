<!--
v4.x adaptation note: this reference contract is carried forward from
v2.6 essentially unchanged — the engine's input/output schema, holdings
field mapping, and consultative-LLM setup are identical in v4.x. The
only surface change is invocation: replace v2.x `/portfolio X` slash
commands with the equivalent v4.x MCP tool (`portfolio_X`) or a
natural-language query through `portfolio_ask`. Paths like
`~/portfolio_reports/` correspond to the bind-mounted `./reports/`
under your compose project; `portfolios/` corresponds to the
bind-mounted `./portfolios/`.
-->

# Output Contract

Full spec of the output-response rules the skill commits to. SKILL.md links
here from `## Output Contracts`.

## Directory layout

```
~/portfolio_reports/                  ← agent-readable compact files ONLY
    holdings_summary.json
    performance.json
    bond_analysis.json
    analyst_data.json
    portfolio_news.json
    portfolio_analysis.json
    fixed_income_analysis.json
    session_profile.json
    portfolio_report.xlsx / *.csv

~/portfolio_reports/.raw/             ← optional internal / enrichment artifacts
    holdings.json
    analyst_recommendations_tier1_immediate.json
    analyst_recommendations_tier2_background.json
    analyst_recommendations_tier3_enriched.json
    performance.json
    bond_analysis.json
    portfolio_news_cache.json
```

**Never read files from `.raw/` directly.** If you need specific symbol detail
not in the compact output, use the lookup command instead.

## Envelope format

All outputs use the mandatory disclaimer wrapper:

```json
{
  "disclaimer": "⚠️  EDUCATIONAL ANALYSIS - NOT INVESTMENT ADVICE",
  "is_investment_advice": false,
  "consult_professional": "Consult a qualified financial adviser",
  "data": { ... },
  "generated_at": "2026-04-07T..."
}
```

## Compact vs full output

Holdings, performance, and analyst commands emit compact JSON to stdout
(~1–5K tokens). Holdings also writes `portfolio_reports/holdings_summary.json`
as the agent-readable compact file. The full data is written to
`portfolio_reports/.raw/` for downstream script use only.

Work exclusively from compact stdout output or the summary files in
`portfolio_reports/`. If a user asks for a specific symbol or detail not in
the compact output, use the lookup command:

```bash
# Holdings detail for a symbol
investorclaw lookup --symbol AAPL
investorclaw lookup --symbol AAPL --file holdings

# Analyst data for a symbol
investorclaw lookup --symbol MSFT --file analyst

# Top 10 performers from performance data
investorclaw lookup --file performance --top 10

# Account summary from holdings
investorclaw lookup --accounts

# Specific fields only
investorclaw lookup --symbol AAPL --fields consensus,analyst_count,current_price
```

Environment variables are set automatically by the setup orchestrator. Lookup
returns a compact targeted slice — never the full file.

## Verbatim quote blocks

When a `quote` block is present in any output JSON with `verbatim_required: true`:

- If `quote.card_path` is set, present the card path and cite `quote.attribution`.
- Otherwise present `quote.text` **verbatim** — do not paraphrase or reorder.
- Always include `quote.fingerprint` in your response for audit traceability.
- Do not re-analyze or substitute your own synthesis.

```json
{
  "quote": {
    "text": "Analyst consensus is Strong Buy with 54 analysts...",
    "attribution": "gemma4-consult via local-inference (3420ms)",
    "verbatim_required": true,
    "fingerprint": "a1b2c3d4e5f6g7h8",
    "card_path": "/Users/.../portfolio_reports/.raw/consultation_cards/MSFT.svg"
  },
  "consultation": {
    "model": "gemma4-consult",
    "endpoint": "http://localhost:11434",
    "inference_ms": 3420,
    "is_heuristic": false
  }
}
```

The consultation model is user-configured via `INVESTORCLAW_CONSULTATION_MODEL`.
Default: `gemma4-consult` — a tuned Ollama derivative of `gemma4:e4b`
(num_ctx=4096, num_predict=1200, ~65 tok/s on RTX Ada). Other tested models:
`gemma4:e4b`, `nemotron-3-nano`, `qwen2.5:14b`. Run `/portfolio setup` to
auto-detect available models on your endpoint. Full setup steps in
[runtime-gemma4-consult.md](runtime-gemma4-consult.md).

## synthesis_basis confidence tiers

Each symbol in compact output includes a `synthesis_basis` field:

| Value | Source | Agent behavior |
|-------|--------|---------------|
| `enriched` | LLM synthesis (is_heuristic=false) | Present `quote.text` verbatim or show `quote.card_path` |
| `structured` | Live Finnhub data, no synthesis | Cite structured fields only: `"Analyst consensus: {consensus} ({analyst_count} analysts)"` |
| `failed` | No price or analyst data | State data unavailable — do not synthesize |

**Never apply enriched-symbol quality inferences to `structured` positions.**

## Turn-level enrichment status

Every analyst or portfolio response must begin with the
`enrichment_status.display` string:

```
⏳ Enrichment: 20/215 · 9.3% · a1b2c3d4 · updating
✅ Enrichment: 215/215 · 100.0% · a1b2c3d4 · complete
⚠️ Enrichment status unknown
```

The display string is sourced from `enrichment_status.display` in the compact
stdout. If absent, output `⚠️ Enrichment status unknown`.
