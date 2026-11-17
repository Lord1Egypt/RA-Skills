# Drafting: Writing the Words

Drafting is where ambiguity is created or killed. Every dispute over a contract is a dispute about a sentence somebody wrote quickly.

**Before drafting**, read `## Positions` in `~/Clawic/data/lawyer/memory.md` for the standing positions to build in, and open any `artifacts/template-*.md` or `artifacts/clause-*.md` the `## Boxes` index names for this document type. Redrafting from memory what already exists in an artifact is how two versions of the user's standard NDA start circulating.

**Contents:** [Document Skeleton](#document-skeleton) · [Defined Terms](#defined-terms) · [The Verbs](#the-verbs) · [Ambiguity Killers](#ambiguity-killers) · [Numbers, Dates And Money](#numbers-dates-and-money) · [Conditions, Obligations And Discretion](#conditions-obligations-and-discretion) · [Structuring Multi-Document Deals](#structuring-multi-document-deals) · [Execution And Signature Blocks](#execution-and-signature-blocks) · [Electronic Signature](#electronic-signature) · [Amendments](#amendments) · [Plain Language](#plain-language) · [Self-Review Pass](#self-review-pass)

## Document Skeleton

Order is conventional and worth keeping, because reviewers scan by position:

1. Title and date
2. Parties — exact registered name, entity form, registration number, registered address
3. Recitals / background — why the parties are here; not operative, but used to construe ambiguity
4. Definitions
5. Operative provisions — what each side does, in the order the deal happens
6. Commercial terms — fees, payment, delivery, acceptance
7. Risk allocation — warranties, liability, indemnity, insurance
8. Term and termination, with survival
9. General / boilerplate — notices, assignment, precedence, entire agreement, governing law
10. Signature blocks
11. Schedules and exhibits

Put anything deal-specific and volatile (pricing, scope, service levels) in a schedule. Then the master agreement stays stable across renewals and only the schedule is renegotiated.

## Defined Terms

- **Define once, in one place**, and use the term consistently. A term defined in the definitions section and re-defined inline in clause 8 creates a conflict the drafter never notices.
- **Capitalise defined terms and nothing else.** If "Services" is capitalised in clause 3 and lowercase in clause 9, a reader is entitled to argue they mean different things.
- **Never define a term you use once.** Inline it. Definitions sections padded with single-use terms hide the three that matter.
- **Do not smuggle obligations into definitions.** "Support Services means the services described in Schedule 2, which the Supplier shall provide 24/7" puts an obligation somewhere nobody looks for one. Definitions describe; the operative clauses oblige.
- **Define by reference to a document only if that document is attached.** "as set out in the Documentation" where Documentation is a URL that changes is an obligation the other side rewrites at will.
- Check every defined term is used, and every capitalised term is defined. Both directions.

## The Verbs

| Word | Means | Use for |
|---|---|---|
| shall / must | Obligation | Duties. Pick one and use it throughout; mixing them invites an argument that they differ |
| will | Future fact, or a softer obligation depending on the system | Statements of what happens, not duties |
| may | Discretion | Rights the party can choose not to exercise |
| is entitled to | Right | Same as may, clearer when the counterparty must not obstruct it |
| shall not / must not | Prohibition | Restrictions |
| is not required to | Absence of obligation | Never write "may not" for this — it is ambiguous between prohibition and permission |

Passive voice hides the obligor: "the Deliverables shall be tested" — by whom? Every obligation names its subject.

## Ambiguity Killers

| Ambiguity | Example | Fix |
|---|---|---|
| "and/or" | "A and/or B" | Say which: "A, B, or both" |
| Serial-comma scope | "consulting, training and support services" — is consulting a service? | Restructure into a list with (a), (b), (c) |
| "including" as a limit | Courts split on whether it is exhaustive | "including without limitation", or list exhaustively and say so |
| "reasonable efforts" vs "best efforts" | Unsettled in most systems, litigated often | Define the standard by example, or state the specific steps required |
| "material" | Everywhere, defined nowhere | Define by threshold: "material means affecting more than 10% of the fees payable in any 12-month period" |
| "promptly", "as soon as practicable" | No date | A number of days, and say business or calendar |
| "from" a date | Inclusive or exclusive | "within 30 days after (but excluding) the Effective Date" |
| Undefined "affiliate" | Different in every system | Define by control threshold, and say whether it is limited to current affiliates |
| Two clauses both governing the same thing | Discovered in dispute | Cross-reference explicitly: "subject to clause 11.3" |
| Dangling "such" and "the same" | "such notice", where two notices are in play | Repeat the noun |

## Numbers, Dates And Money

- Every amount carries its currency in the text, not just a symbol: "USD 120,000". `$` is ambiguous across at least a dozen currencies, and a contract between a US and an Australian party has litigated it.
- Say whether amounts are inclusive or exclusive of VAT, sales tax and withholding, and who bears withholding. A gross-up clause is a real cost, not boilerplate.
- Numbers in words and figures is a convention worth keeping for principal amounts; when they conflict, most systems prefer the words — which is an argument you do not want, so proofread both.
- Dates: unambiguous format (1 March 2026, not 03/01/2026). Any date computed from another date states its counting unit and whether the first day counts (SKILL.md Rule 3).
- Periods: "12 months from the Effective Date" ends on the anniversary; "365 days" does not, in a leap year. Use months for terms and days for notice periods, consistently.

## Conditions, Obligations And Discretion

Distinguish three structures that look alike and behave differently:

- **Condition precedent** — nothing happens until X occurs. "The Supplier's obligation to deliver arises only upon receipt of the Deposit." Failure means no obligation, not a breach.
- **Obligation** — X must happen. Failure is a breach with the usual remedies.
- **Discretion with a standard** — "the Customer may reject Deliverables that do not conform to the Specification, acting reasonably." Unfettered discretion is often read down by courts anyway; adding the standard makes it predictable.

Acceptance mechanics deserve their own drafting: what triggers the acceptance test, who runs it, how long they have, what deemed acceptance looks like if they say nothing, and how many correction cycles exist before a refund right. Services disputes are usually acceptance disputes.

## Structuring Multi-Document Deals

A modern commercial deal is a stack: master agreement + order form + SOW + DPA + security exhibit + policies incorporated by reference. Rules that keep it coherent:

- One precedence clause, in the master, listing every document type in order. Most common and most sensible: order form (deal-specific) → SOW → master → exhibits → policies.
- Each subordinate document says which master it is issued under, with the master's date.
- Amendments to the master do not live in an order form unless the order form says so expressly and the precedence clause permits it. Otherwise a salesperson amends the liability cap by accident.
- Policies incorporated by URL are pinned to a dated version, or attached (SKILL.md Rule 8).

## Execution And Signature Blocks

```
SIGNED for and on behalf of
ACME TECHNOLOGIES LIMITED (company number 12345678)

Name:
Title:
Date:
```

- The party is the registered entity, with its form and registration number. Trade names go in the recitals, never the parties clause.
- Title matters: "Director", "Authorised Signatory", "CEO". A signature by someone with no authority may still bind through apparent authority, but that is a litigation position, not a plan.
- Some entity types and instruments need extra formality — deeds in England and Wales require a witness for individuals, and some jurisdictions require notarisation or an apostille for cross-border corporate documents. Check before scheduling the signing.
- Counterparts clause plus a statement that scanned or electronic copies have the same effect as originals.
- Where a document must be a deed (no consideration, or a longer limitation period is wanted), say so on its face and use the correct execution wording; getting this wrong turns an intended deed into a simple contract with a shorter limitation period.

## Electronic Signature

Generally valid for commercial contracts: US ESIGN Act (2000) and state UETA; EU eIDAS, which recognises simple, advanced and qualified electronic signatures, with qualified carrying the strongest evidential weight; comparable regimes in the UK, Canada, Australia, India and elsewhere. Recurring exclusions to check locally: wills and testamentary instruments, some family-law documents, certain real-property transfers, documents requiring notarisation or a witness, and some court filings.

What actually matters evidentially is the audit trail: who signed, from which email, at what time, from which IP, with what authentication, and whether the document was tamper-evident afterwards. Choose the tool for the trail, and record which tool was used in the contract row.

## Amendments

- **Amendment agreement** for a few changes: recite the original, state clause by clause what is deleted and inserted, confirm everything else continues. Never send a "clean amended version" without also stating what changed.
- **Amended and restated agreement** when the changes exceed roughly a quarter of the document, or after the second amendment — three stacked amendments make the operative text unreadable and errors inevitable.
- Every amendment names the original by title and date, and is signed with the same formality as the original.
- A variation clause requiring writing is generally effective in England and Wales after *Rock Advertising v MWB* (2018); in some other systems oral variation can still bind despite the clause. Do not rely on the clause alone — get the writing.

## Plain Language

Legalese is not precision. "Notwithstanding anything to the contrary herein contained" usually means "despite clause 7" and should say so. Cut: witnesseth, hereinbefore, aforesaid, the said, thereunder. Keep: the technical terms that carry settled meaning (indemnify, warrant, assign, joint and several, without prejudice) — replacing those with plain synonyms loses the case law behind them.

Sentence discipline: one obligation per sentence, average under 25 words, numbered sub-clauses for lists of conditions. A clause that has to be read three times is a clause that will be argued about.

## Self-Review Pass

Run this before sending any draft:

- Every capitalised term defined; every defined term used
- Every cross-reference points at the clause it names (renumbering breaks these silently)
- Every obligation has a named subject and a deadline
- Every amount has a currency and a tax treatment
- The liability cap, its carve-outs and the survival clause agree with each other
- Schedules referenced in the body exist and are attached
- Parties' registered names and numbers verified against the register
- Precedence clause lists every document in this deal

**After a draft ships**, write in the same turn (`memory-template.md`): a reusable document goes to `~/Clawic/data/lawyer/artifacts/template-<type>.md` with a note on what it was built for, and its `## Boxes` line goes into `memory.md`. A drafting decision that took real thought — why the deed form, why this acceptance mechanic — goes to `artifacts/memo-<topic>.md` with the reasoning, because the next person to touch this document will otherwise undo it.
