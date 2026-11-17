# Suppliers — The Other Party

One supplier, one identity, whatever they call themselves this month. Also: what to expect from them, when to notice they went quiet, and when a price rise happened without anyone announcing it.

**Before touching a supplier**, read `## Suppliers` in `~/Clawic/data/invoices/memory.md` (or `~/Clawic/data/invoices/supplier-book.md` if `## Boxes` points there). Every rule below is a comparison against what is already stored; the table is the memory, not the invoice.

**Contents:** [Normalization](#normalization) · [The Supplier Row](#the-supplier-row) · [Cadence And Missing Invoices](#cadence-and-missing-invoices) · [Chasing](#chasing) · [Price Rises](#price-rises) · [Terms](#terms) · [Recurring Charges And The Shared Box](#recurring-charges-and-the-shared-box) · [People At Suppliers](#people-at-suppliers) · [Ending A Supplier](#ending-a-supplier)

## Normalization

The same company arrives as `HETZNER ONLINE GMBH`, `Hetzner Online GmbH`, `Hetzner`, and `hetzner.com`. Four spellings is four rows in a naive ledger and four wrong answers to "what did Hetzner cost".

- **Canonical name is short and human**: what the user calls them. `Hetzner`, not `Hetzner Online GmbH`. It appears in filenames, ledger rows, and reports.
- **Every other spelling is an alias** on the same row. A new spelling is never a new row.
- **The tax ID is the identity**, not the name (Rule 3). Two companies with similar names and different IDs are two suppliers; one company with two names and one ID is one supplier.
- **Legal name changes and acquisitions keep the row** when the tax ID persists. When the tax ID changes, it is a new supplier and the old row gets an end date and a pointer to the successor — the history of what was paid to the old entity must stay attached to the old entity.
- **Marketplaces and resellers are their own supplier**, not the brand sold through them. The invoice comes from the marketplace, the deduction hangs on the marketplace's tax ID, and filing it under the brand makes it unverifiable.
- **A person invoicing as a sole trader** is a supplier row here and, if there is also a relationship to manage, a contact row in the shared box. The company data does not belong in `contacts/`.

## The Supplier Row

| Column | What it holds | Why it is not derivable from the ledger |
|---|---|---|
| Supplier | Canonical name | The ledger uses it; something has to define it |
| Tax ID | Identity key | — |
| Aliases | Every spelling seen | Recognition on the next invoice |
| Category | Default category for their invoices | Stops the category being re-derived monthly |
| Cadence | Expected frequency and day (`monthly, day 1`; `annual, March`; `irregular`) | The absence check has nothing to compare against otherwise |
| Terms | `net 30`, `prepaid`, `2/10 net 30`, `direct debit` | Drives scheduling and the discount clock |
| Bank last4 | Last four of the account last paid to | The whole basis of the Rule 5 check |
| Verified | Date and method the bank detail was confirmed | A stored detail nobody ever verified is not a baseline |
| Notes | Parsing quirks, portal URL, dispute history pointer | — |

Never store the full account number, and never a portal password (`memory-template.md`, Secrets).

## Cadence And Missing Invoices

An invoice that never arrives costs a deduction and is invisible, because nothing generates an alert about an absence. This is the check that pays for the whole supplier table.

```
overdue if today > expected_day + grace, and no invoice from that supplier in the period
grace: 7 days (monthly) · 14 days (quarterly) · 30 days (annual)
```

Run it on the `## Due` cadence, monthly by default. When one fires, in this order:

1. **Check the portal.** Suppliers routinely stop emailing and keep publishing; this resolves a good share of them at zero cost (`capture.md`).
2. **Check the mail folder and spam.** Sender or filter changes are the second-most common cause.
3. **Check whether the service ended.** A missing invoice from a cancelled service is not missing; the supplier row gets an end date and the shared subscriptions row gets deleted.
4. **Then chase.**

Suppliers whose cadence is `irregular` are excluded from the check entirely — an absence carries no information for them, and including them produces noise that trains the user to ignore the whole report.

Direct-debit suppliers are the highest-risk group: the money leaves without anyone looking, so nobody notices the invoice never came. Any direct-debit supplier gets an explicit cadence, always.

## Chasing

- **Ask for the document, not for an explanation.** "Could you resend invoice(s) for <period> to <address>" resolves faster than a question about why it did not arrive.
- **Reference what is known**: period, expected amount, the previous invoice number. A supplier's billing desk searches by number and by account, not by narrative.
- **Escalate on the second miss, not the first.** One missing invoice is a mail failure; two consecutive is a billing-configuration problem on their side, and that is a different request to a different person.
- **The deduction has a deadline.** Chasing has to conclude before the period the invoice belongs to is filed, or the invoice lands in a later period and the reconciliation carries an explanation forever (`period-close.md`).
- Record the chase date in `## Open Items`. An unchased "missing" that has been sitting for three months is not being tracked, it is being ignored.

## Price Rises

A price rise is a correct invoice for the wrong amount — validation flags it as an anomaly, and it is not a dispute (`validation.md`).

- Compare in the **issued currency**. A foreign-currency supplier whose local price never moved will look like a rise every time the exchange rate does.
- Distinguish three causes before reacting: a tariff change (their price list moved), a volume change (you used more), and a plan change (someone upgraded). Only the first is a price rise, and only the first is worth a conversation.
- A rise on a recurring service updates the row in `~/Clawic/data/finances/subscriptions.md` in the same turn — that box exists so a year of small rises is visible as one number rather than twelve invisible ones.
- Contractual indexation clauses raise prices annually on a fixed month. Once seen, that month goes in the `Notes` column of their row in `## Suppliers` and the rise stops being a surprise every year.

## Terms

| Term | Reading |
|---|---|
| `net 30` | Full amount due 30 days from the invoice date — check whether the supplier counts from issue or from receipt, they differ |
| `2/10 net 30` | 2% off if paid within 10 days; the APR of taking it is in `payments.md` Rule 8 |
| `due on receipt` | No credit period; a hard deadline in practice only when the supplier enforces it |
| `EOM 60` | 60 days from the end of the invoice month, which is up to 30 days more than `net 60` |
| `prepaid` / `direct debit` | Already paid or about to be; the invoice documents rather than requests |
| Nothing stated | Statutory default applies and varies by jurisdiction; in EU B2B the ceiling for commercial payment terms is set by the late-payment directive |

Terms live on the supplier row, not re-read from every invoice. When an invoice states terms that differ from the row, the invoice wins for that invoice and the difference is a question for the supplier.

## Recurring Charges And The Shared Box

The second time a supplier bills the same thing on a cadence, it is a standing commitment and gets a row in `~/Clawic/data/finances/subscriptions.md` — shared with every skill that asks "what am I paying monthly" (`memory-template.md` has the full format, identity key, and scale cut).

- **Identity is the service name**, with the account in parentheses when one provider bills two accounts separately.
- **Read before adding.** If the row is there, update it in place; never a second row for the same service.
- **Amounts carry their currency inside the value** (`41 EUR`), because rows written by other skills arrive in other currencies and someone will sum the column.
- **Delete the row when the service ends** and note the date. A subscriptions list that only grows is the reason people pay for things they cancelled.
- **Foreign columns win**: match the header that already exists, add anything extra in the last column, never rewrite it, and never touch a row this skill did not write.

The individual invoices stay in the ledger. The shared box holds the commitment, not the history — duplicating the history there is how two skills start disagreeing about the same number.

## People At Suppliers

A named human — the billing contact who issues corrections, the account manager who approves credits — goes in `~/Clawic/data/contacts/contacts.md`, keyed by email, with the supplier named in their context. The company stays here. Duplicating the company into `contacts/` is the most common way two skills end up contradicting each other about the same entity.

Where a phone number came from goes in that person's `Context` column in `~/Clawic/data/contacts/contacts.md` (`number from the 2024 engagement letter`). Rule 5 verification depends on the number predating the suspicious invoice, and a number of unknown provenance is worth nothing at the moment it matters.

## Ending A Supplier

1. Set an end date in the supplier row; do not delete it. The ledger references it for as long as retention runs.
2. Delete the row in `~/Clawic/data/finances/subscriptions.md` and note the closure date.
3. Remove the cadence, so the absence check stops firing.
4. Check for a final invoice, a pro-rated refund, or a credit note still to come — the last invoice from a supplier is the one most often never filed, because nobody is watching for it any more.

**Write before you finish**: a new supplier, a new alias, a corrected tax ID, a changed cadence or terms, a verified bank detail, or an end date goes to `## Suppliers` in `memory.md` (or `~/Clawic/data/invoices/supplier-book.md` past the split); a recurring commitment or its price change goes to `~/Clawic/data/finances/subscriptions.md`; a named person goes to `~/Clawic/data/contacts/contacts.md`; a chase or a missing invoice goes to `## Open Items`; a supplier quirk long enough to need explaining goes to `artifacts/supplier-<name>-parsing.md` with its `## Boxes` line (`memory-template.md`).
