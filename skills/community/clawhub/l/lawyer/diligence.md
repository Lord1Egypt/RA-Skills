# Diligence, Disclosure and Questionnaires

Somebody is about to inspect the company — a buyer, an investor, an enterprise customer's security team, an auditor. All four ask overlapping questions, all four punish inconsistency, and all four are cheap if the answers already exist and expensive if they do not.

**Before answering anything**, read `## Legal Context`, `## Contracts` and `## Matters` in `~/Clawic/data/lawyer/memory.md`, and open the compliance register and any `artifacts/diligence-*.md` the `## Boxes` index names. Answering a questionnaire from memory when a previous answer exists in writing is how two different answers reach the same buyer.

**Contents:** [The Four Requesters](#the-four-requesters) · [The Standing Answer Set](#the-standing-answer-set) · [The Document Set](#the-document-set) · [What Diligence Always Finds](#what-diligence-always-finds) · [Answering Rules](#answering-rules) · [Reps, Warranties And Disclosure](#reps-warranties-and-disclosure) · [Security Questionnaires](#security-questionnaires) · [Running The Data Room](#running-the-data-room) · [Diligence On Someone Else](#diligence-on-someone-else) · [Pre-Diligence Cleanup](#pre-diligence-cleanup)

## The Four Requesters

| Requester | Wants to know | Their leverage |
|---|---|---|
| Acquirer | What liabilities transfer and what the price should be | Price reduction, escrow, indemnity, or walking away |
| Investor | Whether the cap table and the IP are clean enough to fund | Terms, conditions to closing, or passing |
| Enterprise customer | Whether buying from this company creates risk for them | Not signing, or contractual conditions |
| Auditor / certifier | Whether the controls exist and operated | The report the customers ask for |

They ask the same twelve questions in different formats. Build the answers once (below) and reformat.

## The Standing Answer Set

Maintained in `~/Clawic/data/lawyer/artifacts/diligence-answers.md`, updated when the underlying fact changes, never rebuilt per request.

1. Corporate: entities, jurisdictions, ownership, cap table, board composition, good standing (`entity.md`)
2. IP: what is owned, the assignment chain from every founder and contractor, registrations and their status, open-source position (`ip.md`)
3. Contracts: the material contract list with counterparty, value, term, change-of-control and assignment flags (`obligations.md`)
4. Employment: headcount by jurisdiction, classification of contractors, restrictive covenants, open claims (`employment.md`)
5. Privacy: role, regimes, records of processing, DPAs, transfer mechanisms, breach history (`privacy.md`)
6. Security: certifications, architecture summary, access control, encryption, vendor list, incident history
7. Compliance: the register, licences held, regulatory correspondence (`compliance.md`)
8. Litigation and disputes: open, threatened, and closed within the limitation period (`disputes.md`)
9. Finance and tax: filings current, liabilities, related-party transactions (`accountant`)
10. Insurance: policies, limits, claims history
11. Real estate and equipment: leases, guarantees, obligations
12. Change-of-control exposure: every contract that terminates or needs consent on a sale

Item 12 is the one that delays closings, and it is derivable from item 3 in an afternoon if the contract register exists.

## The Document Set

What a buyer or investor will ask for, in the order they usually ask:

- Certificate/articles of incorporation and all amendments; bylaws or operating agreement
- Stock ledger / register of members, all issuances, option plan and every grant, SAFEs and notes
- Board and shareholder minutes and written consents, complete and signed
- Founder agreements, IP assignments from every founder and early contributor
- Employment agreements, contractor agreements, offer letters, handbook, current headcount by entity
- Material customer and supplier contracts, plus the standard form templates actually used
- IP registrations and prosecution files; open-source inventory
- Privacy documentation: policy versions, records of processing, DPAs, sub-processor list, DPIAs
- Insurance policies and certificates
- Leases and any personal guarantees
- Litigation and regulatory correspondence
- Financial statements, tax returns and filing confirmations

## What Diligence Always Finds

The recurring findings, in rough frequency order. Each is cheap to fix in advance and expensive to fix under a deal timetable.

| Finding | Why it happens | Fix |
|---|---|---|
| IP not assigned from a founder, an early contractor or an agency | Work predates the company or the paperwork was skipped | Confirmatory assignment now, before anyone is asked to sign it under pressure (`ip.md`) |
| Cap table does not reconcile to the signed documents | Grants approved verbally, spreadsheet drift | Reconcile grant by grant to the board consent (`entity.md`) |
| Contractors who are functionally employees | Growth without a hiring process | Reclassify prospectively and take advice on the back period (`employment.md`) |
| Missing board consents for share issuances | Nobody ran the formalities | Ratifying consents, with dates recorded honestly |
| Customer contracts with change-of-control termination or consent | Signed years ago without flagging | List them early; consent-gathering has a long lead time |
| No DPAs with processors handling personal data | Tools adopted without review | Paper them; a missing DPA is a compliance finding for both sides (`privacy.md`) |
| Privacy policy describing a company that does not exist | Copied template | Rewrite from the records of processing |
| Open-source obligations unmet — AGPL or GPL components in a hosted product | No SBOM, no CI gate | Inventory, then remediate or replace (`ip.md`) |
| Unregistered trademark for the main brand, or a conflicting mark in a key market | Filing deferred | File now; disclose the risk |
| Expired insurance or limits below contractual commitments | Renewal missed | Renew and reconcile to contract requirements |
| Undocumented related-party transactions | Founder loans, family suppliers | Document and disclose (`entity.md`) |
| Employee claims not disclosed internally | The complaint went to a manager and stopped there | Ask specifically before the buyer does |

## Answering Rules

- **Answer what is true today**, with a roadmap note where something is planned. An intention stated as a fact becomes a contractual representation and then a misrepresentation claim (SKILL.md Traps).
- **Never answer a question you have not verified.** "We do not store card data" is a sentence that has ended acquisitions when a legacy log turned out to contain it.
- **Consistency across requesters.** The security questionnaire, the privacy policy, the DPA and the customer contract must describe the same company. Buyers and enterprise reviewers compare documents; regulators do too.
- **One owner for the response**, with subject-matter contributors. Parallel answering by three people produces contradictions.
- **Say "not applicable" with the reason**, not just "N/A". The reason is what makes it credible and saves the follow-up.
- **Log every question and answer** as it is given, into `~/Clawic/data/lawyer/artifacts/diligence-answers.md` (security questions into `artifacts/diligence-security.md`), each with its `## Boxes` line. That log becomes the standing answer set for the next requester.

## Reps, Warranties And Disclosure

In an acquisition or an investment, the user gives representations and warranties, and the **disclosure letter or schedule is the shield**: anything fairly disclosed against a warranty cannot be claimed under it. The disclosure exercise is therefore the most valuable legal work in the transaction, and it is the work most often left to the last week.

- Disclose specifically against the numbered warranty; a general dump of documents into a data room is treated as general disclosure and may not qualify as fair disclosure in every system.
- The materiality and knowledge qualifiers matter: "so far as the Sellers are aware" needs a defined awareness standard (which individuals, and after what inquiry).
- Limitations: cap on warranty claims (often a percentage of consideration, with fundamental warranties at 100%), de minimis per claim, an aggregate basket, and time limits (commonly 12-24 months for general warranties, longer for tax and fundamental warranties).
- Warranty and indemnity insurance shifts the risk to an insurer and is common above a deal-size threshold; it changes the negotiation from "how much escrow" to "who pays the premium".
- Specific indemnities cover known issues that diligence found. A known problem is priced, not warranted — expect the buyer to ask for a pound-for-pound indemnity on anything the disclosure letter reveals.
- Anything the user knows and does not disclose is fraud territory, which no cap or time limit protects against. Disclose it.

## Security Questionnaires

The enterprise customer version of diligence, and the one that recurs most often. Efficiency is everything: the same 200 questions arrive in a different spreadsheet every time.

- A current SOC 2 Type II or ISO 27001 report plus a standardised questionnaire response satisfies most reviewers and replaces weeks of bespoke answers. That is the real return on certification (`compliance.md`).
- Keep the canonical answer bank in `~/Clawic/data/lawyer/artifacts/diligence-security.md`, keyed by question intent, not by wording, with its `## Boxes` line. New questionnaires reuse 80% of it.
- Answer honestly about what is not in place, with the compensating control and the plan. Reviewers accept gaps with plans; they escalate discovered inaccuracies.
- Watch what the questionnaire quietly commits to: many contain commitments (notification timelines, sub-processor consent, audit rights, data location) that then get incorporated into the contract by reference. Review them as contract terms, because that is what they become (`clauses.md`).
- Push back on requirements that do not fit the architecture, with an explanation. Agreeing to a control the company cannot operate is a future breach.

## Running The Data Room

- Index by the requester's list, not by internal folder structure. A well-indexed room shortens diligence measurably.
- Access control per user and per folder, with an access log — the log is evidence of what was disclosed and when, which matters for the disclosure letter.
- Redact what must be redacted before upload: personal data of employees and customers, third-party confidential information covered by NDAs with other counterparties, and privileged material. Redaction after the fact does not work.
- **Never upload a document containing a credential.** Executed contracts, runbooks and configuration files routinely carry them, and a data room is the single worst place for one (SKILL.md, secrets).
- Version control: one document, one version, dated. Two versions of the same contract in a data room is a diligence question by itself.
- Keep a complete copy of what was disclosed, exactly as disclosed, at closing, and record where that copy lives as a `file:` pointer in `artifacts/disclosure-<transaction>.md`. If a warranty claim comes later, the question is what was in the room on the day.

## Diligence On Someone Else

The user may be the buyer, or may be onboarding a critical supplier. The compressed version: verify the entity exists and is in good standing in the register; confirm who owns the IP they are selling; check the material contracts for change-of-control and assignment terms; check for litigation in the public record; confirm insurance limits with a certificate, not a statement; confirm that the people who make it work are actually employed and under enforceable terms; and check sanctions and beneficial ownership (`compliance.md`).

For a supplier, the proportionate version is the questionnaire plus a certificate plus the DPA — matched to what the supplier can actually break.

**After any diligence work**, write in the same turn (`memory-template.md`): the standing answer set into `~/Clawic/data/lawyer/artifacts/diligence-answers.md`, the security-questionnaire bank into `artifacts/diligence-security.md`, and the disclosure letter or its outline into `artifacts/disclosure-<transaction>.md` — each with its `## Boxes` line and a read condition naming the requester type. Every gap the exercise revealed becomes a row in `## Matters` with an owner and a date, and every recurring obligation it surfaced goes into `## Due`. If the transaction is tracked as a project, its summary belongs in the shared `~/Clawic/data/projects/<project>.md`, with the documents staying here and referenced by name.
