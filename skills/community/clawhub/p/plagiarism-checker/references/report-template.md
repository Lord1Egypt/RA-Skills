# Detection Report Template

## Report Structure

```
═══════════════════════════════════════════════════════════
                Content Originality & AI Detection Report
═══════════════════════════════════════════════════════════

📝 Text Overview
  Word Count: {word_count}
  Character Count: {char_count}
  Paragraph Count: {para_count}

📊 Comprehensive Score
  Originality: {originality}%
  AI Generation Probability: {ai_prob}%
  Risk Level: {risk_emoji} {risk_level}

───────────────────────────────────────────────────────────
Paragraph Analysis
───────────────────────────────────────────────────────────
{paragraph_analysis}

───────────────────────────────────────────────────────────
Recommendations
───────────────────────────────────────────────────────────
{recommendations}

═══════════════════════════════════════════════════════════
              Report Generated: {timestamp}
═══════════════════════════════════════════════════════════
```

## Example Report

```
═══════════════════════════════════════════════════════════
                Content Originality & AI Detection Report
═══════════════════════════════════════════════════════════

📝 Text Overview
  Word Count: 486
  Character Count: 2341
  Paragraph Count: 4

📊 Comprehensive Score
  Originality: 78%
  AI Generation Probability: 35%
  Risk Level: 🟡 Medium Risk

───────────────────────────────────────────────────────────
Paragraph Analysis
───────────────────────────────────────────────────────────
  ✅ Paragraph 1 (0-120 words): Original content, no significant match
  ⚠️ Paragraph 2 (121-280 words): 42% similarity
     Match Source: Web/article-123 (38%), Blog/tech-post (4%)
  ⚠️ Paragraph 3 (281-390 words): 51% AI probability
     Features: Low burstiness, high-frequency vocabulary, mechanical sentence patterns
  ✅ Paragraph 4 (391-486 words): Original content, no significant match

───────────────────────────────────────────────────────────
Recommendations
───────────────────────────────────────────────────────────
  1. Paragraph 2: Recommend rewriting, add personal analysis and unique perspective
  2. Paragraph 3: Recommend enriching sentence variety, incorporating specific examples
  3. Overall: Add more original viewpoints and firsthand experience

═══════════════════════════════════════════════════════════
              Report Generated: 2026-04-13 11:10 CST
═══════════════════════════════════════════════════════════
```

## Rewriting Suggestion Template

For each high-risk paragraph, provide:
1. **Problem Description**: "This paragraph has X% similarity with a certain source"
2. **Rewriting Direction**: "Recommend re-articulating from the perspective of personal experience / cases / data"
3. **Example Phrasing**: Provide 2-3 rewriting examples