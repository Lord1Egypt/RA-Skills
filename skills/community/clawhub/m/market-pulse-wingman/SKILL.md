---
name: market-pulse-wingman
description: Market risk co-pilot for equities. Use when you need to scan a watchlist for technical context, fresh headlines, and operational/security red flags, then log a disciplined trading recommendation with follow-up notes.
emoji: "🕵️‍♂️"
---

# Market Pulse Wingman

## Overview
Use this skill when the user wants a fast but disciplined read on one or more tickers. It blends the day-trading workflow (trend, catalysts, sizing) with a security-auditor pass over current headlines and finally writes a short log entry for the self-improvement tracker.

## Quick start
1. **Collect context** from the user:
   - Tickers (and optional notes: position size, time horizon, risk tolerance)
   - Any data they already have (price, % change, headlines). If nothing is provided, ask for a watchlist snapshot or proceed with publicly available info.
2. **For each ticker**, run the structured workflow below and append the result.
3. **End with a log template** (filled out or ready for the user to confirm).

## Workflow per ticker
1. **Baseline snapshot**
   - Price, daily % change, volume vs. average, ATR/volatility context, near-term catalysts (earnings date, macro event, options expiry).
   - Mention trend bias (e.g., above/below 20/50 EMA, range-bound) using day-trading-skill language.
2. **Risk + headline sweep**
   - Scan recent news or user-provided headlines for OWASP/security/operational issues: breaches, lawsuits, product recalls, downgrades, exec exits.
   - Tag the severity (⚠️ moderate risk, 🚨 major risk) and cite the source + timestamp.
3. **Bot recommendation**
   - Combine technical + risk view into one clear nudge: e.g., "Trim size into earnings," "Allowed to add on pullbacks," "Stand aside until breach story is verified."
   - Include a quick contingency (“invalidated if price loses $X” or “if additional breach details emerge”).
4. **Decision log**
   - Generate a short entry so the user can drop it in the self-improvement tracker:
     ```
     - Ticker: XYZ
       - Date: 2026-04-16
       - Bot take: ⚠️ Hold until post-earnings volatility settles.
       - Planned action: _____
       - Follow-up reminder: Recheck headlines + price 2026-04-18.
     ```

## Output format
```
## Market Pulse — 16 Apr 2026

### Ticker: XYZ
- Price: $123.45 (+1.8% / vol 1.3× avg) | Earnings: Apr 19 | ATR: 3.2
- Setup: Uptrend holding 21EMA; buyers defending $120 gap.
- Risk flags: 🚨 Data breach rumor (TechCrunch, 4h ago) + class-action chatter.
- Bot take: Trim to core until breach story is confirmed; re-add only above $126 on volume.
- Log: (prefill template for user)
```
Add additional tickers as separate sections.

## Data & tooling notes
- If no live API is available, rely on whatever data the user gives plus broadly known info (earnings calendar, macro events). Be explicit about assumptions.
- Headlines can be summarized manually from user paste or recent articles; cite source + time.
- Keep the total response compact—2–4 bullet lines per ticker plus the log template.

## References
- `references/` can store future templates (e.g., logging schema, API hints). Currently unused; delete if not needed later.
