# Case Study: YouTube Shorts Script Optimization

## Overview

Applied the autoresearch pattern to optimize a SKILL.md prompt that generates YouTube Shorts scripts. Used an LLM judge as the evaluation function.

## Setup

- **Mutable file**: SKILL.md (prompt instructions for generating YouTube Shorts scripts)
- **Eval function**: LLM judge scoring each generated script 1-100 across multiple criteria (hook strength, pacing, word count compliance, emotional impact)
- **Test cases**: 10 diverse topic prompts
- **Total experiments**: 11

## Results

| Metric | Baseline | Final | Change |
|--------|----------|-------|--------|
| **Quality Score** | 94.3/100 | 96.7/100 | **+2.5%** |
| Experiments | — | 11 | — |
| Improvements kept | — | 4 | — |

## Key Discoveries

### 1. Atomic Sentences
- **What**: Added rule "every sentence must convey exactly one idea"
- **Before**: Scripts had compound sentences that felt rushed when read aloud
- **After**: Cleaner pacing, easier for viewers to follow
- **Score impact**: +0.8 points

### 2. Strict 40-50 Word Range
- **What**: Changed "keep it short" to "strictly 40-50 words, no exceptions"
- **Before**: Scripts ranged from 35-65 words, inconsistent pacing
- **After**: Tight, consistent scripts that fit perfectly in 15-second Shorts
- **Score impact**: +0.6 points

### 3. Stronger Negative Examples
- **What**: Added explicit "NEVER do this" examples to the prompt
- **Before**: Prompt said "avoid clichés" (vague)
- **After**: Prompt showed 3 specific bad examples with explanations of why they fail
- **Score impact**: +0.5 points

### 4. Hook Pattern Library
- **What**: Added 5 proven hook templates (question, shocking stat, myth-bust, contrast, story)
- **Score impact**: +0.5 points

## Experiment Log

```
exp-1:  Add "atomic sentences" rule              | 94.3 → 95.1  ✅
exp-2:  Change word limit to 30-40               | 95.1 → 94.8  ❌ REVERTED
exp-3:  Add negative examples section            | 95.1 → 95.6  ✅
exp-4:  Require emoji in every script            | 95.6 → 93.2  ❌ REVERTED
exp-5:  Add hook pattern library                 | 95.6 → 96.1  ✅
exp-6:  Mandate rhetorical questions             | 96.1 → 95.4  ❌ REVERTED
exp-7:  Strict 40-50 word range                  | 96.1 → 96.7  ✅
exp-8:  Add "conversational tone" instruction    | 96.7 → 96.5  ❌ REVERTED
exp-9:  Remove all formatting instructions       | 96.7 → 94.1  ❌ REVERTED
exp-10: Add "end with call to action"            | 96.7 → 96.3  ❌ REVERTED
exp-11: Increase negative examples to 5          | 96.7 → 96.6  ❌ REVERTED
```

## Takeaways

1. **Diminishing returns are real**: Started at 94.3 (already good). Getting from 94→97 is much harder than 80→94. Only 4 of 11 experiments improved the score.
2. **Specificity wins**: Vague instructions ("keep it short") scored worse than precise ones ("40-50 words"). The LLM follows exact rules better than vibes.
3. **Negative examples are powerful**: Showing the model what NOT to do was more effective than adding more positive instructions.
4. **Not every good idea helps**: "Conversational tone" and "call to action" sound like they should improve scripts, but the data said otherwise. Trust the eval, not your intuition.
5. **Know when to stop**: After 3 consecutive reverts (exp-9, 10, 11), the prompt was likely near its ceiling for this eval function. Further gains would need a better eval or different approach.
