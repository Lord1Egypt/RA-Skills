# Privacy Policy

**Effective:** 2026-05-04
**Project:** InvestorClaw v4.x — Containerized portfolio analysis service
**Maintainer contact:** Jason Perlow &lt;jperlow@gmail.com&gt;

## Summary

InvestorClaw v4.x is an open-source (Apache 2.0 substantive code; MIT-0
distribution-edge artifacts) Docker Compose stack that runs entirely on
the user's own machine. The maintainer collects no data. The service
itself collects no data. Portfolio files stay on the user's local
filesystem. Computed summaries leave the local machine only when the
user invokes a query through the agent (Claude Code, Claude Desktop,
openclaw, zeroclaw, or hermes), and even then only travel to the
third-party services the user explicitly configures (the language model
and any market-data API keys).

This policy explains exactly which data leaves the user's machine, where
it goes, and what the user can do to constrain it.

## Data the maintainer collects

**None.** InvestorClaw has no telemetry, no analytics, no phone-home, and
no central server. The maintainer does not see service usage, prompts,
portfolio data, or output. There is no account creation; there is no
operator-controlled service. The Docker image
(`ghcr.io/argonautsystems/ic-engine:4.1.x-cpu`) is pulled anonymously
from GitHub Container Registry and runs entirely on the user's host.

## Local data on the user's machine

- **Raw broker files** (CSV / XLS / XLSX / PDF / screenshots) stay in the
  user's local portfolio directory (the bind-mounted `./portfolios/`
  under the user's compose project, or `${INVESTORCLAW_PORTFOLIO_DIR}`
  if overridden). They are never uploaded by InvestorClaw itself.
- **Account numbers and Social Security numbers** are scrubbed at import
  time before any computed summary is constructed. Scrubbed values are
  replaced with redaction markers; the originals are not retained
  outside the user's local raw files.
- **Computed summaries and signed JSON envelopes** are written to the
  bind-mounted `./reports/` directory (or `${INVESTORCLAW_REPORTS_DIR}`)
  for reproducibility and audit. These remain local.
- **Cache** of recent pipeline runs lives in the `ic-engine-data` Docker
  volume to avoid re-fetching unchanged data; cache contents are local.
- **API keys** the user sets via `portfolio_keys_set` or by editing
  `portfolios/keys.env` are persisted to `/data/keys.env` (mode 0600)
  inside the named Docker volume. They never leave the host.

## Data flows that DO leave the user's machine

When the user asks a portfolio question, the deterministic pipeline runs
locally inside the container and produces a signed JSON envelope. That
envelope and the user's question are passed to the configured language
model for natural-language narration. Specifically:

### 1. Narrative language model (always involved when narrative is enabled)

The container ships pre-configured for Together AI
(`google/gemma-4-31B-it`). When the user supplies a `TOGETHER_API_KEY`
(via `portfolio_keys_set` REST endpoint or `portfolios/keys.env`), the
narrator sends the user's question and the signed envelope to
`https://api.together.xyz/v1`. Together AI's privacy policy applies to
that traffic: https://www.together.ai/privacy

If no LLM key is configured, the engine still runs the deterministic
Python pipeline (numbers are correct) but the narrator returns a stub
catalog summary instead of a real prose answer. **In this mode no
prompt or envelope leaves the local machine.**

The agent talking to the container (Claude Code / Claude Desktop /
openclaw / zeroclaw / hermes) uses its own LLM provider for tool-use
routing — that is a separate flow governed by the agent's privacy
policy, not InvestorClaw's.

### 2. Optional consultative model (only if enabled)

If the user enables `INVESTORCLAW_CONSULTATION_ENABLED=true`, heavier
synthesis prompts are sent to the configured consult endpoint. The
endpoint URL determines whether this is local (e.g. a local Ollama or
llama-server on the user's own GPU) or cloud (e.g. Together AI, Google
AI Studio). The default is **off**. No consult traffic happens unless
the user explicitly enables it.

### 3. Market-data providers (only if API keys are configured)

InvestorClaw uses `yfinance` by default, which is free and
unauthenticated. If the user supplies API keys for any of the following,
request traffic flows to those providers:

| Provider | When used | Privacy policy |
|---|---|---|
| Finnhub | Real-time quotes, analyst ratings, category news | https://finnhub.io/policies/privacy |
| NewsAPI | News headlines correlated to holdings | https://newsapi.org/privacy |
| Alpha Vantage | Supplemental price data | https://www.alphavantage.co/privacy/ |
| MarketAux | Financial news with broader filters | https://www.marketaux.com/privacy |
| Massive (via Massive) | Quotes + history for 200+ symbol portfolios | https://massive.com/privacy |
| FRED (St. Louis Fed) | Treasury yield curve | https://www.stlouisfed.org/privacy-notice-and-policy |

If the user does not configure these keys, none of these providers
receive any traffic. The engine falls back to free `yfinance` queries.

### 4. Image registry (one-time)

The first `docker compose up -d` pulls the engine image
(`ghcr.io/argonautsystems/ic-engine:4.1.x-cpu`) anonymously from GitHub
Container Registry. GitHub may log the pull (IP + user-agent +
timestamp) per their standard policy:
https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement

## What the third parties see

The maintainer cannot guarantee what each third party retains, but
typically:

- The narrative LLM provider sees the user's natural-language question
  and the signed JSON envelope (which contains computed portfolio
  summaries — ticker symbols, asset class breakdowns, performance
  metrics — but account numbers and SSNs are scrubbed).
- Market-data providers see the ticker symbols the user is asking about
  and standard request metadata (IP, user-agent, timestamp).
- News providers see the holdings tickers and date ranges queried.

The user should consult each provider's policy linked above to
understand their retention and use practices.

## User-controlled redaction

The user can constrain data flows by:

1. Running entirely on a local LLM (point `INVESTORCLAW_NARRATIVE_ENDPOINT`
   at a local Ollama / llama-server / LMStudio / vLLM endpoint) so no
   prompt or envelope leaves the local network.
2. Not configuring any market-data API keys (forces yfinance fallback).
3. Keeping `INVESTORCLAW_CONSULTATION_ENABLED=false` (default — skips
   the consult pass).
4. Reviewing the signed JSON envelope under `./reports/` before running
   each ask — what's in the envelope is exactly what the LLM sees.
5. Never typing account numbers, SSNs, or other personal identifiers
   into the prompt itself. The service only sees prompt text the user
   sends through the agent.

## Children's privacy

InvestorClaw is intended for adult investors. The maintainer does not
knowingly process data from children under 13.

## Trades, orders, money movement

InvestorClaw does not execute trades, place orders, move money, or
authenticate to any brokerage. It is a read-only educational analysis
tool that operates on broker-export files the user voluntarily places
in the portfolio directory.

## Vulnerability and data-incident reporting

Suspected privacy or security issues should be emailed privately to
&lt;jperlow@gmail.com&gt;. See `SECURITY.md` for vulnerability-disclosure
expectations.

## Changes to this policy

This policy may be updated alongside service releases. Material changes
will be noted in `CHANGELOG.md` under the corresponding version entry.
The current effective date appears at the top of this document.

## Contact

Privacy questions: &lt;jperlow@gmail.com&gt;
