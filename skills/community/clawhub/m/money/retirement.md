# Retirement — The Number and the Withdrawal

**Before answering**, read `## Goals`, `## Allocation` and `## Net Worth` in `~/Clawic/data/money/memory.md` (or `net-worth.md` and `goals.md` if `## Boxes` points there). "Are we on track" is a comparison question and needs the series, not a single reading.

Terminology is jurisdiction-specific and account names do not translate. Establish `country` before naming a wrapper, a state pension age or an access rule (Rule 3); the mechanics below are wrapper-agnostic.

## The Target Is Spending, Not Income

`target = annual spending in retirement × 25` (the inverse of a 4% withdrawal rate). Three consequences people miss:

- The target moves with **spending**, not with salary. Cutting 200 a month of recurring cost lowers the target by 60,000 and raises the savings rate at the same time — the double effect that makes spending reduction the strongest lever.
- Subtract guaranteed income before applying the multiple: `target = (annual spending − state pension − defined-benefit pension − rental or other reliable income) × 25`. A state pension covering half the spending halves the portfolio needed, which is why an estimate of it is the first input, not an afterthought.
- Retirement spending is not today's spending. Commuting, work clothes, mortgage payments and the savings rate itself all stop; healthcare, insurance and time-rich spending rise. Build the figure line by line, and do not assume the standard "70% of final salary" replacement rate — it is an average of other people's lives.

## The 4% Rule, With Its Assumptions Visible

Bengen's finding was that 4% of the starting portfolio, then increased with inflation each year, survived every rolling 30-year period in the US data he tested, with a 50-75% equity allocation and **no fees**. What that does and does not license:

| Assumption | If it does not hold |
|---|---|
| 30-year horizon | Retiring at 50 needs 40+ years; the sustainable rate falls, commonly cited around 3-3.5% |
| No fees | Subtract your total cost (`investing.md`) directly from the rate: a 1% all-in cost turns 4% into 3% |
| US market history | Most other developed markets produced worse worst-cases in the same era; a globally diversified portfolio is the honest input, and the resulting rate is lower |
| Inflation-linked spending, never adjusted | Real retirees cut in bad years. Flexible spending rules — skipping the inflation rise after a down year, or a floor-and-ceiling band — support a higher starting rate than the rigid version |
| Nothing left at the end | Success meant "did not run out". A plan that ends with zero and a plan that ends with a fortune are both "successes" in that data |

Use 4% as an order-of-magnitude sizing tool, state the assumptions, and never present it as a guarantee. For an early or long retirement, size at 3-3.5% and show both numbers.

## Sequence Risk

The same average return produces very different outcomes depending on when the bad years fall. Losses in the first years of withdrawal are permanent, because the units sold to fund spending are never available to recover.

- The danger window is roughly the **five years either side of the stop date**. That is when the portfolio is largest relative to remaining contributions and the first withdrawals begin.
- Defence 1: a cash and short-bond ladder covering 2-3 years of spending, so a falling market is never sold into. Refill it in good years.
- Defence 2: a rising bond allocation into the window, relaxing again afterwards — the "bond tent". Counterintuitive, and it targets exactly the years that matter.
- Defence 3: flexibility. A retiree who can cut 10% of spending in a bad year, or work part-time for two, has more protection than any allocation change provides.
- Accumulation has the mirror property: a crash early in a saving life is a discount, a crash the year before the finish is a delay. Volatility is not risk in year 5 and is very much risk in year 30.

## Which Wrapper Fills First

Generic order — the local names change, the logic does not:

1. Anything matched by the employer, up to the match ceiling (ladder step 1)
2. The wrapper with the largest tax relief at the **current** marginal rate — relief is worth the rate you avoid now against the rate you expect to pay later
3. Wrappers that are tax-free on the way out, especially where the current marginal rate is low and future income is expected to be higher
4. Any wrapper with an employer, state or bonus top-up not covered above
5. Ordinary taxable investing, once the sheltered space is used

