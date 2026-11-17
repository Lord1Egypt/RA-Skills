# VAT And Deductibility — What The Invoice Is Actually Worth

Input tax is only recoverable when the document, the purpose, and the timing all hold. Most lost deductions are lost on the document, not on the rule.

**Before deciding any treatment**, read `config.yaml` (`country`, `vat_regime`, `base_currency`) and check `## Boxes` for a treatment artifact covering this supplier or this kind of purchase — a decision made once with an accountant is worth more than a decision re-derived every quarter. Where `vat_regime` is `not-registered`, none of this runs: the invoice total is the cost, VAT included, and the ledger keeps the tax column for information only.

**Contents:** [The Three Conditions](#the-three-conditions) · [Rate Bands](#rate-bands) · [Reverse Charge](#reverse-charge) · [Imports](#imports) · [Partial And Mixed Use](#partial-and-mixed-use) · [Commonly Non-Deductible](#commonly-non-deductible) · [Timing](#timing) · [Foreign Currency](#foreign-currency) · [Special Schemes](#special-schemes) · [Recovering Foreign VAT](#recovering-foreign-vat)

## The Three Conditions

All three, always:

1. **A valid invoice**, carrying every mandatory element and naming the recipient with their tax ID where required (`validation.md`). A till receipt with no recipient fails here in most regimes, however genuine the purchase.
2. **A business purpose.** The purchase serves the taxable activity. Where the link is not obvious from the invoice, the purpose goes in the ledger row's `Notes` column at filing time, naming who and what (`lunch with Marta Ruiz, Acme Legal, contract review`) — reconstructing why a restaurant bill was business two years later is how deductions get denied.
3. **Recorded in the books** within the period the deduction is claimed. The archive is not the book; the ledger row is what makes the claim traceable.

Fail any one and the VAT is not recoverable, even though the cost itself may still be deductible for income tax. The two questions are separate and get separate answers: "can I reclaim the VAT" and "is this an expense".

## Rate Bands

Every invoice is split per band in the ledger (`memory-template.md`), because the return is filed per band and a blended figure cannot be un-blended.

- Standard, reduced, and super-reduced rates vary by country and by product within a country. The invoice states them; do not infer a rate from a category.
- **`0%`, `EX`, and `RC` are three different things** and the return treats them differently: zero-rated is taxable at zero with full recovery, exempt is outside the tax with no recovery and can restrict recovery elsewhere, reverse charge shifts the liability to the recipient. An invoice showing "0.00" without a legend needs the legend before it can be coded.
- Mixed-rate invoices produce one ledger row per band, with the full total on the first row only. Repeating the total on every band double-counts the invoice.
- A rate that is not a rate your country uses on a domestic invoice means the supplier is charging foreign VAT — see Recovering Foreign VAT.

## Reverse Charge

The most common cross-border case and the most common filing error.

- **What it looks like**: an intra-EU B2B supply of services, or a domestic supply under a national reverse-charge rule (construction and certain goods are typical). The supplier invoices without VAT, states the recipient's VAT number, and carries a legend naming the mechanism.
- **What it means**: the recipient self-accounts. The output entry and the input entry are both declared. Where the recipient has full recovery, the net cash effect is zero.
- **The error**: filing it as "no VAT, nothing to declare". The net being zero does not make the entries optional; a missing pair is a filing error that shows up in a cross-check against the supplier's own EU sales listing.
- **Preconditions**: the recipient's VAT number must be valid at the time of supply and must have been given to the supplier. A supplier who charges their local VAT because they were never given a valid number is not making a mistake you can unwind by re-coding the invoice — the correction is theirs.
- Ledger convention: `Rate` = `RC`, `Tax` = 0.00, base in the issued currency, FX cell filled if foreign.
- Intra-EU acquisitions of **goods** work on the same self-accounting principle with their own reporting; the distinction from services matters for which listings the transaction appears in.

## Imports

Goods from outside the customs union arrive with two documents and only one of them is the deduction voucher.

- **The supplier's commercial invoice** is the cost. It carries no recoverable import VAT.
- **The customs declaration** — the document issued on clearance, in whatever national form — is what evidences the import VAT and the duty. Without it, the import VAT is not recoverable, no matter how clearly the supplier invoice shows the goods.
- File both. The ledger row points at the customs document, and the commercial invoice is archived alongside with a suffix (`filing.md`).
- **Duty is a cost, not a tax to reclaim.** It goes into the base of the goods.
- **The courier's disbursement invoice** is a third document: the handling fee is deductible on its own terms, and the import VAT it advanced is only recoverable against the customs document, not against the courier's fee note.
- Postponed or deferred import VAT accounting, where available, changes the mechanics to something closer to reverse charge and removes the cash-flow cost. Whether it applies is a `country` question (`countries.md`).

## Partial And Mixed Use

Where a purchase serves both business and private use, only the business share is recoverable, and the share must be justifiable.

- **Vehicles** are the classic case: several regimes apply a standing presumption of partial business use, rebuttable by evidence in both directions. Applying 100% because the car is "mainly for work" without evidence is the single most reliably challenged deduction there is.
- **Home office**: the deductible share is derived from a defensible measure — floor area, or area plus time — and the same measure is applied every period. Changing the basis between periods invites the whole claim to be reopened.
- **Phone and connectivity**: split by a stated method, and keep the method stable.
- Whatever the apportionment, **record the basis once as an artifact** and reference it, rather than re-deriving a percentage each quarter. The basis is what has to be defended; the arithmetic is not.

## Commonly Non-Deductible

Varies by country, but the recurring set:

| Category | Typical treatment |
|---|---|
| Client entertainment and gifts | Frequently non-deductible for VAT, and capped or disallowed for income tax |
| Meals | Conditional: business purpose recorded, often capped, sometimes only when travelling |
| Passenger vehicles and their running costs | Partial by presumption |
| Purchases with no valid invoice | Not recoverable, full stop |
| Purchases attributable to exempt activity | Not recoverable, and they can reduce the recoverable share of general costs |
| Personal purchases run through a business card | Not deductible, and mixing them makes the whole account harder to defend |

Code these at filing time with `Status: non-deductible` rather than dropping them from the ledger. A cost that exists and is not deductible is a fact; an invoice missing from the archive is a hole.

## Timing

- The right to deduct arises when the tax becomes chargeable, generally on supply, and is exercised in a return. Several regimes then allow a window of years to exercise it late.
- **A late invoice belongs to its own period**, not the current one, when the period is already filed. The options are an amended return or claiming in a later period where the rules allow it — the decision is the accountant's, and the ledger row must show the issue date honestly either way (`period-close.md`).
- **The service period can differ from the issue date.** A December invoice for November service raises a genuine allocation question; the answer follows the chargeability rules of `country`, and once decided for a supplier it goes to `artifacts/treatment-<supplier>.md` with its `## Boxes` line and is applied to every later invoice from them unchanged.
- Cash-accounting schemes, where elected, move the trigger to payment for both output and input tax. Electing one changes the reporting boundary for the whole archive (`period-close.md`, Where Experts Disagree in SKILL.md).

## Foreign Currency

- Store as issued; convert with the rate for the date the tax became chargeable — normally the invoice date (Rule 4). EU regimes generally accept the ECB or the national central bank rate for that date; some also permit a customs rate.
- The rate and its source go in the ledger `FX` cell. A converted amount with no recorded rate cannot be reproduced, and a VAT return that cannot be reproduced is a problem the day it is questioned.
- Use the **same source consistently**. Mixing an ECB rate one quarter and a payment-provider rate the next produces differences that look like errors.
- The payment-date difference is an FX gain or loss. It never changes the invoice, the base, or the tax.

## Special Schemes

- **Margin schemes** (second-hand goods, travel, art): the invoice shows no recoverable VAT and says so in a legend. Trying to recover it is a straightforward error.
- **Flat-rate schemes**: input VAT is generally not recovered individually — the flat rate replaces it. When `vat_regime` is `flat-rate`, invoices are still filed and still archived, but nothing is coded as recoverable, and the archive's job becomes retention and expense evidence.
- **Exempt activities** (insurance, finance, health, education in most regimes) do not carry recoverable input tax, and a business that mixes exempt and taxable activity recovers general costs only in proportion. That proportion is an accountant's calculation and belongs in an artifact, not in a heuristic.
- **Small-business exemptions** below a turnover threshold: the supplier charges no VAT and says so; the recipient has nothing to recover and nothing to self-account.

## Recovering Foreign VAT

VAT charged by a supplier in another country is not recoverable on a domestic return. Two paths exist:

- **A refund claim to the other state**, filed through the domestic authority within an annual deadline, subject to minimum amounts and that country's own deductibility rules. Worth it for real amounts — hotel and conference VAT across a year of travel adds up — and not worth it for a single restaurant bill.
- **Fixing the invoice at source**: for services, giving the supplier a valid VAT number usually moves the transaction to reverse charge and there is no foreign VAT to recover in the first place. This is cheaper than every refund procedure and is the reason a VAT number belongs in every supplier account the user opens.

**Write before you finish**: a treatment decided for a supplier or a class of purchase goes to `artifacts/treatment-<subject>.md` with its `## Boxes` line and, where an accountant decided it, their name and the date; an apportionment basis goes to `artifacts/` the first time it is used; the per-band split and the `Rate` code go into the ledger row at filing time; a non-recoverable finding that changes what to expect from a supplier goes to their row in `## Suppliers` (`memory-template.md`).
