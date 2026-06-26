# Loss Reserving Triangle Memo

**Domain:** Actuarial · P&C Loss Reserving · Statement of Actuarial Opinion Support
**Platforms:** Claude · Codex

## Purpose

Drives a CAS-aligned reserving workflow that turns paid- and incurred-loss triangles, exposure data, and prior-period selections into a DRAFT reserving memo. The memo documents per-segment method selection across paid LDF, incurred LDF, Bornhuetter-Ferguson, Cape Cod, and expected-loss-ratio ultimates, runs diagnostics, reconciles indicated vs selected ultimates and IBNR, captures tail-factor and trend judgments, and exposes a sensitivity table — built so a reviewing actuary, Appointed Actuary, or regulator can follow every number to its source. The output is always a DRAFT for actuarial peer review — never a signed Statement of Actuarial Opinion.

## When to Use

- Quarterly or annual P&C reserve review for a personal-lines, commercial-lines, specialty, or reinsurance book
- Producing the work-paper memo that supports the Appointed Actuary's Statement of Actuarial Opinion (SAO) and the Actuarial Opinion Summary
- A prior-year reserve roll-forward or actual-vs-expected (A-vs-E) analysis where ultimates and IBNR must be re-selected
- A new accident-year addition or a re-segmentation of an existing book
- A reasonableness review of a third-party (TPA, captive, or acquired-book) reserve indication
- Loss-portfolio-transfer (LPT) or adverse-development-cover (ADC) reserve diligence

## What It Does

1. Collects role, engagement, line of business, segmentation, evaluation date, currency, reinsurance basis (gross / ceded / net), valuation purpose (statutory / GAAP / IFRS 17 / management / SAO support), and data inventory through one-question-at-a-time intake
2. Reviews triangle data quality (paid loss, case-incurred loss, reported claim counts, closed claim counts, exposures, ALAE basis) and flags structural breaks (mix change, new state / program, claims-handling change, large-loss threshold change)
3. Develops age-to-age factors with an explicit averaging policy (simple, volume-weighted, latest-N, geometric, excluding selected diagonals or cells) and tail-factor selection with a documented basis (curve fit, industry benchmark, judgment)
4. Builds the standard method family per segment: paid LDF, incurred LDF, paid Bornhuetter-Ferguson, incurred Bornhuetter-Ferguson, Cape Cod, expected loss ratio, and (if data permits) frequency-severity
5. Runs diagnostics — paid-to-incurred ratios by AY × maturity, calendar-year diagonals for trend, age-to-age variability and outlier flagging, ultimate-loss-ratio progression by AY, IBNR-to-case ratio reasonableness, A-vs-E for the prior selection
6. Reconciles indicated to selected ultimates per AY and per segment, documents weights between methods, records every override with rationale, and rolls the selections up to IBNR (pure IBNR + IBNER), reported reserves, and case reserves
7. Captures inflation / loss-trend, frequency / severity, social-inflation, large-loss, and reinsurance-cession judgments with named source
8. Produces a sensitivity table that shows the impact on net reserves of changes to tail factor, paid-vs-incurred weighting, ELR, and discount rate (when applicable)
9. Runs an ASOP-defensibility self-check (ASOP 36 — reserve review; ASOP 41 — communications; ASOP 43 — reserves; ASOP 23 — data quality; ASOP 25 — credibility; ASOP 13 — trending procedures) and maintains a chronological judgment log
10. Outputs a complete DRAFT memo with an unsigned reviewing-actuary sign-off block and a verbatim "draft for actuarial peer review" banner

## Notes

This skill produces a **DRAFT reserving memo** for actuarial peer review and Appointed Actuary use. It is not a Statement of Actuarial Opinion (SAO), not a regulatory filing, and not investment, accounting, or legal advice. The drafting agent is never the Appointed Actuary, never the signer of the SAO, and never the actuary of record. Specific company data — claim numbers, claimant identifiers, named insureds, social-security or tax IDs — must remain redacted in the working memo; the skill works from segment codes and AY × maturity grids only. Final memo and reserve indications require a credentialed actuary's review and signature; the SAO is a separate document governed by ASOP 36 and the NAIC SAO instructions.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
