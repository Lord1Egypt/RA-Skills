# GwapScore Protocol

Version: 1.0.1  
Type: Instruction-only OpenClaw skill  
Scope: GwapScore Protocol only  
Chain: Solana-first  
Canonical score range: 300–900  

## Purpose

GwapScore Protocol converts Solana wallet behavior into a transparent, deterministic, partner-safe trust score.

The protocol evaluates:

- Wallet maturity
- Transaction consistency
- Counterparty quality
- Protocol diversity
- Security hygiene
- Lending and credit behavior
- Commerce and creator reliability
- Sybil and farming resistance
- Recovery and decay behavior

The score must never be treated as a measure of wealth, popularity, race, identity, legal status, or personal worth.

GwapScore measures observed onchain trust behavior.

## Operating Principles

1. Score is not wealth.
2. Confidence is separate from score.
3. Evidence must be explainable.
4. Severe risk events apply caps.
5. Sybil detection should trigger review when evidence is uncertain.
6. Recovery must be possible for non-severe negative behavior.
7. Partner-facing outputs must be deterministic and understandable.
8. Spam/dust exposure must not automatically punish the wallet.
9. Repeated intentional interaction with risky counterparties should matter.
10. Manual review exists to handle ambiguous or high-impact cases.

## Canonical v2 Score Tiers

| Score Range | Tier | Meaning |
|---:|---|---|
| 300–449 | critical_risk | Severe negative evidence or active major risk |
| 450–549 | high_risk | Risky, suspicious, or unresolved issues |
| 550–649 | thin_or_developing | Limited clean history or thin evidence |
| 650–724 | standard | Normal usable wallet profile |
| 725–799 | trusted | Strong positive onchain history |
| 800–900 | elite | Long-term, high-confidence, clean behavior |

## GwapScore v2 Category Weights

| Category | Weight |
|---|---:|
| Wallet Maturity | 12% |
| Transaction Consistency | 13% |
| Counterparty Quality | 20% |
| Protocol Diversity | 10% |
| Security Hygiene | 10% |
| Lending / Credit Behavior | 15% |
| Commerce / Creator Reliability | 8% |
| Sybil / Farming Resistance | 7% |
| Recovery / Decay Behavior | 5% |

## Formula

First calculate a 0–100 raw weighted score:

```ts
weightedRawScore =
  walletMaturity * 0.12 +
  transactionConsistency * 0.13 +
  counterpartyQuality * 0.20 +
  protocolDiversity * 0.10 +
  securityHygiene * 0.10 +
  lendingCreditBehavior * 0.15 +
  commerceReliability * 0.08 +
  sybilResistance * 0.07 +
  recoveryBehavior * 0.05;
```

Convert to the canonical 300–900 score:

```ts
protocolScore = 300 + (weightedRawScore / 100) * 600;
```

Then apply all relevant score caps.

## Required Behavior for Agents Using This Skill

When asked to score, design, explain, audit, or extend GwapScore Protocol:

1. Identify the subject wallet or profile.
2. Gather or define available evidence.
3. Normalize raw evidence into canonical events.
4. Convert canonical events into attestations.
5. Score each v2 category on a 0–100 scale.
6. Apply category weights.
7. Convert weighted raw score into 300–900.
8. Apply caps.
9. Calculate confidence separately.
10. Generate explanations, risk flags, and recommended review actions.
11. Avoid unsupported claims.
12. Distinguish verified evidence from assumptions.

## References

Use these files when generating protocol docs, API designs, scoring logic, or partner integration content:

- `references/scoring-model-v2.md`
- `references/confidence-model-v2.md`
- `references/canonical-event-schema.md`
- `references/attestation-taxonomy.md`
- `references/decay-and-recovery-rules.md`
- `references/manual-review-policy.md`
- `references/feature-gating-thresholds.md`
- `references/partner-integration-policy.md`

## Templates

- `templates/score-output-template.md`
- `templates/risk-escalation-template.md`
- `templates/manual-review-template.md`

## Example Payloads

- `assets/example-payloads/gwapscore-v2-score.json`
- `assets/example-payloads/gwapscore-v2-events.json`

## Boundaries

This skill does not require:

- API keys
- environment variables
- database migrations
- external credentials
- RPC endpoints
- background services

This package is instruction-only. Any implementation using Helius, QuickNode, custom RPC, Postgres, NestJS, or workers must be handled outside this skill unless explicitly requested in a separate implementation task.
