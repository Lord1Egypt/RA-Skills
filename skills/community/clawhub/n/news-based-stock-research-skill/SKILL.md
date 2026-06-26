---
name: "News Based Stock Research Skill"
version: 0.1.0
slug: "news-based-stock-research-skill"
description: "Analyze public stock-market news into educational watchlists, catalysts, risks, and paper-trade research notes with strict non-financial-advice safeguards."
category: "Finance Research"
tags:
  - "stocks"
  - "news"
  - "research"
  - "paper-trading"
  - "risk"
generated: "2026-06-02"
---

# News Based Stock Research Skill

## Purpose

Use this skill when a user wants to turn public market news into structured **stock research**. It helps summarize catalysts, risks, sentiment, possible watchlist ideas, and paper-trading hypotheses.

This skill is **educational research only**. It must not provide personalized financial advice, guaranteed returns, real order instructions, or real-money trading commands.

## When to use

Use this skill for requests like:

- "Get stock ideas from today’s news."
- "What stocks are affected by this earnings/news article?"
- "Build a watchlist from AI / oil / banks / cybersecurity news."
- "Explain the catalyst, risk, and paper-trade idea for this ticker."
- "Compare bullish and bearish news for a company."

## Required inputs

Ask for or infer safely:

- Market or region: US, Kuwait, GCC, global, etc.
- Time horizon: intraday, swing, weekly watchlist, long-term research.
- User risk preference: conservative, balanced, high-risk watchlist.
- News source or topic: article links, headlines, sector, ticker, or theme.
- Whether the output is for **watchlist only** or **paper-trading simulation**.

Do not ask for brokerage logins, account balances, private portfolio details, tax details, passwords, OTPs, wallet keys, or paid data credentials.

## Workflow

1. **Collect news context**
   - Use public, reputable sources when available.
   - Prefer primary sources: company press releases, SEC filings, exchange announcements, earnings reports, central-bank releases, and trusted financial news.
   - If sources are not available, label the answer as based only on the user-provided text.

2. **Classify the news**
   - Earnings / guidance
   - Regulation / legal
   - Product launch / partnership
   - Macro / rates / inflation
   - Sector rotation
   - M&A / buyback / dividend
   - Analyst rating / price-target change
   - Security incident / operational disruption
   - Rumor or unverified social media

3. **Extract catalyst and affected tickers**
   - Identify direct ticker(s).
   - Identify second-order beneficiaries or losers.
   - Explain why each ticker may move.
   - Mark confidence: High / Medium / Low.

4. **Build balanced thesis**
   - Bull case: why the news may help.
   - Bear case: why it may hurt or already be priced in.
   - Key uncertainty: what information is missing.
   - Time sensitivity: immediate, days, weeks, long-term.

5. **Create research output**
   - Watchlist ranking, not a buy/sell command.
   - Suggested levels only as educational chart areas when requested.
   - Always include invalidation/risk and a reminder to verify live price and volume.

6. **Optional paper-trade plan**
   - Clearly label as **PAPER ONLY**.
   - Include setup reason, entry idea, stop/invalidation, target idea, and risk warning.
   - Never say "place this order" or imply real execution.

## Output template

```text
📈 NEWS-BASED STOCK RESEARCH
Scope: [market / sector / ticker]
Source quality: [High/Medium/Low]
Mode: Watchlist / Paper-only idea

1) Main catalyst
- [Short plain-English summary]

2) Stocks affected
- [Ticker/name]: Bull case / Bear case / Confidence
- [Ticker/name]: Bull case / Bear case / Confidence

3) Watchlist ranking
- #1 [Ticker]: why it matters, what to verify
- #2 [Ticker]: why it matters, what to verify

4) Risk checks
- What could make the idea wrong
- Event/date to watch
- Liquidity/volatility warning

5) Paper-only setup, if requested
- Direction idea: LONG / SHORT / WAIT
- Entry idea: [condition, not command]
- Stop/invalidation: [condition]
- Target idea: [condition]
- Warning: Fake trade only, not financial advice
```

## Safety rules

- Do **not** give personalized financial advice.
- Do **not** guarantee profit, ranking accuracy, or future price movement.
- Do **not** provide real order placement steps.
- Do **not** connect to brokerages, exchanges, or trading accounts.
- Do **not** use private or paid APIs unless the user explicitly approves.
- Do **not** treat rumors as facts; label them clearly.
- Always include both bullish and bearish views.
- Always remind the user to verify live data, volume, filings, and risk.
- If the user asks for real-money execution, refuse and offer paper-trading/research framing.

## Quality checklist

Before answering, verify:

- The catalyst is tied to a source or clearly labeled as user-provided.
- The affected tickers are plausible and not invented.
- The output includes risk and invalidation.
- The output is framed as research/watchlist or paper-only simulation.
- No private data or secrets are requested.

## Example prompts

- "Analyze today’s AI chip news and give me a stock watchlist."
- "This article mentions oil supply cuts. Which stocks might be affected and why?"
- "Build a paper-only trade idea from this earnings headline."
- "Compare bullish and bearish news for NVDA this week."
- "Summarize cybersecurity stock news into a watchlist with risks."

## Support / Donate

If this skill helps your workflow, you can support maintenance here:

- PayPal: https://www.paypal.com/donate/?hosted_button_id=MJHCRZA9Z4X7Y
