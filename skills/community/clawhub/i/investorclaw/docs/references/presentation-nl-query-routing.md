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

# NL Query Routing — Seed Pattern Dictionary (v2.1.0)

Directive rules for how the calling LLM should turn natural-language
portfolio queries into canonical `/portfolio <command>` invocations.

This is a seed set. It targets the 10 intent clusters that produced the
worst routing outcomes in the internal NL-250 harness run (2026-04-22):
agents either refused to load the skill, or they hallucinated a
portfolio answer without invoking any underlying script (`ic_result`
absent). Each pattern below includes a canonical invocation, expected
output envelope fields, and common anti-patterns.

Full pattern coverage is planned for a follow-on release with fresh
NL-N measurements backing each addition. For now, prefer these patterns
over improvisation when the user's phrasing matches.

## Pattern 1 — "Show me my holdings" (holdings basics)

**NL phrases (non-exhaustive):**
- "Show my holdings"
- "What do I own?"
- "List my positions"
- "What's in my portfolio?"
- "What's my total portfolio value?"

**Canonical invocation:**
```
/portfolio holdings
```

**Output envelope to surface:** `holdings_summary.json` — `total_value`,
`position_count`, top-5 positions by value, sector breakdown.

**Anti-patterns:**
- ❌ *"Use the portfolio skill to run /portfolio holdings"* — OpenClaw's
  skill-loader heuristic rejects NL-wrapped slash commands. Invoke the
  slash form directly.
- ❌ Summarizing from memory / prior-session cache if `ic_result` is
  absent — that is a stale-masquerade failure mode. Say so explicitly.

## Pattern 2 — "How am I doing?" (performance)

**NL phrases:**
- "How is my portfolio doing?"
- "What's my return?"
- "Am I beating the market?"
- "Am I beating the S&P 500?"
- "What's my Sharpe ratio?"
- "What's my volatility?"

**Canonical invocation:**
```
/portfolio performance
```

**Output envelope:** `performance.json` — `total_return`, `annualized_return`,
`sharpe_ratio`, `volatility`, `benchmark_comparison`.

**Anti-patterns:**
- ❌ Speaking to "beating the market" without the benchmark field
  actually present in the envelope. If `benchmark_comparison` is null,
  say benchmark comparison was not computed; do not synthesize a number.

## Pattern 3 — "Show my bonds" (fixed-income basics)

**NL phrases:**
- "Show my bond exposure"
- "Analyze my fixed income"
- "What's my bond allocation?"
- "What's my bond YTM?"
- "Show my bond ladder"

**Canonical invocation:**
```
/portfolio bonds
```

**Output envelope:** `bond_analysis.json` — `bond_count`, `total_value`,
`weighted_ytm`, `weighted_duration`, per-bond detail.

**Empty-state handling:** if `bond_count` is 0, respond exactly:
"No bonds in this portfolio — bond analysis skipped." Do NOT synthesize
a response about bonds; there aren't any. (Empty-set handling guaranteed
by the envelope contract per commit `49e9d1c` / v2.1.0.)

**Anti-patterns:**
- ❌ Asserting a YTM or duration that isn't in the envelope.
- ❌ Treating a missing bond envelope as "TODO later" — the command is
  safe to run on any portfolio; empty results are a valid answer.

## Pattern 4 — "What does Wall Street think?" (analyst consensus)

**NL phrases:**
- "What does Wall Street think?"
- "Show analyst ratings"
- "Any analyst upgrades?"
- "What are analysts saying about [TICKER]?"

**Canonical invocation:**
```
/portfolio analyst
```

For a single symbol:
```
/portfolio lookup --symbol TICKER --file analyst
```

**Output envelope:** `analyst_data.json` — per-holding
`consensus` / `analyst_count` / `price_target`. Each position carries a
`synthesis_basis` tier (`enriched` / `structured` / `failed`) — see
[contract-output.md](contract-output.md).

**Anti-patterns:**
- ❌ Presenting `structured` positions as if they were `enriched` (no
  narrative inference on structured-only data).
- ❌ Answering about a specific ticker without running the lookup
  command — direct-from-envelope only.

## Pattern 5 — "Any news on my stocks?" (news correlation)

