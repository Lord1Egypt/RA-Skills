---
name: polymarket-aion-trader
description: 'Place Polymarket trades through Aionmarket. Use when the user wants to search markets, register wallet credentials, verify a wallet, or submit a Polymarket order with an Aionmarket API key, Polymarket CLOB apiKey/apiSecret/apiPassphrase, wallet private key, or a pre-signed EIP712 order. Keywords: Polymarket, Aionmarket, place trade, market order, limit order, wallet credentials, API key, prediction market, 下单, 钱包私钥.'
argument-hint: 'Describe the market, side, size, price, order type, and which credentials you already have.'
user-invocable: true
---

# Polymarket Aionmarket Trader

Use this skill when the user wants to place, inspect, or prepare a Polymarket trade through Aionmarket. Prefer the documented Python SDK when possible, and fall back to raw REST only when the SDK does not cover the requested step.

## When To Use

- User wants to trade on Polymarket through Aionmarket.
- User asks to register or verify Polymarket wallet credentials.
- User wants a market order or limit order submitted to Aionmarket.
- User has an Aionmarket API key and Polymarket CLOB credentials.
- User can provide a wallet private key for local EIP712 signing, or already has a signed order object.
- User wants an SDK-first workflow rather than only raw HTTP requests.

## Secret Handling Rules

- Ask for secrets only when they are required for the next concrete step.
- Treat Aionmarket API keys, Polymarket apiSecret, apiPassphrase, and wallet private keys as transient secrets.
- Never write secrets into repository files, examples, commits, logs, or markdown artifacts.
- If the user does not want to share a wallet private key, ask for a pre-signed EIP712 order object instead.
- If credentials are missing, stop at the preparation stage and tell the user exactly what is still needed.

## Required Inputs

Collect the following before submitting a live Polymarket order:

1. Aionmarket API key, or permission to register a new agent and return the one-time API key.
2. Wallet address for the Polymarket account.
3. Polymarket CLOB API key, API secret, and API passphrase for wallet credential registration.
4. Either the wallet private key for local signing, or a fully signed EIP712 order payload.
5. Trade intent: marketConditionId, marketQuestion, outcome, orderSize, price, order type, and reasoning.

Use the intake checklist in [trade-request-template.md](./assets/trade-request-template.md).

## Procedure

1. Confirm whether the user wants simulation only or live Polymarket trading.
2. If the user wants SDK-first guidance, initialize `AionMarketClient(api_key=..., base_url="https://pm-t1.bxingupdate.com/bvapi")`.
3. If no Aionmarket API key exists, register an agent with `POST /agents/register` and tell the user to save the returned API key immediately.
4. Verify connectivity with `GET /agents/me` before any stateful action.
5. If live trading is requested, prefer the documented SDK wallet flow:
   - `client.check_wallet_credentials(wallet)`
   - `client.register_wallet_credentials(wallet_address=..., api_key=..., api_secret=..., api_passphrase=...)`
   Use raw REST only if the SDK is unavailable.
6. Search or confirm the target market, then inspect market context before execution.
7. For periodic discovery or risk review, prefer `client.get_briefing(venue="polymarket", include_markets=True, user=wallet)`.
8. If the user gave a wallet private key, sign the Polymarket order locally and never persist the key. If the user did not, require a pre-signed `order` object.
9. Validate trade fields before submit:
   - `venue` defaults to `polymarket`
   - `outcome` must be `YES` or `NO`
   - `orderSize` and `price` must be explicit
   - `walletAddress` should match the registered wallet
   - for immediate BUY orders with `FAK` or `FOK`, precision rules apply to micro-unit amounts
10. Submit the trade through the available execution path. If no SDK submit helper is confirmed for the current environment, call `POST /markets/trade` with the signed order payload and include `reasoning`, `source`, and `skillSlug` when available.
11. After submission, offer to inspect open orders, current positions, or cancel stale orders.

## Documented SDK Methods

The Aionmarket docs explicitly show these Python SDK methods:

- `AionMarketClient(api_key=..., base_url=...)`
- `client.get_briefing(venue="polymarket", include_markets=True, user=wallet)`
- `client.check_wallet_credentials(wallet)`
- `client.register_wallet_credentials(wallet_address=..., api_key=..., api_secret=..., api_passphrase=...)`

Treat any unconfirmed helper names as unknown until the docs or installed SDK prove they exist. If a needed SDK helper is not documented, use the corresponding REST endpoint instead of inventing a client method.

## Execution Notes

- Aionmarket expects a signed Polymarket order payload inside the `order` field. Wallet credential registration alone does not sign orders.
- `POST /markets/trade` supports both limit and market-style execution through `isLimitOrder` and `orderType`.
- The docs explicitly demonstrate SDK coverage for briefing and wallet credential management, but they do not explicitly show a Polymarket trade submit helper name in the pages used for this skill.
- For discovery or risk review, prefer briefing and market context before placing orders.
- If the API returns `401`, re-check the Bearer token. If it returns `403`, verify claim status, wallet registration, and guardrails. If it returns `429`, retry with backoff.

## Resources

- [Aionmarket Polymarket reference](./references/aionmarket-polymarket.md)
- [Aionmarket SDK reference](./references/aionmarket-sdk.md)
- [Trade request template](./assets/trade-request-template.md)