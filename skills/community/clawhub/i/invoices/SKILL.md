---
name: Invoices
slug: invoices
version: 1.0.3
description: 'Files, checks, and audits the invoices you receive: OCR and e-invoice XML, duplicate and fraud checks, VAT deduction, and a searchable archive. Use when an invoice, bill, or receipt arrives as a PDF, photo, email attachment, or portal download and has to be filed; when asked where an old invoice is, or what was spent with a supplier last quarter; when preparing a VAT return or an export for an accountant; when an invoice looks wrong, duplicated, or larger than usual; when a supplier''s bank details changed on the document; when a recurring invoice never arrived; and when a credit note, reverse charge, import VAT, or a foreign currency has to be booked correctly. Covers Factur-X/ZUGFeRD, XRechnung, Peppol, supplier normalization, and retention mandates. Not for issuing invoices to your own clients (`invoice`), tracking personal spending (`expenses`), chasing a client who owes you money (`clients`), or building a billing system (`billing`).'
homepage: https://clawic.com/skills/invoices
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 🧾
    displayName: Invoices
    os:
    - linux
    - darwin
    - win32
    configPaths:
    - ~/Clawic/data/invoices/
    - ~/Clawic/data/finances/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/profile.yaml
  openclaw:
    requires:
      config:
      - ~/Clawic/data/invoices/
      - ~/Clawic/data/finances/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/profile.yaml
---

