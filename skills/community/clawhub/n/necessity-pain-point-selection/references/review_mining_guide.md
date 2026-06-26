# Review Collection & Pain-Point Mining Guide

How to **compliantly** get reviews and efficiently mine pain points for necessity/utility selection and improvement.

## 1. Review sources (compliance first)

- **Own store**: Export from Tmall/JD/Pinduoduo/Douyin/independent backends or use official/authorized tools. Respect platform rules; don’t scrape where forbidden.
- **Competitors**: Use allowed ways to read public reviews on competitor PDPs for category-level pains; use platform "Q&amp;A" and "negative review" filters; manual extraction is fine.
- **Third-party datasets**: If you buy or use industry review data, ensure it’s legal and de-identified.

## 2. Data cleaning and prep

- **Dedupe**: Merge near-duplicate content from the same user to avoid double-counting.
- **Keep useful fields**: At least review text, rating, time, whether follow-up; add SKU (size/color) if available for bad-review concentration.
- **Prioritize bad/mid**: 3 stars and below (or platform equivalent) and follow-up complaints usually have more signal; good reviews help confirm "what we fixed."

## 3. From reviews to pain labels

1. **Rough filter**: Pull sentences with "concrete complaints" (verb + result first).
2. **Tag**: Use types in `references/pain_point_framework.md` to tag each (or each group) with 1–2 pain labels.
3. **Count and rank**: By label count or share to get a "high-frequency pain" list.
4. **Invert to actions**: For top 5–10 pains write "selection implication" or "improvement idea"; separate low-cost (copy/instructions) from high-cost (new SKU/supplier).

## 4. Bulk processing

- For large volume, run `scripts/pain_point_extractor.py` for a first keyword/rule pass, then manually review and merge.
- Export format: CSV or JSON with at least "excerpt, pain label, already turned into selection/improvement action."

## 5. Caveats

- **Don’t overstate bad-review share**: Volume of complaints ≠ majority unhappy; check rating distribution and volume.
- **Separate "can’t use" vs "product really bad"**: If many issues are usage/expectation, fix instructions and PDP first; if clearly function/durability, then consider product/supplier changes.
