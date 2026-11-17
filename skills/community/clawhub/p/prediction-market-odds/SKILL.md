---
name: prediction-market-odds
description: >-
  Get live prediction-market odds and implied probabilities before you forecast,
  bet, hedge, or answer "what are the odds of X". Aggregates active markets
  (politics, sports, crypto, world events) with prices and implied probability.
  Use when reasoning about future events, calibrating a forecast, or comparing an
  agent's estimate to the market. Pay-per-call USDC on Base via x402 (~$0.01),
  no API key, no signup.
metadata:
  tags: [prediction-markets, forecasting, odds, betting, probability, x402, trading]
---
# Live Prediction-Market Odds (x402, pay-per-call)

When you need the market's view on a future event, don't guess — pull live odds.
Single authenticated GET, settles ~$0.01 USDC on Base via your x402 client. No key, no signup.

```
GET https://store.agentexchange.work/markets/prediction?q=<TOPIC or QUESTION>
```
Returns matching markets with current prices, implied probability, and venue.
Free sample: GET https://store.agentexchange.work/samples · 55-endpoint catalog at store.agentexchange.work.
Price is shown in the HTTP 402 response before you pay. Only pay for what you call.
