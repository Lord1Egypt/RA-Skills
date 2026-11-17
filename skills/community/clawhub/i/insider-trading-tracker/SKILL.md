---
name: insider-trading-tracker
description: "Track insider trading from SEC Form 4 filings: insider buying and selling by ticker, market-wide insider activity, cluster buy signals where 3 or more insiders buy the same stock, and 10b5-1 plan detection for officer, director, and 10% owner trades. Use for insider trading data, Form 4 filings, insider buying by ticker, who is selling their own stock, insider cluster buys, CEO stock purchases, insider trading API. Read-only. No trading, no purchases, no write operations, no wallet access."
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
# Insider Trading Tracker (SentiSense)

Track what company insiders are doing with their own stock. This skill reads SEC Form 4 filings, the disclosures that officers, directors, and 10%+ shareholders must file within two business days of any transaction, through the read-only SentiSense API: the insider tape for a single stock, market-wide insider buying and selling, and cluster buy signals where three or more insiders bought the same name. It completes the smart-money triangle with `politicians-stock-tracker` (congressional trades) and `institutional-13f-tracker` (fund holdings).

Read-only educational data interface. Output is informational context, never a personalized buy or sell recommendation.

## When to Use

Reach for this skill when the question is about insider activity:

- "Any insider buying in $TSLA?" or "show me the Form 4 filings for this stock"
- "Which stocks are insiders buying right now?" (market-wide activity)
- "Are there cluster buys?" (3+ distinct insiders buying the same stock, a pattern long studied in academic research)
- "Is the CEO selling?" and "was that sale pre-planned or discretionary?" (10b5-1 detection)
- As the third leg of a convergence check: insider buys lining up with congressional purchases (`politicians-stock-tracker`) or institutional accumulation (`institutional-13f-tracker`) on the same ticker.

Do not use it for order entry, portfolio management, or personalized advice. It has no write, trading, or wallet surface; every endpoint is a GET.

## What this data actually is (read before interpreting)

- **Form 4 rows are individual filed transactions, newest first, not a net position.** A single insider can file many rows in one window; sum and net them before characterizing activity.
- **Each row carries both a raw SEC `transactionCode` and a simplified `transactionType`.** The common codes: `P` (open-market purchase), `S` (open-market sale), `A` (award), `M` (exercise), `G` (gift), `F` (shares withheld to cover taxes on vesting). You will also meet the rest of the SEC Form 4 code table in live data: `C` (conversion), `D` (disposition to the issuer), `H` (expiration), `I` (discretionary transaction), `J` (other acquisition or disposition), and occasionally a blank. Types: `BUY`, `SELL`, `EXERCISE`, `AWARD`, `GIFT`, `OTHER`.
- **Only codes `P` and `S` are open-market, directional signals; treat every other code as corporate mechanics.** Filter inclusively (keep P and S) rather than trying to exclude a list you might not have all of. Two refinements: **code `F` arrives typed `SELL`** but is mechanical tax withholding on vesting, not a decision to sell, so drop code-F rows from sell tallies; and awards and exercises can carry very large dollar values (RSU grants and option exercises in the hundreds of millions or more), which is exactly why leaving them in a "sold" figure is so misleading.
- **`rule10b51: true` means the trade ran under a confirmed pre-arranged 10b5-1 plan.** A scheduled sale says far less than a discretionary one; say which kind you are reporting. The flag is `false` when plan status could not be confirmed, so treat it as "confirmed plan" vs "not confirmed", not a clean either-or.
- **Who is trading matters as much as how much.** `insiderRelation` is `OFFICER`, `DIRECTOR`, `TEN_PCT_OWNER`, or `OTHER`, with `officer` / `director` / `tenPctOwner` booleans since one filer can hold several roles. A 10% owner is often an investment vehicle, not management.
- **`securityBasis` marks a row filed in a different security than the US listing, and those rows have no `pricePerShare`.** It is null on an ordinary domestic filing and carries a label such as `Common Shares (2330.TW)` when a foreign issuer's insiders file in the home-market ordinary shares behind the US listing rather than in the listed line itself. On those rows `pricePerShare` is **null by design** while `totalValue` is still real. That gives a null price two different meanings, so read `securityBasis` before you explain one: with a basis set it means the row is priced in another security, and only with `securityBasis` null does a null price mean the $0-award case. Common enough to matter on a real board rather than a corner case, and it clusters by issuer: on TSM over a 365-day window, 193 of 209 rows carried the basis, every one of them with a null price, 170 of them code `P` open-market purchases and 172 with a non-zero `totalValue`. When you report one, name the basis in the sentence so the reader knows the share count is not in the US line, and do not derive an implied per-share price by dividing `totalValue` by `sharesTransacted`; the two are not necessarily quoted in the same security.
- **Dates:** `transactionDate` is when they traded, `filedDate` is when the SEC received it (at most two business days later, far tighter than the 45-day congressional lag).

