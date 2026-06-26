# Decay and Recovery Rules

GwapScore Protocol v2 must allow fair recovery for non-severe negative behavior.

## Negative Event Decay

| Negative Event | Decay Rule |
|---|---|
| Minor failed transaction spike | Decays after 30 clean days |
| One-time scam exposure | Decays after 90 clean days |
| Repeated risky contract use | Decays over 180 clean days |
| Liquidation | Decays over 180–365 clean days |
| Confirmed fraud | Does not decay without manual review |
| Sybil cluster | Requires manual review |

## Positive Recovery Events

- Debt repaid
- Dispute resolved
- Clean period completed
- Risky behavior stopped
- Identity verified
- Trusted counterparty history improved
- Successful escrow completion after prior dispute
- Healthy collateral maintained after prior liquidation

## Recovery Event Names

```ts
type RecoveryEventName =
  | "recovery.clean_period_completed"
  | "recovery.dispute_resolved"
  | "recovery.debt_repaid"
  | "recovery.risky_behavior_stopped"
  | "recovery.identity_verified"
  | "recovery.counterparty_quality_improved";
```

## Rules

1. Severe confirmed fraud should not decay automatically.
2. Sybil cluster involvement must require review.
3. Recovery should not erase historical evidence; it should reduce active penalty impact.
4. Clean behavior over time should improve both score and confidence.
5. Repeated negative behavior after recovery should reset decay timelines.
