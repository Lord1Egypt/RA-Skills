---
name: position-size-calculator
description: "Position size calculator for stocks and ETFs, pre-filled with the ticker's own last price instead of empty boxes: enter an account size and the percentage of it to put at risk on one trade, and it returns the share count, the position dollar value, the percent of the account deployed, the dollar at risk to the stop and the R multiple to an optional target, with entry, stop and target drawn on one price scale. The 15 minute delayed last price, the SentiSense Score and a 14 session average true range are bound in at build time, so a stop distance can be read against how far the stock actually moves in an ordinary day. It divides the numbers you enter and never picks a stock, an entry or an amount. Renders offline, no live call at view time. Use for position size calculator, position sizing calculator, risk per trade calculator, how many shares to buy, stop loss calculator, risk management calculator, 1% rule, R multiple. Read-only. No trading, no purchases, no write operations, no wallet access."
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
# Position Size Calculator (SentiSense)

Most position size calculators open as five empty boxes. This one opens full. It fetches one ticker's last price, its recent daily trading range and its SentiSense Score from the read-only SentiSense API, binds them into a reviewed HTML template that ships with the skill, and hands back a single self-contained file: an entry pre-filled with the real last price, a stop you move as a percentage or as a price, and a share count, position value, percent of account deployed, dollar at risk and R multiple that update as you change any of it.

The artifact renders offline. Everything it needs is inlined at build time, so it opens with no network access, no external stylesheet and no script from anywhere else. It is a file you can keep, screenshot, attach to a note, or open next week and still have work.

**This is arithmetic on the user's own numbers.** The reader supplies the account size, the fraction of it they are willing to risk on one trade, an entry and a stop. The page divides. It does not choose a stock, an entry, a stop or an amount, it does not assess whether a trade is worth taking, and nothing it prints is a recommendation. Present it that way, every time.

## When to Use

