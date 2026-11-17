---
name: "market-briefing-assistant"
description: "AirnodeHub market skill for current briefings, prices, news, earnings, fundamentals, indicators, portfolio checks, and company snapshots via attested Airnode POSTs."
---

# Market Briefing Assistant

## Execute

1. Extract symbols, asset class, exchange/country when ambiguous, horizon, metrics, and desired depth. Ask only when instrument identity cannot be resolved safely; otherwise default to a compact timestamped snapshot. **Done when:** instruments and scope are unambiguous.

2. Read current documentation for `https://airnode-benzinga.fly.dev/`, `https://airnode-twelvedata.fly.dev/`, and `https://airnode-tickerlayer.fly.dev/`. Use only documented POST operations, symbol formats, and limits. **Done when:** schemas, costs, and signer addresses are known.

3. Choose specialist operations: TickerLayer `snapshot` or Twelve Data `quote` for current prices; Benzinga `news` for narrow company news; Benzinga `earnings`/`earningReports` or Twelve Data `earnings` for earnings; Twelve Data `statistics` or detailed statement operations for fundamentals; and Twelve Data specialist indicator operations for RSI, MACD, ATR, Bollinger Bands, or stochastic oscillator. Keep histories and output sizes small. **Done when:** each requested category has a minimal call plan.

4. Before any paid, credentialed, subscription, or uncertain-cost POST, state the calls and cost and obtain explicit approval. Combine compatible requests and never silently expand scope. **Done when:** calls are free, approved, or blocked before cost.

5. POST `{"operation":"<operation>","parameters":{...}}` to each selected listing. Validate symbol, exchange, dates, interval, units, freshness, and whether values are live, completed bars, filed facts, estimates, or computed indicators. Prefer a second authorized specialist source for consequential price claims. **Done when:** attested data or exact blockers are available.

6. Present: **As of**, price and daily move; up to three relevant news/earnings points; requested fundamentals; technical values with interval/lookback and neutral interpretation; and material data limits. Attribute each fact to its provider via AirnodeHub. Separate facts from inference and estimates from actuals. End: `Market data can be delayed or revised; this is information, not personalized financial advice.` **Done when:** timing and uncertainty are clear.

7. Retry once after correcting a schema issue or transient failure. Use another specialist only when it answers the same category and cost approval permits. Never substitute stale recall or invented attestation data. **Done when:** the briefing or each unavailable section has a transparent blocker.

## Verification

Confirm all current data came from documented specialist POSTs, paid calls were approved, symbols/periods/intervals/units/timestamps were checked, and the envelope contains `airnode`, `requestHash`, `timestamp`, `data`, and `signature`. Cryptographically verify when tooling is available; otherwise describe the response as signed/attested, not independently verified.