**NL phrases:**
- "Any news on my stocks?"
- "Show recent headlines"
- "What's happening with my holdings?"
- "What's moving my portfolio today?"

**Canonical invocation:**
```
/portfolio news
```

**Output envelope:** `portfolio_news.json` — `sentiment_breakdown`,
`top_positive_movers`, `top_negative_movers`, `symbol_digest`,
`macro_themes`.

**Presentation:** follow the "News digest layout" in
[presentation-rules.md](presentation-rules.md) — stacked two-line
movers with dollar impact; never collapse all news into one sentence.

**Anti-patterns:**
- ❌ Reporting portfolio-wide sentiment without the per-symbol breakdown.
- ❌ Summarizing article titles without `portfolio_impact` weighting.

## Pattern 6 — "Should I rebalance?" (scenario + tax-aware)

**NL phrases:**
- "Should I rebalance?"
- "Do I need to rebalance?"
- "Is it time to rebalance?"
- "Would rebalancing help?"
- "Show me a rebalancing scenario"
- "Tax-aware rebalancing options"
- "Calculate my tax loss harvesting opportunities"

**Canonical invocations (two-step):**
```
/portfolio scenario
```
followed by, if the user cares about tax efficiency:
```
/portfolio rebalance-tax
```

**Important — do not route to `/portfolio synthesize`:** "Should I
rebalance?" sits close to "recommend what to do" semantically, but the
canonical answer lives in the scenario/rebalance-tax envelopes (trade
tree + tax-lot impact), not in the synthesis envelope. Route to
`/portfolio scenario` first; only escalate to `/portfolio synthesize`
if the user explicitly asks for a broader recommendation pass.

**Output envelopes:** `scenario` produces rebalancing trade trees;
`rebalance-tax` adds unrealized-gain/loss impact + tax-lot selection.

**Educational framing (non-negotiable):**
- ❌ Never say "You should rebalance" as a directive.
- ❌ Never use imperative-voice advice verbs (sell, buy, must, should).
- ✅ Frame as "If you were to rebalance to X target, the envelope shows
  Y trades with Z tax impact." Educational output only.

## Pattern 7 — "Explain concept X" (financial education)

**NL phrases (representative):**
- "What's yield to maturity?"
- "What is YTM?"
- "Explain bond duration to me"
- "What's a Sharpe ratio?"
- "What's modern portfolio theory?"
- "Explain tax-loss harvesting"
- "What does alpha mean?"
- "Define [any finance term]"

**Routing:** these are NOT InvestorClaw's job. InvestorClaw operates on
the user's own portfolio; it is not a financial-terminology glossary.

**Mandatory behavior — not a suggestion:** when the user asks to
**explain, define, describe, or elaborate on a finance concept** and
the question does **not name one of their specific holdings**, you
MUST decline. **Do NOT answer from your own training data even if you
know the definition.** Answering from general knowledge produces an
`ic_result`-absent response that looks authoritative but is
unverifiable — the exact failure mode this skill's contract exists to
prevent.

**Canonical response (use verbatim or close to it):**

> "That's a general finance-concept question, not specific to your
> portfolio. InvestorClaw is scoped to your actual holdings and does
> not run a glossary or education layer. Try asking 'show me my
> [bonds / performance / holdings]' instead, or use a general-purpose
> knowledge source for concept explanations."

**Self-check before answering any concept-shaped question:**
1. Does the question name a symbol or asset in the user's portfolio?
   If no → **decline, do not answer**.
2. Does the question ask "what is X" / "define X" / "explain X" where
   X is a term, ratio, or concept (not a holding)? → **decline, do
   not answer**.
3. Would my answer come from my pretraining rather than from a skill
   command's output? → **decline, do not answer**.

**Anti-patterns:**
- ❌ Answering the concept question using general knowledge — this
  bypasses the skill entirely and produces `ic_result`-absent output
  that looks authoritative but is unverifiable.
- ❌ Declining but appending "but here's a quick definition anyway..."
  — the decline is absolute, not a preamble.
- ❌ Running an InvestorClaw command just to pad a concept explanation
  with synthetic portfolio data.

## Pattern 8 — Market-wide / macro queries (out of scope)

