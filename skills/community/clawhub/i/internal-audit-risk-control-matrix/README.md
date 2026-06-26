# Internal Audit Risk-Control Matrix

**Platforms:** Claude · Openclaw · Codex
**Domain:** Internal Audit

## Purpose

Turns an audit engagement's objective, scope, and process documentation into a structured, IIA-aligned Risk-Control Matrix (RCM) ready for fieldwork. Walks the auditor through engagement scoping, process decomposition, risk identification, inherent risk rating, key-control mapping, and Test of Design / Test of Operating Effectiveness planning, and produces a DRAFT RCM, Top-10 risk list, control-gap list, and audit-program outline for licensed internal auditor and Chief Audit Executive (CAE) review.

## When to Use

- Annual or rotational audit-plan engagement kickoff (operational, financial, IT, or compliance audit)
- SOX 404 process / key-control documentation refresh
- Pre-acquisition or post-merger control integration assessment
- First-time audit of a process where no prior RCM exists
- Refreshing an existing RCM after a process redesign, system migration, or regulatory change
- Preparing for an external auditor walkthrough or PCAOB / regulator inspection
- Co-sourced or outsourced internal-audit engagements where deliverables must follow IIA Standards

## What It Does

**Phase 1: Engagement Scoping**
1. Collects audit objective, engagement type, in-scope entity / business unit, regulatory overlay, risk appetite tier, and prior-audit history
2. Confirms reporting line (Audit Committee, CAE, external auditor) and target fieldwork window

**Phase 2: Process Decomposition**
3. Breaks the in-scope process into subprocesses and significant transaction classes (initiation, authorization, recording, custody, reconciliation, reporting)
4. Tags each subprocess to its COSO 2013 component and the relevant assertion(s) — Existence / Occurrence, Completeness, Accuracy, Cutoff, Valuation, Rights & Obligations, Presentation

**Phase 3: Risk Identification & Rating**
5. Lists what-could-go-wrong risk statements per subprocess (not vague themes)
6. Scores inherent Likelihood (1–5) and Impact (1–5) with a stated rationale and assigns an Inherent Risk Tier (Low / Moderate / High / Critical)

**Phase 4: Control Mapping**
7. Maps each risk to one or more key controls with attributes — Preventive vs Detective, Manual vs Automated, Frequency, Control Owner, Evidence Source, IT-Dependency (ITGC reliance)
8. Flags risks with no mapped key control as **Design Gaps**

**Phase 5: Test Plan & Output**
9. Drafts a Test of Design (ToD) step and a Test of Operating Effectiveness (ToE) step per key control, with sample-size guidance tied to control frequency, attribute test definition, pass / fail criteria, and required evidence
10. Produces a DRAFT RCM, Top-10 risk summary, design-gap list, and audit-program outline — always labeled **"DRAFT — INTERNAL AUDITOR / CAE REVIEW REQUIRED"**

## Output

A complete RCM workpaper with engagement metadata, RCM rows (Subprocess → Risk → Inherent L × I → Risk Tier → Key Control(s) → Control Attributes → ToD → ToE → Residual Risk → Gap Flag), Top-10 risks, control-gap list, audit-program outline, open questions, and a mandatory review banner.

## Notes

This skill is for **drafting** an RCM. It does not perform fieldwork, does not collect or validate evidence, does not opine on the operating effectiveness of any control, and does not issue an audit opinion. The output is a working draft to be reviewed, edited, and approved by a licensed internal auditor and the Chief Audit Executive (or equivalent) before any test work begins. Confidential entity data shared during the session is not used in examples, tool calls, or external searches.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