## Prerequisites

- A free `SENTISENSE_API_KEY`. Get one at https://app.sentisense.ai/get-api-key. Send it on every call: a request without a valid key gets at most a shaped crawler-facing preview slice, never the dataset, and that fallback is not a contract you can build on. No key yet? Follow "No key yet" in the `0-sentisense-onboarding` skill: one POST returns a temporary free key the agent can use right away and a link the user opens to keep it.
- Any HTTP client. Plain `curl` works, or Python 3.8+ using only the standard library.
- Network access to `https://app.sentisense.ai`.
- Read-only scope. Every endpoint here is a GET. Nothing this skill does can place a trade, move money, or modify account state.

| Tier | Quota | Rate | Insider data |
|------|-------|------|--------------|
| Free | 1,000 requests/month | 30 requests/min | preview slice (top 5 per endpoint); full window on the per-stock tape for the sample companies |
| PRO ($15/mo) | Unlimited | 300 requests/min | full window you ask for |

The free tier exercises every workflow below; preview-gated endpoints return a truncated but real slice on a free key. Full data on a set of sample companies is free: for those tickers `/insider/trades/{ticker}` returns the whole window on a free key, marked `sampleCompany: true` on the envelope next to `isPreview`. The market-wide `/insider/activity` and `/insider/cluster-buys` stay at the top 5 either way. Read the list from `upgrade.sampleTickers` on a per-stock preview, or see https://sentisense.ai/docs/api/#full-sample-responses-with-a-free-key. The first example below uses TSLA, one of them.

## Permissions

- Network: HTTPS to app.sentisense.ai only.
- Credentials: SENTISENSE_API_KEY from the environment.
- Shell: none required.
- Files: none.

## How to Run

The REST recipe in this file is the primary path. A maintained command-line client is available as the separate `sentisense-cli` skill for hosts that prefer one.

**Identify your client.** Send a `User-Agent` naming your agent runtime and this skill, for example `OpenClaw/1.4 (insider-trading-tracker)` or `ClaudeCode/2.1 (insider-trading-tracker)`. Substitute your own runtime and version if neither matches. You can also volunteer what your agent is called by adding an `agent/<your-agent-name>` token inside the same parentheses, as in `OpenClaw/1.4 (insider-trading-tracker; agent/research-desk)`. All of it is optional, and it is what tells us this skill has real integrations behind it, so it gets prioritized and you get notice before it changes.

The market-wide endpoints are plain REST. All three endpoints return the wrapped envelope `{ isPreview, previewReason, data }`; read `.data`. When `isPreview` is true and `totalCount` is above the rows you received, say so ("showing the free preview slice"); a preview that already holds every row truncated nothing. `sampleCompany` appears only when it is true, so read a missing field as false. On `/insider/activity`, `totalCount` counts buys and sells together, so it is not a number of buy signals. A rate-limited call returns `429` with a `Retry-After` header; back off for the indicated seconds.

## Endpoints

- **`GET /api/v1/insider/trades/{ticker}`** : individual Form 4 transactions for one stock, newest first. Query `lookbackDays` (1-365, default 90). Free: top 5, except on a sample company, which gets the full window; PRO: full window. Each row: `insiderName`, `insiderTitle`, `insiderRelation`, `officer`, `director`, `tenPctOwner`, `transactionDate`, `filedDate`, `transactionCode`, `transactionType`, `securityTitle`, `sharesTransacted`, `pricePerShare` (null on $0 awards, and always null when `securityBasis` is set), `totalValue`, `sharesOwnedAfter`, `directOwnership`, `rule10b51`, `securityBasis`.
- **`GET /api/v1/insider/activity`** : market-wide insider activity aggregated by ticker, split into top `buys` and top `sells` by total dollar value (`.data.buys` and `.data.sells`). Query `lookbackDays` (1-365, default 90). Each entry: `ticker`, `companyName`, `tradeCount`, `insiderCount`, `totalShares`, `totalValue`, `latestDate`, `latestInsider`, `latestTitle`. Free: top 5 per direction; PRO: full. The `sells` side already excludes code-F tax withholding server-side, so these dollars are discretionary selling and you should not filter them again; dispositions to the issuer (code `D`) are still counted.
- **`GET /api/v1/insider/cluster-buys`** : stocks where **3 or more distinct insiders** bought within the window. Query `lookbackDays` (1-365, default 90). Each signal: `ticker`, `companyName`, `insiderCount`, `tradeCount`, `totalShares`, `totalValue`, `firstBuyDate`, `lastBuyDate`. Free: top 5; PRO: full.

