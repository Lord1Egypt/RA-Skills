# Groupon Deal Qualification

Use the SAVE scorecard before recommending any Groupon deal.

## SAVE

| Step | What to check | Output |
|------|---------------|--------|
| Scope | city, category, date window, party size, budget, travel tolerance | real use case |
| Assess | merchant quality, review recency, booking friction, deal fit | trust and usability score |
| Verify | restrictions, voucher type, booking path, extras, expiration logic | blocking terms |
| Estimate | total cash outlay, travel overhead, effort, and fallback options | true value verdict |

## Fast Intake

Collect the smallest set of details needed to judge value:
- exact deal link or category
- who it is for
- target date or redemption window
- hard budget ceiling
- whether the user values novelty, convenience, or pure savings most

If any of those are missing and the answer would change the ranking, ask.

## Scoring Grid

Score each category from 1 to 5:

| Category | 1 | 3 | 5 |
|----------|---|---|---|
| Fit | wrong category or timing | usable with caveats | matches the exact need |
| Merchant trust | weak recent signals | mixed | strong recent signals |
| Restrictions | many blockers | manageable | flexible and clear |
| True cost | extras erase savings | small savings | clear and meaningful savings |
| Friction | hard to book or redeem | moderate effort | easy to use |

## Verdict Thresholds

| Score | Verdict | Meaning |
|-------|---------|---------|
| 21-25 | Recommend | strong fit, low friction, real savings |
| 16-20 | Recommend with caveats | worth it only if the caveats are acceptable |
| 5-15 | Skip | too much risk, weak value, or hard to redeem |

## True Cost Checklist

Always estimate:
- voucher price
- taxes and service charges if visible
- gratuity rules
- required upgrades or mandatory spend above the voucher
- travel or parking cost if material
- likely extra spend once on site

## Output Template

```text
Verdict: Recommend | Recommend with caveats | Skip
Deal: [title or URL]
SAVE score: [x/25]
Best for: [who and when]
Why it works:
- ...
- ...
- ...
Caveats:
- ...
True cost:
- Voucher:
- Expected extras:
- Total likely spend:
Next step:
- Buy now | Hold | Compare alternatives | Contact merchant | Request support
```

## When to Downrank Immediately

Downrank hard when any of these appear:
- vague or contradictory fine print
- recent complaints about unavailable booking slots
- inflated "original value" with no credible market check
- a merchant profile that looks inactive, rebranded, or overloaded
- a deal that only works outside the user's usable time window