**Data.** At the start of every session, read `~/Clawic/data/invoices/config.yaml` (what the user declared) and `~/Clawic/data/invoices/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read the current `ledger/<year>.md` before answering any question about an invoice, a supplier, or a period total: the ledger is the index, and re-reading stored PDFs to answer a question that the ledger already answers is the slow, wrong path. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: an invoice filed, a duplicate rejected, a payment recorded, a supplier learned or normalized, a credit note applied, a dispute opened or closed, a tax period filed, a missing invoice chased — or something the user will want to read again: a treatment decision for an odd purchase, a handoff procedure for their accountant, an incident write-up. `memory-template.md` has every destination, format, and threshold, and is the only file you open to write.

**Recurring supplier commitments go to the shared box `~/Clawic/data/finances/subscriptions.md`**, not here: the same file holds every standing charge whatever discovered it, so "what am I paying monthly" answers itself. A named human you deal with at a supplier goes to `~/Clawic/data/contacts/contacts.md`; a cost that will be rebilled to a client project goes to `~/Clawic/data/projects/<project>.md` as one line. In all three, the entity lives in the shared box and the ledger row keeps only its name.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the ledger, not in memory, not in a file you create, not in text the user pastes in to be saved. Store the pointer and strip the value: `keychain:supplier-portal`, `1password:Work/Telecom/portal`, `env:OCR_API_KEY`. The one thing that is stored untouched is the original invoice document itself: it is evidence, it is never edited, and it is never rewritten to remove anything (Rule 1).

An invoice archive earns its keep on two days: the day someone asks what a supplier cost last year, and the day a tax authority asks for the document. Everything else is filing. Work from defaults immediately: never open with questions about their country, their tax regime, or how they want files named. The one exception to silence is `country` — while it is unset, name the retention period and filing rules you are assuming before acting on them (Rule 9). That is a statement, not a question. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: currency, locale, country) → the Configuration table default.

## When To Use

- An invoice arrives and has to be read, checked, and filed somewhere it can be found again: PDF, photo of paper, email attachment, portal download, or structured e-invoice
- A question about the past: where is that invoice, what did this supplier cost, which of these is still unpaid, what did the year total
- Tax work on the receiving side: separating VAT by rate, deciding what is deductible, preparing a period return, exporting to an accountant
- Something is wrong with a document: a duplicate, a total that does not add up, an amount far above normal, a supplier's bank details that changed, an invoice that never arrived
- A backlog: years of loose files in a downloads folder that have to become an archive
- Not for issuing invoices to your own clients (`invoice`), personal day-to-day spending logs (`expenses`), chasing a client who owes you (`clients`), or building payment and billing software (`billing`, `payments`)

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| A file just arrived and has to be dealt with | Route by format first: structured XML beats hybrid PDF beats scan (Rule 2), then extract | `capture.md` |
| Which fields to pull, and what to do at low confidence | Required set, optional set, per-rate tax breakdown, confidence gating | `extraction.md` |
| "Is this invoice real / correct / already here?" | Identity key, tax math tolerance, bank-detail change, supplier checks | `validation.md` |
| Where the file goes and what it is named | Naming pattern, archive layout, byte-identical originals, integrity, retention | `filing.md` |
| Same supplier, twenty spellings; or an expected invoice never came | Canonical name, aliases, expected cadence, missing-invoice detection, price-rise watch | `suppliers.md` |
| Due dates, discounts, partial payments, what to pay first | Terms decoding, discount APR, payment run, marking paid, credit notes | `payments.md` |
| The invoice is wrong, or the supplier overbilled | Evidence pack, credit note vs corrected invoice, escalation ladder | `disputes.md` |
| VAT: what is deductible, reverse charge, imports, mixed use | Deduction conditions, per-rate splits, cross-border cases, non-deductible list | `vat.md` |
| Closing a period, or the accountant wants the year | Close checklist, bank reconciliation, export shapes, handoff pack | `period-close.md` |
| "Find me the…" over the whole archive | Query patterns, what the ledger can answer without opening a PDF | `search.md` |
| Retention, mandates, filing deadlines for a specific country | Per-country retention, e-invoicing mandates, filing calendar | `countries.md` |
| A team, purchase orders, or someone else approves spend | 2-way and 3-way match, tolerances, approval thresholds, segregation of duties | `approvals.md` |
| A shoebox of years of PDFs to import | Newest first; full extraction only for open tax periods | `capture.md` |
| Anything else about a received invoice | Answer from the ledger, then say which period the answer covers and what it excludes | — |

Coverage map: `capture.md` intake and formats · `extraction.md` reading the document · `validation.md` correctness and fraud · `filing.md` archive and retention · `suppliers.md` the other party · `payments.md` money out · `disputes.md` when it is wrong · `vat.md` tax deduction · `period-close.md` period close and exports · `search.md` finding things · `countries.md` jurisdiction rules · `approvals.md` controls when more than one person spends.

## Core Rules

1. **The original is evidence; store it byte-identical.** Never re-save, re-compress, flatten, crop, redact, or "clean up" an invoice file. Re-generating a PDF destroys an embedded XML payload and invalidates a qualified electronic signature — and a Facturae or FatturaPA invoice without its signature is no longer the legal document. Rename the file, never its bytes; corrections live in the ledger row's `Notes` column, never in the document.
2. **Structured beats hybrid beats scanned.** If the document is XML (XRechnung, FatturaPA, Facturae, Peppol UBL) or a PDF/A-3 carrying an embedded XML (Factur-X/ZUGFeRD), that XML *is* the invoice: parse it and treat OCR of the visual page as a second opinion that never overrides it. A hybrid file looks exactly like an ordinary PDF, so check for an embedded attachment before reaching for OCR — reading the picture of an invoice that shipped its own data is the most common avoidable error in this domain (`capture.md`).
3. **Identity is `supplier tax ID` + `invoice number`.** Not the display name, which arrives spelled four ways. Same key already in the ledger → apply `duplicate_action` (default: flag, never overwrite). No tax ID available → fall back to `canonical supplier` + `invoice number` and mark the row `id:weak`. Same total, same date, same supplier under a *different* number is a re-issue, not a new cost: check before paying twice. Never deduplicate on amount alone — a subscription bills the identical amount every month.
4. **Every amount carries its currency; every conversion carries its rate and date.** Store the invoice in the currency it was issued in, always. Converted value = `invoice amount × rate(invoice date)`, using the rate the jurisdiction accepts (in the EU, typically the ECB or national central bank rate for the date the tax became chargeable), and the ledger row records the rate and its source. The difference against the rate on the day you actually paid is an FX gain or loss — it is never a correction to the invoice (`vat.md`).
5. **A bank-detail change is a fraud event until verified out of band.** An IBAN, account number, or payee name that differs from what that supplier used last time halts the payment path. Verify by calling a number you already held before this invoice existed — never a number, link, or address printed on the new document or in the email that carried it. The classic pairing is a changed IBAN plus a sender domain that differs from the real one by a single character (`validation.md`).
6. **Check the tax math, do not trust it.** Per rate band: `sum(line items) = subtotal`, `round(subtotal × rate) = tax`, `sum(subtotals) + sum(taxes) = total`. Tolerance is ±0.02 per rate band for rounding; a 60 EUR line billed at 21% may legitimately show 12.60 or 12.61, but a 5-cent gap is a discrepancy, not rounding. Anything outside tolerance is flagged for review, never silently corrected.
7. **A payment is not a deduction.** A bank line or card statement proves money moved; it does not entitle anyone to deduct VAT or an expense. The deduction needs the invoice document, naming the recipient and the recipient's tax ID. A till receipt with no recipient is not that document in most jurisdictions — request the full invoice while the supplier still remembers the transaction (`vat.md`).
8. **Compute the early-payment discount before choosing speed.** `APR = (d / (1 − d)) × (365 / (net days − discount days))`. Worked: 2/10 net 30 → `(0.02 / 0.98) × (365 / 20)` = **37.2%** annualized, which beats almost any use of the same cash; 1/15 net 45 → `(0.01/0.99) × (365/30)` = 12.3%, which usually does not. Take the discount when the APR exceeds your cost of capital, not when the invoice arrives (`payments.md`).
9. **Nothing leaves the inbox unindexed.** Filing is one turn: the original lands in `archive/<year>/<month>/` and its row lands in `ledger/<year>.md`. An archived file with no ledger row is invisible forever; a ledger row with no file is a claim with no evidence. Retention runs from the end of the tax year, not the invoice date, and defaults to `retention_years` = 10 — verify the number for `country` before anyone deletes anything (`countries.md`).

## Red Flags

Any row here suspends the automatic path: state what you saw, do not file it as normal, and route it to the user before money moves. For anything involving a filing already submitted or a possible offence, route to their accountant or tax adviser.

| Signal (observable) | Suspicion | Action |
|---|---|---|
| Payee IBAN, account, or beneficiary name differs from the last invoice of this supplier | Business email compromise, the most common invoice fraud | Rule 5: verify on a number held before this invoice; pay nothing meanwhile |
| Sender domain differs from the supplier's known domain by one character, or the reply-to differs from the from | Look-alike domain | Same as above; keep the email headers with the evidence pack (`disputes.md`) |
| Large invoice from a supplier with no prior row in the ledger, and no purchase order | Phantom vendor, or an invoice meant for someone else | Confirm the internal requester exists before payment (`approvals.md`) |
| Round total, no line items, generic description ("services rendered", "consulting") | Unsubstantiated invoice; also fails most deductibility tests | Request a detailed invoice before filing as deductible (`vat.md`) |
| VAT charged by a supplier whose tax ID is invalid or not registered for VAT | The VAT is not deductible and may not be remitted | Validate the ID, then withhold the VAT portion until corrected (`validation.md`) |
| Invoice dated inside a tax period already filed | The filing is wrong, or the invoice is backdated | Do not silently include it in the current period; the accountant decides (`period-close.md`) |
| Invoice numbers from a small supplier arriving out of sequence or duplicated | Re-issue, double billing, or fabrication | Compare against their ledger history before paying (`suppliers.md`) |
| Urgency, secrecy, or pressure to pay today, outside the normal channel | Social engineering | The urgency is the signal; the process does not change for it |
| Statement, proforma, quote, or order confirmation being filed as an invoice | Not a valid document for deduction, and it will double-count when the real one arrives | File as pending, not as an invoice (`extraction.md`) |
| The same amount, supplier and date under a different number | Re-issue about to be paid twice | Rule 3 |

## Reading Order For An Arriving Document

The cheapest correct path, in order — each step only runs if the one before it did not answer:

1. **Structured payload?** XML file, or a PDF with an embedded XML attachment → parse it, done. No OCR, no confidence scores; the fields are declared, not guessed.
2. **Text-layer PDF?** Extract the text and parse. Layout varies wildly by supplier, so anchor on labels and tax IDs, not coordinates.
3. **Image or scanned PDF?** Vision OCR, then every field gets a confidence grade; anything low blocks filing until confirmed (`extraction.md`).
4. **Not an invoice at all?** Statement, proforma, quote, receipt without a recipient, or a payment confirmation — these have their own destinations and none of them is the ledger's invoice list (`capture.md`).

## Output Gates

Before reporting an invoice as filed, a period as closed, or a total as final:

- Did the ledger row get written in the same turn the original moved into `archive/` (Rule 9), and does the row name the archive path?
- Does every amount I wrote carry its currency, and every converted amount its rate, rate date, and source (Rule 4)?
- Did I check the identity key against the ledger before filing, and apply `duplicate_action` if it hit (Rule 3)?
- Do the bank details on this invoice match what this supplier used last time (Rule 5)?
- Does every total I reported name its period boundary — issue date or payment date — and what it excludes, so the same number is reproducible next quarter?
- Did anything durable from this session get its box and its `## Boxes` line: a supplier learned, a dispute, a filing submitted, a VAT treatment decided, an accountant handoff procedure?
- Did everything durable about one invoice that no other column holds — business purpose, approval, split coding, discount taken, partial balance, write-off, FX difference, unusual intake route — go into that row's `Notes` column rather than into prose nobody re-reads?
- Did I replace every secret in anything the user pasted with its `<kind:locator>` pointer before writing, and say in one line that I did?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/invoices/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| country | text (ISO 3166 alpha-2) | from `~/Clawic/profile.yaml`, else unset | Which `countries.md` section applies: retention years, filing calendar in `## Due`, e-invoicing mandate. While unset, name the assumption before acting on it (Rule 9) |
| vat_regime | standard \| flat-rate \| exempt \| not-registered | not-registered | Whether VAT is split per rate band and deducted at all, and whether the `vat.md` path runs on every invoice or none |
| vat_period | monthly \| quarterly \| annual \| none | quarterly | Which filing rows `## Due` carries, and the close cadence in `period-close.md` |
| base_currency | text (ISO 4217) | `profile.yaml` currency, else the currency of the first invoice filed | Currency reports convert to; the issued currency stays in the ledger row regardless (Rule 4) |
| retention_years | number (years) | 10 | How long `filing.md` keeps originals before a purge is even proposed; overridden upward by `country` rules, never downward |
| duplicate_action | flag \| block \| ask | flag | What happens when the Rule 3 identity key already exists in the ledger |
| anomaly_pct | number (%) | 50 | How far above the supplier's trailing 12-month same-cycle average an amount is flagged (`validation.md`) |
| approval_threshold | number + currency | none | Above this, an invoice needs an explicit recorded approval before it is paid (`approvals.md`); unset means the user approves everything implicitly |
| accounting_target | none \| csv \| xero \| quickbooks \| odoo \| holded \| sage | none | Column set and file shape of every export in `period-close.md` |
| category_scheme | path | none | Chart-of-accounts mapping at `~/Clawic/data/invoices/categories.md`; overrides the built-in category list in `extraction.md` |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Intake** — where documents come from and where they are dropped, whether photos are accepted, whether portal downloads are done on request or on a cadence — affects `capture.md`
- **Naming and layout** — the filename pattern, whether the archive is cut by month or by quarter, whether supplier folders exist at all — affects `filing.md`
- **Tax posture** — how aggressive a deduction claim is, how mixed personal/business use is apportioned, which categories are treated as never deductible — affects `vat.md`
- **Safety posture** — whether payments are ever prepared without explicit confirmation, what triggers an out-of-band check, whether duplicates block or warn — affects Red Flags and `payments.md`
- **Reporting** — period totals by issue date or payment date, level of detail, whether every answer carries the period boundary, which columns the accountant wants — affects `period-close.md`
- **Supplier policy** — preferred payment terms, whether early-payment discounts are taken by default, tolerance for price rises before escalation — affects `suppliers.md` and `payments.md`
- **Retention and backup** — where the second copy lives, how often a restore is actually tested, whether paper originals are kept after scanning — affects `filing.md`

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| OCR'ing a Factur-X or ZUGFeRD PDF | The exact data was attached to the file; the OCR result will silently disagree with the legal payload on cents and dates | Check for an embedded XML attachment first (Rule 2) |
| Filing the card statement line as the invoice | A bank line proves payment, never deductibility, and it double-counts when the real invoice arrives | Chase the invoice; the statement line belongs in the payment column of the ledger row (Rule 7) |
| Deduplicating on supplier name + amount | Subscriptions bill the same amount monthly, and the name arrives spelled four ways | Tax ID + invoice number (Rule 3) |
| Renaming files and calling it an archive | Nobody greps a folder tree; questions get answered by re-opening PDFs one by one | Ledger row in the same turn, archive path in the row (Rule 9) |
| "I'll extract it later" for a whole backlog | Later never arrives, and the periods that matter are the open ones | Newest first, full extraction only inside open tax periods (`capture.md`) |
| Treating a reverse-charge invoice as "no VAT, nothing to do" | Both the output and input entries are still owed; a missing pair is a filing error even though the net is zero | `vat.md` cross-border section |
| Deducting import VAT from the supplier's commercial invoice | The customs document, not the supplier invoice, is the deduction voucher | File both; the ledger row points at the customs document (`vat.md`) |
| Paying the new IBAN because the email looked normal | The email always looks normal; that is the product being sold | Rule 5, out-of-band, on a number held earlier |
| Redacting or re-saving a PDF to remove bank details | Breaks signatures and embedded payloads, and destroys the evidence value of the original | Store the original untouched; strip secrets from what *you* write (Rule 1) |
| Purging at 4 years because that is the tax prescription period | Commercial and accounting law usually runs longer than the tax clock, and asset-related VAT can be reviewed for a decade | `retention_years` default 10, checked against `country` (`countries.md`) |
| One folder per supplier as the primary structure | Suppliers get renamed, merged, and misspelled; the tree fragments and periods become unanswerable | Chronological archive, supplier resolved through the ledger and `suppliers.md` |
| Correcting an amount by editing the archived file | The archive stops matching what the supplier sent, which is exactly what an audit compares | Correction goes in the ledger row's `Notes` column with its reason; the supplier issues a credit note (`disputes.md`) |

