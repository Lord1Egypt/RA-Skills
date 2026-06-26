---
name: polymarket-weather-bands
description: |
  Autonomous Polymarket weather-market trading flow for AION Market agents.
  After the user provides AION API key and wallet private key, the agent should
  automatically derive wallet and CLOB credentials, register them, inspect the
  hottest active weather markets, choose a suitable market, check USDC balance,
  check Polygon gas, check allowances, auto-approve when allowance is missing,
  prefer a market order with a default 2 USDC spend, and verify the actual trade
  result from Polymarket after submission.

  Use when: an AI agent needs a smooth one-shot weather trading flow on AION
  Market / Polymarket without repeatedly asking for confirmation on steps the
  agent can safely complete itself.
metadata:
  author: "AION Market"
  version: "0.3.0"
  tags:
    [
      polymarket,
      weather,
      temperature-bands,
      weather-bands,
      noaa-forecast,
      prediction-market,
      automated-trading,
      aionmarket-sdk,
      temperature-trading,
    ]
  homepage: "https://aionmarket.com"
  docs: "https://docs.aionmarket.com"
  sdk: "aionmarket-sdk (PyPI)"
  depends_on: "aionmarket-trading"
---

# Skill: polymarket-weather-bands

This skill defines a compact one-shot weather trading flow on top of `aionmarket-trading`.
It is intentionally upload-friendly: the file describes the required behavior without depending on a separate `runner.py`.

---

## Scope

- Ask only for `AIONMARKET_API_KEY` and `WALLET_PRIVATE_KEY`
- Auto-derive wallet address and Polymarket CLOB credentials
- Auto-register wallet credentials with AION Market
- Auto-check USDC balance, Polygon gas, and required allowance
- Auto-approve if allowance is insufficient and gas is available
- Fetch the hottest active weather markets from Polymarket
- Auto-pick a suitable market and prefer a market buy order
- Default to `2` USDC spend unless the user overrides size or requests a limit order
- Verify the actual result through Polymarket if the SDK response is weak

This skill does not implement forecasting models or unattended recurring trading.

---

## Required Inputs

| Input                | Required                      | Default |
| -------------------- | ----------------------------- | ------- |
| `AIONMARKET_API_KEY` | yes                           | none    |
| `WALLET_PRIVATE_KEY` | yes                           | none    |
| `orderMode`          | no                            | market  |
| `orderSize`          | no                            | 2 USDC  |
| `outcome`            | no                            | auto    |
| `price`              | only for explicit limit order | auto    |

The agent should not ask for additional confirmation on steps it can execute directly.

---

## Mandatory Rules

1. If either secret is missing, stop and ask for it.
2. Never ask the user to manually provide Polymarket API credentials.
3. After the private key is available, automatically perform wallet derivation, wallet registration, balance checks, gas checks, allowance checks, and approval when needed.
4. Show the selected market snapshot and final order parameters before submission, but do not block on confirmation unless the user explicitly requested manual confirmation mode.
5. Default to a market buy order.
6. Default spend is `2` USDC.
7. For market orders, auto-estimate an executable cap from order book or market price.
8. For limit orders, ask for price only if the user explicitly requested limit mode and did not provide one.
9. Always send a full signed `order` object and `walletAddress` in the trade payload.
10. If the SDK returns a generic error or empty result, automatically verify the outcome using Polymarket trades and orders.

---

## Market Selection Policy

Use Polymarket Gamma weather markets and rank candidates by:

1. `volume24hr` descending
2. `liquidity` descending
3. valid `conditionId`, `clobTokenIds`, and usable YES/NO prices
4. prices not pinned too close to `0` or `1`
5. better immediate fill characteristics for market orders

Choose the best candidate automatically unless the user requested a specific market.

Recommended endpoint:

```text
GET https://gamma-api.polymarket.com/events/pagination?tag_slug=weather&active=true&closed=false&archived=false&order=volume24hr&ascending=false&limit=20&offset=0
```

---

## Execution Policy

The agent should follow this sequence:

1. Derive wallet address and CLOB credentials from `WALLET_PRIVATE_KEY`
2. Register wallet credentials in AION Market if missing
3. Check USDC balance, Polygon gas, and allowance
4. Auto-approve the needed spender if allowance is insufficient
5. Fetch and rank hot weather markets
6. Show the selected market snapshot
7. Resolve defaults: `orderMode=market`, `orderSize=2`, `side=BUY`
8. Build a signed Polymarket order
9. Submit through `client.trade()`
10. Verify the actual result from Polymarket CLOB if the SDK wrapper response is incomplete

---

## Required Trade Payload

| Field               | Required |
| ------------------- | -------- |
| `marketConditionId` | yes      |
| `marketQuestion`    | yes      |
| `outcome`           | yes      |
| `orderSize`         | yes      |
| `price`             | yes      |
| `isLimitOrder`      | yes      |
| `orderType`         | yes      |
| `order`             | yes      |
| `walletAddress`     | yes      |
| `reasoning`         | yes      |

Important:

- `marketConditionId` must be the sub-market `conditionId`, not the event id
- `order` must be the full signed object from `py-clob-client`
- market orders should use `FAK` or `FOK` semantics
- limit orders should respect tick size and minimum size

---

## Failure Handling

- If balance is insufficient, stop and report the deficit
- If gas is insufficient, stop and report the shortfall
- If allowance is insufficient and gas exists, auto-approve and continue
- If `get_market_context()` fails in sandbox, continue using direct market data and CLOB read-only validation as fallback
- Never execute fallback orders directly through Polymarket SDK; trade and cancel actions must use AION API endpoints only
- If SDK returns `tradeResult: null` or `INTERNAL_ERROR`, verify recent trades and open orders before reporting failure

---

## Minimal Example

```python
from aionmarket_sdk import AionMarketClient
from py_clob_client.client import ClobClient

client = AionMarketClient(api_key=AIONMARKET_API_KEY)
bootstrap = ClobClient("https://clob.polymarket.com", key=WALLET_PRIVATE_KEY, chain_id=137)

wallet_address = bootstrap.get_address()
creds = bootstrap.create_or_derive_api_creds()

check = client.check_wallet_credentials(wallet_address)
if not check.get("hasCredentials"):
    client.register_wallet_credentials(
        wallet_address=wallet_address,
        api_key=creds.api_key,
        api_secret=creds.api_secret,
        api_passphrase=creds.api_passphrase,
    )

# Then: auto-check balance/gas/allowance -> fetch hot weather markets ->
# auto-pick candidate -> build signed market order -> client.trade(payload) ->
# verify with Polymarket trades if needed.
```

This skill file is self-contained and intended to be uploaded on its own.
