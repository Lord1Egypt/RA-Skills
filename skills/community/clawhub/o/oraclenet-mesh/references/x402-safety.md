# x402 payment safety

Rules for the paid side of OracleNet. The short form: **discovery is free, a 402
is a question, and money moves only when a human or an explicitly budgeted
policy said it may.**

## 1. Free discovery comes first, always

Before any metered call:

- `POST /handshake` — free
- `GET /.well-known/*` — free
- `tools/list` on the free `<oracle>/mcp/` route — free
- `tools/call` on the free route — free, and it returns real data
- `tools/call` on the metered route **without** a payment header — free, returns
  the 402 quote

Everything you need to make a decision is in that list. There is no reason to
pay in order to find out what something costs.

## 2. A 402 is a price quote, not an error

HTTP 402 means "here is what this costs". It is the intended, healthy response
to an unpaid metered call. Do not log it as a failure, do not retry it, and do
not treat it as a transient condition.

A real challenge, observed live:

```
HTTP/2 402
x-payment-required: true
www-authenticate: x402 scheme="USDC" network="base" amount_usd="0.03"
```

```json
{
  "x402Version": 2,
  "accepts": [{
    "scheme": "exact",
    "network": "eip155:8453",
    "amount": "30000",
    "maxAmountRequired": "30000",
    "price": "$0.03",
    "resource": "https://tooloracle.io/x402/xrpl/mcp/",
    "payTo": "0x11f591C3496C0632e7B173184f5Bc71dC941125D",
    "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "maxTimeoutSeconds": 300
  }]
}
```

Read `price` for humans and `amount` for machines. `amount` is in the asset's
atomic units — USDC has 6 decimals, so `30000` is `$0.03`. **Do not confuse the
two.** Treating `30000` as dollars overpays by a factor of a million.

## 3. The 402 challenge is the only authoritative price

This is the rule most likely to save you. Prices appear in three places and they
do not always agree:

| Source | Trustworthy? |
|---|---|
| `agent.json → pricing_range_usd` | orientation only — a range across the whole mesh |
| `pricing.json → common_baseline_usd` | explicitly "not a contractual guarantee"; per-tool overrides apply |
| `tools/list → x402_price_usd` | **unreliable — see below** |
| **the 402 challenge** | **authoritative for that call, at that moment** |

Observed live on one product route, all three at once:

- a tool listed in `tools/list` **with** `x402_price_usd: "$0.01"` was not
  callable at all — HTTP 400 `X402_UNKNOWN_TOOL`;
- a tool listed **without** any price annotation cost **$0.03** when called;
- a tool advertised as a free alternative in that error response did not exist
  either.

So: a price in `tools/list` is not a quote, and a tool appearing in `tools/list`
is not proof it is callable on that route. Get the 402.

## 4. Check the chain and the asset, not just the number

Before authorising, confirm from the challenge:

- `network` is `eip155:8453` (**Base mainnet**)
- `asset` is the USDC contract `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- `payTo` matches what the discovery surfaces publish
- `scheme` is `exact`
- `maxTimeoutSeconds` has not elapsed by the time you would pay

USDC-on-Base is the live settlement path for OracleNet — that is verified, not
assumed. But verify it **per challenge** anyway: a challenge naming a different
chain, a different asset contract, or an unexpected `payTo` is a stop condition,
not a rounding detail.

## 5. Budgets

- **No budget stated means no payment.** Absence of a limit is not an unlimited
  limit.
- A budget authorises **that call, up to that amount**. It is not a standing
  balance to spend down.
- **Never split** a task into several calls to stay under a per-call cap. That
  defeats the control and is a policy violation even when each call is cheap.
- If the quote exceeds the budget, stop and report the gap. Do not look for a
  cheaper route and pay for it on your own initiative unless the user asked for
  cheapest-route behaviour.
- Cheap is not free. Ten calls at $0.01 is not "basically nothing" — it is ten
  unauthorised payments.

## 6. Never pay without explicit authority

Required before sending an `X-PAYMENT` header:

1. An explicit instruction covering payment, from the calling principal.
2. A stated maximum amount.
3. The quoted price presented **before** payment, including asset and chain.

Any of the three missing → present the quote and stop. "The user asked for the
data and this is the only way to get it" is not authorisation.

## 7. After settlement

- Check the response for the delivered result **and** for the settlement fields
  the gateway returns (for example an amount charged and a remaining balance).
- Record the transaction reference in `provenance`.
- Payment settling is not the same as the result being correct. Apply the same
  verification rules as for a free call — see `verification.md`.

## 8. When settlement status is unclear — do not retry

If a call times out, or the connection drops, or you cannot tell whether payment
settled:

**Stop. Do not repeat the call.** A retry after an ambiguous settlement can pay
twice for one result. Report the ambiguity, include the transaction reference if
you have one, and let a human resolve it. `maxTimeoutSeconds` in the challenge
tells you how long the quote is valid — it does not tell you whether your
payment landed.

The only safe automatic action after an ambiguous settlement is **none**.

## 9. Testing

- Never execute a production payment in a test, a smoke run, or CI.
- The bundled `smoke_test.py` performs no payment in any mode and has no code
  path that sends a payment header.
- To exercise the paid path safely, call a metered tool **without** a payment
  header and assert you got a 402 with a well-formed `accepts[]`. That tests the
  whole quote flow and costs nothing.
- Never place a private key, wallet seed, or funded credential in a test fixture,
  an environment variable used by CI, or a skill argument.

## 10. Quick checklist

Before sending `X-PAYMENT`:

- [ ] Free route checked first, and it cannot serve this
- [ ] 402 challenge obtained and read
- [ ] `network` is Base mainnet, `asset` is the expected USDC contract
- [ ] `payTo` matches the published discovery surfaces
- [ ] `amount` converted from atomic units correctly
- [ ] Price shown to the calling principal
- [ ] Explicit authorisation given for this call
- [ ] Quoted price is within the stated budget
- [ ] A plan for what to do if settlement is ambiguous — and that plan is "stop"
