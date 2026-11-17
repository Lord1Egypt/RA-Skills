---
name: institutional-13f-tracker
description: "13F institutional ownership tracker: quarterly hedge fund and mutual fund holdings from SEC 13F filings, by ticker or by manager, with top institutional holders per stock, quarter-over-quarter buying and selling deltas, and activist investor positions across thousands of managers. Use for 13F filings, 13F holdings changes, hedge fund holdings, institutional ownership by ticker, who owns this stock, activist fund positions, and superinvestor portfolios. Read-only. No trading, no purchases, no write operations, no wallet access."
homepage: https://sentisense.ai
primaryEnv: SENTISENSE_API_KEY
metadata:
  openclaw:
    primaryEnv: SENTISENSE_API_KEY
    envVars:
      - name: SENTISENSE_API_KEY
        required: false
        description: "SentiSense API key, optional to install. Get one free at https://app.sentisense.ai/get-api-key, or with no key follow the No key yet steps in the 0-sentisense-onboarding skill for a temporary free one with no signup. Used only to authenticate read-only data calls; no write or trading scope."
---
# Institutional 13F Tracker (SentiSense)

See who owns a stock and how the big money is repositioning. This skill reads institutional ownership from SEC 13F filings through the read-only SentiSense API: the top institutional holders for any ticker, aggregate buying and selling per stock, activist positions, and a full portfolio for any manager (from Berkshire Hathaway to the largest index funds), with quarter-over-quarter change types (new, increased, decreased, sold out) across thousands of filers.

Read-only educational data interface. Output is informational context, never a personalized buy or sell recommendation.

## When to Use

Reach for this skill when the question is about institutional ownership or 13F positioning:

