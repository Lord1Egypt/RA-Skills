# Cron Prompt for 15-Minute Scan

Use this as the payload message for the OpenClaw cron job:

---

Kalshi 15-min review. API credentials at ~/.kalshi/key_id.txt and ~/.kalshi/private_key.pem. Base URL: https://api.elections.kalshi.com

**RESEARCH:** Use web_fetch only (no web_search unless no known URL exists).
Data sources: gasprices.aaa.com, whitehouse.gov/presidential-actions, api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd, wttr.in/CityName?format=3, congress.gov

**EXIT RULE:** Exit a position ONLY if current bid >= your fair value estimate (net of exit fee). No stop losses — price drops alone are not a reason to exit. If price dropped significantly, research whether the underlying facts changed first.

**ENTRY RULE:** Only place a trade if EV IRR >= 50% post-fee:
edge = fair_value - (market_price + entry_fee)
EV IRR = (edge / entry_cost) × (365 / days)

**SIZING:** Half Kelly — kelly_fraction = (edge/price) × 0.5, max 20% of balance per trade.

Steps:
1. Check each open position's current bid vs your fair value. Exit any at or above fair value (net of fees).
2. If any position dropped >15%, fetch relevant data URLs to check if fundamentals changed. Exit only if new evidence shows the outcome is unlikely.
3. Scan markets closing within 7 days (volume >500, spread <10%). For each candidate, fetch data from known URLs to estimate fair value. Calculate EV IRR. Place if >= 50%.
4. Report format on every update: Cash | Position cost | Market value | Unrealized P&L | Fees paid | Total portfolio.
5. Notify user only if a trade was placed or exited.
