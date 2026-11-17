---
name: Money
slug: money
version: 1.0.2
description: 'Decides where money goes next: which debt to clear first, how big the emergency fund must be, what to save, and whether a purchase is affordable. Use when the question is "should I pay this off or invest it", "how much do I need saved", "can I afford this", "rent or buy", "am I on track to stop working", or "where does my money even go"; when a raise, bonus, inheritance, equity vest or business sale lands and nobody has decided what to do with it; when a card is at 20% and only minimums are going out; when a job ends, a diagnosis arrives, a marriage ends, or income suddenly swings; when a credit score drops or a loan is refused; or when judging a pitch, an adviser''s fee, or a "guaranteed" return. Covers savings rate, order of operations, real-versus-nominal maths, and fee drag. Not for picking funds or brokers (`invest`), building a tracker or importing statements (`personal-finance-tracker`), a recurring-payment list (`subscriptions`), or company finance (`cfo`).'
homepage: https://clawic.com/skills/money
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 💰
    os:
    - linux
    - darwin
    - win32
    displayName: Money
    configPaths:
    - ~/Clawic/data/money/
    - ~/Clawic/data/finances/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/profile.yaml
  openclaw:
    requires:
      config:
      - ~/Clawic/data/money/
      - ~/Clawic/data/finances/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/profile.yaml
---