- "Who owns $NVDA?" or "top institutional holders of $TSLA"
- "What did Berkshire Hathaway buy and sell last quarter?" (a manager's whole portfolio)
- "What did this manager buy and sell, in dollars?" (estimated dollar flows per position and in total)
- "How has this manager's book changed over the last few years?" (filing-by-filing history)
- "Is institutional money accumulating or distributing $AAPL?" (aggregate flows)
- "Which activist funds took new positions this quarter?"
- "How did 13F ownership of $COIN change quarter over quarter?"

This skill pairs naturally with `politicians-stock-tracker` and `insider-trading-tracker`: line up 13F accumulation against a congressional purchase or an insider cluster buy on the same ticker. Convergence across sources is the high-conviction read.

Do not use it for order entry, portfolio management, or personalized advice. It has no write, trading, or wallet surface; every endpoint is a GET.

## What this data actually is (read before interpreting)

- **13F is quarterly and lagged.** Institutions file 13F-HR within 45 days after each quarter end. A quarter stays `pending: true` through the effective SEC filing deadline day in New York (that 45th day, rolled past weekends and federal holidays) and turns settled (`ownershipEligible: true`) the next calendar day. So the newest settled quarter is the quarter that just ended only once its deadline has passed; for about six weeks after each quarter end it is the one before. Never present any of it as real-time positioning.
- **Always resolve the quarter first.** The quarter-scoped feeds (`/flows`, `/activist`, `/bonds`, `/options`) need a `reportDate`. Four endpoints do not: `/quarters` is the resolver itself, `/holders/{ticker}` serves the latest settled quarter for the ticker when you omit it, echoes the one it used, and reports any newer still-filing quarter separately in `earlyFilers` rather than mixing it into the roster, `/institutions` takes an optional `quarter` (the `value` form, `2026Q2`, not a `reportDate`), and `/institution/{slugOrCik}` takes neither and answers on its own latest quarter. Through the effective filing deadline day, the newest entry is `pending: true` and holds only early filers; use the first quarter with `pending: false` for complete data. **Filter on the flag, never on position.** Once the filing window closes, the pending entry is gone and the newest quarter in the array is already complete, so code that skips index 0 on the assumption that the first row is always pending will quote a quarter that is three months staler than what you were served. Checked live on 2026-08-31: the array led with Q2 2026 at `pending: false` and contained no pending entry at all.
- **Dollar flows are estimates, not trades.** `estimatedFlowUsd`, `boughtUsd`, `trimmedUsd`, `exitedUsd` and `netFlowUsd` are worked out from two quarter-end snapshots (this filing against the one before it), so they are not reported trades and say nothing about when in the quarter anything happened. A 13F also covers long US-listed equity only: short positions, futures and non-US holdings are not in these numbers. Say both whenever you quote a dollar flow.
- **Filer categories:** `INDEX_FUND`, `HEDGE_FUND`, `ACTIVIST`, `PENSION`, `BANK`, `INSURANCE`, `MUTUAL_FUND`, `SOVEREIGN_WEALTH`, `ENDOWMENT`, `CONGLOMERATE`, `OTHER`.
- **Parent/subsidiary rollups.** Large managers file under many CIKs (e.g. Vanguard). A filer profile carries `multiCikRollup` / `childCikCount` / `childCiks` so sub-manager holdings roll up into one portfolio. Report the rollup, not double-counted child rows.
- **Report values as given.** The dollar field is **`valueUsd`** on both sides of the join: on a holder row under `/holders/{ticker}` and on a holding row inside a manager's portfolio. There is no bare `value` field on either. It arrives already denominated in US dollars, so quote it as the reported 13F value and do not re-scale or invent a unit. (`/bonds` names its own total `totalValue` and `/institutional/options` splits into `callValue` / `putValue`; those are the only other dollar keys in this family.)

## Prerequisites

- A free `SENTISENSE_API_KEY`. Get one at https://app.sentisense.ai/get-api-key. Required on every call; anonymous requests return `401 api_key_required`. No key yet? Follow "No key yet" in the `0-sentisense-onboarding` skill: one POST returns a temporary free key the agent can use right away and a link the user opens to keep it.
- Any HTTP client. Plain `curl` works, or Python 3.8+ using only the standard library. On macOS python.org installs can raise `CERTIFICATE_VERIFY_FAILED`: run `Install Certificates.command`, use the system `/usr/bin/python3`, or use `curl`.
- Network access to `https://app.sentisense.ai`.
- Read-only scope. Every endpoint here is a GET.

| Tier | Quota | Rate | 13F data |
|------|-------|------|----------|
| Free | 1,000 requests/month | 30 requests/min | preview slice (top N per endpoint) |
| PRO ($15/mo) | Unlimited | 300 requests/min | full holder lists and full portfolios |

## Permissions

- Network: HTTPS to app.sentisense.ai only.
- Credentials: SENTISENSE_API_KEY from the environment.
- Shell: none required.
- Files: none.

## How to Run

Issue HTTP GET requests to `https://app.sentisense.ai`, authenticated with the `X-SentiSense-API-Key` header. Keep the key in the shell environment; never place it in a query string or in user-facing output.

**Step 1, always: resolve the quarter.** `/quarters` is a bare array (no envelope). Every other institutional endpoint returns the wrapped envelope `{ isPreview, previewReason, data }`, so unwrap `.data` first. Unwrapping is not the same as iterating: on `/holders/{ticker}`, `/institution/{slugOrCik}`, `/institutions` and `/flows` the unwrapped `data` is an **object**, and the rows sit one level further in (`data.holders`, `data.holdings`, `data.institutions`, and `data.inflows` / `data.outflows` respectively). Check for a list before you loop. A `429` returns a `Retry-After` header; back off rather than serving a stale value.

**Identify your client.** Send a `User-Agent` naming your agent runtime and this skill, for
example `OpenClaw/1.4 (institutional-13f-tracker)` or `ClaudeCode/2.1 (institutional-13f-tracker)`. Substitute your own runtime and
version if neither matches. You can also volunteer what your agent is called by adding an
`agent/<your-agent-name>` token inside the same parentheses, as in
`OpenClaw/1.4 (institutional-13f-tracker; agent/research-desk)`. All of it is optional, and it is what tells
us this skill has real integrations behind it, so it gets prioritized and you get notice before it
changes.

```bash
# 1) get valid reporting quarters, pick the first with pending=false
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/institutional/quarters"
# -> [{ "value": "2026Q3", "label": "Q3 2026", "reportDate": "2026-09-30",
#       "pending": true, "ownershipEligible": false, "ownershipEligibleAt": "2026-11-17" }, ...]
```

## Endpoints

- **`GET /api/v1/institutional/quarters`** : available 13F reporting quarters. **Public**, bare array of `{ value, label, reportDate, pending, ownershipEligible, ownershipEligibleAt }`, newest first. `pending` is true through the effective SEC filing deadline day; `ownershipEligible` turns true the next New York calendar day, which `ownershipEligibleAt` gives as an ISO date (it does not certify that every institution filed). Call this first; use the first `pending: false` `reportDate` everywhere below.
- **`GET /api/v1/institutional/holders/{ticker}`** : institutional holders for a stock. `reportDate` is **optional here**: omit it and the endpoint serves the latest quarter that has holders for this ticker, preferring a settled quarter over a still-filing one, and tells you which one it used in `data.reportDate` (`data.selection.status` says whether it is settled). Pass `?reportDate=` from `/quarters` when you want a specific quarter or are comparing several tickers on one date. The holder list is nested at **`data.holders`** (not `data` directly). Each holder carries `filerName`, `filerCik`, `filerCategory`, `entitySlug`, `cikCount`, `shares`, `sharesChange`, `sharesChangePct`, **`valueUsd`** (the dollar field, there is no bare `value`), `changeType` (`NEW` / `INCREASED` / `DECREASED` / `SOLD_OUT` / `UNCHANGED`), and its own `comparisonStatus`. `data` always carries `holderCount` (full-quarter count). It also carries:
  - `data.selection`: `mode` (`DEFAULT` when you omitted `reportDate`, `EXPLICIT` when you passed one), `status` (`settled` or `filing`), `policyVersion`, `marketDefaultReportDate` (the newest eligible quarter market-wide) and `isStaleForMarket` (true when this ticker is served from an older quarter than that).
  - `data.earlyFilersStatus`: `AVAILABLE`, `NONE` (no newer filing quarter observed) or `UNAVAILABLE` (that supplementary read failed; the roster is still served). When `AVAILABLE`, `data.earlyFilers` describes the newer still-filing quarter: `reportDate`, `status` (`filing`), `holderCount`, `distinctFilerCount`, `baselineFilerCount` and an optional `coveragePct` (the share of this ticker's settled-quarter institutional value held by filers already confirmed for the newer quarter). Report it as an early read beside the settled roster, never blended into it.
  - `data.notableHolders` with `data.notableHoldersScope` (`full_roster`): well-known institutions holding the stock, matched against the quarter's full roster rather than the page you fetched. Free returns up to five names and identifiers only; PRO adds position and change fields. It does not expand the free `holders` preview.
  - `data.comparisonReportDate` and `data.comparisonStatus`: the prior quarter used for share changes and a conservative summary (`AVAILABLE`, `PRIOR_QUARTER_UNAVAILABLE`, `INCOMPLETE_INPUT`, `INCOMPLETE_FAMILY_COVERAGE` or `UNAVAILABLE`). The summary can read incomplete while individual rows are complete, so judge each holder by its own `comparisonStatus`: only `AVAILABLE` supports a quarter-change claim for that holder. **Paging (recommended):** pass `limit` (1-1000), `offset`, `sortBy`, `sortDir`. A mega-cap can have 5,000+ holders, and `notableChanges` (holders with a 10%+ change on 10k+ shares) plus `returnedCount` are returned **only when `limit` is passed**. Free: top 5, and free previews omit `returnedCount`, `offset`, and `notableChanges` even when `limit` is passed (`holderCount` stays the full-quarter count).
- **`GET /api/v1/institutional/flows?reportDate=`** : aggregate institutional buying/selling per ticker. **`data` is an object, not a list**, so iterating `.data` gets you nothing: the two ranked ticker arrays are at **`data.inflows`** and **`data.outflows`**, alongside `data.reportDate`, `data.filerCount`, `data.baselineFilerCount` and `data.isPending`. Each row carries `ticker`, `companyName`, `dollarFlowUsd`, `netSharesChange`, `totalSharesBought` / `totalSharesSold`, the position counts (`newPositions`, `increasedPositions`, `decreasedPositions`, `soldOutPositions`), `avgClosePrice`, and a per-category net-change breakdown (`hedgeFundNetChange`, `indexFundNetChange`, `activistNetChange`, and one per remaining filer category). Free: top 5.
- **`GET /api/v1/institutional/activist?reportDate=`** : activist-filer positions for the quarter (NEW or INCREASED stakes). Free: top 3; PRO: full.
- **`GET /api/v1/institutional/bonds?reportDate=`** : convertible bond flows grouped by base ticker, the credit-side leg of the same 13F filings. Free: top 3; PRO: full.
- **`GET /api/v1/institutional/options?reportDate=`** : institutional options positions with the call/put breakdown, as disclosed on 13F. Quarterly and end-of-quarter, not live flow. Free: top 3; PRO: full.
- **`GET /api/v1/institutional/institutions`** : the filterable universe of tracked filers (use it to find a manager's slug/CIK for the endpoint below). Query `category`, `minAumUsd`, `sort`, `quarter`. Full list on every tier, and quota-exempt.
- **`GET /api/v1/institutional/institution/{slugOrCik}`** : a single manager's profile, summary stats, and current-quarter equity holdings. Resolve by URL slug (`Berkshire-Hathaway`) or CIK of 1 to 10 digits (`1067983`, leading zeros optional). Free: profile + top 10 holdings; PRO: full holdings. Holdings include `ticker, companyName, shares, valueUsd, changeType, sharesChange, sharesChangePct, portfolioWeight`, plus `multiCikRollup` / `childCiks` for parent/subsidiary rollups. Returns 404 for an unknown slug or CIK. Paged mode (PRO) starts when you pass `limit` (1-1000) and adds `offset`, `sortBy`, `sortDir` and three filters: `changeType` (a comma list of `NEW`, `INCREASED`, `DECREASED`, `SOLD_OUT`, `UNCHANGED`, or `HELD` for every position still held), `q` (ticker or company name) and `minWeight` (percent). `sortBy` takes `valueUsd` (default), `shares`, `portfolioWeight`, `sharesChangePct`, `valueChangeUsd`, `sharesChange`, `estimatedFlowUsd` or `priorValueUsd`. Filters apply before sorting and paging, the envelope's `totalCount` counts the matches, and `data.matchTotals` sums the whole matching set (`count`, `valueUsd`, and `priorValueUsd` and `estimatedFlowUsd` when the comparison is available). Without `limit` the filters are ignored and you get the full list. `data.matchTotals` appears only when `changeType`, `q` or `minWeight` is passed, not on a sort-only page. On Free, `limit` and every filter are ignored: you get the top 10 holdings by value and no `matchTotals`, so check each row's `changeType` instead of assuming the filter applied. The count of positions held is `data.positionsHeld`; `holdingsCount` and an unfiltered `totalCount` include `SOLD_OUT` rows. Large filers return big payloads (`optionPositions` can be about 1 MB), so select only the fields you need. When `data.comparisonStatus` is `AVAILABLE` the response adds `data.priorTotalValueUsd` and `data.priorPositionsHeld`, and each holding adds `priorValueUsd`, `priorPortfolioWeight` and `estimatedFlowUsd` (positive bought, negative sold, priced at the filing's quarter-end price, so for a fast mover it can exceed the prior position's value; the value change `valueUsd - priorValueUsd` mixes price moves with trading, which is why the flow field exists).
- **`GET /api/v1/institutional/institution/{slugOrCik}/history`** : a manager's book filing by filing, newest first. Query `quarters` (1-40, default 12) and optional `tickers` (comma list, up to 100) which adds `data.positions`: per ticker, a newest-first list of `{reportDate, shares, valueUsd}` (a filing where the manager did not hold the ticker is absent from the list). Free keys get `positions` only for the manager's ten largest holdings (the tickers in the free preview of the detail endpoint); a ticker missing from a Free response may only be outside the top ten, so never say the manager does not hold it. Each row of `data.quarters` carries `reportDate`, `value`, `label`, `status` (`settled` or `filing`), `comparisonStatus`, `comparisonReportDate`, `totalValueUsd`, `positionsHeld` and `top10Pct`, and, only when its `comparisonStatus` is `AVAILABLE`, the position counts plus `boughtUsd`, `trimmedUsd`, `exitedUsd`, `netFlowUsd` (`boughtUsd - trimmedUsd - exitedUsd`) and `priceEffectUsd` (the change in `totalValueUsd` since the previous filing minus `netFlowUsd`: the remainder after trading, mostly price moves, which also absorbs rounding, the different price bases of exits and trades, and positions whose change could not be restated). API key required; PRO returns the requested window, Free the newest four filings as a preview (`isPreview: true`, `totalCount` is the size of the requested window). The first call for a large multi-filer manager can take up to about a minute, so use a 60 second client timeout (repeat calls are fast), and a `503` with `{"error": "history_busy"}` plus a `Retry-After` header means retry after that many seconds. Bad `quarters` or `tickers` return `400`; unknown manager returns 404.

## Workflows

**1. Who owns this stock?**

```bash
Q=2026-06-30  # first pending:false reportDate from /quarters
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/institutional/holders/NVDA?reportDate=$Q&limit=25"
```
Or drop `reportDate` and let the endpoint pick the ticker's latest settled quarter; `data.reportDate` and `data.selection` say which one you got. Read `data.holders` and lead with the largest holders and their `NEW` / `INCREASED` / `SOLD_OUT` change types, quoting a change only where that holder's `comparisonStatus` is `AVAILABLE`; mention `data.earlyFilers` as a separate early read of the next quarter when present; on PRO, `limit` also returns `notableChanges` (a `count` of holders that changed 10% or more on 10k+ shares, plus the `top` five of them by dollar value), while a free preview omits it, so on free read the changes off the five holders shown and never report "no notable changes".

**2. A manager's whole portfolio (what did they buy and sell?)**

```bash
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/institutional/institution/Berkshire-Hathaway"
```
Summarize new positions, adds, trims, and exits by `changeType`, and the biggest holdings by `portfolioWeight`. `portfolioWeight` is rounded to 0.1%: compute a share of the book as `valueUsd / totalValueUsd`. The count of positions held is `data.positionsHeld`, because `holdingsCount` includes `SOLD_OUT` rows.

**2b. What did this manager buy and sell, in dollars?** PRO, paged mode. Rank by the estimated dollars, not by the position's size:

```bash
B="https://app.sentisense.ai/api/v1/institutional/institution/Berkshire-Hathaway"
H="X-SentiSense-API-Key: $SENTISENSE_API_KEY"
# newly opened positions, largest first
curl -s -H "$H" "$B?limit=20&changeType=NEW&sortBy=valueUsd&sortDir=desc"
# biggest adds, then biggest sells (negative flows come first when ascending)
curl -s -H "$H" "$B?limit=20&changeType=NEW,INCREASED&sortBy=estimatedFlowUsd&sortDir=desc"
curl -s -H "$H" "$B?limit=20&changeType=DECREASED,SOLD_OUT&sortBy=estimatedFlowUsd&sortDir=asc"
# whole-quarter exits and their total
curl -s -H "$H" "$B?limit=20&changeType=SOLD_OUT"
```
Read `data.holdings[].estimatedFlowUsd` for each name and `data.matchTotals.estimatedFlowUsd` for the total over everything the filter matched, not just the page (`matchTotals` exists only when `changeType`, `q` or `minWeight` is passed, so a sort-only call has no total). On Free the filters are ignored and `matchTotals` is absent, so check each row's `changeType` yourself. Quote a flow only when `data.comparisonStatus` is `AVAILABLE`, and call it an estimate from two quarter-end snapshots priced at the filing's quarter-end price; it can exceed the prior position's value for a fast mover, and it is not cash. Do not use `valueUsd - priorValueUsd` as "dollars bought": it includes price moves.

**2c. How has this manager's book changed over time?**

```bash
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/institutional/institution/Berkshire-Hathaway/history?quarters=8&tickers=AAPL"
```
Read `data.quarters` newest first for the size of the book (`totalValueUsd`), how many names it holds (`positionsHeld`) and how concentrated it is (`top10Pct`). To explain a change in value, read the bridge: `netFlowUsd` is the estimated trading (`boughtUsd` less `trimmedUsd` and `exitedUsd`) and `priceEffectUsd` is the remainder, mostly price moves. Report it as "estimated trading explains X of the change; the rest, mostly price moves, is Y", and do not conclude that the holdings rose or fell in price from it alone. Rows whose `comparisonStatus` is not `AVAILABLE` have no flow fields; skip them rather than filling in zeros. Sanity-check the sequence before narrating it: if `totalValueUsd` or `positionsHeld` swings by more than about 50% and snaps back in the next filing, treat that filing as possibly incomplete, say so, and do not describe its flows as trading (Berkshire's 2025Q1 filing is a live example: a huge net sale followed by an equal net purchase). `data.positions` follows named tickers across filings (shares and value per filing); on Free it covers only the manager's ten largest holdings. On Free only the newest four filings arrive, so say that a longer view needs PRO.

**3. Aggregate accumulation vs distribution**

```bash
Q=2026-06-30  # first pending:false reportDate from /quarters
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/institutional/flows?reportDate=$Q"
```

Read the accumulation side from `data.inflows` and the distribution side from `data.outflows`, each already ranked by the size of `dollarFlowUsd` (negative on the outflow side). A ticker appears on the side its net quarter landed on, never on both, so read the two lists as one board rather than netting them against each other.

**4. Activist watch**

```bash
Q=2026-06-30  # first pending:false reportDate from /quarters
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/institutional/activist?reportDate=$Q"
```

**5. Follow the convergence.** When institutional accumulation lines up with a congressional purchase (`politicians-stock-tracker`) or insider buying (`insider-trading-tracker`) on the same ticker, that agreement is the read worth surfacing. Cite each source.

## Answering well

- Always state the `reportDate` you are quoting and that 13F data is a quarterly snapshot filed up to 45 days after quarter end.
- Keep the settled quarter and early filers apart: quote the roster from the settled quarter, and present `earlyFilers` (with its `coveragePct` when present) as partial coverage of the next quarter, not as the new ownership picture.
- Attribute holdings to the filer and category; roll parent/subsidiary CIKs into one manager rather than double-counting.
- Use `changeType` and `sharesChangePct` to describe direction; quote `valueUsd` as the reported 13F value without re-scaling.
- When you quote a dollar flow, say it is an estimate from two quarter-end snapshots and that a 13F covers long US equity only; never describe `netFlowUsd` or `estimatedFlowUsd` as reported trades or cash flow.
- Report only what the API returns. Do not infer positions, prices, or intent that are not in the data, and do not frame any of it as advice.

## Going further

Free covers every workflow above at a preview depth (top holders, top-10 portfolio). **PRO ($15/mo)** lifts the monthly cap (no monthly limit, just a 300/min rate) and returns full holder lists and full manager portfolios, plus congressional, insider, options, and AI-insight data across the SentiSense API. Apply coupon `AGENTS` at checkout for a builder launch discount: https://app.sentisense.ai/pricing?coupon=AGENTS

**ClawHub Skill:** [clawhub.ai/TheSentiTrader/institutional-13f-tracker](https://clawhub.ai/TheSentiTrader/institutional-13f-tracker)

---

*SentiSense is a read-only financial intelligence API. This data is for informational and educational purposes only, not investment advice.*
