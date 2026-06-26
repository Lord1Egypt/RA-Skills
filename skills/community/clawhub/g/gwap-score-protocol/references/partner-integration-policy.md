# Partner Integration Policy

Partners may use GwapScore Protocol v2 for trust labels, gating, payment flows, escrow recommendations, creator/merchant profiles, and wallet risk explanations.

## Recommended API Endpoints

```txt
GET /v2/score/:wallet
POST /v2/score/recalculate
GET /v2/score/:wallet/explanation
GET /v2/score/:wallet/attestations
POST /v2/attestations
POST /v2/disputes
POST /v2/manual-review
```

## Partner Output Rules

Partner-facing responses should include:

- Wallet
- Protocol score
- Tier
- Confidence
- Score version
- Category breakdown
- Risk flags
- Caps applied
- Explanation
- Last updated timestamp

## Partner Safety Rules

1. Do not describe the score as personal creditworthiness unless product/legal review approves that framing.
2. Do not present the score as wealth.
3. Do not reveal sensitive or unsupported personal inferences.
4. Explain caps and risk flags clearly.
5. Distinguish low confidence from low trust.
6. Give users a dispute path for severe negative labels.
