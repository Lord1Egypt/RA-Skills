# Attestation Taxonomy

GwapScore Protocol converts canonical events into attestations used for scoring, confidence, explanations, and review.

## v2 Attestation Types

```ts
type AttestationType =
  | "wallet_maturity"
  | "transaction_consistency"
  | "counterparty_quality"
  | "protocol_diversity"
  | "security_hygiene"
  | "lending_credit_behavior"
  | "commerce_reliability"
  | "sybil_resistance"
  | "recovery_behavior"
  | "manual_review"
  | "dispute_resolution";
```

## Attestation Shape

```ts
type GwapAttestation = {
  id: string;
  subjectWallet: string;
  type: AttestationType;
  source: "onchain" | "partner" | "manual_review" | "social_link" | "system";
  severity: "positive" | "neutral" | "warning" | "negative" | "severe";
  confidence: number;
  scoreImpact: number;
  evidence: EvidencePointer[];
  createdAt: string;
  expiresAt?: string;
};
```

## Evidence Pointer

```ts
type EvidencePointer = {
  chain: "solana";
  signature?: string;
  programId?: string;
  mint?: string;
  counterparty?: string;
  slot?: number;
  timestamp?: string;
  metadata?: Record<string, unknown>;
};
```

## Rules

- Positive attestations must identify the evidence supporting the score impact.
- Negative attestations must distinguish severity and review status.
- Severe attestations may trigger caps.
- Partner attestations should be source-labeled.
- Manual review attestations should include resolution state.
- Expiring attestations should be used for temporary risks and recoverable events.
