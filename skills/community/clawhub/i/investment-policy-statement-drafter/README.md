# Investment Policy Statement Drafter

**Domain:** Wealth Management · Investment Advisory · Fiduciary Governance
**Platforms:** Claude · Codex

## Purpose

Turns client facts, objectives, and constraints into a DRAFT Investment Policy Statement (IPS) that an adviser and a client can review, edit, and sign — and that creates the documented "reason why" audit trail for every recommendation, satisfying the SEC Investment Advisers Act fiduciary duty (and Reg BI for dual-registrants), ERISA § 404(a) for plans, UPIA for trusts, and UPMIFA for charitable endowments. The output is always a DRAFT for fiduciary and client review — never investment advice, never a guarantee, never an order ticket.

## When to Use

- Onboarding a new individual / joint / trust / IRA / 401(k) / 403(b) / DB-plan / foundation / endowment / family-office client
- Re-papering an existing client where the prior IPS is missing, stale, or non-compliant
- Drafting an ERISA 3(21) or 3(38) IPS for a plan committee
- Drafting an UPMIFA-compliant IPS with a spending-policy formula for an endowment or community foundation
- Drafting an OCIO IPS for a single-family or multi-family office
- Documenting an updated ESG / mission / faith-based overlay on an existing portfolio policy

## What It Does

1. Collects role, client reference (no SSN / full account #), client type, engagement type (discretionary / non-discretionary / 3(21) / 3(38) / OCIO), regulatory frame, and source documents through one-question-at-a-time intake
2. Drafts purpose, parties, governance, review cadence, recordkeeping, and conflicts-of-interest reference
3. Captures return objective (type, gross/net, horizon) and risk objective (ability + willingness + resolution rule) in operational terms (SD band, max drawdown, loss-event tolerance, liquidity coverage)
4. Captures all five constraints — Liquidity, Time horizon, Taxes, Legal/regulatory, Unique circumstances — plus ERISA-specific items (QDIA, 404(c), brokerage window) and UPMIFA-specific items (donor restrictions, spending-policy formula)
5. Drafts strategic asset allocation (strategic / lower / upper / benchmark / role), parametrized rebalancing policy, permitted and prohibited investments, ESG / mission / faith-based overlay, manager-selection criteria (not names), and proxy-voting / class-actions policy
6. Drafts monitoring, performance-benchmark, net-of-fee reporting, watch-list and replacement triggers, and best-execution monitoring
7. Runs a fiduciary-defensibility self-check (objectives, constraints, allocation rows, rebalancing parameters, ESG match, ERISA items, UPMIFA items, no specific securities, no projections / guarantees, identifier redaction) and maintains a "Reason-Why" audit log
8. Outputs a complete DRAFT IPS with an unsigned adviser-and-client sign-off block and a verbatim fiduciary-review banner

## Notes

This skill produces a **DRAFT IPS**, not investment advice. It does not select securities or managers, does not place orders, does not project, promise, or guarantee returns, and does not backdate. The drafting agent is never the adviser of record, never the fiduciary, never the trustee, and never the plan administrator. Direct identifiers (SSN, full account number, full taxpayer ID, DOB, government IDs) must remain redacted in the working draft — the skill uses a non-identifying client code throughout. Final IPS requires compliance review and client / trustee / plan-fiduciary signature.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
