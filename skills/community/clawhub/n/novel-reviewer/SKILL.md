---
name: novel-reviewer
description: Multi-dimensional novel evaluation based on provided content, assessing across plot, characters, writing quality, worldbuilding, pacing, originality, emotional resonance, dialogue quality, structure, and reader appeal, producing a total score. Use for book reviews, work evaluation, creative feedback, web novel assessment, and similar scenarios.
---

# Multi-Dimensional Novel Evaluation System

## How to Use

Provide novel content (chapter/excerpt/full submission), evaluate as follows:

1. **Input**: Title, author, genre (optional); body content
2. **Score by dimension**: 10 dimensions, each 1-10 points
3. **Comprehensive review**: Total score + strengths/weaknesses analysis + improvement suggestions

## Ten Evaluation Dimensions

| Dimension | Weight | Scoring Summary |
|-----------|--------|-----------------|
| Plot Logic | 15% | Complete causal chain, reasonable conflict, foreshadowed reversals, no dumbing-down |
| Character Development | 15% | Distinct personality, clear motivation, growth arc, dialogue matches profile |
| Writing Quality | 12% | Language fluency, description precision, rhythm control, style consistency |
| Worldbuilding | 10% | Self-consistent rules, unique originality, reasonable reveal rhythm |
| Pacing | 12% | H/W/P/T ratio, information density, fatigue level, climax distribution |
| Originality | 8% | Setting uniqueness, anti-trope plot, narrative approach novelty |
| Emotional Resonance | 10% | Reader immersion, emotional tension, empathy trigger design |
| Dialogue Quality | 8% | Dialogue naturalness, subtext, personalization, information delivery efficiency |
| Structure | 5% | Volume/chapter clarity, foreshadowing resolution rate, multi-plot coordination |
| Reader Appeal | 5% | Opening hook strength, cliffhanger effectiveness, sustained reading desire |

Weights total 100%. Each dimension scored 1-10, weighted to produce **total score (out of 10)**.

## Scoring Tiers

| Score | Tier | Description |
|-------|------|-------------|
| 9.0-10 | ⭐ Masterpiece | Nearly flawless across all aspects, industry benchmark |
| 8.0-8.9 | 🌟 Excellent | Outstanding work with clear highlights |
| 7.0-7.9 | 👍 Good | Quality online, pleasant reader experience |
| 6.0-6.9 | 🆗 Readable | Above passing, room for improvement |
| 5.0-5.9 | ⚠️ Weak | Multiple issues, needs targeted improvement |
| <5.0 | ❌ Rewrite Needed | Fundamental problems exist |

## Evaluation Output Format

```
═══════════════════════════════════════
【Novel Evaluation Report】

Title:
Author:
Genre:
Evaluation scope: Chapter X - Chapter Y

I. Dimension Scores
1. Plot Logic: [X/10]  weighted: X.X
   Comments: ...

2. Character Development: [X/10]  weighted: X.X
   Comments: ...

... (10 items total)

II. Total Score
  Total = Σ(dimension score × weight) = X.X / 10
  Tier: XXX

III. Overall Assessment
- Greatest strengths:
- Key weaknesses:
- Comparison with similar works:
- Target reader match:

IV. Improvement Suggestions
- Priority (high ROI):
- Optional:
- Not recommended to change (signature elements):
═══════════════════════════════════════
```

See [references/dimensions.md](references/dimensions.md) for detailed per-dimension scoring guidelines.
