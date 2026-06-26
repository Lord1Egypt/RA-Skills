---
name: polymarket-tradingskill
description: Use when an OpenClaw user needs fast NBA opportunity scanning, NBA-only /fair pricing, or deep analysis of one specific Polymarket market or event in any domain, including politics, via prompts like /analyze, analyze this market, or direct PM URLs, without making the final trading decision.
---

# OpenClaw Polymarket Decision Support

## Overview

Use this skill as a decision-support tool, not an autonomous trading brain. Its job is to surface promising markets, organize them by priority, and explain the pricing context so the user or higher-level system can make the final decision.

This skill assumes a read-only backend exists under `/api/v1/agent`. It does not place orders, cancel orders, manage wallets, or finalize trade decisions.

Before using the API, ensure these variables are available through the user's own OpenClaw-local configuration, secret store, or env file:

- `OPENCLAW_AGENT_API_BASE_URL`
- `OPENCLAW_AGENT_API_KEY`

Example values:

```bash
OPENCLAW_AGENT_API_BASE_URL=http://your-host:8080/api/v1/agent
OPENCLAW_AGENT_API_KEY=your-own-bearer-token
```

These variables must be configured by the OpenClaw user in their own environment. This skill only defines the required variable names and expected format. It does not manage, provision, or store user credentials.

## Fast Start

Use this routing rule before doing anything else:

- If the user asks for `/fair` and the target is NBA, use the NBA fair shortcut.
- If the user asks for `/analyze`, or gives one concrete PM URL / `market_id` / `event_id`, use deep analysis mode.
- If the user asks to scan, find opportunities, or review NBA trading candidates, use NBA opportunity scan mode.
- If the user asks to scan soccer opportunities, use the soccer basic-markets discovery path.
- If the user asks for `/fair` on any non-NBA domain, say `/fair` is NBA-only and continue with deep analysis mode.

This skill has one public purpose but three operating paths:

- `NBA Opportunity Scan`
- `NBA Fair Shortcut`
- `Universal Deep Analysis`

The current local sports coverage exposed by this skill includes:

- `nba`
- `soccer5` for basic soccer markets

Soccer note:

- soccer is available through the local `/markets` layer as `market_domain=soccer5`
- this is the basic soccer chain, not a blanket promise that every soccer side market is locally priced

## Use This Skill For

- Scanning a sport, league, or time window for worthwhile review candidates
- Returning a prioritized opportunity list with fair, ask, spread, and short reasoning
- Deepening one specific market by `market_id`, `event_id`, slug, or PM URL
- Handling explicit analysis intents such as `/analyze`, `analyze`, `分析`, `分析这个市场`, `分析这个事件`
- Handling `/fair` requests for NBA markets only
- Re-running the same scan in a loop without repeating unchanged analysis

Do not use this skill for:

- Trade execution
- Wallet or portfolio operations
- Final buy/sell decisions
- Internal fair-source debugging unless the user explicitly asks for model internals

## Mode Selection

Choose mode from the input:

- **NBA opportunity scan mode**
  - Use when the user wants quick NBA candidate generation
  - Typical intents:
    - `scan nba`
    - `find nba opportunities`
    - `today's nba markets`
    - `look for nba trades`
  - This mode is optimized for shortlist output, not deep commentary
- **Deep analysis mode**
  - Use when the input points to a specific market or event
  - Inputs can be `market_id`, `event_id`, event slug, or a Polymarket URL
  - Also use this mode when the user says `/analyze`, `analyze`, `分析`, `analyze this`, `分析这个市场`, or equivalent phrasing
- **Fallback discovery mode**
  - Use only when the user gives a broad non-NBA scope and does not name one market or event
  - This mode should usually end in a shortlist, not a long report

## Analyze Intent Mapping

Treat the following as a request for analysis capability, not just discovery:

- `/analyze <pm_url>`
- `analyze <pm_url>`
- `analyze this market`
- `分析这个市场`
- `分析这个 event`
- `deep dive this polymarket`

When the user provides one concrete PM URL, `market_id`, `event_id`, or event slug alongside an analyze-style request, skip discovery mode and go straight to deep analysis mode.

If the user says only `/analyze` with no market reference, ask for one of:

- a Polymarket URL
- a `market_id`
- an `event_id`
- an event slug

## Fair Intent Mapping

