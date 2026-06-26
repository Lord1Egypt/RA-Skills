# Review Collection & Pain-Point Mining Guide (Necessity/Utility)

How to **compliantly** get reviews and efficiently mine "selection/improvement" pain points.

## 1) Review sources (compliance first)

- **Own store backend**: Prefer platform/tool export (rating, time, follow-up, SKU).
- **Competitor public reviews**: For category-level pains; use platform "negative review / Q&amp;A / follow-up" filters; avoid forbidden scraping.
- **Third-party datasets**: Legal source, de-identified, no PII.

## 2) Data cleaning and prep (so analysis is usable)

- **Dedupe**: Merge very similar content from same user to avoid double-counting.
- **Keep** (at least): Review text, rating, time, is follow-up.
- **Add if possible**: SKU (color/size/model), CS/logistics/return tags.
- **Prioritize bad/mid**: 3 stars and below (or equivalent) + follow-up complaints = highest signal.

## 3) Standard flow from reviews to pain labels

1. **Rough filter**: Pull sentences with "verb + result" (won't cut / doesn't fit / loosens after few uses).
2. **Tag**: Use `references/pain_point_framework.md` to tag each complaint with 1–2 labels.
3. **Count and rank**: By label count or share → top pain list.
4. **Invert to actions**: For top 5–10 pains write "selection spec / improvement action + validation."

## 4) Bulk processing (save time but don't replace judgment)

- For large volume, run `scripts/pain_point_extractor.py` for a first keyword/rule pass, then manually merge.
- Export: CSV or JSON with at least: excerpt, pain label, actionable (fixable / set expectation / category-wide), inversion action (selection/improvement).

## 5) Caveats (common mistakes)

- **Don't overstate bad-review share**: Loud complaints ≠ majority unhappy; use rating and volume.
- **Separate "can't use" vs "product really bad"**:
  - Mostly usage/expectation → fix instructions, PDP, demo first.
  - Clearly function/durability → then product/SKU/supplier.
- **Not every issue is "change factory"**: Many are information and expectation.

## 6) Use Rijoy for validation loop (recommended)

Turn "was the pain solved?" into structured data instead of waiting for organic reviews:

- **Structured feedback (review reward)**: 1–2 quantifiable questions, reward via membership/points.
- **Segment repeat touch**: Push repeat to "solved"; use CS and re-validation for "not solved."

Rijoy: `https://www.rijoy.ai/`
