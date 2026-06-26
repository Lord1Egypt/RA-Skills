# GovCon Proposal Response Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** Government Contracting
**Skill:** `govcon-proposal-response`

## Purpose

A federal proposal writing assistant for capture managers, proposal writers, BD leads, and contracts professionals at U.S. federal contractors. Converts solicitation requirements and company capabilities into a compliant, organized proposal draft — ready for proposal-manager review before government submission.

## When to Use

- When responding to a federal RFP, RFQ, IDIQ task order, BAA, SBIR, or STTR solicitation
- When you need to build a compliance matrix from Sections L and M
- When drafting a technical approach section aligned to Section M evaluation factors
- When writing past performance narratives for a competitive proposal
- When drafting management, staffing, or transition plan sections
- When you need a final compliance check before submission

## What It Does

**Phase 1: Solicitation Intake**
1. Collects agency, solicitation number, type, due date, security classification, and set-aside status
2. Builds a compliance matrix from Sections L and M; marks each requirement Compliant / Partially Addressed / MISSING

**Phase 2: Company Context**
3. Collects company profile: UEI/CAGE (user-provided — never fabricated), certifications, teaming partners, key personnel, differentiators, and past performance references

**Phase 3: Draft Proposal Sections**
4. Executive summary with win themes tied to Section M factors
5. Technical approach structured around evaluation criteria
6. Past performance section with one narrative per reference (all data user-provided)
7. Management and staffing section including org chart placeholder, key personnel bios, and transition plan

**Phase 4: Compliance Review and Assembly**
8. Final compliance check against the matrix; surfaces all MISSING and ACTION REQUIRED items
9. Assembles a DRAFT proposal package with ACTION REQUIRED list, OPEN ITEMS checklist, and Proposal Manager Review Block

## Safety Boundaries

- Never fabricates UEI numbers, CAGE codes, DUNS numbers, contract numbers, dollar values, CPARS ratings, or POC names — uses [TBD] placeholders for all missing data
- All pricing and cost data labeled DRAFT — ESTIMATE; requires cost/pricing team review
- Compliance matrix is mandatory before drafting begins
- Includes ITAR/EAR reminder for defense-article procurements
- Recommends attorney review for large competitive awards and IP/data rights clauses
- All output is a DRAFT requiring proposal-manager and contracts-team review before submission

## Notes

This skill covers unclassified proposal drafting. If the solicitation is CUI, Secret, or above, users must handle all draft content through appropriate classified systems. This skill does not constitute legal advice and does not substitute for licensed contracts counsel review before any government submission.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