## Workflows

**1. The insider tape for one stock**

Use: `GET /api/v1/insider/trades/TSLA?lookbackDays=365`. Insiders often trade in bursts, so a quiet 90 days is not a quiet year: ask for the full 365 when the question is about a pattern. Filter to the directional rows first (code `P` and code `S`, minus code `F`), then report: who bought and sold, their roles, net dollars, and how much of the selling was 10b5-1 planned.

Only sum a whole window. A full response (`isPreview: false`: PRO, or a free key on a sample company, marked `sampleCompany: true`) carries every row in the window, so its sums are the window's totals. On any other ticker a free key gets a preview: `isPreview` is true, `data` holds the newest 5 rows, and `totalCount` is how many rows the window holds. Describe those as "the newest 5 of `totalCount` filings" and give no window count or dollar total from them. "No insider buying" is a window claim too: the newest 5 rows cannot show it.

An all-award window is zero insider conviction, not a wave of it; say "no open-market insider activity" rather than presenting awards as trades.

**2. What are insiders buying market-wide?**

`GET /api/v1/insider/activity?lookbackDays=30`, then read `.data.buys`. Check `insiderCount` before crowning a leader: the top row by dollars is sometimes a single 10% owner accumulating through an investment vehicle across many trades, which is a very different fact from five officers buying independently. Lead with breadth, then dollars.

**3. Cluster buys, the classic screen**

`GET /api/v1/insider/cluster-buys?lookbackDays=90`. Three or more distinct insiders buying the same stock in a window is the pattern with academic pedigree. Sanity-check `totalValue` against `insiderCount` before presenting one: a 30-insider cluster whose combined purchases are modest dollars reads very differently from three officers each writing six-figure checks.

**4. The convergence check.** The high-conviction read is agreement across independent sources: insider cluster buys plus congressional purchases (`politicians-stock-tracker`) plus institutional accumulation (`institutional-13f-tracker`) on the same ticker, ideally alongside the sentiment picture (`stock-sentiment`). Cite each source separately and say which legs agree; one leg alone is context, not a case.

## Answering well

- Always separate open-market activity from awards, gifts, exercises, and code-F tax withholding. The single most common misread of Form 4 data is presenting routine compensation mechanics as insider conviction.
- Sanity-check dollar figures before headlining them: on a row with a non-null `pricePerShare` and a null `securityBasis`, `totalValue` should roughly equal `sharesTransacted` times `pricePerShare`, and a total that dwarfs the company's market cap is a data artifact to flag, not a story to tell. **Skip the check when `securityBasis` is set or `pricePerShare` is null** rather than reporting a failure: those rows are filed in another security and have no per-share figure to multiply, so the arithmetic cannot run and its absence says nothing about the row.
- Name the role: "the CFO bought" and "a 10% owner bought" are different sentences.
- Flag 10b5-1 planned sales as scheduled, and never dramatize them.
- Quote `transactionDate` when discussing timing and `filedDate` when discussing disclosure.
- Report only what the API returns. Do not infer motives, and do not frame any of it as advice. This is public-disclosure data presented for education.

## Going further

Free covers every workflow above at a preview depth, and the per-stock tape in full for the sample companies. **PRO ($15/mo)** lifts the monthly cap (no monthly limit, just a 300/min rate) and returns the full window on every insider endpoint, plus institutional flows, congressional detail, and AI insights across the SentiSense API. Apply coupon `AGENTS` at checkout for a builder launch discount: https://app.sentisense.ai/pricing?coupon=AGENTS

For the full REST reference on every endpoint this skill touches, install the `sentisense` skill; for the complete CLI command set, install `sentisense-cli`.

**ClawHub Skill:** [clawhub.ai/TheSentiTrader/insider-trading-tracker](https://clawhub.ai/TheSentiTrader/insider-trading-tracker)

---

*SentiSense is a read-only financial intelligence API. This data is for informational and educational purposes only, not investment advice.*