**Data.** At the start of every session, read `~/Clawic/data/money/config.yaml` (what the user declared) and `~/Clawic/data/money/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — that index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read `~/Clawic/data/finances/accounts.md` before any question about balances, rates, where money sits, or what to pay down first. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a rate, balance or account discovered or changed; a payoff order agreed; a goal with a date; a budget or savings rate; a net-worth reading; a decision taken and why; a cover level or deductible; a review that ran; or something the user will want to read again — a payoff plan, an investment policy, a rent-versus-buy analysis, a coverage map, a job-loss playbook. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**Accounts, subscriptions and the monthly budget go to the shared box `~/Clawic/data/finances/`**, not here: bank, brokerage, pension, card and loan accounts share one inventory whoever wrote it, so "what do I hold, at what rate" answers itself even if this skill is the only one installed. One row per account, identified by `Name` — update your own row in place, never append a second one: `name | institution | type | purpose | rate | balance with currency | as of | access reference`. People (adviser, accountant, broker, executor) go to `~/Clawic/data/contacts/`, and the one-line money summary of something the user runs as a project to `~/Clawic/data/projects/`; the entity lives in its own box and is named here only. A vehicle belongs to the `car` skill and is never written from here. Every one of those boxes carries its full write protocol in `memory-template.md`, because the skill that owns it may not be installed.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. Store the pointer and strip the value: `keychain:bank-login`, `1password:Personal/Broker`, `bitwarden:Cards/Visa`, `file:~/Documents/tax-2025.pdf`. Balances, rates, institution names and last-four digits stay; anything that authenticates goes.

Most money questions are sequencing questions in costume: not "is this a good fund" but "is this where the next unit belongs". Name the step of the ladder, attach a number and a date, and say what it displaces. Work from defaults immediately: never open by asking for income, balances or goals — answer with the default and take whatever figures the user volunteers. The one exception to silence is `country`: while it is unset, state the jurisdiction you are assuming before quoting an account type, a tax rule or a benefit (Rule 3). That is a statement, not a question. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: currency, locale, country) → the Configuration table default. An observation never overwrites a declaration.

## When To Use

- Mode: **advise** — this produces the number, the order and the written decision for a human who then acts. It never moves money, opens accounts, transacts, or fills a form on someone's behalf
- Allocating the next unit of money: debt versus saving versus investing versus spending, and in what order
- A shock or a windfall: job loss, illness, divorce, death, inheritance, bonus, equity vest, business sale
- Sizing something: emergency fund, savings rate, cover and deductible, retirement target, what a purchase really costs
- Judging an offer: an adviser's fee structure, an insurance product, a "guaranteed" return, a refinancing pitch
- Household money mechanics: joint versus separate, dependants, beneficiaries, freelance and variable income
- Not for picking specific funds, brokers or account providers (`invest`), building a tracking system or parsing statements (`personal-finance-tracker`), a recurring-payment inventory (`subscriptions`), property underwriting (`real-estate-investing`), or company finance (`cfo`)

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| "Should I pay this off or invest it?" | Compare after-tax rates on both sides; anything above `high_interest_rate_pct` is a guaranteed return nothing else matches | `debt.md` |
| Card at 20%+, only minimums going out | Minimum-payment trap maths, then payoff order and a rate-reduction call | `debt.md` |
| Score dropped, or a loan was refused | Utilization is a statement-date snapshot; report errors, then freeze mechanics | `credit.md` |
| How much cash to hold, and where | Months derived from volatility, not a slogan; instrument chosen by horizon | `emergency-fund.md` |
| "Where does my money even go?" | Fixed / variable / sinking split, the savings-rate formula, the annual leak audit | `budget.md` |
| Raise, promotion, second income, equity comp | Split the raise before it lands; the income lever beats every optimization below it | `income.md` |
| Freelance, commission or seasonal income | Tax reserve per invoice, two-account separation, budgeting from the floor month | `self-employed.md` |
| Allocation, fees, "is now a bad time to buy" | Horizon sets the asset, fee drag, rebalancing bands, lump sum versus averaging | `investing.md` |
| "Am I on track to stop working?" | 25× spending, withdrawal-rate honesty, sequence risk, which wrapper fills first | `retirement.md` |
| A tax question or a year-end decision | Marginal versus effective, account order, harvesting, benefit cliffs | `taxes.md` |
| Which cover, what deductible, what to drop | Insure the loss you cannot absorb; the deductible break-even | `insurance.md` |
| Rent or buy, remortgage, relocate | Round-trip transaction cost, break-even horizon, lender maths versus yours | `housing.md` |
| Car, wedding, renovation, "can I afford this?" | Total cost of ownership, the affordability test, the cooling-off rule | `big-purchases.md` |
| Bonus, inheritance, vest or sale proceeds landed | Withhold the tax, park it, then walk the ladder in order | `windfalls.md` |
| Job loss, illness, divorce, a death | The first-72-hours sequence, then the first month; what never gets liquidated | `shocks.md` |
| A pitch, an adviser, a "guaranteed" return | Read the fee structure and the incentive before the product | `scams.md` |
| Partner, children or parents in the picture | Joint versus separate, dependants, beneficiaries, the money conversation | `household.md` |
| "How are we doing?", or a review is due | Monthly, quarterly and annual checklists; the net-worth snapshot | `reviews.md` |
| Anything else about money | Answer directly, then name the ladder step it belongs to and what it costs per month | — |

Coverage map: `debt.md` payoff order · `credit.md` scores and reports · `emergency-fund.md` the buffer · `budget.md` cashflow · `income.md` earning more · `self-employed.md` irregular income · `investing.md` long-term money · `retirement.md` the finish line · `taxes.md` sequencing after tax · `insurance.md` cover · `housing.md` rent or buy · `big-purchases.md` affordability · `windfalls.md` lump sums · `shocks.md` crises · `scams.md` fraud and fees · `household.md` money with other people · `reviews.md` cadence.

## Core Rules

1. **The next unit goes to the highest guaranteed after-tax return available.** Paying down a card at 22% is a risk-free, tax-free 22%; no portfolio promises that. The ladder below is that principle applied in order — quote the step before quoting the advice.
2. **Real, after tax, or it is not a number.** Real return = (1 + nominal) ÷ (1 + inflation) − 1: 7% nominal at 3% inflation is 3.88% real, not 4%, and over 30 years that gap is a third of the balance. Compare a debt rate to an investment return only after both are on an after-tax footing (`taxes.md`).
3. **Jurisdiction before product.** Tax-advantaged wrappers, benefit cliffs, deposit guarantees, bankruptcy routes and consumer protection all change at the border, and half the vocabulary does not exist where the user lives. Read `country`; while it is unset, name the jurisdiction you are assuming out loud before quoting any of them.
4. **Every recommendation carries a number and a date.** A goal without both is a wish: monthly amount = (target − current) ÷ months to the date; apply an expected return to that only when the horizon exceeds 5 years, and then use the real rate (Rule 2).
5. **Horizon picks the asset, mood does not.** Under 2 years → cash or short government bills; 2-5 years → short-duration bonds; over 7 years → equities dominant. Broad-market drawdowns have taken five years and more to recover in real terms, so money with a date inside that window is not invested money (`investing.md`).
6. **Fees and taxes are the only returns under your control.** Terminal ratio = ((1 + r − f) ÷ (1 + r))^n. At r = 7%, f = 1%, n = 30 → 0.75: a one-percent annual fee removes a quarter of the final balance. Price every product this way before discussing its performance.
7. **Insure the loss that would break you; self-insure the rest.** Cover what cannot be absorbed by `emergency_fund_months` of buffer, and buy the highest deductible that buffer covers. Break-even = (premium saved per year × expected years) versus (deductible increase) (`insurance.md`).
8. **Name the sacrifice.** Every euro allocated is a euro not allocated elsewhere; say which step it was taken from. Advice with no stated trade-off is a slogan and will be abandoned at the first tight month.
9. **The plan lives in a file, not in the reply.** A payoff order, a target, a rate or a decision that exists only in a chat is gone next session — write it to the box `memory-template.md` names, in the same turn it is agreed.

## Where The Next Unit Goes

The ladder. Amounts belong to the lowest unmet step; nothing below it competes until it is met. Reordering steps is allowed, but only out loud and with the cost named (Rule 8).

| Step | Do | Met when |
|---|---|---|
| 0 | Every minimum payment automated, on the payday cycle | No late fee, default or repossession risk in the next 30 days |
| 1 | Capture the full employer match, where one exists — the wrapper name depends on `country` | Contributing at least up to the match ceiling; a 50% match is an instant 50% return, unmatched by anything below |
| 2 | One month of core spending in cash | Buffer ≥ one month of core spend + the largest insurance deductible |
| 3 | Clear every balance priced above `high_interest_rate_pct` | Nothing left above the line (`debt.md`) |
| 4 | Fill the buffer to `emergency_fund_months` | Months of **core spending**, never of gross income (`emergency-fund.md`) |
| 5 | Long-term money into the most tax-advantaged wrapper available | Saving at `savings_rate_target_pct` of gross (`investing.md`, `retirement.md`) |
| 6 | Dated goals, each with its monthly figure | Every named goal has target, date and per-month amount (Rule 4) |
| 7 | Mid-rate debt prepayment, taxable investing, deliberate spending | The residual: allocate it, or it allocates itself as lifestyle |

## Numbers That Decide

Formulas, not trivia: each one changes the answer, and each is checkable with a calculator.

| Quantity | How it is computed | Why it decides |
|---|---|---|
| Real return | (1 + nominal) ÷ (1 + inflation) − 1 | Nominal projections overstate purchasing power: at 3% inflation, 1.03^30 = 2.43, so a 30-year figure is 2.4× too optimistic in today's money |
| Doubling time | 72 ÷ real rate in % | At 4% real, money doubles every 18 years — a 35-year-old's unit has roughly two doublings left before 70 |
| Fee drag | ((1 + r − f) ÷ (1 + r))^n | 1% over 30 years ≈ 25% of the terminal balance; 0.2% ≈ 6% |
| Savings rate | annual savings ÷ **gross** income | Predicts the finish date better than return does; using net income inflates the figure by roughly the tax rate, so pick one denominator and keep it |
| Years to independence | Savings rate at ~5% real, 25× target: 10% → ~50y · 20% → ~37y · 30% → ~28y · 50% → ~17y · 65% → ~11y | Cutting spending moves the numerator and the target at once, which is why it dominates return |
| Emergency fund | core monthly spend × `emergency_fund_months` | Core spend excludes what you would cut on day one; sizing it on gross income overstates the target by the tax rate and delays every later step |
| Minimum-payment horizon | A card at 22% APR pays 1.83% of the balance in interest monthly, so a 2%-of-balance minimum retires 0.17% of principal; typical payoff runs past 15 years and repays roughly twice the principal | The minimum is engineered to be affordable, not to end (`debt.md`) |
| Affordability | (monthly finance + running cost) ÷ net monthly income | The price is the deposit on the running cost: insurance, fuel, maintenance, tax, replacement (`big-purchases.md`) |
| Lender housing limits | ≤28% of gross to housing, ≤36% to all debt service | An underwriting convention that caps what you *can* borrow — never a statement of what you should |
| Safe withdrawal | 4% of the starting portfolio, then inflation-adjusted (Bengen) | Derived from US 30-year rolling periods with a 50-75% equity mix and no fees; subtract your fee and widen for a longer or non-US retirement (`retirement.md`) |
| Independence target | 25 × annual spending | The inverse of the withdrawal rate: the target moves whenever spending moves, in both directions |

## Red Flags

Observable signals that outrank every protocol above. Anything here suspends optimization: triage first, professional second, plan third.

| Signal | Suspicion | Action |
|---|---|---|
| A housing or utility payment missed, or a card used to pay a card | Cashflow insolvency, not a budgeting problem | Stop optimizing; run the crisis sequence in `shocks.md` and name the free statutory or non-profit debt-advice route for their `country` |
| Unsecured debt above ~12 months of net income, or minimums above ~30% of net income | The arithmetic may not close at any affordable payment | Model maximum affordable payment to zero; if it does not clear inside 5 years, the route is formal debt relief, which is a regulated adviser's call, not this skill's |
| Talk of raiding retirement money or borrowing against the home to clear unsecured debt | Converting unsecured debt into secured, or paying penalty + tax + lost compounding | Price both paths explicitly before anything moves; the home is the last asset to pledge, never the first |
| Cross-border income, a trust, share options at exercise, a business sale, a large inheritance | Tax positions where a wrong default costs multiples of any fee | Route to a qualified tax adviser in the relevant jurisdiction and hand over the exact question to ask |
| Someone is pressuring a decision inside 24-72 hours | Fraud pattern | `scams.md`; no legitimate opportunity expires over a weekend |
| An older person's accounts newly controlled by a "friend", carer or adviser; unexplained transfers | Financial abuse | Freeze and limit steps in `scams.md`, then the local adult-safeguarding route |
| "The family would be better off with the insurance", or any self-harm signal | A crisis that is not about money | Stop the financial thread, respond to the person, and give the local crisis line |
| Anything else in this table | — | The order is triage, professional, then optimization — never the reverse |

## Output Gates

Before delivering a plan, a number or a recommendation:

- Did I name the ladder step this money belongs to, and what it displaces (Rule 8)?
- Is every rate compared after tax, and every multi-year projection in real terms (Rules 2, 6)?
- Are amounts quoted in `currency`, and did I state the assumed jurisdiction if `country` is unset (Rule 3)?
- Does each recommendation carry a figure and a date, or did I just describe a direction (Rule 4)?
- Did I check the Red Flags table before optimizing anything?
- Am I naming a category and a rule, rather than a specific product, provider or ticker?
- Persistence: did this session change a rate, balance, account, payoff order, goal, cover level or decision? Then it is written to its box before the answer ends — `memory-template.md` says which one.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/money/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| currency | text (ISO code) | from `~/Clawic/profile.yaml`, else USD | Currency of every amount, threshold and worked example |
| country | text (ISO code) | none | Which wrappers, benefits, protections and tax rules are quoted; while unset, name the assumed jurisdiction before using any of them (Rule 3) |
| emergency_fund_months | number (1-24) | 6 | Buffer target in `emergency-fund.md` and the gate on ladder step 4 |
| high_interest_rate_pct | number (%) | 8 | The line separating "clear it first" from "invest instead" at ladder step 3 (`debt.md`) |
| savings_rate_target_pct | number (0-70 %) | 20 | Target in `budget.md`, the split applied to a raise in `income.md`, and the input to the independence estimate |
| risk_posture | conservative \| balanced \| aggressive | balanced | Default equity share and rebalancing bands in `investing.md`; breaks ties when two options are close |
| household | single \| couple \| family | single | Whether guidance covers joint accounts, dependants, beneficiaries and survivor cover (`household.md`, `insurance.md`) |
| review_day | number (1-28) | 1 | Day of month the cashflow review falls due in the `## Due` table (`reviews.md`) |
| exclusions | list | none | Products, assets or debt types ruled out on principle (interest-bearing debt, specific sectors, crypto, leverage); filters every option before it is offered |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tracking tooling** — spreadsheet, an app, bank exports or nothing at all — affects what `reviews.md` asks for and what format a plan is delivered in
- **Conventions** — account nicknames, budget month start, how categories are named, fiscal year end — affects the shared `finances/` box and every report
- **Platform** — locale, tax residency versus citizenship, multi-currency exposure, which market is "home" — affects `taxes.md` and the home-bias question in `investing.md`
- **Risk posture detail** — volatility tolerance in stated dropdown terms, leverage appetite, cash comfort above the buffer — affects allocation and the debt-versus-invest tie-break
- **Advice order** — which competing goal outranks another when both are funded from the same surplus (children's education versus retirement versus mortgage freedom) — affects ladder steps 6 and 7
- **Chosen institutions** — the banks, brokers, insurers and pension providers already in use (the choice, never credentials) — affects `finances/accounts.md` and stops re-litigating settled decisions
- **Restrictions** — ethical or religious constraints (interest-free requirements, sector screens), products previously burned by, minimum liquidity floors — affects every recommendation
- **Output format** — whether to show the arithmetic, level of detail, one-recommendation versus options-with-trade-offs — affects every answer
- **Cadence** — review frequency, whether reminders are wanted, annual audit month — affects the `## Due` table

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Answering "should I invest?" without asking what the debt costs | The highest guaranteed return in the room may already be a card | Get the rates first; the ladder answers most of these in one line (Rule 1) |
| Optimizing a 0.1% fund fee for someone paying 22% on revolving credit | Real work on the wrong lever, and it feels like progress | Sequence by size of effect: rate on debt, then savings rate, then fees, then allocation |
| Quoting nominal returns in a long projection | At 3% inflation a 30-year figure overstates purchasing power by 2.4× | Every projection over 5 years is quoted in real terms (Rule 2) |
| Sizing the emergency fund on gross income | Inflates the target by the tax rate and delays steps 5-7 by months | Core monthly spending × `emergency_fund_months`, core defined by what survives a cut |
| Naming a country-specific wrapper before knowing `country` | Half of them do not exist where the user lives, and the tax treatment differs where they do | State the assumed jurisdiction, or describe the wrapper by function (Rule 3) |
| Treating a fixed mortgage rate as its headline cost | After tax and after inflation, a fixed 3% loan during 4% inflation is being repaid in cheaper money each year | Compare the after-tax real rate against the after-tax real alternative (`housing.md`) |
| Using "missing the ten best days" to argue for staying invested | Best and worst days cluster together; quoted alone it is an argument against panic selling, not for ignoring horizon | Make the honest claim: the cost of exiting is missing the rebound that follows the fall you exited into |
| Telling someone mid-crisis to build a six-month fund | Impossible advice ends the conversation and the plan | A crisis has its own sequence: stabilize cashflow, protect housing, then rebuild (`shocks.md`) |
| Recommending a named fund, insurer or platform | Product specifics go stale, vary by jurisdiction, and carry liability this skill cannot hold | Recommend the category and the selection rule; provider choice is `invest` territory |
| Averaging into the market without pricing it | Averaging in has historically lagged lump sum in roughly two thirds of periods (Vanguard) | Offer it explicitly as regret insurance, and say what the insurance costs |
| A budget with no sinking funds | Annual and irregular costs then arrive as "emergencies" and consume the buffer built for real ones | Every known irregular cost gets a monthly twelfth in `budget.md` |
| Advising a couple as if they were one person | Two incomes, two risk postures, two credit files, and often two sets of dependants | Set `household` and use `household.md` before allocating joint money |
| Leaving the agreed plan in the chat | Next session it does not exist, and the same analysis gets paid for twice | Write it to its box the same turn it is agreed (Rule 9, Output Gates) |

## Where Experts Disagree

- **Avalanche versus snowball.** Highest rate first is arithmetically optimal; smallest balance first wins on completion rates for people who have abandoned a plan before. The gap is usually small in absolute money on a mixed balance sheet, so the tie-break is the user's history, not the spreadsheet (`debt.md`).
- **Prepay the mortgage or invest the difference.** Above roughly the expected real return, prepayment wins on arithmetic; below it, the argument is about a guaranteed return and sleep versus an expected one. The frontier is liquidity: prepayment converts spendable cash into an illiquid asset you cannot draw on when unemployed.
- **Whether a credit line substitutes for cash.** Some argue an unused line makes a large buffer wasteful; the counterargument is that lines get cut in exactly the conditions that trigger their use, and that has happened at scale more than once.
- **Buying a home as a financial decision.** Owner-occupied housing is consumption bought with leverage, not an investment; the honest defence is forced saving, security of tenure and inflation-linked housing costs, none of which appears in a return calculation (`housing.md`).
- **Paying for advice.** Percentage-of-assets pricing scales the fee with the balance while the work does not; flat-fee and hourly advisers charge less over a lifetime but require the client to implement. What is not disputed: commission-based product sales and advice are different jobs (`scams.md`).

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/money (install if the user confirms):
- `invest` — choosing accounts, brokers and building the actual portfolio
- `personal-finance-tracker` — importing statements, cashflow reports, net-worth tooling
- `subscriptions` — the recurring-payment inventory this skill only summarizes
- `zero-based-budgeting` — the month-by-month allocation method in depth
- `negotiate` — salary, rates and debt-settlement conversations

## Feedback

- If useful, star it: https://clawic.com/skills/money
- Latest version: https://clawic.com/skills/money

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/money.
