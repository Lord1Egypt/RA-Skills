# Phase 3: Spec Compliance Review

## Current Phase

**[Phase 3] Spec Compliance Review**

## Objective

**Review the implementation** against the targeted RFC (both the formal spec and the implementation guide) using **platonic-coding REVIEW mode**, and produce a compliance report.

## Inputs

- **Code**: Implemented in Phase 2 (relevant directories/modules).
- **RFC spec(s)**: From Phase 1 (filename `RFC-NNN-<name>.md`, e.g. `docs/specs/RFC-001-world-view.md`).
- **Implementation guide(s)**: From Phase 2, using naming convention `IG-<number>-semantic-short-desc.md` (e.g., `docs/impl/IG-001-user-authentication.md`).

## Process

### Step 1: Call REVIEW Mode

- **Use platonic-coding REVIEW mode** to review:
  - The **code implementation** from Phase 2.
  - The **targeted RFC spec** (e.g. `docs/specs/`).
  - The **targeted impl guide** (e.g. `docs/impl/`).
- Read `references/REVIEW/review-spec-compliance.md` (or the skill's review procedure) and invoke the operation accordingly.
- Scope the review to the RFC and impl guide used in this workflow so the report is focused.

### Step 2: Produce Report

- REVIEW mode produces a review/compliance report (default: report-only, no code modification).
- Summarize for the user: what matches, what is missing, what is inconsistent.

## Output

- **Review and compliance report** (from REVIEW mode).
- Clear list of findings and recommended actions; ask the user before making any code changes.

## Handoff to FINISHED

- Once the review is complete, mark the workflow as **FINISHED** and provide a short summary and any follow-up recommendations.
