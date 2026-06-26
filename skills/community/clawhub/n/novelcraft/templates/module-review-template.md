# NovelCraft Module Template: Review

## Task for Subagent

Review ONE chapter and assign a score for automatic decision-making.

**STEP 1: Load Configuration**
Read these files:
1. `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/project-manifest.md`
2. `/home/felix/.openclaw/workspace/novelcraft/config/module-chapters.md`
3. `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/00-concept/concept.md`

**STEP 2: Read Chapter to Review**
Read draft: `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/01-drafts/chapter_{CHAPTER_NUMBER}_draft.md`

**STEP 3: Read Previous Chapter (if applicable)**
If chapter > 1, read previous approved chapter from `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/02-chapters/` for continuity check.

**STEP 4: Score Each Criterion**

Rate 1-10 (10 = excellent):

| Criterion | Weight | Score | Notes |
|-----------|--------|-------|-------|
| Encoding UTF-8 | CRITICAL (×3) | _/10 | No foreign chars |
| Word count 7000-8000 | HIGH (×2) | _/10 | Exact target: 7500 |
| Continuity | HIGH (×2) | _/10 | Consistent with previous |
| Plot progression | HIGH (×2) | _/10 | Story advances logically |
| Character voice | MEDIUM (×1.5) | _/10 | Believable actions |
| Style & atmosphere | MEDIUM (×1.5) | _/10 | Matches project style |
| Grammar & spelling | LOW (×1) | _/10 | Correct German |

**STEP 5: Calculate Weighted Score**

```
Weighted Score = Σ(criterion_score × weight) / Σ(weights)
Max possible: 10.0
```

**STEP 6: Automatic Decision**

| Weighted Score | Decision | Action |
|----------------|----------|--------|
| 8.0 - 10.0 | APPROVED | Proceed to next chapter |
| 6.0 - 7.9 | MINOR_REVISION | Specific fixes, keep most content |
| 4.0 - 5.9 | MAJOR_REVISION | Significant rewrite needed |
| 0.0 - 3.9 | REJECTED | Complete rewrite required |

**STEP 7: Report Structure**

```
## Review: Chapter {CHAPTER_NUMBER}

**Weighted Score:** X.X / 10

**Criterion Breakdown:**
| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| ... | ... | ... | ... |

**Decision:** [APPROVED / MINOR_REVISION / MAJOR_REVISION / REJECTED]

**Required Changes (if not APPROVED):**
1. [Specific change with location]
2. [Specific change with location]
3. ...

**Strengths:**
- ...
- ...

**Weaknesses:**
- ...
- ...
```

**STEP 8: Save Review**
Save to: `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/01-drafts/chapter_{CHAPTER_NUMBER}_review.md`

**STEP 9: If APPROVED - Move to Final Location**
Copy approved chapter to: `/home/felix/.openclaw/workspace/novelcraft/Books/projects/{PROJECT}/02-chapters/chapter_{CHAPTER_NUMBER}.md`

**STEP 10: Return Decision**
State clearly: "DECISION: [APPROVED/MINOR_REVISION/MAJOR_REVISION/REJECTED]"
