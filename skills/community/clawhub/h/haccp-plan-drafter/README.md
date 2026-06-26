# HACCP Plan Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Food Safety — HACCP / FSMA Preventive Controls

## Purpose

A drafting partner for Preventive Controls Qualified Individuals (PCQIs), HACCP coordinators, and food-safety / quality managers. Turns a product description, process flow, and hazard inventory into a DRAFT written HACCP plan or FSMA Preventive Controls food-safety plan organized around the Codex / NACMCF 7 principles, with hazard-analysis matrix, CCP / PC determination via decision tree, critical limits, monitoring, corrective actions, verification, and recordkeeping log.

## When to Use

- Drafting a new HACCP plan or FSMA Preventive Controls food-safety plan for an FDA-regulated human-food facility (21 CFR Part 117), USDA FSIS meat / poultry / egg facility (9 CFR Part 417), FDA seafood (21 CFR Part 123), juice (21 CFR Part 120), or Codex-aligned export operation
- Performing the 3-year reanalysis required under FSMA, or a triggered reanalysis after a significant process / equipment / ingredient / supplier change
- Standardizing the hazard-analysis matrix and CCP / PC determination across multiple products or production lines
- Preparing the documentation pack ahead of an SQF, BRCGS, or FSSC 22000 third-party audit
- Onboarding a co-manufactured product line and aligning supplier-program and customer-specification controls

## What It Does

**Phase 1: Intake**
1. Captures regulatory framework, facility size category, and audit scheme
2. Captures product description, intended consumer, distribution / storage, shelf life, and label safety statements
3. Captures process flow with confirmed parameters and prerequisite-program coverage

**Phase 2: 7-principle workflow**
4. Principle 1 — hazard analysis across biological, chemical, physical, and radiological hazards with severity / likelihood / foreseeability / citation
5. Principle 2 — CCP / PC determination via the Codex decision tree, classified as Process PC, Allergen PC, Sanitation PC, Supply-chain PC, Recall plan, or CCP
6. Principle 3 — critical limits with validation references and instruments
7. Principle 4 — monitoring procedures (what / how / frequency / role / record)
8. Principle 5 — corrective actions covering product disposition, cause investigation, corrective action, and prevention of recurrence
9. Principle 6 — verification activities and reanalysis triggers
10. Principle 7 — recordkeeping with retention

**Phase 3: Assumption summary and drafting**
11. Restates every fact as Confirmed / Assumed / Unknown
12. Drafts the DRAFT plan in the canonical output format
13. Runs the self-check rubric

## Output

A DRAFT plan with:

- Product description and process flow
- Prerequisite-program reference list
- Hazard-analysis matrix with citations
- CCP / PC determination table with decision-tree answers
- Critical-limits table with validation references
- Monitoring, corrective-action, and verification tables
- Recordkeeping table with retention
- Recall-plan cross-reference
- Evidence matrix
- Unresolved-questions list

## Safety

This skill drafts a plan, **not** a signed or approved one. Every output is labeled **DRAFT — PCQI / HACCP TEAM MUST REVIEW AND SIGN**. Critical limits, monitoring frequencies, and process parameters are never invented; unvalidated values are flagged. Sanitation, allergen, and supply-chain controls are never silently elevated to CCPs without the decision tree. The skill never opines on FDA registration, USDA grant of inspection, or third-party-audit certification status. All proprietary recipes and supplier data are treated as confidential and are never written to external services.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
