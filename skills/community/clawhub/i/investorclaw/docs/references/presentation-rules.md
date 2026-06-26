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

# Agent-Side Presentation Rules

Directive rules for how the calling LLM renders this skill's output to the
user. These are not user-facing docs; they govern the agent's turn.

## Mobile-channel formatting

Many users interact via mobile channels (320–430px display width). Format
all output to be readable on small screens:

- **No wide tables** — avoid pipe-separated columns that wrap badly.
- **Max ~60 characters per line** — use stacked two-line formats instead of
  horizontal layouts.
- **No raw JSON to user** — always render the compact digest as prose or short
  lists.
- **Bold tickers** — use `**AAPL**` for symbol emphasis.
- **Short separators** — use `---` or a brief label, not 60/80-char `===`
  banners.
- **Mobile-first default** — assume mobile unless `--verbose` is passed.

## News digest layout

Present `portfolio_news.json` compact digest as follows — do NOT collapse
all news into one sentence:

1. **Overall sentiment** — `sentiment_breakdown` counts + net portfolio
   impact.
2. **Top positive movers** — top 5 from `top_positive_movers`, two-line
   stacked format:
   ```
   📈 **AAPL** +$10,500
      Apple Q1 Earnings Beat Estimates by 12%
   ```
3. **Top negative movers** — top 5 from `top_negative_movers`, same stacked
   format:
   ```
   📉 **NVDA** -$8,200
      Chip export restrictions widen to additional markets
   ```
4. **Symbol digest** — from `symbol_digest`, two lines per holding:
   ```
   **MSFT** · 12.4% · Bullish · 4 articles
     → Azure growth accelerates in Q1 earnings call
   ```
5. **Macro themes** — shared themes across multiple holdings (AI capex,
   rates, energy).
6. **On-demand detail** — tell the user they can run
   `/portfolio news --symbol TICKER` for full articles.

Sort movers by `portfolio_impact` (highest dollar-weighted first).

## ETF / fund guidance

ETF and mutual-fund positions cannot be individually adjusted — the user can
only buy or sell the fund as a whole. Before suggesting any position change,
check `is_etf`. If true, frame at fund level (e.g., "To reduce IVV exposure,
sell IVV shares — you cannot adjust S&P 500 components directly"). Analyst
ratings and news for ETF tickers reflect the fund, not individual underlying
companies.

ETF classification (`is_etf`, `security_type`) is provided but ETF constituent
expansion (detailed allocation view of underlying holdings) is not currently
implemented.

Full holdings-field schema in [schema-holdings-fields.md](schema-holdings-fields.md).
