---
name: layoff-deadline-tracker
description: Use the day a layoff/severance offer lands — extracts the REAL deadline map from the offer letter (COBRA 60-day election vs 45-day notice, 401k loan repayment window before it becomes a distribution + 10% penalty, HSA/FSA use-it-or-lose-it, equity vesting cliff dates, non-compete consideration deadlines) computes severance-vs-notice-pay math, flags the WARN Act 60-day pay rule for group layoffs, and generates the unemployment filing script + benefits-election checklist ordered by what expires first.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [layoff, severance, cobra, unemployment, 401k-loan, career, deadlines]
---

# Layoff Deadline Tracker

A layoff is two events: an emotional shock, and a 60-day administrative
gauntlet where five clocks run simultaneously — COBRA election, 401(k)
loan repayment, equity vesting, benefits end-date, unemployment filing.
Every one of them expires into expensive mistakes: miss the 401(k) loan
window and it converts to a taxed distribution with a 10% penalty;
decline COBRA on day 5 and discover on day 50 that the surgery was
pre-existing in the timeline. This skill reads the offer and builds the
ordered deadline map so nothing expires by neglect.

## When to Use

- You were laid off / given a severance offer / RIF'd / "position
  eliminated" — today or in the last week
- Reviewing a severance agreement (the 21+7 day ADEA consideration
  windows for over-40)
- Deciding: COBRA vs marketplace vs spouse's plan
- You have a 401(k) LOAN outstanding on the employer's plan
- Filing for unemployment and unsure of the timing rules
- Equity (RSUs/options) mid-vest at termination

**Don't use for:** wrongful-termination litigation strategy (employment
attorney); H-1B visa holders facing the 60-day grace clock (immigration
attorney — but the skill will scream that flag); retirement-portfolio
withdrawal planning (a financial planner, not a deadline tool).

## The Method

1. **`map --date 2026-10-16 --state ca --over40`** — builds the dated
   deadline cascade from termination day: benefits end date, COBRA
   election window (60 days from loss OR notice, whichever later) and
   the retroactive-coverage play, unemployment filing (some states
   require a waiting week; file in the FIRST eligible week), 401(k)
   loan repayment window (plan document, often by tax-filing date;
   default = alarm early), equity post-termination exercise windows
   (options often 90 days; RSUs vest-to-date are usually paid out),
   ADEA 21-day consideration + 7-day revocation if 40+.
2. **`severance --offer 14000 --weeks 10 --salary 8400 --notice 0`** —
   severance math: offer vs statutory/notice-pay entitlements, WARN Act
   60-day rule for mass layoffs (100+ employees, plant closures),
   per-week benchmarks, and the "signing fast usually leaves money"
   read with the negotiable-items list.
3. **`cobra --cost 720 --months 18 --events 2500`** — COBRA vs
   marketplace decision: the 60-day election window as a FREE option
   (wait, incur nothing, elect retroactively only if disaster struck),
   subsidy eligibility (marketplace tax credits often beat COBRA for
   lower severance-income years), the surprise-billing gap.
4. **`401kloan --balance 12000 --loan 8000 --age 45 --taxrate 24`** —
   the loan-default trap: what converts to distribution, the tax +
   penalty math, the repayment deadline options (payoff vs roll the
   balance to IRA and repay nobody — depends on plan terms; alarm for
   the plan-document date).
5. **`checklist`** — final-pay items (accrued PTO payout by state),
   references, LinkedIn optics, job-search week-one structure.

Run `python3 scripts/layoff_deadlines.py <cmd> --help`.

## Judgment Rules

- **The COBRA window is an option, not a decision.** You have 60 days
  to elect; coverage is retroactive to the loss date if you do. The
  optimal play is usually: wait, stay uninsured-careful, elect COBRA
  only if a big claim actually happened before day 60. (Electing early
  and paying premiums "to be safe" burns $1,500+/mo for nothing.)
- **Unemployment: file in week one.** Benefits usually start from the
  filing week, not the layoff week; severance timing can affect the
  first checks in some states — file, then reconcile.
- **401(k) loan beats the penalty.** If you can't repay, the balance
  becomes income + 10% penalty if under 59½. A payoff from severance
  or a rollover-into-new-employer-plan negotiation is usually cheaper
  than the tax hit — check the plan document's actual deadline.
- **Over-40 severance: the 21-day consideration period is a floor, not
  a courtesy.** You can sign faster, but the release can't be forced to
  expire sooner; the 7-day revocation after signing means nothing is
  final for a week.
- **Never let the equity window be a surprise.** Post-termination
  option exercise windows are commonly 90 days (sometimes 3 months
  post-"cause" vs post-"without-cause" differ; NSO vs ISO tax treatment
  differs — ISOs exercised after leaving lose ISO status → AMT
  planning needed → loop a CPA before day 90, not after).
- **Keep the layoff letter + the signed release forever.** Unemployment
  offices and future background checks both ask.

## Common Pitfalls

1. Treating COBRA's 60 days as "decide now" — it's a free look; the
   mistake is electing (and paying) when no claims occurred.
2. Missing the 401(k) loan repayment deadline — silent conversion to
   distribution; you discover it as a 1099-R the following January.
3. Filing unemployment "after things settle" — most states don't
   backdate; every delayed week is an unrecoverable check.
4. Rolling the 401(k) into an IRA and THEN taking early withdrawals —
   you lose the age-55 separator rule exception (SEPP/72(t) is the
   only remaining path; see `401kloan` output note).
5. Spending severance as income instead of runway — taxes weren't
   withheld at your marginal blend (supplemental rate is flat 22/37%).
6. Signing the release on day 2 without inventorying equity, PTO
   payouts, and bonus proration that were owed regardless.
7. Letting HSA/FSA money die: FSA is use-it-or-lose-it (some plans
   2.5-month grace), HSA is yours forever but spend the FSA first.

## Verification Checklist

- [ ] Deadline map printed and calendared (paper + phone)
- [ ] Unemployment claim filed in the first eligible week
- [ ] COBRA election form located; decision calendarized at day 45–55
- [ ] 401(k): loan balance known, plan-document deadline in the map,
      distribution-vs-rollover decided deliberately
- [ ] Equity: vested balance, post-termination exercise window, ISO/NSO
      split, CPA looped if options are in the money
- [ ] Severance offer benchmarked; ADEA clock respected if 40+
- [ ] Final pay verified: PTO payout per state rule, last expenses
- [ ] Health records / prescriptions transferred before plan-end
- [ ] Reference letters + LinkedIn updated in week one

## One-Shot Recipe

Laid off 2026-10-16, California, age 47, 10 weeks' severance offered,
$8k 401(k) loan out, surgery scheduled next month:

```bash
python3 scripts/layoff_deadlines.py map --date 2026-10-16 --state ca --over40
python3 scripts/layoff_deadlines.py severance --offer 21000 --weeks 10 \
    --salary 2100 --notice 0
python3 scripts/layoff_deadlines.py cobra --cost 720 --months 18 --events 2500
python3 scripts/layoff_deadlines.py 401kloan --balance 120000 --loan 8000 \
    --age 47 --taxrate 24
```

Then: file unemployment Monday, put the COBRA decision at day 50, and
read the 401(k) plan document's loan section tonight.
