# Skill Audit: changelog

**Version**: skill-audit v1.0
**Date**: 2026-05-21
**Target**: /home/node/.openclaw/workspace/skills/changelog/SKILL.md
**Type**: Documentation / Format Conversion
**N/A Dimensions**: E (Sub-Agent Design)
**Redistributed Weights**: A:24%, B:18%, C:24%, D:18%, F:16%

## Score: 85/100 (B)

| Dimension | Score | Weight | Weighted | Notes |
|-----------|-------|--------|----------|-------|
| A. Structure | 85 | 24% | 20.4 | |
| B. Triggering | 90 | 18% | 16.2 | |
| C. Style Guide | 85 | 24% | 20.4 | |
| D. Workflow | 85 | 18% | 15.3 | |
| E. Sub-Agent Design | N/A | — | — | Does not use sub-agents: N/A |
| F. Conciseness | 80 | 16% | 12.8 | |
| **Total** | | | **85.1** |

## Grade: B

---

## Dimension Details

### A. Structure (85/100)
✅ Frontmatter exists (+15)
✅ name valid: "changelog" — lowercase, hyphens only (+10)
✅ description present — clear (+15)
✅ description has keywords — Korean + English (+10)
✅ No auxiliary files — no README.md, CHANGELOG.md (+10)
✅ references/ organized — 1-level deep, 1 file (+10)
✅ SKILL.md under 500 lines — 142 lines (+10)
✅ No duplication — conventional commits spec in references/ (+5)
✅ Folder name matches name (+15)

**Subtotal: 85/100**

### B. Triggering (90/100)
✅ "What" described — "Generate CHANGELOG.md from git commit history" (+20)
✅ "When" in description — "Use when asked to generate a changelog, create release notes, summarize commits, or document what changed" (+25)
✅ Keywords (Korean) — 체인지로그, 변경 로그, 릴리즈 노트, 커밋 요약, 버전 변경, 변경 사항 (+15)
✅ Keywords (English) — changelog, release notes, commit summary, version history, what changed (+15)
✅ Not too verbose — description ~35 words (+10)
✅ Not too vague — specific with "git commit history" and "conventional commits" (+15)

**Subtotal: 90/100**

### C. Style Guide (85/100)
✅ Preservation criteria — "preserve commit messages verbatim as much as possible", "quote Breaking Changes verbatim", "attach commit hashes" (+25)
✅ Compression criteria — "group similar commits in same scope", "chore/ci/style can be compressed", "exclude merge commits" (+20)
✅ Task essence defined — indirect, implicitly defined through "conventional commits parsing" and "category grouping" (+12)
⚠️ Style rules explicit — references Keep a Changelog format, emoji option exists but style rules are thin (+10)
⚠️ Anti-patterns — only "exclude merge commits" level (+5)
→ Practical and concrete preservation/compression criteria

**Subtotal: 85/100**

### D. Workflow (85/100)
✅ Phase 0 first — "Repo Analysis" git log collection, scope determination, version inference (+30)
✅ Phase numbering — Phase 0, 1, 2, 3, 4 (+15)
⚠️ Context injection — Phase 0→1→2 sequential flow is clear but no explicit "inject Phase 0 results" wording (+18)
✅ Validation step — Phase 3 has version bump validation, Phase 4 has output format validation (+20)
✅ Error handling — 4 error response types table (+10)

**Subtotal: 85/100**

### E. Sub-Agent Design (N/A)
Does not use sub-agents at all. N/A.

### F. Conciseness (80/100)
✅ SKILL.md body < 500 lines — 142 lines (+40)
✅ SKILL.md body < 300 lines — 142 lines, bonus (+10)
✅ No redundant instructions — minimal duplication (+15)
⚠️ "Agent is smart" — Recognized Types table contains info the agent might know but useful as a guide (+12)
⚠️ References linked — 1 reference file link (+10)

**Subtotal: 80/100**

---

## Improvement Recommendations

1. **[Low]** Add task essence definition: "A changelog is the task of restructuring commit history into consumer-friendly documentation" → C score +8 expected
2. **[Low]** Add anti-patterns: "don't merge feat + fix into one entry", "no arbitrary category reclassification" etc. → C score +5 expected
