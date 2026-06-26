# Pay — Domain Rules

Protocol-enforced values. Look up when reasoning about fees, limits, or conversions.

## Fee structure

| Monthly volume (per provider) | Rate |
|-------------------------------|------|
| < $50,000 | 1% (100 bps) |
| >= $50,000 | 0.75% (75 bps) |

Cliff model: once a provider crosses $50k in a calendar month, all
subsequent transactions that month use 0.75%. Resets 1st of month UTC.

### Direct payments

- Agent sends amount. Provider receives amount minus fee.
- Fee paid by provider (recipient), not agent.
- $1.00 minimum.

### Tab fees

| Fee | Who pays | Amount |
|-----|----------|--------|
| Activation fee | Agent | max($0.10, 1% of tab amount) |
| Processing fee | Provider | max($0.002, 1%) per charge |
| Top-up | Nobody | No fee |

Activation fee is non-refundable. Covers tab lifecycle gas + spam
prevention. The 1% rate kicks in at $10+ tabs; a $5 tab pays 2%.

## Minimums

| Operation | Minimum | Why |
|-----------|---------|-----|
| Direct payment | $1.00 | Gas (~$0.004) covered by 1% fee |
| Tab open | $5.00 | Activation fee ($0.10) covers lifecycle gas |
| Tab charge | None | Batched — ~$0.000006 effective per charge |

## Rate limits

| Action | Limit |
|--------|-------|
| Tab opens | 10/minute per wallet |
| Direct payments | 120/minute per wallet |
| Tab charges | No limit (bounded by balance + maxChargePerCall) |
| Webhook registrations | 10/hour per wallet |

## Gas costs (Base L2)

All gas paid by the protocol. Agents never hold ETH.

| Operation | Cost |
|-----------|------|
| Direct payment (permit + transfer) | ~$0.002-$0.004 |
| Tab open (permit + lock) | ~$0.002-$0.004 |
| Tab charge batch (~100/batch) | ~$0.0006/batch (~$0.000006/charge) |
| Tab close (3 USDC transfers) | ~$0.003-$0.006 |
| Tab top-up (permit + transfer) | ~$0.002-$0.004 |

## Micro-USDC conversion

USDC has 6 decimals. API and contracts use micro-USDC integers.
CLI accepts USD amounts (e.g., `5.00`).

| USD | micro-USDC |
|-----|-----------|
| $0.001 | 1,000 |
| $0.01 | 10,000 |
| $0.10 | 100,000 |
| $1.00 | 1,000,000 |
| $5.00 | 5,000,000 |
| $50.00 | 50,000,000 |
| $100.00 | 100,000,000 |

## Webhook events

```
payment.completed    — direct payment settled on-chain
tab.opened           — tab created on-chain
tab.settled          — batch settlement confirmed on-chain
tab.low_balance      — balance below 20% of original
tab.closing_soon     — auto-close imminent
tab.closed           — tab closed, funds distributed
tab.topped_up        — funds added to tab
x402.settled         — x402 payment settled on-chain
```
