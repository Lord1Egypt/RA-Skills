# Manual Review Policy

Manual review is required when automated scoring cannot safely or fairly resolve evidence.

## v2 Manual Review Triggers

```ts
type ManualReviewTrigger =
  | "likely_sybil_cluster"
  | "circular_transaction_pattern"
  | "shared_funding_cluster"
  | "synchronized_wallet_behavior"
  | "suspicious_airdrop_farming"
  | "active_scam_cluster_interaction"
  | "severe_unresolved_fraud_report"
  | "multiple_unresolved_disputes"
  | "major_score_swing_from_thin_evidence"
  | "possible_compromised_wallet";
```

## Required Review Packet

Each review packet should include:

- Wallet
- Trigger
- Severity
- Evidence pointers
- Related counterparties
- Score before review
- Score after temporary cap
- Recommended action
- Reviewer notes
- Resolution
- Timestamp

## Review Outcomes

| Outcome | Effect |
|---|---|
| clear | Remove temporary risk flag and restore normal scoring |
| monitor | Keep flag but avoid severe cap |
| cap | Apply temporary or permanent score cap |
| severe_cap | Apply severe score cap |
| dispute_required | Require formal dispute or additional evidence |
| confirmed_bad_actor | Apply severe negative attestation |

## Rules

- Manual review should be used for ambiguous Sybil or scam-cluster evidence.
- Review should be evidence-based, not assumption-based.
- Wallets should be able to dispute review outcomes.
- Severe caps require clear supporting evidence.
