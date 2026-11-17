# Emergency Fund — Sizing It, Holding It, Using It

**Before answering**, read `## Goals` and `## Money Shape` in `~/Clawic/data/money/memory.md` (target, current level, core monthly spend) and the savings rows of `~/Clawic/data/finances/accounts.md`. "Three to six months" quoted at someone who already has a written target is a wasted turn.

## Size It From The Person, Not The Slogan

The buffer exists to absorb the gap between an income stop and the next income, plus the deductibles of everything insured. Derive the months; do not recite them.

Start at **3**, then add and subtract:

| Factor | Adjustment |
|---|---|
| Single income supporting the household | +3 |
| Dependants | +2 |
| Self-employed, commission-based, or seasonal income | +3 (and see `self-employed.md`) |
| Specialist role, small local job market, or a hiring cycle measured in quarters | +3 |
| Notice period and statutory redundancy pay that actually applies | −1 per two months of guaranteed post-exit income |
| Meaningful statutory unemployment cover in `country` | −1 to −2, only if eligibility is real for this person |
| Health cover with a high deductible or significant out-of-pocket exposure | + the largest annual out-of-pocket, in months |
| Second earner with a stable, separately-employed income | −2 |

Floor 3, ceiling 12 unless the household owns the business that pays it, where 12-18 is defensible because the income and the asset fail together. Record the derived number as `emergency_fund_months` in `config.yaml` only if the user accepts it — otherwise it stays an observation in `## Goals`.

**The base is core monthly spending, never gross income.** Core spend is what continues after a cut on day one: housing, utilities, food, transport to work, insurance premiums, minimum debt payments, childcare. It typically runs 55-75% of total spending, so sizing the target on gross income overstates it by roughly the tax rate plus the discretionary share — often double — and delays every ladder step behind it by a year or more.

Target = core monthly spend × months. Recompute it at the annual review: the target rises with rent and falls when a debt clears, and a target set three years ago is now wrong in both directions.

## Where It Sits

Access is the product feature being bought. Yield is a bonus, and reaching for it is how buffers become unavailable in the week they are needed.

| Tranche | Instrument | Rule |
|---|---|---|
| First month | Instant-access savings at a different institution from the current account | Different institution, so an account freeze or a card fraud lock does not take both. Same-day access, no notice |
| Months 2 to target | Instant-access or a short notice account; a money-market fund or a short government bill ladder where those are simple to hold in `country` | Nothing with a lock-up longer than the notice you can survive |
| Never | Equities, crypto, long bonds, anything with an exit penalty, anything in the employer's stock | The buffer is needed precisely when these are down and the employer is the reason |

Practicalities that decide the answer more than the yield: does a withdrawal settle same-day or in three days; is there a per-year withdrawal limit; is the money visible enough to be raided for a holiday, or separate enough to be forgotten. A buffer in the same view as the current account gets spent.

Deposit guarantees are per institution per depositor and the ceiling differs by `country`. A large buffer in one institution can exceed it — split before that, not after.

## What Counts As An Emergency

An emergency is **unexpected, necessary, and urgent**. Two out of three is a budgeting problem.

| Event | Buffer? | Why |
|---|---|---|
| Job loss, income stop | Yes | The event the fund exists for |
| Medical or dental necessity, insurance deductible | Yes | Unexpected, necessary, urgent |
| Boiler, roof, essential vehicle repair | Yes if unplanned; no if the item was known to be failing | A known-failing boiler is a sinking fund, not an emergency (`budget.md`) |
| Annual insurance premium, road tax, school costs | No | Known and dated: sinking fund |
| A trip, a wedding you were invited to a year ago, a sale | No | Foreseeable is the opposite of unexpected |
| An "investment opportunity" | No | Also see `scams.md` |

## Using It, Then Rebuilding It

Using the fund is a success, not a failure — that is the transaction it was built for. What breaks households is the aftermath.

1. Use it, and say what happened in one line in `## Goals`.
2. **Cut before rebuilding.** The event that emptied it often changed the income; rebuilding from the old budget fails.
3. Rebuilding returns to **ladder step 4** immediately: it outranks investing and outranks extra debt payments above the minimums, and it does not outrank step 3 debt above `high_interest_rate_pct`.
4. Set the monthly figure and the date (Rule 4): monthly = (target − current) ÷ months.
5. If it was emptied by something insurable that was not insured, that is a coverage gap — fix it in `insurance.md` before rebuilding, or the same event will empty it again.

## The Arguments Against Holding One

Worth stating honestly, because a user has heard them:

- **"Hold a credit line instead."** Lines are withdrawn in the conditions that trigger their use — issuers cut limits during recessions and after a missed payment elsewhere. A line is a supplement to a buffer, never a substitute.
- **"Cash loses to inflation."** It does: 6 months of core spend at 3% inflation costs about 1.5% of a year's core spend annually in purchasing power. That is the premium for not force-selling assets or borrowing at 22% during an income stop, and it is cheap insurance at that price.
- **"Pay the card first, it costs 22%."** Correct above the buffer's first month, which is why step 2 stops at one month and step 3 clears high-rate debt before step 4 finishes the buffer. The ladder already encodes this argument.
- **"Keep it in the offset mortgage account."** Legitimate where offset accounts exist: it earns the mortgage rate tax-free and stays accessible. It fails if drawing it requires the lender's consent, which is exactly when consent will not come.

**Write it down.** The derived target, the current level and the monthly figure go to `## Goals` in `~/Clawic/data/money/memory.md`; the account holding it goes to `~/Clawic/data/finances/accounts.md` with its rate and `As of` date. If the user accepts a months figure as their standing preference, it is a declaration: write `emergency_fund_months` to `config.yaml`. Format in `memory-template.md`.
