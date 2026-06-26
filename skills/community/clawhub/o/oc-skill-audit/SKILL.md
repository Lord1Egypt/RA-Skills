---
name: skill-audit
description: >
  Audit and score OpenClaw AgentSkills against structural compliance, quality standards, and
  OpenClaw-specific architecture patterns. Produces a 0-100 score with A-F grade, dimensional
  breakdown, and actionable improvement recommendations. Use when asked to audit, score, validate,
  check, or evaluate a skill or SKILL.md.
  Keywords: skill audit, skill score, skill check, skill validate, 스킬 검증, 스킬 점수, 스킬 평가, 스킬 감사, 스킬 점검, スキル検証, スキル採点, スキル評価, スキル監査, 技能验证, 技能评分, 技能检查, 技能审计.
  validate skill, skill quality, 스킬 품질.
---

# Skill Audit

Audit and score OpenClaw AgentSkills with a multi-dimensional scoring system.

## Quick Start

"audit this skill" or "score path/to/SKILL.md"

## Language Policy

- **Audit reports**: Always generate in **two languages**:
  1. **User's language** — for accessibility (detect from request language or target SKILL.md body language)
  2. **English** — for global shareability and comparability
- Both versions should be complete (scores, dimension analysis, improvement recommendations).
- Format: write the user-language version first, then the English version, separated by a clear divider.
- If the user already requested English, a single English version suffices (no duplication).

## Scoring Overview

```
Total (0–100) = Weighted Average

Dimension           Weight  Score Range  Description
─────────────────── ─────── ─────────── ───────────
A. Structure         20%    0–100       Spec compliance, frontmatter, file structure
B. Triggering        15%    0–100       description quality, keywords, triggering
C. Style Guide       20%    0–100       Judgment criteria, preservation/compression rules
D. Workflow          15%    0–100       Phase 0, sub-agent design
E. Sub-Agent Design  15%    0–100       Context injection, templates
F. Conciseness       15%    0–100       SKILL.md length, references separation

Grade: A(90+) | B(75+) | C(60+) | D(45+) | F(<45)
```

## How to Audit

1. **Read** target SKILL.md and any references/
2. **Score** each dimension using the rubric below
3. **Calculate** weighted total and grade
4. **Report** score card + improvement recommendations

---

## Dimension A: Structure (20%)

Frontmatter, file structure, agentskills spec compliance.

| Check | Points | Criteria |
|-------|--------|----------|
| Frontmatter exists | 15 | `---` opening and closing present |
| `name` valid | 10 | lowercase, hyphens only, 1-64 chars |
| `description` present | 15 | Non-empty, 1-1024 chars |
| `description` has keywords | 10 | Keywords in multiple languages |
| No auxiliary files | 10 | No README.md, CHANGELOG.md, etc. |
| references/ organized | 10 | If exists, 1-level deep, TOC for >100 lines |
| SKILL.md under 500 lines | 10 | Lean body, details in references/ |
| No duplication | 5 | Info in SKILL.md OR references, not both |
| Folder name matches name | 15 | `skill-name/SKILL.md` |

**Max: 100**

---

## Dimension B: Triggering (15%)

Whether the description triggers the agent correctly.

| Check | Points | Criteria |
|-------|--------|----------|
| "What" described | 20 | Clear description of what it does |
| "When" in description | 25 | Trigger conditions in description (not body) |
| Keywords (Korean) | 15 | Korean keywords included |
| Keywords (English) | 15 | English keywords included |
| Not too verbose | 10 | description ≤ 300 words (metadata cost) |
| Not too vague | 15 | Not overly broad (e.g., "helpful skill") |

**Max: 100**

---

## Dimension C: Style Guide (20%)

Whether judgment criteria (preservation/compression) are specified.

**Applicability:**
- **Applies:** Text processing/transformation/summarization skills (tasks that modify original content)
- **Partially applies:** Code generation/modification skills (may need existing code preservation criteria)
- **N/A:** Structured data management (JSON/DB CRUD), simple tool wrappers, configuration management

For N/A skills, **exclude** this dimension and redistribute weights among remaining dimensions:
- Only C is N/A: A:24%, B:18%, D:18%, E:18%, F:22%
- Only E is N/A: A:24%, B:18%, C:24%, D:18%, F:16%
- Both C+E are N/A: A:30%, B:20%, D:20%, F:30%

| Check | Points | Criteria |
|-------|--------|----------|
| Preservation criteria | 30 | "What to preserve" with specific examples |
| Compression criteria | 25 | "What to compress" with specific examples |
| Task essence defined | 20 | Core task definition (e.g., "summarization is restructuring, not compression") |
| Style rules explicit | 15 | Specific rules for tone, style, length, etc. |
| Anti-patterns | 10 | "What not to do" specified (bonus) |

**Max: 100**

---

## Dimension D: Workflow (15%)

Whether Phase 0, execution order, and validation steps exist.

