# Inline Content → References Pattern

The highest-impact fix pattern in the skill library. Moving inline code/structure blocks to `references/` files consistently improves D3 by 1-2 points, D4 by 1 point, and D8 by 1 point.

## What to Move

Anything that's reference material an agent would consult *while doing the work*:

| Inline Content Type | Target Reference File |
|---|---|
| Storage layout tree diagrams | `references/storage-layout.md` |
| OKR YAML definitions | `references/okrs.md` |
| Decision model invariants/rules | `references/decision-invariants.md` |
| Function/command definitions with full signatures | `references/functions.md` |
| CLI surface examples with multiple commands | `references/cli-reference.md` |
| Step-by-step setup procedures (npm install, OAuth, pip install) | `references/initialization.md` |
| Self-update procedures with gh api calls | `references/self-update.md` |
| Data schemas (JSON examples of entities, plans, etc.) | `references/schemas.md` |
| Capabilities tables, filter lists, presentation rules | `references/<feature>-reference.md` |
| Any fenced code block over 15 lines that isn't a script | Split into appropriate ref file |

## What NOT to Move

- Actual prose instructions ("When to Use", "When NOT to Use", "Responsibility boundary", "Gotchas", "Invariants" as prose)
- The "Why" explanations that guide agent decision-making
- Edge case handling and pitfalls (these are instruction, not reference)

## How to Move

1. Create the reference file under `references/` with a descriptive name
2. Replace the inline content in SKILL.md with a one-line pointer: "See `references/<filename>.md` for <what>."
3. Add an entry to the support file map with conditional "When to read" language
4. Verify: YAML still parses, code ratio dropped, no broken references

## Concrete Results from May 2026 Sessions

| Skill | Lines Before | Lines After | Code Ratio Before | Code Ratio After | Score Gain |
|-------|-------------|-------------|-------------------|------------------|------------|
| ocas-dispatch | 361 | 236 | 18.2% | 0% | +6 (42→48) |
| ocas-bower | 280 | 270 | 15.7% | 16.2% | +4 (43→47) |
| ocas-voyage | 370 | 218 | 32.4% | 0.9% | +15 (35→50) |
| ocas-reach | 248 | 234 | 14.1% | 11.5% | +5 (41→46) |

Average impact: +7.5 points per skill, with the biggest gains on skills over 300 lines with code ratio >15%.

## Quick Check Before Scoring D3

Count the lines of non-prose content (code blocks, tree diagrams, YAML, JSON, tables) in the SKILL.md body:
- Under 10 lines: D3 = 4 or 5
- 10-30 lines: D3 = 3 (could be moved to refs)
- Over 30 lines: D3 = 2 (definitely should be moved to refs)

If D3 <= 3 due to inline structure, the fix is clear: move it to references/ before finalizing the score.