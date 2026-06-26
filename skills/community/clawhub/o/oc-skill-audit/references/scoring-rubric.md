# Scoring Rubric — Detailed Examples

Concrete examples for scoring each dimension.

---

## A. Structure Examples

### name validation
| name | Score | Reason |
|------|-------|--------|
| `summarize` | ✅10 | lowercase, hyphens |
| `unit-converter` | ✅10 | lowercase, hyphens |
| `Skill_Creator` | ❌0 | uppercase, underscore |
| `my-skill-is-really-long-and-descriptive-of-what-it-does` | ❌0 | >64 chars |
| `123skill` | ❌0 | starts with digit |

### description quality
| description | Score | Reason |
|------------|-------|--------|
| "Summarize any content..." (200 words, what+when+keywords) | ✅15+10 | clear + keywords |
| "Helpful skill." | ❌0 | too vague |
| "Summarize things." | ❌5 | what exists, but no when/keywords |

### auxiliary files
| Files | Score |
|-------|-------|
| SKILL.md + references/ | ✅10 |
| SKILL.md + README.md | ❌0 |
| SKILL.md + CHANGELOG.md + INSTALL.md | ❌0 |

---

## B. Triggering Examples

### "When" placement
| Location | Score | Reason |
|----------|-------|--------|
| description includes "Use when..." | ✅25 | Loaded before body |
| SKILL.md body has "When to Use" section | ❌0 | Body is loaded after triggering |
| Both present | ⚠️15 | Body presence is meaningless for triggering |

### keywords
| description | ko | en | Score |
|------------|----|----|-------|
| "요약, 짧게 요약, 200자, summarize, digest" | ✅ | ✅ | ✅30 |
| "Summarize content into structured markdown" | ❌ | ✅ | ⚠️15 |

---

## C. Style Guide Examples

### good example (summarize)
```markdown
### Preservation Criteria (never discard)
- Core arguments and evidence — convey the author's intent
- Specific examples — concretize abstract claims
- Figures and data — with sources

### Compression Criteria
- Repeated arguments — if the same content appears in multiple places, keep only one
```
→ ✅ preservation(30) + compression(25) + essence(20) = 75+

### bad example (format-only)
```markdown
## Output Format
- Each chapter 3-5 sentences
- Include key takeaways
```
→ ❌ no preservation criteria, no compression criteria = 0

### N/A exemption
If a skill does not use sub-agents at all and is a single-task operation:
- Apply 50% of full Style Guide score (max 50 → N/A adjustment to 70% score)
- Reason: Single-task agents already have their own built-in judgment criteria

---

## D. Workflow Examples

### good example (explicit Phase 0)
```markdown
### Phase 0: Structure Analysis (★ most important)
1. Scan entire text to understand outline/section structure
2. Map topic flow
3. Include this information in sub-agent prompts

### Phase 1: ...
```
→ ✅ Phase 0(30) + numbering(15) + context plan(25) = 70+

### bad example (no Phase 0)
```markdown
## How to Use
1. Extract text from PDF
2. Split into chunks
3. Send to sub-agent
```
→ ❌ No Phase 0 = 0 for context plan, overall low score

---

## E. Sub-Agent Design Examples

### good template with `[ ]`
```markdown
## Context
[Full structure — filled by Phase 0]
[This chunk's position — filled by Phase 0]

## Preserve (this chunk only)
[Preservation list — filled by Phase 0]
```
→ ✅ template(20) + placeholders(20) + context(20) = 60+

### bad template (no context injection)
```markdown
Summarize the following text in 3-5 sentences.

---
[chunk text]
---
```
→ ❌ no placeholders, no context = low score

---

## F. Conciseness Examples

| SKILL.md lines | Score | Notes |
|---------------|-------|-------|
| 120 lines | ✅50 | Under 300, bonus +10 = 50 |
| 280 lines | ✅40 | Under 500 |
| 520 lines | ⚠️20 | Slightly over, recommend split |
| 800 lines | ❌0 | Way over, must split |

### "Agent is smart" violation
```markdown
## How to Read a File
Use the `read` tool to read the contents of a file. The `read` tool takes a
`path` parameter which specifies the file to read...
```
→ ❌ Redundantly explains tool usage the agent already knows → -15

---

## Score Interpretation Guide

### A (90+): Production Ready
The skill is well-designed with high quality across all dimensions. Ready for deployment with only minor improvements.

### B (75–89): Good
Meets most criteria but has room for improvement in 1-2 dimensions.

### C (60–74): Adequate
Basically functional, but quality may degrade if sub-agents are used.
Style Guide or Phase 0 is likely missing.

### D (45–59): Needs Work
Deficient in multiple dimensions. Sub-agent results are likely inconsistent.
Structural improvements needed.

### F (<45): Poor
Basic spec compliance may be problematic. Frontmatter or description needs rewriting.
