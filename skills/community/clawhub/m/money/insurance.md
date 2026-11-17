# Insurance — Cover, Deductibles, and the Gaps

**Before answering**, read `artifacts/coverage-map.md` if `## Boxes` lists it, plus `## Situation` and `## Goals` in `~/Clawic/data/money/memory.md` (household shape, dependants, buffer size). Cover recommended without knowing what already exists is how people end up paying twice for the same risk.

## The Principle That Decides Everything Here

**Insure the loss you cannot absorb; self-insure the rest.** Insurance is a transfer of catastrophic risk at a premium above the expected loss — the insurer's margin and costs guarantee that, on average, buying insurance loses money. That is fine and it is the point: the average is irrelevant when the tail is ruin.

It follows directly that:

- Losses smaller than the emergency fund should be self-insured. Buying cover for them is paying a margin to avoid an outcome the household can already absorb.
- Losses that would end the household's plan must be insured however unlikely they are.
- The premium spent on small-loss cover is the premium not available for the large-loss cover that is often missing.

| Risk | Absorbable from `emergency_fund_months`? | Default |
|---|---|---|
| Long-term inability to work | No — it removes the income permanently | Insure. Usually the most underbought policy there is |
| Death with dependants | No | Insure, term only |
| Serious illness costs, where `country` does not cover them | No | Insure |
| Liability for injury or damage to others | No — legally uncapped in most systems | Insure, and cheaply |
| Home destroyed or uninhabitable | No | Insure the rebuild, not the market value |
| Car write-off | Depends on the car's value against the buffer | Comprehensive while the car matters; third-party only once its value is below the buffer |
| Phone, laptop, appliance | Yes | Self-insure |
| Travel disruption on a cheap trip | Yes | Self-insure; medical cover abroad is a separate question and is usually not |
| Extended warranty on anything | Yes | Never. Priced far above expected loss and duplicated by statutory rights in many jurisdictions |

## Deductibles: The Break-Even

Buy the highest deductible the buffer covers comfortably. The arithmetic:

`worth raising the deductible when: annual premium saved × expected years between claims > increase in deductible`

Worked: raising a deductible by 500 saves 120 a year, and claims run about once every eight years → 960 saved against 500 extra paid per claim. Raise it, and hold the 500 in the buffer (`emergency-fund.md`, which is why the largest deductible is part of the buffer sizing).

Two conditions: the deductible must be affordable **on the worst day**, and it must be affordable per claim, not per year — two claims in a year means paying it twice in some policies.

## Life Cover, Sized

Only needed if someone depends on the income or would inherit a debt they cannot service.

`sum assured = debts to clear + (annual support needed × years of dependency) + one-off costs (funeral, education, relocation) − existing cover − liquid assets`

- **Term, not whole-of-life.** Term is a multiple cheaper for the same face amount at working age because it expires before the claim becomes likely. Whole-of-life policies bundle an investment with a high-cost wrapper; the investment part belongs in `investing.md` where its cost is visible.
- Term length runs to the end of dependency: the youngest child's independence, or the mortgage end date, whichever is later.
- Cover both partners, including one who is not earning: replacing unpaid childcare and household work has a real market price (`household.md`).
- Level term for income replacement; decreasing term is cheaper and only fits a repayment mortgage whose balance falls in step.
- **Employer death-in-service cover disappears with the job**, and jobs end at exactly the wrong times. Never count it as permanent cover.

## Income Protection, The Underbought One

The probability of being unable to work for six months during a career is materially higher than the probability of dying during it, and the financial effect is often worse because the expenses continue alongside the lost income.

Terms that decide whether a policy pays anything:

- **Definition of incapacity**: own occupation (pays if you cannot do *your* job) is materially better than any occupation (pays only if you cannot do *any* job). This single term is worth more than the premium difference.
- **Deferred period**: how long before it pays. Match it to sick pay plus the buffer — a longer deferred period is a large premium saving that the buffer already covers.
- **Guaranteed versus reviewable premiums**: reviewable is cheaper now and repriced later, usually as the risk rises.
- **Benefit escalation**: a level benefit loses a third of its purchasing power over 30 years at 3% inflation.
- Critical-illness cover pays a lump sum on a defined list of diagnoses; it is not income protection and does not substitute for it. Read the list, because the list *is* the product.

