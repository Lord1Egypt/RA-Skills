---
name: liquid-gas-sponsor
description: Send any transaction on Base with a wallet that holds USDC but no ETH. Pay the gas per operation in USDC over x402 (from $0.03) through an ERC-4337 paymaster; one endpoint for smart-wallet SDKs and plain wallets. No account, no API key.
homepage: "https://api.liquidagent.ai/v1/gas"

metadata:
  openclaw:
    requires:
      bins: ["curl"]
---

# Liquid gas sponsor — transact on Base with USDC only

Most agent wallets hold USDC and nothing else, and every on-chain action needs ETH for gas. This skill
removes that: **POST `https://api.liquidagent.ai/v1/gas`** is an ERC-4337 paymaster you pay **per
operation in USDC over x402**. The 402 is the quote. Pay it, sign what comes back, and the sponsor's
deposit pays the gas. No ETH, no account, no API key, no sign-up.

- Chain: Base mainnet (`eip155:8453`), EntryPoint v0.8, paymaster `0x9676897c3bf08977cdbe78213f84e72a29b844ec`
- Price: `max($0.03, 1.3 × the operation's gas cap)`; a simple transfer is $0.03, a heavy DeFi call a few cents more
- The signed sponsorship locks the gas limits and max fee, so the sponsor can never charge more than it quoted
- Fees settle through a public x402 facilitator (PayAI); the exact price and `payTo` are in the 402

## When to use this skill

- Your wallet has USDC but zero ETH and you need to send, swap, deposit, mint, or call any contract on Base
- You built an unsigned transaction with another API (for example Liquid Agent's stock index: `POST /v1/buy`) and can't broadcast it
- You run a smart-wallet SDK (ERC-4337) and want a paymaster you can pay per op instead of a developer account

## One endpoint, the body picks the lane

### Plain wallet (any EOA) — two calls to the same URL

```bash
# 1. Quote. No payment header -> HTTP 402 with the exact USDC price for THIS operation (valid 120 s).
curl -s -X POST https://api.liquidagent.ai/v1/gas -H 'content-type: application/json' \
  -d '{"sender":"0xYourEOA","calls":[{"to":"0x…","data":"0x…","value":"0"}]}'

# 2. Pay it. Any x402 client (agentcash, x402-fetch) repeats the call with X-PAYMENT and receives:
#    { "userOperation": {...sponsored...}, "typedData": {...}, "authorization": {...} | null, "validUntil": <unix> }
#    - sign typedData with the sender's key (eth_signTypedData_v4) -> put the 65-byte signature in userOperation.signature
#    - if "authorization" is present (first time only): sign it too (EIP-7702; viem: account.signAuthorization)
#    - POST both back to the SAME URL before validUntil:
curl -s -X POST https://api.liquidagent.ai/v1/gas -H 'content-type: application/json' \
  -d '{"userOperation":{...with signature...},"authorization":{...signed, optional...}}'
#    -> { "txHash": "0x…", "success": true, "actualGasCostEth": "…" }   (no further charge)
```

Your EOA becomes an eth-infinitism `Simple7702Account` by delegation (owner = you, reversible, no deployment);
that is what lets the sponsor pay for it. Only operations the sponsor signed are accepted, once each.
Already delegated to another EIP-7702 implementation (MetaMask and friends)? The first call returns 409. Add
`"redelegate": true` to the same body and the sponsor returns an authorization you sign that re-points the wallet
to `Simple7702Account` in the same transaction (reversible), or keep your delegation and use the next section.

### Any other smart account — bring your own operation

Already delegated to a different EIP-7702 implementation, or a deployed smart account (Kernel, Safe, Nexus…)
on EntryPoint v0.8? Build the operation yourself and the sponsor submits it: no bundler, no stake, no ETH.

```bash
# 1. Quote: POST the UNSIGNED EntryPoint v0.8 operation (your sender, calldata and gas limits) -> 402 with the price
curl -s -X POST https://api.liquidagent.ai/v1/gas -H 'content-type: application/json' \
  -d '{"userOperation":{"sender":"0xYourAccount","nonce":"0x…","callData":"0x…","callGasLimit":"0x…","verificationGasLimit":"0x…","preVerificationGas":"0x…","maxFeePerGas":"0x…","maxPriorityFeePerGas":"0x…","signature":"0x"}}'
# 2. Pay it and repeat -> { "userOperation": {...with paymaster fields...}, "typedData": {...}, "validUntil": <unix> }
# 3. Sign it the way YOUR account expects (viem: account.signUserOperation), then POST {"userOperation": <with signature>}
#    to the same URL. The sponsor dry-runs it through the EntryPoint before submitting: a failed dry run returns 400
#    with the reason, costs nothing, and can be retried before validUntil.
```

Reference: https://github.com/LiquidAgent/liquidagentx402/blob/main/examples/gasless-bring-your-own.js
(swap the account constructor for your SDK's). Fresh, never-delegated EOAs should use the plain-wallet lane above.

### Smart-wallet SDK (ERC-7677)

Point the SDK's paymaster URL at `https://api.liquidagent.ai/v1/gas`. `pm_getPaymasterStubData` is free.
An unpaid `pm_getPaymasterData` returns a JSON-RPC error `{code:402, data:<x402 PaymentRequired>}` with HTTP
200 (so SDKs don't treat it as a transport failure). Put the x402 payment object in `params[3].context.x402`
and retry; the result is the standard `{paymaster, paymasterData, paymasterVerificationGasLimit, paymasterPostOpGasLimit}`.
Then POST the signed operation back to the same URL instead of a public bundler: bundlers only relay staked
paymasters and this one is not staked yet, so the bring-your-own-operation step above is the last mile.

## Paying the 402

x402 v2, scheme `exact`, network `eip155:8453`, asset USDC `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`.
The payment is one EIP-3009 `TransferWithAuthorization` signature (off-chain, no gas). With agentcash:
`fetch` handles it automatically; set `maxAmount` to a few cents. A complete Node example that buys a
tokenized-stock index with a zero-ETH wallet: https://github.com/LiquidAgent/liquidagentx402/blob/main/examples/gasless.js

## Reads (free)

- `GET https://api.liquidagent.ai/v1/gas` — what the sponsor is, price rule, addresses, both flows
- `GET https://api.liquidagent.ai/v1/gas/stats` — live usage: sponsorships, fees, success rate

## Limits and safety

- Per-operation ceiling $5 of gas; past 500 sponsored ops per sender per day the floor rises to $0.04 (never blocked)
- Quote and sponsorship expire together after 120 s; submit before `validUntil` or get a fresh quote
- The sponsor never sees your key: you sign the operation and the payment locally, it only signs its own sponsorship
- Spent nothing if the operation fails on-chain? The fee is taken at sponsorship time; build and simulate your calls first
