# Budget — Cashflow, Savings Rate, and the Leak Audit

**Before answering**, read `## Money Shape` in `~/Clawic/data/money/memory.md` and `~/Clawic/data/finances/budget.md` if it exists. Rebuilding a budget that already exists loses the sinking funds, which are the part nobody reconstructs from memory.

**Contents:** [The Only Number That Predicts the Outcome](#the-only-number-that-predicts-the-outcome) · [Three Buckets, Not Twenty Categories](#three-buckets-not-twenty-categories) · [Sinking Funds](#sinking-funds) · [Automate the Order, Not the Discipline](#automate-the-order-not-the-discipline) · [The Named Splits](#the-named-splits) · [The Annual Leak Audit](#the-annual-leak-audit) · [Why Budgets Fail](#why-budgets-fail) · [Cutting, in Order](#cutting-in-order)

## The Only Number That Predicts the Outcome

`savings_rate = annual savings ÷ gross annual income`. Savings means money that leaves spending: contributions to investments and pensions including any employer match, principal repaid on debt (not the interest), and cash added to the buffer.

Pick a denominator and never switch. Gross is the default here because it is the figure the independence table in SKILL.md is built on; net inflates the same behaviour by roughly the tax rate, which is how two people compare "savings rates" and reach opposite conclusions.

It predicts the finish date better than investment return does, because it moves both terms at once: saving more raises the numerator and cutting spending lowers the 25× target. That is why a 5-point rise in savings rate outranks a 1-point rise in expected return, and why the fee conversation belongs after this one.

Track two spend figures, not one — they answer different questions:

- **Core monthly spend** — what survives a cut. Sizes the emergency fund and the shock plan.
- **Total monthly spend** — what actually leaves. Sizes the savings rate and the independence target.

## Three Buckets, Not Twenty Categories

Categories fail because they multiply. Buckets do not, because they are defined by behaviour under pressure:

| Bucket | Definition | Behaviour in a cut |
|---|---|---|
| Fixed | Same amount, contractual, cancelling needs notice | Only moves with a renegotiation or a move |
| Variable | Amount is a choice each month | Moves this week |
| Sinking | Known irregular cost, saved monthly | Cannot be cut, only deferred, and deferring is borrowing from a future month |

**Fragility test**: if fixed + sinking exceeds ~60% of net income, there is nowhere for a cut to land, so the plan breaks on the first shock regardless of how large the surplus looks. That is a structural finding — the answer is a fixed-cost renegotiation or a move, not more discipline (`housing.md`).

Cap the category list at what fits the statement lines. A category that never matches a real transaction gets abandoned within two months; the point of the budget is that the plan and the statement can be compared without translation.

## Sinking Funds

Every known irregular cost divided by twelve, saved monthly, held in the buffer account but earmarked. This is the single change that stops the emergency fund from being drained by things that were never emergencies.

`monthly = annual cost ÷ 12`, and for a lumpy replacement: `monthly = replacement cost ÷ expected months of life`.

Standard list to sweep against: insurance premiums paid annually, road tax and vehicle inspection, servicing and tyres, professional fees and subscriptions billed yearly, holidays, gifts and the December cluster, school and childcare cycles, medical and dental out-of-pocket, home maintenance (a common planning figure is ~1% of property value a year — verify it against the actual property, since it varies with age and type), device replacement, pet costs, and the tax bill if income is not taxed at source (`self-employed.md`).

A household that runs sinking funds properly experiences almost no financial emergencies. That is the whole trick.

## Automate the Order, Not the Discipline

The mechanism is what works; the slogan is not.

- Standing transfers dated **payday**, not month-end. What arrives at month-end is a residual and it is always smaller than intended.
- Savings and sinking funds move out of the current account on payday, into a separate institution (`emergency-fund.md`). Money that stays visible gets spent — this is the entire design.
- Bills paid from an account that only ever holds bills, funded by one transfer. The current account then shows spendable money and no arithmetic is needed.
- Minimum payments automated first (ladder step 0); the surplus is manual only if the user wants the friction.
- Every automation gets a date in `finances/budget.md`, because they silently break when a payday date changes.

## The Named Splits

Useful as starting points, dangerous as rules.

- **50/30/20** (Warren) — 50% needs, 30% wants, 20% savings, **on after-tax income**. Applied to gross it overstates the savings by roughly the tax rate. It also breaks where housing is expensive: in a high-rent city needs pass 50% for people doing nothing wrong, and the honest response is to cut the wants share, not to declare the household a failure.
- **Zero-based** — every unit assigned a job before the month starts. Highest control, highest maintenance; best for irregular income and for someone who has never seen where the money goes (`zero-based-budgeting` covers the method in depth).
- **Pay-yourself-first only** — automate the savings figure, leave the rest unbudgeted. Lowest maintenance, works only once fixed costs are known to be safely below income.

Default: pay-yourself-first at `savings_rate_target_pct`, with sinking funds. Escape hatch: switch to zero-based for three months when spending is genuinely unknown or income is irregular, then relax back.

## The Annual Leak Audit

Once a year, in the `## Due` table. Each line is a recurring saving, so an hour here compounds:

| Sweep | What to look for |
|---|---|
| Subscriptions | Anything unused for 60 days; annual renewals whose notice period starts before the renewal date (`finances/subscriptions.md`) |
| Insurance | Loyalty pricing — renewal quotes routinely exceed new-customer quotes for the same cover; re-quote everything (`insurance.md`) |
| Mobile, broadband, energy | Out-of-contract tariffs are the default trap; the retention desk exists for callers |
| Bank and platform fees | Account fees, ATM and FX fees, platform and fund charges (Rule 6) |
| Debt rates | One retention call per card (`debt.md`) |
| Duplicated cover | Travel or gadget cover already included in a card or home policy |
| Direct debits nobody recognises | The classic finding: a service cancelled years ago still charging |
| Tax reliefs unclaimed | Work expenses, allowances, credits for dependants (`taxes.md`) |

Report the result as an annual figure, not a monthly one: "34/month" is ignored, "408 a year, every year" is not.

## Why Budgets Fail

| Failure | Signature | Fix |
|---|---|---|
| Too many categories | Abandoned in month two | Three buckets, categories matching statement lines |
| No sinking funds | Repeated "emergencies" that were all foreseeable | Twelfths, from the list above |
| Budgeting the average month | Every month is over | Budget the floor month, treat the surplus as allocation (`self-employed.md`) |
| No slack line | One unplanned dinner breaks the plan | An explicit unallocated line, 5-10% of variable spend |
| Built on gross income | Consistently 25-40% short | After-tax income, always |
| Two people, one budget, one author | The non-author defects | Both parties present when it is set (`household.md`) |
| Tracking without deciding | Beautiful records, unchanged behaviour | The budget's output is a changed standing order, or it did nothing |

## Cutting, in Order

When the plan needs less spending, work down this list. It is ordered by ratio of money saved to quality of life lost:

1. Fees and rates — bank, platform, insurance, debt (no lifestyle change at all)
2. Unused recurring items — subscriptions, memberships, cover that duplicates
3. Repriceable fixed costs — mobile, broadband, energy, insurance re-quote
4. Substitutions in the largest variable line, usually food — same function, lower price
5. Frequency reductions in discretionary spend, chosen by the user, never assigned
6. Structural change — housing, vehicle, school. Largest by far, and it is a life decision, not a budget line (`housing.md`, `big-purchases.md`)

Cutting from the bottom of this list first is how people conclude budgeting does not work: they gave up something that mattered before renegotiating a tariff that did not.

**Write it down.** The plan, the categories and the sinking funds go to `~/Clawic/data/finances/budget.md` (shared). Income, core spend, total spend and savings rate go to `## Money Shape` in `~/Clawic/data/money/memory.md`, each with its `As of` date. Recurring payments found or cancelled go to `~/Clawic/data/finances/subscriptions.md`. The monthly review date lives in `## Due`, driven by `review_day`. Format in `memory-template.md`.
