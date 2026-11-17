# Tool Integration Pattern — Impeccable + 10xEng:audit

Concrete example from 2026-06-22: evaluating the Impeccable design quality tool and integrating it into the OCAS 10xEng skill ecosystem.

## What Happened

User shared `github.com/pbakaus/impeccable` and said "this looks like it might be a good addition to 10xeng:audit."

## Evaluation

1. **Read the tool**: Impeccable is a design language for AI coding agents — 23 commands, 44 deterministic detector rules, 5 dimensions (accessibility, performance, theming, responsive, anti-patterns), P0-P3 severity.

2. **Map against existing skills**:
   - `ocas-10xeng-audit` = code complexity (dead code, stdlib, yagni, shrink)
   - Impeccable = design quality (a11y, contrast, typography, responsive, anti-patterns)
   - **Relationship**: Complementary. Different dimensions, same repos.

3. **Decision**: Integration via delegation, not a new standalone skill.

## What Was Done

1. Installed Impeccable files into `skills/software-development/impeccable/`
2. Added "Frontend Audit Mode" section to `ocas-10xeng-audit` SKILL.md
3. Created `references/frontend-audit-mode.md` with the full procedure
4. Added P0-P3 severity scoring to both `ocas-10xeng-audit` and `ocas-10xeng-review` (aligned with Impeccable's definitions)
5. Updated `ocas-10xeng` root skill with a "For frontend repos" workflow section
6. Updated `ocas-10xeng-audit` Boundaries to reference Impeccable for design quality

## Key Principles Applied

- **Delegation over duplication**: 10xEng:audit owns the audit workflow; Impeccable owns design quality detection. The skill delegates rather than reimplementing.
- **Severity alignment**: Adopted Impeccable's P0-P3 definitions rather than inventing a parallel system.
- **Combined output format**: `design: [P1] ...` prefix distinguishes Impeccable findings from complexity findings (`stdlib:`, `delete:`, etc.)
- **Reference file for detail**: The full Impeccable procedure (5 dimensions, scoring rubric, CLI reference) lives in `references/frontend-audit-mode.md`, not inline in the SKILL.md.

## What Was NOT Done

- Did NOT create a new "impeccable-integration" skill (too narrow)
- Did NOT copy Impeccable's 44 detector rules into 10xEng (the rules live in Impeccable; 10xEng just invokes the CLI)
- Did NOT make Impeccable a hard dependency — it's invoked via `npx impeccable detect` when frontend files are present