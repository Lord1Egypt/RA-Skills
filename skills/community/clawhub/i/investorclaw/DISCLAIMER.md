## Important Disclaimer

**InvestorClaw is an educational analysis tool.** It is NOT financial advice
and NOT provided by a fiduciary advisor.

**Before acting on any recommendation:**
- Discuss these findings with your qualified financial advisor
- Verify all data and calculations align with your actual holdings
- Consider your full financial situation, not just this portfolio

*No action should be taken based solely on InvestorClaw analysis.*

InvestorClaw never executes trades, never moves money, and never connects
to brokerage accounts. It is a read-only analysis tool that operates on
broker-export files (CSV / XLS / XLSX / PDF / screenshots) the user
voluntarily places in the portfolio directory.

## Provider Data Flows

InvestorClaw v4.x ships as a Docker Compose stack and exposes its
analytical capabilities to your agent over MCP-HTTP at `localhost:18090`.
Different parts of a typical request leave the local machine on different
paths, depending on what the user has configured:

- **Narrative LLM** — Prompts and the signed JSON envelope are sent to
  the configured narrative provider (Together AI by default —
  `google/gemma-4-31B-it`). The endpoint is set via
  `INVESTORCLAW_NARRATIVE_ENDPOINT` and the API key via
  `TOGETHER_API_KEY` (or other provider key).
- **Optional consultative model** — Only enabled when
  `INVESTORCLAW_CONSULTATION_ENABLED=true`. Off by default. When on,
  heavier synthesis prompts go to the configured consult endpoint
  (typically a local model server on the user's GPU; can be a cloud
  provider).
- **Market-data providers** — Quotes, news, analyst ratings, FRED yield
  curve, etc. flow to NewsAPI, Finnhub, Alpha Vantage, FRED, MarketAux,
  and Massive (via Massive) **only when the user supplies the
  corresponding API keys**. Without keys, InvestorClaw falls back to
  free `yfinance` queries (no auth, no key, but rate-limited).
- **Portfolio CSV / XLS / PDF data** stays local in the bind-mounted
  `./portfolios/` directory. Only computed summaries (the signed JSON
  envelope) and the user's question are sent to the narrative provider —
  not raw broker files.

Account numbers and Social Security numbers are scrubbed at ingest time
before any data leaves the container. See `PRIVACY.md` for the complete
data-handling policy.

## See also

- `PRIVACY.md` — full data-handling policy, what stays local vs what is
  sent to which provider
- `SECURITY.md` — vulnerability-disclosure path
- `SKILL.md` — agent-readable install and usage spec
- `LICENSE` — Apache 2.0 (substantive code) and MIT-0 (distribution-edge
  artifacts)