The invisible distinction: relief-now wrappers win when today's marginal rate exceeds the expected retirement rate; tax-free-later wrappers win when it is the other way around. Early career, low rate, long horizon usually points to the second. Peak earnings points to the first. Anything else — split contributions and stop optimizing a decision whose inputs are 30 years of unknown tax policy.

## Access Rules and Early Withdrawal

- Every sheltered wrapper trades tax advantage for an access restriction. Money locked until a statutory age is not part of the emergency fund and never appears in the buffer figure (`emergency-fund.md`).
- Early withdrawal typically costs a penalty, plus income tax on the amount, plus the compounding it would have produced — three costs where people count one. A withdrawal at 40 of an amount that would have doubled twice by 70 costs four times the sticker figure in retirement terms.
- Retiring before the statutory access age needs a **bridge**: taxable investments, cash, or reduced work covering the years between stopping and access. Most plans that fail on this detail fail late, when the plan is otherwise sound.
- Defined-benefit pensions: a transfer offer converts a guaranteed inflation-linked income into a pot with market risk transferred to the holder. It is one of the largest and least reversible financial decisions available, and it belongs with a regulated adviser (Red Flags), not with an agent.

## Decumulation Order

Once withdrawals start, the order of accounts affects the tax bill and the longevity of the pot:

- Fill the low-tax band each year from the wrapper that is taxed on withdrawal, even if the cash is not needed — unused low bands are lost annually and never recovered.
- Preserve tax-free space for later, large or lumpy needs (care costs, a property adaptation).
- Take from cash and the bond ladder in falling markets, from equities in rising ones. This is the same sequence-risk defence, run in reverse.
- Manage the total taxable income against any cliff-edge threshold in `country`: a withdrawal that crosses one can be taxed at an effective rate far above the headline (`taxes.md`).
- Review the withdrawal rate annually against the current portfolio value rather than the original one, and adjust spending within a band.

## Are We On Track

Compute it, do not eyeball it: `required monthly = (target − current) ÷ months to date`, then compare with the current contribution. If the gap is large, the four levers, in order of how much they move the answer:

1. Spend less in retirement — moves the target by 25× the annual cut
2. Save more now — moves the numerator and, if it comes from spending, the target too
3. Work longer — adds contributions, shortens the horizon to fund, and delays the withdrawal start; two or three years here typically moves the answer more than a decade of allocation tinkering
4. Take more risk — moves the expected outcome and widens the range of outcomes; it is the weakest lever and the one most often reached for first

Run it in **real terms** (Rule 2): a nominal projection at 3% inflation overstates a 30-year figure by 2.4×.

## The Traps Specific To This Subject

| Trap | Why it fails |
|---|---|
| "One more year" indefinitely | The target was hit and the plan has no stopping rule; write the stopping condition down before it is reached |
| Planning to a single average return | The average is not the experience; use a range and check the bad case |
| Ignoring longevity | Planning to average life expectancy leaves roughly half of people short, and the ones who live longest need the money longest |
| Assuming both partners retire at once | Different ages, different pensions, different access dates — model separately, then jointly (`household.md`) |
| Forgetting the survivor | Household spending does not halve when one partner dies, and one pension may stop entirely; check survivor terms and cover (`insurance.md`) |
| Counting a house as retirement funding | It funds retirement only if it is sold or borrowed against, both of which are decisions with costs and neither of which is automatic (`housing.md`) |
| Excluding care costs | Late-life care is the largest single risk to a retirement plan in most countries; know what `country` covers and what it does not |

**Write it down.** The target, the current position and the monthly figure go to `## Goals` in `~/Clawic/data/money/memory.md`; the derived spending estimate, guaranteed income and stopping condition go to an artifact at `~/Clawic/data/money/artifacts/retirement-plan.md`, with its `## Boxes` line the same turn. The annual on-track check goes in `## Due`; each reading goes in `## Net Worth`. A wrapper choice or a transfer decision gets a row in `~/Clawic/data/money/decisions/<year>.md`. Format in `memory-template.md`.
