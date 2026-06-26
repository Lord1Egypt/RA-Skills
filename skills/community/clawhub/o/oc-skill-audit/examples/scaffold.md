# Skill Audit: scaffold

**Version**: skill-audit v1.0
**Date**: 2026-05-21
**Target**: /home/node/.openclaw/workspace/skills/scaffold/SKILL.md
**Type**: Code Generation / Modification
**N/A Dimensions**: E (Sub-Agent Design)
**Redistributed Weights**: A:24%, B:18%, C:24%, D:18%, F:16%

## Score: 81/100 (B)

| Dimension | Score | Weight | Weighted | Notes |
|-----------|-------|--------|----------|-------|
| A. Structure | 85 | 24% | 20.4 | |
| B. Triggering | 90 | 18% | 16.2 | |
| C. Style Guide | 70 | 24% | 16.8 | Partially applies |
| D. Workflow | 80 | 18% | 14.4 | |
| E. Sub-Agent Design | N/A | — | — | Does not use sub-agents: N/A |
| F. Conciseness | 82 | 16% | 13.1 | |
| **Total** | | | **80.9** |

## Grade: B

---

## Dimension Details

### A. Structure (85/100)
✅ Frontmatter exists (+15)
✅ name valid: "scaffold" — lowercase, hyphens only (+10)
✅ description present — clear (+15)
✅ description has keywords — Korean + English (+10)
✅ No auxiliary files — no README.md, CHANGELOG.md (+10)
✅ references/ organized — 1-level deep, 1 file (+10)
✅ SKILL.md under 500 lines — 166 lines (+10)
✅ No duplication — framework templates separated into references/ (+5)
✅ Folder name matches name (+15)

**Subtotal: 85/100**

### B. Triggering (90/100)
✅ "What" described — "Scaffold new projects with best-practice structure, config files, and boilerplate" (+20)
✅ "When" in description — "Use when asked to create a new project, scaffold, initialize, set up, bootstrap, or start a new codebase" (+25)
✅ Keywords (Korean) — 프로젝트 생성, 스캐폴딩, 초기 설정, 프로젝트 구조, 프로젝트 시작, 뼈대 (+15)
✅ Keywords (English) — scaffold, project setup, bootstrap, initialize, new project, create project (+15)
✅ Not too verbose — description ~30 words (+10)
✅ Not too vague — scope specified with "Node.js/TypeScript projects" (+15)

**Subtotal: 90/100**

### C. Style Guide (70/100)
⚠️ Preservation criteria — existing file preservation mentioned but code style preservation criteria weak (+15)
⚠️ Compression criteria — "don't add optional tools not specified by user" but lacking specific examples (+12)
⚠️ Task essence defined — none (only "best-practice" mentioned) (+5)
⚠️ Style rules explicit — only "TypeScript (default), pnpm (default)" level (+8)
❌ Anti-patterns — none (+0)
→ Partially applies but preservation/compression criteria not concretized for code generation

**Subtotal: 70/100**

### D. Workflow (80/100)
✅ Phase 0 first — "Requirements Analysis" user request understanding (+30)
✅ Phase numbering — Phase 0, 1, 2, 3 (+15)
⚠️ Context injection — no sub-agents but Phase 0→1 parameter passing is implicit (+15)
✅ Validation step — Phase 3 "type check passes then complete" (+20)
✅ Error handling — 4 error response types table (+10)

**Subtotal: 80/100**

### E. Sub-Agent Design (N/A)
Does not use sub-agents at all. N/A.

### F. Conciseness (82/100)
✅ SKILL.md body < 500 lines — 166 lines (+40)
✅ SKILL.md body < 300 lines — 166 lines, bonus (+10)
✅ No redundant instructions — minimal duplication (+15)
⚠️ "Agent is smart" — template (JSON) fully included but justified for generation; some parts agent could generate (+10)
✅ References linked — 1 reference file link (+15)

**Subtotal: 82/100**

---

## Improvement Recommendations

1. **[Medium]** Strengthen style guide: specify code formatting criteria (Prettier config contents), naming conventions, file structure principles → C score +15 expected
2. **[Low]** Add anti-patterns: "monorepo requires a separate skill", "no git init (user does it)" etc. → C score +10 expected
3. **[Low]** Move JSON templates to references/ → F score +5 expected
