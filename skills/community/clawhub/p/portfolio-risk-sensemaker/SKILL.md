---
name: portfolio-risk-sensemaker
description: A plain-English portfolio reading skill that turns a holdings list into understandable risk patterns. Use when the user wants to understand the risk profile of their crypto holdings. Prompt-only.
---

# portfolio-risk-sensemaker

A plain-English portfolio reading skill that turns a holdings list into understandable risk patterns.

## Workflow

1. Ask for holdings as percentages, rough buckets, or ranked positions.
2. Identify concentration risk, style overlap, stablecoin assumptions, and exposure imbalance.
3. Describe what kinds of downside scenarios would hurt this mix most.
4. Offer reflection questions before adding more assets.
5. Suggest what information is still missing.

## Output Format

- Portfolio snapshot
- Top 3 risk patterns
- What this mix seems optimized for
- Questions to ask before changing it
- Missing-data note

## Quality Bar

- Easy to understand without charts.
- Honest about assumptions and rough inputs.
- Focuses on exposure logic, not price prediction.
- Helps the user notice behavior risk as well as allocation risk.

## Edge Cases

- If the user gives incomplete numbers, work with ranges and label uncertainty.
- Cannot calculate live valuations, taxes, or actual correlations.

## Compatibility

- Prompt-only, works from user-typed holdings.
- Good fit for monthly review conversations.
