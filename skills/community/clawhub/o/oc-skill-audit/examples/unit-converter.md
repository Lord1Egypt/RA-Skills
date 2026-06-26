# Skill Audit: unit-converter

**Version**: skill-audit v1.0
**Date**: 2026-05-21
**Target**: /home/node/.openclaw/workspace/skills/unit-converter/SKILL.md
**Type**: Single Task
**N/A Dimensions**: C (Style Guide), E (Sub-Agent Design)
**Redistributed Weights**: A:30%, B:20%, D:20%, F:30%

## Score: 76/100 (B)

| Dimension | Score | Weight | Weighted | Notes |
|-----------|-------|--------|----------|-------|
| A. Structure | 85 | 30% | 25.5 | |
| B. Triggering | 90 | 20% | 18.0 | |
| C. Style Guide | N/A | — | — | Simple tool wrapper: N/A |
| D. Workflow | 45 | 20% | 9.0 | |
| E. Sub-Agent Design | N/A | — | — | Does not use sub-agents: N/A |
| F. Conciseness | 78 | 30% | 23.4 | |
| **Total** | | | **75.9** |

## Grade: B

---

## Dimension Details

### A. Structure (85/100)
✅ Frontmatter exists (+15)
✅ name valid: "unit-converter" — lowercase, hyphens only (+10)
✅ description present — clear (+15)
✅ description has keywords — Korean + English (+10)
✅ No auxiliary files — no README.md, CHANGELOG.md (+10)
✅ references/ organized — 1-level deep, 1 file (+10)
✅ SKILL.md under 500 lines — 157 lines (+10)
✅ No duplication — conversion factors separated into references/ (+5)
✅ Folder name matches name (+15)

**Subtotal: 85/100**

### B. Triggering (90/100)
✅ "What" described — "Convert between units using natural language" (+20)
✅ "When" in description — "Use when asked to convert units, change units, or calculate equivalent values" (+25)
✅ Keywords (Korean) — 단위 변환, 단위 환산, 화씨 섭씨, 마일 킬로미터, 파운드 킬로그램, 단위 계산 (+15)
✅ Keywords (English) — convert, unit conversion, unit converter, temperature, length, weight, volume (+15)
✅ Not too verbose — description ~40 words (+10)
✅ Not too vague — clear with "natural language" and example expressions (+15)

**Subtotal: 90/100**

### C. Style Guide (N/A)
Simple unit conversion tool — no text transformation tasks. N/A.

### D. Workflow (45/100)
❌ Phase 0 first — 3-step (Parse → Convert → Respond) but no Phase 0 full understanding step (+0)
❌ Phase numbering — no Phase structure (+0)
⚠️ Context injection — no sub-agents so N/A, but parsing step indirectly serves as context (+10)
✅ Validation step — Precision Rules has output validation criteria (+15)
⚠️ Error handling — none (+5)
→ Workflow is minimal with no Phase structure at all

**Subtotal: 45/100**

### E. Sub-Agent Design (N/A)
Does not use sub-agents at all. N/A.

### F. Conciseness (78/100)
✅ SKILL.md body < 500 lines — 157 lines (+40)
✅ SKILL.md body < 300 lines — 157 lines, bonus (+10)
⚠️ No redundant instructions — conversion tables somewhat repetitive (length, weight, volume etc. similar structure) (+12)
✅ "Agent is smart" — conversion factors are reference data the agent cannot infer, so justified (+15)
⚠️ References linked — 1 reference file link (+10)
→ Conversion tables occupy most of SKILL.md but are reference material so somewhat justified

**Subtotal: 78/100**

---

## Improvement Recommendations

1. **[High]** Introduce Phase structure: Phase 0 (request parsing), Phase 1 (conversion), Phase 2 (validation+output) → D score +20 expected
2. **[Medium]** Add error handling: unsupported units, ambiguous requests etc. → D score +5 expected
3. **[Low]** Move some conversion tables to references/ (Korean parsing table etc.) → F score +5 expected
