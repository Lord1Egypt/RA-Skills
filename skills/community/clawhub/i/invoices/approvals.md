# Approvals — When More Than One Person Spends

Controls for the case where the person who receives the invoice is not the person who ordered the thing or the person who pays for it. Applies when `approval_threshold` is set, when purchase orders exist, or when anyone other than the user can commit spend.

**Before approving or preparing anything for payment**, read `config.yaml` for `approval_threshold`, the supplier's row in `## Suppliers`, and the invoice's ledger row. An approval given without the supplier's history is an approval given on the supplier's word.

**Contents:** [Why Controls Exist Here](#why-controls-exist-here) · [Two-Way And Three-Way Match](#two-way-and-three-way-match) · [Tolerances](#tolerances) · [Approval Thresholds](#approval-thresholds) · [Segregation Of Duties](#segregation-of-duties) · [Coding](#coding) · [Recording An Approval](#recording-an-approval) · [Solo Operators](#solo-operators)

## Why Controls Exist Here

Three failures, each with a different control:

| Failure | Control |
|---|---|
| Paying for something nobody ordered | Match against a purchase order |
| Paying for something ordered but never delivered | Match against a goods receipt |
| Paying the wrong party for something genuinely owed | Bank-detail verification and segregation of duties (Rule 5) |

Every other item in this file is one of those three, made specific. A control that does not map to one of them is ceremony, and ceremony is what gets skipped in the week it matters.

## Two-Way And Three-Way Match

| Match | Compares | Use for |
|---|---|---|
| Two-way | Purchase order ↔ invoice | Services, subscriptions, anything with no physical delivery |
| Three-way | Purchase order ↔ goods receipt ↔ invoice | Physical goods, and anything where partial delivery is possible |

What gets compared, in order of how often each one is the discrepancy:

1. **Quantity** — invoiced more than received, or more than ordered. The most common real discrepancy and the easiest to prove.
2. **Price** — unit price differs from the agreed one. Usually an indexation clause or an expired promotional rate (`suppliers.md`).
3. **Supplier** — the invoice comes from an entity other than the one the order went to. Legitimate under a factoring assignment, and also exactly what a redirection fraud looks like: verify out of band before treating it as normal.
4. **Terms** — payment terms on the invoice differ from the order. The order governs unless someone agreed otherwise in writing.
5. **Line-level match, not header-level.** A total that agrees while two lines offset each other is the discrepancy that survives every header check.

No purchase order for a substantial invoice from an unknown supplier is a Red Flags row, not a paperwork gap: identify the internal requester before payment, always.

## Tolerances

A match that blocks on cents blocks everything and gets bypassed within a month.

```
accept if difference ≤ min(percentage tolerance × PO value, absolute cap)
default: min(2% × PO value, 25 in base_currency)
```

Worked: a 4,000 EUR order tolerates `min(80, 25)` = 25 EUR, and a 200 EUR order tolerates `min(4, 25)` = 4 EUR. The lesser-of rule is what stops a percentage tolerance from waving through a large absolute difference on a large order — which is precisely where the money is.

- Tolerance applies to price differences, **never to quantity**. Being invoiced for one more unit than was received is not rounding.
- Freight, handling, and surcharges not on the order are outside tolerance by definition; they are either agreed and added to the order, or they are queried.
- Under-invoicing is also a mismatch. It is usually a partial delivery or a split invoice, and treating it as a windfall means paying the balance later without expecting it.

## Approval Thresholds

`approval_threshold` sets the point above which an invoice is not paid on the strength of arriving. A workable ladder, adapted to whatever authority the user actually has:

| Band | Requirement |
|---|---|
| Below threshold, known supplier, matches its history | Filed and scheduled; no approval event |
| Below threshold, new supplier | Supplier established first: identity, tax ID, bank details verified (`validation.md`) |
| Above threshold | Named approval recorded before payment, with the date |
| Well above threshold, or outside budget | Second approver, and the underlying commitment checked against the order or contract |
| Any bank-detail change, any amount | Out-of-band verification, unconditionally (Rule 5) |

Thresholds apply to the **commitment**, not the instalment. Four invoices of 900 EUR against a 3,600 EUR order clear a 1,000 EUR threshold individually and should not — match against the order, not against the invoice in front of you.

## Segregation Of Duties

The one control that actually stops internal fraud, and it costs nothing to state:

- **Whoever can change a supplier's bank details must not be the one who approves payments to that supplier.** When the same person does both, no other control matters.
- **Whoever approves must not be the one who created the purchase order**, above the threshold.
- **The person who receives the goods should not be the only person who confirms receipt** for high-value deliveries.

In a business too small for real separation — and most are — the compensating control is visibility, not process: a monthly review of every bank-detail change and every new supplier added, by the owner, taking ten minutes. `## Due` carries it as a cadence. That review is the whole control, and it works because the fraud it detects depends on nobody ever looking.

## Coding

Assigning the invoice to an account, a cost centre, or a project. Done at filing, never at payment — by payment time the person who knows what it was for has moved on.

- **Account** comes from `categories.md` when the user has a mapping, otherwise the built-in category (`extraction.md`).
- **Project attribution**: a cost to be rebilled gets one line in `~/Clawic/data/projects/<project>.md`, with the invoice number as the reference and a `Rebilled` column. The invoice itself stays in the ledger; copying it into the project file is how two records start disagreeing (`memory-template.md`).
- **Split coding** across projects or accounts: write the split in the ledger row's `Notes` column with the amounts (`split: acme-redesign 420.00, internal 280.00, total 700.00`), and make the parts sum to the total. A split that does not reconcile is worse than no split.
- **Capital versus expense** is a coding decision with multi-year consequences — an asset carries its own VAT adjustment window and its own retention (`countries.md`). Flag anything substantial and durable rather than coding it as an expense by default.

## Recording An Approval

Minimum viable record, in the ledger row's `Notes` column, or in `## Open Items` while the approval is still pending:

`approved by <name>, <date>, against <PO or contract reference>`

- **Approval is recorded before payment, not after.** A record created afterwards documents that a payment happened, which was never in doubt.
- **A verbal approval is recorded the same way**, naming who gave it and when. The record's value is that it exists, not that it is signed.
- **A refusal is recorded too**, with the reason. The invoice becomes `disputed` or is returned, and the reason is what stops the same invoice being approved by someone else next month (`disputes.md`).

## Solo Operators

Most users of this skill are one person, and the controls still apply in reduced form — the fraud does not care how many people are involved:

- **Rule 5 out-of-band verification** is not a team control. It is the single highest-value check in the whole skill and it protects a sole trader exactly as much as a company.
- **A new supplier gets its identity established once** — tax ID checked, and the last four of the account plus the date and method of verification written to `Bank last4` and `Verified` in that supplier's row in `## Suppliers`. Five minutes, once, and every subsequent invoice from them is checkable.
- **The monthly review of bank-detail changes and new suppliers** takes minutes when the supplier table is current, and it is the compensating control for having nobody to segregate from.
- Purchase orders, thresholds, and match tolerances are usually overhead for one person and can be skipped without loss — say so rather than proposing a process nobody will run.

**Write before you finish**: an approval, a refusal and its reason, a split coding, or a match discrepancy goes in the `Notes` column of the invoice's ledger row, with `## Open Items` carrying it while it is unresolved; a project attribution goes as one line to `~/Clawic/data/projects/<project>.md` with the invoice number only; a supplier established for the first time gets its row in `## Suppliers` with the verification date; an approval policy the user states — thresholds, who approves what — is a declaration and goes to `config.yaml`, never to `memory.md` (`memory-template.md`).
