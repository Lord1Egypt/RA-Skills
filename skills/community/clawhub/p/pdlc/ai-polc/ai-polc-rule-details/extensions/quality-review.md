<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: Quality Review AI-Assist (Full Rules)

**Stage:** Post-Stage 5, or during Stage 14 (Backlog Operations)
**Adds:** Automated quality scanning of epics and stories

---

## Quality Scan Process

### Scan Triggers
- After Stage 5 (epic decomposition) — validate all new epics
- During Stage 14 (backlog ops) — periodic quality health check
- On user request ("check quality")

### Scan Dimensions

For each epic (or story if Tier 2 active):

| Dimension | What It Checks | Flag If |
|-----------|---------------|---------|
| **Ambiguity** | Vague words: "appropriate", "adequate", "good", "improve", "etc." | >2 vague terms found |
| **Missing AC** | No acceptance criteria, or AC not testable | AC count = 0 or AC uses "should" without measure |
| **Scope Mixing** | Epic addresses multiple unrelated concerns | >2 themes in one epic |
| **Size Risk** | Epic is XL with no split plan | Estimated XL AND no sub-items |
| **Dependency Blind Spots** | References other components without declaring dependency | Mentions "after" or "requires" without deps listed |
| **Value Gap** | No goal linkage or value justification | Missing goal reference |
| **Implementation Leak** | Prescribes HOW instead of WHAT | Contains technology names, code patterns, or "implement using" |

### Scoring

Each epic gets a quality score:

| Score | Meaning | Action |
|:---:|---|---|
| 5 | Excellent — ready for development | No action |
| 4 | Good — minor improvements possible | Optional refinement |
| 3 | Acceptable — passes DoR but has gaps | Recommend refinement |
| 2 | Needs work — fails DoR | Must refine before sprint |
| 1 | Poor — not actionable | Rewrite required |

### Output

Quality review produces a summary:

```
Backlog Quality Report
━━━━━━━━━━━━━━━━━━━━
Epics scanned: {N}
Average quality score: {X}/5

Score distribution:
  5 (Excellent): {N} epics
  4 (Good):      {N} epics
  3 (Acceptable):{N} epics
  2 (Needs work):{N} epics ⚠️
  1 (Poor):      {N} epics ❌

Top issues found:
1. {issue type}: {N} epics affected — {example}
2. {issue type}: {N} epics affected — {example}
3. {issue type}: {N} epics affected — {example}

Recommended actions:
- Refine: {list of epics scoring 2}
- Rewrite: {list of epics scoring 1}
```

### Remediation

For each flagged epic, provide specific fix suggestions:
```
EPIC-007: Score 2/5
Issues:
  ⚠️ Ambiguity: "improve user experience" — what specific UX metric?
  ⚠️ Missing AC: 0 acceptance criteria defined
  ⚠️ Scope mixing: covers both onboarding AND profile management

Suggestion:
  1. Split into EPIC-007a (onboarding) and EPIC-007b (profile)
  2. Add measurable AC: "onboarding completion rate > 80%"
  3. Replace "improve" with specific target metric
```