## Property, Contents, and Underinsurance

- Insure the **rebuild cost**, not the market value. They diverge widely, and in either direction: a flat in an expensive city can be worth far more than the cost to rebuild it, while an old rural house can cost more to rebuild than it would sell for.
- **Underinsurance is punished proportionally** in most markets: declare 70% of the true value and the insurer may settle 70% of any claim, including small ones. This is the most common and least understood reason a valid claim pays less than expected.
- Re-value after renovations, and index the sum insured — building costs move faster than general inflation in most periods.
- High-value single items usually need specifying separately; a general contents limit contains a per-item cap that will not be discovered until the claim.
- Check exclusions actively: flood, subsidence, escape of water, unoccupancy beyond a stated number of days, working from home, letting a room. Each has ended a claim that the policyholder assumed was covered.

## Liability, The Cheapest Cover There Is

Third-party injury and damage claims are uncapped in most legal systems and are the one loss that can exceed every asset a household holds. Personal liability is usually bundled into home cover at a low limit; raising the limit or adding an umbrella policy typically costs a small amount per year for a large multiple of cover. Check the limits actually held rather than assuming the bundle is adequate.

## Buying, Renewing, Claiming

- **Re-quote everything annually.** Renewal pricing in many markets exceeds new-customer pricing for identical cover; loyalty is charged for, not rewarded. The annual leak audit exists for this (`budget.md`).
- Never let cover lapse to shop — arrange the new policy to start when the old one ends.
- **Never mis-state anything on an application.** Non-disclosure, including things that feel irrelevant, is the standard route to a refused claim, and the discovery happens at the claim.
- Cancel duplicated cover deliberately: travel and gadget cover inside a bank account or card, breakdown cover inside a car policy, legal expenses inside home cover. Duplicated cover pays once.
- Claim process: notify inside the stated window, document with photographs and receipts before anything is repaired or discarded, and keep a dated log of every call, reference number and deadline in an artifact at `~/Clawic/data/money/artifacts/claim-<kebab>.md` — a refused claim is argued on that timeline. Where a claim is refused, the internal complaints route and then the statutory ombudsman or equivalent in `country` are free and are used far too rarely.
- Store policy references as pointers, never as full policy numbers or portal logins: `file:~/Documents/home-policy.pdf`, `keychain:insurer-portal`.

## The Review Triggers

Cover is set once and then goes wrong quietly. Re-check the map on any of these, and annually in `## Due`:

marriage or separation · a child · a death in the household · a house move or purchase · a renovation · a job change or going self-employed · a new dependant such as a parent · retirement or a pension crystallising · a major asset bought or sold · moving country · a debt cleared or a new one taken

Two things that break on those events and are missed most often: **beneficiary designations**, which in many systems override a will and are simply not read by the executor's process, and **cover written in trust or its local equivalent**, which decides whether a payout lands outside the estate and how fast it reaches the family.

**Write it down.** The full picture — policy type, insurer, sum assured, deductible, term, renewal date, exclusions that matter, and the gaps deliberately left open — goes to an artifact at `~/Clawic/data/money/artifacts/coverage-map.md`, with its `## Boxes` line added in the same turn. Renewal and review dates go to `## Due`; premiums go to `~/Clawic/data/finances/budget.md` as fixed or sinking lines. A decision to drop or add cover gets a row in `~/Clawic/data/money/decisions/<year>.md`. An open claim gets its own artifact at `~/Clawic/data/money/artifacts/claim-<kebab>.md` — dated log, reference numbers, deadlines — with its `## Boxes` line the same turn, and the next deadline in `## Due`. Beneficiary and estate items go to `artifacts/estate-checklist.md` (`household.md`). Format in `memory-template.md`.
