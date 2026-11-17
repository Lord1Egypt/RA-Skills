# Reviews — The Cadence That Keeps The Plan Alive

**Before answering**, read the `## Due` table in `~/Clawic/data/money/memory.md` against today's date and state any overdue item in one line — a statement, not a question. Then read `## Net Worth` (or `net-worth.md` if `## Boxes` points there) and `## Money Shape`. A review without the previous readings is a snapshot, and a snapshot answers nothing.

A plan decays. Rates change, subscriptions accumulate, the buffer target rises with rent, and beneficiary forms go stale after a birth. The cadence is what converts a good decision made once into a system.

## The Schedule

Everything below lives in the `## Due` table, with its last-run and next-due dates. `review_day` sets the monthly one.

| Cadence | Review | Time |
|---|---|---|
| Monthly, on `review_day` | Cashflow | 15 minutes |
| Quarterly | Net worth + allocation drift | 30 minutes |
| Annually, in a fixed month | The full audit | 2 hours |
| On a trigger | Whatever the trigger touches | Varies |

Fewer, deeper reviews beat constant checking. Daily balance-watching increases action without increasing quality, and in investing specifically the correlation runs the wrong way (`investing.md`).

## Monthly: Cashflow, 15 Minutes

Not a full audit. Five questions:

1. Did the planned savings transfer actually go out, on the day, in full?
2. Which category missed the plan, and was it a one-off or the new normal? One month is noise; two is a plan that needs changing rather than more discipline.
3. Any new recurring payment appear? Add or remove it in `finances/subscriptions.md`.
4. Any balance or rate change worth recording — a card rate rise, a savings rate cut, a debt milestone?
5. What is due next month that the sinking funds should already cover?

Output: at most one changed standing order. **A review with no possible action is a report, and reports get skipped within three months.**

Two-person households: this is the monthly money conversation, both present, thirty minutes, at a scheduled time (`household.md`).

## Quarterly: Net Worth and Drift, 30 Minutes

`net worth = total assets − total liabilities`, both at current values, on the same date, in `currency`.

- Take the reading on the same date each quarter — quarter end is the obvious choice — because the comparability is the entire value of the series.
- Include: cash, investments, pensions, property at a conservative estimate, and material vehicles. Exclude: the tax reserve, which is not yours (`self-employed.md`), and anything whose value you would not accept from a buyer today.
- Write the composition into the `## Net Worth` row, not only the total: a rising net worth driven entirely by an estimated property value is not the same result as one driven by contributions.
- **The number to watch is contributions plus debt principal repaid, not the total.** Market movement is noise in a single quarter and dominates the total; the part under the household's control is the part worth reviewing.
- Then check allocation drift against the target band; rebalance with new contributions where possible (`investing.md`).

One reading means nothing. Four readings show the direction. Twelve show whether the plan works — which is why the series lives in a box and never gets overwritten.

## Annually: The Full Audit, 2 Hours

Fix the month and keep it. Run in this order, because each step feeds the next:

| Step | What | Detail |
|---|---|---|
| 1 | Re-derive the buffer target | Core spend has moved; `emergency_fund_months` × the new figure (`emergency-fund.md`) |
| 2 | Re-price every fixed cost | Insurance, mobile, broadband, energy, bank fees — loyalty pricing is the default (`budget.md`) |
| 3 | Subscription sweep | Anything unused 60 days; annual renewals whose notice period starts before the renewal date |
| 4 | Debt rates | One retention call per card; check any promotional rate about to revert (`debt.md`) |
| 5 | Savings rate | Recompute against gross; compare to `savings_rate_target_pct` and to last year |
| 6 | Investment costs | All-in: fund, platform, advice, FX. Price it with the fee-drag table (`investing.md`) |
| 7 | Insurance and beneficiaries | Cover still matches the household; beneficiaries updated after every life event (`insurance.md`) |
| 8 | Tax position | Allowances that reset, deadlines, unclaimed reliefs, the prep file (`taxes.md`) |
| 9 | Goals | Still wanted? Still dated? Recompute the monthly figure for each (Rule 4) |
| 10 | On-track check | Retirement target against current position (`retirement.md`) |
| 11 | Estate checklist | Will, power of attorney, document locations, digital access (`household.md`) |
| 12 | Shock playbook | Runway today, and does the cut list still reflect reality (`shocks.md`) |

Report the outcome as annual figures — "412 a year, recurring" — not monthly ones. Monthly savings get dismissed; annual ones get acted on.

## Trigger Reviews

Some events invalidate parts of the plan immediately and should not wait for a date:

| Trigger | Re-check |
|---|---|
| Income change above ~10% | Savings rate, budget, buffer target, cover amounts |
| Job change | Employer match ceiling, benefits ending and starting, pension continuity, notice terms |
| Move, or a rent or mortgage change | The largest budget line, buffer target, the fragility test |
| Birth, marriage, separation, death | Beneficiaries, cover, will, powers of attorney, household structure |
| A debt cleared | Where its payment now goes — the ladder, not lifestyle. This is the highest-value trigger and the most commonly wasted |
| A rate change on any debt or savings account | Payoff order, and whether anything crossed `high_interest_rate_pct` |
| Moving country | Almost everything: tax residency, wrappers, cover, credit file, beneficiaries |
| A windfall | The whole ladder (`windfalls.md`) |

## Making Reviews Survive

- **Same day, same duration, in the calendar.** An unscheduled review is an intention.
- **Compare to the previous reading, never to an ideal.** Progress is the metric; a plan measured against perfection gets abandoned.
- **One action per review, maximum three.** A list of twelve improvements produces zero.
- **Write the outcome down in the same session.** An unrecorded review has to be redone, which is why the next one is skipped.
- Put the *reason* in the `decisions/<year>.md` row alongside the decision. Six months later the reasoning is what is missing, not the number.
- **A review that never says "no change needed" is not being run honestly.** Most quarters, the correct output is to confirm the plan and stop.

**Write it down.** Every run updates `Last run` and `Next due` in the `## Due` table of `~/Clawic/data/money/memory.md`. The quarterly reading goes as one row in `## Net Worth`, never a second row for the same date. Savings rate and spend figures go to `## Money Shape` with their `As of` date. Anything decided goes as a row in `~/Clawic/data/money/decisions/<year>.md`. Balance and rate changes update `~/Clawic/data/finances/accounts.md`; budget changes update `~/Clawic/data/finances/budget.md`. If `## Net Worth` passes ~15 readings, split it to `net-worth.md` by the procedure in `memory-template.md` and add its `## Boxes` line in the same turn.
