---
name: mpptester
version: 0.1.0
description: Run a Machine Payments Protocol (MPP) conformance test — prove an agent or wallet can complete a real $0.50 USDC payment on Solana and get a shareable "passed" proof. Use when verifying an agent can send (or receive) an on-chain payment, testing an agent's payment integration, or generating a verifiable payment proof. Supports mainnet (real USDC) and devnet (test USDC).
homepage: https://mpptester.com
repository: https://github.com/kris-hansen/mpptester
---

# MPP Tester

MPP Tester verifies that an agent can actually move money: it issues a unique
**$0.50 USDC** payment request on Solana, watches the chain, and flips the test
to **passed** once the transfer is confirmed on-chain (via a Helius webhook,
with an RPC poll fallback). A passed test is a public, linkable proof.

- **Send test** (no account needed): your agent pays $0.50 USDC to the test
  wallet; we confirm receipt.
- **Receive test** (needs a signed-in account): the service pays $0.50 USDC to
  your address; unlocked 1 per 3 confirmed sends, per network.

Base URL: `https://mpptester.com`

## Run a send test

The quickest path is the helper script:

```bash
# mainnet (real $0.50 USDC) or devnet (test USDC)
scripts/run-test.sh mainnet-beta
scripts/run-test.sh devnet
```

It starts a test, prints the Solana Pay URL to pay, polls until the result is
known, and prints the shareable receipt link. To do it manually:

### 1. Start the test

```bash
curl -s -X POST https://mpptester.com/api/mpp/start \
  -H 'Content-Type: application/json' \
  -d '{"network":"mainnet-beta"}'
```

Returns:

```json
{
  "reference": "<base58>",
  "network": "mainnet-beta",
  "paymentUrl": "solana:<wallet>?amount=0.5&spl-token=<USDC>&reference=<ref>&...",
  "amountUsdc": 0.5,
  "status": "pending",
  "expiresAt": "<iso8601>"   // tests expire after 30 minutes
}
```

### 2. Pay the request

Pay the `paymentUrl` — a standard [Solana Pay](https://docs.solanapay.com)
transfer request. The `reference` key in the URL is how the test is correlated
to your payment, so the payment **must include it** (any Solana Pay-compatible
wallet or library does this automatically; a manual address-only transfer will
not be recognized).

- **Agent / programmatic:** have your wallet tooling pay the Solana Pay URL
  (recipient, amount, SPL token, and reference are all encoded in it).
- **Human:** render the `paymentUrl` as a QR code and scan it with a Solana Pay
  wallet (Phantom, Solflare, etc.), or open `https://mpptester.com/test/<reference>`
  which shows the QR and live status.

Requires a funded wallet: $0.50 USDC plus a little SOL for fees on the chosen
network. On devnet, fund from a faucet first.

### 3. Poll for the result

```bash
curl -s https://mpptester.com/api/mpp/tests/<reference>
```

`status` becomes `confirmed` once the transfer is validated on-chain (amount,
token, and recipient checked), or `expired` after 30 minutes unpaid. On success
the response includes `txSignature` and `txUrl` (Solscan link).

### 4. Share the proof

The passing test is viewable and linkable at:

```
https://mpptester.com/test/<reference>
```

## Receive test (optional)

Proves your agent can *receive* a payment: the service sends $0.50 USDC to an
address you control. This requires a signed-in account (email magic link at
`https://mpptester.com/signin`) and an allowance of **1 receive per 3 confirmed
send tests on the same network**. From the dashboard: Receive test → pick the
network → enter your address → run. (No anonymous API for receive yet.)

## Notes

- Networks: `mainnet-beta` (real USDC, default) or `devnet` (test USDC). Pick
  devnet to try the flow without spending real money.
- Each test is exactly **$0.50 USDC**; one on-chain transaction confirms one
  test (overpaying or paying twice does not grant extra credit).
- Send tests are anonymous; sign in only to keep a private history or run
  receive tests.
