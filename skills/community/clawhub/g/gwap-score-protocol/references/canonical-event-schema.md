# Canonical Event Schema

GwapScore Protocol converts raw Solana activity into canonical events before scoring.

## v2 Canonical Event Names

```ts
type CanonicalEventName =
  | "wallet.first_seen"
  | "wallet.funded"
  | "wallet.active_period_detected"
  | "transaction.success"
  | "transaction.failed"
  | "transaction.spam_pattern_detected"
  | "counterparty.trusted_interaction"
  | "counterparty.risky_interaction"
  | "counterparty.scam_cluster_exposure"
  | "protocol.reputable_interaction"
  | "protocol.unknown_interaction"
  | "security.risky_approval_detected"
  | "security.approval_revoked"
  | "security.wallet_drain_detected"
  | "lending.borrow_opened"
  | "lending.loan_repaid"
  | "lending.position_liquidated"
  | "commerce.payment_received"
  | "commerce.escrow_completed"
  | "commerce.escrow_disputed"
  | "commerce.refund_issued"
  | "sybil.shared_funding_detected"
  | "sybil.circular_flow_detected"
  | "sybil.cluster_similarity_detected"
  | "recovery.clean_period_completed"
  | "recovery.dispute_resolved";
```

## Event Shape

```ts
type GwapScoreEvent = {
  id: string;
  wallet: string;
  eventName: CanonicalEventName;
  chain: "solana";
  signature?: string;
  slot?: number;
  timestamp: string;
  programId?: string;
  counterparty?: string;
  mint?: string;
  amount?: string;
  metadata?: Record<string, unknown>;
};
```

## Event Normalization Rules

1. Raw Solana transactions must be converted into canonical event names before scoring.
2. Each event should preserve evidence pointers: signature, slot, timestamp, program ID, mint, amount, and counterparty when available.
3. Unknown programs should be marked as `protocol.unknown_interaction`, not automatically treated as malicious.
4. Spam or dust received should be marked as noise unless connected to repeated intentional behavior.
5. Circular flows, synchronized behavior, and shared funding should generate risk events and may trigger manual review.
