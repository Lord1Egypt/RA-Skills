# Pay — Tab Guide

Tabs are pre-funded metered accounts. Agent locks USDC, provider charges
per use, either party can close anytime.

## When to use tabs

- Agent will make multiple calls to the same provider
- Per-call cost is under $1 (direct settlement has a $1 minimum)
- Service has variable/metered pricing
- x402 tab settlement (the CLI handles this for existing tabs)

## Sizing

### Recommended: $50 tabs

The activation fee is `max($0.10, 1% of tab amount)`:

| Tab size | Activation fee | Fee % | Effective calls at $0.01/call |
|----------|---------------|-------|-------------------------------|
| $5 | $0.10 | 2% | 490 |
| $10 | $0.10 | 1% | 990 |
| $20 | $0.20 | 1% | 1,980 |
| $50 | $0.50 | 1% | 4,950 |
| $100 | $1.00 | 1% | 9,900 |

$10 is where the activation fee drops to 1%. Below $10, the floor
applies but at 2% it's still very reasonable.

### Sizing heuristics

| Situation | Tab size |
|-----------|----------|
| Unknown usage, just trying it | $5 (minimum, accept the 2% hit) |
| Known budget ("spend up to $20") | Match the budget |
| Known volume (~1000 calls at $0.01) | $15 (1.5x expected) |
| Ongoing heavy use | $50 (recommended default) |
| High-volume production | $100+ |

### Top-up strategy

Top up when the tab balance drops below 20% of original (matches the
`tab.low_balance` webhook threshold). Top-up amount: same as original
tab size. No additional activation fee on top-ups.

```
pay tab topup <tab_id> <amount>
```

Always confirm top-ups with the operator before executing.

## Max charge per call

Set `--max-charge` to the expected per-call price. This is contract-
enforced protection against overcharging.

```
# API charges $0.01/call
pay tab open 0xProvider 50.00 --max-charge 0.01

# API charges $0.50/call
pay tab open 0xProvider 50.00 --max-charge 0.50
```

If the provider tries to charge more than max-charge, the contract
reverts the transaction. The agent's total risk is bounded by the
tab balance.

If you don't know the per-call price, set max-charge to $1 as a
reasonable ceiling for most APIs. Adjust after seeing actual charges.

## Closing tabs

Either party can close unilaterally:

```
pay tab close <tab_id>
```

On close, funds are distributed:
- Provider receives: totalCharged * 0.99
- Fee wallet receives: totalCharged * 0.01
- Agent receives: remaining balance (refunded)

## Idle tab cleanup

Tabs with no charges for an extended period are wasting locked capital.
When reviewing tabs (`pay tab list`), flag any that appear idle:

- No charges in the last 24+ hours (if the service was supposed to
  be active)
- Balance is nearly full (opened but barely used)
- Provider is no longer being used

Suggest closing idle tabs to free up the balance. Tabs auto-close
after 30 days of inactivity. The agent receives a `tab.closing_soon`
webhook before this happens.

## Multiple tabs with same provider

Unusual but valid. Different max-charge limits or purposes. Don't warn,
but if an agent has two tabs with the same provider, ask if one should
be closed.

## What tabs are NOT

- Not subscriptions. No recurring charge. Pay per use.
- Not escrow. No deliverable-based release.
- Not streams. No per-second rate.
