# OpenReview Review Synthesis Report Template

## Standard Report Format

```
══════════════════════════════════════════════════════
  论文评审综合分析报告 / Paper Review Synthesis Report
══════════════════════════════════════════════════════

📄 论文信息 / Paper Info
  标题: [title]
  作者: [authors]
  会议: [venue]
  链接: [url]

══════════════════════════════════════════════════════

📊 评分概览 / Score Overview

| Reviewer | Rating | Confidence | 一句话评价 |
|----------|--------|------------|-----------|
| Reviewer 1 (签名) | X/10 | X/5 | [核心观点] |
| Reviewer 2 (签名) | X/10 | X/5 | [核心观点] |
| Reviewer 3 (签名) | X/10 | X/5 | [核心观点] |
| **平均** | **X.X** | **X.X** | |

══════════════════════════════════════════════════════

✅ 共识优点 / Consensus Strengths
[多位审稿人共同认可的优点，标注被几位审稿人提到]

❌ 共识缺点 / Consensus Weaknesses
[多位审稿人共同指出的缺点]

⚔️ 意见分歧 / Key Disagreements
[审稿人之间观点不一致的地方，说明各方立场]

══════════════════════════════════════════════════════

📋 逐条审稿意见 / Detailed Review Breakdown

### Reviewer 1 [签名] — Rating: X/10, Confidence: X/5

**优点 (Strengths):**
- [要点1]
- [要点2]

**缺点 (Weaknesses):**
- [要点1]
- [要点2]

**问题 (Questions):**
- [问题1]

**其他评论:**
[额外评论]

---
[对每个 Reviewer 重复上述结构]

══════════════════════════════════════════════════════

💬 作者回复摘要 / Author Rebuttal Summary
[如有 rebuttal，总结作者对主要质疑的回应]
[标注审稿人是否在讨论后修改了评分]

══════════════════════════════════════════════════════

📝 Meta-Review / AC 意见
[如有 meta-review，总结 AC 的综合评估和建议]

══════════════════════════════════════════════════════

🏁 Decision / 最终决定
[如有 decision，列出接受/拒绝/修改后接受等决定]

══════════════════════════════════════════════════════

🔍 综合评估 / Overall Assessment

**核心发现:**
[用 2-3 句话总结审稿人的整体态度]

**主要风险点:**
[列出论文最需要解决的 2-3 个关键问题]

**建议:**
[基于审稿意见，给出论文修改方向的建议]

══════════════════════════════════════════════════════
```

## Analysis Guidelines

When synthesizing reviews, follow these principles:

1. **Quantitative first** — Always present scores and averages prominently
2. **Cross-reviewer patterns** — Identify which concerns are raised by multiple reviewers vs. only one
3. **Weight by confidence** — Higher-confidence reviewers' opinions carry more analytical weight
4. **Preserve nuance** — Don't flatten disagreements into a single narrative
5. **Track score changes** — If reviewers updated scores post-rebuttal, note the before/after
6. **Flag critical issues** — Issues marked as "major weaknesses" or that could independently justify rejection
7. **Separate fact from opinion** — Distinguish technical errors found by reviewers from subjective assessments
8. **Comment threads** — Summarize substantive discussion threads between authors and reviewers

## Common Review Content Fields

Different venues use different field names. Common ones include:

- `rating` / `recommendation` / `score` / `overall_assessment` — numerical score
- `confidence` / `reviewer_confidence` — how confident the reviewer is
- `summary` / `review` — main review body
- `strengths` / `main_strengths` — positive aspects
- `weaknesses` / `main_weaknesses` — negative aspects
- `questions` / `questions_for_authors` — questions raised
- `limitations` / `ethical_concerns` — limitations/ethics discussion
- `soundness` / `presentation` / `contribution` / `clarity` — sub-scores

## Handling Edge Cases

- **Withdrawn paper with hidden reviews**: Inform user that reviews are not publicly available. Suggest checking if a cached version exists.
- **No reviews yet**: Inform user that the review period may not have ended. Provide paper metadata.
- **Only 1 review**: Skip "consensus" section, do detailed analysis of the single review.
- **Very long reviews**: Summarize each review to key points (strengths, weaknesses, questions). Offer to show full text if requested.
- **Author responses in comments**: Include them in the rebuttal section even if formally posted as "Official Comment" rather than "Rebuttal".
