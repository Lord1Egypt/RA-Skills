# Source List

This skill works best when it combines broad market news with a few gold-specific sources.

## Preferred Source Types

- top-tier wire services
  - Reuters
  - Bloomberg
  - Dow Jones / WSJ when available
- gold-focused market media
  - Kitco
  - World Gold Council
- macro and market calendars
  - Federal Reserve
  - BLS
  - BEA
  - U.S. Treasury
  - CME FedWatch context if available
- market data and commentary
  - Investing
  - TradingEconomics
  - MarketWatch

## Practical Retrieval Note

The bundled `scripts/fetch_news.py` uses lightweight RSS-style query endpoints from Google News and Bing News because they are easy to run with no API key and no third-party package. This is a retrieval convenience, not a credibility claim. The model should still:

- prefer original publishers over aggregator text
- inspect the cited source in each item
- down-weight low-quality republishes

If one provider is blocked, rate-limited, or times out in the current environment, treat that as a partial retrieval failure rather than a market signal. The skill should say that the news pull was incomplete if the remaining evidence is too thin.

## Signal Hierarchy

When conflicts exist, weight information roughly in this order:

1. official macro release or central bank statement
2. top-tier original reporting
3. gold-specific institutional research
4. broad financial commentary
5. aggregators and rewrites

## Typical Gold-Relevant Query Buckets

- gold price
- spot gold
- Fed rates gold
- US Treasury yields gold
- dollar index gold
- inflation gold
- central bank gold buying
- gold ETF flows
- geopolitics gold safe haven

## Common Failure Modes

- repeated headlines after the same macro event
- old articles resurfacing in search results
- articles where gold is only mentioned once
- commentary pieces with no new information
- sensational geopolitical headlines with weak market impact
