# Payments — Money Out

When to pay, what it costs to pay early or late, how a payment gets recorded, and what to do with partial payments, credit notes, and refunds.

**Before answering anything about what is owed**, read the current `ledger/<year>.md` (unpaid rows are those with an empty `Paid` column) and `## Open Items` in `memory.md`. A payables answer computed from anything else is a guess.

**Contents:** [What Is Owed Right Now](#what-is-owed-right-now) · [The Discount Decision](#the-discount-decision) · [Prioritizing A Payment Run](#prioritizing-a-payment-run) · [Recording A Payment](#recording-a-payment) · [Partial Payments](#partial-payments) · [Credit Notes And Refunds](#credit-notes-and-refunds) · [Overpayment And Double Payment](#overpayment-and-double-payment) · [Late Payment](#late-payment) · [Payment Methods](#payment-methods)

## What Is Owed Right Now

The answer is a table, always with the same shape, and always with its boundary stated:

| Supplier | Number | Total | Due | Days to due | State |
|---|---|---|---|---|---|

- **Due date, not issue date**, is the sort key. An older invoice with 60-day terms is not more urgent than a newer one due on receipt.
- Exclude `disputed`, `duplicate-of`, and `credited-by` rows from the payable total, and say how many were excluded. A payables number that silently contains a disputed invoice is the number someone pays.
- Exclude prepaid and direct-debit suppliers from the action list, but not from the total — the money is committed either way.
- Say what the list excludes: invoices not yet received (`## Open Items`) are real commitments that no ledger row represents yet.

## The Discount Decision

`2/10 net 30` is a financing offer, and its price is knowable (SKILL.md Rule 8):

```
APR = (d / (1 − d)) × (365 / (net_days − discount_days))
```

| Terms | Working | APR | Verdict |
|---|---|---|---|
| 2/10 net 30 | (0.02/0.98) × (365/20) | 37.2% | Take it unless cash is genuinely short |
| 1/10 net 30 | (0.01/0.99) × (365/20) | 18.4% | Usually take it |
| 2/10 net 60 | (0.02/0.98) × (365/50) | 14.9% | Depends on the cost of capital |
| 1/15 net 45 | (0.01/0.99) × (365/30) | 12.3% | Usually not, unless cash is idle |
| 3/5 net 30 | (0.03/0.97) × (365/25) | 45.2% | Take it |

The comparator is the user's actual cost of capital — the rate on their credit line or the return on cash they would otherwise hold — not a feeling about whether 2% is a lot. The reason this looks like free money and is not: taking a 37.2% APR discount while carrying a balance at 8% is correct; taking it while overdrawing at 45% is not.

Discounts are forfeited by a day. When one is taken, `Paid` takes the date the money left and the ledger row's `Notes` column takes the amount actually paid and the difference (`paid 87.71 EUR, 2/10 discount 1.79 EUR`) — a year of 2% discounts on real volume is a number worth being able to state, and it is only statable if each one was written down.

## Prioritizing A Payment Run

When everything cannot be paid at once, in order:

1. **Anything that stops if unpaid.** Hosting, telecom, insurance, anything with a same-week cutoff. The cost of a lapse dwarfs the invoice.
2. **Discounts still inside their window**, when the APR clears the cost of capital.
3. **Anything already late**, oldest first, and the supplier most likely to escalate first among equals.
4. **Statutory or contractual interest exposure** — some jurisdictions accrue late-payment interest automatically in B2B.
5. **Everything else by due date.**
6. **Nothing under dispute, and nothing with an unverified bank-detail change** — those are not late, they are held, and the difference should be communicated to the supplier so the hold does not read as delinquency (`disputes.md`).

A payment run is prepared, never executed autonomously: the output is a list with amounts, accounts, and references, and the user moves the money.

## Recording A Payment

The `Paid` column takes the **date the money left**, not the date it was scheduled and not a boolean. That single choice is what makes cash-basis reporting possible later (`period-close.md`).

- Payment confirmations and bank lines fill an existing row; they never create one (Rule 7).
- Use the supplier's payment reference. A payment with the wrong reference is a payment the supplier cannot match, and it produces a dunning notice for an invoice that was paid weeks earlier.
- Foreign-currency payment: the ledger keeps the invoice-date rate (Rule 4). The difference against the rate on the payment date is an FX gain or loss and goes in the ledger row's `Notes` column with its sign (`FX loss 3.20 EUR at payment`) — it never changes the invoice amount, the base, or the tax.
- Bank fees on an international transfer are a separate cost, not a reduction of the invoice. A supplier who receives less than the invoice total because of intermediary fees still has an unpaid balance, and that is how a 12 EUR residual becomes a dunning notice a year later.

## Partial Payments

- The row stays open with the amount paid and the balance left in the ledger row's `Notes` column (`partial 500 EUR 2026-04-02, balance 618 EUR`); `Paid` fills only when the balance reaches zero. A half-paid invoice shown as paid is the most expensive rounding error in this file.
- Instalment plans agreed with a supplier: the schedule goes in the `Notes` column of the supplier's row in `## Suppliers`, not as separate invoices. There is one invoice; there are several payments.
- A residual under about one currency unit, left by rounding or fees, is written off in the ledger row's `Notes` column with its amount and cause (`write-off 0.14 EUR, intermediary fee`), because an unexplained missing cent is indistinguishable from an unpaid balance.

## Credit Notes And Refunds

Three different things that people call the same thing:

| Instrument | What it does | Ledger treatment |
|---|---|---|
| Credit note | Reverses all or part of an issued invoice | Its own row, negative amounts, `Status: credit-note for <number>`; the original row becomes `credited-by <its number>`. Original amounts are never edited |
| Corrected invoice | Replaces the original entirely, new number | New row; the original becomes `superseded-by <number>`. Both files stay in the archive |
| Refund | Money coming back | A payment event on the credit note's row, not a new negative invoice |

- A credit note carries its own VAT and belongs in the period it was **issued**, which is often not the period of the invoice it credits. Netting a credit note against an earlier period's invoice is a filing error (`vat.md`).
- A credit note against an unpaid invoice reduces what is owed; against a paid one, it creates a receivable from the supplier, which is worth tracking in `## Open Items` because suppliers do not chase themselves.
- A credit note with no reference to an original is not a credit note; it is an invoice with a negative sign and the supplier needs to reissue it properly.

## Overpayment And Double Payment

The failure Rule 3 exists to prevent, and the recovery when it happens anyway:

1. Confirm it is a double payment and not two genuine invoices with the same amount — the ledger check is by identity key, never by amount.
2. Ask the supplier for a refund rather than a credit against future invoices, unless the relationship is ongoing and the amount is small. A credit at a supplier you stop using is money gone.
3. Record it in `## Open Items` until it is resolved, with the amount and the date. Nothing else is watching for it.
4. Write what let it through into the `Notes` column of the supplier's row in `## Suppliers`: a duplicated number, an invoice paid from two channels, a re-issue mistaken for a new invoice. That note is the only thing that stops the second occurrence.

## Late Payment

- In EU B2B, late-payment interest and a fixed recovery cost generally accrue by statute once the term expires, without a reminder being required. Being unaware of the term does not stop the clock.
- A dunning notice for an invoice that is in the ledger as paid means the payment did not match on the supplier's side: the reference, the account, or the amount. Check those three before assuming the supplier is wrong.
- A dunning notice for an invoice **not** in the ledger is a genuine finding: either the invoice never arrived (`suppliers.md`) or it was never filed. Both need the original before anything is paid — paying against a reminder is paying against a document that is not an invoice.
- Repeated lateness with the same supplier is a terms problem, not a discipline problem. Renegotiating to terms that match the user's actual cash cycle costs one conversation and removes the recurring cost.

## Payment Methods

| Method | What it changes here |
|---|---|
| Bank transfer | Bank details are the fraud surface (Rule 5); the reference is what matches the payment |
| Direct debit | The money leaves whether or not the invoice arrived — cadence tracking is mandatory for these suppliers (`suppliers.md`) |
| Card | Statement lines are not invoices (Rule 7); the invoice still has to be collected, usually from a portal |
| Payment platform | The platform's own fee is a separate deductible cost with its own invoice, and it is one people never collect |
| Cash | Needs a receipt naming the recipient to be deductible at all, and several jurisdictions cap deductible cash payments (`countries.md`) |

**Write before you finish**: a payment fills the `Paid` column of its ledger row; a discount taken, a partial payment and its balance, a write-off, or an FX difference goes in that row's `Notes` column; a credit note gets its own negative row and updates the original's status; a refund still owed, a double payment, or a disputed hold goes to `## Open Items`; a change in terms, an instalment schedule, or what let a double payment through goes to the supplier's row in `## Suppliers` (`memory-template.md`).
