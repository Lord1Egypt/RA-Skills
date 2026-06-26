# M&A Diligence Issues List

**Platforms:** Claude · Openclaw · Codex
**Domain:** Corporate Development

## Purpose

Turns raw target-company data room artifacts (contracts, financial statements, cap table excerpts, customer concentration data, IP schedules, employment agreements, litigation summaries, regulatory filings, IT/security questionnaires) into a structured M&A diligence issues list. Each issue is tagged by workstream, severity, source evidence, and recommended action so that the deal team can drive purchase-price adjustments, indemnities, conditions precedent, or a walk-away decision.

## When to Use

- Corporate development associate or director running diligence on a strategic acquisition
- Private equity or growth-equity deal team working a confirmatory diligence sprint
- M&A attorney synthesizing red-flag findings into a legal issues summary
- Investment-banking analyst preparing a sell-side QofE response or a buy-side red flag report
- Integration lead reviewing a target ahead of signing for day-one risks

## What It Does

**Phase 1: Deal Framing**
1. Captures the deal context: target, deal type (asset / stock / merger), thesis, deal size, indicative timeline, materiality threshold, and any known deal-breakers
2. Inventories the data-room artifacts the user can share (or document snippets the user pastes), and confirms what is missing

**Phase 2: Workstream Analysis**
3. Walks each workstream in order — Legal/Corporate, Commercial/Customer, Financial/Accounting, Tax, HR/Employment, IP/Technology, IT/Security, Regulatory/Compliance, ESG/Litigation — and applies a workstream-specific red-flag checklist
4. Logs every finding as an issue with workstream tag, severity (Deal-killer / High / Medium / Low), source evidence quote or document reference, and a recommended action (price adjustment / indemnity / CP / R&W / disclosure schedule update / walk)

**Phase 3: Synthesis**
5. Produces the consolidated issues list, a Top-10 critical-issues summary, an open-questions list for management, and reps & warranties / escrow recommendations
6. Flags every assumption and gap so legal counsel and the deal partner can sign off on the record

## Output

A DRAFT diligence issues package: deal-context header, workstream issues table, Top-10 critical issues, management Q&A, R&W / escrow recommendations, deal-killer banner, and an unresolved-information list. The output is explicitly labeled as a working draft for licensed-counsel and deal-partner review — it is never a substitute for legal advice or a binding diligence opinion.

## Safety Notes

The skill never accesses external data rooms, never calls third-party services, and never fabricates contract clauses, financial numbers, or counterparty identities. Every issue must cite a source document or be marked as an unresolved question. The skill treats target name, deal terms, counterparty names, and financials as confidential and never reuses them in examples. It always recommends licensed-counsel and deal-partner review before any decision and refuses to render a valuation opinion or a binding go/no-go verdict.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.