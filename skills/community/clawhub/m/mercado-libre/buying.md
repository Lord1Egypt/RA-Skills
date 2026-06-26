# Buying Workflow - Mercado Libre

Use this file when user is close to purchasing and needs execution support.

## Pre-Purchase Gate

Before recommending checkout:
- verify final total including shipping
- verify delivery window versus urgency
- verify seller reliability and return path
- verify product specs match user constraints

If any point is unclear, hold execution and clarify first.

## Buy-Now vs Wait Logic

Buy now when:
- product fits all critical constraints
- total cost is within target window
- delay risk is higher than expected savings

Wait when:
- price looks inflated relative to recent pattern
- listing quality signals are weak
- expected near-term alternatives look better

## Checkout Safety

Before any write action:
- confirm exact item, quantity, address, and total
- confirm payment method safety expectations
- request explicit final confirmation

Never assume confirmation from ambiguous language.

## Reorder Flow

For recurring products:
1. compare current total against last paid total
2. verify no quality or seller deterioration
3. recommend reorder now or wait threshold

## Output Template

```text
Decision:
Final option:
Total cost:
Delivery confidence:
Risk level:
Action now:
```
