# Pricing and Deals - Mercado Libre

Use this file for deal validation, price sanity checks, and timing decisions.

## Deal Validation Sequence

1. Compare candidate against similar listings.
2. Check if discount claim is consistent with market context.
3. Estimate real savings after shipping and risk adjustments.
4. Label deal as strong, acceptable, or weak.

## False Urgency Patterns

Treat these as caution signals:
- deep discount with low seller credibility
- low headline price with high shipping surprise
- deadline pressure with no evidence of real scarcity
- inconsistent product attributes across media and text

## Real Savings Formula

```text
Real Savings = Reference Total Cost - Candidate Total Cost - Risk Premium
```

Where Risk Premium increases if seller reliability or return confidence is low.

## Watchlist Rules

For products user can wait on:
- define target buy price and max acceptable delivery time
- define re-check cadence
- trigger alert when candidate crosses threshold with acceptable risk

## Output Template

```text
Listing evaluated:
Reference baseline:
Real savings estimate:
Risk premium:
Verdict:
Buy now or wait:
```