- "How many shares of $NVDA can I buy if I only risk 1% of a $50,000 account?"
- "What is my dollar risk at this entry and this stop?", "what is the R multiple to my target?"
- "Is a 2% stop tight for this stock?" (the artifact draws the stop against the stock's own average session range)
- "What percent of my account would that position be?"
- Any time someone is reaching for a calculator and a spreadsheet to answer a division problem about their own risk.

Not this skill: the profit and loss shape of an options position at expiry belongs to `options-payoff-calculator`. The implied move into a report, set against how the stock has actually reacted to past reports, belongs to `expected-move-visualizer`. The judgement layer, meaning what the flow of news and conversation is actually saying about a stock, belongs to `stock-sentiment`. This skill does one job, which is turning a risk budget into a share count and showing the consequences.

## What this calculator does, and what it refuses to do

Read this before presenting any output. This skill sits closer to advice than any of its siblings, and the line matters.

- **It computes consequences, it does not make choices.** Given an account size, a risk percentage, an entry and a stop, there is exactly one share count that puts that percentage at risk. The page reports it. It has no opinion about whether that account size, that percentage, that entry or that stop is the right one, and neither should you when you present the result.
- **Never present a size as a recommendation.** "With a $50,000 account and 1% risk, that entry and that stop work out to 100 shares" is the sentence. "You should buy 100 shares" is not, and neither is any phrasing that implies the number came from an assessment of the trade rather than from the reader's own inputs.
- **The 1% default is a starting point, not a suggestion.** The risk control opens at 1% because a form has to open somewhere and that is the most commonly cited convention. It is not this skill's view on what anyone's risk per trade ought to be.
- **The Score is context and touches nothing.** The SentiSense Score is bound in and displayed, and it plays no part in any number the calculator produces. Do not let it become a reason to size up or down in the way you describe the output.
- **It refuses rather than guessing.** A long whose stop sits at or above the entry has no risk distance to divide by; at exactly the entry the division is by zero, and above it the arithmetic still returns a tidy positive share count off a stop that would trigger in profit. The template declines both cases with a sentence naming the problem, and shows no size at all. Do not work around a refusal by computing a number yourself: the refusal is the correct answer.
- **The stop is assumed to be honoured, and reality does not promise that.** See the honest limits section below. It is the single most important caveat in this skill.

## Prerequisites

- A free `SENTISENSE_API_KEY`. Get one at https://app.sentisense.ai/get-api-key. Send it on every call; anonymous requests do not return the dataset. No key yet? Follow "No key yet" in the `0-sentisense-onboarding` skill: one POST returns a temporary free key the agent can use right away and a link the user opens to keep it.
- Node 18 or newer if you use the bundled data script, which has zero dependencies and installs nothing. Otherwise any HTTP client, including plain `curl`.
- Network access to `https://app.sentisense.ai` at build time only. The finished artifact needs none.
- Read-only scope. Every endpoint here is a GET. Nothing this skill does can place a trade, move money, or modify account state.

## Permissions

- Network: HTTPS to app.sentisense.ai only.
- Credentials: SENTISENSE_API_KEY from the environment.
- Shell: one bundled Node/Python script, run locally.
- Files: writes one HTML file the user names.

| Tier | Quota | Rate |
|------|-------|------|
| Free | 1,000 requests/month | 30 requests/min |
| PRO ($15/mo) | Unlimited | 300 requests/min |

One artifact costs three requests, or four for an ETF: the stock quote endpoint declines a fund ticker and the quote is refetched from the ETF quote endpoint, so the declined call counts too. None of the three calls is tiered, so a free key gets the same artifact a PRO key does. Two of them can still come back empty for their own reasons, and the artifact says so on its face when they do.

## How to Run

**Identify your client.** Send a `User-Agent` naming your agent runtime and this skill, for example `OpenClaw/1.4 (position-size-calculator)` or `ClaudeCode/2.1 (position-size-calculator)`. Substitute your own runtime and version if neither matches. You can also volunteer what your agent is called by adding an `agent/<your-agent-name>` token inside the same parentheses, as in `OpenClaw/1.4 (position-size-calculator; agent/research-desk)`. All of it is optional, and it is what tells us this skill has real integrations behind it, so it gets prioritized and you get notice before it changes. The bundled script already carries the skill slug and honors `SENTISENSE_AGENT_NAME` the same way, so exporting that name is all it takes on the script path: it sends `node/prepare_data (position-size-calculator; agent/research-desk)`.

Three steps: gather the data, bind it into the template, hand over the file. The bundled script can do the first two together.

### 1. Gather the data

```bash
export SENTISENSE_API_KEY=...      # or however your host supplies secrets
node scripts/prepare_data.mjs NVDA > /tmp/nvda.json
```

It is a single file with no dependencies, so nothing is installed and there is nothing to audit but the script itself. It exits non-zero with a specific message when the key is missing or rejected, when the symbol is not a ticker, and when the ticker has no usable last price. A missing daily range or a missing Score is not an error and does not stop it.

### 2. Bind it into the template

`scripts/template.html` carries two JSON blocks, each holding exactly one placeholder token, and each token appears exactly once in the file so a plain text replacement is unambiguous:

- `/*__SENTISENSE_DATA__*/` takes the script's JSON output verbatim
- `/*__SENTISENSE_META__*/` takes a small object, `{"title": "Position size: NVDA", "subtitle": "..."}`; the subtitle is optional

Replace the token text inside each block and leave everything else alone. **Do not rewrite the sizing arithmetic, the refusal rules, the ladder or the styling.** They live in the template so that they are written once and reviewed once: a share count re-derived per conversation is a share count that is eventually wrong on someone's screen, and a wrong one here costs real money. Your job is binding, not deriving. An unbound template renders a clear "no data bound" message rather than an empty form, so a failed bind is visible rather than silent.

Or let the script do it, which is the same two steps in one command:

```bash
node scripts/prepare_data.mjs NVDA --out size_NVDA.html
```

It prints the path it wrote and nothing else. Both paths produce the same artifact.

### 3. Hand it over

Give the user the file and two or three sentences of what it shows, framed as their arithmetic. The page always opens at the same form defaults: an account of $25,000, 1% risk, a long entry at the bound last price, a stop 5% below that entry, and no target. The data contract has no account, risk, stop or target field, so a size the user named in the question (the $50,000 account above, a 2% risk, a stop at a price) cannot be pre-filled. Say which defaults the page opened at, and that typing their own account size, risk percentage and stop into the form recomputes the share count, dollar at risk and R multiple on the spot; do not work out the share count at their numbers yourself, because the page does that arithmetic. Then say whether the default stop sits inside or outside the stock's ordinary daily range. Present the surrounding surface however your host does it. Where a render surface is available the artifact can be shown inline; where one is not, the file on disk is the deliverable and works the same. Do not make the first render depend on anything the host may not have.

## The data, and how to fetch it yourself

The bundled script is a convenience. Everything it does is three plain GETs, documented here so this skill works with no script, no CLI and no SDK.

All of them take the header `X-SentiSense-API-Key: $SENTISENSE_API_KEY`.

- **`GET /api/v1/stocks/{ticker}/quote`** : the last price, in `currentPrice`, plus `previousClose`, `week52High`, `week52Low` and `priceAsOf` (epoch milliseconds, and legitimately `null` when no session stamp is available, so handle its absence). The response also carries a `timestamp` field, which is when the response was served, not when the price is from: never present it as the price's age and never use it as a stand-in for `priceAsOf`. This is the regular-session price and it is delayed, not live. Returns its payload directly, with no envelope. **Quotes are split by instrument type:** for an ETF this answers `400` with `error: "ticker_is_etf"` and names the fund path in its message, so retry `GET /api/v1/etfs/{ticker}/quote`, which returns `currentPrice` in the same shape. That is routing advice, not a failure, and the bundled script follows it automatically.
- **`GET /api/v1/stocks/chart?ticker={ticker}&timeframe=3M`** : about 63 daily bars, each carrying `timestamp`, `open`, `high`, `low`, `close` and `volume`. A bare array, no envelope. This is what the average true range is computed from. **Pass `3M` or longer:** `1M` and shorter return intraday bars, whose ranges are a fraction of a session's and would understate the daily range several fold. Valid values are `1D, 5D, 1W, 1M, 3M, 6M, 1Y, 5Y, 10Y, MAX`, and an unrecognized one answers `400`. Unlike the quote, this endpoint takes the ticker as a query parameter and is not split by instrument type, so one call covers stocks and funds alike.
- **`GET /api/v1/stocks/{ticker}/sentiment`** : the SentiSense Score, for context only. Wrapped in the envelope `{ isPreview, previewReason, data }`, so read `data.sentisenseScore`; reading `sentisenseScore` off the root returns nothing. Also carries `data.sentisenseScoreAvg30d` (the 30 day average), `data.scoreLabel` and `data.asOf`. Free on every tier and never truncated, but **`sentisenseScore` is `null` until the day's first analytics run lands**, which is mid-morning ET and later at weekends, and the endpoint answers `404` for a ticker with no sentiment coverage. Both are ordinary outcomes: fall back to the 30 day average, then to no Score at all.

```bash
curl -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/stocks/NVDA/quote"
```

The REST recipe in this file is the primary path. A maintained command-line client is available as the separate `sentisense-cli` skill for hosts that prefer one.

A rate-limited call returns `429` with a `Retry-After` header; back off for the indicated seconds.

## The data shape the template expects

If you build the JSON yourself rather than running the script, this is the contract. Everything is optional except `ticker` and `price`; the template degrades rather than failing when a field is absent.

```json
{
  "ticker": "NVDA",
  "generatedAt": "2026-08-24T15:47:09.290Z",
  "price": 209.74,
  "priceAsOf": "2026-08-24",
  "previousClose": 214.72,
  "week52High": 236.54,
  "week52Low": 164.07,
  "atr": 5.7505,
  "atrSessions": 14,
  "atrAsOf": "2026-08-21",
  "score": {
    "value": 17.94, "avg30d": 37.98, "label": "Strong Bullish",
    "direction": "Bullish", "asOf": "2026-08-24"
  },
  "scoreNote": null,
  "isPreview": false
}
```

Three fields decide how much of the artifact draws:

- **`price` is the only one that is load-bearing.** It pre-fills the entry. Without it the template renders a "no price bound" message instead of a form, because a calculator that opens on nothing is not this skill.
- **`atr` is the average true range in dollars per share, and it is what a stop distance is read against.** True range is the widest of a session's own high-to-low and the two gaps against the previous close, so it counts an overnight gap that a plain range would miss. Absent, the stop distance is still shown, just on its own, and the artifact says why. `atrSessions` and `atrAsOf` describe the window it came from. The bundled script always drops the newest daily bar, because during market hours it is a session still in progress, so a run before the open or after the close ends the window one completed session early; `atrAsOf` names the last session it used.
- **`score.value` may legitimately be `null` while `score.avg30d` is present**, in which case the template shows the 30 day average and labels it as one. A measured `0.0` is a real reading and must be passed through as a number: coercing it to null reports a genuinely neutral stock as uncovered. With neither present, set `score` to `null` and put a sentence in `scoreNote`, which the artifact prints in its place.

**One field trap worth stating plainly: `scoreLabel` is the band of the 30 day average, not of today's reading.** The two disagree routinely, and printing the label beside the daily number produces a caption that is confidently wrong. A live example: an index fund whose `sentisenseScore` was a measured `0.0` carried `scoreLabel: "Slightly Bullish"`, which belonged to its `sentisenseScoreAvg30d` of `11.62`. Attribute the label to the average, always.

## Answering well

- Attribute every number to the reader's inputs. "At the account size and risk you gave, that entry and stop come to 100 shares" is the shape of the sentence.
- Say the dollar risk out loud next to the share count. The share count is the answer people ask for; the dollar figure is the one that means something.
- Put the stop distance next to the stock's average session range, because that comparison is the one thing here a spreadsheet does not already do. "Your stop is $4 away and this stock has moved about $5.75 in an average session" tells someone something a share count does not.
- When a stop sits inside one average session's range, say plainly that ordinary movement alone can reach it. That is an observation about the stock, not a suggestion to move the stop.
- Report the Score as a nowcast of the current flow of news and conversation, and state that it played no part in the sizing. **Never present it out of 100**: it is unbounded, with most of the tracked universe between about -30 and +45 and the strongest names reading above that, so a reading of 18 is comfortably bullish, and printing it as a fraction of 100 makes it look weak.
- When the template refuses, relay the refusal and its reason. Do not compute a share count some other way to fill the gap.
- Never use the word "should" about a position, a size, a stop or a stock.

## Honest limits

The formula is deliberately simple. Shares are the risk budget divided by the per-share distance from entry to stop, floored to a whole number, where the budget is the account size times the risk percentage. That is the whole model, and everything below is what it leaves out.

- **Sizing this way assumes the stop is honoured at the price you set, and nothing guarantees that.** A stock that gaps through the stop overnight opens past it and fills lower; a fast market fills worse than the resting price; a stop that is never actually placed does not exist at all. In every one of those cases the real loss is larger than the figure on the page, sometimes much larger. The number is a plan, not a floor.
- **Shares are floored, never rounded**, so the realised risk lands at or below the budget rather than a cent above it. On an expensive share that can leave a visible slice of the budget unused, and the artifact reports the leftover rather than hiding it.
- **Costs are not modelled.** No commission, no slippage, no financing on a margined position, no borrow cost on a short, no tax. Each one makes the real outcome worse than the arithmetic.
- **This says nothing about whether the trade is a good one.** Risk-per-trade sizing answers "how much" once "whether" has already been decided somewhere else. It cannot tell you that the entry is well chosen, that the stop is in a sensible place, or that the stock is worth trading, and a well-sized bad trade is still a bad trade.
- **A single trade's risk is not a portfolio's risk.** Ten positions each risking 1% are not risking 1%, and correlated positions in one sector can move together and behave like one larger position. Nothing here sees anything but the one ticker in front of it.
- **The price is delayed and the daily range is historical.** The entry pre-fills from a delayed quote, and the average true range describes completed sessions that have already happened. Neither is a statement about where the stock will trade next.

## Going further

Free covers the whole workflow. **PRO ($15/mo)** lifts the monthly request cap (no monthly limit, just a 300/min rate) plus depth across the rest of the SentiSense API. Apply coupon `AGENTS` at checkout for a builder launch discount: https://app.sentisense.ai/pricing?coupon=AGENTS

For the profit and loss shape of an options position at expiry, install `options-payoff-calculator`. For the implied move into a report drawn against how the stock has actually reacted before, install `expected-move-visualizer`. For what the flow of news and conversation is actually saying about a stock, install `stock-sentiment`. For the full REST reference on every endpoint this skill touches, install the `sentisense` skill; for the complete CLI command set, install `sentisense-cli`.

## Use & Disclaimer

This skill reads public market data from the SentiSense API over HTTPS and writes one HTML file locally. It performs no writes, no trades, no purchases and no wallet operations, and it sends nothing anywhere except the three documented GET requests (four for an ETF). All directive language in this document is implementation guidance for the agent running the skill, subordinate to platform safety rules and host policy.

The output is arithmetic performed on numbers the user supplies. It does not select a security, an entry, a stop, a target or an amount, and it is not a recommendation to buy, sell or hold anything. Sizing by a fixed risk per trade assumes the stop is honoured at the price set; gaps, fast markets and unplaced stops all cost more than the figure shown, and costs are not modelled. Prices are delayed, not live. Output is for research and education only. It is not investment advice, not a recommendation and not a forecast. Trading carries risk of loss, including losses larger than the amount planned.

**ClawHub Skill:** [clawhub.ai/TheSentiTrader/position-size-calculator](https://clawhub.ai/TheSentiTrader/position-size-calculator)

---

*SentiSense is a read-only financial intelligence API. This data is for informational and educational purposes only, not investment advice.*