Treat `/fair` as a narrower shortcut than `/analyze`.

- `/fair` is supported only for NBA markets or NBA events
- If the referenced PM URL, event, or market is NBA, `/fair` may return the compact fair-price view
- If the referenced market is not NBA, do not force the fair-only workflow
- For non-NBA sports, leagues, props, esports, soccer, politics, or any other domain, route the request to `/analyze` behavior instead

Practical rule:

- `NBA + /fair` -> use fair-price-first handling
- `non-NBA + /fair` -> respond that `/fair` is only supported for NBA and continue with `/analyze` style deep analysis
- `/analyze` remains valid for every supported domain

If discovery mode finds a strong but uncertain candidate, it may automatically deepen at most `1-2` markets. Do not deepen the whole candidate set.

## Routing Table

- User asks for quick NBA trading ideas:
  - route to `NBA Opportunity Scan`
- User asks for soccer basic-market opportunities:
  - route to shortlist-oriented discovery with `market_domain=soccer5`
- User asks for `/fair` on NBA:
  - route to `NBA Fair Shortcut`
- User asks for `/fair` on non-NBA:
  - tell them `/fair` is NBA-only
  - then route to `Universal Deep Analysis`
- User gives one concrete PM URL, `market_id`, `event_id`, or event slug:
  - route to `Universal Deep Analysis`
- User asks about one politics event, election market, macro market, or other non-NBA topic:
  - route to `Universal Deep Analysis`
- User gives only a broad scope with no specific target:
  - route to shortlist-oriented discovery

## New Agent Operating Rules

For a newly spawned agent, default to these behaviors:

- Prefer routing correctly over exploring broadly.
- If the user gives one concrete market, analyze it immediately.
- If the user wants NBA opportunities, produce a shortlist quickly.
- If the user wants soccer opportunities, treat them as `soccer5` discovery unless they gave one specific market.
- Do not force every task through `/fair`.
- Do not use `/fair` outside NBA.
- Do not turn one concrete event question into a large scan unless the user asked for scanning.

## API Order Of Operations

Read [`references/agent-api.md`](references/agent-api.md) before using the API.

### NBA Opportunity Scan

1. Call `GET /api/v1/agent/markets` with NBA scope and an explicit time window.
2. Filter to the locally tradable universe first.
3. Split candidates by market family before ranking.
   - At minimum do not mix:
     - moneyline / winner
     - spread
     - total
     - props
4. Use list responses only for coarse filtering.
5. For the strongest few candidates in each pool, call:
   - `GET /api/v1/agent/markets/{market_id}/fair`
   - `GET /api/v1/agent/markets/{market_id}/check`
6. Rank only on executable price, not theoretical mid:
   - YES side uses `best_ask_yes`
   - NO side uses `best_ask_no`
7. Prefer markets with:
   - `data_status = tradable`
   - positive edge versus ask
   - tighter spreads
   - fresher data
8. Avoid concentration:
   - if multiple candidates come from the same event, prefer only the strongest one unless there is a strong reason to keep more
9. Auto-deepen at most `1-2` borderline but interesting markets with `orderbook` if needed.
10. Return a compact prioritized review list and stop.

### Universal Deep Analysis

1. Resolve the exact `market_id`.
2. Call:
   - `GET /api/v1/agent/markets/{market_id}/fair`
   - `GET /api/v1/agent/markets/{market_id}/orderbook`
   - `GET /api/v1/agent/markets/{market_id}/check`
3. If event-level context is needed, first resolve official metadata with:
   - `GET /api/v1/agent/events`
   - `GET /api/v1/agent/events/{event_id}`
   - `GET /api/v1/agent/events/{event_id}/markets`
4. Compare fair to executable ask on both sides when fair exists.
5. If fair is missing or weak, continue with structure-driven analysis instead of failing the whole task.
6. Classify the market as:
   - `high_priority_review`
   - `watch`
   - `low_priority`
7. Return one compact structured analysis block and stop.

### NBA Fair Shortcut

When the user explicitly asks for `/fair` on an NBA market:

1. Resolve the exact `market_id`.
2. Call `GET /api/v1/agent/markets/{market_id}/fair`.
3. If needed for execution context, also call:
   - `GET /api/v1/agent/markets/{market_id}/orderbook`
4. Return a compact fair-price view.

Do not use this shortcut for non-NBA markets.

