# Period Close — Totals, Reconciliation, And Handing It Over

Turning a ledger into a number somebody else will rely on: period totals, reconciliation against the bank, exports, and the annual pack for the accountant.

**Before producing any figure**, read the ledger years the period spans, `## Filings` in `memory.md` (what was already submitted), `config.yaml` for `vat_period`, `base_currency` and `accounting_target`, and any `artifacts/accountant-handoff*.md` that `## Boxes` names — the accountant's stated format outranks every default in this file.

**Contents:** [State The Boundary](#state-the-boundary) · [Close Checklist](#close-checklist) · [The VAT Summary](#the-vat-summary) · [Bank Reconciliation](#bank-reconciliation) · [Export Shapes](#export-shapes) · [The Annual Pack](#the-annual-pack) · [Recurring Outputs](#recurring-outputs) · [Reproducibility](#reproducibility)

## State The Boundary

Every total names three things or it is not a total:

1. **Which dates**: the period, explicitly.
2. **Which date field**: issue date (accrual) or payment date (cash). Never both in one figure, never mixed across figures being compared.
3. **What is excluded**: disputed rows, duplicates, non-deductible items, invoices known to be missing.

A quarter computed by issue date and compared against a bank total computed by payment date will never reconcile, and the hours spent hunting the "error" are spent on a difference that was designed in. The boundary lives in `config.yaml` under `reporting.boundary` once the user states it.

## Close Checklist

Run in order; each step can send you back to a different file.

| Step | Check | Where it goes when it fails |
|---|---|---|
| 1 | `inbox/` is empty | `capture.md` |
| 2 | No ledger row in the period is `pending` or carries a low-confidence required field | `extraction.md` |
| 3 | Every recurring supplier with a cadence has its invoice for the period | `suppliers.md` — a missing invoice is a lost deduction and is the most common close finding |
| 4 | Open disputes are resolved, or how each unresolved one is filed this period is written to its `artifacts/dispute-<supplier>-<number>.md` and to the ledger row's `Notes` | `disputes.md` |
| 5 | Arithmetic and duplicate checks pass across the whole period, not just per invoice | `validation.md` |
| 6 | Every foreign-currency row has its rate, source, and date | Rule 4 |
| 7 | Rate codes are real: no bare `0` where `0%`, `EX`, or `RC` was meant | `vat.md` |
| 8 | Credit notes sit in the period they were issued, not the period they credit | `payments.md` |
| 9 | The bank reconciles both ways | Below |
| 10 | Totals computed, boundary stated, submitted figures written to `## Filings` | `memory-template.md` |

Steps 3 and 9 find almost everything. The rest are cheap enough to run anyway.

## The VAT Summary

Per rate band, with the four zero-cases kept apart:

| Band | Base | Rate | Tax | Count |
|---|---|---|---|---|
| Standard | | | | |
| Reduced | | | | |
| Super-reduced | | | | |
| Zero-rated (`0%`) | | 0 | 0 | |
| Exempt (`EX`) | | — | — | |
| Reverse charge (`RC`) | | — | self-accounted | |
| Non-deductible | | | not reclaimed | |

- Reverse-charge rows produce both an output and an input entry on the return even though the invoice shows no tax (`vat.md`). Listing them only as a base is the error that makes a return fail a cross-check against the supplier's own listing.
- Non-deductible costs appear in the expense total and not in the reclaim total. Showing them in neither hides real spend; showing them in both overstates the reclaim.
- Import VAT comes from the customs documents, never from the supplier invoices, and is listed separately so the two are not double-counted.
- Every figure is stated in `base_currency`, with the note that conversions used the invoice-date rate.

## Bank Reconciliation

The check that finds what nothing else does, and it runs **both directions**:

- **Ledger → bank**: every paid row has a payment. A row marked paid with no bank movement is a bookkeeping error, or a payment that failed and nobody noticed.
- **Bank → ledger**: every business payment out has an invoice. This is the valuable direction — the unmatched list *is* the list of invoices never collected, and each one is a deduction sitting unclaimed.

Matching tolerance: amount exact, date within ±5 days for transfers and ±30 for card charges, allowing for statement lag. Legitimate unmatched items, which get labelled rather than chased:

- Direct debits whose invoice arrives after the charge
- Card payments where the supplier bills monthly rather than per transaction
- Bank fees and FX differences, which have no invoice at all
- Payments to non-suppliers: salaries, tax, transfers between the user's own accounts

Anything left after those labels is either a missing invoice (chase it) or a payment that should not have happened (`validation.md`).

## Export Shapes

`accounting_target` decides the columns. The default `csv` shape, which most systems and most accountants accept:

```csv
date,supplier,tax_id,invoice_number,base,rate,tax,total,currency,fx_rate,category,status,paid_date,file,notes
2026-02-13,Hetzner,DE812871812,INV-12345,75.21,19,14.29,89.50,EUR,,hosting,filed,2026-02-15,archive/2026/02/2026-02-13_hetzner_INV-12345_89.50EUR.pdf,
```

- **One row per rate band**, matching the ledger. A target that expects one row per invoice gets the invoice-level shape instead, and that mapping is recorded in the handoff artifact so it is identical next quarter.
- **Credit notes as negative rows in the same file**, unless the target requires them separately. Splitting them by default is how a quarter silently overstates.
- **Amounts unformatted**: dot decimal, no thousands separator, no currency symbol. The currency is its own column.
- **The file-path column** is what makes a request for one specific document answerable in a single step; drop it only if the recipient objects.
- **The notes column travels with the export.** It carries the business purpose, the split coding, the approval, and the write-off — exactly the things an accountant queries — and dropping it turns every one of those into a question back. Quote it and strip line breaks; a `Notes` cell containing a comma is the standard reason a CSV opens one column short. Drop it only when the target's importer rejects unknown columns, and say so in the handoff artifact.
- **UTF-8 encoding, ISO dates.** Supplier names carry accents, and every locale-formatted date export is eventually read by a system that guesses wrong.
- Anything the target expects that differs from this goes in the handoff artifact, once — including quirks like "wants the tax ID without the country prefix", which are otherwise re-discovered every period.

## The Annual Pack

What an accountant actually needs, as opposed to what people send.

Include:

- **One CSV per period**, or one for the year if that is what they asked for, boundary stated.
- **The documents**, in the archive's folder structure, so a file referenced by a row can be found by its path.
- **A summary sheet**: totals per period, per rate band, per category, plus the reconciliation result.
- **The exceptions list**, explicitly: invoices without a valid tax ID, non-deductible items, unresolved disputes, and invoices from a prior period included here with the reason. This list is what stops twenty questions coming back, and answering them in advance is most of the pack's value.
- **What is missing and known to be missing**, with the estimated amount. An acknowledged gap is workable; an unacknowledged one surfaces at the worst moment.

Leave out: the inbox, duplicates, anything superseded, and personal-use purchases already coded non-deductible unless they were asked for.

## Recurring Outputs

Driven by `## Due`, so they happen without being requested:

| Output | Cadence | Answers |
|---|---|---|
| Inbox sweep | weekly | What arrived and never got filed |
| Missing recurring invoices | monthly | Which cadence suppliers went quiet (`suppliers.md`) |
| Period VAT summary | `vat_period` | What the return will say, before the deadline rather than on it |
| Spend by category and supplier | quarterly | Where the money went, and which supplier grew |
| Annual pack | yearly | Everything above, for the accountant |
| Retention review | yearly | What is now eligible to purge (`filing.md`) |

Each one states its boundary, and each one records its run date in `## Due`. Anything with no last-run date gets skipped for two quarters and nobody notices.

## Reproducibility

The same question asked next year must return the same number.

- **Filed figures are frozen.** `## Filings` records what was submitted, not what is currently computable. A recomputed total that disagrees with a filed one is a finding — and it is only a finding because the filed number was written down.
- **Never rewrite a past year's ledger** to a new column set or a corrected category scheme. Improvements apply going forward; history stays as it was reported (`memory-template.md`).
- **A late invoice does not silently change a closed period.** It is filed with its true issue date, and how it is treated — amended return or later period — is recorded next to the filing it affects (`vat.md`).
- **Say what changed.** When a restated number is right and the filed one was wrong, both appear, with the reason. A number that quietly improves is a number nobody can trust.

**Write before you finish**: the figures actually submitted go to `## Filings` in `memory.md` with the filing date; the run date of every recurring output goes to `## Due`; anything the reconciliation could not match goes to `## Open Items`; an accountant's stated format, deadline, or quirk goes to `artifacts/accountant-handoff.md` with its `## Boxes` line; the generated pack itself is not stored — it is regenerated from the ledger, which is the only copy that stays correct (`memory-template.md`).
