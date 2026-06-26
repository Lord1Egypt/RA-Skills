# Localization Readiness Audit

**Platforms:** Claude · Openclaw · Codex
**Domain:** Localization — Product / Engineering Internationalization Readiness

## Purpose

A pre-launch i18n / l10n readiness auditor for product managers, engineering leads, globalization managers, localization PMs, and DevRel teams preparing a single product (web app, mobile app, desktop app, API, marketing site, or game) for one or more new locales. Turns a structured intake (target locales, tech stack, current i18n approach, content sources, launch deadline) into a DRAFT audit with severity-rated findings across eight dimensions, a Top-10 blockers list, a Ship / Fix-then-ship / Hold verdict, and an owner-tagged remediation plan — produced **before** engaging a translation vendor or committing to a launch date.

## When to Use

- Standing up a new locale on an existing product for the first time
- Adding the second locale after an English-only product was "internationalized" only as far as the first locale needed
- Pre-vendor audit before sending strings for translation (avoid paying to translate broken keys)
- Post-incident review after a launch failure (broken plurals, mojibake, clipped UI, RTL regression)
- Standardizing the readiness bar across multiple products in a portfolio
- Preparing a globalization roadmap and the engineering effort estimate that goes with it

## What It Does

**Phase 1: Intake**
1. Captures the product surface in scope (and what is explicitly out of scope)
2. Captures target locales (BCP-47 tags) and launch order
3. Captures tech stack: frontend framework(s), backend framework(s), mobile platforms, database(s) and collation, build pipeline, current i18n libraries
4. Captures current i18n approach: hardcoded vs. externalized strings, file format (ICU MessageFormat, gettext .po, XLIFF, JSON, .strings, .resw), translation-management system (TMS), pseudolocalization usage, RTL test coverage
5. Captures content sources beyond UI strings: emails, push notifications, system messages, legal text, marketing content, in-product images with embedded text, video subtitles
6. Captures launch deadline and the team's tolerance for shipping with known gaps
7. Restates every fact with **Confirmed / Assumed / Unknown** tags before auditing

**Phase 2: Audit across 8 dimensions**
8. Walks each of the 8 dimensions (Unicode and encoding; string externalization and message format; plural and gender rules; dates, numbers, currency, units; locale-aware sorting and search; RTL and bidi; UI expansion and layout; content-localization process and legal-regulatory)
9. Records each finding with: dimension, severity (Blocker / Major / Minor / Nit), evidence (file / endpoint / screenshot / config), recommended fix, owner role, effort estimate (S / M / L)

**Phase 3: Verdict and plan**
10. Builds the Top-10 blockers list and the Ship / Fix-then-ship / Hold verdict
11. Builds the prioritized remediation plan with owners and effort
12. Builds the launch-readiness checklist tied to the target locales and the deadline

**Phase 4: Output**
13. Produces the DRAFT audit using the structure in `SKILL.md`
14. Runs the self-check rubric and lists failures back to the team
15. Produces an unresolved-information list (what the team still needs to confirm before the audit is final)

## Output

A DRAFT audit with:

- Cover block (product, target locales, owner, deadline, verdict)
- Scope (in / out)
- Intake summary with assumption tags
- Findings by dimension (with severity, evidence, recommended fix, owner, effort)
- Top-10 blockers
- Ship / Fix-then-ship / Hold verdict with rationale
- Remediation plan (sequenced, owner-tagged, effort-estimated)
- Launch-readiness checklist for each target locale
- Unresolved-information list

## Safety

This skill produces an **audit recommendation**, not a deployment decision and not legal advice. Every output is labeled **DRAFT — PRODUCT / ENGINEERING / GLOBALIZATION LEAD MUST REVIEW**. The skill never modifies code, configuration, or content; never executes translations; never selects a translation vendor; never makes a launch decision; never opines on whether a localized product meets a target market's legal or regulatory requirements (GDPR, CCPA, accessibility statutes, age-rating, content-moderation, payments licensing). Country and language compliance items are flagged for licensed-counsel and market-specific review. Source code, content, customer data, and unreleased product information are treated as confidential and are never written to external services.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
