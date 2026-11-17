# Taxes — Sequencing, Cliffs, and the Records

**Before answering**, read `country` in `~/Clawic/data/money/config.yaml` and `## Situation` in `~/Clawic/data/money/memory.md` (residency, filing status, income sources). Tax advice given against the wrong jurisdiction is worse than no advice, because it is confidently wrong.

This file covers the tax *reasoning* that changes a money decision. It does not compute anybody's liability, and it never replaces a qualified adviser where the Red Flags table says otherwise: cross-border income, trusts, share options at exercise, business sales, large inheritances.

## Marginal Versus Effective

The distinction behind most bad tax intuitions.

- **Marginal rate** — the rate on the next unit earned. It decides whether a raise, an extra job, a deductible contribution or a realised gain is worth it.
- **Effective rate** — total tax ÷ total income. It describes the year. It decides nothing.

Consequence: in a normal progressive system, **a raise never leaves you with less money.** Only the amount above the threshold is taxed at the higher rate. Anyone who says otherwise has either met a benefit cliff (below) or is repeating folklore.

Use the marginal rate for every forward-looking comparison in this skill: after-tax debt cost, the value of a deductible contribution, the real return on a taxable holding, the worth of a second income.

## Benefit Cliffs Are The Real Trap

Cliffs are where the folklore is actually true: a threshold at which a benefit, credit or allowance is withdrawn, producing an effective marginal rate far above the headline one — sometimes above 100% at a hard cliff, where one unit of extra income costs more than one unit.

Common shapes, present in most systems under different names:

| Shape | Effect |
|---|---|
| Tapered allowance | An allowance withdrawn at a rate per unit of income above a threshold, stacking on top of the ordinary rate |
| Means-tested support withdrawn on a taper | Combined effective rates commonly above 60-70% for a band of income |
| Hard eligibility cutoff | Childcare support, a health subsidy, a fee waiver disappearing entirely one unit over |
| Household-level thresholds | A second earner's first unit taxed at the household's combined rate, not at a starting rate |

The action is the same everywhere: find the thresholds that apply in `country`, and where income lands just above one, look at whether a deductible pension contribution, a charitable gift, or timing income into another year moves it back below. This is one of the few places where a single hour of arithmetic is worth thousands.

## Timing Is The Lever An Individual Actually Has

Rates are fixed; the year an item falls in usually is not.

- **Allowances that reset annually are use-it-or-lose-it.** Sheltered contribution room, tax-free gain allowances, gift allowances — unused is gone in most systems, so the last weeks of a tax year are a deadline, not a formality. Put the date in `## Due`.
- **Realise gains across tax years** to use more than one annual allowance where one exists: sell part in December and part in January where the year boundary falls there.
- **Defer income into a lower-rate year, accelerate deductions into a higher-rate one.** Relevant at a job change, a career break, parental leave, the first year of self-employment, and retirement.
- **Bunch deductible items into one year** where a threshold or standard deduction means small annual amounts produce no relief.
- Where employment income is taxed at source and other income is not, the second is where the surprise bill comes from (`self-employed.md`).

## Loss Harvesting, Carefully

Selling a loss to offset a gain is real, and it is oversold.

- The benefit is a **deferral**, not a saving, in most cases: the replacement holding has a lower cost base, so the gain reappears later. It is worth the time value of the deferred tax, plus a genuine saving where the loss offsets income taxed at a higher rate or where the eventual gain falls in a lower-rate year.
- Every jurisdiction has an anti-avoidance rule against selling and repurchasing the same asset within a window (30 days is the common length, and some regimes look at connected persons and accounts too). Breaking it disallows the loss and turns the exercise into pure cost.
- Never let the tax outcome pick the portfolio. A worse holding chosen to preserve a small loss offset costs more over a decade than the offset was worth.

## Records, Deadlines, and the Prep File

The largest avoidable overpayment is not a missed strategy, it is a deduction with no receipt.

Standing list, adapted to `country`:

- Income documents from every source, including foreign accounts and platforms
- Deductible items: professional fees, work-from-home costs, equipment, mileage, training, charitable gifts, some childcare and medical
- Contribution certificates for every sheltered wrapper
- Cost-base records for every asset: purchase price, dates, costs, corporate actions. **Missing cost-base data means the gain gets computed as if the base were zero** — an entirely self-inflicted loss, and unrecoverable years later
- Dates of residence changes, and days spent in each jurisdiction where residency depends on a day count
- Retention period: most systems require several years past filing; keep them for the longest window that applies

Filing and payment deadlines, including any payment on account, go in the `## Due` table. Penalties for late filing are usually fixed and immediate, which makes them the most expensive avoidable cost per minute in the domain.

## Where Tax Changes the Money Answer

| Decision | Tax term that flips it |
|---|---|
| Pay debt or invest | Compare after-tax rates: deductible interest lowers the debt's real cost, taxable returns lower the investment's (`debt.md`) |
| Which wrapper first | Relief now at the current marginal rate versus tax-free later at the expected future rate (`retirement.md`) |
| Which asset in which account | Whether income and gains are taxed differently, and whether foreign-domiciled funds are penalised (`investing.md`) |
| Take the bonus or the equity | Income at vest versus gain at sale, and whether withholding covers the marginal rate (`income.md`) |
| Sell or hold the property | Main-residence relief, holding-period rules, and what a rental period does to them (`housing.md`) |
| Take the lump sum or the income | Almost always a tax question wearing a lifestyle costume (`retirement.md`) |
| Gift now or leave it | Lifetime gift allowances versus estate treatment, and the clock some systems run on gifts before death (`household.md`) |

## Rules That Hold Everywhere

1. **Never let the tax tail wag the dog.** A bad decision with a good tax outcome is a bad decision. Tax is a modifier on the ranking, not the ranking.
2. **The rate you save is the rate you avoid.** A deduction is worth the marginal rate, not the face amount — a 1,000 deduction at a 30% marginal rate is worth 300.
3. **Sheltered space is a renewable resource that does not accumulate.** Unused room in most systems disappears each year, which makes it the one deadline worth an annual reminder.
4. **A scheme marketed as a tax saving, with a fee attached, is a product.** Aggressive schemes have a long record of being unwound retrospectively with interest and penalties (`scams.md`).
5. **Residency is not citizenship, and it is not where the post arrives.** Anyone moving, working remotely across a border, or holding foreign accounts needs the day-count and reporting rules for `country` checked by a professional before the year ends, not after.

**Write it down.** The standing document list, the deadlines, the deductions specific to this person and the cost-base gaps go to an artifact at `~/Clawic/data/money/artifacts/tax-prep.md`, with its `## Boxes` line added the same turn. Filing, payment and allowance-reset dates go to `## Due`. Residency, filing status and income sources go to `## Situation` in `~/Clawic/data/money/memory.md`; an accountant is a person and goes to `~/Clawic/data/contacts/contacts.md`, named here only. Format in `memory-template.md`.