**NL phrases (representative):**
- "What's happening in the market today?"
- "How is the S&P 500 performing?"
- "What's the Fed doing?"
- "Latest inflation data?"
- "Show me economic calendar"
- "What about Bitcoin?"
- "What's the VIX at?"

**Routing:** InvestorClaw does not cover market-wide, macro, or
non-held-position queries. Its news and analyst layers join *on the
user's own holdings*, not on open-universe market data.

**Canonical response:** decline and redirect:

> "InvestorClaw is scoped to your own portfolio — it joins news,
> analyst, and performance data to positions you actually hold. For
> open-market commentary, VIX levels, Fed policy, or macroeconomic
> data, use a dedicated market-data tool instead."

**Anti-patterns:**
- ❌ Running `/portfolio news` and framing it as "market news" — it
  is portfolio-joined news only.
- ❌ Answering from general knowledge about today's market movement
  — that fabricates recency and is unverifiable.

## Pattern 9 — Multi-intent / "full picture" queries

**NL phrases:**
- "Show my holdings and find tax-loss opportunities"
- "Analyze my performance and tell me if I should rebalance"
- "Give me the full picture"

**Canonical invocation:**
```
/portfolio analysis
```

Or the full 8-stage pipeline:
```
/portfolio complete
```

**Output envelope:** `portfolio_analysis.json` stitched from the
primary envelopes (holdings + performance + bonds + analyst + news +
synthesis).

**When to split instead:**
- If the user specified exactly two intents that don't overlap with
  `/portfolio analysis`'s coverage (e.g., tax-loss + peer comparison),
  invoke the two commands sequentially and splice their envelopes.

**Anti-patterns:**
- ❌ Invoking each sub-command separately when `/portfolio analysis`
  already produces the combined envelope — wastes tokens and produces
  divergent `ic_result` trails.
- ❌ Narrating "doing both" without actually invoking anything.

## Pattern 10 — "Dashboard" requests (v2.1.0 deferral)

**NL phrases:**
- "Show me the dashboard"
- "Open the portfolio dashboard"
- "Generate the 15-tab view"
- "Where's the dashboard?"
- "Can I see the dashboard?"

**Routing:** the interactive PWA dashboard is in development and not
shipped in the v2.1.0 default install. The `/investorclaw:ic-dashboard`
slash command is moved to `claude/commands/_incomplete/` and is not
available after a standard marketplace install.

**Signal to use this response:** if you try `/portfolio dashboard` and
get back `❌ Unknown command: dashboard` (or an equivalent "dashboard
not available" signal from the skill router), switch to this canonical
response template. Do NOT just relay the raw "Unknown command" error
to the user — they will read it as a broken install. Explain the
deferral.

**Canonical response (use verbatim or close to it):**

> "The interactive PWA dashboard is in development for a future release
> and isn't shipped in the v2.1.0 install — you'll see an 'Unknown
> command: dashboard' error if you try to run it directly. In place of
> the dashboard I can run a narrative portfolio walkthrough right now
> with `/portfolio analysis`, or the full 8-stage pipeline with
> `/portfolio complete`. Both produce the same underlying data the
> dashboard is going to visualize."

**Anti-patterns:**
- ❌ Trying to invoke `/investorclaw:ic-dashboard` — the slash file
  won't be registered after install.
- ❌ Relaying the raw `❌ Unknown command: dashboard` output as the
  final answer — technically correct, operationally a failure; the
  user needs the context that the dashboard is *deferred*, not broken.
- ❌ Synthesizing what a dashboard *would* show from memory —
  `ic_result`-absent answer that looks authoritative but isn't.

## Coverage note

These ten patterns cover the highest-volume intent clusters observed
in the NL-250 harness run: holdings basics, performance, fixed income,
analyst ratings, news correlation, rebalancing, finance-concept
deflection, market-wide deflection, multi-intent routing, and the
deferred dashboard surface. Queries that don't match a listed pattern
should fall back to either `/portfolio help` or the finance-concept
decline in Pattern 7.

Full pattern coverage (targeting all 250 NL-250 categories with
per-category `ic_result` measurements) is planned for a follow-on
release. Until then, log any intent-cluster miss you observe and file
it for inclusion in the next expansion.
