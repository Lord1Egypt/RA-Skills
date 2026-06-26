# Sentiment Rules - Google Reviews

Use deterministic heuristics first, then optional model refinement.

## Classification Baseline

- `positive`: clear praise, favorable outcome, no unresolved complaint.
- `neutral`: factual note without strong positive or negative tone.
- `negative`: clear dissatisfaction, unresolved issue, or strong warning.
- `mixed`: explicit positives and negatives in the same review.

## Theme Taxonomy

Apply one or more themes when evidence exists:
- service-quality
- delivery-or-wait-time
- pricing-value
- product-quality
- staff-behavior
- refund-or-resolution
- listing-accuracy

## Alert Triggers

Flag high urgency when any condition is true:
- Negative review includes legal, fraud, safety, or discrimination claims
- 7-day negative ratio increases above configured threshold
- Average rating drops sharply vs baseline in a single refresh window

## Confidence Guidance

- Fewer than 10 reviews in window: mark trend confidence as low.
- 10-49 reviews: medium confidence.
- 50+ reviews: high confidence when source coverage is stable.
