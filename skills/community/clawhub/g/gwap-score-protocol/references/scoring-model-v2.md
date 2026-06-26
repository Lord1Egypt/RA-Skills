# GwapScore Protocol v2 Scoring Model

## Canonical Range

GwapScore v2 uses a 300–900 trust score.

| Score Range | Tier | Meaning |
|---:|---|---|
| 300–449 | critical_risk | Severe negative evidence or active major risk |
| 450–549 | high_risk | Risky, suspicious, or unresolved issues |
| 550–649 | thin_or_developing | Limited clean history or thin evidence |
| 650–724 | standard | Normal usable wallet profile |
| 725–799 | trusted | Strong positive onchain history |
| 800–900 | elite | Long-term, high-confidence, clean behavior |

## Category Weights

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

## Category Definitions

### 1. Wallet Maturity — 12%

Measures wallet age, active months, continuity, funding source quality, and long-term holding behavior.

Positive signals:

- Older wallet with real activity
- Multiple active months
- Stable funding source
- Long-term asset holding
- Wallet continuity

Negative signals:

- Brand-new wallet
- One-day burst behavior
- Repeated wallet resets
- Dormancy followed by suspicious high-volume activity

### 2. Transaction Consistency — 13%

Measures whether transaction behavior looks normal, useful, and intentional.

Positive signals:

- Steady transaction cadence
- Low failed transaction ratio
- Human-like timing
- Natural transaction size variance
- Meaningful program interactions

Negative signals:

- High failed transaction ratio
- Same-second repetitive actions
- Dust-transfer spam
- Airdrop-only activity
- Farming loops

### 3. Counterparty Quality — 20%

Measures repeated interaction with trusted or risky wallets, programs, merchants, creators, and clusters.

Positive signals:

- Interactions with high-score wallets
- Receives from verified merchants or creators
- Clean counterparty graph
- Diverse non-circular relationships

Negative signals:

- Repeated scam-cluster exposure
- Circular transaction flows
- Suspicious one-hop or two-hop exposure
- Shared funding with risky clusters

Important rule: dust/spam received should not automatically lower the score.

### 4. Protocol Diversity — 10%

Measures healthy participation across reputable Solana protocol categories.

Categories:

- DeFi
- Staking
- NFT marketplace
- Payments
- Identity
- Escrow
- DAO/governance
- Creator tools
- Gaming

Healthy diversity should not reward random protocol hopping or suspicious airdrop farming.

### 5. Security Hygiene — 10%

Measures safe wallet behavior.

Positive signals:

- Risky approvals revoked
- Clean program interaction history
- Maintains SOL fee reserve
- Avoids malicious contracts
- Stable balance behavior

Negative signals:

- Risky token approvals
- Known malicious program interaction
- Sudden wallet drain
- Repeated scam-token trading
- Possible compromised-wallet pattern

### 6. Lending / Credit Behavior — 15%

Measures onchain borrowing, repayment, collateral, liquidation, and responsible leverage behavior.

Positive signals:

- Loan repaid
- Healthy collateral ratio
- Liquidation avoided
- Debt reduced during volatility
- Responsible leverage

Negative signals:

- Multiple liquidations
- Unresolved bad debt
- Excessive leverage
- Collateral collapse with no recovery

### 7. Commerce / Creator Reliability — 8%

Measures payments, escrow, refunds, repeat customers, royalties, and seller/creator reliability.

Positive signals:

- Repeat customer payments
- Escrow completed
- Royalty received consistently
- Low refund rate
- Verified merchant payments

Negative signals:

- Escrow disputed
- High refund ratio
- Unresolved seller disputes
- Fraud-linked payment flows

### 8. Sybil / Farming Resistance — 7%

Measures suspicious wallet-farm behavior.

Risk signals:

- Shared funding source
- Synchronized wallet behavior
- Circular funds
- Cluster similarity
- Airdrop-only behavior
- Consolidation into one wallet

Sybil signals should often trigger manual review instead of automatic punishment.

### 9. Recovery / Decay Behavior — 5%

Measures whether a wallet resolves problems and builds clean history over time.

Positive signals:

- Debt repaid
- Dispute resolved
- Clean period completed
- Risky behavior stopped
- Identity verified
- Counterparty history improved

## Formula

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

protocolScore = 300 + (weightedRawScore / 100) * 600;
```

## Score Caps

| Condition | Max Score |
|---|---:|
| Wallet younger than 7 days | 549 |
| Wallet younger than 30 days with thin evidence | 599 |
| Low confidence profile | 649 |
| Active scam-cluster interaction | 449 |
| Severe unresolved fraud attestation | 399 |
| Confirmed Sybil cluster | 499 |
| Multiple unresolved disputes | 549 |
| Recent liquidation with no recovery | 599 |
| Possible compromised wallet | 649 |
| High score but weak evidence | 699 |

## TypeScript Constants

```ts
export const GWAPSCORE_V2_WEIGHTS = {
  walletMaturity: 0.12,
  transactionConsistency: 0.13,
  counterpartyQuality: 0.20,
  protocolDiversity: 0.10,
  securityHygiene: 0.10,
  lendingCreditBehavior: 0.15,
  commerceReliability: 0.08,
  sybilResistance: 0.07,
  recoveryBehavior: 0.05,
} as const;

export const GWAPSCORE_TIERS = [
  { min: 300, max: 449, tier: "critical_risk" },
  { min: 450, max: 549, tier: "high_risk" },
  { min: 550, max: 649, tier: "thin_or_developing" },
  { min: 650, max: 724, tier: "standard" },
  { min: 725, max: 799, tier: "trusted" },
  { min: 800, max: 900, tier: "elite" },
] as const;

export const GWAPSCORE_V2_CAPS = {
  NEW_WALLET_UNDER_7_DAYS: 549,
  THIN_FILE_UNDER_30_DAYS: 599,
  LOW_CONFIDENCE: 649,
  ACTIVE_SCAM_CLUSTER_EXPOSURE: 449,
  SEVERE_UNRESOLVED_FRAUD: 399,
  CONFIRMED_SYBIL_CLUSTER: 499,
  MULTIPLE_UNRESOLVED_DISPUTES: 549,
  RECENT_LIQUIDATION_NO_RECOVERY: 599,
  POSSIBLE_COMPROMISED_WALLET: 649,
  HIGH_SCORE_WEAK_EVIDENCE: 699,
} as const;
```
