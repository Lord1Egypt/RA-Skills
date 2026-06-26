# GwapScore Protocol v2 Confidence Model

Confidence is separate from score.

A wallet can have:

- High score and high confidence
- High score and low confidence
- Low score and high confidence
- Low score and low confidence

The protocol must never use score alone for high-impact decisions.

## Confidence Levels

| Level | Meaning |
|---|---|
| low | Thin evidence, short history, weak source quality, or conflicting signals |
| moderate | Enough reliable evidence for basic trust decisions |
| high | Deep history across time, counterparties, protocols, and/or verified attestations |

## Confidence Factors

| Factor | Positive Indicator |
|---|---|
| Evidence depth | More reliable onchain events and attestations |
| Wallet age | Longer observed history |
| Activity duration | Multiple active months |
| Source quality | Reputable protocols, partners, and verified events |
| Counterparty reliability | Interactions with known clean counterparties |
| Manual review status | Resolved review can increase confidence |
| Conflicting evidence penalty | Conflicting signals reduce confidence |

## Formula Concept

```ts
confidenceScore =
  evidenceDepthScore * 0.25 +
  activityDurationScore * 0.20 +
  sourceQualityScore * 0.20 +
  counterpartyReliabilityScore * 0.20 +
  manualReviewScore * 0.10 -
  conflictingEvidencePenalty * 0.15;
```

## Confidence Classification

| Confidence Score | Level |
|---:|---|
| 0–44 | low |
| 45–74 | moderate |
| 75–100 | high |

## Required Output

Every score response must include:

```ts
type ConfidenceBreakdown = {
  evidenceDepth: number;
  activityDuration: number;
  sourceQuality: number;
  counterpartyReliability: number;
  manualReviewStatus: number;
  conflictPenalty: number;
  finalConfidence: "low" | "moderate" | "high";
};
```

## Rules

- New wallets should usually have low confidence.
- Thin evidence should cap confidence.
- Manual review can increase or decrease confidence depending on outcome.
- Spam/dust token receipts should not reduce confidence unless tied to repeated intentional interaction.
- Conflicting evidence must be disclosed in the explanation.
