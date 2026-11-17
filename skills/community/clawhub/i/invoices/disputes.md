# Disputes — When The Invoice Is Wrong

An invoice that is incorrect is not a filing problem, it is a negotiation with a deadline. The archive's job is to make the negotiation short.

**Before opening or continuing a dispute**, read the supplier's ledger history for the last twelve months, their row in `## Suppliers`, and any `artifacts/dispute-*.md` that `## Boxes` names for them. A dispute argued without the history is argued from the supplier's version of it.

**Contents:** [Classify First](#classify-first) · [The Evidence Pack](#the-evidence-pack) · [Common Disputes](#common-disputes) · [Credit Note Or Corrected Invoice](#credit-note-or-corrected-invoice) · [Escalation Ladder](#escalation-ladder) · [Paying Under Dispute](#paying-under-dispute) · [Deadlines That Bite](#deadlines-that-bite) · [Closing](#closing)

## Classify First

The four categories need four different first moves, and treating them alike wastes the fastest window.

| Category | Signal | First move |
|---|---|---|
| Extraction error | The document is right; the ledger row is wrong | Fix the row. Not a dispute; never contact the supplier |
| Clerical error on the invoice | Wrong date, wrong address, missing tax ID, wrong rate | Request a corrected invoice; usually resolved in one message |
| Commercial disagreement | Wrong quantity, wrong price, service not delivered, contract mismatch | Evidence pack, then a specific ask |
| Not our invoice at all | Names someone else, or a service never contracted | Do not pay, do not file as a cost; return it and check for a phantom-vendor pattern (Red Flags) |

Most "the invoice is wrong" reports resolve in the first row. Check the row against the document before anything else.

## The Evidence Pack

Assembled once, at the start, from what is already stored:

- **The invoice itself** and its archive path.
- **The prior twelve months** from the same supplier: what the same thing cost before. A price comparison from your own ledger ends more disputes than any argument about what was agreed.
- **The contract, order, or quote**, if one exists and is archived alongside (`filing.md`).
- **The purchase order and the goods receipt**, where the workflow has them (`approvals.md`).
- **The specific delta**: the amount in dispute, stated separately from the total. "Your invoice is wrong" invites a defence; "line 3 bills 4 seats, we have 2, the difference is 118.00 EUR" invites a credit note.

Write the pack into `artifacts/dispute-<supplier>-<number>.md` from the first message, not once it escalates. The useful part is the chronology, and a chronology reconstructed three months later is missing exactly the dates that decide who let it drift.

## Common Disputes

| Situation | What is usually true | The ask |
|---|---|---|
| Billed for seats, licences, or units no longer used | The supplier bills the plan, not the usage; downgrades often apply next cycle | Credit for the difference, and confirm the effective date of the change |
| Price higher than agreed | Indexation clause, promotional rate expired, or plan auto-upgraded | Ask which of the three; the answer decides whether it is a dispute or a price rise (`suppliers.md`) |
| Service not delivered or partially delivered | Genuine, and the supplier often knows | Credit note for the undelivered portion, with the period stated |
| Duplicate billing | A re-issue treated as new, on their side or yours | Rule 3 check first; if theirs, a credit note referencing both numbers |
| Charges after cancellation | Cancellation not processed, or notice period applies | Ask for the cancellation record and the terms; notice periods are often legitimate and often forgotten |
| VAT charged when reverse charge applies | The supplier lacks a valid VAT number for the user | Provide the number and request a corrected invoice; this cannot be fixed by re-coding (`vat.md`) |
| Currency or exchange rate on the invoice | Supplier converted at their own rate | Not a dispute if the contract permits it; the FX handling is yours (Rule 4) |
| Late fee on an invoice that was paid | Payment did not match: reference, account, or amount | Send the payment evidence with the reference used (`payments.md`) |
| Invoice for an unrecognised service, small amount | Sometimes legitimate and forgotten, sometimes a low-value fraud that survives on nobody checking | Identify the internal requester before paying (`approvals.md`) |

## Credit Note Or Corrected Invoice

The supplier chooses, but the choice changes the accounting, so ask for the right one:

- **Corrected invoice** when the original was wrong in a way that makes it invalid — wrong recipient, wrong tax ID, wrong rate, missing mandatory element. It replaces the original; the original row becomes `superseded-by <number>` and both files stay archived (Rule 1).
- **Credit note** when the original was valid and the amount changes — a partial credit, a return, an agreed reduction. Its own row, negative, in the period **it** was issued (`payments.md`).
- **Never** a verbal agreement to "just pay less". A payment that does not match an issued document leaves an open balance on the supplier's side and produces a dunning notice months later, usually after the person who agreed it has left.
- **Never** an edited PDF. Neither party's edit is the document; the supplier issues, the archive stores (Rule 1).

## Escalation Ladder

One rung at a time, each with a stated deadline, each appended to `artifacts/dispute-<supplier>-<number>.md` with its date on the day it happens:

1. **Billing desk, in writing**, with the specific delta and the requested instrument. Most disputes end here.
2. **Account manager or the named contact** at the supplier (`contacts/`), when the billing desk has not answered within their stated turnaround or two weeks, whichever is shorter.
3. **Written formal notice** stating the disputed amount, the reason, that the undisputed portion has been paid, and a deadline. In several jurisdictions this is also what stops late-payment interest running on the disputed part.
4. **Withholding the disputed amount** while paying the rest, communicated explicitly.
5. **Cancellation or legal escalation.** Below the cost of the process, this is a decision to stop rather than a step — and it is the user's decision, always stated with the amount at stake and the likely cost of pursuing it.

Escalating faster than this ladder costs goodwill on a supplier who was going to fix it in one message. Escalating slower means arriving after the window in which they can still issue a correction for the period.

## Paying Under Dispute

- **Pay the undisputed portion, on time.** It removes the late-payment argument entirely and narrows the conversation to the delta.
- **Say what is withheld and why**, in writing, referencing the invoice number. A silent short payment reads as delinquency and gets processed as one.
- **Do not pay in full to "sort it out later".** Recovering money already paid is a different and much slower problem than not sending it, especially from a supplier you are about to stop using.
- A disputed invoice stays out of the payables total and is reported separately (`payments.md`).

## Deadlines That Bite

- **The tax period.** A dispute unresolved when the period is filed forces a choice: file with the invoice as issued and correct later, or exclude it and carry the explanation. Both are worse than resolving it in time, which is why the period-close checklist reviews open disputes explicitly (`period-close.md`).
- **The supplier's own correction window.** Some can only issue a credit note within the same fiscal year; after that the process becomes slower and occasionally impossible.
- **Contractual notice periods** for objecting to an invoice — often 30 days, sometimes shorter, buried in terms nobody reads until they matter. When one exists for a supplier, it belongs in their row.
- **Statutory limitation** on the underlying claim, measured in years, which is the outer bound and rarely the binding one.

## Closing

1. The credit note or corrected invoice is filed like any other document, with its own row (`filing.md`).
2. The original row's status is updated: `credited-by` or `superseded-by`, never edited amounts.
3. The `## Open Items` row is **deleted**, not annotated — the ledger holds the history, and a list of resolved disputes is how that section silently grows past its split threshold.
4. The artifact is closed with the outcome, the instrument number, and the elapsed time. Elapsed time is the number that tells the user whether this supplier is worth the friction.
5. Anything learned that changes future handling — a notice period, an indexation clause, a billing contact who actually responds — goes to the supplier row or `contacts/`.

**Write before you finish**: the dispute chronology lives in `artifacts/dispute-<supplier>-<number>.md` from the first message, with its `## Boxes` line; the open state lives in `## Open Items` and is deleted on resolution; the credit note or corrected invoice gets its own ledger row and updates the original's status; a recurring cause goes to the supplier row in `## Suppliers` (`memory-template.md`).
