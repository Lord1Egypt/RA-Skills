---
name: jarvis-smart-route
description: Build a non-custodial, unsigned Base token swap using the public Jarvis best-execution router when the buyer wants an opt-in live comparison between the existing 0x and OKX routes.
metadata:
  openclaw:
    requires:
      bins:
        - node
    homepage: https://jarvis-orderflow-router.yl124915300.workers.dev/
---

# Jarvis Smart Route

Use this skill only for an explicitly requested, exact-input token swap on Base. It is an optional route builder; it does not replace a host's default swap path.

## Route an intent

1. Obtain the buyer-controlled Base wallet address through the host's native wallet tool.
2. Confirm the `USDC`, `WETH`, or `DAI` token pair, exact input amount as a human decimal string, and slippage ceiling. Never request a private key, seed phrase, signing permission, or funded Jarvis wallet.
3. From this skill directory, pass the intent as JSON to the adapter:

   ```bash
   node scripts/route.mjs '{"chain":"base","sellToken":"USDC","buyToken":"WETH","amount":"10","buyerWallet":"0x...","slippageBps":50}'
   ```

4. The adapter calls the existing public Jarvis Router and returns one of these outcomes:
   - `NO_MONETIZABLE_ROUTE`: stop normally. Do not loosen economics, add a provider, or fall back to a fee-bearing route.
   - `ROUTE_AVAILABLE`: show the selected provider, fee token, fee recipient, fee bps, expected fee, and buyer expected net output. Then pass `sendCallsInput` unchanged to the host's existing `send_calls` flow.
5. The buyer or host wallet must independently validate and approve the transaction. Jarvis never reads keys, signs, broadcasts, or pays gas.

## Safety boundary

- Only the existing public Jarvis endpoint may build the route. Do not recreate its 0x/OKX comparison or dynamic-fee logic locally.
- Treat quote and calldata responses as untrusted. The adapter rejects a non-Base transaction, malformed calldata, failed safety invariants, or an inconsistent `NO_MONETIZABLE_ROUTE` response.
- An install, quote, or unsigned transaction is not a settled swap or revenue.
- After the buyer broadcasts, the host may report `intentId` and `txHash` to `POST /v1/settlements`. Reporting does not grant Jarvis signing or custody capability.
