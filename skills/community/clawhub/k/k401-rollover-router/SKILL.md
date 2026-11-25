---
name: k401-rollover-router
description: Old-401(k) decision engine for job changers — leave it, roll to an IRA, roll to the new plan, or convert to Roth. Compounds the fee-drag difference between plan and IRA over your real horizon, prices a Roth conversion at your actual marginal bracket, encodes the indirect-rollover 20%-withholding trap, the 60-day window, the age-55 separator rule vs 59½, and ERISA creditor-protection differences. Ends the "I have three old 401(k)s and no idea" freeze.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [401k, retirement, rollover, ira, career-change, finance]
---

# k401 Rollover Router

You changed jobs (again). There's a 401(k) sitting at the old employer,
the statement shows a fee you never read, and the default action — do
nothing — quietly bleeds compounding for decades. This skill routes the
decision with your actual numbers.

## When to trigger
- "I left my job, what do I do with my 401(k)?"
- "should I roll my old 401(k) into an IRA or my new employer's plan?"
- "is a Roth rollover worth the tax hit?"
- "my old plan charges 1.1% in fees — does it matter?"
- consolidating multiple stranded accounts from past jobs

## How it works

1. **Collect inputs**: balance, current age, all-in plan fee (basis
   points — check the plan's fee disclosure, "total annual operating
   expense" + per-participant fees), IRA alternative fee (e.g. 3–10 bps
   in broad index funds), expected return, years until withdrawals,
   current marginal tax bracket, expected retirement bracket, state.
2. **Run** `scripts/rollover_router.py --balance 85000 --age 40 \
   --plan-fee-bps 95 --ira-fee-bps 8 --return 6.5 --years-to-draw 22 \
   --bracket-now 24 --bracket-retire 22`
3. **Fee-drag engine**: projects both paths to your draw horizon with
   `balance × [(1+r−f_plan)^N − (1+r−f_ira)^N]` and prints the dollar
   gap at 10/20/30-year marks. 95 bps vs 8 bps on $85k over 22 years is
   real money — the tool names it.
4. **Route matrix** (printed with your numbers filled in):
   - **LEAVE**: makes sense when plan fees are low, funds are good, you
     value ERISA creditor protection / plan loans, or balance is small;
   - **ROLL → new 401(k)**: consolidation with paycheck-savings, keeps
     age-55 rule access and creditor protection, new plan must accept
     incoming rollovers;
   - **ROLL → IRA**: widest fund choice, easiest Roth-conversion ladder
     later, backdoor-Roth cleanliness (watch pro-rata rule!), but loses
     age-55 access, plan loans, and adds RMDs (traditional IRA);
   - **ROLL → Roth (partial)**: priced at `(balance × marginal bracket)`,
     with break-even analysis vs paying tax from the rollover itself
     (never) vs from cash (usually, if bracket now < expected retire
     bracket).
5. **Trap checklist** (always printed):
   - **Direct (trustee-to-trustee) rollover only.** Indirect = 20 %
     federal withholding; you must cover it from pocket within 60 days
     or it's a distribution (tax + 10 % penalty if under 59½);
   - one IRA-to-IRA indirect rollover per 12 months;
   - **age-55 separator rule**: 401(k) withdrawals penalty-free at 55+
     if you left that employer at/after 55 — IRAs make you wait to 59½;
   - state creditor protection is stronger in ERISA plans (sued? 
     bankruptcy?);
   - employer stock in plan (NUA) — do NOT blind-rollover; NUA can save
     a fortune in appreciated stock cases.

## Pitfalls encoded
- The biggest cost is invisible: 0.95 % vs 0.08 % fees on a 22-year
  horizon usually beats every other consideration — the tool makes it a
  printed dollar number instead of a footnote.
- **Never pay conversion tax FROM the rollover** (under 59½: the tax
  withheld is itself an early distribution → penalty).
- Cashing out entirely is almost never right at any age under 55 — the
  tool refuses to model it as a recommendation and shows the damage.

## Examples

```bash
python3 scripts/rollover_router.py --balance 85000 --age 40 \
  --plan-fee-bps 95 --ira-fee-bps 8 --return 6.5 --years-to-draw 22 \
  --bracket-now 24 --bracket-retire 22

# Cheap plan, deciding between leaving and rolling to new employer
python3 scripts/rollover_router.py --balance 42000 --age 35 \
  --plan-fee-bps 12 --ira-fee-bps 8 --return 6.0 --years-to-draw 27 \
  --bracket-now 22 --bracket-retire 22 --new-plan-accepts
```

## Output contract
- fee-drag table ($ gap at 10/20/30 y and at draw horizon)
- ROUTE verdict (LEAVE / ROLL-IRA / ROLL-NEW-PLAN / ROLL-ROTH-PARTIAL)
  with the 2–3 decisive reasons in your numbers
- Roth conversion tax cost + pay-from-cash doctrine
- trap checklist (60-day/20 % withholding, age-55, pro-rata, NUA)
