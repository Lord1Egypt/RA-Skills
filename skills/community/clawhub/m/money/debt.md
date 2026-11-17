# Debt — What To Clear, In What Order

**Before answering anything about a debt**, read `## Debt Plan` in `~/Clawic/data/money/memory.md` (or `debt-plan.md` if the `## Boxes` index points there) and `~/Clawic/data/finances/accounts.md`. A payoff order proposed without the current rates and balances is a guess, and re-deriving one the user already agreed to wastes the session.

**Contents:** [Priority Beats Rate](#priority-beats-rate) · [The Minimum-Payment Trap](#the-minimum-payment-trap) · [Avalanche, Snowball, and the Honest Gap](#avalanche-snowball-and-the-honest-gap) · [Cut the Rate Before You Cut the Balance](#cut-the-rate-before-you-cut-the-balance) · [Consolidation and Refinancing](#consolidation-and-refinancing) · [Mortgages and Student Loans](#mortgages-and-student-loans) · [Buy Now Pay Later](#buy-now-pay-later) · [Arrears and Collections](#arrears-and-collections) · [When the Arithmetic Does Not Close](#when-the-arithmetic-does-not-close)

## Priority Beats Rate

Order by consequence first, rate second. A 0% arrears balance that ends in eviction outranks a 24% card every time, and this is the single ordering mistake that turns a repayable situation into a crisis.

| Tier | Debts | Ordered by | Consequence of non-payment |
|---|---|---|---|
| 1 — Priority | Rent or mortgage, property tax, utilities, income tax and social contributions, court fines, child maintenance, secured vehicle finance where the vehicle is how you earn | Consequence, never rate | Loss of home, disconnection, enforcement, seizure, loss of income |
| 2 — Rate-ordered | Cards, overdrafts, personal loans, BNPL, car finance on a non-essential vehicle, family loans with a rate | Highest after-tax rate first | Rising cost, credit damage |
| 3 — Deliberately unpaid early | Anything priced below `high_interest_rate_pct` and below the expected real return: a cheap fixed mortgage, a subsidized student loan, a 0% purchase plan running to term | Not paid early on purpose | None — this is a decision, and it goes in `## Debt Plan` with its reason |

Tier 3 exists so the decision is visible. An unwritten "we are not prepaying the mortgage" gets re-argued every quarter.

## The Minimum-Payment Trap

Card minimums are set to be affordable, not to end. Two common formulas, both self-perpetuating:

- **Percentage of balance (2%).** At 22% APR the monthly interest is 1.83% of the balance, so a 2% minimum sends 0.17% to principal — the balance falls about 2% in the first year.
- **Interest plus 1%.** The principal falls by exactly 1% of the balance a month at the start: on 3,000, the first payment retires under 30 of principal.

Both run past 15 years on a typical balance once the floor payment takes over, repaying roughly twice the principal. The fix is arithmetic, not willpower: **fix the payment in currency, never as a percentage.** A payment frozen at today's amount while the balance falls converts the whole structure into a fixed-term loan, and the payoff date becomes computable and datable (Rule 4).

Payoff months at a fixed payment P on balance B at monthly rate i: `n = −ln(1 − iB/P) ÷ ln(1 + i)`. If `iB ≥ P` there is no solution — the payment never clears it, and that is the signal to stop planning and read [When the Arithmetic Does Not Close](#when-the-arithmetic-does-not-close).

## Avalanche, Snowball, and the Honest Gap

Same total payment, different target for the surplus after minimums.

- **Avalanche** — surplus to the highest rate. Minimizes interest. Always the arithmetic answer.
- **Snowball** — surplus to the smallest balance. Closes accounts sooner, which is what predicts finishing for people who have abandoned a plan before.

Quantify the gap rather than arguing it: on a typical three-debt mix (a small high-rate card, a mid-size card, a larger low-rate loan) the lifetime difference is usually in the low hundreds of currency units — less than the cost of one abandoned attempt. Compute both, show the two numbers, and let the user's own track record break the tie. Where the gap is genuinely large — a big balance at a high rate sitting behind a small one — say the number out loud and recommend avalanche.

Hybrid that usually wins in practice: clear anything under one month of surplus first (a fast, visible close), then strict avalanche from there.

## Cut the Rate Before You Cut the Balance

Rate reduction is free money and is skipped almost universally.

| Move | The maths | Watch |
|---|---|---|
| Retention call on a card | A 3-point APR cut on a 4,000 balance is 120/yr for a ten-minute call; issuers hold retention scripts precisely because attrition costs more | Ask for the rate, not a limit increase; a limit increase is the counter-offer they want you to accept |
| Balance transfer to a 0% promo | Break-even in months = fee % ÷ old monthly rate. A 3% fee against a 22% APR (1.83%/month) breaks even in 1.6 months — the fee is almost never the problem | The problem is the revert rate, new spending on the emptied card, and the balance not being cleared by the promo end. Divide the balance by the promo months; if that payment is not affordable, the transfer just relocates the debt |
| Overdraft → personal loan | Overdraft pricing is often the highest rate in the whole balance sheet and the least visible because it has no statement | Only if the account is not re-used as an overdraft afterwards |
| Secured refinance of unsecured debt | Lower rate, longer term, and the house is now collateral | Red Flags: this converts a survivable default into a repossession. Price both paths before anything moves |

## Consolidation and Refinancing

The monthly payment is the number sold; the total is the number that matters.

- Total cost = monthly payment × number of months + fees. Compare that to the total of the existing debts run to their own payoff dates. A consolidation that halves the payment and doubles the term usually raises the total interest even at a lower rate.
- Consolidation only works with a behaviour lock: the cleared cards get closed or frozen. Re-running the balances behind a consolidation loan is the most common way a repayable situation doubles.
- Fees to price in: arrangement fee, early-settlement penalty on the old debt, insurance sold alongside. Ask for the total amount repayable, a figure most jurisdictions require the lender to state.
- Family loans: put the rate and the schedule in writing. Undocumented family debt is the one that survives longest and costs the most in non-financial terms (`household.md`).

## Mortgages and Student Loans

- **Mortgage prepayment** competes with ladder steps 5-7, not with steps 0-4. It wins on arithmetic when the after-tax rate exceeds the expected after-tax real return; it loses on liquidity always — prepaid principal cannot be withdrawn when unemployed, and lenders do not lend to the unemployed (`housing.md`).
- **A fixed mortgage below the inflation rate is being repaid in cheaper money each year.** Prepaying it early is choosing a guaranteed low return over an expected higher one, plus giving up the option value of the cheap fix.
- **Student loans vary more than any other debt class**: income-contingent repayment, write-off after a fixed period, subsidised rates, or ordinary commercial terms — the correct action ranges from "never prepay" to "clear immediately". Establish `country` and the loan's regime before advising anything; a wrong default here can cost years of payments that would have been forgiven.
- Where repayment is income-contingent and written off at a horizon, extra payments are a pure gift unless the borrower will clearly repay in full before that date.

## Buy Now Pay Later

- The dangerous feature is not the rate — most are 0% — it is that four simultaneous plans have no single statement, so total commitment is invisible. List every plan with its dates in `finances/subscriptions.md` alongside recurring payments; it is the same cashflow object.
- Late fees are flat, so on small purchases they are enormous in percentage terms: a 6 fee on a 40 instalment is 15% for a few days.
- Missed BNPL payments are increasingly reported to credit bureaus in many jurisdictions, which surprises borrowers who assumed they were invisible (`credit.md`).

## Arrears and Collections

- **Contact the priority creditor before missing the payment, not after.** Forbearance, payment holidays and hardship arrangements exist and are almost always better than the enforcement path, but they are granted to people who ask early.
- **Never pay a collector before validating the debt in writing**: amount, original creditor, and their authority to collect. Bought debt is frequently mis-recorded.
- **Acknowledging or part-paying an old debt can restart the limitation clock in many jurisdictions.** Establish `country` before recommending any payment on a debt older than a few years — a well-meant token payment can revive an unenforceable debt.
- Settlement offers on charged-off debt are routinely accepted well below face value; get the settlement terms in writing before paying, including that the balance is treated as satisfied.
- In some jurisdictions forgiven debt is taxable income. Flag it and route to `taxes.md`.

## When the Arithmetic Does Not Close

Signals that this stops being an optimization problem, from the SKILL.md Red Flags table: unsecured debt above ~12 months of net income, minimums above ~30% of net income, a card being used to pay another card, or `n` with no solution in the payoff formula above.

Then: stop building plans, name the free statutory or non-profit debt-advice service for their `country`, and set out what formal debt relief would and would not do. Producing an optimistic schedule at that point costs the user the months they still had to act.

**Write it down.** A payoff order agreed, a rate reduced, a debt cleared, or a deliberate decision not to prepay goes to `## Debt Plan` in `~/Clawic/data/money/memory.md` — order, method, and the tier-3 reasons — with balances and rates updated in `~/Clawic/data/finances/accounts.md`. A full plan with dates and projected interest saved is an artifact: `~/Clawic/data/money/artifacts/payoff-plan.md`, with its `## Boxes` line added in the same turn. Format in `memory-template.md`.