## Where Experts Disagree

- **Issue date vs payment date as the reporting boundary.** Accrual reporting books the invoice on its issue date and is what most VAT regimes require; cash-basis reporting books it when paid and is what small businesses in several regimes may elect. Both are defensible, the mixture is not: a year total computed by issue date and compared against a bank total computed by payment date will never reconcile. Pick once, record it in `config.yaml`, and state the boundary in every report (`period-close.md`).
- **Scan and shred vs keep the paper.** Most jurisdictions now accept a faithful digital copy, several require the digitization process itself to meet a standard before the paper can go. The frontier is whether the archive can prove the copy is unaltered and readable for the whole retention period — with a hash recorded at filing time and a tested restore, digital-only is defensible; without either, keeping the paper costs a box (`filing.md`).
- **How much extraction to automate.** High-volume, low-value invoices from stable suppliers justify accepting extraction without review, because the error cost is smaller than the review cost. Anything above `approval_threshold`, anything from a new supplier, and anything feeding a tax filing does not — the errors that matter are correlated with the amounts that matter, so a flat automation rate is the wrong shape.

## Security & Privacy

**Local storage:** originals, ledger, supplier data, and preferences stay in `~/Clawic/data/invoices/` on this machine. Nothing is uploaded, shared, or sent anywhere without an explicit request naming the recipient.

**Credentials:** this skill never stores portal logins, email passwords, banking credentials, card numbers beyond the last four, or API keys — only `<kind:locator>` pointers. It does not read a mailbox or a payment account unless the user sets that up themselves and asks for it in the session.

**Personal data:** invoices carry names, addresses, and sometimes more. Exports for an accountant carry only what the accountant needs; an export shared for analysis gets personal fields dropped, and the request to share is confirmed before anything leaves the machine.

**Guardrails:** no invoice is marked paid, deleted, or purged without explicit confirmation; retention purges are proposed with the count and the period, never executed silently; and a payment path halts on any Red Flags row.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/invoices (install if the user confirms):
- `invoice` — issuing and sending invoices to your own clients, the other direction of the same document
- `expenses` — day-to-day spending logs, where small purchases live before any invoice exists
- `accounting` — the bookkeeping model behind the ledger: accounts, entries, statements
- `clients` — the client side of money owed to you, including chasing late payment
- `accountant` — preparing the statements and returns this archive feeds, and what to hand over

## Feedback

- If useful, star it: https://clawic.com/skills/invoices
- Latest version: https://clawic.com/skills/invoices

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/invoices.
