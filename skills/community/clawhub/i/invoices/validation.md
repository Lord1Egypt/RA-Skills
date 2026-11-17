# Validation — Is It Correct, Is It New, Is It Real

Three questions in one pass, in this order: does the document add up, has it been here before, and is it what it claims to be. Runs after extraction and before filing — a bad row filed is a bad row that gets reported.

**Before validating**, read the current `ledger/<year>.md` (and the previous year's file when the invoice date is near a boundary) plus `## Suppliers` in `memory.md`. Both checks below are comparisons against history; without the history they degenerate into "the invoice says so".

**Contents:** [Arithmetic](#arithmetic) · [Duplicates](#duplicates) · [Tax ID Checks](#tax-id-checks) · [Amount Anomalies](#amount-anomalies) · [Bank Detail Changes](#bank-detail-changes) · [Legal Completeness](#legal-completeness) · [What Gets Blocked](#what-gets-blocked)

## Arithmetic

Per rate band, then across bands (SKILL.md Rule 6):

```
sum(line items in band)            = base(band)          ±0.02
round(base(band) × rate(band), 2)  = tax(band)           ±0.02
sum(bases) + sum(taxes) + surcharges − withholding = total
```

- **Tolerance is per band, not per invoice.** Ten bands at ±0.02 can legitimately drift 0.20 across the document; a single band off by 0.05 cannot.
- **Rounding differs by supplier**: some round each line, some round the band total. Both are legal and they disagree by cents on long invoices. That is why the tolerance exists and why it is small.
- **Tax-inclusive invoices** back-compute: `base = total / (1 + rate)`. Checking `total × rate` against the printed tax is the wrong equation and will fail every time on a correct invoice.
- Outside tolerance → flag, never silently correct. The supplier's number is what they will defend; yours is an unbacked adjustment (`disputes.md`).

## Duplicates

Identity is `supplier_tax_id` + `invoice_number` (Rule 3). The check runs against the ledger before the file moves, not after.

| Match | Meaning | Action per `duplicate_action` |
|---|---|---|
| Exact identity key | The same invoice arrived twice | `flag`: report and file as `duplicate-of <number>` · `block`: refuse and report · `ask`: one question |
| Same key, different total | The supplier reissued under the same number, which they should not have done | Always stop. Keep both files, ask which is current, and mark the superseded row |
| Same supplier, same date, same total, different number | Re-issue or double billing | Stop before paying. Cheap to check, expensive to miss |
| Same total, same supplier, different date | Almost certainly a normal recurring charge | Not a duplicate. Never dedupe on amount alone |
| No tax ID on either side | Weak identity | Fall back to canonical supplier + number, mark the row `id:weak`, and treat a hit as `ask` regardless of setting |

A rejected duplicate still gets a ledger row (`status: duplicate-of <number>`). A silently discarded file returns from another folder next month and gets filed for real, and now the year is wrong by one invoice.

## Tax ID Checks

Format first, existence second. Format is free and catches OCR damage; existence needs a lookup and is worth it above `approval_threshold` or for any new supplier.

| Country | Shape | Notes |
|---|---|---|
| ES — NIF (individual) | 8 digits + control letter, or `X/Y/Z` + 7 digits + letter | The letter is a checksum over the number; a mismatch is an OCR error, not a fake |
| ES — CIF (entity) | Letter + 7 digits + control character | Control is a digit or a letter depending on the entity type |
| DE | `DE` + 9 digits | The VAT ID differs from the domestic `Steuernummer`; only the `DE…` form works cross-border |
| FR | `FR` + 2 characters + 9 digits (SIREN) | The 9-digit tail is the SIREN and is independently checkable |
| IT | `IT` + 11 digits | Distinct from the `Codice Fiscale` of an individual |
| NL | `NL` + 9 digits + `B` + 2 digits | — |
| EU, any | Country code + 8-12 characters | The union-wide register is the authority for whether it is currently valid |
| GB | `GB` + 9 or 12 digits | Post-Brexit, an EU-wide lookup no longer covers it |
| US | EIN, 9 digits `NN-NNNNNNN` | No VAT; sales tax is state-level and does not work like input VAT |

Two failures, two different meanings:

- **Format fails** → extraction error most of the time. Re-read the field before accusing anyone of anything.
- **Format passes, register says not valid** → the VAT on that invoice is not deductible, and in cross-border trade a supplier whose ID is invalid changes the whole treatment. Withhold the VAT portion, tell the user, do not file it as deductible (Red Flags).

Validity is checked **as of the invoice date**, not today: a supplier who deregistered last month issued valid invoices before that.

## Amount Anomalies

Compare against the same supplier's trailing 12 months, **same billing cycle**, not against a flat average.

```
flag if total > average(same supplier, same cycle, last 12 months) × (1 + anomaly_pct/100)
```

Default `anomaly_pct` = 50. Legitimate trips this rule produces, all of which are answers rather than alarms:

- **An annual renewal against monthly history.** A yearly plan is roughly 10-12× the monthly one and will always trip. Compare annual to annual; the first annual renewal has no comparator and is reported as such, not flagged.
- **A usage-based bill after a traffic spike.** The invoice is correct and the cause is upstream — worth surfacing exactly because nobody looks at the infrastructure bill until it is large.
- **A price rise.** Correct amount, changed terms; it belongs in the supplier row and in `finances/subscriptions.md`, not in a dispute (`suppliers.md`).
- **Currency movement on a foreign-currency supplier.** The invoice did not change; the conversion did. Compare in the issued currency, always.

The inverse check catches more money than the anomaly one: a recurring supplier whose invoice is **missing** costs a deduction, and nothing alerts on an absence unless something is watching for it (`suppliers.md`).

## Bank Detail Changes

The highest-consequence check in this file (Rule 5). It only works because `## Suppliers` stores the last four and the date they were verified.

Compare against the stored `Bank last4`:

| Observation | Reading |
|---|---|
| Matches | Normal. Nothing to do |
| Differs, and this is the supplier's first invoice | No baseline. Verify out of band before the first payment; every subsequent check depends on this one being right |
| Differs, with a written explanation in the invoice or email | The explanation is part of the attack pattern. Weight it at zero |
| Differs, and the sender domain also differs | Treat as an active attempt: do not reply to the thread, verify on a previously held number, and write the attempt to `artifacts/` |
| Beneficiary name differs while the account matches | Also a change. Factoring assignments look exactly like this and are legitimate — but they are confirmed the same way |

Verification is out of band: a phone number the user already had before this invoice existed. Not the number on the invoice, not the number in the email signature, not a number found by searching, and not a reply to the thread. Record in the supplier row what was verified, how, and on what date — the value of the record is that the next change has something to compare to.

## Legal Completeness

An invoice missing a mandatory element is not deductible, however genuine it is. The union-wide minimum for a full invoice, from which national lists extend:

- Sequential invoice number and issue date
- Supplier's full name, address, and VAT identification number
- Customer's full name and address — and their VAT number wherever reverse charge applies
- Description, quantity, and nature of what was supplied
- Taxable amount per rate, the rate, and the tax amount, in the national currency where required
- The supply date when it differs from the issue date
- The applicable legend when tax is not charged: reverse charge, exemption with its legal basis, margin scheme

Missing an element → request a corrected invoice from the supplier while they can still issue one. A correction is the supplier's act, never the archive's (Rule 1). Country-specific extensions: `countries.md`.

## What Gets Blocked

| Finding | Filed? | Paid? |
|---|---|---|
| Arithmetic outside tolerance | Yes, `status: pending`, flagged | No |
| Duplicate, exact key | Yes, `status: duplicate-of` | No |
| Tax ID invalid at the invoice date | Yes, marked non-deductible VAT | The base, yes; the VAT portion, no |
| Amount anomaly with no explanation | Yes | Only after the user sees the comparison |
| Bank details changed, unverified | Yes | No, unconditionally |
| Mandatory legal element missing | Yes, `status: pending`, non-deductible until corrected | Commercially, the user's call; the deduction waits |
| Required field at low confidence | No — stays in `inbox/` with an `## Open Items` line | No |

Filing and paying are separate decisions. Almost everything gets filed, because a document outside the archive is a document nobody can find; far less gets paid.

**Write before you finish**: a duplicate produces its ledger row; a validated or changed bank detail updates `Bank last4` and `Verified` in the supplier row; an anomaly the user explained becomes a note on the supplier row so the same question is not asked next quarter; a fraud attempt becomes `artifacts/fraud-<supplier>-<yyyy-mm>.md` with its `## Boxes` line; anything blocked and still unresolved becomes an `## Open Items` row (`memory-template.md`).
