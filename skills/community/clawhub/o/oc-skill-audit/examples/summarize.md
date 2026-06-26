# Skill Audit: summarize

**Version**: skill-audit v1.0
**Date**: 2026-05-21
**Target**: /home/node/.openclaw/workspace/skills/summarize/SKILL.md
**Type**: Sub-agent Pipeline
**N/A Dimensions**: None (all dimensions evaluated)

## Score: 88/100 (B)

| Dimension | Score | Weight | Weighted | Notes |
|-----------|-------|--------|----------|-------|
| A. Structure | 90 | 20% | 18.0 | |
| B. Triggering | 95 | 15% | 14.3 | |
| C. Style Guide | 95 | 20% | 19.0 | |
| D. Workflow | 90 | 15% | 13.5 | |
| E. Sub-Agent Design | 72 | 15% | 10.8 | |
| F. Conciseness | 90 | 15% | 13.5 | |
| **Total** | | | **87.0** |

## Grade: B

---

## Dimension Details

### A. Structure (90/100)
✅ Frontmatter exists (+15)
✅ name valid: "summarize" — lowercase, hyphens only (+10)
✅ description present — clear, comprehensive (+15)
✅ description has keywords — Korean + English keywords (+10)
✅ No auxiliary files — no README.md, CHANGELOG.md (+10)
✅ references/ organized — 1-level deep, 3 files (+10)
✅ SKILL.md under 500 lines — 169 lines (+10)
✅ No duplication — parameter mapping and templates in references/ (+5)
✅ Folder name matches name — summarize/SKILL.md (+15)

**Subtotal: 90/100**

### B. Triggering (95/100)
✅ "What" described — "Summarize any content..." clear (+20)
✅ "When" in description — "Use when asked to summarize, abstract, digest, condense, shorten, or give a TL;DR" (+25)
✅ Keywords (Korean) — 요약, 짧게 요약, 상세 요약, TL;DR, 챕터 요약, 이모지 요약, 200자, 1000자, 전부 요약, 누락 없이 (+15)
✅ Keywords (English) — summarize, summary, digest, condense, abstract, TLDR, brief (+15)
✅ Not too verbose — description ~50 words, concise (+10)
✅ Not too vague — specific content types listed (+15)
→ Small bonus: diverse keywords for broad trigger coverage

**Subtotal: 95/100**

### C. Style Guide (95/100)
✅ Preservation criteria — core arguments, specific examples, figures and data, quotes, metaphors and analogies specified (+30)
✅ Compression criteria — repeated arguments, supplementary explanations, example lists, intro/conclusion duplication specified (+25)
✅ Task essence defined — "summarization is information restructuring" clear (+20)
✅ Style rules explicit — 7 style-specific table + language-specific rules (+15)
✅ Anti-patterns — "no simple concatenation" etc. specified in Phase 4 (+10)
→ Excellent style guide

**Subtotal: 95/100**

### D. Workflow (90/100)
✅ Phase 0 first — "Input Analysis (★)" marker present (+30)
✅ Phase numbering — Phase 0–5 clear (+15)
✅ Context injection described — "inject Phase 0 results into prompts" (+25)
✅ Validation step — Phase 4 has length/style/language validation (+20)
✅ Error handling — context overflow, rate limit, length over/under, quality degradation responses (+10)

**Subtotal: 90/100**

### E. Sub-Agent Design (72/100)
✅ Prompt template exists — references/subagent-templates.md (+20)
✅ `[ ]` placeholders — "fill template `[ ]` blanks in Phase 0" (+20)
⚠️ Context fields defined — full context, chunk position, preservation list mentioned but detailed context field definitions delegated to references/ (+15)
⚠️ Style rules in template — "see references/subagent-templates.md" but no 3-4 line summary in SKILL.md (+8)
✅ Merge ≠ concatenate — "no simple concatenation — restructure according to Phase 0 topic flow" (+15)
⚠️ Sequential pipeline — parallel (max 2) only mentioned, sequential pipeline not explicitly stated (+5)
→ Template content only in references/ with no core summary in SKILL.md

**Subtotal: 72/100**

### F. Conciseness (90/100)
✅ SKILL.md body < 500 lines — 169 lines (+40)
✅ SKILL.md body < 300 lines — 169 lines, bonus (+10)
✅ No redundant instructions — minimal duplication (+18)
✅ "Agent is smart" — many conversion tables but these are reference materials the agent cannot compute, so justified (+12)
✅ References linked — "See references/parameter-mapping.md", "참조" etc. (+15)

**Subtotal: 90/100**

---

## Improvement Recommendations

1. **[Medium]** Add 3-4 line core style instruction summary from sub-agent template to SKILL.md → E score +7 expected
2. **[Medium]** Explicitly define context fields in SKILL.md (full context, chunk position, preservation list) → E score +5 expected
3. **[Low]** Specify sequential pipeline processing conditions → E score +5 expected