### Broad Discovery Outside NBA

Use this only when the user asked to scan a broad non-NBA scope.

For soccer basic markets:

1. Prefer `GET /api/v1/agent/markets?market_domain=soccer5`.
2. Filter for tradable local soccer candidates first.
3. Use `fair + check` on the shortlist.
4. Stop after shortlist output unless the user asked to analyze one specific event.

For other non-NBA domains:

1. Start with `GET /api/v1/agent/events`.
2. Narrow to one promising event or a small candidate set.
3. Move quickly from event discovery to `Universal Deep Analysis`.
4. Do not stay in endless broad scanning.

## Decision-Support Rules

### NBA Scan Defaults

- Default output is a prioritized opportunity list, not a full candidate dump.
- Prefer short, decision-support phrasing over long commentary.
- If nothing stands out, say so explicitly and stop.
- Do not keep searching just to fill the list.

### Universal Analysis Defaults

- Default output is one structured analysis block for one market or event.
- For politics and other non-sports domains, focus on event structure, orderbook, tradability, and key drivers.
- For soccer, deep analysis is supported when the user points to one concrete market or event.
- If fair is unavailable, still provide a useful structure-first analysis.
- Do not try to force an NBA-style opportunity ranking onto one-off event analysis.

### Side Framing

Evaluate both sides from executable ask:

- YES edge = `fair_yes - best_ask_yes`
- NO edge = `fair_no - best_ask_no`

Only surface the stronger side for each binary market. Do not present both sides of the same binary market unless the user explicitly asks for a symmetric comparison.

### Auto-Deepen Trigger

Auto-deepen only if a candidate is near the top and one of these is true:

- edge is strong but `data_status = watch`
- spread is near the acceptable limit
- freshness is borderline stale
- there is a conflict between strong fair and weak orderbook quality

Do not auto-deepen more than 2 markets per scan.

## Cooldown And Dedup Rules

This skill is designed for repeated OpenClaw reuse. Enforce these defaults unless the caller overrides them:

- Re-scan scope cooldown: `5m`
- Same market recommendation cooldown: `15m`
- Same market deep-analysis cooldown after `low_priority`: `10m`
- Same market deep-analysis cooldown after `high_priority_review`: `15m`

Treat a market as changed enough to revisit only if one of these is materially different since the last pass:

- `fair_yes` or `fair_no`
- `best_ask_yes` or `best_ask_no`
- spread
- `data_status`
- freshness bucket

If no material change occurred, do not repeat the same output.

When possible, compare against the previous scan and classify each market as:

- `new`
- `upgraded`
- `downgraded`
- `removed`
- `unchanged`

## Stop Rules

Stop immediately when any of these is true:

- NBA opportunity scan already produced the prioritized review list
- no worthwhile review candidates remain after filtering
- a deep-analysis result reached `high_priority_review`, `watch`, or `low_priority`
- the only remaining work would repeat a recent assessment without material state change

Do not drift into open-ended commentary.

## Output Contracts

Read [`references/decision-contract.md`](references/decision-contract.md) for exact field sets.

## Important Constraints

- `/fair` is NBA-only.
- Non-NBA requests that mention `/fair` must be handled through `/analyze` logic instead of failing or pretending fair-only support exists.
- NBA scans should optimize for speed-to-shortlist, not maximum explanation depth.
- Soccer scans should use the local `soccer5` basic-market universe.
- Universal deep analysis should optimize for one target at a time.
- Convert relative windows like `today`, `tomorrow`, or `next 24h` into explicit dates and a named timezone before scanning.
- Do not expose internal fair-source routing unless the user explicitly asks.
- Do not explain direct-vs-line-shift internals by default.
- Use compact, structured output over long prose.
- If the API returns `watch` or `unpriced`, do not force a strong conclusion.
- If the market is tradable but edge is weak, classify it as `low_priority`, not a recommendation.
- Do not store API tokens in prompts or responses; keep them in the local env file and send them as a Bearer token.
- The final trading decision belongs to the user or a separate execution layer, not this skill.

## Recommended Response Headings

When responding in natural language, keep sections short:

- `Opportunity Scan`
- `Priority Markets` or `Market Analysis`
- `Pricing View`
- `Risk Notes`
- `Next Check`

The point of this skill is to help OpenClaw users discover and analyze opportunities quickly without replacing final judgment.