| Check | Points | Criteria |
|-------|--------|----------|
| Phase 0 (analysis) first | 30 | Full understanding step before task execution |
| Clear phase numbering | 15 | Phase 0, 1, 2... structured |
| Context injection described | 25 | Explicit statement that Phase 0 results are injected into sub-agent prompts |
| Validation step | 20 | Result quality validation step (length/style/omissions) |
| Error handling | 10 | Failure response instructions |

**Max: 100**

---

## Dimension E: Sub-Agent Design (15%)

Sub-agent prompt design quality.

**Applicability:**
- **Applies:** Skills that use sub-agents (parallel/sequential chunk processing, etc.)
- **Partially applies:** Skills that optionally mention sub-agent delegation (core is single-agent)
- **N/A:** Skills that do not use sub-agents at all

For N/A skills, **exclude** this dimension and redistribute weights among remaining dimensions:
- Only C is N/A: A:24%, B:18%, D:18%, E:18%, F:22%
- Only E is N/A: A:24%, B:18%, C:24%, D:18%, F:16%
- Both C+E are N/A: A:30%, B:20%, D:20%, F:30%

| Check | Points | Criteria |
|-------|--------|----------|
| Prompt template exists | 20 | Template file in references/ |
| `[ ]` placeholders | 20 | Blank fields filled by Phase 0 explicitly marked |
| Context fields defined | 20 | Full context, chunk position, preservation list |
| Style rules in template | 15 | 3-4 line style instructions included |
| Merge ≠ concatenate | 15 | Explicit prohibition of simple concatenation |
| Sequential pipeline | 10 | Sequential ordering for multi-stage output |

**Max: 100**

---

## Dimension F: Conciseness (15%)

Context window efficiency.

| Check | Points | Criteria |
|-------|--------|----------|
| SKILL.md body < 500 lines | 40 | Length compliance |
| SKILL.md body < 300 lines | 10 | Bonus (very concise) |
| No redundant instructions | 20 | No duplicate instructions |
| "Agent is smart" principle | 15 | Does not redundantly explain what the agent already knows |
| References linked | 15 | "When to read" description for each reference file |

**Max: 100**

---

## Output Format

### Delivery

Always do both:
1. **File**: Save the full audit report (bilingual) to `~/.openclaw/workspace/skill-audit-reports/[skill-name]-audit-[YYYY-MM-DD-HHmm].md`. If the same skill is audited again, a new timestamped file is created — never overwrite previous reports. Never save inside the target skill's directory — keep skill folders clean for distribution.
2. **Response**: Include a summary card in your reply — total score, grade, top 3 improvement recommendations, and file path. Do NOT paste the full report in the response.

### Bilingual Output

Per the Language Policy above, generate two complete versions:
1. **User's language version** (first)
2. **English version** (second)

Separate them with a clear divider:
```
---
## English Version
```

If the user requested English, a single English version suffices.

### Score Card

```markdown
# Skill Audit: [skill-name]

**Version**: skill-audit v1.0
**Date**: YYYY-MM-DD
**Target**: path/to/SKILL.md

## Score: 78/100 (B)

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| A. Structure | 85 | 20% | 17.0 |
| B. Triggering | 90 | 15% | 13.5 |
| C. Style Guide | 60 | 20% | 12.0 |
| D. Workflow | 70 | 15% | 10.5 |
| E. Sub-Agent Design | 80 | 15% | 12.0 |
| F. Conciseness | 85 | 15% | 12.8 |
| **Total** | | | **77.8** |

## Grade: B

---

## Dimension Details

### A. Structure (85/100)
✅ Frontmatter exists (+15)
✅ name valid: "summarize" (+10)
✅ description present (+15)
...
❌ SKILL.md over 500 lines (-10)
→ Tip: Split detailed specs into references/

### B. Triggering (90/100)
...

## Improvement Recommendations

1. **[High]** Add preservation/compression criteria to Style Guide → C score +20 expected
2. **[Medium]** Specify Phase 0 → D score +15 expected
3. **[Low]** Add references/ TOC → A score +5 expected
```

### Improvement Priority Labels

- **[Critical]** — Skill may not function properly
- **[High]** — Major impact on quality
- **[Medium]** — Meaningful score improvement if addressed
- **[Low]** — Minor improvement

---

## Batch Mode

Audit multiple skills at once:

"Audit all skills in the skills/ folder"

→ Generate individual score cards per skill, then produce a comparison table:

```
| Skill | Total | Grade | A | B | C | D | E | F |
|-------|-------|-------|---|---|---|---|---|---|
| summarize | 82 | B+ | 93 | 88 | 88 | 77 | 78 | 65 |
| changelog | 85 | B+ | 90 | 85 | 90 | 85 | N/A | 80 |
| scaffold | 81 | B | 85 | 80 | 75 | 80 | N/A | 85 |
```

## References

- `references/scoring-rubric.md` — Detailed scoring rubric with examples per dimension
- `examples/` — Completed audit reports and batch comparisons for validated skills
