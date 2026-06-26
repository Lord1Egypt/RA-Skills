# mortgage-underwriting-analysis

Analyzes a residential mortgage borrower file against CFPB ATR/QM rules and agency guidelines, computing DTI, LTV, and QM eligibility, and producing a DRAFT underwriting analysis memo.

## Overview

This skill guides a loan officer, underwriter, or processor through six structured phases — loan and property intake, income analysis, liability review, ratio calculations, agency guideline comparison, and memo assembly — producing a DRAFT underwriting analysis memo with an Approve/Refer/Suspend recommendation for licensed-underwriter review.

## Use When

- A loan officer or processor needs a structured pre-underwrite analysis before submitting a file
- An underwriter needs a preliminary analysis memo to work from
- A mortgage team needs to check ATR/QM eligibility and QM safe-harbor rate spread before pricing
- A junior processor is learning to walk through DTI, LTV, and agency guideline analysis systematically

## What It Produces

- A structured DRAFT underwriting analysis memo with:
  - Loan summary (type, purpose, AUS finding, note rate)
  - Income analysis (qualifying income per borrower, documentation types, trend assessment)
  - Liability review (all monthly debts, exclusions documented with rule citations, proposed PITI breakdown)
  - Ratio analysis: front-end DTI, back-end DTI, LTV, CLTV, QM rate spread (APR vs APOR), VA residual income (if applicable)
  - Agency guideline comparison table (pass / fail / exception needed per dimension)
  - Compensating factors
  - Conditions list (items required before clear-to-close)
  - Approve / Refer / Suspend recommendation
  - Underwriter review attestation placeholder
  - DRAFT FLAGS checklist of unresolved items

## Scope and Boundaries

- Covers Conventional (Fannie Mae/Freddie Mac), FHA, VA, USDA, and references Non-QM flag
- Purchase and refinance transactions; 1-4 unit residential properties
- **This is an analysis aid only — not a credit decision, commitment to lend, or regulatory finding.** Requires licensed underwriter review before any action.
- **Never** applies discriminatory factors; all analysis is based on financial and property criteria only
- Does not access live AUS systems, credit bureaus, or pricing engines — uses inputs supplied by the loan officer/processor

## Compatible Platforms

- Claude Code (SKILL.md)
- Codex (SKILL.md)
- OpenClaw (SKILL.md)

## Feedback & Contributions

Found a gap or have a lender-overlay-specific improvement? Open an issue at:
https://github.com/archlab-space/Open-Skill-Hub/issues
