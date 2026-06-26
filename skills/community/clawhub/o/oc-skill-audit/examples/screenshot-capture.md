# Skill Audit: screenshot-capture

**Version**: skill-audit v1.0
**Date**: 2026-05-21
**Target**: /home/node/.openclaw/workspace/skills/screenshot-capture/SKILL.md
**Type**: Tool Integration
**N/A Dimensions**: C (Style Guide), E (Sub-Agent Design)
**Redistributed Weights**: A:30%, B:20%, D:20%, F:30%

## Score: 78/100 (B)

| Dimension | Score | Weight | Weighted | Notes |
|-----------|-------|--------|----------|-------|
| A. Structure | 85 | 30% | 25.5 | |
| B. Triggering | 90 | 20% | 18.0 | |
| C. Style Guide | N/A | — | — | Tool wrapper: N/A |
| D. Workflow | 60 | 20% | 12.0 | |
| E. Sub-Agent Design | N/A | — | — | Does not use sub-agents: N/A |
| F. Conciseness | 75 | 30% | 22.5 | |
| **Total** | | | **78.0** |

## Grade: B

---

## Dimension Details

### A. Structure (85/100)
✅ Frontmatter exists (+15)
✅ name valid: "screenshot-capture" — lowercase, hyphens only (+10)
✅ description present — clear (+15)
✅ description has keywords — Korean + English (+10)
✅ No auxiliary files — no README.md, CHANGELOG.md (+10)
✅ references/ organized — 1-level deep, 1 file (+10)
✅ SKILL.md under 500 lines — 133 lines (+10)
✅ No duplication — browser automation notes in references/ (+5)
✅ Folder name matches name (+15)

**Subtotal: 85/100**

### B. Triggering (90/100)
✅ "What" described — "Capture screenshots from web pages, nodes, or paired devices..." (+20)
✅ "When" in description — "Use when asked to take a screenshot, capture a screen, snap a page, or visually analyze" (+25)
✅ Keywords (Korean) — 스크린샷, 캡처, 화면 캡처, 웹 캡처, 페이지 스크린샷, 노드 화면 (+15)
✅ Keywords (English) — screenshot, capture, screen capture, page capture, visual analysis, device screen (+15)
✅ Not too verbose — description ~35 words (+10)
✅ Not too vague — source types (URL, node, device) specified (+15)

**Subtotal: 90/100**

### C. Style Guide (N/A)
Tool integration skill — no text transformation tasks. N/A.

### D. Workflow (60/100)
⚠️ Phase 0 first — Source Detection table indirectly serves as Phase 0 (+15)
❌ Phase numbering — steps exist but no Phase 0, 1, 2... structure (+0)
⚠️ Context injection — no sub-agents but source detection step serves as context (+10)
⚠️ Validation step — response format exists but no explicit output quality validation step (+8)
✅ Error handling — 4 error response types table (+10)
→ Quick Reference flow exists but no Phase structure

**Subtotal: 60/100**

### E. Sub-Agent Design (N/A)
Does not use sub-agents at all. N/A.

### F. Conciseness (75/100)
✅ SKILL.md body < 500 lines — 133 lines (+40)
✅ SKILL.md body < 300 lines — 133 lines, bonus (+10)
✅ No redundant instructions — minimal duplication (+18)
⚠️ "Agent is smart" — Response Format section somewhat detailed, agent could judge on its own (+10)
✅ References linked — 1 reference file link (+15)

**Subtotal: 75/100**

---

## Improvement Recommendations

1. **[High]** Introduce Phase structure: Phase 0 (source detection + requirements analysis), Phase 1 (capture), Phase 2 (analysis/output) → D score +15 expected
2. **[Medium]** Explicit Phase numbering → D score +5 expected
3. **[Low]** Move Response Format section to references/ → F score +5 expected
