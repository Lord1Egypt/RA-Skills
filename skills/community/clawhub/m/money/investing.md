# Investing — Long-Term Money

**Before answering**, read `## Allocation` and `## Goals` in `~/Clawic/data/money/memory.md`, and `artifacts/investment-policy.md` if `## Boxes` lists it. A written policy exists precisely so that a market move does not get re-litigated as a fresh question.

Scope here is the decision layer: whether to invest at all, in what proportions, at what cost, and what would change it. Choosing the provider, the account and the specific fund is `invest`.

**Contents:** [First, Is This Investable Money](#first-is-this-investable-money) · [Horizon Picks the Asset](#horizon-picks-the-asset) · [Capacity, Tolerance, Need](#capacity-tolerance-need) · [Cost Is the Only Guaranteed Return](#cost-is-the-only-guaranteed-return) · [Diversification, and What It Does Not Cover](#diversification-and-what-it-does-not-cover) · [Lump Sum Versus Averaging In](#lump-sum-versus-averaging-in) · [Rebalancing](#rebalancing) · [Where to Hold What](#where-to-hold-what) · [The Written Policy](#the-written-policy) · [Claims That Sound Like Analysis](#claims-that-sound-like-analysis)

## First, Is This Investable Money

Investable money satisfies all four. Anything failing one belongs to an earlier ladder step:

1. No balance above `high_interest_rate_pct` outstanding (step 3)
2. The buffer is at `emergency_fund_months` (step 4)
3. Nothing this money is needed for inside the horizon in the table below
4. The employer match is already captured (step 1) — nothing here beats an instant 50%

The most common error in the whole domain is answering a fund question for someone who fails point 1.

## Horizon Picks the Asset

| Money needed in | Held as | Because |
|---|---|---|
| Under 2 years | Instant-access cash, short government bills, money-market funds | Certainty is the requirement; there is no return worth a 30% shortfall on a deposit date |
| 2-5 years | Short-duration bonds, term deposits laddered to the date | Duration risk is small and the date is fixed |
| 5-7 years | A partial equity allocation, declining as the date approaches | The transition zone; glide down rather than switch on the day |
| Over 7 years | Equities dominant, per `risk_posture` | Broad equity drawdowns have taken five years and longer to recover in real terms; the horizon has to survive that, not the average |
| No date at all (independence) | Equities dominant with a bond ballast that rises near decumulation | Sequence risk is what a fixed date converts into a real loss (`retirement.md`) |

Default equity share by `risk_posture`, as a starting point rather than a rule: conservative 40-50%, balanced 60-70%, aggressive 80-90%, with the remainder in high-quality bonds. Age-based formulas ("100 minus age") are a crude proxy for horizon and ignore the three inputs below.

## Capacity, Tolerance, Need

Three different questions, and conflating them is how portfolios get abandoned at the bottom:

- **Capacity** — how much loss the plan can absorb without failing. Set by horizon, income stability and the buffer. Objective.
- **Tolerance** — how much loss the person can hold without selling. Set by temperament and experience. Subjective, and only measurable by what they did last time markets fell, not by what they say they would do.
- **Need** — how much return the goal actually requires. If the goal is already funded, taking equity risk is buying a risk you no longer need to hold.

Take the **lowest** of the three. A high-capacity, high-tolerance investor with no need for return should still not carry 90% equities, and a high-need investor with no tolerance will sell at the worst moment regardless of the spreadsheet.

## Cost Is the Only Guaranteed Return

Terminal ratio = ((1 + r − f) ÷ (1 + r))^n (SKILL.md Rule 6). At r = 7%, n = 30 years:

| Annual cost | Terminal balance retained | Lost to cost |
|---|---|---|
| 0.10% | 97% | 3% |
| 0.20% | 94% | 6% |
| 0.75% | 81% | 19% |
| 1.00% | 75% | 25% |
| 2.00% | 57% | 43% |

Count every layer, because they stack: fund ongoing charge, platform or custody fee, advice fee, transaction and spread costs, currency conversion on foreign-denominated holdings, and tax drag from distributions or turnover. A "1% adviser" whose funds charge 0.9% is a 1.9% arrangement, and the table above is the right way to price that conversation before discussing performance.

Cost is knowable in advance. Return is not. That asymmetry is the entire case for starting the analysis here.

## Diversification, and What It Does Not Cover

- Broad market exposure removes the risk of a single company or sector; it does not remove market risk, and nothing does.
- **Home bias** is the default error: a domestic index is a bet that your country's listed companies outperform, taken by someone whose salary, house and pension already depend on that same economy. Some home tilt is defensible for currency-matching of near-term spending; a 100% home portfolio is a concentrated position that feels like prudence.
- **Employer stock is the worst concentration available** — the job, the salary, the pension and the holding all fail in the same event (`income.md`). Cap it at ~10% of investable assets.
- Bonds diversify equities most of the time and not in an inflation shock, when both fall together. That happened recently enough that "bonds are the safe part" needs the qualification.
- Diversification across *fund providers* is not diversification if the funds track the same index; check the holdings, not the names.

## Lump Sum Versus Averaging In

Investing a lump sum immediately has historically beaten averaging it in over 6-12 months in roughly two thirds of periods (Vanguard), for the unglamorous reason that markets rise more often than they fall, so time out of the market usually costs.

The honest framing: averaging in is **regret insurance**, and it has a price — the expected return given up. Offer it explicitly on those terms. It is the right choice when the alternative is that the user does not invest at all, or would sell after an immediate drop; those are real outcomes and worth more than the expected difference.

Regular contributions from salary are not averaging in. They are investing money as it arrives, which is the only option available, and the language should not be confused.

## Rebalancing

- **Bands, not the calendar**: rebalance when an allocation drifts more than ~5 percentage points from target, checked quarterly. Calendar rebalancing trades when nothing has moved; band rebalancing trades when something has.
- Rebalance with **new contributions first** — direct the monthly amount to the underweight asset. It costs nothing in transaction terms and nothing in tax.
- In a taxable account, selling to rebalance realises tax. Weigh it: a 5-point drift is rarely worth a taxable event that a few months of contributions would fix (`taxes.md`).
- Rebalancing is a risk control, not a return enhancer. Claiming a "rebalancing bonus" is not supportable in general, and the correct defence is that it stops the portfolio drifting into a risk level nobody chose.

## Where to Hold What

Asset location — which wrapper holds which asset — is worth real money and costs nothing, but the rules are entirely jurisdiction-specific: which wrappers exist, what they shelter, and whether income and gains are taxed differently. Establish `country` first (Rule 3), and route anything non-obvious to a qualified adviser.

The generic principle that survives translation: **fill tax-sheltered space first, and put the most heavily taxed asset inside it.** Where income is taxed harder than capital gains, income-producing assets go inside the shelter and growth assets outside; where the shelter is unlimited, the question does not arise. Also check whether foreign-domiciled funds carry a punitive local treatment — in several jurisdictions they do, and it dwarfs any fee difference.

## The Written Policy

One page, written before the money is invested, saved as an artifact. It exists to answer questions asked in a falling market, which is the one moment nobody thinks clearly:

- Target allocation and the rebalancing band
- Contribution amount and its automation date
- What would change the plan: a horizon shortening below 7 years, a stated posture change, a goal being funded — and explicitly, **never a market move**
- What happens in a fall of 20%, 30%, 50%, written down as an instruction to the future self
- Any `exclusions` and their reason

A policy written in calm and read in panic is the highest-return page in the domain, and it costs twenty minutes.

## Claims That Sound Like Analysis

| Claim | The honest version |
|---|---|
| "Missing the 10 best days halves your return" | True, and incomplete: the best days cluster within days of the worst, so the finding argues against selling into a fall, not for ignoring horizon or valuation |
| "Past performance is a guide" | Last period's leading fund is a coin-flip for the next; persistence studies find little that survives cost |
| "It's a bad time to invest" | Said in every year that turned out fine and in every year that did not; the answer is horizon (Rule 5), never a forecast |
| "Cash is safe" | Nominally certain, and guaranteed to lose purchasing power at the inflation rate — safety and certainty are different properties |
| "This fund beat the market" | Over what period, against which index, after which costs, and out of how many funds that were launched? |
| "Everyone is buying it" | Popularity is priced in already; it is a description of the price, not a reason for it (`scams.md`) |

**Write it down.** A target allocation, a rebalancing band or a posture change goes to `## Allocation` in `~/Clawic/data/money/memory.md`; the accounts holding it go to `~/Clawic/data/finances/accounts.md`. The one-page policy is an artifact at `~/Clawic/data/money/artifacts/investment-policy.md`, with its `## Boxes` line added in the same turn, and the quarterly rebalance check goes in `## Due`. A decision taken against an alternative — averaging in versus lump sum, hedged versus unhedged — gets a row in `~/Clawic/data/money/decisions/<year>.md`. Format in `memory-template.md`.
