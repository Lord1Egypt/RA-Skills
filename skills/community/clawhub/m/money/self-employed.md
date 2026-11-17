# Self-Employed — Irregular Income, Reserves, and Rates

**Before answering**, read `## Money Shape` and `## Situation` in `~/Clawic/data/money/memory.md` and the reserve and business accounts in `~/Clawic/data/finances/accounts.md`. Freelance advice given against an employee's assumptions is wrong in almost every step.

Everything in this file also applies to commission-only sales, seasonal work, gig work as a main income, and a salaried person with a material side business.

## Two Failures, Both Fatal, Both Preventable

1. **Spending the tax.** Income arrives gross. Money that is already owed to a tax authority sits in the same account as money that is spendable, so it gets spent, and the bill arrives after it is gone. This is the single most common way an otherwise profitable freelancer ends up borrowing at 22%.
2. **Budgeting the average month.** Averages hide the trough. A year that averages 4,000 a month but contains two months at 900 breaks a household budgeted at 4,000 — the two bad months arrive before the good ones have been saved.

## Account Structure

The structure does the work that discipline cannot:

| Account | Holds | Rule |
|---|---|---|
| Business receiving | Every payment received | Nothing is paid from here except transfers to the three below |
| Tax reserve | Reserve percentage of every payment, moved the day it lands | Separate institution if possible. This money is not yours and is never counted in net worth |
| Business operating | Costs, tools, software, professional fees | Business costs never touch the personal current account, whatever the legal form |
| Personal salary | A **fixed monthly transfer** to the personal current account | The fixed transfer is the point: it converts irregular income into a salary the household can budget |

The fixed transfer is set at the **floor month**, not the average: take the lowest three months of the last twelve, and pay that. Surplus stays in the business receiving account as a buffer, and is swept by the ladder once the buffer reaches target.

## The Tax Reserve

`reserve % = marginal income tax rate + social contributions rate + (sales tax collected, if the regime makes you hold it)`

The rate is jurisdiction-specific: establish `country` before quoting one, and route anything unusual to a qualified adviser (`taxes.md`). Three rules that hold everywhere:

- Move the reserve **per payment received**, not monthly and never quarterly. A percentage of every incoming payment, on the day it lands.
- Sales tax or VAT collected on behalf of the authority is not revenue at any point. Where the regime requires collection, it is held in the reserve from arrival.
- The first year is the dangerous one in regimes with payments on account: the first bill can arrive as the previous period's tax **plus** an advance on the next, so the first reserve target is larger than the steady-state one. Reserve as if it were, and refund the surplus to yourself later.

Under-reserving is discovered exactly when cash is tightest. Over-reserving costs a little interest and is corrected in an afternoon.

## Setting the Rate

Employees compare gross salary to gross fees and conclude freelancing pays double. It does not, and the arithmetic is the argument that gets rates raised.

`required day rate = (target annual income + business costs + benefits you now buy yourself + tax and contributions) ÷ billable days`

Billable days are the term everyone gets wrong. From 260 working days, subtract holiday, public holidays, sickness, admin, sales and marketing, unbilled revisions, and the gap between contracts. **Sustained billable utilization for a solo professional is commonly 55-70%** — call it 140-180 billable days a year, and derive the rate from that, not from 260. The benefits an employer used to buy — pension contribution, income protection, health cover, paid leave, paid sick leave, equipment — are now line items in the rate.

Pricing rules that matter more than the rate itself:

- Price the outcome where possible, the day where not, the hour last. Hourly billing caps income at the ceiling of a day and penalizes getting faster.
- Raise rates on new clients first; the existing book reprices at renewal with notice, not by surprise.
- A client above ~30% of revenue is an employer with none of the protections. Treat concentration as a risk to be reduced, and size the buffer for the day that client leaves.

## Cashflow and Getting Paid

- **Deposit up front** — 30-50% for project work, or the first month in advance for retainers. It filters non-payers before the work, which is where filtering is free.
- Invoice the day the work is delivered. Payment terms start from the invoice date, so an invoice sent two weeks late is paid two weeks late.
- Short terms, stated: 14 days is normal for small suppliers. Long terms are a request for free credit and can be declined.
- Escalation ladder, on a schedule and without emotion: reminder at term, statement at +7, formal demand at +14 with the statutory late-payment interest most jurisdictions grant, then the small-claims or collection route. Applying it consistently changes which supplier gets paid first.
- Track outstanding invoices as a number: `days sales outstanding = receivables ÷ (annual revenue ÷ 365)`, kept as a dated row in `## Money Shape` in `~/Clawic/data/money/memory.md` so the trend is visible across sessions. Above ~45 days, the collection process is the problem, not the clients.

## The Buffer Is Bigger Here

Self-employment adds +3 months in the `emergency-fund.md` sizing table, and the reason is compounding: the income stops, the pipeline stops with it, and the recovery takes as long as a sales cycle. Where the household also owns the business assets, 12-18 months is defensible because the income and the asset fail together.

Distinguish three pools and never merge them: the **tax reserve** (not yours), the **business buffer** (covers a slow quarter and business costs), and the **household emergency fund** (covers the household). A single pot means a slow quarter eats the tax money.

## What Nobody Buys For You Anymore

| Gap | Why it bites | Action |
|---|---|---|
| Income protection / disability cover | No sick pay, and a solo income has no redundancy | Usually the highest-value policy a freelancer can buy (`insurance.md`) |
| Retirement contributions | No employer match, no automatic enrolment, no default | A standing order on the fixed salary date, at `savings_rate_target_pct` (`retirement.md`) |
| Professional indemnity / liability | One claim can exceed a year of income | Often contractually required; check before signing |
| Health cover | Depends entirely on `country` | Price it into the rate |
| Paid leave | Unpaid time off is a cost of the year | Already inside the billable-days calculation above |

## Legal Form and Bookkeeping

The choice between sole trader, company and local equivalents changes tax, liability and administrative load, and the right answer flips with income level and `country` — route the decision to a qualified adviser once profit is material (Red Flags). Two things hold regardless:

- Keep business and personal money separate from day one, whatever the legal form. Reconstructing a mixed year costs more in fees than the separation ever costs in effort.
- Keep the receipts as they happen, in one place, and note where that place is in `~/Clawic/data/money/artifacts/tax-prep.md`. A deduction with no evidence is not a deduction, and this is the single largest avoidable overpayment freelancers make (`taxes.md`).

**Write it down.** The reserve percentage, the fixed monthly transfer figure, the floor month, the day rate and the latest days-sales-outstanding reading go to `## Money Shape` in `~/Clawic/data/money/memory.md`, each with its date; the account structure goes to `~/Clawic/data/finances/accounts.md`, with the tax reserve marked as not-yours so it is excluded from net worth. Tax deadlines and payment-on-account dates go to `## Due`. A rate calculation or a client-concentration plan worked through in the session is an artifact at `~/Clawic/data/money/artifacts/<kebab-name>.md`, with its `## Boxes` line added the same turn. Format in `memory-template.md`.
